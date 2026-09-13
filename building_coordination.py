"""Concept 21: preliminary service routes, roof sections and design inputs."""
import json
from math import hypot, tan, radians
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,DATA=load_model()
PLANT=json.loads((ROOT/'output/pdf/concept-17-study-check.json').read_text())['B']
COMFORT=json.loads((ROOT/'output/pdf/concept-11-study-check.json').read_text())
ROUTES={
 'Family distribution':[(24.5,19.3),(24.5,17.7),(20.9,17.7),(20.9,14.4),(17.15,14.4),(17.15,13.4),(4.1,13.4),(4.1,5.5)],
 'Guest distribution':[(20.9,14.4),(17.15,14.4),(17.15,5.5)],
 'Family hot-water route':[(23.4,20.0),(23.4,17.7),(20.9,17.7),(20.9,14.4),(17.15,14.4),(4.1,14.4),(4.1,5.5),(2.65,5.5)]}
LENGTHS={name:sum(hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(pts,pts[1:])) for name,pts in ROUTES.items()}
COOLED=['P','C1','C2','C3','G','KL','OR','O','S','GY']
assert set(COOLED)<=set(m.R)
assert all(m.overlap(COMFORT['shade_reservation_m'],r)==0 for r in COMFORT['roof_vent_reservations_m'])
GROSS_ZONE=3.20-2.60
assert abs(GROSS_ZONE-.6)<1e-8
OUT=ROOT/'output/pdf';PDF=OUT/'concept-21-building-coordination.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 21 - preliminary building coordination')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.7,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 21 / BUILDING COORDINATION',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'PRELIMINARY COORDINATION | Proposed routes / volumes only. No equipment capacity, structure, airflow, heat-loss, overheating or compliance result.',2.25,fill='muted')
    text(406,287,f'{n} / 5',2.6,align='right',fill='muted')
header(1,'The difficult connection is across the shared-room vault','Route study 1:100 at A3 | Uses unselected plant option B for comparison | South up / north down')
p=m.Plan(21,53,10);p.draw(labels=False)
for f in m.furniture:
    if f['kind']=='bed' and f['room'] in ['P','C1','C2','C3']:
        x,y,w,h=f['rect'];p.rect(x,y,w,h,'furniture','muted',.12)
        if f['room']=='P':p.rect(x+.1,y+h-.48,w-.2,.38,'paper','muted',.1)
        elif f['room']=='C2':p.rect(x+.1,y+.1,.35,h-.2,'paper','muted',.1)
        else:p.rect(x+w-.45,y+.1,.35,h-.2,'paper','muted',.1)
p.rect(*PLANT['outer'],'green',None);p.rect(*PLANT['clear'],'wet',None)
for name,points in ROUTES.items():
    colour='amber' if name=='Family hot-water route' else 'green'
    for a,b in zip(points,points[1:]):p.line(a,b,colour,.6,[1.5,1])
for room in COOLED:
    x,y=m.R[room].label;X,Y=p.xy((x,y));m.rect(X-3.5,Y-2.5,7,4.2,'paper','green',.1);text(X,Y+.5,room,2.3,True,align='center',fill='green')
p.rect(4.1,13.15,13.05,.5,None,'amber',.35)
p.text(10.2,12.65,'VISIBLE EDGE BAND TO REVIEW',2.5,fill='amber')
p.text(24.8,19.0,'OPTION B',2.6)
for n,(x,y) in enumerate([(20.9,15.4),(17.15,13.4),(4.1,13.4)],1):
    X,Y=p.xy((x,y));m.rect(X-3,Y-3,6,6,'paper','amber',.3);text(X,Y+1,str(n),2.8,True,align='center',fill='amber')
note(313,53,'1 / PLANT TO SERVICE WING',[
 'Trace above the gym / service rooms.',
 'Keep access to filters and connections.',
 'Check crossing of the retained gym wall.',
 'Do not use the gym floor for equipment.' ])
note(313,104,'2 / GUEST WING BRANCH',[
 'Guest hall offers a candidate route.',
 'Check duct + silencer dimensions.',
 'Coordinate office and snug sound.',
 'No terminal positions are selected.' ])
