"""Concept 18: office day/night use and guest bedroom / shower."""
import ast
import copy
import json
import hashlib
from dataclasses import asdict
from pathlib import Path

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'family_rooms_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'family_rooms_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'family_rooms_study.py'),'exec'),s)
m=s['m'];GEOMETRY=copy.deepcopy((m.rooms,m.doors,m.windows))
m.furniture=[f for f in m.furniture if f['room'] not in ('O','G','GS','GB')]
ITEMS=[('O','Desk / gaming worktop',(18.95,6.29,2.60,.75),'desk'),
 ('O','Working chair reservation',(20.15,7.05,.65,.65),'chair'),
 ('O','Books / equipment',(17.87,6.29,.35,1.40),'cabinet'),
 ('O','Occasional sofa bed closed',(19.35,8.44,2.00,.90),'sofa'),
 ('G','Guest double frame allowance',(20.05,.65,1.65,2.10),'bed'),
 ('G','Guest bedside left',(19.60,.85,.35,.40),'cabinet'),
 ('G','Guest bedside right',(21.85,.85,.35,.40),'cabinet'),
 ('G','Guest hanging wardrobe',(16.55,.35,.60,1.52),'cabinet'),
 ('GS','Luggage and spare bedding',(17.87,3.77,2.36,.50),'cabinet'),
 ('GB','Guest WC',(21.68,3.77,.65,.72),'wc'),
 ('GB','Guest vanity',(21.95,5.42,.50,.70),'basin'),
 ('GB','Guest shower fixed screen',(21.535,3.77,.03,1.00),'glass'),
 ('GB','Guest shower return',(20.35,4.755,.27,.03),'glass')]
for room,name,r,kind in ITEMS:m.furn(room,name,*r,kind)
SHOWER=(20.35,3.77,1.20,1.00)
m.routes.update({
 'Office entry to work':[(17.15,8.65),(18.65,8.65),(18.65,7.8),(19.6,7.8),(19.6,7.5)],
 'Office to window':[(18.65,7.8),(18.85,8.07),(21.8,8.07),(22.02,7.65)],
 'Guest bed left':[(18.4,2.6),(19.25,3.15),(19.65,3.15),(19.65,2.2)],
 'Guest bed right':[(19.65,3.15),(22.08,3.15),(22.08,2.2)],
 'Guest wardrobe':[(18.4,2.6),(18.5,1.4),(17.65,1.4)],
 'Guest shower room':[(17.15,5.6),(19.7,5.6),(20.7,5.6)],
 'Guest shower entry':[(20.7,5.6),(21.1,5.35),(21.1,4.35)],
 'Guest WC approach':[(20.7,5.6),(21.1,5.14),(21.6,5.14),(21.92,5.02)],
 'Guest vanity approach':[(20.7,5.6),(21.5,5.6)]})
DAY_ISSUES=m.verify();assert not DAY_ISSUES,DAY_ISSUES
DAY_FURNITURE=copy.deepcopy(m.furniture);DAY_ROUTES=copy.deepcopy(m.routes)
BED_OPEN=(19.35,7.14,2.00,2.20)
PARKED_CHAIR=(18.28,6.35,.65,.65)
m.furniture=[f for f in m.furniture if f['name'] not in ('Occasional sofa bed closed','Working chair reservation')]
m.furn('O','Sofa bed open frame',*BED_OPEN,'bed');m.furn('O','Chair parked for guests',*PARKED_CHAIR,'chair')
del m.routes['Office entry to work'];del m.routes['Office to window']
m.routes['Office guest left side']=[(17.15,8.65),(18.75,8.65),(18.75,7.75)]
m.routes['Office guest right side to window']=[(21.92,8.65),(21.92,7.65)]
# The open bed blocks a route between its sides; guests use the entry-side edge.
NIGHT_ISSUES=m.verify();assert not NIGHT_ISSUES,NIGHT_ISSUES
NIGHT_FURNITURE=copy.deepcopy(m.furniture);NIGHT_ROUTES=copy.deepcopy(m.routes)
m.furniture=DAY_FURNITURE;m.routes=DAY_ROUTES
assert (m.rooms,m.doors,m.windows)==GEOMETRY
OUT=ROOT/'output/pdf';PDF=OUT/'concept-18-office-and-guests.pdf'
m.PALETTE.update({'wet':'#e3e9e1'})
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 18 - office and overnight guests')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.8,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 18 / OFFICE + GUESTS',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'PROPOSAL | Furniture, fixtures and use envelopes require selection. No accessibility, acoustic or construction compliance claimed. Print at 100%.',2.25,fill='muted')
    text(406,287,f'{n} / 4',2.6,align='right',fill='muted')
