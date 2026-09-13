"""Concept 20: a single current development plan with decision status."""
import json
from dataclasses import asdict
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,DATA=load_model()
assert not DATA['day_issues'] and not DATA['night_issues']
assert len({r.id for r in m.rooms})==len(m.rooms)
assert next(d for d in m.doors if d.id=='D03').y==5.05
assert any(d.id=='D19' for d in m.doors)
assert abs(next(r for r in m.rooms if r.id=='GY').area-24)<1e-8
assert any(f['room']=='ST' and f['kind']=='plant' for f in m.furniture)
assert m.R['W'].dimensions=='3.18 x 2.10 m'
COURT=json.loads((ROOT/'output/pdf/concept-09-study-check.json').read_text())
OUT=ROOT/'output/pdf';PDF=OUT/'concept-20-current-whole-house-plan.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 20 - current whole-house development plan')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.7,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 20 / CURRENT DEVELOPMENT PLAN',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'DEVELOPMENT PLAN | Combines retained decisions and unselected proposals. See status register. No plant extension adopted. Print at 100%.',2.3,fill='muted')
    text(406,287,f'{n} / 3',2.6,align='right',fill='muted')
def court(p):
    p.poly(COURT['court_polygon_m'],'garden',None)
    for r in COURT['paving_rectangles_m']:p.rect(*r,'#eee9dc',None)
    for name,r in COURT['planting_beds']:p.rect(*r,'#9eae89',None)
    for name,r,material,kind in COURT['outdoor_furniture']:p.rect(*r,'furniture','muted',.12)
def details(p):
    for r in [(.35,4.47,1.2,1.2),(6.75,2.57,1.1,1.78),(20.35,3.77,1.2,1)]:p.rect(*r,'wet','muted',.1)
    for f in m.furniture:
        if f['kind']=='glass':p.rect(*f['rect'],'green','green',.15)
        if f['kind']=='bed' and f['room'] in ['P','C1','C2','C3']:
            x,y,w,h=f['rect'];p.rect(x,y,w,h,'furniture','muted',.12)
            if f['room']=='P':p.rect(x+.1,y+h-.48,w-.2,.38,'paper','muted',.1)
            elif f['room']=='C2':p.rect(x+.1,y+.1,.35,h-.2,'paper','muted',.1)
            else:p.rect(x+w-.45,y+.1,.35,h-.2,'paper','muted',.1)
    p.rect(.35,13.5,1.35,1.5,None,'amber',.2)
header(1,'One plan for the house as it stands today','Full plan 1:100 at A3 | South up / north down / east left / west right | 13 September 2026')
p=m.Plan(21,57,10);court(p);p.draw(labels=False);details(p)
for r in m.rooms:
    x,y=r.label
    if r.id=='O':x,y=18.7,7.5
    elif r.id=='G':x,y=18.9,2.15
    elif r.id=='S':x,y=18.7,10.3
    elif r.id=='KL':x,y=6.3,16.15
    elif r.id=='ST':x,y=2.4,7.8
    elif r.id=='GB':x,y=21.15,5.7
    X,Y=p.xy((x,y));m.rect(X-3.5,Y-2.5,7,4.2,'paper',None);text(X,Y+.5,r.id,2.5,True,align='center')
p.dimension((0,0),(27.15,0),-.7,'27.15 m maximum width')
p.dimension((0,0),(0,18.4),-.7,'18.40 m maximum depth',True)
p.text(11.8,2.0,'SOUTH COURTYARD',2.4)
p.text(11.8,3.0,'Selected arrangement',2.1)
for id in ['D03','D19']:
    d=next(d for d in m.doors if d.id==id);p.text(d.x+(.5 if id=='D03' else -.65),d.y-.15,id,2.3,fill='green')
note(312,53,'READ THIS AS A WORKING PLAN',[
 'Parents-suite A retained.',
 'Children / family bath: concept 15.',
 'Office / guests: concept 18 proposal.',
 'Snug / utility / shared room retained.',
 'Room codes: schedule on page 2.' ])
note(312,106,'KEY CURRENT DETAILS',[
 'D03 moved 0.25 m north.',
 'D19 links kitchen and laundry.',
 'Garden room open year-round.',
 'Eight dining chairs, three stools.',
 'Full 4 x 6 m gym retained.' ])
note(312,160,'KEPT OPEN FOR REVIEW',[
 'Plant remains in the linen store.',
 'Gym extension is a separate option.',
 'Office bed exit is one-sided at night.',
 'Ten-at-one-table layout unresolved.',
 'Site, structure and services pending.' ])
note(312,215,'EXTENT OF THIS DRAWING',[
 'No site boundary or carport siting.',
 'No dimensions for construction.',
 'Hearth outline is a reservation.',
 'Windows / door hardware unselected.' ])
text(21,257,'0',2.4);m.rect(21,261,50,1.4,'ink',None);text(71,257,'5 m',2.4,align='right')
text(91,264,'Furniture and fixed glass drawn from one source-checked model.',2.8,fill='muted')
m.c.showPage()
header(2,'Room schedule and what the area numbers mean','Clear room polygons from the current model | Measurements in metres | Furniture is included on page 1')
text(20,51,'CODE',2.7,True);text(41,51,'ROOM',2.7,True);text(149,51,'CLEAR DIMENSIONS / ENVELOPE',2.7,True);text(281,51,'m2',2.7,True,align='right')
for i,r in enumerate(m.rooms):
    y=62+i*7.8;m.line(20,y+2.5,285,y+2.5,'line',.12)
    text(20,y,r.id,2.8,True);text(41,y,r.name,2.7)
    dims=r.dimensions
    if r.id=='KL':dims='Stepped plan; main depth 4.90 m'
    if r.id=='G':dims='4.58 x 3.30 m + wardrobe recess'
    if r.id=='L':dims='L-shape; envelope 4.58 x 3.15 m'
    text(149,y,dims,2.6);text(281,y,f'{r.area:.2f}',2.7,align='right')
