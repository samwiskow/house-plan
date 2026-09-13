"""Concept 27: measured central and local MVHR space comparison."""
import copy
import hashlib
import json
from math import ceil, hypot, pi, radians, tan
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,BASE=load_model()
PLAN=json.loads((ROOT/'output/pdf/concept-25-study-check.json').read_text())
STRATEGY=json.loads((ROOT/'output/pdf/concept-26-study-check.json').read_text())
for filename,digest in [('revised_house_plan.py',PLAN['source_sha256']),('heating_ventilation_options.py',STRATEGY['source_sha256'])]:
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest,filename
state=PLAN['model'];m.rooms=[m.Room(**r) for r in state['rooms']];m.R={r.id:r for r in m.rooms}
m.doors=[m.Door(**d) for d in state['doors']];m.windows=state['windows'];m.OUTLINE=state['outline'];m.INNER=state['inner']
FAMILY_BAY=(.35,7.27,.80,1.42)
FAMILY_BODY=(.40,7.35,.570,.725)
FAMILY_SERVICE=(.970,7.35,1.0,.725)
REAR_BAY=(26.0,10.6,.80,.95)
REAR_BODY=(26.205,10.60,.570,.725)
REAR_SERVICE=(25.205,10.60,1.0,.725)
LINEN={'A':(.35,8.24,2.05,.45),'B':(1.15,8.24,1.25,.45)}
ORIGINAL_LINEN=(1.50,8.24,.90,.45)
SHELF_LEVELS=5
PACK={'nominal_duct_m':.200,'radial_insulation_m':.025,'gap_m':.050,'edge_m':.050,'width_m':.650,'depth_m':.350}
OD=PACK['nominal_duct_m']+2*PACK['radial_insulation_m']
assert abs(2*OD+PACK['gap_m']+2*PACK['edge_m']-PACK['width_m'])<1e-8
assert abs(OD+2*PACK['edge_m']-PACK['depth_m'])<1e-8
SHARED_BAND=(4.10,13.15,13.05,.65)
COMMON=[(26.49,10.96),(25.2,10.96),(25.2,12.55),(17.15,12.55)]
CROSSING=[(17.15,12.55),(17.15,13.475),(4.1,13.475),(4.1,7.70)]
FAMILY_LOCAL=[(.685,7.7125),(4.1,7.7125)]
DUCT_ROUTES={
 'Common rear connection':COMMON,
 'Central family connection':CROSSING,
 'Local family connection':FAMILY_LOCAL,
 'Family north spine':[(4.1,7.70),(4.1,4.70)],
 'Family south spine':[(4.1,7.70),(4.1,12.85)],
 'Service north spine':[(17.15,12.55),(17.15,2.65)],
 'Kitchen extract via pantry':[(17.15,12.55),(17.15,16.50),(15.0,16.50),(13.88,16.50)],
 'Living high-wall supply':[(4.1,12.85),(4.1,13.15)],
 'Dining high-wall supply':[(17.15,12.55),(17.15,14.15),(17.75,14.15)],
 'Garden high-wall supply':[(17.15,10.50),(16.55,10.50)]}
LENGTHS={k:sum(hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(v,v[1:])) for k,v in DUCT_ROUTES.items()}
TERMINALS={'rear':[(23.30,9.65),(25.40,9.65)],'family':[(.95,7.75),(2.95,7.75)]}
SEPARATIONS={k:hypot(v[1][0]-v[0][0],v[1][1]-v[0][1]) for k,v in TERMINALS.items()}
assert all(d>=1.5 for d in SEPARATIONS.values())
for group,pts in TERMINALS.items():
    room='PL' if group=='rear' else 'ST'
    assert all(m.inside(p,m.R[room].poly) for p in pts)
