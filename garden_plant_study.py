"""Concept 22: garden-side plant, internal access and wing cooling strategy."""
import copy
import hashlib
import json
from dataclasses import asdict
from math import hypot, ceil
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,BASE_DATA=load_model();BASE_OUTLINE=copy.deepcopy(m.OUTLINE)
BASE_ROOMS=copy.deepcopy(m.rooms);BASE_WINDOWS=copy.deepcopy(m.windows)
GYM_BASE=copy.deepcopy([f for f in m.furniture if f['room']=='GY'])
PLANT_OUTER=(22.45,8.70,4.70,3.00)
PLANT_CLEAR=(22.80,9.05,4.00,2.65)
m.OUTLINE=[(0,0),(8.2,0),(8.2,12.8),(12.2,12.8),(12.2,9.3),(16.2,9.3),(16.2,0),(22.8,0),(22.8,8.7),(27.15,8.7),(27.15,18.4),(0,18.4)]
m.INNER=[(.35,.35),(7.85,.35),(7.85,13.15),(12.55,13.15),(12.55,9.65),(16.55,9.65),(16.55,.35),(22.45,.35),(22.45,9.05),(26.8,9.05),(26.8,18.05),(.35,18.05)]
m.room('PL','Garden-side plant',*PLANT_CLEAR,'service',10.6,label=(24.8,10.6),lines=('Plant',))
m.R['PL']=m.rooms[-1]
removed=[w for w in m.windows if w[0]=='v' and w[1]==22.8 and w[2]==9.8]
assert len(removed)==1
m.windows=[w for w in m.windows if w not in removed]
ROOFLIGHT=(18.65,9.95,1.10,1.10)
assert all(m.inside(p,m.R['S'].poly) for p in m.box(*ROOFLIGHT))
GYM_ITEMS=[('Combined rack / cables',(22.85,16.80,2.40,1.10),'cabinet'),
 ('Bench',(24.05,13.70,.70,1.50),'bench'),
 ('Treadmill',(25.55,13.25,1.00,2.05),'cabinet'),
 ('Dumbbells',(22.90,13.50,.40,2.00),'cabinet')]
m.furniture=[f for f in m.furniture if f['room']!='GY']
for name,r,kind in GYM_ITEMS:m.furn('GY',name,*r,kind)
for old in GYM_BASE:
    new=next(f for f in m.furniture if f['room']=='GY' and f['name']==old['name'])
    assert sorted(old['rect'][2:])==sorted(new['rect'][2:])
for d in m.doors:
    if d.id=='D18':d.y=15.60
INTERNAL=m.Door('D21','GY','PL',23.40,11.875,.90,False,hinge_end=True,side=-1,thickness=.35)
EXTERNAL=m.Door('D22','PL','OUT',26.975,9.50,1.00,True,side=1,thickness=.35)
m.doors.extend([INTERNAL,EXTERNAL])
EQUIPMENT=[('P1 cylinder / connections',(22.95,9.20,.90,.90)),
 ('P2 ventilation allowance',(25.95,10.60,.65,.85)),
 ('P3 hydraulic / controls',(24.10,9.20,.80,.45))]
SERVICE=[(22.95,10.10,.9,1),(24.95,10.60,1,.85),(24.10,9.65,.8,1)]
for name,r in EQUIPMENT:m.furn('PL',name,*r,'plant')
TREADMILL_REAR=(25.35,15.45,1.35,2.20)
assert not any(m.overlap(TREADMILL_REAR,f['rect'])>1e-8 for f in m.furniture)
for r in SERVICE:
    assert all(m.inside(p,m.R['PL'].poly) for p in [(r[0]+.001,r[1]+.001),(r[0]+r[2]-.001,r[1]+r[3]-.001)])
    assert not any(m.overlap(r,e)>1e-8 for _,e in EQUIPMENT)
