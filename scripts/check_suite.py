"""Check suite circulation against measured plan obstacles."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'studies/l-house-booklet/plans.json'
plans=json.loads(SOURCE.read_text())

def inside(x,y,p):
    c=False
    for a,b in zip(p,p[1:]+p[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
    return c

def box(x,y,w,h):return [[x,y],[x+w,y],[x+w,y+h],[x,y+h]]

checks={}
for option in ['default','enclosed']:
    data=plans[option]
    rooms={r['id']:r for r in data['rooms']}
    bedroom=rooms['U1']['p']
    assert len(bedroom)==4 and all(abs(y-.35)<1e-6 or abs(y-3.65)<1e-6 for x,y in bedroom),'Bedroom must retain its full rectangle'
    assert all(.35<=x<=6.55 and .35<=y<=9.90 for rid in ['U1','U2','U3','UG'] for x,y in rooms[rid]['p'])
    doors={d['id']:d for d in data['doors']}
    assert not {'Landing to dressing','Dressing to bedroom','Bedroom to ensuite'} & doors.keys()
    assert all(name in doors for name in ['Landing to gallery','Gallery to bedroom','Gallery to dressing','Gallery to ensuite'])
    walkable=[r['p'] for r in data['rooms'] if r['floor']=='u']
    for d in data['doors']:
        if d['floor']=='u':walkable.append(box(d['x'],d['y']-.10,d['w'],.20) if d['axis']=='h' else box(d['x']-.10,d['y'],.20,d['w']))
    obstacles=[f['r'] for f in data['furniture'] if f['floor']=='u' and f['kind']!='wet']
    targets={'bedroom':[(5.95,10.5),(5.95,3.05),(4.8,3.05)],'dressing':[(5.95,10.5),(5.95,5.175),(2.7,5.175)],'bathroom':[(5.95,10.5),(5.95,7.75),(2,7.75)],'shower':[(2,7.75),(1.85,9.05)],'WC':[(4.5,7.75),(4.5,8.65)]}
    count=0
    for name,route in targets.items():
        for a,b in zip(route,route[1:]):
            steps=math.ceil(math.dist(a,b)/.05)
            for i in range(steps+1):
                x=a[0]+(b[0]-a[0])*i/steps;y=a[1]+(b[1]-a[1])*i/steps
                for angle in range(32):
                    px=x+.35*math.cos(angle*math.tau/32);py=y+.35*math.sin(angle*math.tau/32)
                    assert any(inside(px,py,p) for p in walkable),(option,name,'wall',px,py)
                    assert not any(rx<px<rx+w and ry<py<ry+h for rx,ry,w,h in obstacles),(option,name,'furniture',px,py)
                count+=1
    fixtures={f['name']:f for f in data['furniture'] if f['roomId']=='U3'}
    assert fixtures['Ensuite shower']['r'][2:]==[3,1.5]
    assert fixtures['Double vanity']['r'][2:]==[1.5,.55]
    assert fixtures['Soaking tub allowance']['r'][2:]==[.85,1.1]
    checks[option]={'700mm_route_samples':count,'routes':list(targets),'doors':'Open; occupied use and hardware not validated'}

windows=plans['suiteDaylight']['windows']
assert any(w['x']==6.725 and w['y']==1.2 and w['w']==2 for w in windows)
assert any(w['x']==6.725 and w['y']==3.9 and w['w']==.9 for w in windows)
assert all(w['y']+w['w']<=5 for w in windows if w['axis']=='v' and w['x']==6.725),'Garden openings must stay on the exposed wall'
for light in plans['suiteDaylight']['rooflights']:
    assert all(inside(x,y,rooms[light['roomId']]['p']) for x,y in box(*light['r']))
result={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'options':checks,'limits':'Sampled plan footprint screening only. No occupied use, daylight, roof, services or construction validation.'}
(ROOT/'studies/l-house-booklet/suite-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
