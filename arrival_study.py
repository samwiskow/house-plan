"""Concept 12: arrival, boot-room storage, utility and pantry study."""
import ast
import copy
import json
from pathlib import Path

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'shared_space_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'shared_space_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'shared_space_study.py'),'exec'),s)
m=s['m'];original=copy.deepcopy((m.rooms,m.doors));m.furniture=[f for f in m.furniture if f['room'] not in ('PA','L','B','H')]
ITEMS=[]
def item(id,room,name,rect,height,kind='cabinet'):
    m.furn(room,name,*rect,kind);ITEMS.append(dict(id=id,room=room,name=name,rect=rect,height_m=height,kind=kind))
item('B1','B','Closed coats / sports bags',(19.15,15.45,1.1,.6),2.3)
item('B2','B','Bench / three shoe bays',(19.15,17.5,1.85,.55),.45,'bench')
item('H1','H','Visitor coat cupboard',(16.47,17.45,.9,.6),2.3)
item('H2','H','Keys ledge / mirror',(18.75,15.45,.28,.6),.9)
item('P1','PA','Pantry counter / drawers',(14,15.45,2.35,.6),.92)
item('P2','PA','Dry-food shelves',(14,17.65,2.35,.4),2.25)
for id,name,y,w in [('L1','Washer bay',12.23,.65),('L2','Dryer bay',12.88,.65),('L3','Sink base',13.53,.8),('L4','Sorting / detergent drawers',14.33,.95)]:
    item(id,'L',name,(21.7,y,.75,w),.92)
item('L5','L','Ventilated hanging cupboard',(17.87,13.7,.7,.6),2.3)
item('L6','L','Folding counter / baskets',(18.62,13.7,1.45,.6),.92)
m.routes['Utility to washer']=[(20.9,14.8),(20.72,13.85),(20.72,12.55)]
m.routes['Utility to folding']=[(20.9,14.8),(19.2,14.8)]
m.routes['Boot bench approach']=[(20.25,16.65),(20.05,17.05)]
DIRECT_DOOR=m.Door('D19','KL','L',17.81,14.43,.8,True,hinge_end=True,side=1)
m.doors.append(DIRECT_DOOR)
m.routes['Kitchen directly to utility']=[(16.8,14.83),(17.81,14.83),(18.8,14.83),(19.2,14.8)]
issues=m.verify();assert not issues,issues
assert m.rooms==original[0] and m.doors[:-1]==original[1]
OPEN=[(21.15,12.23,.55,.65),(21.15,12.88,.55,.65)]
for i,r in enumerate(OPEN):m.furn('L',f'Machine open-door reservation {i+1}',*r,'open')
# Reserve the part of the fully open 40 mm leaf inside the utility, clear of its frame.
OPEN_LEAF=(17.875,15.21,.735,.04)
m.furn('L','D19 fully open leaf',*OPEN_LEAF,'open')
open_issues=m.verify()
# The leaf reservation necessarily intersects its own sweep, already checked above.
open_issues.remove('Door swing hits furniture: D19 / D19 fully open leaf (L)')
assert not open_issues,open_issues
m.furniture=m.furniture[:-3]
CLEARANCES={'pantry_closed_aisle_m':1.6,'utility_closed_head_aisle_m':1.48,'utility_machine_open_aisle_m':.93,'utility_folding_aisle_m':1.03,
            'boot_bench_to_coat_front_m':1.45,'pantry_one_500mm_drawer_open_aisle_m':1.1}
C={'paper':'#fffdf8','ink':'#30392f','muted':'#6a6656','line':'#c9c0af','oak':'#c29b66','ivory':'#f1e7d5','green':'#376248','amber':'#af743b',
   'family':'#f1eee6','shared':'#f2e7d5','guest':'#f1eee6','service':'#f4eddf','circulation':'#faf7ef','furniture':'#dcc8a5','white':'#fffdf8'}