m.routes['Boot to gym']=[(20.25,17.1),(21.0,16.65),(21.65,16.05),(22.625,16.05),(23.675,16.05)]
m.routes['Gym to plant']=[(23.675,16.05),(23.675,12.70),(23.85,12.50),(23.85,11.40),(23.85,10.55)]
m.routes['Plant cylinder approach']=[(23.85,10.55),(23.40,10.55)]
m.routes['Plant ventilation approach']=[(23.85,10.55),(24.7,10.55),(25.45,11.00)]
m.routes['Plant controls approach']=[(23.85,10.55),(24.5,10.55),(24.5,10.15)]
m.routes['Plant external door approach']=[(23.85,10.55),(24.70,10.55),(26.35,10.05)]
del m.routes['Snug to window']
m.routes['Snug rooflight control']=[(19.75,10.66),(18.55,10.66),(18.55,10.0)]
ISSUES=m.verify();assert not ISSUES,ISSUES
OPEN_INTERNAL=(24.28,10.98,.04,.87)
for name in ['Gym to plant','Plant cylinder approach','Plant ventilation approach','Plant controls approach','Plant external door approach']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):
        count=max(1,ceil(hypot(b[0]-a[0],b[1]-a[1])/.025))
        for i in range(count+1):
            x=a[0]+i/count*(b[0]-a[0]);y=a[1]+i/count*(b[1]-a[1]);X,Y,W,H=OPEN_INTERNAL
            assert hypot(max(X-x,0,x-X-W),max(Y-y,0,y-Y-H))>=.35-1e-8,(name,x,y)
assert m.rooms[:-1]==BASE_ROOMS
assert abs(m.polygon_area(m.OUTLINE)-m.polygon_area(BASE_OUTLINE)-13.05)<1e-8
OUT=ROOT/'output/pdf';PDF=OUT/'concept-22-garden-plant-and-wing-services.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 22 - garden plant and wing services')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.75,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 22 / GARDEN PLANT + WING SERVICES',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.7,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'REVISED PROPOSAL | Equipment / rooflight sizes and services are allowances. No capacity, acoustic, daylight, site or construction approval.',2.3,fill='muted')
    text(406,287,f'{n} / 6',2.6,align='right',fill='muted')
def crop(p,r):
    x,y,w,h=r;m.c.saveState();clip=m.c.beginPath();clip.rect(x*m.mm,(297-y-h)*m.mm,w*m.mm,h*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False);m.c.restoreState()
def rooflight(p):
    p.rect(*ROOFLIGHT,None,'green',.35);x,y,w,h=ROOFLIGHT;p.line((x,y),(x+w,y+h),'green',.2,[1,1]);p.line((x+w,y),(x,y+h),'green',.2,[1,1])
header(1,'Put plant behind the gym, with a door from inside','Full-house location plan 1:100 at A3 | Garden / south up; arrival / north down | Previous arrival-side addition declined')
p=m.Plan(23,57,10);p.draw(labels=False);rooflight(p)
p.rect(*PLANT_CLEAR,None,'green',.65)
p.text(24.8,10.6,'PLANT',2.8);p.text(24.8,15.8,'FULL GYM',2.8);p.text(20.0,10.8,'SNUG',2.5)
p.text(12.0,3.0,'GARDEN / SOUTH',3);p.text(17.9,19.1,'ARRIVAL / NORTH',2.8)
for id in ['D18','D21','D22']:
    d=next(d for d in m.doors if d.id==id);p.text(d.x-.3,d.y-.3,id,2.3,fill='green')
note(315,54,'REVISED LOCATION',[
 'Continues the existing gym block',
 'toward the garden, beside the snug.',
 'No projection past the arrival front.',
 '4.00 x 2.65 m clear plant room.',
 '13.05 m2 added external footprint.' ])
note(315,109,'INTERNAL AND EXTERNAL ACCESS',[
 'Boot room -> gym -> plant room.',
 'D21: 0.90 m opening allowance.',
 'D22: separate 1.00 m outside opening.',
 'Frames / clear widths unselected.',
 'External access supports replacement.' ])
note(315,164,'SNUG CHANGE',[
 'Existing side window is covered.',
 'Replace it with a rooflight proposal.',
 'TV, sofa and reading use stay.',
 'A rooflight brings sky light, not a view.',
 'Blackout and ventilation need design.' ])
note(315,220,'GYM CHANGE',[
 'Retains all equipment and 24 m2.',
 'Rack and dumbbells move.',
 'Boot-to-gym door shifts 0.60 m.',
 'Treadmill and bench stay in place.' ])
