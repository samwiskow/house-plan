"""Concept 10: lighting positions, control scenes and an illustrative evening view."""
import ast
import json
from pathlib import Path
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).parent
src=ast.parse((ROOT/'shared_space_study.py').read_text())
cut=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
s={'__file__':str(ROOT/'shared_space_study.py')}
exec(compile(ast.Module(body=src.body[:cut],type_ignores=[]),str(ROOT/'shared_space_study.py'),'exec'),s)
m=s['m'];np=s['np']
court=json.loads((ROOT/'output/pdf/concept-09-study-check.json').read_text())
OUT=ROOT/'output/pdf';TMP=ROOT/'tmp/pdfs/concept-10';TMP.mkdir(parents=True,exist_ok=True)
PDF=OUT/'concept-10-lighting-scenes.pdf'
GROUPS={
 'K':('Kitchen task','6 adjustable ceiling spots','2700 K; beam/output study needed'),
 'A':('Soft ambient','4 concealed linear runs','2700 K; accessible ledges/drivers'),
 'H':('Pantry / WC approach','3 concealed wall runs toward pantry / WC','2700 K; separate dimmable ambient group'),
 'D':('Dining feature','Existing six-arm chandelier','2700 K; dimmable lamps'),
 'L':('Lounge reading','2 shaded lamps','2700 K; local controls retained'),
 'G':('Garden-room reading','1 wall reading light on solid pier','2700 K; no fixing to roof glass'),
 'E':('Courtyard pillars + thresholds','4 bronze pillars + 2 low threshold lights','0.75 m pillars; 2200-2700 K; shielded downward'),
 'W':('Courtyard ambient wall lights','7 broad downward lights; numbers match markup','2.00 m mounting proposal; separate dimmer'),
 'T':('Pantry / WC local task','Pantry shelf light + WC mirror light','Local switches; independent of shared scenes'),
 'P':('Garden-room table lamp','1 rechargeable, manually operated','Indoor only; courtyard tables stay clear')}
SCENES={'Everyday':{'K':100,'A':50,'D':60,'L':30,'G':50,'H':50,'E':0,'W':0},
        'Entertaining':{'K':15,'A':25,'D':40,'L':40,'G':30,'H':35,'E':30,'W':35},
        'Quiet evening':{'K':0,'A':10,'D':0,'L':35,'G':20,'H':20,'E':15,'W':10}}
LIGHTS=[]
def light(group,point,kind,target=None,length=0,axis='x'):
    count=sum(l['group']==group for l in LIGHTS)+1
    LIGHTS.append({'id':f'{group}{count}','group':group,'point_m':point,'kind':kind,'target_m':target,'length_m':length,'axis':axis})
for x in [11.35,12.35,13.35]:light('K',(x,15.65,s['tan'](s['radians'](30))*(18.05-15.65)+3.5-.07),'spot',(x,15.65,.92))
for x in [10.25,11.35,12.2]:light('K',(x,17.13,3.5+(18.05-17.13)*s['tan'](s['radians'](30))-.07),'spot',(x,17.7,.92))
for x,y,length in [(1.9,13.2,2.2),(6.2,13.2,2.6),(2.65,18,2.8),(8.1,18,2.8)]:light('A',(x,y,3.28),'linear',length=length)
light('H',(15.15,15.28,2.65),'linear',length=1.8)
light('H',(17.70,14.2,2.65),'linear',length=1.3,axis='y')
light('H',(17.70,11.85,2.35),'linear',length=.9,axis='y')
light('T',(15.15,15.6,1.5),'linear',length=1.8)
light('T',(18.95,12.22,1.85),'linear',length=.6)
light('D',(8.35,15.7,2.35),'chandelier')
light('L',(.7,17.1,1.05),'table lamp')
light('L',(4.2,17.55,1.35),'floor lamp')
light('G',(12.60,10.1,1.45),'wall reading',(13.1,10.65,.7))
light('E',(12.18,12.3,.35),'wall path',(11.25,12.1,0))
light('E',(15.95,9.28,.35),'wall path',(15.1,8.75,0))
for x,y,tx,ty in [(14.25,8,13.5,8),(14.25,5,13.5,5),(12.5,3.3,13.35,3.3),(12.5,.6,11.8,.6)]:
    light('E',(x,y,.65),'pillar',(tx,ty,0))