m.PALETTE.update(C)
OUT=ROOT/'output/pdf';PDF=OUT/'concept-12-arrival-storage-utility.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm))
m.c.setTitle('Concept 12 - entrance, boot room, utility and pantry')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines,size=2.8):
    text(x,y,title,3.2,True);m.paragraph(x,y+7,lines,size=size,step=5)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 12 / ARRIVAL + STORAGE',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.8,fill='muted')
    m.line(14,36,406,36,'line',.3);m.line(14,280,406,280,'line',.25)
    text(14,287,'SPATIAL PROPOSAL | Joinery, appliance models, services, drying airflow and fixing details require design. Print at 100% for stated scales.',2.35,fill='muted')
    text(406,287,f'{n} / 4',2.6,align='right',fill='muted')
def tag(p,x,y,l):
    X,Y=p.xy((x,y));m.rect(X-3.3,Y-2.8,6.6,4.8,'paper','green',.15);text(X,Y+.7,l,2.6,True,align='center',fill='green')
def dimension(x,y,w,label):
    m.line(x,y,x+w,y,'muted',.2)
    for xx in [x,x+w]:m.line(xx,y-1.2,xx,y+1.2,'muted',.2)
    text(x+w/2,y-1.5,label,2.55,align='center',fill='muted')
def room_elev(x,base,w,scale=40):
    m.rect(x,base-2.6*scale,w*scale,2.6*scale,'paper','line',.2)
    m.line(x,base,x+w*scale,base,'ink',.5)
def cabinet(x,base,w,h,scale=40,fill='ivory',divs=0):
    m.rect(x,base-h*scale,w*scale,h*scale,fill,'muted',.25)
    for i in range(1,divs+1):m.line(x+w*scale*i/(divs+1),base-h*scale,x+w*scale*i/(divs+1),base,'muted',.2)
def shelf(x,y,w,scale=40):m.rect(x,y-.8,w*scale,1.6,'oak','muted',.15)
def machine(x,base,w,label,scale=40):
    cabinet(x,base,w,.85,scale,'white');m.line(x,base-.7*scale,x+w*scale,base-.7*scale,'muted',.2)
    m.c.setStrokeColor(m.color('muted'));m.c.circle((x+w*scale/2)*m.mm,(297-base+.38*scale)*m.mm,.19*scale*m.mm,stroke=1,fill=0)
    text(x+w*scale/2,base-1.7,label,2.5,align='center')

header(1,'A place for the things that arrive with you','Furnished plan 1:50 at A3 | D19 adds direct kitchen / utility access | South up / north down / east left / west right')
p=m.Plan(20-13.5*20,58-11.8*20,20)
m.c.saveState();clip=m.c.beginPath();clip.rect(14*m.mm,(297-201)*m.mm,215*m.mm,149*m.mm);m.c.clipPath(clip,stroke=0)
old=m.doors;m.doors=[d for d in old if d.id not in ('O05','O07')];p.draw(labels=False);m.doors=old
for r in OPEN:p.rect(*r,None,'amber',.4)
for it in ITEMS:
    x,y,w,d=it['rect'];tag(p,x+w/2,y+d/2,it['id'])
for x,y,t in [(15.15,16.9,'PANTRY'),(17.75,17.05,'ENTRANCE'),(20.8,16.9,'BOOT ROOM'),(19.4,14.57,'UTILITY'),(19,13.1,'WC')]:p.text(x,y,t,2.8)
tag(p,17.25,14.3,'D19')
for name in ['Arrival to kitchen','Boot to pantry','Boot to laundry','Kitchen directly to utility']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.35,[1.3,1])
p.dimension((14,16.2),(16.35,16.2),.35,'2.35 pantry')
p.text(20.68,12.45,'1.48 closed',2.3,fill='muted')
p.text(20.66,13.35,'0.93 open',2.3,fill='amber')
p.text(19.8,18.5,'A / LOOK NORTH',2.3,fill='green')
p.text(19.65,15.2,'B / LOOK SOUTH',2.3,fill='green')
m.c.restoreState()
text(23,211,'Dashed green: arrival / shopping / laundry routes.',2.6,fill='muted')
text(23,217,'Amber outlines: 0.55 m open-machine projections.',2.6,fill='muted')
for i in range(3):m.rect(23+i*20,226,20,1,'ink' if i%2==0 else 'paper','ink',.1)
text(23,234,'0',2.4);text(83,234,'3 m',2.4,align='right')
note(23,249,'D19 / DIRECT KITCHEN ACCESS',[
 '0.80 m opening allowance; leaf opens back into the utility.',
 'Retain boot-room access. Final frame / clear passage to specify.',
 'Coordinate the door head with the adjacent ambient lighting.' ])
