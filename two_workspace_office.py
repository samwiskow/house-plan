"""Concept 23: professional and personal workspaces plus occasional guests."""
import copy
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,BASE_DATA=load_model()
GARDEN=json.loads((ROOT/'output/pdf/concept-22-study-check.json').read_text())
assert hashlib.sha256((ROOT/'garden_plant_study.py').read_bytes()).hexdigest()==GARDEN['source_sha256'],'Rebuild garden_plant_study.py'
state=GARDEN['model'];m.rooms=[m.Room(**r) for r in state['rooms']];m.R={r.id:r for r in m.rooms};m.doors=[m.Door(**d) for d in state['doors']]
m.windows=state['windows'];m.OUTLINE=state['outline'];m.INNER=state['inner'];m.furniture=copy.deepcopy(GARDEN['furniture']);m.routes=copy.deepcopy(GARDEN['routes'])
GEOMETRY=copy.deepcopy((m.rooms,m.doors,m.windows))
OTHER_FURNITURE=copy.deepcopy([f for f in m.furniture if f['room']!='O'])
m.furniture=copy.deepcopy(OTHER_FURNITURE)
ITEMS=[('Professional workspace',(20.85,6.29,1.60,.75),'desk'),
 ('Personal workspace',(21.70,7.54,.75,1.80),'desk'),
 ('Sofa bed closed',(17.87,6.29,.90,1.90),'sofa'),
 ('Shallow books / small items',(19.00,9.04,1.20,.30),'cabinet')]
for name,r,kind in ITEMS:m.furn('O',name,*r,kind)
FIXED=copy.deepcopy(m.furniture)
CHAIRS={'Professional':(20.93,7.12,.65,.65),'Personal':(20.93,8.10,.65,.65),'Night':(20.93,8.60,.65,.65)}
m.routes={name:pts for name,pts in m.routes.items() if not name.startswith('Office ')}
NON_OFFICE_ROUTES=copy.deepcopy(m.routes)
WORK_ROUTES={'Office entry to work':[(17.15,8.65),(19.1,8.65),(20.45,8.65),(20.45,7.5)],
 'Office personal setup approach':[(20.45,8.65),(20.45,8.25)]}
WORK_STATES={}
for mode in ['Professional','Personal']:
    m.furniture=copy.deepcopy(FIXED);m.furn('O','One task chair',*CHAIRS[mode],'chair')
    m.routes=copy.deepcopy(NON_OFFICE_ROUTES);m.routes.update(WORK_ROUTES)
    issues=m.verify();assert not issues,(mode,issues)
    WORK_STATES[mode]={'furniture':copy.deepcopy(m.furniture),'routes':copy.deepcopy(m.routes),'issues':issues}
OPEN_BED=(17.87,6.29,2.20,1.90)
MATTRESS=(17.97,6.54,2.00,1.40)
m.furniture=[f for f in FIXED if f['name']!='Sofa bed closed'];m.furn('O','Open sofa bed frame',*OPEN_BED,'bed');m.furn('O','Task chair parked',*CHAIRS['Night'],'chair')
m.routes=copy.deepcopy(NON_OFFICE_ROUTES)
m.routes['Office wall-side sleeper foot exit']=[(20.45,6.90),(20.45,8.65),(19.1,8.65),(17.15,8.65)]
m.routes['Office room-side sleeper foot exit']=[(20.45,7.65),(20.45,8.65),(19.1,8.65),(17.15,8.65)]
NIGHT_ISSUES=m.verify();assert not NIGHT_ISSUES,NIGHT_ISSUES
NIGHT={'furniture':copy.deepcopy(m.furniture),'routes':copy.deepcopy(m.routes),'issues':NIGHT_ISSUES}
assert (m.rooms,m.doors,m.windows)==GEOMETRY
assert [f for f in m.furniture if f['room']!='O']==OTHER_FURNITURE
m.furniture=copy.deepcopy(WORK_STATES['Professional']['furniture']);m.routes=copy.deepcopy(WORK_STATES['Professional']['routes'])
OUT=ROOT/'output/pdf';PDF=OUT/'concept-23-two-workspace-office.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 23 - professional and personal office')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.75,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 23 / TWO WORKSPACES',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'OFFICE PROPOSAL | One person switching between setups. Actual furniture, mechanisms, window operation and clearances remain to select.',2.3,fill='muted')
    text(406,287,f'{n} / 4',2.6,align='right',fill='muted')
def crop(p):
    m.c.saveState();clip=m.c.beginPath();clip.rect(16*m.mm,(297-204)*m.mm,224*m.mm,150*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False);m.c.restoreState()
