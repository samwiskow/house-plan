"""Concept 16: historical family-wing annexe, declined on 12 September 2026."""
import ast
import copy
import json
from math import ceil, hypot, cos, sin, pi
from pathlib import Path

ROOT=Path(__file__).parent
STATUS='Declined family-wing annexe; investigate laundry and gym-block extension instead'
src=ast.parse((ROOT/'family_rooms_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'family_rooms_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'family_rooms_study.py'),'exec'),s)
m=s['m'];original=copy.deepcopy((m.rooms,m.doors,m.windows));gym=copy.deepcopy([f for f in m.furniture if f['room']=='GY'])
m.furniture=[f for f in m.furniture if f['room']!='ST']
LINEN=(.45,8.14,2.00,.55)
m.furn('ST','Conditional dedicated linen shelving',*LINEN)
m.routes['Linen approach']=[(4.1,7.90),(2.9,7.90),(2.9,7.73),(1.65,7.73)]
del m.routes['Plant approach']
m.routes['Full linen run approach']=[(2.9,7.90),(2.9,7.73),(.85,7.73)]
issues=m.verify();assert not issues,issues
assert (m.rooms,m.doors,m.windows)==original
assert [f for f in m.furniture if f['room']=='GY']==gym
# Candidate annexe is a separate overlay, not an adopted change to the house envelope.
ANNEX_OUTER=(-2.55,6.20,2.55,2.70)
ANNEX_CLEAR=(-2.20,6.55,2.20,2.00)
ANNEX_DOOR=m.Door('D21','OUT','PL',-2.375,6.70,.95,True,side=1,thickness=.35)
EQUIPMENT=[
 {'id':'P1','name':'Cylinder and connections allowance','rect':(-.85,7.65,.80,.80),'height_m':1.85,'base_m':0},
 {'id':'P2','name':'MVHR allowance','rect':(-.60,6.65,.60,.80),'height_m':.90,'base_m':1.10},
 {'id':'P3','name':'Hydraulic / electrical wall allowance','rect':(-2.20,7.80,.25,.65),'height_m':1.10,'base_m':.60}]
SERVICE=[{'id':'P1','rect':(-1.85,7.65,1.0,.80),'basis':'1.0 m planning allowance; selected cylinder access still to verify'},
         {'id':'P2','rect':(-1.60,6.65,1.0,.80),'basis':'1.0 m in front per reference ComfoAir Q installer manual'}]
LOCAL_ROUTES={'MVHR approach':[(-1.8,7.175),(-1.25,7.175),(-1.20,7.05)],
              'Cylinder approach':[(-1.8,7.175),(-1.25,7.175),(-1.25,7.95)]}
rects=[e['rect'] for e in EQUIPMENT]
for i,r in enumerate(rects):
    x,y,w,h=r
    assert all(m.inside(p,m.box(*ANNEX_CLEAR)) for p in [(x+.001,y+.001),(x+w-.001,y+.001),(x+w-.001,y+h-.001),(x+.001,y+h-.001)])
    assert not any(m.overlap(r,o)>1e-8 for o in rects[i+1:])
for area in SERVICE:
    x,y,w,h=area['rect']
    assert all(m.inside(p,m.box(*ANNEX_CLEAR)) for p in [(x+.001,y+.001),(x+w-.001,y+h-.001)])
    assert not any(m.overlap(area['rect'],r)>1e-8 for r in rects)
for name,pts in LOCAL_ROUTES.items():
    for a,b in zip(pts,pts[1:]):
        for j in range(ceil(hypot(b[0]-a[0],b[1]-a[1])/.025)+1):
            t=j/max(1,ceil(hypot(b[0]-a[0],b[1]-a[1])/.025))
            p=(a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]))
            for k in range(16):
                q=(p[0]+.35*cos(k*pi/8),p[1]+.35*sin(k*pi/8))
                assert m.inside(q,m.box(*ANNEX_CLEAR)),(name,q)
                assert not any(m.inside(q,m.box(*r)) for r in rects),(name,q)
assert not any(o=='v' and x==0 and y<8.90 and y+w>6.20 for o,x,y,w in m.windows)
OUT=ROOT/'output/pdf';PDF=OUT/'concept-16-plant-and-linen.pdf'
m.PALETTE.update({'wet':'#e3e9e1','proposed':'#e6edde'})
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 16 - plant location and linen review')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.8,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 16 / PLANT + LINEN',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'HISTORICAL OPTION | Family-wing annexe declined. Investigate laundry / gym-block plant instead. Linen conversion remains conditional.',2.3,fill='muted')
    text(406,287,f'{n} / 3',2.6,align='right',fill='muted')
def tag(p,x,y,label):
    X,Y=p.xy((x,y));m.rect(X-3.5,Y-2.7,7,4.8,'paper','green',.12);text(X,Y+.8,label,2.4,True,align='center',fill='green')
