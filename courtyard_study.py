"""Concept 09: measured courtyard layout and coordinated garden elevations."""
import ast
import json
from math import cos, sin, pi, hypot, tan, radians
from pathlib import Path

ROOT = Path(__file__).parent
source = ast.parse((ROOT/'shared_space_study.py').read_text())
cut = next(i for i,n in enumerate(source.body) if isinstance(n,ast.Assign)
           and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
scope = {'__file__':str(ROOT/'shared_space_study.py')}
exec(compile(ast.Module(body=source.body[:cut],type_ignores=[]),str(ROOT/'shared_space_study.py'),'exec'),scope)
m = scope['m']
COURT = [(8.2,0),(16.2,0),(16.2,9.3),(12.2,9.3),(12.2,12.8),(8.2,12.8)]
PAVING = [(9.3,5.0,4.8,4.3),(9.3,9.3,2.9,3.5),(12.2,8.2,4,1.1),
          (12.1,1.05,3.55,3.2),(12.9,4.25,1.2,.75),
          (11.2,0,1.2,5.0),(11.2,3.75,2.9,1.25)]
BEDS = [('Family buffer',(8.55,.4,.75,11.45)),
        ('Guest-side planting',(15.65,.4,.55,7.35))]
FURNITURE = [('Dining table',(9.55,6.2,3,1),'oak','table')]
for x in [9.675,10.425,11.175,11.925]:
    FURNITURE += [('Dining north',(x,5.6,.55,.55),'linen','south'),
                  ('Dining south',(x,7.25,.55,.55),'linen','north')]
FURNITURE += [('Outdoor sofa',(14.7,1.3,.85,2.2),'linen','west'),
              ('Outdoor chair',(12.45,1.65,.85,.85),'linen','east'),
              ('Low table',(13.65,2.4,.6,.6),'oak','table')]
ROUTES = {'House to dining approach':[(10.95,12.25),(10.95,8.75)],
          'Between house and garden-room approaches':[(10.95,8.75),(15.1,8.75)],
          'Dining to main garden':[(13.5,8.75),(13.5,4.375),(11.8,4.375),(11.8,.55)],
          'Dining to quiet sitting':[(13.5,4.375),(13.5,3.75)]}


def contains(p,b):
    x,y,w,h=b
    return x-1e-8<=p[0]<=x+w+1e-8 and y-1e-8<=p[1]<=y+h+1e-8


def area_union(boxes):
    xs=sorted({v for x,y,w,h in boxes for v in (x,x+w)})
    ys=sorted({v for x,y,w,h in boxes for v in (y,y+h)})
    return sum((b-a)*(d-c) for a,b in zip(xs,xs[1:]) for c,d in zip(ys,ys[1:])
               if any(contains(((a+b)/2,(c+d)/2),r) for r in boxes))


def check_court(furniture):
    issues=[]
    for name,b,mat,kind in furniture:
        x,y,w,h=b
        for point in m.box(x+.001,y+.001,w-.002,h-.002):
            if not m.inside(point,COURT):issues.append(f'{name}: outside court')
            if not any(contains(point,r) for r in PAVING):issues.append(f'{name}: outside paving')
        if any(m.overlap(b,bed)>1e-7 for _,bed in BEDS):issues.append(f'{name}: planting overlap')
    for i,(name,b,_,_) in enumerate(furniture):
        for other,r,_,_ in furniture[i+1:]:
            if m.overlap(b,r)>1e-7:issues.append(f'{name}/{other}: overlap')
    obstacles=[b for _,b,_,_ in furniture]+[b for _,b in BEDS]
    probes=0
    for name,points in ROUTES.items():
        for a,b in zip(points,points[1:]):
            steps=max(1,int(hypot(b[0]-a[0],b[1]-a[1])/.025))
            for i in range(steps+1):
                p=(a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps)
                for j in range(-1,32):
                    q=p if j<0 else (p[0]+.5*cos(j*pi/16),p[1]+.5*sin(j*pi/16))
                    probes+=1
                    if not any(contains(q,r) for r in PAVING):issues.append(f'{name}: outside paving at {q}');break
                    if not m.inside(q,COURT):issues.append(f'{name}: outside court at {q}');break
                    if any(contains(q,r) for r in obstacles):issues.append(f'{name}: obstacle at {q}');break
                if issues:break
            if issues:break
    return issues,probes


normal,normal_probes=check_court(FURNITURE)
pulled=[]
for name,(x,y,w,h),mat,kind in FURNITURE:
    if name=='Dining north':y-=.4
    elif name=='Dining south':y+=.4
    pulled.append((name,(x,y,w,h),mat,kind))
pulled_issues,pulled_probes=check_court(pulled)
assert not normal,normal
assert not pulled_issues,pulled_issues
assert abs(m.polygon_area(COURT)-88.4)<1e-8
for door_id,width in [('O04',2.6),('O06',2.8)]:
    assert next(d.width for d in m.doors if d.id==door_id)==width
assert all(m.inside(p,COURT) for r in PAVING for p in m.box(r[0]+.001,r[1]+.001,r[2]-.002,r[3]-.002))
paved_area=area_union(PAVING)
OUT=ROOT/'output/pdf'
PDF=OUT/'concept-09-courtyard-elevations.pdf'
C={'paper':'#fffdf8','ink':'#30392f','muted':'#696653','line':'#c8c0ae',
   'stone':'#dfcaa4','oak':'#bf9863','linen':'#e6d7b8','paving':'#e9deca',
   'plant':'#9bab78','garden':'#e5ead6','glass':'#dfece4','bronze':'#816c4c',
   'roof':'#b5a083','wall':'#384238','shared':'#f4ebdd','family':'#f1ede2',
   'furniture':'#e6d7b8','guest':'#f1ede2','service':'#f1ede2','circulation':'#faf7ef','green':'#376248'}
m.PALETTE.update(C)
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm))
m.c.setTitle('Concept 09 - courtyard and garden elevations')
m.c.setAuthor('House plan working study')


