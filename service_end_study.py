"""Concept 17: compare laundry plant with an extension of the full gym block."""
import ast
import copy
import json
from pathlib import Path
from math import ceil, hypot, cos, sin, pi

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'family_rooms_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'family_rooms_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'family_rooms_study.py'),'exec'),s)
m=s['m']
BASE=copy.deepcopy(m.furniture)
GEOMETRY=copy.deepcopy((m.rooms,m.doors,m.windows))
BASE_ROUTES=copy.deepcopy(m.routes)
A_ITEMS=[('Washer bay',(21.7,12.23,.75,.65)),('Dryer bay',(21.7,12.88,.75,.65)),
 ('P2 ventilation allowance',(21.8,13.58,.65,.75)),('P1 cylinder allowance',(21.55,14.38,.9,.9)),
 ('Air-drying cupboard',(17.87,13.7,.7,.6)),('Relocated sink',(18.62,13.7,.8,.6)),
 ('Reduced folding counter',(19.42,13.7,.65,.6))]
A_SERVICE=[(20.8,13.58,1,.75),(20.55,14.38,1,.9)]
m.furniture=[f for f in BASE if f['room']!='L']
for name,r in A_ITEMS:m.furn('L',name,*r)
A_FURNITURE=copy.deepcopy(m.furniture)
A_ISSUES=m.verify()
assert not A_ISSUES,A_ISSUES
m.furniture=copy.deepcopy(BASE)
EXT_OUTER=(22.45,18.4,4.7,2.6)
EXT_CLEAR=(22.8,18.4,4,2.25)
EXT_DOOR=m.Door('D21','PL','OUT',26.975,19.0,1,True,side=1,thickness=.35)
B_ITEMS=[('P1 cylinder allowance',(22.95,19.7,.9,.9)),
 ('P2 ventilation allowance',(24.20,19.90,.85,.65)),
 ('P3 hydraulic / controls allowance',(25.50,20.15,.65,.45))]
B_SERVICE=[(22.95,18.7,.9,1),(24.20,18.9,.85,1),(25.50,19.15,.65,1)]
B_ROUTES={'Cylinder':[(26.4,19.5),(26.4,19.15),(23.4,19.15)],
 'Ventilation':[(26.4,19.5),(24.6,19.5)],'Controls':[(26.4,19.5),(25.8,19.5)]}
for i,(name,r) in enumerate(B_ITEMS):
    x,y,w,h=r
    assert all(m.inside(p,m.box(*EXT_CLEAR)) for p in [(x+.001,y+.001),(x+w-.001,y+h-.001)])
    assert not any(m.overlap(r,o)>1e-8 for _,o in B_ITEMS[i+1:])
for r in B_SERVICE:
    x,y,w,h=r
    assert all(m.inside(p,m.box(*EXT_CLEAR)) for p in [(x+.001,y+.001),(x+w-.001,y+h-.001)])
    assert not any(m.overlap(r,o)>1e-8 for _,o in B_ITEMS)
for name,pts in B_ROUTES.items():
    for a,b in zip(pts,pts[1:]):
        count=max(1,ceil(hypot(b[0]-a[0],b[1]-a[1])/.025))
        for i in range(count+1):
            p=(a[0]+i/count*(b[0]-a[0]),a[1]+i/count*(b[1]-a[1]))
            for k in range(16):
                q=(p[0]+.35*cos(k*pi/8),p[1]+.35*sin(k*pi/8))
                assert m.inside(q,m.box(*EXT_CLEAR)),(name,q)
                assert not any(m.inside(q,m.box(*r)) for _,r in B_ITEMS),(name,q)
assert not m.verify()
assert (m.rooms,m.doors,m.windows)==GEOMETRY
assert m.routes==BASE_ROUTES
OUT=ROOT/'output/pdf';PDF=OUT/'concept-17-service-end-comparison.pdf'
m.PALETTE.update({'proposed':'#e6edde','amber':'#af743b'})
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm))
m.c.setTitle('Concept 17 - service-end comparison')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.8,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 17 / SERVICE END',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'COMPARISON ONLY | No option selected. Equipment, maintenance and envelope dimensions are planning allowances. Print at 100%.',2.35,fill='muted')
    text(406,287,f'{n} / 4',2.6,align='right',fill='muted')
def crop(p,rect):
    x,y,w,h=rect;m.c.saveState();clip=m.c.beginPath();clip.rect(x*m.mm,(297-y-h)*m.mm,w*m.mm,h*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False);m.c.restoreState()
