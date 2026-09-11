"""Continuous shared-room vault and lower-wing massing over concept 05."""
import ast
import json
from math import radians, tan
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).parent
OUT = ROOT / 'output/pdf'
PDF = OUT / 'concept-06b-continuous-vault-low-wings.pdf'
DATA = {}
for node in ast.parse((ROOT/'plan_model.py').read_text()).body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ('OUTLINE','windows','open_poly'):
                DATA[target.id] = ast.literal_eval(node.value)
PITCH = 30
K = tan(radians(PITCH))
EAVE = 3.70
RIDGE = EAVE + 2.8*K
LOW_TOP = 3.20
SPRING = 3.50
APEX = SPRING + 2.45*K
LOW_ZONES = [('Family wing',(0,0,8.2,12.8)),('Guest wing',(16.2,0,22.8,12.8)),
             ('Gym',(22.8,11.7,27.15,18.4)),('Orangery',(12.2,9.3,16.2,12.8))]
MAIN = (0,12.8,22.8,18.4)

def within(x,y,b): return b[0]<=x<=b[2] and b[1]<=y<=b[3]
def roof(x,y):
    if within(x,y,MAIN): return EAVE+min(y-12.8,18.4-y)*K
    if any(within(x,y,b) for _,b in LOW_ZONES): return LOW_TOP
    return 0

def ceiling(y): return SPRING+min(y-13.15,18.05-y)*K

def page_x(x,arrival=False): return 20+10*(x if arrival else 27.15-x)

def inside(x,y,poly):
    result=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: result=not result
    return result