# W1-W7 follow the user's annotated positions, adjusted onto solid wall faces.
for x,y,tx in [(8.24,7.9,11.1),(8.24,12.4,10.9),(8.24,4.1,11.2),(8.24,.85,11.2),
               (16.16,.8,13.2),(16.16,3.6,13.2),(16.16,7.9,13.2)]:
    light('W',(x,y,2.0),'ambient wall',(tx,y,.25))
light('P',(14.1,11.3,.66),'portable')
for l in LIGHTS:
    if l['group']!='W':continue
    x,y,z=l['point_m']
    wall_x=8.2 if x<12 else 16.2
    assert not any(orientation=='v' and abs(wx-wall_x)<.01 and wy-.15<y<wy+width+.15
                   for orientation,wx,wy,width in m.windows),(l['id'],'window conflict')
    assert m.inside(l['target_m'][:2],court['court_polygon_m'])

PILLAR_BASES=[(l['point_m'][0]-.09,l['point_m'][1]-.09,.18,.18) for l in LIGHTS if l['kind']=='pillar']
CONTROLS=[('S1',(16.3,15.3),'Entrance / shared room'),('S2',(4.65,13.2),'Family-hall approach'),('S3',(11.85,13.2),'Dining slider pier')]
for levels in SCENES.values():
    assert set(levels)==set(GROUPS)-{'P','T'} and all(0<=v<=100 for v in levels.values())
assert all(l['target_m'][2]<l['point_m'][2] for l in LIGHTS if l['group'] in ('E','W'))
assert all(l['point_m'][0]>12 for l in LIGHTS if l['group']=='E')
assert sum(l['group']=='D' for l in LIGHTS)==1
assert not any(l['kind']=='spot' and m.inside(l['point_m'][:2],m.R['OR'].poly) for l in LIGHTS)
# Reserve the added floor-lamp base and rerun the existing indoor route checks.
m.furn('KL','Lighting floor-lamp base',4.10,17.45,.2,.2,'lamp')
route_issues=m.verify();assert not route_issues,route_issues
m.furniture.pop()
# Check new pillar bases against the retained furniture, planting and route envelopes.
from math import hypot
for base in PILLAR_BASES:
    assert all(m.inside(p,court['court_polygon_m']) for p in m.box(*base))
    assert not any(m.overlap(base,bed)>0 for _,bed in court['planting_beds'])
    for name,(x,y,w,h),_,_ in court['outdoor_furniture']:
        for pull in (0,.4):
            offset=-pull if name=='Dining north' else pull if name=='Dining south' else 0
            assert m.overlap(base,(x,y+offset,w,h))==0,(base,name)
    for points in court['outdoor_routes'].values():
        for a,b in zip(points,points[1:]):
            for t in np.linspace(0,1,max(2,int(hypot(b[0]-a[0],b[1]-a[1])/.025)+1)):
                x,y=np.array(a)+(np.array(b)-a)*t
                dx=max(base[0]-x,0,x-base[0]-base[2]);dy=max(base[1]-y,0,y-base[1]-base[3])
                assert hypot(dx,dy)>.5,(base,(x,y))

C={'paper':'#fffdf8','ink':'#30392f','muted':'#6a6656','line':'#c9c0af','amber':'#ba7937','gold':'#f5d69a',
   'furniture':'#dec9a5','shared':'#f1e6d4','family':'#f4f0e7','guest':'#f4f0e7','service':'#f4f0e7','circulation':'#faf6ed','garden':'#e5e9d5','green':'#376248'}