def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.25,True)
    m.paragraph(x,y+7,lines,step=5,size=2.8)
def header(page,title,sub):
    m.rect(0,0,420,297,'paper',None)
    text(14,12,'COURTYARD HOUSE / CONCEPT 09 / OUTSIDE ROOMS + ELEVATIONS',2.7,fill='muted')
    text(14,23,title,6.1,True);text(14,31,sub,2.8,fill='muted')
    m.line(14,36,406,36,'line',.3);m.line(14,280,406,280,'line',.25)
    text(14,287,'WORKING PROPOSAL | Plot, sunlight, planting, roof junctions, drainage and finished thresholds require design.',2.5,fill='muted')
    text(406,287,f'{page} / 2',2.6,align='right',fill='muted')
def badge(p,x,y,label):
    X,Y=p.xy((x,y));m.rect(X-3,Y-3,6,5.5,'paper','muted',.15)
    text(X,Y+1,label,2.6,True,align='center')


header(1,'A dining terrace, a quiet seat and a planted edge','Courtyard plan 1:75 at A3, printed at 100% | Existing footprint and opening widths retained | Plan top points toward the main garden')
p=m.Plan(22-6.7*40/3,54,40/3)
m.c.saveState();clip=m.c.beginPath();clip.rect(15*m.mm,(297-244)*m.mm,177*m.mm,199*m.mm);m.c.clipPath(clip,stroke=0)
p.poly(COURT,'garden',None)
for r in PAVING:p.rect(*r,'paving',None)
for x,y,w,h in PAVING:
    for yy in [y+.6*i for i in range(1,int(h/.6)+1)]:p.line((x,yy),(x+w,yy),'line',.08)
for name,r in BEDS:
    p.rect(*r,'plant',None)
    x,y,w,h=r
    for j in range(int(h/.5)):
        X,Y=p.xy((x+w/2,y+.25+j*.5));m.c.setStrokeColor(m.color('green'));m.c.setLineWidth(.1*m.mm)
        m.c.circle(X*m.mm,(297-Y)*m.mm,.22*p.s*m.mm,stroke=1,fill=0)
old_furniture,old_doors=m.furniture,m.doors
m.furniture=[f for f in old_furniture if f['room']=='OR']
m.doors=[d for d in old_doors if d.id not in ('O05','O07')]
p.draw(labels=False)
m.furniture,m.doors=old_furniture,old_doors
for name,(x,y,w,h),mat,kind in FURNITURE:
    p.rect(x,y,w,h,mat,'muted',.15)
    if kind!='table':
        back={'south':(x,y,w,.08),'north':(x,y+h-.08,w,.08),
              'west':(x+w-.12,y,.12,h),'east':(x,y,.12,h)}[kind]
        p.rect(*back,mat,'muted',.1)
for name,pts in ROUTES.items():
    for a,b in zip(pts,pts[1:]):p.line(a,b,'green',.35,[2,1.2])