def crop(p,r):
    x,y,w,h=r;m.c.saveState();clip=m.c.beginPath();clip.rect(x*m.mm,(297-y-h)*m.mm,w*m.mm,h*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False);m.c.restoreState()
def office(p):
    for r in [(19.3,6.4,.75,.15),(20.2,6.4,.75,.15)]:p.rect(*r,'ink',None)
header(1,'A working office that can host overnight','Office plan 1:25 at A3 | 4.58 x 3.05 m clear | Daily work / gaming for one person')
p=m.Plan(30-17.87*40,68-6.29*40,40);crop(p,(15,54,221,145));office(p)
p.dimension((17.87,6.29),(22.45,6.29),-.35,'4.58 m')
p.text(20.2,6.87,'2.60 m DESK',2.5);p.text(20.35,8.9,'2.00 m SOFA BED',2.5)
for name in ['Office entry to work','Office to window']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line((max(a[0],17.60),a[1]),(max(b[0],17.60),b[1]),'green',.3,[1,1])
note(254,56,'WORKING LAYOUT',[
 '2.60 x 0.75 m desk on the solid south wall.',
 '0.65 m chair reservation shown in use.',
 '1.40 m shallow book / equipment run by entry.',
 '2.00 x 0.90 m closed sofa bed opposite.',
 'West window stays accessible in daily use.' ])
note(254,111,'LIGHT, POWER AND SOUND',[
 'Recess blind for screen glare and guest blackout.',
 'Separate desk task light and dimmable ambient light.',
 'Power / data and accessible cable tray at the desk.',
 'Ventilated equipment storage; avoid heat build-up.',
 'Coordinate sound through the shared snug wall.' ])
note(25,222,'KEEP IT EASY TO CHANGE OVER',[
 'Choose the sofa by its fully open footprint, mattress and mechanism; the drawn 2.00 x 2.20 m envelope is a brief.',
 'Park the task chair in the south-east corner for guests. Store guest bedding in the nearby luggage cupboard.',
 'The next page shows the compromise: with the bed open, the desk cannot be used and only one bed side has an exit route.' ])
m.c.showPage()
header(2,'The open bed fits, with a one-sided night-time route','Office night plan 1:25 at A3 | Sofa-bed envelope 2.00 x 2.20 m | Not simultaneous work and sleeping')
m.furniture=NIGHT_FURNITURE;p=m.Plan(30-17.87*40,68-6.29*40,40);crop(p,(15,54,221,145));office(p)
p.rect(19.65,7.24,1.40,2.00,None,'green',.3)
for a,b in zip(NIGHT_ROUTES['Office guest left side'],NIGHT_ROUTES['Office guest left side'][1:]):p.line((max(a[0],17.60),a[1]),(max(b[0],17.60),b[1]),'green',.35,[1,1])
p.text(20.35,8.3,'1.40 x 2.00 m',2.8);p.text(20.35,8.57,'mattress allowance',2.6)
p.text(18.75,8.03,'EXIT SIDE',2.4);p.text(21.91,8.85,'NO THROUGH',2.0)
note(254,56,'WHAT WORKS',[
 'Room door and its full swing stay clear.',
 'Chair has a drawn parking position.',
 'Entry-side bed approach clears 0.70 m envelope.',
 'Guest shower is reached through the guest hall.',
 'No furniture is moved into the corridor.' ])
note(254,110,'THE COMPROMISE',[
 'Only 0.10 m between desk and open bed end.',
 'Far-side strip has no floor route back to the door.',
 'A second sleeper must cross the mattress to exit.',
 'This may suit occasional children sharing.',
 'It is not a two-sided accessible guest bed.' ])
note(25,223,'FIVE OVERNIGHT GUESTS / ONE EXAMPLE, NOT A UNIVERSAL CAPACITY',[
 'Two guests in the guest double + two sharing the office sofa bed + one visiting child sharing a child-room bed.',
 'That accommodates five visitors without a third sleeper in the sofa bed. Household children keep their rooms.',
 'This could cover four adults and one child, subject to sofa-bed comfort and its one-sided exit; children may share instead.' ])
m.c.showPage()
header(3,'Give the main guest bed access from both sides','Guest bedroom, storage and shower plan 1:30 at A3 | Existing walls, windows and doors retained')
m.furniture=DAY_FURNITURE;p=m.Plan(26-16.2*(1000/30),59,1000/30);crop(p,(20,49,230,224))
p.rect(*SHOWER,'wet','muted',.15)
for f in m.furniture:
    if f['room']=='GB' and f['kind']=='glass':p.rect(*f['rect'],'green','green',.2)