pdfmetrics.registerFont(TTFont('Study','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('StudyBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
C={'ink':'#30392f','muted':'#6b6d5c','line':'#c9c5b7','paper':'#fffdf8',
   'stone':'#e3d2ad','timber':'#c49d68','roof1':'#d6c6ae','roof2':'#eee4d3',
   'glass':'#e2ece4','garden':'#eef1e3','accent':'#376248','old':'#9a6341'}
c=canvas.Canvas(str(PDF),pagesize=(420*mm,297*mm))
c.setTitle('Concept 06B - continuous vault and lower stone wings')
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


def scale_bar(x,y):
    for i in range(5): rect(x+i*10,y,10,1.2,'ink' if i%2==0 else 'paper','ink')
    text(x,y-2,'0',2.5); text(x+50,y-2,'5 m',2.5,align='right')


def arrow(x,y,xx,yy):
    line(x,y,xx,yy,'accent',.35)
    dx,dy=xx-x,yy-y; n=(dx*dx+dy*dy)**.5
    ux,uy=dx/n,dy/n
    line(xx,yy,xx-ux*2-uy,yy-uy*2+ux,'accent',.35)
    line(xx,yy,xx-ux*2+uy,yy-uy*2-ux,'accent',.35)


def header(page,title,subtitle):
    rect(0,0,420,297,'paper',None)
    text(14,12,'COURTYARD HOUSE / CONCEPT 06B / CONTINUOUS VAULT + LOWER WINGS',2.7,fill='muted')
    text(14,23,title,6.2,True)
    text(14,31,subtitle,3,fill='muted')
    line(14,36,406,36,'line');line(14,280,406,280,'line')
    text(14,287,'EXPLORATORY OPTION | Concept 05 floor plan retained. Heights and roof connections are proposals, not construction details.',2.45,fill='muted')
    text(406,287,f'{page} / 3',2.7,align='right',fill='muted')


header(1,'Let the shared room lead','Roof arrangement 1:100 at A3, printed at 100% | Low-roof outlines show envelope tops, not drainage surfaces')
xy=lambda x,y:(20+x*10,61+y*10)
polygon([xy(8.2,0),xy(16.2,0),xy(16.2,9.3),xy(12.2,9.3),xy(12.2,12.8),xy(8.2,12.8)],'garden',None)
for name,(x0,y0,x1,y1) in LOW_ZONES:
    polygon([xy(x0,y0),xy(x1,y0),xy(x1,y1),xy(x0,y1)],'glass' if name=='Orangery' else 'roof2')
for y0,y1,col in [(12.8,15.6,'roof1'),(15.6,18.4,'roof2')]:
    polygon([xy(0,y0),xy(22.8,y0),xy(22.8,y1),xy(0,y1)],col)
polygon([xy(*p) for p in DATA['OUTLINE']],None,'ink',.55)
for a,b in zip(DATA['open_poly'],DATA['open_poly'][1:]+DATA['open_poly'][:1]):
    line(*xy(*a),*xy(*b),'accent',.35,True)
text(*xy(4.1,3),'FAMILY WING',3,True,'center')
text(*xy(4.1,3.8),'+3.20 m envelope top',2.8,align='center')
text(*xy(19.5,3),'GUEST WING',3,True,'center')
text(*xy(19.5,3.8),'+3.20 m envelope top',2.8,align='center')
text(*xy(12.2,5),'OPEN COURTYARD',3,True,'center')
text(*xy(12.2,5.8),'88.40 m2 at ground level',2.7,align='center')
tag(*xy(14.2,10.6),'ORANGERY')
text(*xy(14.2,11.4),'roof reserved',2.6,align='center')
tag(*xy(25,14),'GYM')
text(*xy(25,14.8),'+3.20 m',2.8,align='center')
tag(*xy(10,15.6),f'ONE RIDGE +{RIDGE:.2f}')
text(*xy(7,17.2),'VAULT OVER SHARED ROOM',2.8,True,'center')
text(*xy(18.7,17.2),'SERVICE CEILINGS BELOW',2.5,align='center')
for x in [6,12]:
    arrow(*xy(x,14.8),*xy(x,13.25));arrow(*xy(x,16.1),*xy(x,17.7))
for x,y,label in [(5.8,12.8,'J1'),(16.2,12.8,'J2'),(22.8,15.6,'J3')]:tag(*xy(x,y),label)
line(*xy(4.1,-.8),*xy(4.1,19.3),'accent',.45,True)
line(*xy(-.8,15.6),*xy(28,15.6),'accent',.45,True)
tag(*xy(4.1,-1.3),'A');tag(*xy(4.1,19.8),'A')
tag(*xy(-1.1,15.6),'B');tag(*xy(28.1,15.6),'B')
tag(*xy(4.1,3),'FAMILY WING')
tag(*xy(4.1,3.8),'+3.20 m envelope top')
tag(*xy(7,17.2),'VAULT OVER SHARED ROOM')
tag(*xy(10,15.6),f'ONE RIDGE +{RIDGE:.2f}')
text(100,49,'27.15 x 18.40 m wall envelope retained',2.8)
text(309,49,'THE DESIGN MOVE',3.2,True)
para(309,57,['The pitched roof runs across the','whole rear block, including the','lounge and enclosed service rooms.','The two projecting wings stop','beneath its courtyard-side eave.'])
text(309,90,'A HEIGHT TEST',3.2,True)
para(309,98,['Main roof edge: +3.70 m.','Main ridge: +5.32 m at 30 degrees.','Lower roof envelope tops: +3.20 m.','','The 0.50 m gross level difference','is before fascia, gutter and flashing','design. It is not a verified clearance.'])
text(309,139,'WHAT THE LINES MEAN',3.2,True)
para(309,147,['Dashed green: shared-room outline','below the roof; no new room walls.','Low roofs reserve a zone for falls,','insulation, drainage and edge detail.','No low-roof drainage falls or','outlet positions are fixed here.'])
text(309,183,'CONNECTIONS TO DEVELOP',3.2,True)
para(309,191,['J1  Low family roof / main eave.','J2  Guest and orangery connections.','J3  Gym roof / main gable wall.','','Orangery top shown at +3.20 m','for massing only. Glazing and','seasonal / year-round use stay open.'])
scale_bar(20,264)
text(84,266,'All levels are above floor +0.00. Overhangs and rooflights remain to be designed.',2.7,fill='muted')
c.showPage()


def elevation(base,arrival=False,compare=False):
    def ep(x,h): return page_x(x,arrival),base-h*10
    def area(points,fill):polygon([ep(*p) for p in points],fill)
    def opening(x,w,sill,head):
        area([(x,sill),(x+w,sill),(x+w,head),(x,head)],'glass')
        line(*ep(x+w/2,sill),*ep(x+w/2,head),'muted',.2)
    area([(0,0),(22.8,0),(22.8,EAVE),(0,EAVE)],'timber')
    area([(0,EAVE),(22.8,EAVE),(22.8,RIDGE),(0,RIDGE)],'roof1')
    area([(22.8,0),(27.15,0),(27.15,LOW_TOP),(22.8,LOW_TOP)],'stone')
    if arrival:
        area([(16.41,0),(22.8,0),(22.8,EAVE),(16.41,EAVE)],'stone')
        for axis,x,y,w in DATA['windows']:
            if axis=='h' and y==18.4:opening(x,w,.55,2.7)
        for x in [17.6,21.15]:opening(x,1,0,2.2)
        text(page_x(7,True),base+6,'Timber shared-room facade',2.8,align='center')
        text(page_x(18.1,True),base+6,'Entrance',2.8,align='center')
        text(page_x(21.65,True),base+6,'Boot',2.8,align='center')
    else:
        for x0,x1 in [(0,8.2),(16.2,22.8)]:
            area([(x0,0),(x1,0),(x1,LOW_TOP),(x0,LOW_TOP)],'stone')
            line(*ep(x0,LOW_TOP-.12),*ep(x1,LOW_TOP-.12),'muted',.2)
        opening(.8,2.4,.75,2.35);opening(19,2.6,.75,2.35)
        opening(9,2.6,0,2.7)
        area([(12.2,0),(16.2,0),(16.2,LOW_TOP),(12.2,LOW_TOP)],'timber')
        opening(13,2.8,0,2.35)
        for x,label in [(4.1,'Family wing'),(10.1,'Dining'),(14.2,'Orangery'),(19.5,'Guest wing')]:
            text(page_x(x),base+6,label,2.8,align='center')
    text(page_x(25,arrival),base+6,'Gym',2.8,align='center')
    line(15,base,296,base,'ink',.5)
    if compare:
        for x0,x1 in [(0,8.2),(16.2,22.8)]:
            mid=(x0+x1)/2
            for a,b in [((x0,2.8),(mid,2.8+(x1-x0)/2*K)),((mid,2.8+(x1-x0)/2*K),(x1,2.8))]:
                line(*ep(*a),*ep(*b),'old',.4,True)
        line(*ep(0,2.8+2.8*K),*ep(22.8,2.8+2.8*K),'old',.4,True)
        for a,b in [((22.8,2.8),(22.8,2.8+3.35*K)),((22.8,2.8+3.35*K),(27.15,2.8+3.35*K))]:
            line(*ep(*a),*ep(*b),'old',.4,True)
    return ep


header(2,'A taller centre, quieter wings','Elevations 1:100 at A3 | Window and door widths retained; shared glazing heads raised to +2.70 m as a proposal')
text(20,49,'FROM THE GARDEN / GYM ON THE LEFT',3.3,True)
ep=elevation(117,compare=True)
tag(*ep(11.4,RIDGE+.35),'NEW MAIN RIDGE +5.32')
line(20,130,32,130,'old',.4,True)
text(36,131,'Dashed brown: earlier pitched-wing roof lines, at the same scale and position.',2.7,fill='muted')
text(309,54,'WHAT CHANGES',3.2,True)
para(309,62,['Wing gables disappear, leaving','lower stone volumes in front of','one continuous timber roof.','','Family top: 5.17 to 3.20 m.','Guest top: 4.71 to 3.20 m.','Gym top: 4.73 to 3.20 m.','Main ridge: 4.42 to 5.32 m.','Overall highest: 5.17 to 5.32 m.'])
text(20,149,'FROM THE ARRIVAL SIDE / GYM ON THE RIGHT',3.3,True)
elevation(215,arrival=True)
text(309,155,'THE TRADEOFF',3.2,True)
para(309,163,['The rear pitched volume becomes','more prominent. Its taller eaves','reserve room to investigate the','lower-roof connections.','','This is a height study, not the','minimum workable roof height.','Roof-covering colours are placeholders.'])
line(14,233,406,233,'line')
para(20,243,['The family and guest wings retain their positions and warm stone character. Main arrival wall: timber, with stone at services.',
             'These orthographic views compress depth. The courtyard plan on sheet 1 shows which volumes sit forward.',
             'Roof-edge details, window proportions, shade and daylight need refinement once the overall heights feel right.',
             'The orangery is shown as a low enclosure only; its roof system has not been selected.'],2.9,5)
scale_bar(339,269)
c.showPage()


header(3,'One ceiling from sofa to kitchen','Located sections 1:100 at A3 | The pitched ceiling is continuous over the shared-room footprint')
text(20,49,'B-B / ALONG THE RIDGE, LOOKING TOWARD THE GARDEN',3.3,True)
base=120
xp=lambda x,z:(20+x*10,base-z*10)
polygon([xp(0,RIDGE),xp(22.8,RIDGE),xp(22.8,APEX),xp(0,APEX)],'roof2')
for x0,x1 in [(0,.35),(13.88,14),(16.35,16.47),(19.03,19.15),(22.45,22.8),(26.8,27.15)]:
    h=2.6 if x0 in (16.35,19.03) else (LOW_TOP if x0>22.45 else APEX)
    polygon([xp(x0,0),xp(x1,0),xp(x1,h),xp(x0,h)],'stone')
line(*xp(0,0),*xp(27.15,0),'ink',.8)
line(*xp(.35,APEX),*xp(13.88,APEX),'accent',.7)
line(*xp(14,2.6),*xp(22.45,2.6),'accent',.4)
polygon([xp(22.8,LOW_TOP),xp(27.15,LOW_TOP),xp(27.15,2.7),xp(22.8,2.7)],'roof2')
for x,w,h in [(4.6,1,.8),(7.15,2.4,.75),(10.95,2.8,.92)]:
    polygon([xp(x,0),xp(x+w,0),xp(x+w,h),xp(x,h)],'timber')
for x,label in [(6.8,'Lounge / dining / kitchen'),(15.175,'Pantry'),(17.75,'Hall'),(20.8,'Boot'),(25,'Gym')]:
    text(*xp(x,-.65),label,2.7,align='center')
tag(*xp(6.9,APEX-.6),f'CONTINUOUS CEILING APEX +{APEX:.2f}')
text(309,55,'THE INTERIOR RESULT',3.2,True)
para(309,63,['The lounge no longer inherits a','crossing bedroom-wing roof.','One ridge runs over the sofa,','dining table and kitchen.','','Pantry, hall and boot room have','flat ceilings under the same roof.','Furniture beyond the cut is shown','for context. No supports are designed.'])
line(14,141,406,141,'line')
text(20,151,'A-A / THROUGH THE FAMILY WING AND LOUNGE, LOOKING TOWARD THE GYM',3.1,True)
base=232
yp=lambda y,z:(20+y*10,base-z*10)
polygon([yp(0,LOW_TOP),yp(12.8,LOW_TOP),yp(12.8,2.6),yp(0,2.6)],'roof2')
polygon([yp(12.8,EAVE),yp(15.6,RIDGE),yp(18.4,EAVE),
         yp(18.4,ceiling(18.4)),yp(15.6,APEX),yp(12.8,ceiling(12.8))],'roof2')
for y0,y1,h,bottom in [(0,.35,2.6,0),(4.35,4.47,2.6,2.2),(13.03,13.15,ceiling(13.15),2.2)]:
    polygon([yp(y0,bottom),yp(y1,bottom),yp(y1,h),yp(y0,h)],'stone')
for z0,z1 in [(0,.55),(2.7,ceiling(18.05))]:
    polygon([yp(18.05,z0),yp(18.4,z0),yp(18.4,z1),yp(18.05,z1)],'stone')
line(*yp(18.225,.55),*yp(18.225,2.7),'accent',.25)
line(*yp(13.15,SPRING),*yp(15.6,APEX),'accent',.65)
line(*yp(15.6,APEX),*yp(18.05,SPRING),'accent',.65)
line(*yp(0,0),*yp(18.4,0),'ink',.8)
tag(*yp(15.6,RIDGE+.4),'ROOF +5.32')
text(*yp(6.3,-.6),'Family rooms / corridor: 2.60 m ceiling',2.7,align='center')
text(*yp(15.6,-.6),'Lounge vault',2.7,align='center')
text(228,166,'WORKING INTERNAL HEIGHTS',3.2,True)
para(228,175,['Shared ceiling: 3.50 m at the internal side walls, rising to 4.91 m.',
              'Wing / service ceilings: 2.60 m. Gym ceiling: 2.70 m for testing.',
              'Shaded roof bands are space reservations, not build-up details.',
              'The main roof edge is 0.50 m above the lower roof envelope;',
              'fascia, overhang and weatherproof connections still need fitting.'],2.9,5)
text(228,208,'WHAT TO JUDGE NEXT',3.2,True)
para(228,217,['Does the shared room feel too tall, or comfortably generous?',
              'If the form is right, refine roof depth and junctions to see whether',
              'the main eaves can come down while retaining the continuous vault.',
              'Confirm gym equipment height and the orangery use separately.'],2.9,5)
line(14,251,406,251,'line')
para(20,260,['Checked: unchanged floor geometry; full roof coverage; continuous shared vault; garden/arrival orientation; all three pages rendered.',
             'Unresolved: structure, roof build-ups, low-roof falls/outlets, rooflights, thermal design, stove/flue and site-specific daylight.'],2.8,5)
c.showPage();c.save()

checks=0
for i in range(272):
    for j in range(185):
        x,y=i*.1+.003,j*.1+.003
        assert bool(roof(x,y))==inside(x,y,DATA['OUTLINE']),(x,y)
        checks+=1
vault_checks=0
for i in range(178):
    for j in range(50):
        x,y=i*.1+.003,13.15+j*.1+.003
        if inside(x,y,DATA['open_poly']):
            assert within(x,y,MAIN)
            assert abs(roof(x,y)-(EAVE+min(y-12.8,18.4-y)*K))<1e-8
            assert ceiling(y)<roof(x,y)
            vault_checks+=1
assert page_x(25)<page_x(4.1)
assert page_x(25,True)>page_x(4.1,True)
assert abs(RIDGE-5.3165807537)<1e-8
assert abs(APEX-4.9145081595)<1e-8
(OUT/'concept-06b-study-check.json').write_text(json.dumps({
    'baseline':'concept 05, unchanged','coverage_sample_checks':checks,
    'shared_vault_sample_checks':vault_checks,
    'main_roof_eave_m':EAVE,'main_roof_ridge_m':round(RIDGE,4),
    'shared_ceiling_spring_m':SPRING,'shared_ceiling_apex_m':round(APEX,4),
    'lower_envelope_top_m':LOW_TOP,
    'elevation_orientation':'Garden: gym left; arrival: gym right',
    'status':'Exploratory heights and massing; no structural or roof junction validation'
},indent=2)+'\n')
print(PDF)
print(f'Coverage: {checks}; vault samples: {vault_checks}; ridge: {RIDGE:.4f}; ceiling apex: {APEX:.4f}')
