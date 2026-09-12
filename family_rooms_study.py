"""Concept 15: children's bedrooms, family bathroom and linen / plant store."""
import ast
import copy
import json
from pathlib import Path

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'suite_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='A_STATE' for t in n.targets))
s={'__file__':str(ROOT/'suite_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'suite_study.py'),'exec'),s)
m=s['m'];original=copy.deepcopy((m.rooms,m.doors,m.windows))
m.furniture=[f for f in m.furniture if f['room'] not in ('C1','C2','C3','FB','ST')]
ITEMS=[]
def item(id,room,name,r,h,kind='cabinet'):
    m.furn(room,name,*r,kind);ITEMS.append(dict(id=id,room=room,name=name,rect=r,height_m=h,kind=kind))
ROOMS={'C1':(4.82,8.81,False),'C2':(.35,8.81,True),'C3':(4.82,4.47,False)}
def coord(room,p):
    x,y,mirror=ROOMS[room];return (x+(3.03-p[0] if mirror else p[0]),y+p[1])
def local_rect(room,r):
    x,y,w,h=r;X,Y,mirror=ROOMS[room];return (X+(3.03-x-w if mirror else x),Y+y,w,h)
for room in ROOMS:
    for id,name,r,h,kind in [
        ('B','Small-double bed frame',(.83,2.77,2.10,1.35),.6,'bed'),
        ('W','Clothes wardrobe',(0,1.28,.66,1.80),2.3,'cabinet'),
        ('D','Desk by window',(2.38,1.13,.65,1.40),.74,'desk'),
        ('C','Desk chair use reservation',(1.58,1.32,.65,.65),.85,'chair')]:
        item(room+id,room,name,local_rect(room,r),h,kind)
    hall_x=4.1
    start=coord(room,(-.3,.68));entry=coord(room,(1.1,.68));aisle=coord(room,(1.1,2.10))
    m.routes[f'{room} entry to bed']=[(hall_x,start[1]),entry,aisle,coord(room,(1.3,2.35))]
    m.routes[f'{room} wardrobe approach']=[entry,coord(room,(1.10,1.6))]
    m.routes[f'{room} desk approach']=[aisle,coord(room,(1.1,2.35)),coord(room,(1.98,2.35))]
# Move the bathroom doorway clear of the double vanity; retain the existing swing.
for d in m.doors:
    if d.id=='D03':d.y=5.05
item('F1','FB','Bath',(.35,6.40,1.70,.75),.58,'bath')
item('F2','FB','Double vanity',(1.98,4.47,1.40,.50),.85,'basin')
item('F3','FB','WC',(2.53,6.43,.65,.72),.42,'wc')
SHOWER=(.35,4.47,1.20,1.20)
SCREENS=[(1.535,4.47,.03,.18),(1.535,5.55,.03,.12),(.35,5.655,1.185,.03)]
for i,r in enumerate(SCREENS):item(f'F4-{i+1}','FB','Fixed shower screen',r,2.10,'glass')
item('L1','ST','Retained plant allowance',(.50,7.40,.85,.85),None,'plant')
item('L2','ST','Linen shelves',(1.50,8.24,.90,.45),2.20)
m.routes['Family bathroom vanity']=[(4.1,5.50),(3.0,5.50),(2.65,5.50)]
m.routes['Family bathroom shower']=[(3.0,5.50),(2.05,5.40),(1.88,5.32),(1.6,5.15),(.95,5.10)]
m.routes['Family bathroom bath']=[(3.0,5.50),(2.2,5.8),(1.90,6.02)]
m.routes['Family bathroom WC']=[(3.0,5.50),(2.80,5.98)]
m.routes['Linen approach']=[(4.1,7.90),(2.8,7.90),(1.95,7.80)]
m.routes['Plant approach']=[(2.8,7.90),(1.75,7.80)]
issues=m.verify();assert not issues,issues
assert m.rooms==original[0] and m.windows==original[2]
assert all(d==old for d,old in zip(m.doors,original[1]) if d.id!='D03')
OUT=ROOT/'output/pdf';PDF=OUT/'concept-15-family-bedrooms-bath-linen.pdf'
m.PALETTE.update({'wet':'#e3e9e1','linen':'#e7d9bd'})
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 15 - children, family bath and linen')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.8,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 15 / FAMILY ROOMS',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'PROPOSAL | Room sizes retained; bathroom door moved 0.25 m. Furniture, window operation, plant and bathroom construction require design. Print at 100%.',2.25,fill='muted')
    text(406,287,f'{n} / 4',2.6,align='right',fill='muted')
def tag(p,x,y,label):
    X,Y=p.xy((x,y));m.rect(X-3.4,Y-2.7,6.8,4.8,'paper','green',.12);text(X,Y+.8,label,2.35,True,align='center',fill='green')
def bed(p,room):
    p.rect(*local_rect(room,(.83,2.77,2.10,1.35)),'linen','muted',.15)
    p.rect(*local_rect(room,(.90,2.845,2.00,1.20)),None,'muted',.10)
    p.rect(*local_rect(room,(2.50,2.97,.32,.95)),'paper','muted',.10)
def bathroom(p):
    p.rect(*SHOWER,'wet','muted',.12)
    for r in SCREENS:p.rect(*r,'green','green',.15)
    p.rect(1.98,4.47,1.4,.5,'oak','muted',.12)
    for x in [2.07,2.77]:p.rect(x,4.54,.52,.33,'paper','muted',.1)
def draw(p,clip_box,room_labels=False):
    x,y,w,h=clip_box;m.c.saveState();clip=m.c.beginPath();clip.rect(x*m.mm,(297-y-h)*m.mm,w*m.mm,h*m.mm);m.c.clipPath(clip,stroke=0)
    p.draw(labels=False);bathroom(p)
    for room in ROOMS:bed(p,room)
    if room_labels:
        for room in ROOMS:
            X,Y=coord(room,(1.25,.75));p.text(X,Y,room,2.6)
    m.c.restoreState()
header(1,'Three equal rooms, ready to grow with them','Family-wing plan 1:50 at A3 | Each child room 3.03 x 4.22 m / 12.79 m2 | South up / north down / east left / west right')
p=m.Plan(25,58-4.3*20,20);draw(p,(15,51,181,187),True)
for room in ROOMS:
    for a,b in zip(m.routes[f'{room} entry to bed'],m.routes[f'{room} entry to bed'][1:]):p.line(a,b,'green',.3,[1,1])
p.text(1.85,5.85,'FAMILY BATH',2.4);p.text(1.85,7.75,'LINEN / PLANT',2.3)
note(220,55,'SAME ALLOWANCE IN ALL THREE ROOMS',[
 '1.20 x 2.00 m small-double mattress; 1.35 x 2.10 m frame allowance.',
 'Bed turned across the far end, with the head at the external wall.',
 '1.80 m wardrobe and a 1.40 x 0.65 m desk by the window.',
 'Keep the central route clear with the desk chair in its use position.',
 'C1 / C3 share a layout; C2 mirrors it across the family hall.' ])
note(220,104,'FAMILY BATHROOM / BRIEF CONFIRMED',[
 '1.70 x 0.75 m bath and separate 1.20 x 1.20 m shower.',
 '1.40 m double vanity with storage; WC beside the bath on the north wall.',
 'Move D03 north by 0.25 m to clear the vanity.',
 'Room walls, floor area and existing window remain unchanged.' ])
note(220,148,'LINEN / KEEP THE PLANT ALLOWANCE HONEST',[
 'Retain the existing 0.85 x 0.85 m plant footprint for now.',
 'Add 0.90 m of linen shelving at 0.45 m depth.',
 'The door swing and a floor approach remain clear.',
 'Actual equipment, pipes and maintenance space are not selected.',
 'Final linen capacity depends on the services design.' ])
note(220,197,'PARENTS SUITE / DECISION RECORDED',[
 'Option A is selected: super king, two basins and the larger shower.',
 'The bath alternative and wardrobe compromise are declined.',
 'This study inherits Option A and retains the snug and D19.' ])
text(25,251,'Dashed green: new bed approaches; detailed routes recorded in the study JSON.',2.5,fill='muted')
text(25,259,f'{len(m.routes)} sampled routes pass at a 0.70 m envelope; room-door sweeps clear furniture.',2.5,fill='muted')
m.c.showPage()
header(2,'A proper bed, desk and clothes storage for each child','Bedroom details 1:30 at A3 | Small-double frames are allowances, not selected products | Existing doors and windows retained')
for room,left,label in [('C1',35,'C1 / C3 - WINDOW ON THE WEST'),('C2',235,'C2 - WINDOW ON THE EAST')]:
    rx,ry,_=ROOMS[room];p=m.Plan(left-rx*(1000/30),61-ry*(1000/30),1000/30)
    text(left,49,label,3.1,True);draw(p,(left-8,56,120,158))
    for it in ITEMS:
        if it['room']==room:
            x,y,w,h=it['rect'];tag(p,x+w/2,y+h/2,it['id'][-1])
    for name in [f'{room} entry to bed',f'{room} desk approach']:
        for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.3,[1,1])
    p.dimension((rx,ry),(rx+3.03,ry),-.12,'3.03 m')