p.line((11.8,.6),(11.8,-.2),'green',.45)
p.line((11.8,-.2),(11.6,.1),'green',.45);p.line((11.8,-.2),(12,.1),'green',.45)
p.dimension((8.2,0),(16.2,0),-.15,'8.00 courtyard')
p.dimension((8.2,12),(12.2,12),0,'4.00 between walls')
p.dimension((9.55,6.2),(12.55,6.2),.53,'3.00 x 1.00 table')
p.text(14.1,11.6,'GARDEN ROOM',2.6)
p.text(10.2,13.75,'SHARED ROOM',2.6)
p.text(7.45,5.0,'FAMILY',2.5)
p.text(17.0,5.0,'GUEST',2.5)
p.text(10.8,2.3,'Open',2.4,fill='muted');p.text(10.8,2.6,'garden',2.4,fill='muted')
for x,y,label in [(10.95,10.8,'1'),(13.2,6.7,'2'),(14.1,3.8,'3'),(8.9,8.8,'4')]:badge(p,x,y,label)
badge(p,8.45,11.7,'B');badge(p,15.9,5.0,'C');badge(p,12.05,10.8,'D')
p.text(10.3,12.7,'O04',2.4);p.text(15.1,9.15,'O06',2.4)
m.c.restoreState()
text(40,46,'MAIN GARDEN / NO COMPASS ORIENTATION ASSIGNED',2.5,fill='muted')
for i in range(3):m.rect(25+i*40/3,256,40/3,1.2,'ink' if i%2==0 else 'paper','ink',.1)
text(25,263,'0',2.5);text(65,263,'3 m',2.5,align='right')
text(88,259,'B / C / D locate the return elevations on sheet 2.',2.55,fill='muted')
note(216,50,'1 / KEEP THE NECK OPEN',[
    'The 4.00 m strip beside the garden room is the route out.',
    'A broad paved landing connects the two existing sliders.',
    'Keep furniture out of the final approaches to both doors.' ])
note(216,81,'2 / EIGHT OUTSIDE, CLOSE TO THE KITCHEN',[
    'A 3.00 x 1.00 m table sits in the wider part of the court.',
    'Four chairs per long side; none at the ends.',
    'The main route passes on the guest-wing side of dining.',
    'Pulled-out chairs leave 1.10 m before the garden-room face.' ])
note(216,117,'3 / A SEPARATE PLACE TO SIT',[
    'A 2.20 m sofa, one chair and a low table face into planting.',
    'This pad sits beside the guest wing\'s existing solid return.',
    'It offers a different outlook from the dining terrace.',
    'Sun, wind shelter and any overhead shade remain untested.' ])
note(216,153,'4 / FILTER THE BEDROOM EDGE',[
    'A 0.75 m planted band sits beyond a 0.35 m wall-side strip.',
    'Test a maintained 0.90-1.20 m planting height by dining.',
    'Lower planting nearer the garden keeps the mouth open.',
    'This filters views; it does not establish bedroom privacy.',
    'Review the actual window sills, daylight and mature growth.' ])
note(216,195,'MATERIALS + SPACE ALLOCATION',[
    'Warm buff paving, textured stone and warm-toned timber.',
    f'Open court: 88.40 m2; proposed paving: {paved_area:.2f} m2.',
    f'Remaining soft landscape / wall-side strips: {88.4-paved_area:.2f} m2.',
    'Paving is more extensive than the earlier rough terrace.',
    'Levels, drainage and surface specification are still open.' ])
note(216,237,'CHECKED / STILL TO CONFIRM',[
    'Four outside routes: sampled 1.00 m walking envelope.',
    'Passes with dining chairs normal and pulled out 0.40 m.',
    'Routes stop outside door faces; actual slider clear openings',
    'and accessible thresholds require product and level design.' ])
m.c.showPage()


header(2,'Stone wings, warm timber and a lighter garden room','Garden elevation A and courtyard returns B-D at 1:100 on A3 | Heights follow concepts 06B / 07B and remain provisional')
EAVE=3.7;RIDGE=3.7+2.8*tan(radians(30));LOW=3.2

def panel(mapper,coords,fill):pnts=[mapper(x,z) for x,z in coords];m.poly(pnts,fill,'ink',.2)
def box_e(mapper,x,z,w,h,fill):panel(mapper,[(x,z),(x+w,z),(x+w,z+h),(x,z+h)],fill)
def hatch(mapper,x0,x1,z0,z1,mat):
    box_e(mapper,x0,z0,x1-x0,z1-z0,mat)
    if mat=='oak':
        x=x0+.16
        while x<x1:
            m.line(*mapper(x,z0),*mapper(x,z1),'bronze',.08);x+=.16
    elif mat=='stone':
        z=z0+.28
        while z<z1:
            m.line(*mapper(x0,z),*mapper(x1,z),'line',.1);z+=.28