note(313,151,'3 / FAMILY WING CROSSING',[
 'No existing enclosed corridor spans',
 'the open living / dining room.',
 'A visible service band may be needed.',
 'Section on page 2 exposes the effect.',
 'Concealment is not yet resolved.' ])
note(313,207,'AMBER / HOT WATER',[
 f'{LENGTHS["Family hot-water route"]:.1f} m drawn plan route to family basin.',
 'No verticals, fittings or final branches.',
 'Compare waiting time and heat loss;',
 'size pipes before choosing circulation.' ])
text(21,267,'Green = conceptual ventilation / cooling distribution. Amber = conceptual water route and unresolved crossing. Lines are not installed duct sizes.',2.6,fill='muted')
m.c.showPage()
header(2,'Keep the vault honest about the space services need','Longitudinal section through the family-hall / shared-room junction at x = 4.10 m | 1:40 at A3')
sc=25;ox=25;floor=208
X=lambda y:ox+(y-10.2)*sc
Y=lambda z:floor-z*sc
m.line(X(10.2),Y(0),X(18.4),Y(0),'ink',.6)
m.line(X(10.2),Y(2.6),X(13.03),Y(2.6),'muted',.3)
m.line(X(10.2),Y(3.2),X(12.8),Y(3.2),'ink',.5)
m.line(X(12.8),Y(3.2),X(12.8),Y(3.7),'ink',.4)
ridge=3.7+2.8*tan(radians(30));apex=3.5+2.45*tan(radians(30))
m.poly([(X(12.8),Y(3.7)),(X(15.6),Y(ridge)),(X(18.4),Y(3.7)),(X(18.05),Y(3.5)),(X(15.6),Y(apex)),(X(13.15),Y(3.5))],'#eee4d3','muted',.3)
m.line(X(13.15),Y(3.5),X(15.6),Y(apex),'ink',.35);m.line(X(15.6),Y(apex),X(18.05),Y(3.5),'ink',.35)
m.rect(X(13.03),Y(3.2),.12*sc,1.1*sc,'wall',None)
m.rect(X(13.15),Y(3.1),.5*sc,.4*sc,None,'amber',.6)
m.line(X(12.2),Y(2.85),X(13.65),Y(2.85),'green',.6,[1,1])
text(X(11.5),Y(1.5),'FAMILY HALL',2.8,True,align='center');text(X(15.7),Y(1.5),'SHARED ROOM',2.8,True,align='center')
text(X(10.2),Y(3.2)-3,'+3.20 roof top',2.5);text(X(10.2),Y(2.6)+5,'+2.60 ceiling',2.5)
text(X(15.6),Y(apex)+9,f'+{apex:.2f} ceiling apex',2.5,align='center');text(X(18.05),Y(3.5)+6,'+3.50 spring',2.5,align='right')
m.line(X(13.4),Y(2.7),X(13.4),Y(2.1),'amber',.25);text(X(13.4),Y(2.1)+5,'EDGE BAND',2.4,align='center',fill='amber')
note(260,55,'A RESERVATION, NOT A HIDDEN SOLUTION',[
 'Test a 0.50 m projection x 0.40 m deep edge band.',
 'Its underside is +2.70 m; top +3.10 m.',
 'It would be visible below the shared-room vault.',
 'The lighting ledge and room proportions need review.',
 'No enclosure is added to the current plan.' ])
note(260,113,'LOWER ROOF / CEILING ZONE',[
 'Roof top +3.20 m minus ceiling +2.60 m = 0.60 m gross.',
 'Roof structure, insulation, falls and ceiling consume this.',
 'Do not count 0.60 m as a usable duct void.',
 'Header penetrations and door head remain unresolved.',
 'No structural member may be assumed drillable.' ])
note(260,172,'COMPARE BEFORE CHOOSING',[
 'A: accept an accessible service band at the shared edge.',
 'B: investigate distributed ventilation / short cooling runs.',
 'B trades a major crossing for more local equipment.',
 'Both need capacities, noise, terminals and access checked.',
 'Neither distribution strategy is selected.' ])
