"""Concept 14: parents' bedroom, dressing room and ensuite."""
import ast
import copy
import json
from pathlib import Path

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'snug_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'snug_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'snug_study.py'),'exec'),s)
m=s['m'];original=copy.deepcopy((m.rooms,m.doors,m.windows))
m.furniture=[f for f in m.furniture if f['room'] not in ('P','W','E')]
ITEMS=[]
def item(id,room,name,rect,height,kind='cabinet'):
    m.furn(room,name,*rect,kind);ITEMS.append(dict(id=id,room=room,name=name,rect=rect,height_m=height,kind=kind))
item('B1','P','Super-king frame allowance',(1.15,2.10,1.95,2.15),.60,'bed')
item('B2','P','East bedside',(.65,3.75,.40,.40),.55)
item('B3','P','West bedside',(3.20,3.75,.35,.40),.55)
item('W1','W','Hanging wardrobe wall',(4.76,.35,3.00,.66),2.30)
item('W2','W','Shallow drawers / folded clothes',(5.65,2.10,2.10,.35),.95)
item('E1','E','Double vanity',(4.72,2.57,1.20,.50),.85,'basin')
item('E2','E','WC allowance',(6.00,2.57,.65,.72),.42,'wc')
SHOWER=(6.75,2.57,1.10,1.78)
SCREEN=(6.735,2.57,.03,.88)
# The shower floor is walkable; only its fixed screen is an obstacle.
item('E3','E','Fixed shower screen',SCREEN,2.10,'glass')
m.routes['Suite entry to bed west']=[(4.03,4.85),(4.03,4.0),(3.9,3.2),(3.65,2.5)]
m.routes['Suite around bed to east']=[(3.65,2.5),(3.7,1.65),(.75,1.65),(.75,3.25)]
m.routes['Suite to hanging and drawers']=[(3.7,1.65),(4.15,1.825),(4.9,1.825),(5.30,1.55),(7.35,1.55)]
m.routes['Suite to ensuite vanity']=[(3.9,3.2),(4.15,3.575),(4.9,3.575),(5.2,3.5)]
m.routes['Ensuite WC approach']=[(5.2,3.5),(5.75,3.8),(6.2,3.8)]
m.routes['Ensuite shower entry']=[(6.2,3.8),(7.3,3.8),(7.3,3.05)]
issues=m.verify();assert not issues,issues
assert (m.rooms,m.doors,m.windows)==original

A_STATE=copy.deepcopy((m.rooms,m.doors,m.furniture,m.routes))
m.R['W'].poly=m.box(4.67,.35,3.18,1.40)
m.R['W'].dimensions='3.18 x 1.40 m'
m.R['E'].poly=m.box(4.67,1.87,3.18,2.48)
m.R['E'].dimensions='3.18 x 2.48 m'
m.doors=[d for d in m.doors if d.id!='P01']
m.doors.append(m.Door('D20','P','W',4.61,.80,.85,True,side=-1))
m.furniture=[f for f in m.furniture if f['room'] not in ('W','E')]
B_ITEMS=[
 ('W','Hanging wardrobe wall',(5.16,.35,2.60,.66),'cabinet'),
 ('E','Double vanity',(4.82,1.87,1.20,.50),'basin'),
 ('E','WC allowance',(6.15,1.87,.65,.72),'wc'),
 ('E','Bath allowance',(7.10,1.95,.75,1.70),'bath'),
 ('E','Shower left screen',(5.835,3.35,.03,1.00),'glass'),
 ('E','Shower right screen',(7.035,3.35,.03,1.00),'glass'),
 ('E','Shower front left',(5.865,3.335,.185,.03),'glass'),
 ('E','Shower front right',(6.85,3.335,.185,.03),'glass')]
for room,name,r,kind in B_ITEMS:m.furn(room,name,*r,kind)
m.routes['Suite to hanging and drawers']=[(3.7,1.65),(4.1,1.225),(4.85,1.225),(5.0,1.38),(7.35,1.38)]
m.routes['Suite to ensuite vanity']=[(3.9,3.2),(4.15,3.575),(4.9,3.575),(5.3,2.95)]
m.routes['Ensuite WC approach']=[(5.3,2.95),(6.45,2.96)]
m.routes['Ensuite shower entry']=[(6.45,2.96),(6.45,3.8)]
m.routes['Ensuite bath approach']=[(6.45,2.96),(6.68,2.96)]
b_issues=m.verify();assert not b_issues,b_issues
B_STATE=copy.deepcopy((m.rooms,m.doors,m.furniture,m.routes))
B_DATA={'status':'Declined alternative; Option A selected',
 'ensuite_m':[3.18,2.48],'wardrobe_m':[3.18,1.40],'shower_m':[1.20,1.00],
 'bath_m':[1.70,.75],'double_vanity_width_m':1.20,'wardrobe_aisle_m':.74,
 'wardrobe_hanging_wall_m':2.60,'furniture':B_ITEMS,'routes':m.routes,'issues':b_issues,
 'partition_move_m':.70,'removed_door':'P01','new_door':m.doors[-1].__dict__}