def extension(p):
    p.rect(*EXT_OUTER,'green',None);p.rect(*EXT_CLEAR,'proposed',None);p.opening(EXT_DOOR)
    for r in B_SERVICE:p.rect(*r,None,'amber',.25)
    for name,r in B_ITEMS:
        p.rect(*r,'furniture','muted',.15);x,y,w,h=r;p.text(x+w/2,y+h/2,name[:2],2.7)
header(1,'Keep the gym; compare what happens to the laundry','Both options 1:60 at A3 | South up / north down / east left / west right | Amber = maintenance floor reservation')
text(18,49,'A / REWORK THE EXISTING LAUNDRY',3.5,True)
m.furniture=A_FURNITURE;p=m.Plan(18-17.5*(1000/60),62-11.7*(1000/60),1000/60);crop(p,(16,58,185,198))
for r in A_SERVICE:p.rect(*r,None,'amber',.3)
p.text(24.7,15.8,'24 m2 GYM',3);p.text(19.1,14.1,'SINK / FOLD',2.2)
p.text(22,14.8,'P1',2.7);p.text(22.1,13.98,'P2',2.7)
text(222,49,'B / EXTEND THE EXISTING GYM BLOCK',3.5,True)
m.furniture=BASE;p=m.Plan(222-17.5*(1000/60),62-11.7*(1000/60),1000/60);crop(p,(220,58,187,198));extension(p)
p.text(24.7,15.8,'24 m2 GYM',3);p.text(24.7,18.72,'9 m2 PLANT',2.7)
p.dimension((22.8,20.65),(26.8,20.65),.8,'4.00 m clear')
text(18,264,'A: no added footprint; laundry functions reduced; P3 unresolved.',2.8)
text(222,264,'B: +12.22 m2 footprint; full laundry and gym retained.',2.8)
m.c.showPage()
header(2,'The laundry fit comes with a real loss of working space','Option A plan 1:25 at A3 | Side-by-side machines retained | A fit test, not a complete services solution')
m.furniture=A_FURNITURE;p=m.Plan(25-17.75*40,61-12.05*40,40);crop(p,(20,55,194,151))
for r in A_SERVICE:p.rect(*r,None,'amber',.35)
for name,r in A_ITEMS:
    if name.startswith('P'):x,y,w,h=r;p.text(x+w/2,y+h/2,name[:2],3)
p.dimension((20.22,12.18),(21.7,12.18),-.28,'1.48 m closed aisle')
note(232,56,'WHAT STILL FITS',[
 'Two 0.65 m appliance bays, side-by-side.',
 'Existing 0.70 m air-drying cupboard.',
 '0.80 m sink relocated to the folding run.',
 'D19 and boot-room pocket access retained.',
 'Existing house routes and door sweeps pass.' ])
note(232,103,'WHAT IS LOST OR UNRESOLVED',[
 'Folding run falls from 1.45 m to 0.65 m.',
 'The 0.95 m sorting / detergent drawers disappear.',
 'P1 and P2 maintenance occupies the working aisle.',
 'No equivalent P3 wall / service zone is resolved.',
 'Plant enclosure, ducts and separation add space.' ])
note(25,218,'ASSESSMENT / DOES NOT MEET THE FULL BRIEF YET',[
 'The plant bodies can be drawn in; the same laundry function and full plant package cannot yet be retained.',
 'Stacking might recover a bay, but is a fallback and has not been used to make this option appear equivalent.',
 'A shared utility still requires acoustic treatment toward the snug, moisture control and replacement planning.',
 'The 0.90 m cylinder reservation is not a selected capacity. Keep the family-wing plant placeholder for now.' ])
m.c.showPage()
header(3,'A separate compartment preserves both working rooms','Option B plant plan 1:25 at A3 | External access | Existing gym wall and all gym equipment retained')
m.furniture=BASE;p=m.Plan(28-22.45*40,64-18.05*40,40);crop(p,(24,49,195,31));extension(p)
p.dimension((22.8,20.65),(26.8,20.65),.8,'4.00 m clear')
p.dimension((22.8,18.4),(22.8,20.65),-.52,'2.25 m clear',True)
for pts in B_ROUTES.values():
    for a,b in zip(pts,pts[1:]):p.line(a,b,'green',.25,[1,1])
note(255,54,'TESTED RESERVATIONS',[
 'P1: 0.90 x 0.90 m cylinder / connections bay.',
 'P2: 0.85 x 0.65 m wall ventilation bay.',
 'P3: 0.65 x 0.45 m hydraulics / controls bay.',
 'Each has a 1.00 m front floor reservation.',
 'Internal 0.70 m approach envelopes pass.' ])
note(255,110,'ADDED VOLUME',[
 '4.70 x 2.60 m extension; 12.22 m2 footprint.',
 '4.00 x 2.25 m clear; 9.00 m2 plant floor.',
 'Extends the block north (down on the plan).',
 '1.00 m door opening on the west outer wall.',
 'No new passage through the gym is assumed.' ])
