"""Concept 26: coordinated services options and transparent demand examples."""
import hashlib
import json
import math
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,BASE=load_model()
PLAN=json.loads((ROOT/'output/pdf/concept-25-study-check.json').read_text())
assert hashlib.sha256((ROOT/'revised_house_plan.py').read_bytes()).hexdigest()==PLAN['source_sha256']
SOURCES=[
 ('Energy Saving Trust: air-to-water heating and hot water','https://energysavingtrust.org.uk/advice/air-source-heat-pumps/'),
 ('Energy Saving Trust: air-to-air heating and cooling','https://energysavingtrust.org.uk/advice/air-to-air-heat-pumps/'),
 ('Daikin Multi+: system and tank options','https://www.daikin.co.uk/en_gb/residential/products-and-advice/product-categories/heat-pumps/air-to-air-heat-pumps/multi-plus-split.html'),
 ('Daikin user guide: priority operation, pages 35-36','https://www.daikin.co.uk/content/dam/document-library/user%20reference%20guide/opt-and-acc/ckhws-bv3-ckhwsu-bv3/CKHWS-BV3.CKHWSU-BV3_User%20reference%20guide_4PEN779552-1_English.pdf'),
 ('Zehnder: MVHR and equipment access','https://www.zehnder.co.uk/en/indoor-ventilation/solutions/mechanical-ventilation-with-heat-recovery?stay=true'),
 ('Vaillant: dedicated hot-water heat pump example','https://professional.vaillant.co.uk/for-installers/products/arostor-domestic-hot-water-heat-pump-200-litre-145477.html'),
 ('Zehnder: air distribution components','https://www.zehnder.co.uk/en/indoor-ventilation/solutions/air-distribution?stay=true')]
SHOWERS=[]
for flow in [12,16,20]:
    mixed=2*flow*10
    SHOWERS.append({'each_shower_l_min':flow,'duration_min':10,'mixed_l':mixed,
      'ideal_hot_l':mixed*(40-10)/(55-10),'heat_kwh':mixed*4.186*(40-10)/3600})
PIPES=[]
for bore in [16,20]:
    litres=math.pi*(bore/1000)**2/4*30*1000
    PIPES.append({'internal_bore_mm':bore,'example_length_m':30,'water_l':litres,'flush_seconds_at_6_l_min':litres/6*60})
assert SHOWERS[1]['mixed_l']==320 and abs(SHOWERS[1]['ideal_hot_l']-213.3333333)<1e-6
assert 6.03<PIPES[0]['water_l']<6.04 and 9.42<PIPES[1]['water_l']<9.43
SUPPLY={'family':['P','C1','C2','C3'],'service_and_shared':['G','O','S','GY','KL','OR']}
EXTRACT={'family':['E','FB'],'service_and_shared':['GB','WC','L','KL']}
ids={r['id'] for r in PLAN['model']['rooms']}
assert set(sum(SUPPLY.values(),[])+sum(EXTRACT.values(),[]))<=ids
OUT=ROOT/'output/pdf';PDF=OUT/'concept-26-heating-hot-water-and-ventilation.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 26 - heating, hot water and ventilation')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.8,step=5.2)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 26 / SERVICES STRATEGY',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.7,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'STRATEGY STUDY | Underfloor preference confirmed. Other recommendations remain proposals; no equipment, duct or pipe size is selected.',2.3,fill='muted')
    text(406,287,f'{n} / 4',2.6,align='right',fill='muted')
def box(x,y,w,h,title,lines,fill='family'):
    m.rect(x,y,w,h,fill,'line',.2);text(x+5,y+9,title,3.2,True);m.paragraph(x+5,y+17,lines,size=2.65,step=5)
header(1,'Underfloor heating, separate cooling, one hot-water store','Recommended system architecture | Household of five; up to five overnight visitors | Northumberland working location')
box(20,51,117,53,'WINTER HEAT + HOT WATER [1]',[
 'Air-to-water heat pump at service end.',
 'Wet underfloor circuits via local manifolds.',
 'Cylinder in the proposed rear plant room.',
 'Capacity and store volume remain unselected.' ])
