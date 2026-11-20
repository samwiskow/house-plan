"""Coordinate the L01.1 plan and selected interior without changing either source."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEVELS = {'g': 0, 'u': 3.5, 'a': 0, 'o': 3.0}
HEIGHTS = {'g': 3.2, 'u': 2.7, 'a': 2.7, 'o': 2.7}


def rect(x, y, w, d):
    return [[x, y], [x+w, y], [x+w, y+d], [x, y+d]]


def inside(x, y, poly):
    result = False
    for a, b in zip(poly, poly[1:]+poly[:1]):
        if (a[1] > y) != (b[1] > y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            result = not result
    return result


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(poly, poly[1:]+poly[:1])))/2


def clip(poly, fn):
    out = []
    for a, b in zip(poly, poly[1:]+poly[:1]):
        fa, fb = fn(*a), fn(*b)
        if fa >= -1e-8:
            out.append(a)
        if (fa > 0) != (fb > 0):
            t = fa/(fa-fb)
            out.append([a[0]+t*(b[0]-a[0]), a[1]+t*(b[1]-a[1])])
    return out if len(out) > 2 and area(out) > 1e-8 else []


def subtract_rect(poly, r):
    x, y, w, d = r
    parts = []
    for fn in [lambda a,b:x-a, lambda a,b:a-x-w, lambda a,b:y-b, lambda a,b:b-y-d]:
        p = clip(poly, fn)
        if p:
            parts.append(p)
        poly = clip(poly, lambda a,b:-fn(a,b)) if poly else []
    return parts


def cells(shells, holes):
    xs = sorted({round(x, 7) for p in shells+holes for x,y in p})
    ys = sorted({round(y, 7) for p in shells+holes for x,y in p})
    for x0,x1 in zip(xs,xs[1:]):
        for y0,y1 in zip(ys,ys[1:]):
            x,y = (x0+x1)/2,(y0+y1)/2
            if any(inside(x,y,p) for p in shells) and not any(inside(x,y,p) for p in holes):
                yield [x0,y0,x1-x0,y1-y0]


def load():
    paths = ['studies/l-house-booklet/plans.json', 'studies/l-house-booklet/site.json',
             'output/design/kitchen-selections/boot-room-option.json', 'viewer-l-house/model.json']
    plans, site, option, old = [json.loads((ROOT/p).read_text()) for p in paths]
    data = copy.deepcopy(plans['default'])
    for room in data['rooms']:
        if room['id'] in option['room_polygons']:
            room['p'] = option['room_polygons'][room['id']]
    data['rooms'].append(dict(id='G4',floor='g',name='Utility',p=option['room_polygons']['G4'],label=[14.65,7]))
    data['doors'] = [d for d in data['doors'] if d['id'] not in ['Kitchen to pantry','Kitchen to laundry','Laundry to boot']]
    for name,x,y,axis,w in option['doors']:
        data['doors'].append(dict(id=name,floor='g',x=x,y=y,axis=axis,w=w,side=-1,style='door'))
    data['doors'].append(dict(id='Garden bifolds',floor='g',x=.55,y=.175,axis='h',w=5.8,side=1,style='bifold'))
    data['windows'] = copy.deepcopy(old['windows'])
    for window in data['windows']:
        if window['floor']=='u' and window['axis']=='v' and window['x']==.175 and window['y']==8.65:
            window.update(y=6.75,w=1.3,sill=1.05,head=2.4)
    data['windows'].append(dict(floor='g',axis='h',x=8.35,y=14.625,w=2.1,sill=.45,head=3.08,private=False,id='Stair picture window'))
    data['rooflights'] = copy.deepcopy(plans['suiteDaylight']['rooflights'])
    for rooflight in data['rooflights']:
        if rooflight['id']=='G1':
            rooflight['r'][1]=4.9
            rooflight['status']='Shifted 1.15 m toward bedroom to clear the valley, including flashing'
    for item in data['furniture']:
        if item['roomId']=='U5' and item['kind']=='bed':
            item['r']=[6.85,6.1,2.05,1.3]
        if item['roomId']=='O4' and item['name']=='Office shelves':
            item['r'][1]=18.25
    data['interior_revision']={
        'bath':'Custom hinoki-style ofuro allowance, 1100 x 850 x 740 mm; 610 mm internal depth',
        'bath_reference':'https://www.bartokdesign.com/japan/7-custom_ofuro/square_tub_for_canada.php',
        'shower':'Two overhead and hand shower stations behind the fixed glass; independent central controls on the real rear wall and hinged glass door',
        'shutters':['G5','G7','O4'],
        'bed':'U5 head moved to solid west wall; all headboards checked against windows'}
    for room in data['rooms']:
        if room['id']=='G2':room['p']=[[6.85,5.35],[11.35,5.35],[11.35,7.85],[11.7,7.85],[11.7,9.3],[6.7,9.3],[6.7,6.7],[6.85,6.7]]
        if room['id']=='G3':room.update(name='Walk-in pantry',p=[[11.5,5.35],[13.3,5.35],[13.3,9.3],[11.85,9.3],[11.85,8.0],[11.5,8.0]],label=[12.4,7.5])
    data['doors']=[d for d in data['doors'] if d['id']!='Kitchen → utility']
    pocket_slides={'Gallery to bedroom':-1,'Gallery to dressing':-1,'Gallery to ensuite':1,'Guest shower':1,'Office shower room':1,'Kitchen → pantry':-1,'Utility → pantry':1}
    for door in data['doors']:
        if door['id']=='Hall to kitchen':door.update(x=9.85,w=.95,side=1)
        if door['id']=='Boot to link':door['side']=1
        if door['id']=='Gallery to dressing':door['y']=4.76
        if door['id'] in pocket_slides:door.update(style='pocket',slide=pocket_slides[door['id']],pocketLength=door['w']+.03)
        if door['id']=='Kitchen → pantry':door['style']='concealed'
    for opening in data['openings']:
        if opening[:3]==['g',8.2,11.075]:opening[4]=2.4
        if opening[:3]==['u',9.6,11.075]:opening[1]=8.2
    data['openings'].append(['g',10.675,11.15,'v',3.3])
    for item in data['furniture']:
        if item['name']=='Shower screen left':item['r']=[.35,8.52,1.0,.01]
        if item['name']=='Shower screen right':item['r']=[2.35,8.52,1.0,.01]
    data['finish_revision']={'palette':'Warm ivory, natural oak, linen, pale limestone and muted blue accents',
        'lighting':'Golden hour: 7 degree sun, physical multiple-scattering sky and dim warm lamps',
        'stair_window_m':[2.1,2.63],
        'pantry_door':'Concealed cabinet-front door; closed in kitchen views and open in pantry view',
        'reference_models':['modern_arm_chair_01','wooden_bowl_01','vintage_electric_kettle'],
        'stone_rooms':['G4','G10'],'continuous_parquet':['G1','G2','G3'],
        'pantry_area_m2':round(area(next(r['p'] for r in data['rooms'] if r['id']=='G3')),3),
        'fridge':'Two 600 mm integrated fridge/freezer columns in a recessed bank; generic appliance allowance',
        'stair':'Swapped house flights, open east side, integrated storage under lower flight and large stair window',
        'roof_reference':'https://www.vmzinc.com/en-gb/standing-seam-vmzinc',
        'roof':'Standing-seam zinc appearance; 430 mm panel spacing, 25 mm seams running down each pitch',
        'shower':'Two wall-mounted rain heads, handsets, central wall controls and a 1 m glass door'}
    data['site'] = site
    data['levels'] = LEVELS
    data['heights'] = HEIGHTS
    data['source_hashes'] = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    data['shells'] = {'g':[data['house'],rect(16.2,11.35,2.5,2.4)],'u':[data['house']],
                      'a':[data['garage'],data['plant']],'o':[data['office']]}
    data['stairs'] = [dict(id='House stair',floor='g',upper='u',r=[8.2,11.15,2.4,3.3],risers=18,going=.2875,rise=3.5/18,lower_side=1),
                      dict(id='Garage stair',floor='a',upper='o',r=[19.05,13.35,2.4,3.5],risers=16,going=.30,rise=3/16,lower_side=0)]
    return data


def openings(data, floor):
    out = []
    for d in data['doors']:
        if d['floor']==floor or (floor=='a' and d['id']=='Link to lobby'):
            out.append(dict(d,lo=0,hi=2.4 if d['style']=='bifold' else (2.3 if floor=='g' else 2.15)))
    for f,x,y,axis,w in data['openings']:
        if f==floor:
            out.append(dict(id='Passage',x=x,y=y,axis=axis,w=w,lo=0,hi=3.2 if floor=='g' and (x==6.625 or (axis=='v' and x==10.675) or (axis=='h' and y==11.075 and x==8.2)) else 2.4))
    out.extend(dict(w,lo=w['sill'],hi=w['head'],id='Window') for w in data['windows'] if w['floor']==floor)
    return out


def walls(data, floor):
    shell = data['shells'][floor]
    rooms = [r['p'] for r in data['rooms'] if r['floor']==floor]
    gaps = []
    for d in openings(data,floor):
        r = [d['x'],d['y']-.2,d['w'],.4] if d['axis']=='h' else [d['x']-.2,d['y'],.4,d['w']]
        gaps.append((r,d['lo'],d['hi']))
    for door in data['doors']:
        if door['floor']!=floor or door['style']!='pocket':continue
        length=door['w']+.03;start=(door['x'] if door['axis']=='h' else door['y'])+(door['w'] if door['slide']>0 else -length)
        r=[start,door['y']-.05,length,.10] if door['axis']=='h' else [door['x']-.05,start,.10,length]
        gaps.append((r,0,2.34 if floor=='g' else 2.19))
    xs=sorted({round(x,7) for p in shell+rooms+[rect(*r) for r,_,_ in gaps] for x,y in p})
    ys=sorted({round(y,7) for p in shell+rooms+[rect(*r) for r,_,_ in gaps] for x,y in p})
    rows=[]
    for y0,y1 in zip(ys,ys[1:]):
        row=[]
        for x0,x1 in zip(xs,xs[1:]):
            x,y=(x0+x1)/2,(y0+y1)/2
            if not any(inside(x,y,p) for p in shell) or any(inside(x,y,p) for p in rooms):
                continue
            intervals=[(0,HEIGHTS[floor])]
            for (a,b,w,d),lo,hi in gaps:
                if a-1e-8<=x<=a+w+1e-8 and b-1e-8<=y<=b+d+1e-8:
                    intervals=[q for l,u in intervals for q in [(l,min(u,lo)),(max(l,hi),u)] if q[1]-q[0]>.0001]
            for lo,hi in intervals:
                if row and abs(row[-1][0]+row[-1][2]-x0)<1e-7 and row[-1][4:]==[lo,hi]:
                    row[-1][2]=x1-row[-1][0]
                else:
                    row.append([x0,y0,x1-x0,y1-y0,lo,hi])
        rows+=row
    merged=[]
    for r in rows:
        match=next((s for s in reversed(merged) if abs(s[0]-r[0])<1e-7 and abs(s[2]-r[2])<1e-7 and abs(s[1]+s[3]-r[1])<1e-7 and s[4:]==r[4:]),None)
        if match:
            match[3]+=r[3]
        else:
            merged.append(r)
    return merged


def roof_height(x,y):
    west=6.41+2.05*(1-abs(x-3.45)/3.63)
    east=6.41+2.05*(1-abs(y-9.9)/5.08)
    return west if y<4.82 or x<3.45 else (east if x>7.08 else max(west,east))


def roofs():
    west=lambda x,y:6.41+2.05*(1-abs(x-3.45)/3.63)
    east=lambda x,y:6.41+2.05*(1-abs(y-9.9)/5.08)
    out=[(rect(-.18,-.18,3.63,15.16),west,'House'),(rect(3.45,-.18,3.63,5),west,'House')]
    for y,d in [(4.82,5.08),(9.9,5.08)]:
        p=rect(3.45,y,3.63,d)
        out.extend([(clip(p,lambda x,y:west(x,y)-east(x,y)),west,'House'),(clip(p,lambda x,y:east(x,y)-west(x,y)),east,'House'),(rect(7.08,y,9.3,d),east,'House')])
    for x,y,w,d,eave,ridge,name in [(18.7,11.45,7.2,9.35,5.9,7.75,'Office'),(18.7,7.3,7.2,4.15,2.9,4,'Gym')]:
        fn=lambda a,b,x=x,w=w,eave=eave,ridge=ridge:eave+(ridge-eave)*(1-abs(a-(x+w/2))/(w/2+.15))
        for xx in [x-.15,x+w/2]:
            out.append((rect(xx,y-.15,w/2+.15,d+.3),fn,name))
    out.extend([(rect(16.08,11.23,2.74,2.64),lambda x,y:3.65-(y-11.23)*.07,'Link'),(rect(22.08,4.03,3.94,3.39),lambda x,y:3.1-(y-4.03)*.035,'Plant'),(rect(18.55,20.8,7.5,.55),lambda x,y:3.1-(y-20.8)*.16,'Garage lip')])
    return out