def use(state):
    m.rooms,m.doors,m.furniture,m.routes=copy.deepcopy(state)
    m.R={r.id:r for r in m.rooms}
use(A_STATE)

OUT=ROOT/'output/pdf';PDF=OUT/'concept-14-parents-suite.pdf'
m.PALETTE.update({'wet':'#e3e9e1','linen':'#e7d9bd'})
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 14 - parents suite')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.35,True);m.paragraph(x,y+8,lines,size=2.85,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 14 / PARENTS SUITE',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.8,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'PROPOSAL | A retains room geometry; B changes the suite partition and wardrobe door. Products and construction require design. Print at 100%.',2.4,fill='muted')
    text(406,287,f'{n} / 4',2.6,align='right',fill='muted')
def tag(p,x,y,label):
    X,Y=p.xy((x,y));m.rect(X-3.3,Y-2.7,6.6,4.8,'paper','green',.15);text(X,Y+.8,label,2.5,True,align='center',fill='green')
def double_vanity(p,x,y):
    p.rect(x,y,1.20,.50,'oak','muted',.15)
    for dx in [.07,.67]:p.rect(x+dx,y+.07,.46,.33,'paper','muted',.12)
def details(p):
    double_vanity(p,4.72,2.57)
    p.rect(*SHOWER,'wet','muted',.15)
    p.rect(*SCREEN,'green','green',.2)
    p.line((7.75,2.72),(7.75,4.15),'muted',.18,[.6,.6])
    # Redraw pillows at the north head of the bed.
    p.rect(1.15,2.10,1.95,2.15,'linen','muted',.15)
    p.rect(1.225,2.20,1.80,2.00,None,'muted',.10)
    for x in [1.30,2.20]:p.rect(x,3.75,.70,.35,'paper','muted',.12)
    p.line((1.15,3.55),(3.10,3.55),'muted',.1)
    for it in ITEMS:
        if it['id']=='E3':continue
        x,y,w,d=it['rect'];tag(p,x+w/2,y+d/2,it['id'])
    p.text(7.3,3.10,'SHOWER',2.4)
header(1,'Sleep, dress and get ready without a squeeze','Suite plan 1:40 at A3 | South up / north down / east left / west right | Super king confirmed | Double basins and separate shower take priority over a bath')
p=m.Plan(24,65,25)
m.c.saveState();clip=m.c.beginPath();clip.rect(14*m.mm,(297-188)*m.mm,225*m.mm,140*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False);details(p)
for name in list(m.routes)[-6:]:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.3,[1.2,1])
m.c.restoreState()
p.dimension((.35,.35),(4.55,.35),-.48,'4.20 m bedroom')
p.dimension((4.67,.35),(7.85,.35),-.48,'3.18 m dressing / ensuite')
p.text(2.45,1.05,'BEDROOM / 16.80 m2',2.7)
p.text(6.25,1.65,'1.09 m aisle',2.5)
note(257,56,'BEDROOM / A SOLID HEADBOARD WALL',[
 'Confirmed 1.80 x 2.00 m mattress; allow a 1.95 x 2.15 m frame.',
 'Turn the bed away from the existing south window.',
 'Allow 0.80 m east and 1.45 m west of the frame.',
 'Keep bedside furniture clear of the entrance swing.',
 'Final frame dimensions remain to select.' ])
note(257,103,'DRESSING / ROOM TO USE THE STORAGE',[
 'W1: 3.00 m hanging wall, 0.66 m overall depth.',
 'W2: 2.10 m shallow drawers / shelves, 0.35 m deep.',
 'This leaves 1.09 m between the closed fronts.',
 'Use the shallow side for folded clothes and shoes.',
 'Keep the room-door pocket free of fixings / services.' ])