STATES={}
for option in ['A','B']:
    m.furniture=copy.deepcopy([f for f in PLAN['furniture'] if f['room']!='ST' and f['name']!='P2 ventilation allowance'])
    m.furn('PL','MVHR service bay',*REAR_BAY,'plant')
    m.furn('ST','Conditional linen shelves',*LINEN[option],'cabinet')
    if option=='B':m.furn('ST','Family MVHR service bay',*FAMILY_BAY,'plant')
    m.routes=copy.deepcopy(PLAN['routes']);del m.routes['Plant approach']
    m.routes['Linen approach']=[(4.1,7.9),(2.8,7.9),(1.85,7.8)]
    if option=='A':m.routes['Linen far-end approach']=[(1.85,7.8),(.80,7.8)]
    else:m.routes['Family MVHR approach']=[(2.8,7.9),(1.70,7.75)]
    issues=m.verify();assert not issues,(option,issues)
    for room,reserve,own in [('PL',REAR_SERVICE,'MVHR service bay')]+([('ST',FAMILY_SERVICE,'Family MVHR service bay')] if option=='B' else []):
        x,y,w,h=reserve
        assert all(m.inside(p,m.R[room].poly) for p in m.box(x+.001,y+.001,w-.002,h-.002))
        assert not any(m.overlap(reserve,f['rect'])>1e-8 for f in m.furniture if f['name']!=own)
    STATES[option]={'furniture':copy.deepcopy(m.furniture),'routes':copy.deepcopy(m.routes),'issues':issues}
    print(f'Option {option}: {len(m.routes)} daytime routes pass.',flush=True)
# The internal plant leaf is already checked in concept 22; retain that additional check here.
leaf=(24.28,10.98,.04,.87)
for option,s in STATES.items():
    for name in ['Gym to plant','Plant cylinder approach','Plant ventilation approach','Plant controls approach','Plant external door approach']:
        for a,b in zip(s['routes'][name],s['routes'][name][1:]):
            n=max(1,ceil(hypot(b[0]-a[0],b[1]-a[1])/.025))
            for i in range(n+1):
                x=a[0]+(b[0]-a[0])*i/n;y=a[1]+(b[1]-a[1])*i/n;X,Y,W,H=leaf
                assert hypot(max(X-x,0,x-X-W),max(Y-y,0,y-Y-H))>=.35-1e-8
assert all([f for f in s['furniture'] if f['room'] not in ['PL','ST']]==[f for f in PLAN['furniture'] if f['room'] not in ['PL','ST']] for s in STATES.values())
MANUAL='https://www.zehnder.ee/wp-content/uploads/2024/05/40015975-0118-fc-fc-A4-ComfoAir-Q-Installer_Zehnder-SI_EN-2.pdf'
PRODUCT='https://www.zehnder.co.uk/en/indoor-ventilation/solutions/mechanical-ventilation-with-heat-recovery/zehnder-comfoair-q600-st/zehnder-comfoair-q600'
OUT=ROOT/'output/pdf';PDF=OUT/'concept-27-measured-ventilation-layouts.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 27 - measured ventilation layouts')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.75,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 27 / MEASURED VENTILATION OPTIONS',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.7,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'SPATIAL COMPARISON | Proposed service reservations, not selected equipment or verified airflow / duct construction. Print at 100% for scale.',2.3,fill='muted')
    text(406,287,f'{n} / 5',2.6,align='right',fill='muted')
def activate(option):m.furniture=STATES[option]['furniture'];m.routes=STATES[option]['routes']
def crop(p,x,y,w,h):
    m.c.saveState();path=m.c.beginPath();path.rect(x*m.mm,(297-y-h)*m.mm,w*m.mm,h*m.mm);m.c.clipPath(path,stroke=0);p.draw(labels=False);m.c.restoreState()
def route(p,pts,colour='green',width=.35):
    for a,b in zip(pts,pts[1:]):p.line(a,b,colour,width,[1,1])
def ring(p,x,y,colour='green',r=.18):
    X,Y=p.xy((x,y));m.c.setStrokeColor(m.color(colour));m.c.setFillColor(m.color('paper'));m.c.setLineWidth(.25*m.mm);m.c.circle(X*m.mm,(297-Y)*m.mm,r*p.s*m.mm,stroke=1,fill=1)