def desktops(p):
    for r in [(20.95,6.42,.60,.12),(21.65,6.42,.60,.12),(22.18,7.95,.12,.80)]:p.rect(*r,'ink',None)
    p.text(21.65,6.9,'PROFESSIONAL',2.35)
    X,Y=p.xy((22.10,8.7));m.c.saveState();m.c.translate(X*m.mm,(297-Y)*m.mm);m.c.rotate(90);m.c.setFont('Helvetica',2.35*m.mm);m.c.setFillColor(m.color('ink'));m.c.drawString(0,0,'PERSONAL');m.c.restoreState()
def route(p,points):
    for a,b in zip(points,points[1:]):p.line((max(a[0],17.58),a[1]),(max(b[0],17.58),b[1]),'green',.35,[1,1])
header(1,'Two dedicated setups, with one chair between them','Office plan 1:25 at A3 | 4.58 x 3.05 m clear | Professional-work mode shown')
p=m.Plan(30-17.87*40,70-6.29*40,40);crop(p);desktops(p)
p.rect(17.87,6.29,.90,1.90,'furniture','muted',.15);p.line((18.08,6.44),(18.08,8.04),'muted',.15)
p.text(18.33,7.25,'SOFA',2.5);p.text(19.6,9.25,'BOOKS',2.3)
route(p,WORK_ROUTES['Office entry to work'])
p.dimension((17.87,6.29),(22.45,6.29),-.37,'4.58 m')
note(256,55,'PROFESSIONAL WORKSPACE',[
 '1.60 x 0.75 m desk on the solid south wall.',
 'Illustrated with two screens; actual devices to select.',
 'Leave the setup connected and ready for work.',
 'Provide accessible power / data and task light.' ])
note(256,103,'PERSONAL WORKSPACE',[
 '1.80 x 0.75 m desk along the west wall.',
 'Separate keyboard, screens and personal equipment.',
 'One task chair moves between the two stations.',
 'Check monitor glare and the existing window blind.' ])
note(256,151,'SEATING AND STORAGE',[
 '1.90 x 0.90 m closed sofa bed along the opposite wall.',
 '1.20 m shallow shelf run for books / small items.',
 'The door and room boundaries stay unchanged.',
 'No second occupied workstation is assumed.' ])
note(25,226,'WINDOW COORDINATION',[
 'The personal desk sits at the existing west window. Verify sill height, sash / handle access and blind controls.',
 'An opening or escape requirement cannot be assumed satisfied by this furniture plan; check the actual window before fixing joinery.',
 'The adjacent plant extension keeps this window, but its roof edge is close to the window end and needs a daylight / outlook review.' ])
m.c.showPage()
header(2,'Switch tasks without clearing the other setup','Office plan 1:25 at A3 | Personal-work mode | One chair, two tested positions')
m.furniture=WORK_STATES['Personal']['furniture'];p=m.Plan(30-17.87*40,70-6.29*40,40);crop(p);desktops(p)
p.rect(*CHAIRS['Professional'],None,'amber',.25)
route(p,WORK_ROUTES['Office personal setup approach'])
note(256,55,'THE DAILY CHANGEOVER',[
 'Move the chair from the professional desk to the personal desk.',
 'Both sets of devices stay in place.',
 'Amber outline shows the alternative chair position only.',
 'It does not represent a second person or second chair.' ])
note(256,109,'MAKE THE TWO SETUPS FEEL DISTINCT',[
 'Independent task lighting and reachable sockets.',
 'Separate cable trays and labelled power / data connections.',
 'Keep computer ventilation and leg space clear.',
 'Match desk heights to the same chair and user.' ])
note(256,166,'VERIFIED SPATIAL STATES',[
 f'{len(WORK_STATES["Professional"]["routes"])} routes with the chair at the professional desk.',
 f'{len(WORK_STATES["Personal"]["routes"])} routes with the chair at the personal desk.',
 'Furniture stays inside the existing office boundary.',
 'Door sweeps clear the desk, sofa and shelf footprints.' ])
note(25,226,'PRODUCT SELECTION',[
 'Desk heights, monitor arms, computer cases and drawers are not specified. Check actual equipment before choosing the joinery.',
 'A shallow desk pedestal can consume knee space; reserve device storage deliberately within the chosen desk system.' ])