box(150,51,117,53,'ACTIVE COOLING [2]',[
 'Separate air-to-air systems for the wings.',
 'Room delivery with doors closed.',
 'Shared / garden space is its own load zone.',
 'Refrigerant, power and condensate routes.' ])
box(280,51,120,53,'FRESH AIR [5, 7]',[
 'Balanced mechanical ventilation with heat recovery.',
 'Compare one central unit with two local systems.',
 'Supply rooms; extract wet rooms and kitchen.',
 'See the distribution choice on page 2.' ])
note(20,122,'WHY THIS IS THE LEAD OPTION',[
 'You prefer underfloor heating for everyday winter comfort.',
 'Air-to-water equipment can serve both wet floors and the cylinder [1].',
 'Cooling remains independently available while hot water is reheated.',
 'Use local UFH manifolds; pipes can cross in the floor construction,',
 'subject to a coordinated build-up. They do not require a cooling duct',
 'across the shared vault. Agree control deadbands to avoid heating',
 'and cooling the same room at the same time.' ])
note(222,122,'THE COST AND SPACE TRADE-OFF',[
 'This adds a wet heating network alongside the cooling equipment.',
 'Allow for a separate air-to-water outdoor unit in addition to the two',
 'suggested wing cooling units. More cooling units may be needed',
 'once connection counts, shared-space loads and pipe limits are known.',
 'Keep cylinder, controls, expansion / hydraulic components and access',
 'within the plant design. A buffer is not automatically required;',
 'the selected system determines minimum flow and water volume.' ])
note(20,183,'ALTERNATIVE B / AIR HEATING + DEDICATED HOT WATER',[
 'Use the cooling units for winter heat; omit most wet-floor equipment [2].',
 'A dedicated heat-pump water heater is possible; some use air ducts [6].',
 'This reduces wet heating work but changes your preferred comfort.',
 'An indoor air-source water heater needs an air / noise / condensate',
 'design; taking heat from an occupied room creates a winter heat load.' ])
note(222,183,'ALTERNATIVE C / COMBINED AIR SYSTEM + HOT WATER',[
 'Multi+ is a real example: up to four indoor air units plus a tank [3].',
 'Its documented priority modes can interrupt cooling for hot water,',
 'or use the backup heater for water when air conditioning takes priority [4].',
 'It does not establish a wet-UFH solution for this house. With your floor',
 'preference and shower demand, retain it as a comparison, not the lead.' ])
text(20,258,'Recommendation is a house-specific judgement. No quoted costs, savings, capacities or final outdoor-unit count are inferred.',2.75,fill='muted')
m.c.showPage()
header(2,'Ventilation is the remaining services-routing decision','Both options serve the same rooms | Diagram is functional, not a duct route or equipment layout')
box(20,52,180,49,'A / ONE CENTRAL MVHR IN THE REAR PLANT ROOM',[
 'One set of filters and main equipment away from bedrooms.',
 'Supply AND extract duct paths must reach the family wing.',
 'No proven route through the vaulted shared room yet.',
 'Carry forward only if a coordinated section demonstrates the fit.' ])
box(220,52,180,49,'B / TWO BALANCED SYSTEMS, ONE FOR EACH SIDE',[
 'Shorter local networks; no family MVHR trunks across the vault.',
 'Family unit needs an accessible, acoustically treated cupboard.',
 'Second unit in the rear plant room serves service / shared areas.',
 'More filters, exterior terminals and commissioning duties.' ])
note(20,117,'FAMILY NETWORK',[
 'Supply: parents and three children\'s bedrooms.',
 'Extract: parents\' ensuite and family bathroom.',
 'Transfer air through designed door / hall paths.',
 'Possible unit location: existing ST plant / linen zone.',
 'That would consume space and limit the hoped-for linen gain.',
 'It also reintroduces mechanical equipment near bedrooms.' ])
