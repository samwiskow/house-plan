"""Concept 11: Northumberland orientation and year-round comfort intent."""
import ast
import json
from math import cos, sin, tan, radians, hypot
from pathlib import Path

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'shared_space_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'shared_space_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'shared_space_study.py'),'exec'),s)
m=s['m']
court=json.loads((ROOT/'output/pdf/concept-09-study-check.json').read_text())
OUT=ROOT/'output/pdf';PDF=OUT/'concept-11-year-round-comfort.pdf'
LATITUDE=55.2
NOON={name:round(90-LATITUDE+declination,1) for name,declination in [('Summer solstice',23.44),('Equinox',0),('Winter solstice',-23.44)]}
ROOF=(12.55,9.65,4,3.15)
SHADE=(12.55,9.65,4,2.2)
VENTS=[(12.9,12.1,.8,.5),(14.7,12.1,.8,.5)]
for r in [SHADE,*VENTS]:
    assert r[0]>=ROOF[0] and r[1]>=ROOF[1]
    assert r[0]+r[2]<=ROOF[0]+ROOF[2]+1e-8 and r[1]+r[3]<=ROOF[1]+ROOF[3]+1e-8
assert all(m.overlap(SHADE,r)==0 for r in VENTS)
assert not m.verify()
C={'paper':'#fffdf8','ink':'#30392f','muted':'#6a6656','line':'#cec3b2','blue':'#477e8b','green':'#376248',
   'heat':'#b97447','sun':'#c58a30','roof':'#e8deca','glass':'#dce9e5','shade':'#b5c2a1',
   'family':'#f1eee6','shared':'#f2e7d5','guest':'#f1eee6','service':'#f1eee6','circulation':'#faf7ef','furniture':'#deccac'}
m.PALETTE.update(C)
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm))
m.c.setTitle('Concept 11 - Northumberland, south-facing courtyard, year-round comfort')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines,size=2.8):
    text(x,y,title,3.15,True)
    m.paragraph(x,y+7,lines,size=size,step=5)
def arrow(a,b,colour='blue',width=.45):
    m.line(*a,*b,colour,width)
    dx,dy=b[0]-a[0],b[1]-a[1];n=hypot(dx,dy);ux,uy=dx/n,dy/n
    for side in [-1,1]:m.line(*b,b[0]-2.2*ux+side*uy,b[1]-2.2*uy-side*ux,colour,width)
def badge(p,x,y,label):
    X,Y=p.xy((x,y));m.rect(X-3.4,Y-2.8,6.8,4.8,'paper','green',.2);text(X,Y+.7,label,2.6,True,align='center',fill='green')
def header(page,title,sub):
    m.rect(0,0,420,297,'paper',None)
    text(14,12,'COURTYARD HOUSE / CONCEPT 11 / YEAR-ROUND COMFORT',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.8,fill='muted')
    m.line(14,36,406,36,'line',.3);m.line(14,280,406,280,'line',.25)
    text(14,287,'DESIGN INTENT | No heat-loss, airflow, overheating, daylight or regulatory compliance result. Dimensions of systems remain provisional.',2.35,fill='muted')
    text(406,287,f'{page} / 3',2.6,align='right',fill='muted')