m.PALETTE.update(C)
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm))
m.c.setTitle('Concept 10 - lighting plan and three evening settings')
m.c.setAuthor('House plan working study')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.2,True);m.paragraph(x,y+7,lines,size=2.8,step=5)
def header(n,title,subtitle):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 10 / LIGHT + CONTROLS',2.7,fill='muted')
    text(14,23,title,6.0,True);text(14,31,subtitle,2.85,fill='muted')
    m.line(14,36,406,36,'line',.3);m.line(14,280,406,280,'line',.25)
    text(14,287,'LIGHTING INTENT | Locations and dimming values are proposals. No lux, glare, electrical or ecological compliance calculation.',2.4,fill='muted')
    text(406,287,f'{n} / 3',2.6,align='right',fill='muted')


header(1,'Light the activity, soften the edges','Lighting plan 1:100 at A3, printed at 100% | Symbols show proposed positions above the furnished plan; they are not coverage contours')
p=m.Plan(20,52,10)
m.c.saveState();clip=m.c.beginPath();clip.rect(14*m.mm,(297-240)*m.mm,208*m.mm,191*m.mm);m.c.clipPath(clip,stroke=0)
p.poly(court['court_polygon_m'],'garden',None)
for r in court['paving_rectangles_m']:p.rect(*r,'#e6dac3',None)
for name,r in court['planting_beds']:p.rect(*r,'#a6b587',None)
for name,r,mat,kind in court['outdoor_furniture']:p.rect(*r,'furniture','muted',.12)
old_furniture,old_doors=m.furniture,m.doors
m.furniture=[f for f in m.furniture if f['room'] in ('KL','OR','PA','WC')]
m.doors=[d for d in m.doors if d.id not in ('O05','O07')]
p.draw(labels=False);m.furniture,m.doors=old_furniture,old_doors
# Fade rooms outside this study without implying they have no lighting.
m.rect(21,53,76,125,'#f4f0e7',None)
text(56,93,'FAMILY ROOMS',2.5,True,align='center',fill='muted');text(56,99,'Separate lighting study',2.4,align='center',fill='muted')
for l in LIGHTS:
    x,y,z=l['point_m'];X,Y=p.xy((x,y));group=l['group']
    if l['kind']=='linear':
        dx=l['length_m']/2 if l['axis']=='x' else 0;dy=l['length_m']/2 if l['axis']=='y' else 0
        p.line((x-dx,y-dy),(x+dx,y+dy),'amber',.8)
    elif l['kind']=='pillar':m.rect(X-1.2,Y-1.2,2.4,2.4,'amber','ink',.15)
    else:
        m.c.setFillColor(m.color('gold'));m.c.setStrokeColor(m.color('amber'));m.c.setLineWidth(.2*m.mm)
        m.c.circle(X*m.mm,(297-Y)*m.mm,1.05*m.mm,stroke=1,fill=1)
    if group in ('K','A'):continue
    label_x=X-6 if group=='W' and x>12 else X-3 if group=='H' and l['axis']=='y' else X+1.8
    text(label_x,Y+4.5 if l['id']=='T1' else Y-1.4,l['id'],2.2,True,fill='amber')
for x,y,label in [(12.5,16.45,'K / TASK'),(5.8,13.65,'A'),(2.8,17.7,'A'),(8.6,17.7,'A')]:p.text(x,y,label,2.3,fill='amber')
for id,(x,y),label in CONTROLS:
    X,Y=p.xy((x,y));m.rect(X-1.3,Y-1.3,2.6,2.6,'green',None);text(X+2,Y-1.6,id,2.4,True,fill='green')
p.text(10.5,2.0,'MAIN GARDEN',2.4,fill='muted')
p.text(14.3,12.2,'GARDEN ROOM',2.4)
p.text(3,16,'LOUNGE',2.4)
p.text(15.15,16.8,'PANTRY',2.4)
p.text(18.65,13.15,'WC',2.4)
p.text(17.05,12.7,'HALL',2.0)
m.c.restoreState()
text(23,253,'Amber: lights / amber square: pillar / green square: controls',2.6,fill='muted')
for i in range(5):m.rect(23+i*10,261,10,1,'ink' if i%2==0 else 'paper','ink',.1)
text(23,269,'0',2.4);text(73,269,'5 m',2.4,align='right')
y=49
for key,(name,description,detail) in GROUPS.items():
    text(240,y,f'{key} / {name.upper()}',3.05,True)
    text(240,y+5.5,description,2.8)
    text(240,y+10.5,detail,2.65,fill='muted')
    y+=19.5