note(220,117,'SERVICE + SHARED NETWORK',[
 'Supply: guest room, office, library, gym, living and garden areas.',
 'Extract: guest shower, visitor WC, laundry and kitchen.',
 'Kitchen supply and extract need separation within the open room.',
 'Kitchen cooker hood is a separate coordinated duty;',
 'do not assume grease-laden hood air uses the MVHR network.',
 'Balance both systems and account for connecting-door positions.' ])
note(20,177,'RECOMMENDED NEXT TEST',[
 'Develop the two-system option first to protect the continuous vault.',
 'This is conditional on accepting a family-side service cupboard.',
 'Compare a section of central routing before settling that compromise.',
 'Neither the old ST placeholder nor the plant MVHR rectangle proves',
 'unit, silencer, manifold, duct bend or filter-removal space will fit.' ])
note(220,177,'KEEP THE INTERIORS WORKING [5, 7]',[
 'Reserve supply outlets clear of the snug cornice and TV bookcases.',
 'Locate filters and service panels where they can be reached indoors.',
 'Design quiet bedroom air speeds, transfer paths and attenuation.',
 'Roof / floor depths must include structure and insulation as well as ducts.',
 'MVHR recovers heat; it is not the designed active cooling system.',
 'Allow exterior intake / exhaust separation and condensate drainage.' ])
text(20,258,'Coverage checked against all relevant room IDs in concept 25. Airflow, pressure, acoustic and duct-fit calculations remain outstanding.',2.75,fill='muted')
m.c.showPage()
header(3,'Size hot water from shower use, then check the long pipe run','Illustrative sensitivity calculations, not cylinder selection or operating-temperature advice')
text(20,53,'TWO SHOWERS TOGETHER FOR TEN MINUTES',3.3,True)
cols=[20,91,158,231];titles=['EACH SHOWER','MIXED WATER','IDEAL HOT DRAW','HEAT TO WATER']
for x,t in zip(cols,titles):text(x,65,t,2.6,True)
for i,row in enumerate(SHOWERS):
    y=78+i*12;m.line(20,y+4,290,y+4,'line',.15)
    for x,t in zip(cols,[f"{row['each_shower_l_min']} L/min",f"{row['mixed_l']} L",f"{row['ideal_hot_l']:.0f} L",f"{row['heat_kwh']:.2f} kWh"]):text(x,y,t,3)
note(311,54,'ARITHMETIC ASSUMPTIONS',[
 'Mixed shower water: 40 C.',
 'Incoming cold water: 10 C.',
 'Illustrative stored water: 55 C.',
 'No recovery during the draw.',
 'No losses or unusable store volume.',
 'These are not control setpoints.' ])
note(20,123,'WHAT THE NUMBERS MEAN',[
 'Two 16 L/min showers use 320 L of mixed water in ten minutes.',
 'The ideal hot draw is 213 L; real usable storage and recovery matter.',
 'A second pair immediately afterwards doubles that ideal draw to 427 L',
 'if there is no recovery. Bath overlap and guest repetition add demand.',
 'A bigger cylinder does not fix poor incoming pressure / flow.',
 'The supply must sustain both showers plus any simultaneous outlets.' ])
note(222,123,'DISTRIBUTION CHOICE',[
 'Start with one correctly sized store at the service end.',
 'Compare insulated direct distribution with a controlled return loop.',
 'A return can reduce waiting but adds heat loss and pump / control work.',
 'A local family-side store shortens the final run but needs more plant',
 'near bedrooms. Keep it as a fallback if the remote distribution fails.',
 'Agree water hygiene, mixing and scald protection in the detailed design.' ])
text(20,178,'WHY PIPE BORE AND DISTANCE MATTER',3.3,True)
for i,row in enumerate(PIPES):
    y=192+i*12
    text(20,y,f"30 m example / {row['internal_bore_mm']} mm internal bore",2.9)
    text(133,y,f"{row['water_l']:.2f} L held in pipe",2.9)
    text(222,y,f"{row['flush_seconds_at_6_l_min']:.0f} seconds at 6 L/min hot-side flow",2.9)
