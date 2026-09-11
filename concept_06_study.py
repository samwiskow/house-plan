"""Independent roof study; reads concept 05 data without running its renderer."""
import ast
import json
from math import tan, radians
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).parent
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / 'concept-06-roof-elevations-sections.pdf'
source = ast.parse((ROOT / 'plan_model.py').read_text())
DATA = {}
for node in source.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ('OUTLINE', 'windows'):
                DATA[target.id] = ast.literal_eval(node.value)
OUTLINE = DATA['OUTLINE']
PITCH = 30
EAVE = 2.8
K = tan(radians(PITCH))
# Bounds, ridge direction, finish. The gym turns across its shorter depth.
VOLUMES = [
    ('Family wing', (0, 0, 8.2, 18.4), 'y', 'stone'),
    ('Guest / service wing', (16.2, 0, 22.8, 18.4), 'y', 'stone'),
    ('Shared room', (0, 12.8, 22.8, 18.4), 'x', 'timber'),
    ('Gym', (22.8, 11.7, 27.15, 18.4), 'x', 'stone'),
]
FACES = []
for name, (x0, y0, x1, y1), axis, finish in VOLUMES:
    if axis == 'y':
        mid = (x0 + x1) / 2
        FACES += [(name, (x0, y0, mid, y1), (K, 0, EAVE-K*x0)),
                  (name, (mid, y0, x1, y1), (-K, 0, EAVE+K*x1))]
    else:
        mid = (y0 + y1) / 2
        FACES += [(name, (x0, y0, x1, mid), (0, K, EAVE-K*y0)),
                  (name, (x0, mid, x1, y1), (0, -K, EAVE+K*y1))]
FACES.append(('Orangery', (12.2, 9.3, 16.2, 12.8), (0, .6/3.5, 2.6-.6/3.5*9.3)))


def z(plane, x, y):
    return plane[0]*x + plane[1]*y + plane[2]


def active(x, y):
    return [f for f in FACES if f[1][0]-1e-9 <= x <= f[1][2]+1e-9
            and f[1][1]-1e-9 <= y <= f[1][3]+1e-9]


def roof(x, y):
    faces = active(x, y)
    return max((z(f[2], x, y) for f in faces), default=0)


def plane_at(x, y):
    faces = active(x, y)
    return max(faces, key=lambda f: z(f[2], x, y))[2] if faces else None


def clip(poly, a, b, d):
    result = []
    for p, q in zip(poly, poly[1:]+poly[:1]):
        u, v = a*p[0]+b*p[1]+d, a*q[0]+b*q[1]+d
        if u >= -1e-9:
            result.append(p)
        if (u > 1e-9 and v < -1e-9) or (u < -1e-9 and v > 1e-9):
            t = u/(u-v)
            result.append((p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])))
    return result


xs = sorted({v for f in FACES for v in (f[1][0], f[1][2])})
ys = sorted({v for f in FACES for v in (f[1][1], f[1][3])})
PATCHES = []
for x0, x1 in zip(xs, xs[1:]):
    for y0, y1 in zip(ys, ys[1:]):
        candidates = active((x0+x1)/2, (y0+y1)/2)
        for face in candidates:
            poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            for other in candidates:
                poly = clip(poly, *(a-b for a, b in zip(face[2], other[2])))
                if len(poly) < 3:
                    break
            if len(poly) >= 3:
                PATCHES.append((face, poly))