def glazed(mapper,x,w,sill,head,slider=False):
    box_e(mapper,x,sill,w,head-sill,'glass')
    for xx in (x,x+w/2,x+w):m.line(*mapper(xx,sill),*mapper(xx,head),'bronze',.3)
    for zz in (sill,head):m.line(*mapper(x,zz),*mapper(x+w,zz),'bronze',.3)
    if slider:
        m.line(*mapper(x+w*.6,.18),*mapper(x+w*.35,.18),'bronze',.2)
        m.line(*mapper(x+w*.35,.18),*mapper(x+w*.43,.26),'bronze',.2)


def garden(x,z):return 20+(27.15-x)*10,117-z*10
assert garden(25,0)[0]<garden(19.5,0)[0]<garden(14.2,0)[0]<garden(4.1,0)[0]
text(20,48,'A / FROM THE MAIN GARDEN: GYM LEFT, FAMILY WING RIGHT',3.2,True)
hatch(garden,0,22.8,0,EAVE,'oak')
box_e(garden,0,EAVE,22.8,RIDGE-EAVE,'roof')
for x in [i*.5 for i in range(46)]:m.line(*garden(x,EAVE),*garden(x,RIDGE),'bronze',.08)
stove=next(f for f in scope['items'] if f['name']=='Stove placeholder')
flue_x,flue_y=stove['rect'][0]+.26,stove['rect'][1]+.29
flue_roof=EAVE+(flue_y-12.8)*tan(radians(30))
m.line(*garden(flue_x,flue_roof),*garden(flue_x,5.8),'muted',.3,[2,1])
text(*garden(flue_x,6.05),'FLUE ZONE',2.3,align='center',fill='muted')
glazed(garden,9,2.6,0,2.7,True)
# The roof plane's 0.60 m rise is visible in this depth-compressed projection.
hatch(garden,12.2,16.2,0,2.85,'oak')
glazed(garden,13,2.8,0,2.35,True)
box_e(garden,12.2,2.85,4,.6,'glass')
for x in [12.2,13.2,14.2,15.2,16.2]:m.line(*garden(x,2.85),*garden(x,3.45),'bronze',.18)
for x0,x1 in [(0,8.2),(16.2,22.8),(22.8,27.15)]:
    hatch(garden,x0,x1,0,LOW,'stone')
    box_e(garden,x0,LOW-.1,x1-x0,.1,'bronze')
for axis,x,y,w in m.windows:
    if axis=='h' and y==0:glazed(garden,x,w,.75,2.35)
# Foreground planting is illustrative height massing, not a species specification.
for x,w,h in [(8.55,.75,.95),(15.65,.55,.9)]:box_e(garden,x,0,w,h,'plant')
for name,(x,y,w,d),mat,kind in FURNITURE:
    h=.75 if name=='Dining table' else (.4 if kind=='table' else .8)
    box_e(garden,x,0,w,h,mat)
m.line(15,117,297,117,'ink',.4)
for x,label in [(25,'Gym'),(19.5,'Guest wing'),(14.2,'Garden room'),(10.3,'Dining doors'),(4.1,'Family wing')]:
    text(*garden(x,-.65),label,2.6,align='center')
text(156,59,f'MAIN RIDGE +{RIDGE:.2f}',2.5,align='center',fill='muted')
text(20,133,'Orthographic projection: the front wings and deeper shared room align on paper. Use the plan to read their depth.',2.5,fill='muted')
note(309,50,'THE MATERIAL RULE',[
    'Stone on the projecting wings.',
    'Vertical timber on shared living.',
    'Warm bronze frames and slim edges.',
    'Roof covering is a colour placeholder.',
    'Timber finish needs a plan for',
    'retaining warmth as it weathers.' ])
note(309,94,'LEVELS BEING TESTED',[
    'Main eave +3.70 / ridge +5.32.',
    'Low-wing roof envelope +3.20.',
    'Garden glass +2.85 to +3.45.',
    'Flue marker: termination height unresolved.' ])
m.line(14,143,406,143,'line',.25)
text(20,154,'B / FAMILY RETURN',3.0,True)
text(170,154,'C / GUEST RETURN',3.0,True)
text(288,154,'D / GARDEN-ROOM SIDE',3.0,True)
family=lambda y,z:(20+(12.8-y)*10,203-z*10)
guest=lambda y,z:(170+y*10,203-z*10)
orangery=lambda y,z:(288+(y-9.3)*10,203-z*10)
assert family(12.8,0)[0]<family(0,0)[0]
assert guest(0,0)[0]<guest(9.3,0)[0]
hatch(family,0,12.8,0,LOW,'stone');box_e(family,0,3.1,12.8,.1,'bronze')
family_windows=[]
for axis,x,y,w in m.windows:
    if axis=='v' and x==8.2:
        glazed(family,y,w,.75,2.35);family_windows.append([y,w])