note(20,224,'FURNITURE + EVERYDAY USE',[
 'B: small double. W: 0.66 m-deep wardrobe with sliding fronts proposed.',
 'D: desk height / chair to suit the child; allow task lighting and accessible power.',
 'C: 0.65 m chair reservation, set 0.15 m back from the desk front.',
 'The bed-end placement keeps the main window area available for studying.' ])
note(220,224,'LIGHT, STORAGE + PERSONALITY',[
 'Use a bedside reading light, local desk light and separate soft general light.',
 'Keep books on the hall-side wall; avoid shelving across the window.',
 'Warm ivory and oak form the base; let each child choose the accent colour.',
 'Test window sill height, handles, blackout, safe furniture fixings and reach.' ])
m.c.showPage()
header(3,'A family bathroom with a bath and a separate shower','Bathroom plan 1:20 at A3 | 3.03 x 2.68 m / 8.12 m2 | Double vanity and generous shower confirmed')
p=m.Plan(24-.35*50,65-4.47*50,50);draw(p,(17,57,174,151))
p.text(.95,5.10,'1.20 x 1.20',2.6);p.text(.95,5.32,'SHOWER',2.5)
p.text(1.20,6.80,'1.70 x 0.75 BATH',2.5)
for name in ['Family bathroom vanity','Family bathroom bath','Family bathroom WC']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.3,[1,1])
p.dimension((.35,4.47),(3.38,4.47),-.20,'3.03 m')
note(220,54,'THE LAYOUT',[
 'Bath along the north wall; shower in the south-east corner.',
 'Double vanity on the south wall, clear of the revised door swing.',
 'WC sits beside the bath on the north wall.',
 'A 0.90 m shower entry is reserved between fixed glass pieces.',
 'Door position is a proposal; the room footprint is unchanged.' ])
