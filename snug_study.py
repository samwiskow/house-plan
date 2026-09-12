"""Concept 13: a furnished snug with shallow storage and local lighting."""
import ast
import copy
import json
from pathlib import Path

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'arrival_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'arrival_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'arrival_study.py'),'exec'),s)
m=s['m'];original=copy.deepcopy((m.rooms,m.doors,m.windows))
m.furniture=[f for f in m.furniture if f['room']!='S']
ITEMS=[
 {'id':'N1','name':'Three-seat sofa allowance','rect':[19.35,11.11,2.30,.90],'height_m':.85,'kind':'sofa'},
 {'id':'N2','name':'Books / toys low storage','rect':[19.15,9.46,2.70,.30],'height_m':.55,'kind':'cabinet'},
 {'id':'N3','name':'Movable upholstered footstool','rect':[20.35,10.56,.50,.50],'height_m':.40,'kind':'table'},
 {'id':'N4','name':'Sofa side table','rect':[21.75,11.51,.40,.40],'height_m':.50,'kind':'table'}]
for it in ITEMS:m.furn('S',it['name'],*it['rect'],it['kind'])
m.routes['Hall to snug sofa']=[(17.15,11.65),(17.15,10.8),(18.5,10.8),(19.75,10.66)]
m.routes['Snug to window']=[(19.75,10.66),(19.75,10.26),(19.75,10.12),(21.6,10.12),(22.02,10.6)]
issues=m.verify();assert not issues,issues
assert (m.rooms,m.doors,m.windows)==original
OUT=ROOT/'output/pdf';PDF=OUT/'concept-13-snug.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm))
m.c.setTitle('Concept 13 - snug, TV and reading')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.4,True);m.paragraph(x,y+8,lines,size=2.9,step=5.3)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 13 / SNUG',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.8,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'PROPOSAL | Furniture, joinery, window hardware, lighting output and finishes require selection. Print at 100% for stated scales.',2.4,fill='muted')
    text(406,287,f'{n} / 2',2.6,align='right',fill='muted')
def dot(p,x,y,label):
    X,Y=p.xy((x,y));m.rect(X-3.3,Y-2.8,6.6,4.8,'paper','green',.15);text(X,Y+.7,label,2.5,True,align='center',fill='green')
header(1,'A comfortable room for films and reading','Furnished plan 1:25 at A3 | 4.58 x 2.60 m clear / 11.91 m2 | South up / north down / east left / west right')
p=m.Plan(42-17.87*40,75-9.46*40,40)
m.c.saveState();clip=m.c.beginPath();clip.rect(14*m.mm,(297-203)*m.mm,234*m.mm,142*m.mm);m.c.clipPath(clip,stroke=0)
p.draw(labels=False)
# Redraw the sofa back on its north edge, facing the storage wall to the south.
p.rect(19.35,11.11,2.3,.9,'furniture','muted',.15)
p.line((19.5,11.79),(21.5,11.79),'muted',.2)
for x in [20.12,20.88]:p.line((x,11.15),(x,11.77),'muted',.12)
p.line((19.25,9.61),(21.75,9.61),'amber',.8)
p.line((19.891,9.49),(21.109,9.49),'ink',1.2)
for it in ITEMS:
    x,y,w,d=it['rect'];dot(p,x+w/2,y+d/2,it['id'])
for name in ['Hall to snug sofa','Snug to window']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.35,[1.3,1])
dot(p,19.53,11.99,'R1');dot(p,21.95,11.95,'R2')
p.text(18.25,9.95,'ENTRY',2.5,fill='muted')
p.text(20.2,10.0,'0.80 m passage',2.3,fill='muted')
m.c.restoreState()
p.dimension((17.87,9.46),(22.45,9.46),-.40,'4.58 m')
p.dimension((22.45,9.46),(22.45,12.06),.36,'2.60 m',vertical=True)
note(267,57,'ONE COMFORTABLE SOFA',[
 'N1: 2.30 x 0.90 m; a nominal three-seat allowance.',
 'Use supportive seats and soft, durable upholstery.',
 'Keep the entry end open, rather than adding a chaise.',
 'Actual arm widths determine usable seating.' ])
note(267,99,'SHALLOW, USEFUL STORAGE',[
 'N2: 2.70 m long and 0.30 m deep.',
 'Books above; closed toys / games storage below.',
 'A centred 55-inch screen is drawn as a size allowance.',
 'Final TV dimensions and mount remain to select.' ])
note(267,141,'A FLEXIBLE MIDDLE',[
 'N3: movable 0.50 m upholstered footstool.',
 'Park it by the sofa for reading; move it for floor play.',
 'N4: a small side table keeps drinks off the floor.',
 'No fixed coffee table or additional armchair.' ])
note(267,183,'WINDOW + PRIVACY',[
 'Retain the 1.50 m west-facing window and room door.',
 'Propose a recess blind to avoid floor-level fabric.',
 'Check handles, opening arc and blind hardware.',
 'The guest-wing door stays beyond the snug.' ])
note(24,219,'CLEARANCES IN THE FURNISHED MODEL',[
 '1.35 m sofa to storage; footstool parked 0.05 m from sofa leaves a 0.80 m passage.',
 'Dashed green: sampled 0.70 m routes to the sofa and window, with the footstool present.',
 f'All {len(m.routes)} whole-house routes and room-door / furniture sweep checks pass.',
 'These checks cover furniture footprints, not occupied seating or selected window hardware.' ])
