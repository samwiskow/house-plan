"""Concept 25: revised whole-house proposal and next design decisions."""
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,BASE=load_model()
DATA=json.loads((ROOT/'output/pdf/concept-24-study-check.json').read_text())
for name,digest in [('library_snug.py',DATA['source_sha256']),('two_workspace_office.py',DATA['office_source_sha256']),('garden_plant_study.py',DATA['garden_source_sha256'])]:
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
state=DATA['model'];m.rooms=[m.Room(**r) for r in state['rooms']];m.R={r.id:r for r in m.rooms}
m.doors=[m.Door(**d) for d in state['doors']];m.windows=state['windows'];m.OUTLINE=state['outline'];m.INNER=state['inner']
m.furniture=DATA['furniture'];m.routes=DATA['routes']
assert all(not s['issues'] for s in DATA['states'].values())
assert len({r.id for r in m.rooms})==len(m.rooms)
assert abs(m.R['PL'].area-10.60)<1e-8
COURT=json.loads((ROOT/'output/pdf/concept-09-study-check.json').read_text())
OUT=ROOT/'output/pdf';PDF=OUT/'concept-25-revised-whole-house-plan.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 25 - revised whole-house proposal')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.7,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 25 / REVISED WHOLE-HOUSE PROPOSAL',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'REVISED PROPOSAL | Includes garden-side plant, two-workspace office and library snug for review. Equipment and construction remain to design.',2.3,fill='muted')
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
header(1,'The revised house, with the library and rear plant room','Full plan 1:100 at A3 | South up / north down / east left / west right | 13 September 2026')
p=m.Plan(21,57,10);court(p);p.draw(labels=False);details(p)
for f in m.furniture:
    if f['room']=='S' and f['kind']=='cabinet':p.rect(*f['rect'],'#564032','ink',.12)
p.rect(*DATA['snug_rooflight_reservation_m'],None,'amber',.25)
p.text(23.9,8.4,'PROPOSED PLANT',2.1,fill='green')
for r in m.rooms:
    x,y=r.label
    if r.id=='O':x,y=18.7,7.5
    elif r.id=='G':x,y=18.9,2.15
    elif r.id=='S':x,y=20.0,10.35
    elif r.id=='PL':x,y=24.4,10.6
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
note(312,53,'CHANGES IN THIS PROPOSAL',[
 'Garden-side plant behind the gym.',
 'Internal door through the gym.',
 'Snug rooflight replaces side window.',
 'Library bookcases with TV provision.',
 'Two permanent office workspaces.' ])
note(312,108,'RETAINED HOUSEHOLD BRIEF',[
 'Parents-suite A; child-room doubles.',
 'Office sofa bed for occasional guests.',
 'Full 4 x 6 m gym and laundry.',
 'Dining assumption: 8 + 2 at island.',
 'Existing three island stools drawn.' ])
note(312,163,'SERVICES DIRECTION',[
 'Separate wing cooling systems.',
 'Shared space needs its own zone.',
 'Hot-water / winter heat to coordinate.',
 'Fresh-air ventilation still to route.',
 'Original ST plant is a placeholder.' ])
note(312,218,'WHAT REMAINS PROVISIONAL',[
 'Plant equipment and its capacity.',
 'Rooflight and all joinery heights.',
 'Heating / ventilation arrangement.',
 'Site, structure, windows and cost.' ])
text(21,257,'0',2.4);m.rect(21,261,50,1.4,'ink',None);text(71,257,'5 m',2.4,align='right')
text(91,264,'Furniture and fixed glass drawn from one source-checked model.',2.8,fill='muted')
m.c.showPage()
header(2,'Room schedule and what the area numbers mean','Clear room polygons from the current model | Measurements in metres | Furniture is included on page 1')
text(20,51,'CODE',2.7,True);text(41,51,'ROOM',2.7,True);text(149,51,'CLEAR DIMENSIONS / ENVELOPE',2.7,True);text(281,51,'m2',2.7,True,align='right')
for i,r in enumerate(m.rooms):
    y=61+i*7.65;m.line(20,y+2.5,285,y+2.5,'line',.12)
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
 'Carport and external works.',
 'Courtyard and external paving.',
 'Any plot or boundary allowance.',
 'No cost or valuation basis implied.' ])
