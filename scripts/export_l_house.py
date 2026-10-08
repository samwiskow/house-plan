"""Build the L-house scene from the approved booklet's measured snapshots."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'studies/l-house-booklet/plans.json'
plans=json.loads(SOURCE.read_text())
site=json.loads((SOURCE.parent/'site.json').read_text())

def box(x,y,w,h):return [[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
def inside(x,y,p):
    c=False
    for a,b in zip(p,p[1:]+p[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
    return c

def window(floor,axis,x,z,w,sill=.85,head=2.4,private=False):
    return dict(floor=floor,axis=axis,x=x,y=z,w=w,sill=sill,head=head,private=private)
windows=[
 window('g','v',.175,1.4,2.4),window('g','v',.175,5.8,2.2),
 window('g','h',.9,14.625,2.8),window('g','h',5.0,14.625,2.3),
 window('g','h',7.1,5.175,3.2,1.2),window('g','v',16.025,6.3,2,1.2),
 window('g','v',16.025,13.25,.95,1.2),
 window('u','h',.9,14.625,2.8),window('u','h',5.1,14.625,2.4),window('u','h',12,14.625,3),
 window('u','h',7.2,5.175,3.2),window('u','h',11.65,5.175,.8,1.5,2.4,True),
 window('u','h',13.65,5.175,1.6,1.5,2.4,True),window('u','v',16.025,8.9,1.4,1.4,2.4,True),window('u','v',16.025,11.4,2.2),
 window('a','v',18.875,8.1,2.4),window('a','v',25.725,8.1,2.4),window('a','v',25.725,14,1.8,1.2),
 window('o','v',25.725,15.1,3),window('o','h',21.8,20.625,2.6),window('o','v',18.875,18,1.9),window('o','h',23.9,11.625,1,1.5,2.4,True),
]
windows.extend(plans['suiteDaylight']['windows'])
levels={'g':0,'a':0,'u':3,'o':3}

def openings(data,floor):
    out=[]
    for d in data['doors']:
        if levels[d['floor']]==levels[floor]:out.append((d,0,2.15))
    for f,x,z,axis,w in data['openings']:
        if f==floor:out.append((dict(x=x,y=z,axis=axis,w=w),0,2.3 if f=='a' and w>3 else 2.4))
    for win in windows:
        if win['floor']==floor:out.append((win,win['sill'],win['head']))
    return out

def walls(data,floor):
    rooms=[r['p'] for r in data['rooms'] if r['floor']==floor]
    shell={'g':[data['house'],box(16.2,11.35,2.5,2.4)],'u':[data['house']],'a':[data['garage'],data['plant']],'o':[data['office']]}[floor]
    gaps=[]
    for d,lo,hi in openings(data,floor):
        x,z,w=d['x'],d['y'],d['w'];r=[x,z-.19,w,.38] if d['axis']=='h' else [x-.19,z,.38,w]
        gaps.append((r,lo,hi))
    xs={p[0] for poly in shell+rooms for p in poly};zs={p[1] for poly in shell+rooms for p in poly}
    for (x,z,w,h),_,_ in gaps:xs.update([x,x+w]);zs.update([z,z+h])
    xs=sorted(xs);zs=sorted(zs);spans=[]
    for z0,z1 in zip(zs,zs[1:]):
        row=[]
        for x0,x1 in zip(xs,xs[1:]):
            x,z=(x0+x1)/2,(z0+z1)/2
            if not any(inside(x,z,p) for p in shell) or any(inside(x,z,p) for p in rooms):continue
            intervals=[(0,2.7)]
            for (a,b,w,h),lo,hi in gaps:
                if a-1e-7<=x<=a+w+1e-7 and b-1e-7<=z<=b+h+1e-7:
                    intervals=[part for l,u in intervals for part in [(l,min(u,lo)),(max(l,hi),u)] if part[1]-part[0]>.001]
            ext=any(not any(inside(x+dx,z+dz,p) for p in shell) for dx,dz in [(.21,0),(-.21,0),(0,.21),(0,-.21)])
            for lo,hi in intervals:
                if row and abs(row[-1]['rect'][0]+row[-1]['rect'][2]-x0)<1e-7 and row[-1]['bottom']==lo and row[-1]['top']==hi and row[-1]['external']==ext:
                    row[-1]['rect'][2]=x1-row[-1]['rect'][0]
                else:row.append(dict(rect=[x0,z0,x1-x0,z1-z0],bottom=lo,top=hi,external=ext))
        spans.extend(row)
    merged=[]
    for s in spans:
        match=next((p for p in reversed(merged) if p['rect'][0]==s['rect'][0] and abs(p['rect'][2]-s['rect'][2])<1e-7 and abs(p['rect'][1]+p['rect'][3]-s['rect'][1])<1e-7 and p['bottom']==s['bottom'] and p['top']==s['top'] and p['external']==s['external']),None)
        if match:match['rect'][3]+=s['rect'][3]
        else:merged.append(s)
    return [dict(s,floor=floor) for s in merged]

for key in ['default','enclosed']:
    data=plans[key]
    data['doors'].append(dict(floor='g',id='Dining to terrace',x=6.725,y=3.95,axis='v',w=.95,side=1,style='proposed'))
    data['doors'].append(dict(floor='g',id='Living to terrace',x=1.8,y=.175,axis='h',w=2.2,side=1,style='slider'))
    data['walls']=[w for floor in levels for w in walls(data,floor)]
    data['doors'].append(dict(floor='g',id='Kitchen divider',x=6.625,y=6.7,axis='v',w=2.4,side=-1,style='telescopic'))
    data['doors'].append(dict(floor='a',id='Garage door',x=18.875,y=17.25,axis='v',w=3.3,side=1,style='garage'))
    for floor in ['g','u','a','o']:
        source_rooms=[r for r in json.loads(SOURCE.read_text())[key]['rooms'] if r['floor']==floor]
        assert source_rooms==[r for r in data['rooms'] if r['floor']==floor]
model=dict(name='L-house',revision='L01.1 approved suite study',units='metres',levels=levels,
    sourceHash=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),default=plans['default'],enclosed=plans['enclosed'],site=site,windows=windows,
    rooflights=plans['suiteDaylight']['rooflights'],
    stairs=[dict(id='house',x=8.2,z=11.15),dict(id='garage',x=19.05,z=13.35)],
    assumptions=['Roof forms and windows are proposals.','The 40 x 65 m plot and north-side road are assumed.','Floor to floor 3.00 m; clear ceiling 2.70 m.','Furniture and finishes are illustrative.'])
OUT=ROOT/'viewer-l-house/model.json';OUT.write_text(json.dumps(model,separators=(',',':'))+'\n')
print(f'{OUT}: {len(model["default"]["rooms"])} rooms, {len(model["default"]["walls"])} wall solids, two pantry options')