note(257,150,'ENSUITE / SHOWER-FIRST PROPOSAL',[
 'A 1.10 x 1.78 m shower zone occupies the far end.',
 'A compact 1.20 m double vanity and WC share the south wall.',
 'The shower uses a fixed screen and open entry.',
 'Option A retains the room sizes; Option B tests adding a bath.',
 'Sanitaryware and screen dimensions are allowances.' ])
note(24,204,'WHAT THE FIT TEST TELLS US',[
 f'{len(m.routes)} sampled whole-house routes pass at a 0.70 m envelope, including six new suite routes.',
 'The bed foot has 1.75 m to the south wall; window operation still needs checking.',
 'Room-door sweeps clear proposed fixtures and furniture. The shower screen is a checked obstacle.',
 'Wardrobe drawers, occupied use, frame tolerances and door rescue access are not validated.' ])
note(257,203,'KEEP THE QUIET PART QUIET',[
 'The headboard backs onto the family bathroom.',
 'Coordinate plumbing and the separating wall build-up.',
 'Use individual bedside reading / dimming controls.',
 'Avoid a night-time route through the dressing room.',
 'No acoustic or lighting performance is claimed.' ])
m.c.showPage()
header(2,'A calm bed wall and useful everyday storage','Bedroom head wall looking north and hanging wall looking south at 1:25 | Provisional 2.60 m ceiling')
base=176;sc=40
text(20,49,'A / BED HEAD - LOOK NORTH',3.4,True)
m.rect(20,base-2.6*sc,4.2*sc,2.6*sc,None,'line',.2)
# North elevation reverses x: the entry is on the left.
b=20+(4.55-3.10)*sc
m.rect(b-3,base-1.15*sc,1.95*sc+6,1.15*sc,'linen','muted',.15)
m.rect(b,base-.60*sc,1.95*sc,.60*sc,'furniture','muted',.2)
for x,w in [(20+(4.55-3.55)*sc,.35),(20+(4.55-1.05)*sc,.40)]:m.rect(x,base-.55*sc,w*sc,.55*sc,'oak','muted',.15)
m.rect(20+(4.55-4.48)*sc,base-2.10*sc,.90*sc,2.10*sc,None,'muted',.18)
for x in [20+(4.55-.85)*sc,20+(4.55-3.375)*sc]:
    m.line(x,base-1.35*sc,x,base-1.15*sc,'amber',.7)
text(b+.975*sc,189,'1.95 m frame fit test / low upholstered headboard',2.5,align='center',fill='muted')
text(222,49,'B / HANGING WALL - LOOK SOUTH',3.4,True)
a=222;w=3.0*sc
m.rect(a,base-2.6*sc,3.18*sc,2.6*sc,None,'line',.2)
a+=.09*sc
m.rect(a,base-2.3*sc,w,2.3*sc,'ivory','muted',.2)
for offset in [1.2,2.4]:m.line(a+offset*sc,base-2.3*sc,a+offset*sc,base,'muted',.15)
for start,width in [(0,1.2),(1.2,1.2)]:
    for z in [.95,1.90]:m.line(a+(start+.08)*sc,base-z*sc,a+(start+width-.08)*sc,base-z*sc,'oak',.7)
    text(a+(start+width/2)*sc,base-1.4*sc,'DOUBLE HANG',2.5,align='center')
m.line(a+2.48*sc,base-1.8*sc,a+2.92*sc,base-1.8*sc,'oak',.7)
text(a+2.7*sc,base-1.1*sc,'LONG',2.4,align='center')
text(a+1.5*sc,189,'3.00 m overall / illustrative interiors, fronts omitted',2.5,align='center',fill='muted')
note(20,210,'BEDROOM LIGHT + MATERIALS',[
 'Warm ivory walls, linen headboard, oak bedside furniture and bronze lights.',
 'Propose a wool-rich carpet; use blackout blinds at both bedroom windows.',
 'Each side gets a reading light, accessible socket and independent control.',
 'Separate soft general light from a low-level night route to the ensuite.',
 'Choose the mattress / frame first; bedside heights should follow it.' ])
note(222,210,'DRESSING STORAGE + LIGHT',[
 'Two 1.20 m double-hanging bays and one 0.60 m long-hanging allowance.',
 'Carcasses, dividers, door tracks and clothes reduce usable space.',
 'Sliding fronts on the hanging wall; shallow drawers on the opposite side.',
 'An end-wall mirror and front-facing wardrobe lights support dressing.',
 'A pulled-out drawer temporarily occupies the aisle; test the hardware.' ])
