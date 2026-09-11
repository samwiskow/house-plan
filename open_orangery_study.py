"""Measured open garden-room revision using the retained concept 05 geometry."""
import ast
import copy
import json
import sys
import types
from pathlib import Path

ROOT = Path(__file__).parent
source = ast.parse((ROOT/'plan_model.py').read_text())
cutoff = next(i for i,n in enumerate(source.body) if isinstance(n,ast.Assign)
              and any(isinstance(t,ast.Name) and t.id=='PALETTE' for t in n.targets))
m = types.ModuleType('baseline_plan')
m.__file__ = str(ROOT/'plan_model.py')
sys.modules[m.__name__] = m
# Load model definitions without running the baseline PDF and JSON exports.
exec(compile(ast.Module(body=source.body[:cutoff],type_ignores=[]),str(ROOT/'plan_model.py'),'exec'),m.__dict__)
helpers={'color','text','line','rect','poly','Plan','courtyard','paragraph'}
selected=[]
for node in source.body[cutoff:]:
    if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in helpers:
        selected.append(node)
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('PALETTE','PW') for t in node.targets):
        selected.append(node)
exec(compile(ast.Module(body=selected,type_ignores=[]),str(ROOT/'plan_model.py'),'exec'),m.__dict__)
m.PW,m.PH=420,297
BASELINE=copy.deepcopy((m.rooms,m.doors,m.furniture,m.routes))
before_issues=m.verify()
assert not before_issues,before_issues


def walkable(x,y):
    return any(m.inside((x,y),r.poly) for r in m.rooms) or any(m.inside((x,y),d.opening) for d in m.doors)


removed_wall_probes=[(13.2,12.975),(16.375,10.2),(16.375,12.975)]
assert all(not walkable(*p) for p in removed_wall_probes)
m.R['OR'].poly=m.box(12.55,9.65,4.0,3.5)
m.R['OR'].name='Open garden sitting area'
m.R['OR'].lines=('Garden sitting',)
m.R['OR'].dimensions='4.00 x 3.50 m open zone'
m.R['OR'].label=(14.45,11.8)
m.R['GH'].poly=m.box(16.55,1.99,1.2,7.35)
m.R['GH'].dimensions='1.20 x 7.35 m'
m.R['GH'].label=(17.15,7.15)
m.room('GH2','Shared hall',16.55,9.46,1.2,3.69,'circulation',4.4,
       (17.15,12.35),('Shared','hall'))
m.R['GH2']=m.rooms[-1]
for d in m.doors:
    if d.id=='O05':
        d.x,d.y,d.width,d.kind,d.thickness=12.55,13.15,4.0,'opening',.01
    elif d.id=='D17':
        d.id,d.x,d.y,d.width,d.kind,d.thickness='O07',16.55,9.65,3.5,'opening',.01
for d in m.doors:
    if d.id in ('O02','D12','D14','O07'):
        if d.a=='GH':d.a='GH2'
        if d.b=='GH':d.b='GH2'
m.doors.append(m.Door('D17','GH','GH2',16.7,9.4,.9,False,side=-1))
m.routes['Garden sitting to dining']=[(14.7,12.25),(14.7,13.9),(10.2,13.9)]
m.routes['Guest hall to garden sitting']=[(17.15,10.9),(16.65,11.9),(15.6,12.15)]
assert all(walkable(*p) for p in removed_wall_probes)
assert all(d.kind=='opening' for d in m.doors if d.id in ('O05','O07'))
assert any(d.id=='D17' and d.a=='GH' and d.b=='GH2' for d in m.doors)
for old in BASELINE[0]:
    if old.id not in ('OR','GH'):assert m.R[old.id].poly==old.poly
assert (m.furniture==BASELINE[2])
issues=m.verify()
assert not issues,issues
AFTER=copy.deepcopy((m.rooms,m.doors,m.furniture,m.routes))
OUT=ROOT/'output/pdf'
PDF=OUT/'concept-07-open-garden-room.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm))
m.c.setTitle('Concept 07 - year-round open garden sitting area')
m.c.setAuthor('House plan working study')


