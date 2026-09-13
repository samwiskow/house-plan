"""Export a fresh 3D scene directly from the current measured room polygons."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from house_design_model import load_current_model, roof_surfaces, rooflights, vaulted_ceiling_surfaces, REVISION

source, snapshot = load_current_model()
OUT = Path(__file__).parent / 'model.json'


def read_study(filename):
    return json.loads((ROOT / 'output/pdf' / filename).read_text())


def room_data(room):
    return dict(id=room.id, name=room.name, polygon=room.poly, category=room.category,
                area=round(room.area, 4), dimensions=room.dimensions,
                label=room.lines, labelPoint=room.label)


def door_data(door):
    return dict(id=door.id, x=door.x, y=door.y, width=door.width,
                vertical=door.vertical, kind=door.kind, hingeEnd=door.hinge_end,
                side=door.side, pocketDirection=door.pocket_direction,
                **{'from':door.a, 'to':door.b})


def furniture_data(item):
    return dict(room=item['room'],name=item['name'],rect=item['rect'],kind=item['kind'])


def outdoor_data(data):
    result=[]
    for name, rect, mat, facing in data['outdoor_furniture']:
        kind='table' if 'table' in name.lower() else 'sofa' if 'sofa' in name.lower() else 'diningchair'
        result.append(dict(name=name,rect=rect,material='oak',kind=kind,facing=facing))
    return result


def light_data(data):
    return [dict(id=l['id'],group=l['group'],point=l['point_m'],kind=l['kind'],
                 length=l['length_m'],axis=l['axis']) for l in data['lights']]


def in_rect(x,y,rect):
    a,b,w,d=rect
    return a-1e-6<x<a+w+1e-6 and b-1e-6<y<b+d+1e-6


def window_rect(window):
    axis,x,y,length=window
    # Windows are recorded on the outside wall face in the measured model.
    if axis=='h':
        return [x, y if y==0 else y-.35, length, .35]
    return [x if x in (0,12.2,16.2) else x-.35,y,.35,length]


def wall_solids():
    openings=[]
    for door in source.doors:
        points=door.opening
        xs,ys=zip(*points)
        head=3.1 if door.id=='O05' else 2.6 if door.id in ('O04','O06','O07') else 2.2
        openings.append(([min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)],0,head))
    openings += [(window_rect(w),.82,2.15) for w in source.windows]
    xs={p[0] for r in source.rooms for p in r.poly}|{p[0] for p in source.OUTLINE}
    ys={p[1] for r in source.rooms for p in r.poly}|{p[1] for p in source.OUTLINE}
    xs.update([12.2,16.2,22.8]);ys.update([9.3,12.8])
    for (x,y,w,d),_,_ in openings:
        xs.update((x,x+w));ys.update((y,y+d))
    xs=sorted(set(round(v,5) for v in xs));ys=sorted(set(round(v,5) for v in ys))
    rows=[]
    for y0,y1 in zip(ys,ys[1:]):
        row=[]
        for x0,x1 in zip(xs,xs[1:]):
            x,y=(x0+x1)/2,(y0+y1)/2
            if not source.inside((x,y),source.OUTLINE) or any(source.inside((x,y),r.poly) for r in source.rooms):
                continue
            external=not source.inside((x,y),source.INNER)
            main=x<22.8 and y>=12.8
            height=3.7 if main and external else 3.5 if main else 3.2 if external else 2.6
            if external and 12.2<=x<=16.2 and 9.3<=y<12.8:
                height=2.85+(y-9.3)/3.5*.6
            mat=('timber' if main else 'stone') if external else 'ivory'
            bands=[(0,height)]
            for rect,low,high in openings:
                if not in_rect(x,y,rect):continue
                bands=[part for bottom,top in bands for part in [(bottom,min(top,low)),(max(bottom,high),top)] if part[1]-part[0]>.001]
            for bottom,top in bands:
                key=(round(bottom,4),round(top,4),mat)
                previous=next((b for b in reversed(row) if b['key']==key and abs(b['rect'][0]+b['rect'][2]-x0)<1e-5),None)
                if previous:previous['rect'][2]=x1-previous['rect'][0]
                else:row.append(dict(rect=[x0,y0,x1-x0,y1-y0],key=key))
        rows.extend(row)
    merged=[]
    for item in rows:
        x,y,w,d=item['rect'];key=item['key']
        previous=next((b for b in reversed(merged) if b['key']==key and abs(b['rect'][0]-x)<1e-5 and abs(b['rect'][2]-w)<1e-5 and abs(b['rect'][1]+b['rect'][3]-y)<1e-5),None)
        if previous:previous['rect'][3]=y+d-previous['rect'][1]
        else:merged.append(item)
    return [dict(rect=[round(v,5) for v in b['rect']],bottom=b['key'][0],top=b['key'][1],material=b['key'][2]) for b in merged]


def styled_furniture(item):
    result = furniture_data(item)
    name, kind, room = item['name'].lower(), item['kind'], item['room']
    result['material'] = 'oak'
    if kind in ('bed', 'sofa', 'chair'):
        result['material'] = 'oatmeal'
    if kind in ('basin', 'wc', 'bath'):
        result['material'] = 'porcelain'
    if kind in ('kitchen', 'tall'):
        result['material'] = 'ivory'
    if kind == 'island':
        result['material'] = 'green'
    if kind == 'glass':
        result['material'] = 'glass'
        result['heightM'] = 2.0
    if room == 'S' and kind == 'cabinet':
        result['material'] = 'darkOak'
        result['heightM'] = 2.6
    if kind == 'stove':
        result['material'] = 'charcoal'
    if kind == 'plant':
        result['material'] = 'equipment'
    if kind == 'table':
        result['heightM'] = .75 if 'dining' in name else .43
    if 'wardrobe' in name or 'hanging' in name:
        result['heightM'] = 2.3
    if 'desk' in name or kind == 'desk':
        result['heightM'] = .74
    return result


def main():
    court, lighting, comfort = [read_study(f'concept-{n}-study-check.json') for n in ('09','10','11')]
    walls = wall_solids()
    doors = [door_data(door) for door in source.doors]
    model = {
        'modelVersion': 3, 'revision': REVISION, 'name': 'The courtyard house', 'units': 'metres',
        'metadata': {'giaM2': round(source.polygon_area(source.INNER),2),
                     'externalFootprintM2': round(source.polygon_area(source.OUTLINE),2),
                     'clearRoomM2': round(sum(r.area for r in source.rooms),2),
                     'outerWidthM': 27.15, 'outerDepthM': 18.4, 'briefDate': '2026-09-13'},
        'outline': source.OUTLINE, 'innerEnvelope': source.INNER,
        'rooms': [room_data(room) for room in source.rooms], 'walls': walls, 'doors': doors,
        'windows': [dict(orientation=o,x=x,y=y,length=w) for o,x,y,w in source.windows],
        'furniture': [styled_furniture(f) for f in source.furniture],
        'officeStates': {mode:[styled_furniture(f) for f in state['furniture'] if f['room']=='O'] for mode,state in snapshot['states'].items()},
        'routes': source.routes, 'courtyard': court['court_polygon_m'],
        'paving': court['paving_rectangles_m'],
        'plantingBeds': [dict(name=name,rect=rect) for name,rect in court['planting_beds']],
        'outdoorFurniture': outdoor_data(court), 'lights': light_data(lighting),
        'roofSurfaces': roof_surfaces(), 'rooflight': snapshot['snug_rooflight_reservation_m'],
        'rooflights': rooflights(), 'vaultedCeilingSurfaces': vaulted_ceiling_surfaces(),
        'roofInfill': [
            {'rect':[0,12.8,8.2,.16],'bottom':3.2,'top':3.7,'material':'timber'},
            {'rect':[16.2,12.8,6.6,.16],'bottom':3.2,'top':3.7,'material':'timber'},
            {'rect':[12.2,12.8,4,.14],'bottom':3.45,'top':3.7,'material':'timber'}],
        'wetZones': [[.35,4.47,1.2,1.2],[6.75,2.57,1.1,1.78],[20.35,3.77,1.2,1]],
        'roofHeights': read_study('concept-06b-study-check.json'),
        'shadeReservation': comfort['shade_reservation_m'],
        'ventReservations': comfort['roof_vent_reservations_m'],
        'palette': {'stone':'#d9c8ac','timber':'#ac8155','roof':'#6c6860','ivory':'#eee7da',
                    'oak':'#ba9669','darkOak':'#523c2b','green':'#294d38','oatmeal':'#cbbca4',
                    'porcelain':'#f8f4e9','floor':'#ded3bd','glass':'#a6c1bf','bronze':'#92714e',
                    'charcoal':'#333731','equipment':'#b3b9b4'},
        'status': {'layout':'Current drawn proposal, based on concept 25',
                   'heating':'Wet underfloor heating confirmed',
                   'ventilation':'Two local MVHR units recommended for development; unselected',
                   'roof':'Study heights; low roofs are envelopes without designed falls',
                   'rooflights':'Proposed main-space and family-hall openings; dimensions and shading to develop with the site and PV layout',
                   'site':'Illustrative ground only; no plot or boundary is implied',
                   'furniture':'Measured plan allowances; forms, heights and finishes illustrative'},
    }
    OUT.write_text(json.dumps(model,indent=2)+'\n')
    print(f"Exported {len(model['rooms'])} rooms, {len(walls)} wall runs and {len(doors)} doors")


if __name__ == '__main__':
    main()