note(25,241,'SECTION STATUS',[
 'Roof heights follow the existing concept 06B direction. The header and services band are coordination reservations only.',
 'This section identifies a design clash; it does not resolve roof construction, duct sizing or architectural acceptance.' ])
m.c.showPage()
header(3,'Coordinate the plant height, roof drainage and glazed roof together','Plant wall elevation 1:25 at A3 | Roof / shade diagram 1:50 at A3 | Provisional dimensions')
sc=40;x=25;base=178
m.rect(x,base-2.6*sc,4*sc,2.6*sc,'paper','ink',.4)
m.rect(x,base-3.2*sc,4*sc,.6*sc,'#eee4d3','muted',.2)
m.rect(x+.15*sc,base-2.1*sc,.9*sc,2.1*sc,'furniture','muted',.2)
m.rect(x+1.4*sc,base-1.95*sc,.85*sc,.95*sc,'furniture','muted',.2)
m.rect(x+2.7*sc,base-1.65*sc,.65*sc,1.05*sc,'furniture','muted',.2)
for xx,label in [(x+.6*sc,'P1'),(x+1.825*sc,'P2'),(x+3.025*sc,'P3')]:text(xx,base-1.2*sc,label,3,True,align='center')
text(x+80,base-2.83*sc,'0.60 m gross roof / ceiling zone',2.6,align='center')
text(x+1.825*sc,base-2.3*sc,'0.65 m above P2',2.4,align='center')
text(x+80,190,'4.00 m internal width / equipment heights unselected',2.6,align='center')
p=m.Plan(259-12.55*20,69-9.65*20,20)
p.rect(*COMFORT['roof_plan_m'],'wet','muted',.25);p.rect(*COMFORT['shade_reservation_m'],'#d9c3a0','muted',.25)
for r in COMFORT['roof_vent_reservations_m']:p.rect(*r,'paper','green',.3)
p.text(14.55,10.65,'SHADE',2.7);p.text(14.55,13.13,'VENT STRIP',2.5)
note(241,146,'GLAZED ROOF / RETAINED CONCEPT 11',[
 'Roof shade stops before the high vent reservations.',
 'Approximately 0.95 m of upper glass remains unshaded.',
 'Plan rectangles do not overlap; hardware may still conflict.',
 'Check opening arcs, cassette, runoff and maintenance.',
 'Include the unshaded strip in overheating calculations.' ])
note(25,216,'PLANT AND GYM ROOF',[
 'Continue the lower-block roof direction, with falls and outlets designed for the enlarged catchment.',
 'Check foundations, equipment weights, vibration, moisture and service / replacement access.',
 'Select outdoor-unit locations, air intake / exhaust separation and condensate / discharge routes against the actual site.',
 'PV, battery and inverter locations are open; do not count them as fitted in this plant room.' ])
m.c.showPage()
header(4,'Design comfort for each room, then test the solar contribution','Required room coverage and calculations | No capacities inferred from floor area alone')
text(20,53,'SPACE',2.8,True);text(101,53,'CLEAR AREA',2.8,True);text(145,53,'COORDINATION PRIORITY',2.8,True)
priorities={'P':'Quiet night cooling; avoid bed draughts.','C1':'Night comfort, blackout and desk / bed air paths.','C2':'Night comfort, blackout and desk / bed air paths.','C3':'Night comfort, blackout and desk / bed air paths.','G':'Guest night comfort and local controls.','KL':'Vaulted volume, cooking gains and glazing.','OR':'Connected to KL; roof glass and shade dominate.','O':'Computer gains; work and overnight guest modes.','S':'Quiet film use; avoid screen reflections / fan noise.','GY':'Exercise gains, fresh air and clear equipment zones.'}
for i,id in enumerate(COOLED):
    r=m.R[id];y=66+i*12;m.line(20,y+4,393,y+4,'line',.12);text(20,y,r.name,2.8);text(125,y,f'{r.area:.2f} m2',2.8,align='right');text(145,y,priorities[id],2.8)