header(1,'South-facing courtyard, one connected interior','Working location: Northumberland | Plan 1:100 at A3, printed at 100% | South is at the top; north at the bottom')
p=m.Plan(20,54,10)
m.c.saveState();clip=m.c.beginPath();clip.rect(14*m.mm,(297-242)*m.mm,214*m.mm,193*m.mm);m.c.clipPath(clip,stroke=0)
p.poly(court['court_polygon_m'],'#e5ead7',None)
for r in court['paving_rectangles_m']:p.rect(*r,'#e6dac3',None)
for _,r in court['planting_beds']:p.rect(*r,'shade',None)
for _,r,_,_ in court['outdoor_furniture']:p.rect(*r,'furniture','muted',.12)
oldf,oldd=m.furniture,m.doors
m.furniture=[f for f in oldf if f['room'] in ('KL','OR','PA','WC')]
m.doors=[d for d in oldd if d.id not in ('O05','O07')]
p.draw(labels=False);m.furniture,m.doors=oldf,oldd
m.rect(21,55,76,125,'family',None)
p.rect(*ROOF,None,'blue',.35)
p.rect(*SHADE,'shade','green',.3)
for y in [9.9,10.25,10.6,10.95,11.3,11.65]:p.line((12.55,y),(16.55,y),'green',.15)
for r in VENTS:p.rect(*r,'glass','blue',.5)
for room in ['KL','OR']:p.poly(m.R[room].poly,None,'heat',.6)
for x,y,l in [(14.5,10.7,'S1'),(13.3,12.35,'V2'),(15.1,12.35,'V2'),(14.4,9.35,'V1'),(8.0,18.05,'V3'),(15.9,14.35,'H1')]:badge(p,x,y,l)
for a,b in [((14.4,8.4),(14.4,9.8)),((14.3,11.7),(14.3,12.7)),((12.3,14.3),(9.1,16.7)),((8,17.2),(8,18.65))]:arrow(p.xy(a),p.xy(b))
p.line((9,12.76),(11.6,12.76),'green',.8)
p.line((13,9.4),(15.8,9.4),'green',.8)
p.line((12.48,10.4),(12.48,11.9),'green',.8)
p.text(10.25,12.3,'S2',2.8,fill='green');p.text(11.9,11.15,'S3',2.8,fill='green')
p.line((13.2,8.85),(13.2,18.4),'muted',.2,[1.5,1]);p.text(13.2,8.65,'A',2.8);p.text(13.2,18.7,'A',2.8)
p.text(10.5,2,'SOUTH / GARDEN',3,fill='green')
p.text(4.1,7,'FAMILY WING',3);p.text(4.1,7.6,'Court windows face west',2.5,fill='muted')
p.text(5.3,14,'H1 / WET UNDERFLOOR HEATING',2.7,fill='heat')
p.text(15.2,16.8,'PANTRY',2.4);p.text(18.75,13.1,'WC',2.4)
m.c.restoreState()
text(23,251,'Blue arrows: possible purge path, not predicted airflow.',2.6,fill='muted')
text(23,257,'Warm outline: heating design area, not pipe loops.',2.6,fill='muted')
for i in range(5):m.rect(23+i*10,265,10,1,'ink' if i%2==0 else 'paper','ink',.1)
text(23,273,'0',2.4);text(73,273,'5 m',2.4,align='right')
arrow((183,249),(183,267),'ink');text(183,273,'N',3,True,align='center');text(183,246,'S',3,align='center')
text(175,258,'E',3,align='center');text(192,258,'W',3,align='center')
note(243,49,'S1 / SHADE THE ROOF FIRST',[
 'Retractable external roof shade below the high vent strip.',
 'Retain insulating solar-control glass throughout.',
 'The unshaded upper strip needs explicit solar testing.' ])
note(243,79,'S2 + S3 / SHADE THE VERTICAL GLASS',[
 'Reserve external screens at the south dining / garden sliders',
 '(S2) and east-facing garden-room side window (S3).',
 'Retain the current opening widths and bronze frames.' ])
note(243,109,'V1 - V3 / A ROUTE FOR EXCESS HEAT',[
 'V1: attended south door opening; secure intake to design.',
 'V2: two high roof vent reservations, subject to pitch / system.',
 'V3: opening portions in the north dining window.',
 'Keep widths fixed; calculate effective opening areas.' ])
note(243,144,'H1 / HEAT THE CONNECTED SPACE',[
 'Develop wet underfloor heating with a heat-pump design.',
 'Coordinate garden / shared-room loops and controls.',
 'Exclude fixed joinery and hearth; size from heat loss.',
 'Check comfort by glass before deciding on extra emitters.' ])
note(243,179,'FRESH AIR AND SERVICES',[
 'Study whole-house MVHR separately from summer purge.',
 'Reserve accessible duct routes in service / hall ceilings.',
 'Plant, terminals and manifolds have no selected locations.',
 'Keep the vault, lighting ledges and roof head coordinated.' ])
note(243,214,'ORIENTATION CHANGES THE CHECKS',[
 'South-facing roof and front glass: priority solar assessment.',
 'West-facing family windows: check afternoon bedroom gains.',
 'Courtyard shelter, trees and neighbouring shadows unknown.' ])
note(243,249,'SITE ASSUMPTION',[
 'Northumberland; due-south courtyard axis for this study.',
 'Exact plot, exposure, altitude and weather file remain open.' ])
m.c.showPage()