text(23,260,'The retained side wall overlaps 1.05 m2 of the 4.70 x 3.00 m study rectangle; net new footprint is 13.05 m2.',2.7,fill='muted')
m.c.showPage()
header(2,'An interior route without reducing the gym','Gym and plant detail 1:50 at A3 | Equipment body envelopes retained | Amber = equipment service / treadmill rear reservations')
p=m.Plan(29-22.45*20,59-8.7*20,20);crop(p,(20,49,135,209))
for r in SERVICE+[TREADMILL_REAR]:p.rect(*r,None,'amber',.3)
for name in ['Gym to plant','Plant ventilation approach']:
    for a,b in zip(m.routes[name],m.routes[name][1:]):p.line(a,b,'green',.4,[1,1])
for name,r in EQUIPMENT:
    x,y,w,h=r;p.text(x+w/2,y+h/2,name[:2],2.5)
p.text(24.1,17.4,'RACK / CABLES',2.4);p.text(26.03,14.3,'RUN',2.2)
p.dimension((22.8,9.05),(26.8,9.05),-.5,'4.00 m clear')
note(206,54,'PLANT FIT TEST',[
 'P1: 0.90 x 0.90 m cylinder / connections allowance.',
 'P2: 0.65 x 0.85 m ventilation allowance.',
 'P3: 0.80 x 0.45 m hydraulic / control allowance.',
 'Each has a 1.00 m front floor reservation.',
 'Capacities, vessels, valves, ducts and drains remain unsized.' ])
note(206,108,'GYM REARRANGEMENT',[
 'Rack / cables move to the arrival-end wall.',
 'Dumbbell storage turns onto the side wall.',
 'The bench and treadmill remain in their original positions.',
 'Retain the provisional 1.35 x 2.20 m treadmill rear zone.',
 'D18 moves from y=16.20 to 15.60 m to clear the rack.' ])
note(206,162,'WHAT HAS BEEN CHECKED',[
 f'{len(m.routes)} sampled house / equipment approach routes pass.',
 'Room doors clear the drawn equipment; internal D21 opens into plant.',
 'The new approach routes also clear the fully open D21 leaf.',
 'All existing room polygons and equipment body sizes are retained.',
 'Exercise movements, cable travel and barbell handling are unverified.' ])
note(206,218,'DETAILS STILL TO RESOLVE',[
 'Internal door sound separation and any required fire performance.',
 'Acoustic mounting on the snug side; quieter equipment positioning.',
 'External landing, removal handling, drainage and actual boundaries.',
 'Roof structure and both new door lintels need coordination.' ])
m.c.showPage()
header(3,'Keep the snug for films; bring daylight from above','Snug plan 1:25 at A3 | 1.10 x 1.10 m rooflight opening reservation | Existing furniture retained')
p=m.Plan(29-17.87*40,67-9.46*40,40);crop(p,(17,53,220,126));rooflight(p)
p.text(19.20,10.52,'ROOFLIGHT',2.7,fill='green')
p.line((22.625,9.8),(22.625,11.3),'amber',.9);p.text(22.10,10.6,'INFILL',2.3,fill='amber')
note(256,55,'THE BENEFIT',[
 'Plant sits behind the gym, away from the arrival front.',
 'The snug retains its full 4.58 x 2.60 m room.',
 'Top light can work with a cinema / reading room.',
 'No plant access door is routed through the snug.' ])
note(256,103,'THE TRADE-OFF',[
 'The side view and existing opening window are lost.',
 'Specify blackout for daytime films and assess solar gain.',
 'Rain noise, glare and cleaning access need review.',
 'Choose fixed or opening rooflight with the ventilation design.',
 'An opening unit needs reachable controls and weather protection.' ])
note(25,207,'ROOF AND ACOUSTIC COORDINATION',[
 'Rooflight location is a spatial reservation, not a daylight calculation or a selected product.',
 'Check joists, trimmers, upstand, roof falls and gutter / outlet positions across the extended lower block.',
 'The plant-to-snug wall needs acoustic design; a rooflight does not solve plant noise.',
 'Keep ventilation independent of rooflight opening; reposition the general ceiling light around it.',
 'The plant front is only 0.25 m beyond the office window extent; assess roof-edge shading and outlook there.' ])