note(309,165,'SOURCE CONTROL',[
 'Measured baseline: plan_model.py.',
 'Open layout: concept 07.',
 'Furnishing: retained studies + 23 / 24.',
 'Courtyard: concept 09 arrangement.',
 'Lighting direction: concept 10.',
 'Rear plant and rooflight: concept 22.' ])
text(20,264,'Narrow rooms use overall clear dimensions; joinery, pocket cavities and actual frames reduce usable space.',2.8,fill='muted')
m.c.showPage()
header(3,'What to decide next, and what this proposal establishes','Use concepts 22-24 for the detailed plant, services, office and library studies')
note(20,54,'USER DIRECTION CARRIED FORWARD',[
 'Plant behind the gym with an interior door; arrival projection declined.',
 'Separate cooling systems on the two sides as the starting concept.',
 'One person switching between permanent professional / personal desks.',
 'Occasional office sofa bed and visiting children sharing beds.',
 'Library character, floor-to-ceiling books and space for a television.',
 'Dining accepted; working interpretation is eight plus two at the island.' ])
note(225,54,'DRAWN ALLOWANCES TO DETAIL',[
 '4.00 x 2.65 m plant room; 13.05 m2 net footprint addition.',
 'Gym rack / dumbbells repositioned; internal D18 moved 0.60 m.',
 'Snug rooflight 1.10 m square; bookcase height provisionally 2.60 m.',
 'Office bed envelope 2.20 x 1.90 m; both foot exits connect.',
 'Original family plant retained as a placeholder pending full relocation.',
 'No extra installed equipment or released linen storage is implied.' ])
note(20,119,'1 / RESOLVE HEATING, HOT WATER AND FRESH AIR',[
 'Choose winter heating: wet underfloor, air-to-air, or a defined combination.',
 'Calculate room loads and allocate closed rooms and shared-space cooling.',
 'Compare central versus wing-based fresh-air ventilation and service routes.',
 'Size hot-water storage / recovery for the agreed simultaneous shower use.',
 'Check incoming water / power, pipe wait times, losses and maintenance.' ])
note(225,119,'2 / DRAW ROOF, WINDOWS AND THE EXTERIOR',[
 'Coordinate the rear plant roof with the wing and snug rooflight.',
 'Check nearby office-window outlook, shading and daylight.',
 'Resolve vault junctions, roof structure, insulation and service penetrations.',
 'Design summer shading / ventilation alongside glazing.',
 'Place outdoor units for access, air flow and acceptable noise.' ])
note(20,183,'3 / CHECK SITE AND COST BEFORE FINISH SELECTION',[
 'Use the actual survey, levels, boundaries and service connection positions.',
 'Coordinate arrival, carport, garden use and maintenance access.',
 'Obtain a cost review of the revised footprint, roof and services package.',
 'Then fix joinery products, lighting / sockets and material samples.',
 'Recheck everyday use against the actual chosen furniture.' ])
note(225,183,'VERIFICATION AND LIMITS',[
 f"{len(m.routes)} sampled 0.70 m routes pass in each of three office states.",
 'Room boundaries, furniture footprints and door sweeps checked.',
 'Library approaches and both office foot exits are connected.',
 'These are spatial checks, not sizing or construction certification.',
 'Concept 20 is historical; this is the latest consolidated proposal.' ])
text(20,258,'Detailed drawings: 22 plant / services; 23 office; 24 library. Selected products and professional coordination remain outstanding.',2.8,fill='muted')
m.c.showPage();m.c.save()
(OUT/'concept-25-study-check.json').write_text(json.dumps({'status':'Revised consolidated proposal',
 'model':state,'furniture':m.furniture,'routes':m.routes,'gia_m2':gia,'external_footprint_m2':gea,'clear_room_area_m2':clear,
 'plant_extension_included_as_proposal':True,'family_plant_placeholder_retained':True,'dining_assumption':'8 at table plus 2 at island',
 'snug_rooflight_reservation_m':DATA['snug_rooflight_reservation_m'],'source_hashes':BASE['model_sources'],
 'library_source_sha256':DATA['source_sha256'],'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'state_route_counts':{name:len(s['routes']) for name,s in DATA['states'].items()},'issues':[]},indent=2)+'\n')
print(PDF);print(f'{len(m.rooms)} rooms; {gia:.2f} m2 GIA; {gea:.2f} m2 footprint; {clear:.2f} m2 clear rooms.')