note(240,253,'TWO OUTDOOR LIGHTING LAYERS',[
    'W adds broad ambient light around the retained E pillars / thresholds.',
    'Aim across paving; check overlap and bedroom-window spill on site.' ])
m.c.showPage()

header(2,'Three settings, with ordinary wall controls','Starting dimmer values for commissioning, not calculated light output | Eight scene groups; pantry / WC task and indoor portable lamp stay local')
cols=[20,137,201,267,339]
for x,label in zip(cols,['GROUP','EVERYDAY','ENTERTAINING','QUIET EVENING','CONTROL']):text(x,51,label,2.8,True)
m.line(20,57,401,57,'line',.25)
for i,(key,(name,_,_)) in enumerate(GROUPS.items()):
    y=66+i*14
    if i%2==0:m.rect(18,y-7,383,14,'#f1eadc',None)
    text(22,y,f'{key}  {name}',3)
    for x,scene in zip(cols[1:4],SCENES):text(x,y,('Local / optional' if key=='P' else 'On demand' if key=='T' else f'{SCENES[scene][key]}%'),2.85)
    text(339,y,'Local switch' if key=='T' else 'Manual' if key=='P' else ('Scene + local' if key in ('L','G') else 'Scene + override'),2.65)
note(20,211,'WHERE THE BUTTONS GO',[
    'S1: enter the shared room from the entrance hall.',
    'S2: enter from the family-bedroom hall.',
    'S3: beside the dining slider, inside on the solid pier.',
    'Each recalls the three scenes, dims and turns the shared lights off.',
    'S3 also switches / dims E pillars and W wall lights independently.' ])
note(220,211,'HOW IT SHOULD BEHAVE',[
    'Everyday starts with outside lights off; override when needed.',
    'Outside scene levels apply after dark while the court is in use.',
    'Propose a 60-minute outside auto-off, extendable at S3.',
    'Pantry shelf / WC mirror lights have independent local switches.',
    'Keep local reading controls and dedicated labelled lamp outlets.' ])
text(20,267,'Groups describe the intended controls, not final wiring circuits. Match dimmers, drivers and lamps; keep general power sockets separate.',2.65,fill='muted')
m.c.showPage()

# Reuse the measured geometry, omitting the source document's authoring and exports.
Cnode=next(n for n in src.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='C' for t in n.targets))
s['C']=ast.literal_eval(Cnode.value)
face_start=next(i for i,n in enumerate(src.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='faces' for t in n.targets))
render_index=next(i for i,n in enumerate(src.body) if isinstance(n,ast.FunctionDef) and n.name=='render')
geometry=ast.unparse(ast.Module(body=src.body[face_start:render_index],type_ignores=[])).replace("'linen', 0.085)","'glowD', 0.085)")
s['C'].update({'glowD':'#ffdf9d','glow':'#ffe3a6','sky':'#253746','glass':'#34474b','plant':'#6d7950','paving':'#dac8a9'})
exec(compile(geometry,'concept-08-scene','exec'),s)
cube,face,cylinder=s['cube'],s['face'],s['cylinder']
for r in court['paving_rectangles_m']:cube(r[0],r[1],-.025,r[2],r[3],.005,'paving')
for name,(x,y,w,d) in court['planting_beds']:cube(x,y,-.03,w,d,.8 if x<10 else .65,'plant')
face([(8.2,0,0),(8.2,3,0),(8.2,3,3.2),(8.2,0,3.2)],'stone')
face([(8.205,2.9,.75),(8.205,3.75,.75),(8.205,3.75,2.35),(8.205,2.9,2.35)],'glass')
face([(16.2,0,0),(16.2,9.3,0),(16.2,9.3,3.2),(16.2,0,3.2)],'stone')
for name,(x,y,w,d),mat,kind in court['outdoor_furniture']:
    if kind=='table':
        h=.75 if name=='Dining table' else .4
        s['legs'](x,y,w,d,h-.05,'oak');cube(x,y,h-.05,w,d,.05,'oak')
    else:
        s['legs'](x,y,w,d,.4,'oak');cube(x,y,.4,w,d,.08,'linen')
        back={'west':(x+w-.1,y,.1,d),'east':(x,y,.1,d),'south':(x,y,w,.08),'north':(x,y+d-.08,w,.08)}[kind]
        cube(back[0],back[1],.48,back[2],back[3],.32,'linen')