def annex(p):
    p.rect(*ANNEX_OUTER,'green',None);p.rect(*ANNEX_CLEAR,'proposed',None);p.rect(0,6.20,.35,2.70,'wall',None);p.opening(ANNEX_DOOR)
    for a in SERVICE:p.rect(*a['rect'],None,'amber',.3)
    for e in EQUIPMENT:
        p.rect(*e['rect'],'furniture','muted',.15)
        x,y,w,h=e['rect'];tag(p,x+w/2,y+h/2,e['id'])
header(1,'Separate the equipment from the bedding','Location review 1:125 at A3 | Full gym retained | South up / north down / east left / west right')
p=m.Plan(38,54,8);p.draw(labels=False);annex(p)
p.rect(.35,7.27,3.03,1.42,None,'green',.7)
p.text(1.85,7.96,'LINEN',2.3)
p.text(24.8,16.15,'FULL GYM',2.4)
note(275,55,'MOST PROMISING / FAMILY-WING ANNEXE',[
 'An insulated, dry plant room beside the linen store.',
 '2.20 x 2.00 m clear, with external service access.',
 'Near the family bathrooms and existing plant allowance.',
 'Keeps the full gym and fitted utility intact.' ])
note(275,98,'THE ARCHITECTURAL COST',[
 'Adds 2.55 x 2.70 m, or 6.89 m2, to the footprint.',
 'New foundations, walls, door and roof junction.',
 'The plot, boundaries, roof and drainage are unknown.',
 'It is a candidate volume, not an approved extension.' ])
note(275,141,'OTHER LOCATIONS REVIEWED',[
 'Existing store: insufficiently defined for all services.',
 'Utility: would displace the developed laundry joinery.',
 'Gym corner: ruled out by your full-gym preference.',
 'Service-end annexe: longer family hot-water routes.',
 'Roof void: filters and heavy equipment need access.' ])
note(24,219,'WHAT THIS LOCATION DOES - AND DOES NOT - RESOLVE',[
 'The candidate volume does not overlap an existing wall opening in plan.',
 'Only 0.25 m / 0.30 m separates it from the neighbouring window extents; daylight and roof edges need review.',
 'Outdoor heat pump, air terminals and discharge routes are not positioned; the annexe is for indoor equipment.',
 'It preserves existing interior room sizes. The conditional linen layout only applies if relocation is accepted.' ])
note(275,219,'RECOMMENDED NEXT DESIGN CHECK',[
 'Ask the services designer to confirm the plant package,',
 'duct space, maintenance access and hot-water routes.',
 'Then test the candidate against the actual plot',
 'and develop its roof / wall junction.' ])
m.c.showPage()
header(2,'Reserve maintenance space as well as equipment','Candidate plant room plan 1:20 at A3 | 2.20 x 2.00 m clear | Provisional 2.60 m internal height')
p=m.Plan(35+2.55*50,65-6.20*50,50);annex(p)
for name,pts in LOCAL_ROUTES.items():
    for a,b in zip(pts,pts[1:]):p.line(a,b,'green',.3,[1,1])
p.dimension((-2.2,6.55),(0,6.55),-.42,'2.20 m clear')
p.text(-1.22,8.52,'1.0 m front reservations',2.4)
note(220,55,'P1 / HOT-WATER CYLINDER',[
 'Reserve 0.80 x 0.80 m and 1.85 m height as a first fit test.',
 'Reference uniSTOR HP 300: 595 mm body diameter, 1745 mm high.',
 'The reference drawing includes connections beyond the cylinder body.',
 '300 litres is a size reference, not a selected or calculated capacity.',
 'Check expansion vessel, valves, discharge and replacement handling.' ])
note(220,103,'P2 / VENTILATION UNIT',[
 'Reserve 0.80 m along the wall x 0.60 m projection, 0.90 m high.',
 'Reference Q450: 725 x 570 x 850 mm (width x depth x height).',
 'Mounting proposal: base 1.10 m, top 2.00 m; duct space above.',
 'The reference installer manual calls for 1.0 m maintenance space in front.',
 'Airflow capacity, silencers and the full duct assembly remain unverified.' ])
note(220,151,'P3 / CONNECTIONS + CONTROLS',[
 'Reserve a shallow wall area; this does not represent a complete package.',
 'Hydraulics, electrical equipment and pipework need coordinated separation.',
 'Manifolds may need distributed accessible locations elsewhere.',
 'Do not assume a buffer tank, every manifold and all controls fit here.' ])
note(24,219,'SERVICE ACCESS',[
 'Amber outlines are clear floor reservations, not cabinets.',
 'Internal 0.70 m approach envelopes clear the equipment allowances.',
 'D21: 0.95 m external opening allowance; frame / clear width to select.',
 'No plot-side approach, lifting, removal or door-handling test is claimed.' ])