def body(p,r):p.rect(*r,'#9aab94','green',.2)
def bed_heads(p):
    for f in m.furniture:
        if f['kind']=='bed' and f['room'] in ['P','C1','C2','C3']:
            x,y,w,h=f['rect'];p.rect(x,y,w,h,'furniture','muted',.12)
            if f['room']=='P':p.rect(x+.1,y+h-.48,w-.2,.38,'paper','muted',.1)
            elif f['room']=='C2':p.rect(x+.1,y+.1,.35,h-.2,'paper','muted',.1)
            else:p.rect(x+w-.45,y+.1,.35,h-.2,'paper','muted',.1)
header(1,'Two layouts, with the shared-room ventilation included','Full-house comparison 1:150 at A3 | South / garden up | Dashed lines are candidate overhead spine routes, not every branch')
for option,ox in [('A',20),('B',220)]:
    activate(option);p=m.Plan(ox,65,1000/150);p.draw(labels=False);bed_heads(p)
    text(ox,51,'A / ONE CENTRAL UNIT' if option=='A' else 'B / TWO LOCAL UNITS',3.3,True)
    for name in ['Common rear connection','Family north spine','Family south spine','Service north spine','Kitchen extract via pantry','Living high-wall supply','Dining high-wall supply','Garden high-wall supply']:
        route(p,DUCT_ROUTES[name])
    route(p,CROSSING if option=='A' else FAMILY_LOCAL,'amber' if option=='A' else 'green',.5)
    if option=='A':p.rect(*SHARED_BAND,None,'amber',.3)
    for room in ['ST','FH','PL','GY','S','GH','KL','OR']:
        x,y=m.R[room].label
        if room=='ST':x,y=2.25,8.4
        if room=='S':x,y=20,10.55
        X,Y=p.xy((x,y));m.rect(X-2.6,Y-2,5.2,3.4,'paper',None);text(X,Y+.5,room,2,True,align='center')
    for group in (['rear'] if option=='A' else ['rear','family']):
        for i,(x,y) in enumerate(TERMINALS[group]):ring(p,x,y,'green' if i==0 else 'amber')
    for x,y in [(4.1,13.15),(17.75,14.15),(16.55,10.5)]:ring(p,x,y,'green',.14)
    p.rect(*PLAN['snug_rooflight_reservation_m'],None,'amber',.2)
note(20,204,'A / LARGER LINEN GAIN, VISIBLE SHARED CROSSING',[
 'Rear unit connects to both wings; amber crosses 13.05 m between halls.',
 'Test a continuous 0.65 m projection x 0.35 m deep edge enclosure.',
 'The band also runs along the garden-room / shared-room opening.',
 'Conditional linen run: 2.05 m, after the old plant is fully relocated.' ])
note(220,204,'B / NO THROUGH-RUNNING FAMILY TRUNKS',[
 'Family unit also supplies the living end from the family-wing boundary.',
 'Service unit supplies dining / garden; kitchen extract uses the pantry route.',
 'High-wall outlet reach must be proven; this is not a throw calculation.',
 'Conditional linen run: 1.25 m, plus a 0.80 m-deep service bay.' ])
text(20,259,'Roof circles: intake / exhaust position allowances. All wet-room and bedroom branches, pressure losses, controls and terminal details still need design.',2.6,fill='muted')
m.c.showPage()
header(2,'The family unit fits best facing along the cupboard','ST clear dimensions 3.03 x 1.42 m | Plans 1:25 at A3 | Both alternatives assume the original heating / water plant is relocated')
for option,ox in [('A',25),('B',228)]:
    activate(option);p=m.Plan(ox-.35*40,80-7.27*40,40);crop(p,ox-7,66,173,92)
    text(ox,53,'A / LINEN ONLY' if option=='A' else 'B / LINEN + MVHR',3.3,True)
    p.dimension((.35,7.27),(3.38,7.27),-.28,'3.03 m')
    if option=='B':
        p.rect(*FAMILY_BAY,None,'green',.3);body(p,FAMILY_BODY);p.rect(*FAMILY_SERVICE,None,'amber',.35)
        p.text(1.47,7.85,'1.00 m access',2.1,fill='amber');p.text(.74,8.46,'SERVICE BAY',2.0)
        route(p,m.routes['Family MVHR approach'])
    else:route(p,m.routes['Linen far-end approach'])
    x,y,w,h=LINEN[option];p.text(x+w/2,y+.29,f'{w:.2f} m LINEN',2.4)