def use(state):
    m.rooms,m.doors,m.furniture,m.routes=copy.deepcopy(state)
    m.R={r.id:r for r in m.rooms}


def header(page,title,sub):
    m.text(14,12,'COURTYARD HOUSE / CONCEPT 07 / YEAR-ROUND OPEN GARDEN ROOM',2.7,fill='muted')
    m.text(14,23,title,6.2,font='Helvetica-Bold')
    m.text(14,31,sub,3,fill='muted')
    m.line(14,36,406,36,'#bcc8bf',.3)
    m.line(14,280,406,280,'#bcc8bf',.2)
    m.text(14,287,'DESIGN INTENT | Wall removal and full-width openings subject to structural design. Roof form follows concept 06B.',2.5,fill='muted')
    m.text(406,287,f'{page} / 2',2.6,align='right',fill='muted')


def draw(p,labels=True,include=None):
    saved=m.doors
    m.doors=[d for d in saved if d.id not in ('O05','O07') or d.kind!='opening']
    p.draw(labels=labels,include=include)
    m.doors=saved


def route(p,name):
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'#168271',.4,[2,1])


def outline(p,points):
    for a,b in zip(points,points[1:]+points[:1]):p.line(a,b,'#a46f49',.3,[1.5,1])


use(AFTER)
header(1,'A garden-facing part of the living space','Revised plan 1:100 at A3, printed at 100% | Original exterior footprint and room positions retained')
p=m.Plan(22,62,10)
m.courtyard(p)
draw(p)
for name in ['Garden sitting to dining','Guest hall to garden sitting']:route(p,name)
p.dimension((0,0),(27.15,0),-1.0,'27.15 m overall')
p.dimension((0,0),(0,18.4),-.8,'18.40 m overall',True)
m.text(310,51,'THE CHANGE',3.5,font='Helvetica-Bold')
m.paragraph(310,60,[
 'Remove the internal sliding doors',
 'and wall to the shared room.',
 'Open the wall to the shared hall.',
 'Relocate its door beyond the snug.',
 '',
 'The former orangery becomes an',
 'open, year-round garden sitting',
 'area beside the main living space.'
],step=5.2,size=2.9)
m.text(310,110,'THE CONNECTIONS',3.5,font='Helvetica-Bold')
m.paragraph(310,119,[
 '4.00 m open edge to shared living.',
 '3.50 m open edge to shared hall.',
 'These are wall-removal dimensions;',
 'beam bearings or posts may reduce',
 'the finished clear openings.',
 '',
 'New 0.90 m door across the hall',
 'separates office and guest rooms.',
 'Snug and WC stay on the shared side.'
],step=5.2,size=2.9)
m.text(310,175,'YEAR-ROUND DESIGN',3.5,font='Helvetica-Bold')
m.paragraph(310,184,[
 'Design heating, ventilation and',
 'summer shading together with the',
 'shared room. No internal separating',
 'doors enclose the garden sitting area.',
 '',
 'Low garden-room roof retained as',
 'the current form. The ceiling meets',
 'the taller vault at a broad opening;',
 'its overhead detail is not resolved.'
],step=5.2,size=2.9)
m.paragraph(310,243,[
 f'GIA unchanged: {m.GIA:.2f} m2.',
 f'Footprint unchanged: {m.GEA:.2f} m2.',
 'All nine nominated routes checked.'
],step=5,size=2.9)
p.text(2.5,19.65,'5 m scale bar',2.6,fill='muted')
for a in range(5):p.rect(a,19.9,1,.12,'wall' if a%2==0 else '#ffffff','ink',.12)
m.c.showPage()