header(2,'Give the shade and vents their own space','Section A-A at plan x = 13.20 m | 1:50 at A3 | South / courtyard left; north / rear right | Heights retained from concept 07B')
base=175;pt=lambda y,z:(22+(y-8.8)*20,base-z*20)
glass=lambda y:2.85+(y-9.3)*.6/3.5
ceiling=lambda y:3.5+min(y-13.15,18.05-y)*tan(radians(30))
roof=lambda y:3.7+min(y-12.8,18.4-y)*tan(radians(30))
m.poly([pt(9.3,glass(9.3)),pt(12.8,glass(12.8)),pt(12.8,glass(12.8)-.1),pt(9.3,glass(9.3)-.1)],'glass','blue',.3)
m.poly([pt(12.8,roof(12.8)),pt(15.6,roof(15.6)),pt(18.4,roof(18.4)),pt(18.4,ceiling(18.4)),pt(15.6,ceiling(15.6)),pt(12.8,ceiling(12.8))],'roof','ink',.3)
m.poly([pt(12.8,3.1),pt(13.15,3.1),pt(13.15,3.5),pt(12.8,3.5)],'shared','ink',.3)
m.line(*pt(9.475,0),*pt(9.475,2.85),'blue',.6)
m.line(*pt(18.225,0),*pt(18.225,3.5),'ink',.8)
m.line(*pt(8.8,0),*pt(18.4,0),'ink',.6)
m.line(*pt(9.65,.07),*pt(18.05,.07),'heat',1)
for y in [10.3,11.5,13.8,15.2,16.6,17.5]:arrow(pt(y,.15),pt(y,.55),'heat',.35)
m.line(*pt(9.65,glass(9.65)+.18),*pt(11.85,glass(11.85)+.18),'green',1.3)
m.line(*pt(12.1,glass(12.1)),*pt(12.6,glass(12.6)+.28),'blue',.8)
arrow(pt(10.2,.9),pt(11.6,2),'blue');arrow(pt(11.6,2),pt(12.3,3.85),'blue')
for y,z,label in [(10.6,3.7,'S1 / SHADE'),(12.3,4.45,'V2 / VENT'),(15.6,5.75,'RIDGE +5.32'),(10.4,2.35,'GLASS +2.85 TO +3.45')]:text(*pt(y,z),label,2.6,True,align='center',fill='green' if 'S1' in label else 'ink')
text(*pt(10.9,-.7),'GARDEN ROOM / SOUTH',2.8,align='center');text(*pt(15.7,-.7),'SHARED ROOM / NORTH',2.8,align='center')
note(243,49,'THE JUNCTION TO RESOLVE',[
 'Stop the shade at y = 11.85 m in this reservation.',
 'Keep roof vents in the upper strip at y = 12.10-12.60 m.',
 'This avoids overlap in plan, not a proven assembly fit.',
 'The remaining upper glass strip is approximately 0.95 m.' ])
note(243,84,'WHAT THE SUPPLIERS MUST COORDINATE',[
 'Actual roof pitch, vent upstands and weathering.',
 'Shade cassette, guide rails, fixings and maintenance access.',
 'Opening vent sweep and wind / rain controls.',
 'Drainage below the main eave and around the vents.',
 'A compatible system may require a revised junction.' ])
note(243,124,'KEEP THE INTERIOR INTENT',[
 'Retain the 3.10 m opening head and continuous floor.',
 'Run services within planned hall / service ceiling zones.',
 'Keep ambient lighting ledges and drivers accessible.',
 'Do not fill the vault with ad hoc ducts or blind boxes.' ])
note(243,164,'VENTILATION IS A DESIGN RESERVATION',[
 'No opening free area or exhaust capacity is established.',
 'Select a low-pitch-compatible system and test it together',
 'with the external shade and secure air inlet.' ])
m.line(14,198,406,198,'line',.3)
note(20,208,'GLASS + FRAME',[
 'Specify whole-unit insulation and solar performance.',
 'Check visible light, neutral appearance and glare.',
 'Review edge temperatures, airtightness and',
 'thermal bridges at the roof / frame junction.' ],2.65)
note(151,208,'FLOOR + HEATING',[
 'Keep insulation continuous at the glazed threshold.',
 'Check usable heated floor area and floor finish.',
 'Use coordinated controls for the open interior.',
 'The stove is an optional local heat source;',
 'its output must suit the calculated room demand.' ],2.65)
note(282,208,'IF PASSIVE MEASURES FALL SHORT',[
 'Test shading and usable ventilation first.',
 'If modelling still shows overheating, investigate',
 'targeted active cooling with a services designer.',
 'No cooling capacity or location is selected.' ],2.65)
m.c.showPage()