note(220,105,'WHAT NEEDS CAREFUL DETAILING',[
 'The existing window overlaps the shower zone.',
 'Resolve privacy, waterproof reveals, sill and window operation.',
 'Select an enclosure that contains spray without blocking the entry.',
 'Check bath-side access and help-at-bath space with actual products.',
 'Frame thickness, handles and simultaneous use are not validated.' ])
note(220,156,'LIGHT + MATERIALS',[
 'Warm ivory / buff porcelain and honey-oak vanity fronts.',
 'Mirror lighting on both sides; a separate soft night light.',
 'Use local reading and desk controls in bedrooms, independent of this room.',
 'Bathroom fittings, drainage, ventilation and electrical zones need design.',
 'Keep plumbing off the parents bed-head wall where practical.' ])
note(24,225,'SPACE CHECK',[
 'The nominated routes pass with the fixed shower glass treated as an obstacle.',
 'The bath / shower corner is tighter than the open middle of the room.',
 'These are footprint checks, not an accessibility or construction assessment.' ])
note(220,225,'DAY-TO-DAY STORAGE',[
 'Use vanity drawers for daily toiletries and spare supplies.',
 'Locate towel hooks on the dry side, outside the door swing.',
 'Keep bulk towels and bedding in the neighbouring linen store.' ])