for l in LIGHTS:
    x,y,z=l['point_m'];kind=l['kind']
    if kind=='chandelier':continue
    if kind=='linear':
        if l['axis']=='x':cube(x-l['length_m']/2,y-.02,z,l['length_m'],.04,.025,'glow' if l['group']!='T' else 'bronze')
        else:cube(x-.02,y-l['length_m']/2,z,.04,l['length_m'],.025,'glow')
    elif kind=='ambient wall':
        cube(x-.055,y-.12,z-.12,.11,.24,.24,'bronze')
        face([(x-.055,y-.095,z-.121),(x+.055,y-.095,z-.121),(x+.055,y+.095,z-.121),(x-.055,y+.095,z-.121)],'glow')
    elif kind=='pillar':
        cube(x-.09,y-.09,0,.18,.18,.75,'bronze')
        side=1 if l['target_m'][0]>x else -1
        xx=x+side*.091
        face([(xx,y-.055,.59),(xx,y+.055,.59),(xx,y+.055,.68),(xx,y-.055,.68)],'glow')
    elif kind in ('table lamp','floor lamp','portable'):
        floor=.5 if kind=='table lamp' else (z-.25 if kind=='portable' else 0)
        cylinder((x,y,floor),(x,y,z-.12),.014,'bronze')
        cylinder((x,y,z-.12),(x,y,z+.12),.13 if kind!='portable' else .075,'glow',.075)
    else:cube(x-.045,y-.045,z-.035,.09,.09,.07,'glow')