header(2,'Open the garden room, close off the guest wing','Before and after at 1:50 on A3 | View orientation matches the plan above')
for state,left,title in [(BASELINE,15,'BEFORE / ENCLOSED ORANGERY'),(AFTER,219,'AFTER / OPEN GARDEN SITTING AREA')]:
    use(state)
    m.text(left,47,title,3.5,font='Helvetica-Bold')
    m.c.saveState()
    clip=m.c.beginPath();clip.rect(left*m.mm,(297-211)*m.mm,186*m.mm,155*m.mm);m.c.clipPath(clip,stroke=0)
    p=m.Plan(left-11.65*20,57-8.1*20,20,True)
    m.courtyard(p,False)
    draw(p,include=['OR','S','WC'])
    if state is AFTER:
        outline(p,m.box(12.55,12.8,4,.35))
        outline(p,m.box(16.2,9.65,.35,3.15))
        route(p,'Garden sitting to dining');route(p,'Guest hall to garden sitting')
        p.text(14.8,14.45,'OPEN SHARED ROOM',3.0)
        p.text(18.55,8.75,'Office beyond',2.8)
        p.text(18.9,9.3,'Relocated hall door',2.8,fill='muted')
        p.line((18.1,9.25),(17.55,9.4),'muted',.2)
    else:
        p.text(14.8,14.45,'SHARED ROOM',3.0)
        p.text(13.6,12.65,'Wall + sliding doors',2.6,fill='muted')
    m.c.restoreState()
    if state is AFTER:
        m.paragraph(left,223,[
          'Brown dashed: former wall positions, removed in this study.',
          'Green dashed: checked routes through the open corner.',
          'Door beyond the snug separates office and guest rooms.'
        ],step=5.5,size=2.8)
    else:
        m.paragraph(left,223,[
          '1.10 m sliding connection to the main shared room.',
          '0.90 m hinged door to the guest hall.',
          'Internal walls make this a separate room.'
        ],step=5.5,size=2.8)
m.line(14,243,406,243,'#bcc8bf',.2)
m.paragraph(15,252,[
 'The hall door is beyond the snug when walking from shared living. It swings toward the office; the existing office door stays.',
 'Full garden-room openings are the intent; beams, bearings and a possible corner post still require structural design.',
 'The 14.00 m2 garden sitting zone includes former wall and doorway-threshold strips. Overall GIA does not increase.',
 'Geometry checks cover room/furniture fit, retained doors and sampled 0.70 m routes; they do not establish structural or environmental performance.'
],step=5.3,size=2.75)
m.c.showPage();m.c.save()
use(AFTER)
(OUT/'concept-07-area-check.json').write_text(json.dumps({
 'baseline':'concept 05; roof direction concept 06B',
 'gia_m2':m.GIA,'external_footprint_m2':m.GEA,
 'garden_sitting_zone_m2':m.R['OR'].area,
 'partitions_and_thresholds_m2':m.GIA-sum(r.area for r in m.rooms),
 'rooms':[{'id':r.id,'name':r.name,'area_m2':round(r.area,4)} for r in m.rooms],
 'shared_and_garden_zones_m2':m.R['KL'].area+m.R['OR'].area,
 'removed_internal_doors':['O05 sliding leaves'],
 'relocated_hall_door':{'id':'D17','width_m':.9,'wall_y_m':9.4,'shared_side':['Snug','WC','Garden sitting'],'private_side':['Office','Guest bedroom','Guest shower']},
 'open_connections':[{'id':d.id,'width_m':d.width} for d in m.doors if d.id in ('O05','O07')],
 'checked_routes':list(m.routes),'checks':issues,
 'baseline_checks':before_issues,'former_wall_probe_count':len(removed_wall_probes),
 'structural_status':'Full openings are design intent; beams, bearings and possible posts are unresolved',
 'year_round_use':True,'garden_room_separating_doors':False
},indent=2)+'\n')
print(PDF)
print(f'{len(m.routes)} routes; {len(issues)} geometry issues; garden zone {m.R["OR"].area:.2f} m2; GIA {m.GIA:.2f} m2')