m.c.showPage()
header(3,'Both sleepers can leave at the foot of the bed','Office night plan 1:25 at A3 | 2.20 x 1.90 m open frame reservation | 2.00 x 1.40 m mattress allowance')
m.furniture=NIGHT['furniture'];p=m.Plan(30-17.87*40,70-6.29*40,40);crop(p);desktops(p)
p.rect(*OPEN_BED,'furniture','muted',.15);p.rect(*MATTRESS,'paper','muted',.15)
p.line((17.97,7.24),(19.97,7.24),'muted',.1,[1,1])
for y in [6.64,7.34]:p.rect(18.05,y,.32,.5,'furniture','muted',.12)
for name in ['Office wall-side sleeper foot exit','Office room-side sleeper foot exit']:route(p,NIGHT['routes'][name])
p.text(19.2,7.2,'2.00 x 1.40 m',2.6)
p.text(20.45,6.52,'0.78 m',2.25,fill='green')
note(256,55,'WHAT IMPROVES',[
 'Both mattress halves open onto the foot-end floor route.',
 'Neither sleeper needs to cross the other mattress half.',
 'The narrowest drawn foot gap is 0.78 m to the work desk.',
 'The wider room-side strip leads to the existing door.' ])
note(256,112,'NIGHT CHANGEOVER',[
 'Park the single chair at the personal desk end, as drawn.',
 'Open the sofa bed toward the centre of the room.',
 'Both desks and all devices stay in place.',
 'The tested scenario assumes office work pauses for guests.' ])
note(256,169,'SOFA-BED REQUIREMENTS',[
 'Selected full open envelope must fit 2.20 x 1.90 m.',
 'Choose an unobstructed foot end; no tall footboard.',
 'Check mechanism travel, frame and mattress height.',
 'The 0.78 m gap is a nominal spatial allowance.' ])
note(25,226,'CHECKED ROUTES, NOT AN ACCESSIBILITY CLAIM',[
 f'{len(NIGHT["routes"])} routes pass with the open bed and parked chair, including both foot positions through to the guest hall.',
 'The routes use the existing 0.70 m envelope. Selected furniture tolerances, actual users and occupied bed movements remain to verify.',
 'This supersedes concept 18\'s one-sided exit proposal; the guest bedroom and other house furniture are retained.' ])
m.c.showPage()
header(4,'Keep the office useful every day and straightforward for guests','Furniture brief and retained household assumptions')
note(22,56,'FURNITURE TO TEST / SELECT',[
 'Professional desk: 1.60 x 0.75 m.',
 'Personal desk: 1.80 x 0.75 m.',
 'One task chair: 0.65 m-square plan reservation.',
 'Sofa: 1.90 x 0.90 m closed; 2.20 x 1.90 m open.',
 'Mattress allowance: 2.00 x 1.40 m.',
 'Books / small items: 1.20 x 0.30 m shallow run.' ])
note(222,56,'CONFIRMED USE',[
 'One person switching between professional and personal work.',
 'Separate permanent setups; no daily clearing of either desk.',
 'Occasional overnight sleeping remains part of the brief.',
 'Visiting children may share beds.',
 'A five-visitor example remains two in the guest bedroom, two',
 'in this room and one visiting child sharing a child-room bed.' ])
note(22,128,'WHAT STAYS',[
 'Office room, door and window positions.',
 'Guest bedroom and shower layout from concept 18.',
 'Garden-side plant / gym / snug proposal from concept 22.',
 'The proposed full gym area and existing laundry functions.',
 'The original family plant placeholder pending full relocation design.' ])
note(222,128,'NEXT REVIEW POINTS',[
 'Actual screens, desk heights and personal computer dimensions.',
 'Window sill, operation / escape and light control.',
 'Open sofa-bed product and a full-size night-route mock-up.',
 'Quiet cooling / ventilation for work and overnight modes.',
 'Acoustic separation from the snug and nearby plant.' ])
text(22,228,'The layout gives each activity a fixed place. Product selection must preserve the foot-end exit and the two desk positions.',3.0,True)
m.c.showPage();m.c.save()
(OUT/'concept-23-study-check.json').write_text(json.dumps({'status':'Two-workspace office proposal; one person switching setups confirmed',
 'model':GARDEN['model'],'work_states':WORK_STATES,'night_state':NIGHT,'office_items':ITEMS,'chair_positions':CHAIRS,
 'open_bed_m':OPEN_BED,'mattress_m':MATTRESS,'narrowest_foot_gap_m':.78,'both_sleeper_foot_exits_connected':True,
 'office_geometry_unchanged':True,'other_furniture_unchanged':True,'garden_source_sha256':GARDEN['source_sha256'],
 'base_sources':BASE_DATA['model_sources'],'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'snug_rooflight_reservation_m':GARDEN['snug_rooflight_reservation_m'],'limitations':['Actual sofa-bed mechanism not selected','Window sill operation and escape to check','No human-use or accessibility validation']},indent=2)+'\n')
print(PDF);print('Both work modes and both connected sleeper foot exits pass.')