text(20,269,'Depth reference: IKEA PAX / AULI is 0.66 m overall with sliding doors. This is a dimensional reference, not a selected wardrobe.',2.45,fill='muted')
m.c.linkURL('https://www.ikea.com/gb/en/p/pax-auli-wardrobe-with-sliding-doors-white-mirror-glass-s99561351/',(20*m.mm,25*m.mm,390*m.mm,32*m.mm),relative=0)
m.c.showPage()
header(3,'Give the shower the space it needs','Ensuite plan 1:20 and south-wall elevation 1:25 | 3.18 x 1.78 m clear / 5.66 m2 | Option A: double vanity and generous shower')
p=m.Plan(24-4.67*50,66-2.57*50,50)
m.c.saveState();clip=m.c.beginPath();clip.rect(17*m.mm,(297-166)*m.mm,181*m.mm,111*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False)
p.rect(*SHOWER,'wet','muted',.15);p.rect(*SCREEN,'green','green',.2)
double_vanity(p,4.72,2.57)
p.text(7.35,3.05,'1.10 x 1.78 m',2.7);p.text(7.35,3.25,'SHOWER ZONE',2.5)
p.text(6.72,3.95,'0.90 m entry',2.35)
for name in ['Suite to ensuite vanity','Ensuite WC approach','Ensuite shower entry']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.3,[1,1])
m.c.restoreState()
p.dimension((4.67,2.57),(7.85,2.57),-.22,'3.18 m')
text(24,181,'SOUTH WALL / LOOKING SOUTH - 1:25',3.2,True)
a=24;sc=40;base=267
m.line(a,base,a+3.18*sc,base,'ink',.2)
v=a+(4.72-4.67)*sc
m.rect(v,base-.85*sc,1.20*sc,.55*sc,'oak','muted',.2)
m.rect(v+.04*sc,base-1.85*sc,1.12*sc,.80*sc,None,'green',.25)
for x in [v-.08*sc,v+1.28*sc]:m.line(x,base-1.7*sc,x,base-1.2*sc,'amber',.6)
x=a+(6.00-4.67)*sc;m.rect(x,base-.42*sc,.65*sc,.42*sc,'ivory','muted',.2)
x=a+(6.75-4.67)*sc;m.line(x,base-2.10*sc,x,base,'green',.45)
text(x+.55*sc,base-1.25*sc,'WET ZONE',2.5,align='center',fill='muted')
note(225,57,'WATER + WINDOW',[
 'Treat this as a designed wetroom, not a loose tray allowance.',
 'Coordinate floor falls, drainage, waterproofing and ventilation.',
 'The existing courtyard-side window falls inside the shower zone.',
 'Resolve privacy, waterproof reveals, sill and opening hardware.',
 'Screen length and spray containment need product-level testing.' ])
note(225,105,'DAILY USE',[
 'Two basins share a compact 1.20 m vanity allowance.',
 'Choose small basins, useful drawers and mirrored storage.',
 'Fit controls near the shower entry to avoid reaching through spray.',
 'Locate towel storage on the dry side, outside the door sweep.',
 'Choose easy-clean, slip-appropriate surfaces and floor transitions.' ])
note(225,153,'LIGHT + FINISH',[
 'Propose warm ivory / buff porcelain and a honey-oak vanity.',
 'Bronze fittings connect to the rest of the house.',
 'Light the mirror from both sides; separate the low-level night light.',
 'Bathroom electrical zones and suitable fittings require design.',
 'No waterproofing, electrical or accessibility compliance is claimed.' ])
note(225,201,'DECISIONS TO CONFIRM',[
 'Super king, double basins and a generous separate shower are confirmed.',
 'A bath is secondary; see Option B and its dressing-room trade-off.',
 'Final WC, vanity, shower screen and wardrobe hardware.',
 'The geometry fits; it is not a construction-ready bathroom design.' ])
text(225,260,'Wetroom reference: Schluter bathroom and wetroom systems',2.45,fill='green')
m.c.linkURL('https://eu.schluter.com/en-GB/bathroom-wetroom-systems-222.html',(225*m.mm,33*m.mm,406*m.mm,41*m.mm),relative=0)
m.c.showPage()
use(B_STATE)
header(4,'A bath fits, but the dressing room pays for it','Option B: move the ensuite partition 0.70 m towards the wardrobe | Suite plan 1:40 at A3 | Alternative for review, not a selected revision')
p=m.Plan(24,65,25)
m.c.saveState();clip=m.c.beginPath();clip.rect(14*m.mm,(297-188)*m.mm,225*m.mm,140*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False)
p.rect(5.85,3.35,1.20,1.00,'wet','muted',.15)
for room,name,r,kind in B_ITEMS:
    if kind=='glass':p.rect(*r,'green','green',.2)