note(220,199,'SITE + CONSTRUCTION TO COORDINATE',[
 'Insulation, frost protection, load-bearing floor and safe drainage.',
 'Duct penetrations, outdoor air separation and noise near bedrooms.',
 'Heat-pump selection, outdoor siting and the distribution strategy.',
 'Provisional equipment heights are not an installation approval.' ])
text(24,258,'Sources: Vaillant uniSTOR HP installation manual, dimensions / siting.',2.5,fill='green')
m.c.linkURL('https://professional.vaillant.co.uk/downloads/aproducts/cylinders-1/unistor/pre-plumbed-unistor-heat-pump-cylinder-slimline-0020221303-00-1044907.pdf',(24*m.mm,35*m.mm,205*m.mm,43*m.mm),relative=0)
text(220,258,'Zehnder Q450 data and ComfoAir Q installer manual, section 2.',2.5,fill='green')
m.c.linkURL('https://zehnder-systems-si.zendesk.com/hc/en-us/article_attachments/4417585038993',(220*m.mm,35*m.mm,405*m.mm,43*m.mm),relative=0)
m.c.showPage()
header(3,'A dedicated linen cupboard with room to reach the shelves','Conditional linen plan and elevation 1:20 at A3 | Only after plant relocation is selected and designed')
p=m.Plan(25-.35*50,67-7.27*50,50)
m.c.saveState();clip=m.c.beginPath();clip.rect(17*m.mm,(297-163)*m.mm,176*m.mm,106*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False)
for name in ['Linen approach','Full linen run approach']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.3,[1,1])
p.text(1.45,8.47,'2.00 m LINEN',2.6);p.text(1.45,7.65,'0.87 m aisle',2.5);m.c.restoreState()
text(225,50,'SHELVING / 2.00 M',3.3,True)
x=225;base=181;sc=50
m.rect(x,base-2.30*sc,2.0*sc,2.30*sc,'ivory','muted',.2)
m.line(x+sc,base-2.3*sc,x+sc,base,'muted',.15)
for z in [.35,.75,1.15,1.55,1.95]:m.rect(x,base-z*sc,2.0*sc,.025*sc,'oak','muted',.12)
text(x+sc,194,'0.55 m depth / five shelf levels',2.7,align='center',fill='muted')
note(24,194,'THE STORAGE GAIN',[
 'Shelf run increases from 0.90 m to 2.00 m.',
 'Depth increases from 0.45 m to 0.55 m for bedding.',
 'Two nominal 1.00 m bays; dividers / boards reduce usable width.',
 'Middle shelves for towels and sheets, lower shelves for bulkier items.',
 'Keep everyday items within comfortable reach; check actual folded stacks.' ])
note(225,216,'ACCESS + LIMITS',[
 'Retain D04 and its swing; keep the shelf end clear of the leaf.',
 f'All {len(m.routes)} house routes pass with the conditional shelving in place.',
 'The full gym and previous room / door / window geometry are unchanged.',
 'Keep the existing plant reservation until relocation is approved.',
 'No new shelf capacity is counted as available in the current design.' ])
m.c.showPage();m.c.save()
(OUT/'concept-16-study-check.json').write_text(json.dumps({
 'status':STATUS,
 'confirmed_preference':'Keep full gym; explore other plant locations',
 'house_geometry_unchanged':True,'gym_furniture_unchanged':True,
 'annexe_is_separate_unadopted_overlay':True,'annexe_outer_m':ANNEX_OUTER,'annexe_clear_m':ANNEX_CLEAR,
 'annexe_added_footprint_m2':6.885,'annexe_door':ANNEX_DOOR.__dict__,
 'equipment_allowances':EQUIPMENT,'service_reservations':SERVICE,'annexe_internal_routes':LOCAL_ROUTES,
 'conditional_linen_rect_m':LINEN,'conditional_house_routes':m.routes,'route_envelope_m':.7,'issues':issues,
 'window_side_gaps_m':[.25,.30],
 'limitations':['Plant capacity and products not selected','No site or boundary verification','No roof / daylight design','No full service distribution or equipment removal test','Linen conversion conditional on relocation'],
 'sources':['https://professional.vaillant.co.uk/downloads/aproducts/cylinders-1/unistor/pre-plumbed-unistor-heat-pump-cylinder-slimline-0020221303-00-1044907.pdf','https://www.zehnder.co.uk/en/indoor-ventilation/solutions/mechanical-ventilation-with-heat-recovery/zehnder-comfoair-q450-st/zehnder-comfoair-q450','https://zehnder-systems-si.zendesk.com/hc/en-us/article_attachments/4417585038993']},indent=2)+'\n')
print(PDF);print(f'{len(m.routes)} conditional house routes and two internal plant approaches pass.')
