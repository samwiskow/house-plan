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
    data['windows'] = old['windows']
    data['rooflights'] = plans['suiteDaylight']['rooflights']
    data['site'] = site
    data['levels'] = LEVELS
    data['heights'] = HEIGHTS
    data['source_hashes'] = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    data['shells'] = {'g':[data['house'],rect(16.2,11.35,2.5,2.4)],'u':[data['house']],
                      'a':[data['garage'],data['plant']],'o':[data['office']]}
    data['stairs'] = [dict(id='House stair',floor='g',upper='u',r=[8.2,11.15,2.4,3.3],risers=18,going=.2875,rise=3.5/18),
                      dict(id='Garage stair',floor='a',upper='o',r=[19.05,13.35,2.4,3.5],risers=16,going=.30,rise=3/16)]
    return data


def openings(data, floor):
    out = []
    for d in data['doors']:
        if d['floor']==floor or (floor=='a' and d['id']=='Link to lobby'):
            out.append(dict(d,lo=0,hi=2.4 if d['style']=='bifold' else (2.3 if floor=='g' else 2.15)))
    for f,x,y,axis,w in data['openings']:
        if f==floor:
            out.append(dict(id='Passage',x=x,y=y,axis=axis,w=w,lo=0,hi=3.2 if floor=='g' and x==6.625 else 2.4))
    out.extend(dict(w,lo=w['sill'],hi=w['head'],id='Window') for w in data['windows'] if w['floor']==floor)
    return out


def walls(data, floor):
    shell = data['shells'][floor]
    rooms = [r['p'] for r in data['rooms'] if r['floor']==floor]
    gaps = []
    for d in openings(data,floor):
        r = [d['x'],d['y']-.2,d['w'],.4] if d['axis']=='h' else [d['x']-.2,d['y'],.4,d['w']]
        gaps.append((r,d['lo'],d['hi']))
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