note(25,174,'A / 2.05 m SHELF RUN',[
 '0.45 m deep; five illustrative shelf levels.',
 '4.61 m2 total nominal shelf surface.',
 'Existing proposal: 0.90 m run / 2.03 m2 shelf surface.',
 'The shelf stops clear of the existing D04 door sweep.' ])
note(228,174,'B / 1.25 m SHELF RUN',[
 'Same depth / levels: 2.81 m2 nominal shelf surface.',
 '1.80 m2 less shelf surface than option A.',
 'Still 0.35 m more shelf run than the existing proposal.',
 'Unit faces the long room axis; front service space stays clear.' ])
note(25,224,'BODY FIT IS NOT A COMPLETE CUPBOARD SPECIFICATION',[
 'Q-series spatial example: 0.725 m wide x 0.570 m deep x about 0.850 m high; reserve 1.00 m in front [1, 2]. No capacity is selected.',
 'Across the narrow room: 0.570 + 1.00 = 1.570 m, already more than 1.42 m before wall offsets or joinery. Rotating avoids that conflict.',
 'The 0.80 x 1.42 m bay reserves connections above. Acoustic lining, access panels and any UFH manifold could reduce the shelf gain further.',
 'Use a suitable support / isolation detail at the external wall; verify noise into adjacent bedrooms. Door handling and frames remain to check.' ])
m.c.showPage()
header(3,'Retain a full maintenance approach in the rear plant room','Plant plan 1:25 at A3 | Same spatial unit envelope for either strategy; actual unit duty and model remain to select')
activate('B');p=m.Plan(26-22.8*40,70-9.05*40,40);crop(p,16,53,192,142)
body(p,REAR_BODY);p.rect(*REAR_SERVICE,None,'amber',.35)
p.rect(24.8,10.6,1.15,.8,None,'green',.3)
p.text(25.70,10.93,'ACCESS',2.4,fill='amber')
p.text(25.37,11.58,'DISTRIBUTION ABOVE',2.0,fill='green')
p.text(23.40,9.71,'CYLINDER',2.2);p.text(24.5,9.45,'CONTROLS',2.0)
p.dimension((22.8,9.05),(26.8,9.05),-.28,'4.00 m')
route(p,[(23.85,12.0),(23.85,11.4),(23.85,10.55)]);route(p,m.routes['Plant ventilation approach'])
note(228,53,'UNIT-WALL SECTION / 1:25',[
 '0.35 m base height + 0.85 m body = 1.20 m top.',
 'Test 1.00 m vertical silencer reservations above the unit.',
 'Then 0.30 m for bends; top at approximately 2.50 m.',
 'Only 0.10 m remains below a 2.60 m ceiling.',
 'These ancillary dimensions are study allowances, not selected parts.' ])
sc=40;x=241;base=250
m.rect(x,base-2.6*sc,1.50*sc,2.6*sc,'paper','line',.2)
m.rect(x+.12*sc,base-1.20*sc,.725*sc,.85*sc,'#9aab94','green',.2)
for xx in [x+.15*sc,x+.52*sc]:
    m.rect(xx,base-2.20*sc,.30*sc,1.0*sc,None,'green',.3)
    m.rect(xx,base-2.50*sc,.30*sc,.30*sc,None,'amber',.25)
text(x+1.02*sc,base-.75*sc,'UNIT',2.3)
text(x+1.02*sc,base-1.70*sc,'SILENCERS',2.1)
text(x+1.02*sc,base-2.35*sc,'BENDS',2.1)
text(x,base+6,'Front elevation; outdoor ducts omitted for clarity.',2.4,fill='muted')
note(26,207,'ACCESS AND CONNECTIONS',[
 'The 1.00 m front reservation clears fixed equipment and the open D21 leaf.',
 'A 1.15 x 0.80 m ceiling distribution zone sits over clear service floor.',
 'Four unit connections, outdoor duct insulation, drainage and supports',
 'must be coordinated in 3D before this becomes an installation layout.',
 'The front access area cannot become storage; rear exterior door stays.' ])
