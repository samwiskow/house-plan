"""The book and browser use the same current, verified study snapshot."""
import copy
import hashlib
import json
from math import tan, pi
from pathlib import Path

from development_model import load_model

ROOT = Path(__file__).parent
REVISION = 'Design book / 02'


def read_study(number):
    return json.loads((ROOT / f'output/pdf/concept-{number}-study-check.json').read_text())


def load_current_model(mode='Professional'):
    model, _ = load_model()
    data = read_study('24')
    for filename, key in [('library_snug.py', 'source_sha256'),
                          ('two_workspace_office.py', 'office_source_sha256'),
                          ('garden_plant_study.py', 'garden_source_sha256')]:
        assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == data[key], filename
    state = data['model']
    model.rooms = [model.Room(**room) for room in state['rooms']]
    model.R = {room.id: room for room in model.rooms}
    model.doors = [model.Door(**door) for door in state['doors']]
    model.windows = state['windows']
    model.OUTLINE, model.INNER = state['outline'], state['inner']
    for office in data['states'].values():
        for item in office['furniture']:
            if item['room'] == 'O' and item['name'] == 'Personal workspace':
                item['rect'] = [21.7, 7.04, .75, 2.3]
    model.furniture = copy.deepcopy(data['states'][mode]['furniture'])
    model.routes = copy.deepcopy(data['states'][mode]['routes'])
    return model, data


def rooflights():
    lights = [dict(name='Library rooflight', room='S', rect=read_study('24')['snug_rooflight_reservation_m'])]
    lights += [dict(name=name+' rooflight', room='KL', rect=[x, 16.15, .9, 1.2])
               for name, x in [('Living', 3.0), ('Dining', 7.9), ('Kitchen', 11.8)]]
    lights += [dict(name='Family hall rooflight '+str(i+1), room='FH', rect=[3.775, y, .65, .9])
               for i, y in enumerate([6.0, 10.2])]
    for light in lights:
        x, y, w, d = light['rect']
        points = [(x,y), (x+w,y), (x+w,y+d), (x,y+d)]
        pitched = light['room'] == 'KL'
        light['roofVertices'] = [[a,b,3.7+(18.4-b)*tan(pi/6)+.03 if pitched else 3.23] for a,b in points]
        light['ceilingVertices'] = [[a,b,3.5+(18.05-b)*tan(pi/6) if pitched else 2.6] for a,b in points]
    return lights


def surface_with_openings(name, rect, height, openings, material):
    x, y, w, d = rect
    xs = sorted({x,x+w} | {v for a,b,c,e in openings for v in (a,a+c)})
    ys = sorted({y,y+d} | {v for a,b,c,e in openings for v in (b,b+e)})
    result = []
    for a,c in zip(xs,xs[1:]):
        for b,e in zip(ys,ys[1:]):
            mx,my = (a+c)/2,(b+e)/2
            if any(hx < mx < hx+hw and hy < my < hy+hd for hx,hy,hw,hd in openings):
                continue
            result.append(dict(name=name, vertices=[[u,v,height(v)] for u,v in [(a,b),(c,b),(c,e),(a,e)]], material=material))
    return result


def vaulted_ceiling_surfaces():
    height = lambda y: 3.5+min(y-13.15,18.05-y)*tan(pi/6)
    lights = [l['rect'] for l in rooflights() if l['room']=='KL']
    return (surface_with_openings('Shared ceiling courtyard slope', [.35,13.15,17.4,2.45], height, [], 'ivory') +
            surface_with_openings('Shared ceiling arrival slope', [.35,15.6,17.4,2.45], height, lights, 'ivory'))


def roof_surfaces():
    roof = read_study('06b')
    glass = read_study('07b')
    eave = roof['main_roof_eave_m']
    low = roof['lower_envelope_top_m']
    lights = rooflights()
    surfaces = []
    for name, rect, room in [('Family wing roof envelope', [0,0,8.2,12.8], 'FH'),
                              ('Guest roof envelope', [16.2,0,6.6,12.8], 'S'),
                              ('Continuous gym and rear plant roof envelope', [22.8,8.7,4.35,9.7], None)]:
        surfaces += surface_with_openings(name, rect, lambda y: low, [l['rect'] for l in lights if l['room']==room], 'roof')
    surfaces += surface_with_openings('Main roof courtyard slope', [0,12.8,22.8,2.8], lambda y: eave+(y-12.8)*tan(pi/6), [], 'roof')
    surfaces += surface_with_openings('Main roof arrival slope', [0,15.6,22.8,2.8], lambda y: eave+(18.4-y)*tan(pi/6), [l['rect'] for l in lights if l['room']=='KL'], 'roof')
    surfaces += [dict(name=l['name'], vertices=l['roofVertices'], material='glass') for l in lights]
    surfaces.append(dict(name='Garden room glazed roof', vertices=[[12.2,9.3,glass['garden_glass_low_m']], [16.2,9.3,glass['garden_glass_low_m']], [16.2,12.8,glass['garden_glass_high_m']], [12.2,12.8,glass['garden_glass_high_m']]], material='glass'))
    return surfaces


if __name__ == '__main__':
    for mode in ('Professional', 'Personal', 'Night'):
        model, _ = load_current_model(mode)
        issues = model.verify()
        assert not issues, (mode, issues)
        print(f'{mode}: {len(model.routes)} routes, no issues')