note(267,229,'WORKING BRIEF',[
 'Confirmed: TV and films, with room to read.',
 'The sofa and screen form the primary arrangement.',
 'No room, door or window geometry changes.' ])
m.c.showPage()
header(2,'Books, soft light and a clear centre','Storage wall looking south and sofa wall looking north at 1:25 | Provisional 2.60 m ceiling | Joinery dimensions are allowances')
# Elevations cover the full 4.58 m room width. Looking south follows plan x.
base=178;sc=40
for x,title in [(20,'A / STORAGE WALL - LOOK SOUTH'),(222,'B / SOFA WALL - LOOK NORTH')]:
    text(x,49,title,3.3,True);m.rect(x,base-2.6*sc,4.58*sc,2.6*sc,None,'line',.2);m.line(x,base,x+4.58*sc,base,'ink',.3)
a=20+(19.15-17.87)*sc
m.rect(a,base-.55*sc,2.7*sc,.55*sc,'ivory','muted',.2)
for k in range(1,5):m.line(a+k*.54*sc,base-.55*sc,a+k*.54*sc,base,'muted',.15)
for z in [1.05,1.45]:
    m.rect(a,base-z*sc,.60*sc,.035*sc,'oak','muted',.12)
    m.rect(a+2.10*sc,base-z*sc,.60*sc,.035*sc,'oak','muted',.12)
m.rect(a,base-1.93*sc,2.7*sc,.035*sc,'oak','muted',.12)
m.line(a+4,base-1.945*sc,a+2.7*sc-4,base-1.945*sc,'amber',.6)
m.rect(a+(1.35-.609)*sc,base-1.343*sc,1.218*sc,.686*sc,'ink','muted',.15)
text(a+1.35*sc,base-1.0*sc,'55-INCH ALLOWANCE',2.6,align='center',fill='ivory')
text(a+1.35*sc,base-.22*sc,'BOOKS / TOYS / GAMES',2.6,align='center')
text(a+1.35*sc,190,'2.70 m storage / 0.30 m depth / 0.55 m base height',2.6,align='center',fill='muted')
# Looking north reverses x, consistent with the plan compass.
b=222+(22.45-21.65)*sc
m.rect(b,base-.85*sc,2.3*sc,.85*sc,'furniture','muted',.2)
m.line(b+4,base-.45*sc,b+2.3*sc-4,base-.45*sc,'muted',.2)
for k in [1,2]:m.line(b+k*2.3*sc/3,base-.70*sc,b+k*2.3*sc/3,base-.12*sc,'muted',.15)
for x,label in [(222+(22.45-19.53)*sc,'R1'),(222+(22.45-21.95)*sc,'R2')]:
    m.line(x,base-1.40*sc,x,base-1.22*sc,'amber',.8);text(x,base-1.52*sc,label,2.6,True,align='center',fill='green')
text(b+1.15*sc,190,'2.30 m sofa allowance; reading lights around 1.40 m',2.6,align='center',fill='muted')
note(20,208,'LIGHTING THAT BELONGS TO THIS ROOM',[
 'Film: general / reading off; low, dimmable storage-wall glow.',
 'Reading: R1 / R2 locally switched, with soft ambient light retained.',
 'Everyday / cleaning: separate dimmable ceiling light; position to test.',
 'Use independent local controls by the latch side of the entry door.',
 '2700 K proposal; assess output and screen reflections after selection.' ])
note(222,208,'MATERIALS + NEXT DECISIONS',[
 'Warm-ivory walls, honey-oak shelves and bronze light fittings.',
 'An olive or moss sofa gives the snug its own identity; sample before choosing.',
 'Consider a fitted wool-rich carpet for a softer feel underfoot.',
 'TV centre approximately 1.00 m high; check against seated eye height.',
 'Allow cable access and equipment ventilation; choose the blind and sofa.' ])
text(20,269,'Viewing reference: Sony minimum-distance guidance. Final screen size and seated viewing comfort remain to test.',2.5,fill='muted')
m.c.linkURL('https://www.sony.co.uk/electronics/support/televisions-projectors/articles/00008601',(20*m.mm,25*m.mm,290*m.mm,32*m.mm),relative=0)
m.c.showPage();m.c.save()
(OUT/'concept-13-study-check.json').write_text(json.dumps({
 'viewing_reference':'https://www.sony.co.uk/electronics/support/televisions-projectors/articles/00008601',
 'status':'TV and films with room to read confirmed; furnishing proposal for review',
 'room_m':{'width':4.58,'depth':2.60,'area':m.R['S'].area},'furniture':ITEMS,
 'routes':m.routes,'route_envelope_m':.70,'issues':issues,
 'room_door_window_geometry_changed':False,'retained_kitchen_utility_door':'D19',
 'clearances_m':{'sofa_to_storage':1.35,'sofa_to_footstool':.05,'storage_to_footstool':.80},
 'tv_allowance':{'diagonal_inches':55,'screen_width_m':1.218,'screen_height_m':.686,'centre_height_m':1.0,'approximate_eye_distance_m':2.0},
 'lighting_proposal':{'ambient':'Concealed warm storage-wall light','reading_points_m':[[19.53,12.01,1.4],[21.95,12.01,1.4]],'general':'Dimmable ceiling light; final location open','colour_temperature_K':2700},
 'limitations':['55-inch screen is a dimensional allowance, not product selection','No occupied-seating, window-swing or joinery-hardware check','No photometric or acoustic calculation','Provisional ceiling and joinery heights']},indent=2)+'\n')
print(PDF);print(f'{len(m.routes)} routes and door sweeps pass.')