p.text(21.075,1.8,'DOUBLE',2.5);p.text(19.05,4.13,'LUGGAGE / BEDDING',2.2)
p.text(20.9,4.38,'1.20 m SHOWER',2.2)
for name in ['Guest bed left','Guest bed right','Guest wardrobe','Guest shower entry']:
    for a,b in zip(DAY_ROUTES[name],DAY_ROUTES[name][1:]):p.line(a,b,'green',.25,[1,1])
note(266,56,'BEDROOM',[
 '1.65 x 2.10 m double-frame allowance.',
 'Bed head on south wall below existing window.',
 '0.75 m on the narrower west side.',
 '0.90 m between bed foot and north wall.',
 'Retain wardrobe recess and two small bedsides.' ])
note(266,112,'SHOWER ROOM',[
 '1.20 x 1.00 m walkable shower zone.',
 'Fixed glass / entry replace the original placeholder.',
 '0.70 m vanity and separate WC in the room.',
 'Window privacy and wet-zone detailing need design.',
 'Door swing clears the drawn fixtures.' ])
note(266,170,'GUEST COMFORT',[
 'Bedside reading controls and reachable outlets.',
 'Blackout coordinated with headboard / window.',
 'Low-level night lighting toward the shower.',
 'Use the nearby storage for bags and spare bedding.',
 'No wet-room accessibility standard is established.' ])
m.c.showPage()
header(4,'Keep the everyday character; prepare for occasional visits','Interior direction and review points | Warm ivory, honey oak and bronze remain the shared palette')
note(20,55,'OFFICE DESK ELEVATION / 1:25',[
 'Worktop height 0.74 m is a proposal; fit to the actual chair and user.',
 'Monitor heights / arms adjustable. Keep the wall above uncluttered.' ])
x=22;sc=40;base=197
m.rect(x,base-2.3*sc,2.6*sc,2.3*sc,'paper','line',.2)
m.rect(x,base-.74*sc,2.6*sc,.04*sc,'oak','muted',.15)
for xx in [x+14,x+54]:m.rect(xx,base-1.26*sc,30,18,'ink','muted',.2)
text(x+52,209,'2.60 m desk / accessible cables beneath',2.7,align='center')
note(225,55,'DECISIONS STILL TO MAKE',[
 'Choose a sofa bed whose full mechanism fits the envelope.',
 'Accept the one-sided night route or revise the room layout.',
 'Select guest mattress / frame and check actual side clearance.',
 'Confirm adult sofa-bed comfort and any children sharing beds.',
 'Choose shower screen entry, fittings and window treatment.' ])
note(225,119,'VERIFICATION',[
 f'{len(DAY_ROUTES)} daytime routes tested with the working chair present.',
 f'{len(NIGHT_ROUTES)} night routes tested with the open bed and parked chair.',
 'Night far-side strip checked locally; not counted as an exit route.',
 'Room boundaries, doors and windows remain unchanged.',
 'Tests cover geometry, not human comfort or product mechanisms.' ])
note(225,187,'PALETTE AND LIGHTING PROPOSALS',[
 'Ivory walls, oak desk / storage and warm bronze details.',
 'A durable muted green sofa and soft bedroom flooring.',
 'Desk light, room ambient and bedside light on local controls.',
 'Carry cooling and ventilation requirements into both rooms.' ])
m.c.showPage();m.c.save()
(OUT/'concept-18-study-check.json').write_text(json.dumps({'status':'Proposal; office sofa-bed use confirmed, products not selected',
 'model':{'rooms':[asdict(r) for r in m.rooms],'doors':[asdict(d) for d in m.doors],'windows':m.windows,'outline':m.OUTLINE,'inner':m.INNER},
 'model_sources':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['plan_model.py','open_orangery_study.py','shared_space_study.py','arrival_study.py','snug_study.py','suite_study.py','family_rooms_study.py','office_guest_study.py']},
 'day_furniture':DAY_FURNITURE,'night_furniture':NIGHT_FURNITURE,'day_routes':DAY_ROUTES,'night_routes':NIGHT_ROUTES,
 'day_issues':DAY_ISSUES,'night_issues':NIGHT_ISSUES,'geometry_unchanged':True,
 'office_open_bed_m':BED_OPEN,'office_mattress_allowance_m':[1.4,2],'office_night_exit':'Entry side only; far-side sleeper crosses mattress',
 'guest_example':{'guest_double_people':2,'office_sofa_people':2,'child_room_sharing_visitors':1},
 'guest_shower_m':SHOWER,'limitations':['Spatial proposal','One-sided office bed exit','Guest mix is conditional','No occupied bathroom or compliance validation']},indent=2)+'\n')
print(PDF)