pdfmetrics.registerFont(TTFont('Study', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('StudyBold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
C = {'ink':'#30392f', 'muted':'#6b6d5c', 'line':'#c9c5b7', 'paper':'#fffdf8',
     'stone':'#e3d2ad', 'timber':'#c49d68', 'roof1':'#d6c6ae', 'roof2':'#eee4d3',
     'glass':'#e2ece4', 'garden':'#eef1e3', 'accent':'#376248', 'white':'#ffffff'}
c = canvas.Canvas(str(PDF), pagesize=(420*mm, 297*mm))
c.setTitle('Concept 06 - roof, elevations and sections | first coordinated study')
c.setAuthor('House plan working study')


def colour(k):
    return HexColor(C.get(k, k))


def text(x, y, value, size=3, bold=False, align='left', fill='ink'):
    c.setFillColor(colour(fill))
    c.setFont('StudyBold' if bold else 'Study', size*mm)
    {'left':c.drawString, 'center':c.drawCentredString, 'right':c.drawRightString}[align](x*mm, (297-y)*mm, value)


def line(x, y, xx, yy, fill='ink', width=.3, dash=False):
    c.setStrokeColor(colour(fill)); c.setLineWidth(width*mm)
    c.setDash([2*mm, mm] if dash else [])
    c.line(x*mm, (297-y)*mm, xx*mm, (297-yy)*mm)
    c.setDash([])


def polygon(points, fill=None, stroke='ink', width=.3):
    p = c.beginPath(); p.moveTo(points[0][0]*mm, (297-points[0][1])*mm)
    for x, y in points[1:]: p.lineTo(x*mm, (297-y)*mm)
    p.close()
    if fill: c.setFillColor(colour(fill))
    if stroke: c.setStrokeColor(colour(stroke))
    c.setLineWidth(width*mm)
    c.drawPath(p, fill=bool(fill), stroke=bool(stroke))


def rect(x, y, w, h, fill=None, stroke='ink'):
    polygon([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],fill,stroke)


def para(x, y, lines, size=3, step=5):
    for t in lines:
        text(x,y,t,size); y+=step


def tag(x, y, label):
    w=pdfmetrics.stringWidth(label,'StudyBold',2.7*mm)/mm+3
    rect(x-w/2,y-3.3,w,4.5,'paper',None)
    text(x,y,label,2.7,True,'center')


def header(page, title, subtitle):
    rect(0,0,420,297,'paper',None)
    text(14,12,'COURTYARD HOUSE / CONCEPT 06 / FIRST ROOF STUDY',2.7,fill='muted')
    text(14,23,title,6.2,True)
    text(14,31,subtitle,3,fill='muted')
    line(14,36,406,36,'line')
    line(14,280,406,280,'line')
    text(14,287,'PROPOSAL | Concept 05 floor plan retained. Heights, openings and roof details require development. Not for construction.',2.45,fill='muted')
    text(406,287,f'{page} / 3',2.7,align='right',fill='muted')


def scale_bar(x,y):
    for i in range(5): rect(x+i*10,y,10,1.2,'ink' if i%2==0 else 'paper','ink')
    text(x,y-2,'0',2.5); text(x+50,y-2,'5 m',2.5,align='right')


def arrow(x,y,xx,yy):
    line(x,y,xx,yy,'accent',.35)
    dx,dy=xx-x,yy-y; n=(dx*dx+dy*dy)**.5
    ux,uy=dx/n,dy/n
    line(xx,yy,xx-ux*2-uy,yy-uy*2+ux,'accent',.35)
    line(xx,yy,xx-ux*2+uy,yy-uy*2-ux,'accent',.35)


header(1,'One plan, several roof junctions','Roof plan 1:100 at A3, printed at 100% | Metres | No north direction assigned')
ox,oy,s=20,61,10
xy=lambda x,y:(ox+x*s,oy+y*s)
polygon([xy(8.2,0),xy(16.2,0),xy(16.2,9.3),xy(12.2,9.3),xy(12.2,12.8),xy(8.2,12.8)],'garden',None)
for face,poly in PATCHES:
    fill='glass' if face[0]=='Orangery' else ('roof1' if face[2][0]+face[2][1]>0 else 'roof2')
    polygon([xy(*p) for p in poly],fill,None)
for face, poly in PATCHES:
    for a,b in zip(poly,poly[1:]+poly[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1]; n=(dx*dx+dy*dy)**.5
        if n<1e-7: continue
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        nx,ny=-dy/n*1e-5,dx/n*1e-5
        if plane_at(mx+nx,my+ny)!=plane_at(mx-nx,my-ny):
            line(*xy(*a),*xy(*b),'ink',.3)
polygon([xy(*p) for p in OUTLINE],None,'ink',.55)
for x0,y0,x1,y1 in [(1.8,5, .5,5),(6.3,5,7.7,5),(17.5,5,16.7,5),(21,5,22.3,5),
                         (10,14.8,10,13.3),(10,16.2,10,17.9),(25,14.3,25,12.3),(25,16,25,17.9),(14.2,11.8,14.2,9.8)]:
    arrow(*xy(x0,y0),*xy(x1,y1))
tag(*xy(4.1,2),'FAMILY RIDGE +5.17')
tag(*xy(19.5,2),'GUEST RIDGE +4.71')
tag(*xy(11.2,15.6),'SHARED RIDGE +4.42')
tag(*xy(25,15.05),'GYM +4.73')
tag(*xy(14.2,10.4),'LOW ROOF')
text(*xy(12.2,6),'OPEN COURTYARD',3,True,'center')
text(*xy(12.2,6.7),'88.40 m2 at ground level',2.7,align='center')
for x,y,label in [(8.2,12.8,'J1'),(16.2,12.8,'J2'),(22.8,13,'J3')]:
    tag(*xy(x,y),label)
line(*xy(9.5,-.8),*xy(9.5,19.3),'accent',.45,True)
line(*xy(-.8,14.2),*xy(28,14.2),'accent',.45,True)
tag(*xy(9.5,-1.3),'A');tag(*xy(9.5,19.8),'A')
tag(*xy(-1.1,14.2),'B');tag(*xy(28.1,14.2),'B')
text(20,49,'27.15 m overall wall envelope',2.8)
text(309,49,'WORKING ASSUMPTIONS',3.2,True)
para(309,57,['30 degree main roof pitches.','+2.80 m roof datum at wall edges.','Levels measured above floor +0.00.','Roof lines stop at wall faces;','eaves overhangs remain open.'])
text(309,88,'WHY THE RIDGES DIFFER',3.2,True)
para(309,96,['Family span: 8.20 m.','Guest span: 6.60 m.','Shared-room roof depth: 5.60 m.','Gym roof depth: 6.70 m.','A common pitch gives four heights.'])
text(309,128,'JUNCTIONS TO RESOLVE',3.2,True)
para(309,136,['J1  Family roof meets shared roof.','J2  Guest / shared / orangery meet.','J3  Gym ridge runs across the wing;','      a roof step needs detailing.','','Arrows show surface fall only.','Valleys lead toward inside','corners; outlets are not designed.'])
text(309,181,'ORANGERY: TEST ONLY',3.2,True)
para(309,189,['Low mono-pitch: +2.60 to +3.20 m.','Approx. 9.7 degrees, falling to court.','Its high edge meets the house','above the +2.80 m eave datum.','An abutment / local roof change','is required here, not yet resolved.'])
text(309,229,'WHAT IS RETAINED',3.2,True)
para(309,237,['319.91 m2 GIA; 360.26 m2 footprint.','Room layout and wall geometry.','Rooflights await junction design.'])
scale_bar(20,263)
text(84,265,'A-A and B-B locate the sections on sheet 3. Roof-covering colours are diagrammatic.',2.7,fill='muted')
c.showPage()


def elevation(base, arrival=False):
    def ex(x): return 20+(x if arrival else 27.15-x)*10
    def ep(x,h): return ex(x),base-h*10
    def area(points,fill,stroke='ink'): polygon([ep(*p) for p in points],fill,stroke)
    def opening(x,w,sill,head):
        area([(x,sill),(x+w,sill),(x+w,head),(x,head)],'glass')
        line(*ep(x+w/2,sill),*ep(x+w/2,head),'muted',.2)
    shared=EAVE+2.8*K; gym=EAVE+3.35*K
    area([(0,0),(22.8,0),(22.8,EAVE),(0,EAVE)],'timber')
    area([(0,EAVE),(22.8,EAVE),(22.8,shared),(0,shared)],'roof1')
    area([(22.8,0),(27.15,0),(27.15,EAVE),(22.8,EAVE)],'stone')
    area([(22.8,EAVE),(27.15,EAVE),(27.15,gym),(22.8,gym)],'roof2')
    for x0,x1 in [(0,8.2),(16.2,22.8)]:
        mid=(x0+x1)/2; ridge=EAVE+(x1-x0)/2*K
        area([(x0,0),(x1,0),(x1,EAVE),(mid,ridge),(x0,EAVE)],'timber' if arrival and x0==0 else 'stone')
        line(*ep(x0,EAVE),*ep(mid,ridge),'ink',.65)
        line(*ep(mid,ridge),*ep(x1,EAVE),'ink',.65)
    if arrival:
        for axis,x,y,w in DATA['windows']:
            if axis=='h' and y==18.4: opening(x,w,.55,2.35)
        for x,w in [(17.6,1),(21.15,1)]: opening(x,w,0,2.2)
        text(ex(18.1),base+6,'Entrance',2.8,align='center')
        text(ex(21.65),base+6,'Boot',2.8,align='center')
        text(ex(5.5),base+6,'Timber at the shared room',2.8,align='center')
    else:
        opening(.8,2.4,.75,2.35);opening(19,2.6,.75,2.35)
        opening(9,2.6,0,2.35)
        area([(12.2,0),(16.2,0),(16.2,2.6),(12.2,2.6)],'timber')
        area([(12.2,2.6),(16.2,2.6),(16.2,3.2),(12.2,3.2)],'glass')
        opening(13,2.8,0,2.3)
        text(ex(4.1),base+6,'Stone family wing',2.8,align='center')
        text(ex(10.1),base+6,'Dining',2.8,align='center')
        text(ex(14.2),base+6,'Orangery',2.8,align='center')
        text(ex(19.5),base+6,'Stone guest wing',2.8,align='center')
    text(ex(25),base+6,'Gym',2.8,align='center')
    line(15,base,296,base,'ink',.5)
    for x0,x1 in ([(0,8.2)] if arrival else [(8.2,12.2)]):
        for i in range(int((x1-x0)/.3)):
            x=x0+i*.3
            if arrival and any(a<=x<=a+w for a,w in [(1.1,3.1),(6.6,3)]): continue
            if not arrival and 9<=x<=11.6: continue
            line(*ep(x,.05),*ep(x,2.75),'#b38f60',.15)
    return ep


header(2,'Stone wings, timber shared room','Garden and arrival elevations 1:100 at A3 | Opening widths from concept 05; all vertical dimensions proposed')
text(20,49,'01 / FROM THE MAIN GARDEN, LOOKING INTO THE U',3.3,True)
ep=elevation(114)
assert ep(25,0)[0] < ep(4.1,0)[0]
for x,h,label in [(4.1,5.167,'+5.17'),(19.5,4.705,'+4.71'),(25,4.734,'+4.73')]: tag(*ep(x,h+.35),label)
text(309,56,'A RECESSED CENTRE',3.3,True)
para(309,65,['The stone gables frame the view.','Dining sits at the back of the U;','the lounge remains behind the','family wing, as in arrangement A.','','Orthographic view: depth is not','visible here. Use the roof plan','to read the courtyard setback.'])
text(20,144,'02 / FROM THE ARRIVAL SIDE, LOOKING TOWARD THE GARDEN',3.3,True)
ep=elevation(211,True)
assert ep(25,0)[0] > ep(4.1,0)[0]
text(309,151,'THE EVERYDAY FRONT',3.3,True)
para(309,160,['Timber follows the shared-room','wall, including its lounge end.','Stone continues around the','entrance / service wing and gym.','','Entrance and boot doors keep','their measured positions.','Canopies, steps and carport','are outside this first study.'])
line(14,229,406,229,'line')
text(20,238,'READING THESE ELEVATIONS',3.2,True)
para(20,246,['Warm buff stone, honey timber and a warm muted roof tone express the materials brief.',
            'Roof colour is a placeholder. Covering, pitch suitability, eaves, gutters and timber weathering remain open.',
            'Window heads: +2.35 m. Garden bedroom sills: +0.75 m; arrival shared-room sills: +0.55 m.',
            'The stove / flue and proposed rooflights are deferred until roof junctions and internal positions are agreed.'],2.9,4.7)
scale_bar(336,267)
c.showPage()


def section_profile(base, start, end, fixed, axis):
    values=[start+(end-start)*i/1200 for i in range(1201)]
    points=[(20+v*10,base-roof(v,fixed)*10) if axis=='x' else (20+v*10,base-roof(fixed,v)*10) for v in values]
    for a,b in zip(points,points[1:]):
        if a[1]<base and b[1]<base: line(*a,*b,'ink',.65)


header(3,'The ceiling needs its own design','Two located sections 1:100 at A3 | Vertical roof profiles derive from the same geometry as sheet 1')
text(20,49,'B-B / ACROSS LOUNGE, DINING, KITCHEN, LAUNDRY AND GYM',3.3,True)
base=115
section_profile(base,0,27.15,14.2,'x')
for x0,x1,name in [(.35,17.75,'Shared kitchen / dining / living'),(17.87,22.45,'Laundry'),(22.8,26.8,'Gym')]:
    line(20+x0*10,base,20+x1*10,base,'ink',1)
    text(20+(x0+x1)*5,base+7,name,2.7,align='center')
for x in [0,.35,17.75,17.87,22.45,22.8,26.8,27.15]:
    h=2.6 if 17<x<23 else max(0,roof(min(27.15,max(0,x)),14.2)-.3)
    line(20+x*10,base,20+x*10,base-h*10,'ink',.5)
line(20+17.87*10,base-26,20+26.8*10,base-26,'accent',.45,True)
text(20+24.5*10,base-21,'2.60 m ceiling?',2.6,align='center',fill='accent')
for x,y,w,h in [(4.6,0,1,.8),(7.15,0,2.4,.75),(10.95,0,2.8,.92)]:
    rect(20+x*10,base-(y+h)*10,w*10,h*10,'timber')
text(309,55,'A CHANGE ABOVE THE SOFA',3.2,True)
para(309,64,['The family-wing roof continues','over the lounge end. A fully open','ceiling would change direction','between lounge and dining.','','Test a deliberate ceiling transition','or a revised roof junction before','assuming one uninterrupted vault.'])
text(309,110,'Furniture is shown beyond the cut.',2.9)
text(309,115,'Gym height needs equipment checks.',2.9)
line(14,136,406,136,'line')
text(20,146,'A-A / THROUGH THE COURTYARD AND SHARED ROOM AT x = 9.50 m',3.3,True)
base=222
section_profile(base,0,18.4,9.5,'y')
line(20,base,20+12.8*10,base,'line',.6)
line(20+12.8*10,base,20+18.4*10,base,'ink',1)
for y in [12.8,13.15]:
    line(20+y*10,base,20+y*10,base-(roof(9.5,y)-.3)*10,'ink',.5)
for y in [18.05,18.4]:
    line(20+y*10,base,20+y*10,base-5.5,'ink',.5)
    line(20+y*10,base-23.5,20+y*10,base-(roof(9.5,y)-.3)*10,'ink',.5)
line(20+18.05*10,base-5.5,20+18.4*10,base-5.5,'ink',.5)
line(20+18.225*10,base-5.5,20+18.225*10,base-23.5,'accent',.25)
line(20+12.8*10,base-23.5,20+13.15*10,base-23.5,'ink',.5)
line(20+12.975*10,base,20+12.975*10,base-23.5,'accent',.25)
line(20+13.15*10,base-25,20+15.6*10,base-40.9,'accent',.35,True)
line(20+15.6*10,base-40.9,20+18.05*10,base-25,'accent',.35,True)
rect(20+15.2*10,base-7.5,10,7.5,'timber')
tag(20+15.6*10,base-49,'ROOF +4.42')
text(68,base+7,'Open courtyard',2.8,align='center')
text(20+15.6*10,base+7,'4.90 m clear room depth',2.8,align='center')
text(228,161,'HEIGHTS TO TEST, NOT TARGETS TO FREEZE',3.2,True)
para(228,170,['The main roof datum is +2.80 m at the external wall face.',
              'A 2.60 m flat ceiling is tested in laundry and gym.',
              'The dashed pitched ceiling indicates the shared-room intent;',
              'its exact underside depends on structure and insulation.',
              'No beam, truss, roof thickness or clear apex height is specified.'],2.9,5)
text(228,205,'THE NEXT TWO DECISIONS',3.2,True)
para(228,214,['1. Should the lounge join the dining vault, or have a calmer',
              '   separate ceiling beneath the intersecting family roof?',
              '2. Is the orangery seasonal or a year-round heated room?',
              '   Its low roof and three-way junction need that brief.'],2.9,5)
line(14,245,406,245,'line')
para(20,254,['Checked: source outline and window widths retained; ridge calculations, roof coverage and section samples agree.',
            'Unresolved: structural support, roof steps/abutments, rainwater outlets, insulation, acoustics, daylight and stove/flue.',
            'This study exposes those interfaces; it does not establish technical compliance or suitability for a particular site.'],2.9,4.8)
c.showPage(); c.save()


def inside(x,y):
    result=False
    for a,b in zip(OUTLINE,OUTLINE[1:]+OUTLINE[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: result=not result
    return result


checks=0
for i in range(272):
    for j in range(185):
        x,y=i*.1+.003,j*.1+.003
        assert bool(active(x,y))==inside(x,y),(x,y)
        checks+=1
ridge_levels={name:round(EAVE+((bounds[2]-bounds[0]) if axis=='y' else (bounds[3]-bounds[1]))/2*K,4)
              for name,bounds,axis,_ in VOLUMES}
assert abs(roof(4.1,1)-ridge_levels['Family wing'])<1e-4
assert abs(roof(19.5,1)-ridge_levels['Guest / service wing'])<1e-4
assert abs(roof(10,15.6)-ridge_levels['Shared room'])<1e-4
assert abs(roof(25,15.05)-ridge_levels['Gym'])<1e-4
(OUT/'concept-06-study-check.json').write_text(json.dumps({
    'baseline':'concept 05', 'roof_pitch_degrees':PITCH,'roof_wall_edge_datum_m':EAVE,
    'ridge_levels_m':ridge_levels,'roof_coverage_sample_checks':checks,
    'baseline_geometry_read_only':True,
    'elevation_orientation':'Garden: gym left; arrival: gym right',
    'limitations':['Unresolved roof abutments and drainage','No structural or compliance validation','No site orientation']
},indent=2)+'\n')
print(PDF)
print(f'Roof coverage checked at {checks} points; ridge levels: {ridge_levels}')