note(245,49,'B1 + B2 / BOOT ROOM',[
 '1.10 m closed coats / bags; 1.85 m oak bench.',
 'Three shoe bays below and five staggered hooks above.',
 'Wet coats stay on the open hooks, not in closed storage.',
 'Bench stays outside the house-door swing.' ])
note(245,84,'H1 + H2 / ENTRANCE',[
 '0.90 m visitor-coat cupboard beside the front door.',
 'A 0.28 m-deep keys ledge and mirror near the shared room.',
 'Use the boot-room bench for muddy shoes and bags.' ])
note(245,114,'L1 - L6 / UTILITY',[
 'Separate washer / dryer bays, sink and sorting drawers.',
 '1.45 m folding counter with basket spaces below.',
 '0.70 m ventilated hanging-cupboard reservation.',
 'Its airflow and drying capacity still need design.' ])
note(245,149,'P1 + P2 / PANTRY',[
 '2.35 m counter wall, 0.60 m deep, with open shelves above.',
 'Opposite: 0.40 m-deep food shelving.',
 '1.60 m clear between fronts with drawers closed.' ])
note(245,179,'WHAT WAS CHECKED',[
 f'{len(m.routes)} sampled routes pass at 0.70 m width.',
 'Room-door sweeps clear the proposed furniture.',
 'Routes pass with machines and the D19 leaf fully open.',
 'Actual appliance hinges and cupboard use need checking.' ])
note(245,214,'THE TRADE-OFF',[
 'The utility return has a 1.03 m aisle beside the folding top.',
 'It is primarily a one-person work zone.',
 'Drawers / baskets occupy circulation while being used.',
 'No claim of two-person access or accessibility compliance.' ])
m.c.showPage()

header(2,'Open hooks for wet things, cupboards for the rest','Boot-room elevations A / B at 1:25 | Hall cupboard at 1:40 | Heights are joinery proposals within a provisional 2.60 m room height')
text(20,48,'A / BENCH WALL - LOOKING NORTH',3.2,True)
room_elev(20,165,3.3)
# Looking north reverses plan x: west is on the left of this elevation.
cabinet(20+.3*40,165,1,2.2,fill='paper');text(20+.8*40,165-1.1*40,'OUTSIDE',2.8,align='center')
x=20+1.45*40;cabinet(x,165,1.85,.45,fill='oak',divs=2)
shelf(x,165-1.95*40,1.85)
for i in range(5):
    xx=x+(i+.5)*1.85*40/5;yy=165-(1.2 if i%2 else 1.65)*40
    m.line(xx,yy,xx,yy+3,'amber',.7);m.line(xx,yy+3,xx+2,yy+3,'amber',.7)
text(x+1.85*20,165-.7*40,'OPEN WET-COAT HOOKS',2.65,align='center')
dimension(x,174,1.85*40,'1.85 bench / three shoe bays')
text(226,48,'B / COATS + LAUNDRY DOOR - LOOKING SOUTH',3.2,True)
room_elev(226,165,3.3)
cabinet(226,165,1.1,2.3,divs=1);text(248,139,'COATS / BAGS',2.6,align='center')
cabinet(226+1.3*40,165,.9,2.2,fill='paper');text(226+1.75*40,120,'UTILITY',2.8,align='center')
m.rect(226+2.2*40,165-2.2*40,1*40,2.2*40,None,'amber',.3)
text(226+2.7*40,115,'POCKET',2.6,align='center',fill='amber');text(226+2.7*40,122,'KEEP CLEAR',2.3,align='center',fill='amber')
dimension(226,174,1.1*40,'1.10 coats')
text(20,191,'H1 / HALL COATS - 1:40',3.1,True)
cabinet(20,263,.9,2.3,25,divs=1)
dimension(20,270,.9*25,'0.90')
note(60,205,'A QUIETER ENTRANCE',[
 'Visitor coats behind warm-ivory doors; shelf for hats / gloves.',
 'H2: 0.60 m-long, 0.28 m-deep ledge at approximately 0.90 m.',
 'Mirror above; exact size and wall fixings to coordinate.',
 'Bench height 0.45 m; hook heights are 1.20 / 1.65 m proposals.' ])