note(20,200,'HEATING / HOT WATER / VENTILATION',[
 'Room heat loss follows confirmed fabric, weather and temperatures.',
 'Hot water: two simultaneous high-flow showers, then repeat-use recovery.',
 'Design extract in kitchen, bathrooms, WC and laundry; balance supply.',
 'Keep MVHR duties separate from required active cooling capacity.' ])
note(225,200,'SOLAR / BATTERY / GRID',[
 'Match hourly PV generation to cooling and other household loads.',
 'Include evening / night cooling and the office guest mode.',
 'Compare direct PV use, storage losses, battery power and capacity.',
 'Report grid imports and solar coverage; no solar-only claim yet.' ])
m.c.showPage()
header(5,'A concrete brief for the next design stage','Inputs, owners and outputs | Prepare these before equipment or joinery is ordered')
rows=[
 ('Site / architect','Survey, levels, boundaries, orientation, exposure and access.','Locate the extension, outdoor units, carport / PV and drainage.'),
 ('Architect / structure','Wall, floor, roof, glazing and airtightness assumptions.','Resolve roof junctions, the service crossing and maintenance access.'),
 ('Heating / water designer','Temperatures, fabric, shower flows / duration, incoming supply.','Room heat loss, hot-water storage / recovery and distribution design.'),
 ('Ventilation / cooling designer','Occupancy, room gains, acoustic targets and control preferences.','Airflows, cooling loads, terminals, silencers and condensate routes.'),
 ('Solar / electrical designer','Array areas, shading, load profile and battery / EV preferences.','Hourly energy balance, supply capacity and protected equipment siting.'),
 ('Cost review','Chosen scope and coordinated quantities.','Compare capital / running cost and maintenance before selection.'),
]
for i,(owner,inputs,output) in enumerate(rows):
    y=53+i*25;text(20,y,owner.upper(),2.8,True);text(98,y,inputs,2.7);text(98,y+8,output,2.7,fill='muted');m.line(20,y+18,398,y+18,'line',.12)
text(20,212,'CURRENT PRIMARY REFERENCES / CHECKED 13 SEPTEMBER 2026',3.1,True)
SOURCES=[('Energy Saving Trust: room-by-room heat loss','https://greenheattoolkit.energysavingtrust.org.uk/t/heat-pump-installers-toolkit/heat-pump-system-design/heat-loss-calculations-detailed-guidance/'),
 ('Zehnder: ventilation system selection and duties','https://www.zehnder.co.uk/en/indoor-ventilation/resources/mvhr-selection-tool'),
 ('Energy Saving Trust: battery storage','https://energysavingtrust.org.uk/advice/battery-storage/'),
 ('GOV.UK: Approved Document O; applicability / edition to confirm for project','https://www.gov.uk/government/publications/overheating-approved-document-o')]
for i,(label,url) in enumerate(SOURCES):
    y=223+i*9;text(20,y,label,2.7,fill='green');m.c.linkURL(url,(20*m.mm,(297-y-2)*m.mm,390*m.mm,(297-y+4)*m.mm),relative=0)
m.c.showPage();m.c.save()
(OUT/'concept-21-study-check.json').write_text(json.dumps({'status':'Preliminary coordination; technical design pending',
 'uses_unselected_plant_option':'B','concept_routes':ROUTES,'plan_route_lengths_m':LENGTHS,'routes_are_not_sized_installation_paths':True,
 'cooled_room_ids':COOLED,'gross_roof_ceiling_zone_m':GROSS_ZONE,'gross_zone_is_not_usable_duct_void':True,
 'shared_edge_band_proposal':{'projection_m':.5,'height_m':.4,'underside_m':2.7,'top_m':3.1,'adopted':False},
 'roof_shade_vent_plan_overlap':False,'plant_extension_adopted':False,
 'heat_loss_calculated':False,'cooling_loads_calculated':False,'ventilation_sized':False,'hot_water_sized':False,'solar_energy_balance_calculated':False,'site_verified':False,
 'sources':SOURCES},indent=2)+'\n')
print(PDF);print(LENGTHS)