note(25,211,'SECTION INTENT / CONTINUE THE LOWER GYM ROOF',[
 'Reserve 2.60 m clear below a provisional 3.20 m external roof top, matching the existing lower-block direction.',
 'Reserve P1 height up to 2.10 m; P2 base 1.00 m / top 1.95 m, leaving 0.65 m above for coordination.',
 'These heights do not establish a duct / silencer fit or roof build-up. Falls, outlets, structure and loads need design.',
 'The door-side external landing, boundaries and complete removal route depend on the actual site.' ])
m.c.showPage()
header(4,'Develop B first; retain the existing plant reservation meanwhile','Recommendation for design development | Neither option adopted | Same household and services brief for both')
note(20,53,'WHY B IS THE STRONGER START',[
 'Preserves the fitted laundry, side-by-side machines and full 4 x 6 m gym.',
 'Gives equipment an external service door without taking it through the house.',
 'Keeps plant toward the service end as requested.',
 'Costs additional footprint and a coordinated extension of the roof.' ])
note(220,53,'LINEN GAIN IS CONDITIONAL',[
 'Current concept 15: 0.90 x 0.45 m shelving plus retained plant.',
 'After successful relocation: test 2.00 x 0.55 m linen shelving.',
 'The old annexe location stays declined.',
 'Do not count that larger linen run in the current storage total.' ])
note(20,113,'DESIGN THE COMPLETE PACKAGE',[
 'Heating / hot water, MVHR and active cooling are separate duties.',
 'No selected cylinder capacity, heat-pump output or airflow is implied.',
 'Allow for valves, expansion, silencers, pipe insulation and local manifolds.',
 'Outdoor units, battery / inverter and cooling units remain unpositioned.',
 'Compare hot-water routes to the distant family bathrooms and service noise.' ])
note(220,113,'WHAT THE SPATIAL CHECKS ESTABLISH',[
 f'{len(BASE_ROUTES)} retained house routes pass in A and B.',
 'Both retain the full gym and existing house doors / windows.',
 'B has three clear internal approaches and equipment service zones.',
 'No occupied laundry or complete equipment-removal test is claimed.',
 'No heat loss, cooling load, acoustics or site compliance is calculated.' ])
note(20,181,'DIMENSION REFERENCES / CHECKED 13 SEPTEMBER 2026',[
 'Vaillant 2024 heat-pump cylinder brochure: 300 L reference body 595 mm diameter / 1745 mm high.',
 'Our larger allowance includes provisional connection space; 300 L is not selected or sized for the household.',
 'Zehnder ComfoAir Q450 product page is a ventilation reference only; no Q450 capacity selection is made.',
 'All front access and enclosure dimensions on these drawings are our planning allowances, not supplier approval.' ])
for y,label,url in [(218,'Vaillant cylinder dimensional reference','https://professional.vaillant.co.uk/downloads/aproducts/unistor-500-800l/vaillant-heat-pump-cylinder-brochure-2024-1198831.pdf'),(228,'Zehnder ventilation reference','https://www.zehnder.co.uk/en/indoor-ventilation/solutions/mechanical-ventilation-with-heat-recovery/zehnder-comfoair-q450-st/zehnder-comfoair-q450')]:
    text(20,y,label,2.8,fill='green');m.c.linkURL(url,(20*m.mm,(297-y-2)*m.mm,200*m.mm,(297-y+4)*m.mm),relative=0)
text(20,253,'Next decision: select a location direction after reviewing the added volume and laundry compromise.',3.2,True)
m.c.showPage();m.c.save()
(OUT/'concept-17-study-check.json').write_text(json.dumps({
 'status':'Comparison for review; no option adopted','recommended_for_development':'B',
 'A':{'furniture':A_ITEMS,'service_floor':A_SERVICE,'issues':A_ISSUES,'full_package_resolved':False,'folding_width_m':.65,'sorting_drawers_retained':False},
 'B':{'outer':EXT_OUTER,'clear':EXT_CLEAR,'added_footprint_m2':12.22,'clear_area_m2':9,'equipment':B_ITEMS,'service_floor':B_SERVICE,'internal_routes':B_ROUTES,'door':EXT_DOOR.__dict__},
 'retained_house_route_count':len(BASE_ROUTES),'gym_unchanged':True,'house_geometry_unchanged':True,'linen_conversion_adopted':False,
 'limitations':['Provisional equipment and access allowances','No complete equipment removal check','No site or boundary validation','No heating cooling airflow or energy sizing']},indent=2)+'\n')
print(PDF)
print('Both house scenarios and three B internal approaches pass; A has recorded functional shortfalls.')