m.c.showPage()
header(4,'Useful linen storage without losing the service space','Linen / plant plan 1:20 and shelving elevation 1:20 | 3.03 x 1.42 m / 4.30 m2 | Plant footprint is a placeholder')
p=m.Plan(25-.35*50,70-7.27*50,50);draw(p,(17,61,176,96))
p.text(.925,7.8,'PLANT',2.6);p.text(1.95,8.5,'LINEN',2.6)
for name in ['Linen approach','Plant approach']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.3,[1,1])
text(239,49,'LINEN SHELVES / 0.90 M',3.2,True)
x=239;base=177;sc=50
m.rect(x,base-2.2*sc,.9*sc,2.2*sc,'ivory','muted',.2)
for z in [.35,.75,1.15,1.55,1.95]:m.rect(x,base-z*sc,.9*sc,.025*sc,'oak','muted',.12)
text(x+.45*sc,190,'0.45 m depth',2.7,align='center',fill='muted')
note(305,69,'FIVE SHELF LEVELS',[
 'Towels and daily bedding',
 'on the middle shelves.',
 'Less-used items above.',
 'Keep heavy items low.',
 'Shelf spacing is adjustable.' ])
note(24,182,'AN ALLOWANCE, NOT A PLANT DESIGN',[
 'Retain the original 0.85 x 0.85 m plant footprint.',
 'The checked approach does not establish maintenance / replacement clearance.',
 'Cylinder, ventilation unit, pipes and valves may need more space.',
 'Do not enclose equipment or order the linen joinery before services coordination.' ])
note(24,229,'LINEN CAPACITY',[
 '0.90 m-wide x 0.45 m-deep shelves, on five proposed levels.',
 'This is a modest cupboard for a five-bedroom house.',
 'Check actual towel / bedding stacks before assigning storage quantities.' ])
note(220,220,'IF MORE LINEN SPACE IS NEEDED',[
 'First resolve the plant location and access requirements.',
 'Then assess whether this room can become dedicated linen storage.',
 'Do not assume the retained plant can move into the fitted utility.',
 'No equipment relocation is proposed in this study.' ])
text(24,269,'Services reference: Vaillant heat-pump installation guidance - allow space for internal equipment as well as the outdoor unit.',2.4,fill='muted')
m.c.linkURL('https://vaillant.co.uk/advice/understanding-heating-technology/heat-pumps/your-heat-pump-journey/',(24*m.mm,25*m.mm,405*m.mm,32*m.mm),relative=0)
m.c.showPage();m.c.save()
(OUT/'concept-15-study-check.json').write_text(json.dumps({
 'status':'Family rooms proposal; parents suite Option A selected',
 'confirmed_preferences':['Small double beds where they fit','Family bath, separate generous shower and two basins','Parents suite Option A'],
 'furniture':ITEMS,'routes':m.routes,'route_envelope_m':.7,'issues':issues,
 'shower_zone_m':SHOWER,'fixed_shower_screens_m':SCREENS,
 'bed_mattress_m':[1.20,2.0],'bed_frame_m':[1.35,2.1],
 'changed_door':next(d.__dict__ for d in m.doors if d.id=='D03'),'previous_D03_y_m':4.80,
 'room_window_geometry_changed':False,'linen_shelves_m':{'width':.9,'depth':.45,'heights':[.35,.75,1.15,1.55,1.95]},
 'retained_plant_footprint_m':[.50,7.40,.85,.85],
 'limitations':['Plant not selected or sized','No occupied-use, window-operation or actual furniture hardware check','No bathroom services or compliance design','Shower floors walkable; fixed glass obstacles checked']},indent=2)+'\n')
print(PDF);print(f'{len(m.routes)} routes and door / furniture sweeps pass.')