note(226,205,'MATERIALS + INSTALLATION',[
 'Warm ivory closed storage, honey oak bench and bronze hooks.',
 'Continue the warm hard floor; allow a washable entrance mat.',
 'Use sliding fronts for B1 / H1 to limit cupboard-door projection.',
 'Check hanger depth, tracks, ventilation and actual usable storage.',
 'Keep laundry pocket cavities free of service runs and fixings.' ])
note(60,239,'D19 / SOUND CONTROL',[
 'Investigate a solid-core leaf, perimeter seals and a suitable bottom seal.',
 'Specify the complete doorset; no sound-reduction rating is claimed.',
 'Coordinate the seals with a designed ventilation transfer path.' ],2.65)
text(226,258,'Acoustic reference: Lorient sealing systems',2.6,fill='green')
m.c.linkURL('https://www.lorientuk.com/files/Lorient-Acoustic-Sealing-Systems.pdf',(226*m.mm,36*m.mm,399*m.mm,43*m.mm),relative=0)
m.c.showPage()

header(3,'Wash, sort and fold within one room','Utility elevations at 1:25 | L1-L4 looking west; L5-L6 looking south | Cabinet / machine dimensions are allowances, not selected products')
text(20,48,'LONG WALL / 3.15 M',3.2,True);room_elev(20,169,3.15)
# Looking west: south (low y) is on the left, north is on the right.
for start,w,label,kind in [(.05,.65,'WASHER','machine'),(.7,.65,'DRYER','machine'),(1.35,.8,'SINK','base'),(2.15,.95,'SORT','base')]:
    xx=20+start*40
    if kind=='machine':machine(xx,169,w,label)
    else:
        cabinet(xx,169,w,.88,divs=1);text(xx+w*20,163,label,2.5,align='center')
        if label=='SINK':m.rect(xx+5,169-.92*40,w*40-10,2,'white','muted',.2)
shelf(20,169-.92*40,3.15)
shelf(20+1.35*40,169-1.65*40,1.75)
dimension(20,179,3.15*40,'0.05 + 0.65 + 0.65 + 0.80 + 0.95 + 0.05')
text(227,48,'RETURN / 2.20 M',3.2,True);room_elev(227,169,2.2)
cabinet(227,169,.7,2.3,divs=1);text(241,112,'HANG',2.5,align='center');text(241,119,'TO DRY',2.5,align='center')
for y in [84,158]:
    for j in range(4):m.line(230,y+j,252,y+j,'muted',.2)
cabinet(227+.75*40,169,1.45,.9,divs=2);shelf(227+.75*40,169-.92*40,1.45)
text(227+( .75+1.45/2)*40,163,'BASKETS',2.5,align='center');shelf(227+.75*40,169-1.65*40,1.45)
dimension(227,179,2.2*40,'0.70 hanging + 0.05 gap + 1.45 folding')
note(20,202,'APPLIANCE ACCESS',[
 'Reserve 0.75 m from wall to worktop front for appliances / connections.',
 'Machine bays are 0.65 m wide; model, hoses and tolerances still matter.',
 '1.48 m aisle closed; 0.93 m behind the 0.55 m open-door allowance.',
 'This checks a rectangular reservation, not a selected hinge sweep.',
 'Keep isolation valves, drainage and sockets accessible.' ])
note(227,202,'DRYING + WORKFLOW',[
 'The 0.70 m hanging cupboard is modest air-drying provision.',
 'Use sliding fronts; airflow / extraction and moisture control need design.',
 'It is not a demonstrated substitute for a full drying room.',
 'Sort below the counter, fold on top and return baskets to the house.',
 'Keep laundry noise and service penetrations away from the snug / WC.' ])