gia=m.polygon_area(m.INNER);gea=m.polygon_area(m.OUTLINE);clear=sum(r.area for r in m.rooms)
note(309,54,'AREA BASIS',[
 f'{gia:.2f} m2 internal envelope (GIA).',
 f'{gea:.2f} m2 external footprint.',
 f'{clear:.2f} m2 summed clear rooms.',
 'GIA includes internal partitions.',
 'This is a model area convention.' ])
note(309,112,'NOT INCLUDED',[
 'Proposed gym-block extension.',
 'Carport and external paving.',
 'Any plot or boundary allowance.',
 'No cost or valuation basis implied.' ])
note(309,165,'SOURCE CONTROL',[
 'Measured baseline: plan_model.py.',
 'Open layout: concept 07.',
 'Furnishing: concepts 08, 12-15, 18.',
 'Courtyard: concept 09 arrangement.',
 'Lighting direction: concept 10.',
 'Comfort direction: concept 11.' ])
text(20,264,'Narrow rooms use overall clear dimensions; joinery, pocket cavities and actual frames reduce usable space.',2.8,fill='muted')
m.c.showPage()
header(3,'A drawing register that keeps decisions separate from proposals','Use this page when briefing an architect, services designer or joinery supplier')
note(20,54,'RETAINED / SELECTED DIRECTION',[
 'Single-storey courtyard house with continuous shared-room vault and lower wings.',
 'Year-round open garden room; hall separation beyond the snug.',
 'Parents-suite A; super king, two basins and shower priority over an ensuite bath.',
 'Small double beds for the children; family bath, separate shower and two basins.',
 'Direct kitchen-utility door; separate washer / dryer, preferably side-by-side.',
 'Full gym; plant at the service end is the intended direction.',
 'Active cooling and solar intent; occasional office sofa bed and child sharing.' ])
note(20,114,'DRAWN PROPOSALS / NOT PRODUCT OR CONSTRUCTION APPROVAL',[
 'Room furniture and joinery dimensions, guest shower and D03 relocation.',
 'Office sofa-bed envelope, chair parking and one-sided night exit.',
 'Lighting positions, roof shading / vent reservations and the stove hearth.',
 'Current linen shelves around the original plant placeholder.',
 'Finishes and hardware remain subject to samples and selection.' ])
note(225,54,'SEPARATE OPTIONS / NOT IN THE MAIN PLAN',[
 'Concept 17 A: laundry plant; loss of folding / sorting space.',
 'Concept 17 B: gym-block extension; +12.22 m2 footprint.',
 'B is recommended for development, not selected.',
 'Larger linen storage is conditional on successful relocation.',
 'The concept 16 family-wing annexe stays declined.' ])
note(225,114,'REVIEW BEFORE FIXING JOINERY',[
 'Plant location, complete equipment and maintenance space.',
 'Office sofa-bed mechanism and far-side sleeper exit.',
 'Dining for ten together versus eight plus island seating.',
 'Occupied bathroom and family arrival / laundry routines.',
 'Cooling units, ducts, lighting and roof junctions together.' ])
note(20,180,'CURRENT DOCUMENT REGISTER',[
 '17 / Service-end comparison - two locations, same household brief.',
 '18 / Office and guests - day / night furniture and sleeping example.',
 '19 / Everyday-use review - temporary obstacles and passing alternatives.',
 '20 / This plan - one consolidated daytime geometry and decision register.',
 '21 / Building coordination - route, section and design-input study to follow.' ])
note(225,180,'TECHNICAL WORK STILL NEEDED',[
 'Actual site survey, orientation, boundaries, levels and service connections.',
 'Architectural / structural roof and envelope design.',
 'Room heat loss, cooling loads, ventilation and hot-water demand.',
 'Solar / battery / grid energy balance, including night-time cooling.',
 'Budget / cost review against a coordinated scope.' ])
text(20,251,'This plan supersedes earlier full-plan exports for development review; the individual studies remain the detail references.',3.0,True)
m.c.showPage();m.c.save()
(OUT/'concept-20-study-check.json').write_text(json.dumps({'status':'Consolidated development plan; selected directions and proposals explicitly separated',
 'rooms':[asdict(r) for r in m.rooms],'doors':[asdict(d) for d in m.doors],'windows':m.windows,'furniture':m.furniture,
 'source_hashes':DATA['model_sources'],'gia_m2':gia,'external_footprint_m2':gea,'clear_room_area_m2':clear,
 'plant_extension_included':False,'family_plant_retained':True,'parents_suite':'A','dining_chairs':8,
 'day_route_count':len(DATA['day_routes']),'day_route_issues':DATA['day_issues'],'court_reference':'concept-09-study-check.json'},indent=2)+'\n')
print(PDF);print(f'{len(m.rooms)} rooms; {gia:.2f} m2 GIA; retained concept 15 plant.')