box_e(family,.4,0,3.5,.6,'plant');box_e(family,3.9,0,7.95,1.05,'plant')
hatch(guest,0,9.3,0,LOW,'stone');box_e(guest,0,3.1,9.3,.1,'bronze')
box_e(guest,.4,0,7.35,.9,'plant')
roof_high=3.45
panel(orangery,[(9.3,0),(12.8,0),(12.8,roof_high-.12),(9.3,2.85-.12)],'oak')
for axis,x,y,w in m.windows:
    if axis=='v' and x==12.2:glazed(orangery,y,w,.65,2.35)
# This side view shows the true shallow roof slope, rising toward the house.
for delta in (0,-.10):m.line(*orangery(9.3,2.85+delta),*orangery(12.8,3.45+delta),'bronze',.25)
m.line(*orangery(12.8,0),*orangery(12.8,3.7),'ink',.4)
text(337,172,'Glass rises',2.65);text(337,178,'0.60 over 3.50 m',2.65)
text(337,184,'toward the house.',2.65)
text(337,195,'Approx. 9.7 degrees.',2.65,fill='muted')
for mapper,a,b in [(family,0,12.8),(guest,0,9.3),(orangery,9.3,12.8)]:m.line(*mapper(a,0),*mapper(b,0),'ink',.35)
text(20,211,'Shared-room end',2.4);text(148,211,'Garden end',2.4,align='right')
text(170,211,'Garden end',2.4);text(263,211,'Garden-room junction',2.4,align='right')
text(288,211,'Court',2.4);text(323,211,'House',2.4,align='right')
note(20,226,'WINDOWS + PRIVACY',[
    'Existing family-side window positions and widths stay.',
    'Planting height is a proposal to test against views and light.',
    'The guest return stays solid above its planted edge.',
    'Its existing outward-facing windows are on the other side.' ])
note(158,226,'SLIDERS + THRESHOLDS',[
    'O04: 2.60 m overall; O06: 2.80 m overall opening.',
    'Two-panel operation shown; aim for at least 1.20 m',
    'clear passage after framing, subject to supplier design.',
    'Drainage, flush access and shading hardware need fitting.' ])
note(296,226,'JUNCTIONS TO DEVELOP',[
    'Low-wing roofs against the taller main eave.',
    'Glass roof against timber wall and guest wing.',
    'Coordinate gutters, flashings, insulation and',
    'external shading before fixing edge dimensions.' ])
for i in range(5):m.rect(340+i*10,269,10,1.1,'ink' if i%2==0 else 'paper','ink',.1)
text(340,276,'0',2.4);text(390,276,'5 m',2.4,align='right')
m.c.showPage();m.c.save()
(OUT/'concept-09-study-check.json').write_text(json.dumps({
    'status':'Courtyard and facade proposal; house geometry retained',
    'references':['concept 08 shared-space revision','concept 07 open garden room','concepts 06B/07B roof'],
    'court_polygon_m':COURT,'court_area_m2':88.4,'paving_rectangles_m':PAVING,
    'paving_union_area_m2':round(paved_area,3),'remaining_soft_landscape_and_strips_m2':round(88.4-paved_area,3),
    'planting_beds':BEDS,'outdoor_furniture':FURNITURE,'outdoor_routes':ROUTES,
    'route_envelope_m':1.0,'dining_chair_pullout_m':.4,'normal_route_probes':normal_probes,
    'pulled_out_route_probes':pulled_probes,'normal_issues':normal,'pulled_out_issues':pulled_issues,
    'retained_family_return_windows_y_width_m':family_windows,
    'garden_elevation_orientation':'Gym left, family wing right; mirrored relative to plan',
    'sliding_opening_widths_m':{'O04':2.6,'O06':2.8},'net_slider_opening_validated':False,
    'site_orientation_assigned':False,'solar_or_daylight_analysis':False,'privacy_verified':False,
    'stove_flue_plan_position_m':[flue_x,flue_y],
    'flue_marker_is_not_termination_height':True,'structural_roof_and_drainage_design':False
},indent=2)+'\n')
print(PDF)
print(f'Four routes pass in both chair positions; paving {paved_area:.2f} / 88.40 m2; orientation checks pass.')