text(25,251,'Rooflight / blind options: VELUX flat-roof window accessories (linked in sources on page 6).',2.6,fill='green')
m.c.showPage()
header(4,'Separate the cooling systems by wing','Conceptual zones, not selected outdoor-unit counts or installation routes | No cross-vault cooling duct is assumed')
for x,title,lines in [(22,'FAMILY SIDE / COOLING GROUP A',['Parents + C1 + C2 + C3','Four bedroom zones','Outdoor unit on the family-side exterior']),
 (222,'SERVICE SIDE / COOLING GROUP B',['Guest bedroom + office + snug + gym','Four room zones','Outdoor unit on the gym / service-side exterior'])]:
    m.rect(x,54,176,71,'wet','green',.25);text(x+8,65,title,3.2,True);m.paragraph(x+8,76,lines,size=2.9,step=9)
note(22,146,'SHARED / GARDEN ROOM',[
 'Treat the connected living and garden space as its own load / control zone.',
 'Connect it to one wing system only if indoor connections and simultaneous',
 'capacity allow. A separate outdoor unit or more than one emitter may be needed.',
 'Do not count a single hallway head as cooling the closed bedrooms.' ])
note(222,146,'WHAT THE MULTI-SPLITS STILL NEED',[
 'Refrigerant pipes, power, condensate drainage and service access.',
 'Wall / floor units or short local ducts matched to each room.',
 'Room heat-gain calculations, line lengths and permitted combinations.',
 'Acoustic siting of outdoor and indoor units; no location is fixed here.' ])
note(22,214,'COOLING DISTRIBUTION DIRECTION',[
 'The earlier cross-vault cooling band is no longer the assumed solution.',
 'Daikin documents multiple indoor units per outdoor unit; the final number',
 'depends on the product and room loads. Two outdoor units are a starting idea.' ])
note(222,214,'VENTILATION IS A SEPARATE QUESTION',[
 'MVHR supplies fresh air and removes stale / humid air.',
 'Multi-split cooling alone does not establish that ventilation.',
 'Compare wing ventilation systems / local solutions against a central route;',
 'unit positions, noise, balance and shared-room supply remain open.' ])
m.c.showPage()
header(5,'Hot water needs its own distribution decision','Same two simultaneous high-flow shower requirement | No cylinder size or heat-pump capacity selected')
note(22,55,'A / ONE CYLINDER AT THE SERVICE END',[
 'A separate air-to-water heat pump can serve hot water and proposed wet UFH.',
 'That normally adds an outdoor unit beyond the cooling outdoor units.',
 'Hot-water pipes still have to reach the family bathrooms.',
 'Investigate insulated runs within floor / service construction, so large',
 'overhead air ducts need not cross the shared room for hot water.',
 'Compare actual pipe lengths, waiting time and distribution heat loss.',
 'A controlled return loop is an option to calculate, not an automatic choice.' ])
note(222,55,'B / LOCAL HOT-WATER STORAGE',[
 'A second store nearer the family bathrooms shortens hot delivery runs.',
 'It adds equipment, maintenance, standing losses and connections.',
 'It would use family-side space that was intended to become linen storage.',
 'Heat input still needs routing or a separate source.',
 'This conflicts with the preference to keep major plant away from bedrooms;',
 'keep it as a comparison, not the default recommendation.' ])
note(22,129,'C / A COMBINED AIR-TO-AIR + HOT-WATER PRODUCT',[
 'Ordinary air-to-air units usually do not produce domestic hot water.',
 'Combined products exist, including Daikin Multi+ with a tank connection.',
 'Tank size, compatible indoor units and simultaneous duties are product-specific.',
 'The two high-flow showers and repeat-use recovery must be checked before selection.',
 'Do not assume this arrangement also supplies the proposed wet underfloor heating.' ])
note(222,129,'RECOMMENDED NEXT COMPARISON',[
 'Begin with A, keeping the full gym and laundry while avoiding a cooling duct crossing.',
 'Compare C if it can satisfy the hot-water brief and the chosen heating strategy.',
 'Use B only if the shorter hot-water runs justify extra family-side equipment.',
 'Confirm whether winter heat stays as wet UFH or also uses the air-to-air systems.',
 'That choice changes the plant package more than moving an equipment rectangle.' ])
note(22,208,'WHAT THE DRAWING CANNOT YET ESTABLISH',[
 'Water supply pressure / flow, shower flow rates and duration, recovery and usable storage are not known.',
 'Floor build-up, pipe zones, penetrations, insulation and service access need coordinated design.',
 'Solar intent remains: model daylight generation and evening / night demand, with battery / grid contribution explicit.' ])