# This mood render uses illustrative falloff; no fixture photometry or reflected-glass model.
render_source=ast.unparse(src.body[render_index])
render_source=render_source.replace("pixels[:] = [235, 239, 226]","pixels[:] = [25, 35, 42]\n    emitting=np.zeros((height,width),dtype=bool)")
a=render_source.index('        shade =');b=render_source.index('        view =',a)
render_source=render_source[:a]+"        colour=np.array([int(C[material][i:i+2],16) for i in [1,3,5]],dtype=np.uint8)\n"+render_source[b:]
render_source=render_source.replace("normals[ymin:ymax + 1, xmin:xmax + 1][mask] = normal", "normals[ymin:ymax + 1, xmin:xmax + 1][mask] = normal\n            emitting[ymin:ymax+1,xmin:xmax+1][mask]=material.startswith('glow')")
a=render_source.index('    edge =')
shading='''    yy,xx=np.mgrid[0:height,0:width]
    depth=np.where(np.isfinite(zbuf),zbuf,0)
    world=cam+depth[...,None]*forward+((xx-width/2)/focal*depth)[...,None]*right+((height/2-yy)/focal*depth)[...,None]*up
    X,Y,Z=world[...,0],world[...,1],world[...,2]
    outdoors=(X>=8.2)&(X<16.2)&(Y>=0)&((Y<9.3)|((X<12.2)&(Y<12.8)))
    illumination=np.full((height,width),.18)
    levels=SCENES['Entertaining']
    for l in LIGHTS:
        group=l['group'];pos=np.array(l['point_m']);delta=pos-world
        dist2=np.sum(delta*delta,axis=2)
        level=(.3 if group=='P' else 0 if group=='T' else levels[group]/100)
        gain={'K':5,'A':5,'D':11,'L':6,'G':6,'H':3,'E':3,'W':8,'T':0,'P':3}[group]
        is_out=(group in ('E','W')) or (group=='P' and pos[1]<9.3)
        region=outdoors if is_out else ~outdoors
        falloff=1/(1+dist2)
        if group in ('K','G','E','W'):
            direction=np.array(l['target_m'])-pos;direction/=np.linalg.norm(direction)
            cosine=np.sum((-delta)*direction,axis=2)/np.sqrt(np.maximum(dist2,.01))
            if group=='W':falloff*=np.clip((cosine-.25)/.75,0,1)*(Z<pos[2])
            else:falloff*=np.clip((cosine-.55)/.45,0,1)**2
        illumination+=gain*level*falloff*region
    illumination=np.clip(illumination,.12,1.1)
    pixels=np.clip(pixels.astype(float)*illumination[...,None]*np.array([1.0,.91,.76]),0,255).astype(np.uint8)
    pixels[emitting]=[255,221,155]
'''
render_source=render_source[:a]+shading+render_source[a:]
# Use the original projection and orientation check with a view toward the courtyard.
s.update({'LIGHTS':LIGHTS,'SCENES':SCENES})
exec(compile(render_source,'evening-render','exec'),s)
CAM=(9.0,17.6,1.6);TARGET=(11.7,8.0,1.85)
assert m.inside(CAM[:2],m.R['KL'].poly)
assert not any(m.inside(CAM[:2],m.box(*f['rect'])) for f in m.furniture)
view=s['render'](CAM,TARGET,TMP/'evening.png')
header(3,'An evening view into the courtyard','Entertaining setting / Eye height 1.60 m near dining | Illustrative light and colour; not a photometric simulation')
m.c.drawImage(ImageReader(str(TMP/'evening.png')),14*m.mm,69*m.mm,392*m.mm,181.75*m.mm)
m.line(14,234,406,234,'line',.25)
note(20,245,'THE INTENDED BALANCE',[
    'Dimmed chandelier and lamps; kitchen task light stays in reserve.',
    'Seven perimeter wall lights add broad ambient light to the four pillars.',
    'Separate E / W dimmers balance route light and the wider courtyard.' ])
note(225,245,'WHAT THIS VIEW CANNOT VERIFY',[
    'Brightness, glare, spill, shadows and glass reflections need testing.',
    'Mounting details, electrical design and outdoor ratings remain open.',
    'Outdoor intent follows the DarkSky / IES lighting principles.' ])
m.c.linkURL('https://darksky.org/resources/guides-and-how-tos/lighting-principles/',(225*m.mm,27*m.mm,400*m.mm,33*m.mm),relative=0)
m.c.showPage();m.c.save()
(OUT/'concept-10-study-check.json').write_text(json.dumps({
 'status':'Revised proposal: seven courtyard wall lights added to retained pillars','groups':GROUPS,'lights':LIGHTS,
 'scenes_percent':SCENES,'manual_portables_group':'P','local_task_group':'T','controls':CONTROLS,
 'wall_light_mounting_height_m':2.0,'wall_light_numbers_match_user_markup':True,
 'wall_light_window_position_issues':[],'uniformity_verified':False,
 'pillar_height_m':.75,'pillar_bases_m':PILLAR_BASES,'pillar_route_clearance_issues':[],
 'outdoor_auto_off_proposal_minutes':60,'indoor_route_issues_with_floor_lamp':route_issues,
 'camera':view,'photometric_calculation':False,'electrical_design':False,'glare_reflections_or_ecology_verified':False,
 'outdoor_reference':'https://darksky.org/resources/guides-and-how-tos/lighting-principles/'},indent=2)+'\n')
print(PDF)
print(f'{len(LIGHTS)} light locations; eight scene groups plus local task and one indoor portable; scene and route checks pass.')