double_vanity(p,4.82,1.87)
p.rect(1.15,2.10,1.95,2.15,'linen','muted',.15)
for x in [1.30,2.20]:p.rect(x,3.75,.70,.35,'paper','muted',.12)
p.text(6.45,3.95,'1.20 x 1.00',2.3)
p.text(7.48,2.75,'BATH',2.3)
p.text(6.45,1.52,'0.74 m aisle',2.3)
p.line((4.67,2.51),(7.85,2.51),'amber',.45,[1.2,1])
for name in ['Suite to hanging and drawers','Suite to ensuite vanity','Ensuite WC approach','Ensuite shower entry','Ensuite bath approach']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.3,[1.2,1])
m.c.restoreState()
note(257,55,'PRIORITIES RETAINED',[
 'Super-king bed, 1.20 m double vanity and separate shower.',
 'Shower allowance: 1.20 x 1.00 m with 0.80 m entry.',
 'Bath allowance: 1.70 x 0.75 m along the outside wall.',
 'Existing external walls and windows stay in place.' ])
note(257,99,'WHAT CHANGES',[
 'Ensuite grows from 5.66 to 7.89 m2.',
 'Dressing room reduces from 6.68 to 4.45 m2.',
 'Move the shared partition by 0.70 m.',
 'Replace the wardrobe pocket door with relocated D20.',
 'The new hinged door opens into the bedroom.' ])
note(257,148,'THE STORAGE COST',[
 'Hanging wall reduces from 3.00 to 2.60 m.',
 'The 2.10 m shallow drawer / folded-clothes run is lost.',
 'Only 0.74 m remains in front of the wardrobes.',
 'Most dressing would happen in the bedroom.',
 'This is a compact clothes store, not a generous dressing room.' ])
note(24,205,'MY RECOMMENDATION / OPTION A',[
 'Choose A if double basins and a generous shower matter more than an ensuite bath.',
 'It retains the larger 1.10 x 1.78 m shower, useful storage and a 1.09 m dressing aisle.',
 'Option B adds the bath but makes the clothes store and bathroom approaches much tighter.',
 'Amber dashed line: previous partition location. Both layouts retain a bath in the family bathroom.' ])
note(257,205,'FIT CHECK / OPTION B',[
 f'{len(m.routes)} sampled routes and door / furniture sweeps pass.',
 'The shower approach has only about 0.75 m clear depth.',
 'Door / screen frames and actual fixtures may consume that margin.',
 'Do not freeze B without a detailed product and service layout.' ])
use(A_STATE)
m.c.showPage()

m.c.save()
(OUT/'concept-14-study-check.json').write_text(json.dumps({
 'status':'Option A selected; Option B declined because of dressing-room compromises',
 'option_b':B_DATA,'selected_option':'A','recommended_option':'A - double basins and larger shower without ensuite bath',
 'furniture':ITEMS,'shower_walkable_zone_m':SHOWER,'fixed_screen_m':SCREEN,
 'routes':m.routes,'route_envelope_m':.70,'issues':issues,'room_door_window_geometry_changed':False,
 'bed_mattress_fit_test_m':[1.8,2.0],'bed_frame_fit_test_m':[1.95,2.15],
 'clearances_m':{'bed_east':.8,'bed_west':1.45,'bed_foot':1.75,'wardrobe_closed_aisle':1.09,'shower_entry':.90},
 'retained_prior_revisions':['D19 kitchen utility door','Concept 13 snug furniture'],
 'limitations':['Fixture footprints only','No occupied use or joinery drawer-swing verification','No wetroom or electrical design','No selected bed frame','Provisional ceiling and joinery heights'],
 'sources':['https://www.ikea.com/gb/en/p/pax-auli-wardrobe-with-sliding-doors-white-mirror-glass-s99561351/','https://eu.schluter.com/en-GB/bathroom-wetroom-systems-222.html']},indent=2)+'\n')
print(PDF);print(f'{len(m.routes)} routes and door / furniture sweeps pass.')