m.c.showPage()
header(6,'Resolve systems and the building envelope before more room detailing','Next decisions and current technical references | Preliminary concept development')
note(22,55,'1 / CONFIRM THE ARCHITECTURAL DIRECTION',[
 'Garden-side plant with access through the gym, revised D18 and snug rooflight.',
 'Accept the loss of the snug side view and check plant-to-snug sound isolation.',
 'Keep the original plant placeholder until a complete relocation is designed.' ])
note(22,97,'2 / CHOOSE THE SERVICES PRINCIPLE',[
 'Separate wing cooling; solve ventilation separately.',
 'Decide winter heating: retained wet UFH, air-to-air heat, or a defined combination.',
 'Size hot water for two simultaneous rain showers and repeat use.' ])
note(222,55,'3 / COORDINATE ROOF, WINDOWS AND SITE',[
 'Actual site, orientation, boundaries, levels and outdoor-unit locations.',
 'Continuous lower-block roof falls, structure, rooflight and access.',
 'Glazing / shading / fabric assumptions for heat-loss and cooling calculations.' ])
note(222,97,'4 / CHECK COST AND DAILY OPERATION',[
 'Budget the chosen footprint and system package before detailed joinery.',
 'Check noise, controls, maintenance access and energy use together.',
 'Physical room / door mock-ups remain useful for final comfort checks.' ])
text(22,156,'PRIMARY REFERENCES / CHECKED 13 SEPTEMBER 2026',3.3,True)
SOURCES=[('Daikin: multi-split room connections and combined hot-water option','https://www.daikin.co.uk/en_gb/residential/products-and-advice/product-categories/heat-pumps/air-to-air-heat-pumps/multi-split.html'),
 ('Energy Saving Trust: air-to-air heat pumps and usual hot-water limitation','https://energysavingtrust.org.uk/advice/air-to-air-heat-pumps/?cats%5B%5D=1782'),
 ('Energy Saving Trust: air-to-water heat pumps','https://energysavingtrust.org.uk/advice/air-source-heat-pumps?loc=wales'),
 ('Zehnder: MVHR duties and ventilation system options','https://www.zehnder.co.uk/en/indoor-ventilation/resources/mvhr-selection-tool'),
 ('VELUX: light / heat / glare control for flat-roof windows','https://www.velux.co.uk/products/blinds-and-shutters/blinds-for-flat-roof-windows')]
for i,(label,url) in enumerate(SOURCES):
    y=169+i*13;text(22,y,label,2.8,fill='green');m.c.linkURL(url,(22*m.mm,(297-y-2)*m.mm,397*m.mm,(297-y+4)*m.mm),relative=0)
text(22,248,'Manufacturer examples explain system types; no supplier, equipment capacity or installation layout is selected.',2.8,fill='muted')
m.c.showPage();m.c.save()
(OUT/'concept-22-study-check.json').write_text(json.dumps({'status':'Revised garden-side plant proposal; arrival-side option declined',
 'model':{'rooms':[asdict(r) for r in m.rooms],'doors':[asdict(d) for d in m.doors],'windows':m.windows,'outline':m.OUTLINE,'inner':m.INNER},
 'furniture':m.furniture,'routes':m.routes,'issues':ISSUES,'base_sources':BASE_DATA['model_sources'],
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'plant_clear_m':PLANT_CLEAR,'net_added_footprint_m2':13.05,'snug_window_removed':removed,'snug_rooflight_reservation_m':ROOFLIGHT,
 'gym_area_retained_m2':24,'gym_equipment_body_sizes_retained':True,'treadmill_rear_reservation_m':TREADMILL_REAR,
 'equipment':EQUIPMENT,'service_reservations':SERVICE,'internal_door_open_leaf_checked':True,
 'cooling_strategy':'Separate wing multi-splits; shared room load and connection allocation open','cooling_duct_crossing_assumed':False,
 'ventilation_distribution_resolved':False,'hot_water_sized':False,'winter_heat_choice_open':True,'sources':SOURCES},indent=2)+'\n')
print(PDF);print(f'{len(m.routes)} routes pass; 13.05 m2 net addition; all original room polygons retained.')