text(20,264,'Size reference only: Bosch WGG245S2GB lists 0.632 m depth including door and 1.049 m with door open; no appliance selected.',2.5,fill='muted')
m.c.linkURL('https://media3.bosch-home.com/Documents/specsheet/en-GB/WGG245S2GB.pdf',(20*m.mm,29*m.mm,390*m.mm,37*m.mm),relative=0)
m.c.showPage()

header(4,'A pantry you can walk through and actually use','Pantry end-wall elevations at 1:25 | Clear room 2.35 x 2.60 m | Side walls reserved for the two pocket doors')
for x,title in [(20,'P1 / COUNTER WALL - LOOKING SOUTH'),(226,'P2 / FOOD SHELVES - LOOKING NORTH')]:
    text(x,48,title,3.2,True);room_elev(x,170,2.35)
x=20
for w,label in [(.6,'DRAWERS'),(.6,'BULK'),(.6,'APPLIANCE'),(.5,'BINS')]:
    cabinet(x+1,170,w,.9);text(x+1+w*20,162,label,2.15,align='center');x+=w*40
shelf(20,170-.92*40,2.35)
for h in [1.55,1.9,2.25]:shelf(20,170-h*40,2.35)
text(20+47,170-1.16*40,'CLEAR LANDING / SMALL APPLIANCES',2.35,align='center')
cabinet(226,170,2.35,2.25,divs=3)
for h in [.4,.8,1.2,1.55,1.9]:m.line(226,170-h*40,320,170-h*40,'muted',.25)
text(273,165,'HEAVIER STORES LOW DOWN',2.35,align='center')
for x in [20,226]:dimension(x,180,2.35*40,'2.35 overall / 0.025 end scribes')
note(20,202,'COUNTER WALL',[
 '0.60 m base depth; 0.30 m upper shelves; 0.92 m worktop height.',
 '2.30 m nominal modules plus two 0.025 m end scribes.',
 'Keep daily items reachable; use upper shelves for lighter stores.',
 'Coordinate the shelf light beneath the first shelf and accessible sockets.',
 'Select any countertop appliances before deciding shelf clearance.' ])
note(226,202,'KEEP THE THROUGH-ROUTE USEFUL',[
 'Opposite shelves are 0.40 m deep, leaving a 1.60 m clear aisle.',
 'One 0.50 m drawer projection leaves 1.10 m between fronts.',
 'Doorways remain 0.90 m: avoid drawer use during shopping passage.',
 'Do not fix shelves or run services through either pocket cavity.',
 'No extra sink or refrigerator is assumed in this pantry.' ])
text(20,264,'Proposed joinery follows the ivory / honey oak / warm bronze palette. Cabinet divisions are preliminary; carcasses and hardware reduce usable space.',2.5,fill='muted')
m.c.showPage();m.c.save()
(OUT/'concept-12-study-check.json').write_text(json.dumps({
 'status':'Arrival joinery proposal; direct hinged kitchen / utility door selected','furniture':ITEMS,'clearances_m':CLEARANCES,
 'routes':m.routes,'route_envelope_m':.7,'normal_issues':issues,'open_machine_projection_rectangles_m':OPEN,'open_machine_issues':open_issues,
 'room_geometry_changed':False,'room_doors_changed':True,'added_door':DIRECT_DOOR.__dict__,
 'new_wall_opening_m':DIRECT_DOOR.opening,'fully_open_door_leaf_reservation_m':OPEN_LEAF,
 'door_sweeps_checked':'All room door sweeps against furniture; fully open D19 leaf included in route check; not selected appliance or joinery hinges',
 'acoustic_source':'https://www.lorientuk.com/files/Lorient-Acoustic-Sealing-Systems.pdf',
 'acoustic_brief':'Solid-core hinged doorset with perimeter and suitable bottom seals; coordinate ventilation transfer; no verified rating',
 'laundry_preference_confirmed':'Separate washer and dryer plus some air-drying space',
 'air_drying_proposal':'Modest ventilated hanging cupboard; capacity and airflow unverified',
 'product_selection':False,'source':'https://media3.bosch-home.com/Documents/specsheet/en-GB/WGG245S2GB.pdf'},indent=2)+'\n')
print(PDF);print(f'{len(ITEMS)} furniture reservations; {len(m.routes)} routes pass, including open-machine and fully open D19 leaf reservations.')