note(20,225,'LIMITS AND FORMULAE',[
 '30 m is an illustrative length, not the measured revised route; internal bore is not nominal pipe size. Actual runs and flow remain to design.',
 'The delay is a simple volume flush, excluding pipe warm-up and mixing. Larger pipes hold more water but may reduce pressure loss.',
 'Hot draw = mixed volume x (40 - 10) / (55 - 10). Heat = litres x 4.186 x (40 - 10) / 3600 kWh. Pipe volume = pi x bore squared / 4 x length.' ])
m.c.showPage()
header(4,'What the next design pass must prove','Keep the current house geometry; coordinate equipment before changing the roof or fixing joinery')
note(20,53,'PLANT ROOM AND LOCAL SERVICE SPACE',[
 'Rear plant room remains 4.00 x 2.65 m clear, with interior gym access.',
 'Dimension actual cylinder, hydraulics, ventilation and all service zones.',
 'Allow drainage, electrical isolation, replacement route and structural loads.',
 'Check plant vibration / noise at the library wall and gym.',
 'Reserve local UFH manifolds; do not force every component into one room.',
 'Two MVHR systems would require a second cupboard on the family side.' ])
note(222,53,'CALCULATIONS BEFORE EQUIPMENT SELECTION',[
 'Room heat loss using the actual envelope, glazing and Northumberland site.',
 'UFH output against floor finish, furniture, loop limits and water temperature.',
 'Room cooling loads, outdoor-unit combinations and night noise.',
 'Ventilation flows, pressure losses, transfer paths and acoustic performance.',
 'Shower flow / duration, water supply, store recovery and distribution losses.',
 'Solar / battery / grid balance; solar-only overnight cooling is not proven.' ])
note(20,112,'CONTROLS TO MAKE DAILY USE SIMPLE',[
 'Separate temperature control for family, guest and shared use.',
 'Coordinate slow floor response with cooling; prevent conflicting commands.',
 'Hot-water scheduling must preserve shower comfort during guest visits.',
 'Keep ordinary local controls; commissioning should include guest mode.',
 'Check simultaneous hot-water / UFH priority on the selected heat pump.' ])
note(222,112,'NEXT ARCHITECTURAL OUTPUT',[
 'A services section through each wing and the shared-room junction.',
 'One dimensioned plant layout, including filter and cylinder removal.',
 'A central-versus-two-system ventilation space comparison.',
 'Rooflight, nearby office window, exterior terminals and outdoor-unit siting.',
 'Budget comparison using the same duties; no speculative prices here.' ])
text(20,180,'PRIMARY REFERENCES / ACCESSED 13 SEPTEMBER 2026',3.1,True)
for i,(label,url) in enumerate(SOURCES):
    y=191+i*8;text(20,y,f'[{i+1}] {label}',2.7,fill='green')
    m.c.linkURL(url,(20*m.mm,(297-y-1)*m.mm,280*m.mm,(297-y+4)*m.mm),relative=0)
text(20,257,'References support system principles and product examples. Recommendations, room allocations and arithmetic are specific to this study.',2.6,fill='muted')
m.c.showPage();m.c.save()
(OUT/'concept-26-study-check.json').write_text(json.dumps({'status':'Underfloor preference confirmed; coordinated architecture recommended, not sized',
 'geometry_reference':'concept-25-study-check.json','geometry_reference_sha256':hashlib.sha256((OUT/'concept-25-study-check.json').read_bytes()).hexdigest(),
 'geometry_changed':False,'supply_room_groups':SUPPLY,'extract_room_groups':EXTRACT,
 'shower_scenarios':SHOWERS,'pipe_examples':PIPES,'temperature_assumptions_c':{'mixed':40,'cold':10,'stored':55},
 'recommendation':'Wet UFH and separate air-to-water hot-water system plus wing cooling; test two local MVHR systems against central routing',
 'family_mvhr_not_selected':True,'sources':[{'title':t,'url':u} for t,u in SOURCES],
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
print(PDF)
print('Room coverage, source hash and illustrative water calculations checked. Geometry unchanged.')