m.c.showPage()
header(4,'A central system leaves a substantial edge enclosure','Section through family hall and shared vault 1:40 at A3 | Duct packing detail 1:5 | Roof geometry retained as a concept')
sc=25;ox=23;floor=206
X=lambda y:ox+(y-10.2)*sc
Y=lambda z:floor-z*sc
m.line(X(10.2),Y(0),X(18.4),Y(0),'ink',.5)
m.line(X(10.2),Y(2.6),X(13.03),Y(2.6),'muted',.3)
m.line(X(10.2),Y(3.2),X(12.8),Y(3.2),'ink',.4)
m.line(X(12.8),Y(3.2),X(12.8),Y(3.7),'ink',.3)
apex=3.5+2.45*tan(radians(30));ridge=3.7+2.8*tan(radians(30))
m.poly([(X(12.8),Y(3.7)),(X(15.6),Y(ridge)),(X(18.4),Y(3.7)),(X(18.05),Y(3.5)),(X(15.6),Y(apex)),(X(13.15),Y(3.5))],'#eee4d3','muted',.25)
m.rect(X(13.03),Y(3.2),.12*sc,1.1*sc,'wall',None)
m.rect(X(13.15),Y(3.05),.65*sc,.35*sc,None,'amber',.5)
route_points=[(X(11.8),Y(2.75)),(X(12.6),Y(2.75)),(X(13.325),Y(2.875))]
for a,b in zip(route_points,route_points[1:]):m.line(*a,*b,'green',.4,[1,1])
text(X(10.2),Y(3.2)-3,'+3.20 roof top',2.5);text(X(10.2),Y(2.6)+5,'+2.60 ceiling',2.5)
text(X(11.5),Y(1.55),'FAMILY HALL',2.7,True,align='center');text(X(15.7),Y(1.55),'SHARED VAULT',2.7,True,align='center')
text(X(15.6),Y(apex)+8,f'+{apex:.2f} ceiling apex',2.4,align='center')
m.line(X(13.475),Y(2.70),X(13.475),Y(2.0),'amber',.25);text(X(13.475),Y(2.0)+5,'+2.70 underside',2.4,align='center',fill='amber')
text(260,53,'PAIR OF DUCTS / 1:5',3.3,True)
x=263;y=69;scale=200
m.rect(x,y,.65*scale,.35*scale,None,'amber',.4)
for dx in [.175,.475]:
    m.c.setStrokeColor(m.color('green'));m.c.setLineWidth(.25*m.mm)
    m.c.circle((x+dx*scale)*m.mm,(297-y-.175*scale)*m.mm,.125*scale*m.mm,stroke=1,fill=0)
    m.c.circle((x+dx*scale)*m.mm,(297-y-.175*scale)*m.mm,.100*scale*m.mm,stroke=1,fill=0)
text(x+65,y+79,'650 mm projection / 350 mm depth',2.6,align='center')
note(260,161,'PACKING ASSUMPTIONS',[
 'Two 200 mm nominal ducts, each with 25 mm insulation.',
 '250 mm outer envelopes; 50 mm gap between them.',
 '50 mm each side for lining / fixing / working allowance.',
 '50 mm above and below; no spare space beyond this.',
 'Ducts are NOT sized from pressure or airflow calculations.' ])
note(23,228,'WHAT STILL HAS TO FIT',[
 'The 13.05 m band runs between halls. Reserve larger local turn / junction zones; a straight packing section does not prove an elbow fits.',
 'The lower wing has 0.60 m gross between roof top and ceiling. Structure, insulation and falls consume that depth; no clear void is assumed.',
 'B uses local high-wall outlets near the wing boundaries instead. Their headers, grille depth, throw and acoustic performance still need design.',
 'If local outlets cannot distribute fresh air well, B may still need short shared-room ducts; it is not a guaranteed invisible solution.' ])