header(3,'Let the house behave differently by season','Operating intent and a simple solar-noon comparison | Illustrations are not a weather simulation or a prediction of indoor temperature')
for x,season,angle in [(20,'SUMMER SOLSTICE',NOON['Summer solstice']),(218,'WINTER SOLSTICE',NOON['Winter solstice'])]:
    text(x,48,f'{season} / APPROX. {angle:.1f} DEGREES',3.15,True)
    anchor=(x+90,111);a=radians(angle);start=(anchor[0]-60*cos(a),anchor[1]-60*sin(a))
    m.line(x+18,111,x+115,111,'line',.3)
    arrow(start,anchor,'sun',.65)
    m.c.setFillColor(m.color('sun'));m.c.circle(start[0]*m.mm,(297-start[1])*m.mm,2*m.mm,stroke=0,fill=1)
    text(x+118,91,'Solar noon',2.7);text(x+118,97,'Sun due south',2.7)
    text(x+118,103,'Flat horizon assumed',2.5,fill='muted')
for x,title,colour,steps in [
 (20,'SUNNY SUMMER DAY','green',['Shade deployed','Fresh air maintained','Purge if outside is cooler']),
 (151,'COOLER SUMMER NIGHT','blue',['Secure intake + high vent','Purge only while cooler','Rain / wind / security control']),
 (282,'WINTER DAY','heat',['Shade retracted as useful','Heat recovery + steady heating','Purge vents normally closed'])]:
    m.rect(x,123,118,63,'#f3eddf',None);text(x+5,132,title,3.1,True)
    for i,step in enumerate(steps):
        y=143+i*13;text(x+5,y,step,2.85)
        if i<2:arrow((x+8,y+2),(x+8,y+8),colour,.3)
text(20,196,'Angles use a representative latitude of 55.2 N: altitude = 90 - latitude + solar declination. Equinox: 34.8 degrees.',2.65,fill='muted')
text(20,202,'No plot coordinates, horizon, shade duration or wind direction are inferred. Closed-door night use needs a designed secure inlet.',2.65,fill='muted')
note(20,214,'NEXT TECHNICAL CHECK',[
 'Model the connected interior and the bedrooms using site-appropriate current / future weather.',
 'Test glazing, shade, usable openings, occupancy and heat gains; calculate room-by-room winter heat loss.',
 'Select opening areas, heating output and control settings from those results. Confirm the applicable regulations.' ],2.8)
text(20,245,'References supporting the design brief; no compliance assessment has been carried out:',2.65,fill='muted')
refs=[('CIBSE: year-round comfort and overheating','https://www.cibse.org/policy-advocacy/key-policy-areas/health-and-wellbeing/overheating-position-statement/'),
      ('GOV.UK: Overheating (Document O)','https://www.gov.uk/government/publications/overheating-approved-document-o'),
      ('Energy Saving Trust: wet underfloor heating','https://energysavingtrust.org.uk/advice/underfloor-heating/')]
for y,(label,url) in zip([252,259,266],refs):
    text(20,y,label,2.7,fill='green');m.c.linkURL(url,(20*m.mm,(297-y-1)*m.mm,190*m.mm,(297-y+4)*m.mm),relative=0)
text(220,259,'Ventilation guidance (Document F)',2.7,fill='green')
m.c.linkURL('https://www.gov.uk/government/publications/ventilation-approved-document-f',(220*m.mm,37*m.mm,390*m.mm,43*m.mm),relative=0)
m.c.showPage();m.c.save()
(OUT/'concept-11-study-check.json').write_text(json.dumps({
 'working_location':'Northumberland, England','courtyard_faces':'south','plan_up':'south','plan_down':'north','plan_left':'east','plan_right':'west',
 'latitude_for_solar_illustration_deg':LATITUDE,'latitude_is_plot_coordinate':False,'solar_noon_altitudes_deg':NOON,
 'roof_plan_m':ROOF,'shade_reservation_m':SHADE,'roof_vent_reservations_m':VENTS,'shade_vent_plan_overlap_issues':[],
 'unshaded_upper_roof_strip_m':.95,'room_geometry_changed':False,'route_issues':[],
 'heat_loss_calculated':False,'thermal_simulation_completed':False,'airflow_calculated':False,'compliance_verified':False,
 'technical_next_step':'Site-specific year-round thermal modelling, room heat loss and roof shade/vent coordination',
 'sources':[url for _,url in refs]+['https://www.gov.uk/government/publications/ventilation-approved-document-f']},indent=2)+'\n')
print(PDF)
print('Three A3 sheets; orientation, retained routes and roof reservation checks pass.')