m.c.showPage()
header(5,'Develop the two-unit option, while keeping the trade-off explicit','No room, door or window changes adopted | All shelving gains are conditional on full relocation of the original plant')
cols=[20,157,272]
for x,t in zip(cols,['MEASURE / CONSEQUENCE','A / CENTRAL','B / TWO LOCAL']):text(x,54,t,2.8,True)
rows=[('Main units / roof terminal pairs','1 / 1','2 / 2'),('ST linen run, 450 mm deep','2.05 m','1.25 m'),('Five-level shelf surface','4.61 m2','2.81 m2'),('Family-side unit bay','None','0.80 x 1.42 m'),('Through-running family trunks','13.05 m across shared edge','None in this proposal'),('Unit front maintenance space','1.00 m at rear','1.00 m at both'),('Key unresolved issue','Band, turns and roof/header fit','Local outlet throw and bedroom noise')]
for i,row in enumerate(rows):
    y=67+i*10
    for x,t in zip(cols,row):text(x,y,t,2.65)
    m.line(20,y+3,400,y+3,'line',.15)
note(20,154,'SHARED-ROOM DUTIES UPDATED',[
 'Family unit: parents / child bedrooms plus the shared living end;',
 'extract from parents\' ensuite and family bathroom.',
 'Service unit: guest, office, library, gym, garden and dining supply;',
 'extract guest shower, WC, laundry and kitchen.',
 'Both systems need balancing, including shared-room transfer effects.',
 'Kitchen hood, plant and storage-space ventilation remain separate duties.' ])
note(222,154,'RESULTS AND NEXT PROOF',[
 f"{len(STATES['A']['routes'])} sampled daytime routes pass in each alternative.",
 'Unit service rectangles clear fixed items; the open plant door clears routes.',
 'Room geometry and all non-plant / linen furniture stay unchanged.',
 'Roof pairs reserve 2.10 m rear / 2.00 m family spacing in plan.',
 'Their height, windows, flues, PV and wind interaction are unresolved.',
 'Prove outlet throw, noise, duty and complete duct fit before selection.' ])
text(20,227,'PRIMARY DIMENSION REFERENCES / CHECKED 13 SEPTEMBER 2026',3.0,True)
for i,(label,url) in enumerate([('Q installer manual: access / drawings / terminals, pp. 5, 8-9, 16',MANUAL),('Current UK Q600 page: 725 x 570 x 850 mm body',PRODUCT)]):
    y=237+i*8;text(20,y,f'[{i+1}] {label}',2.6,fill='green');m.c.linkURL(url,(20*m.mm,(297-y-1)*m.mm,330*m.mm,(297-y+4)*m.mm),relative=0)
text(20,260,'Manufacturer dimensions ground the body/access examples. Bay sizes, ancillary zones, pipe packing and routing are this study\'s provisional design.',2.6,fill='muted')
m.c.showPage();m.c.save()
(OUT/'concept-27-study-check.json').write_text(json.dumps({'status':'Measured alternatives; two local units recommended for further design, not selected',
 'base_geometry_reference':'concept-25-study-check.json','base_geometry_sha256':hashlib.sha256((OUT/'concept-25-study-check.json').read_bytes()).hexdigest(),
 'strategy_reference':'concept-26-study-check.json','strategy_sha256':hashlib.sha256((OUT/'concept-26-study-check.json').read_bytes()).hexdigest(),
 'model':state,'alternatives':STATES,'family_bay_m':FAMILY_BAY,'family_body_m':FAMILY_BODY,'family_service_m':FAMILY_SERVICE,
 'rear_bay_m':REAR_BAY,'rear_body_m':REAR_BODY,'rear_service_m':REAR_SERVICE,'linen_rectangles_m':LINEN,
 'shelf_levels':SHELF_LEVELS,'shelf_surface_m2':{k:r[2]*r[3]*SHELF_LEVELS for k,r in LINEN.items()},
 'duct_spines_m':DUCT_ROUTES,'plan_spine_lengths_m':LENGTHS,'shared_band_m':SHARED_BAND,'duct_pack':PACK,
 'roof_terminal_points_m':TERMINALS,'terminal_pair_plan_separation_m':SEPARATIONS,
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'limitations':['No capacity selection','No airflow pressure or acoustic calculation','No certified roof or header penetration','No verified terminal throw','Conditional plant relocation and shelf gains','Ancillary dimensions are study allowances']},indent=2)+'\n')
print(PDF)
