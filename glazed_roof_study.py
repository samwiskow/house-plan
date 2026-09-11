"""Glazed garden-room roof and interior transition over the concept 07 plan."""
import ast
import json
from math import atan, degrees, sqrt, tan, radians
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT=Path(__file__).parent
OUT=ROOT/'output/pdf'
PDF=OUT/'concept-07b-glazed-roof-transition.pdf'
K=tan(radians(30))
GLASS_LOW,GLASS_HIGH=2.85,3.45
HEAD=3.10

def glass(y):return GLASS_LOW+(y-9.3)*(GLASS_HIGH-GLASS_LOW)/3.5

def ceiling(y):return 3.50+min(y-13.15,18.05-y)*K

def main_roof(y):return 3.70+min(y-12.8,18.4-y)*K

pdfmetrics.registerFont(TTFont('Study','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('StudyBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
C={'ink':'#30392f','muted':'#6b6d5c','line':'#c9c5b7','paper':'#fffdf8',
   'stone':'#e3d2ad','timber':'#c49d68','roof1':'#d6c6ae','roof2':'#eee4d3',
   'glass':'#e2ece4','garden':'#e6edda','accent':'#376248','ivory':'#f3eddf',
   'oatmeal':'#c9b997','frame':'#827356'}
c=canvas.Canvas(str(PDF),pagesize=(420*mm,297*mm))
c.setTitle('Concept 07B - glazed roof and ceiling transition')
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


def arrow(x,y,xx,yy):
    line(x,y,xx,yy,'accent',.35)
    dx,dy=xx-x,yy-y; n=(dx*dx+dy*dy)**.5
    ux,uy=dx/n,dy/n
    line(xx,yy,xx-ux*2-uy,yy-uy*2+ux,'accent',.35)
    line(xx,yy,xx-ux*2+uy,yy-uy*2-ux,'accent',.35)


def header(page,title,subtitle):
    rect(0,0,420,297,'paper',None)
    text(14,12,'COURTYARD HOUSE / CONCEPT 07B / GLAZED ROOF + OPEN INTERIOR',2.7,fill='muted')
    text(14,23,title,6.2,True);text(14,31,subtitle,3,fill='muted')
    line(14,36,406,36,'line');line(14,280,406,280,'line')
    text(14,287,'PROPOSAL | Roof heights, framing and shading are study allowances. Structure, drainage and thermal performance require design.',2.4,fill='muted')
    text(406,287,f'{page} / 2',2.6,align='right',fill='muted')


header(1,'A simple frame, then glass and sky','Section A-A at 1:50 on A3 | Cut at plan x = 13.20 m, from courtyard through garden sitting into the shared room')
base=174
pt=lambda y,z:(23+(y-8.8)*20,base-z*20)
polygon([pt(9.3,glass(9.3)),pt(12.8,glass(12.8)),pt(12.8,glass(12.8)-.1),pt(9.3,glass(9.3)-.1)],'glass')
polygon([pt(12.8,main_roof(12.8)),pt(15.6,main_roof(15.6)),pt(18.4,main_roof(18.4)),
         pt(18.4,ceiling(18.4)),pt(15.6,ceiling(15.6)),pt(12.8,ceiling(12.8))],'roof2')
polygon([pt(12.8,HEAD),pt(13.15,HEAD),pt(13.15,3.5),pt(12.8,3.5)],'ivory')
polygon([pt(9.3,2.35),pt(9.65,2.35),pt(9.65,glass(9.65)-.1),pt(9.3,glass(9.3)-.1)],'stone')
line(*pt(9.475,0),*pt(9.475,2.35),'accent',.3)
polygon([pt(18.05,0),pt(18.4,0),pt(18.4,ceiling(18.4)),pt(18.05,ceiling(18.05))],'stone')
line(*pt(8.8,0),*pt(18.4,0),'ink',.8)
polygon([pt(10.35,0),pt(11.95,0),pt(11.95,.82),pt(10.35,.82)],'oatmeal')
polygon([pt(14.5,0),pt(15.5,0),pt(15.5,.92),pt(14.5,.92)],'timber')
polygon([pt(17.25,0),pt(18.05,0),pt(18.05,2),pt(17.25,2)],'ivory')
tag(*pt(9.85,3.1),'GLASS LOW +2.85')
tag(*pt(12.3,3.9),'GLASS HIGH +3.45')
tag(*pt(15.6,5.75),'MAIN ROOF +5.32')
text(*pt(11, -.65),'Garden sitting',2.8,align='center')
text(*pt(15.5,-.65),'Main shared room',2.8,align='center')
line(*pt(13.3,HEAD),*pt(14.3,2.7),'accent',.35)
text(*pt(14.45,2.65),'3.10 m clear head',2.8,fill='accent')
text(245,49,'WHAT IS NOW AGREED',3.2,True)
para(245,58,['A predominantly glazed, shallow single-slope roof.',
             'A broad opening with a plain warm-ivory head.',
             'Continuous flooring and an open connection to the hall.',
             'Solar-control insulating glass, retractable external shading',
             'provision, high-level vents and a whole-space comfort assessment.'],2.9,5.2)
text(245,91,'HEIGHTS BEING TESTED',3.2,True)
para(245,100,['Roof surface: +2.85 m at court, +3.45 m at the house.',
              'The 0.60 m rise over 3.50 m gives a slope of about 9.7 degrees.',
              'Opening head: +3.10 m; main ceiling beside it: +3.50 m.',
              'That leaves a visible 0.40 m ivory band on the shared-room side.',
              'The earlier +3.20 m garden-roof box was a placeholder;',
              'this sloping profile replaces it in the new study only.'],2.9,5.2)
text(245,139,'WHAT THE DRAWING DOES NOT SETTLE',3.2,True)
para(245,148,['The opening head is a spatial target, not a sized beam.',
              'The glass/frame system must establish its actual pitch and depth.',
              'The high roof edge, main eave and shading cassette meet closely.',
              'The hall-side roof edge also needs a coordinated connection.',
              'A post-free corner remains an ambition, not a structural result.'],2.9,5.2)
line(14,195,406,195,'line')
text(20,205,'THE COMFORT BRIEF',3.2,True)
para(20,214,['Glass: low-emissivity insulation and solar control, with neutral-looking samples.',
             'Shading: allow for retractable external roof shading; coordinate guides and cassette.',
             'Ventilation: investigate motorised high-level vents with rain control and safe air inlets.',
             'Heating/cooling: calculate winter heat loss and summer overheating for the connected space.',
             'Performance is unverified until glazing, orientation, climate and systems are assessed.'],2.9,5.5)
text(266,205,'SECTION + CAMERA KEY / DIAGRAMMATIC',2.8,True)
rect(269,224,46,20,'ivory');rect(278,213,25,11,'glass')
line(287,211,287,245,'accent',.3,True)
tag(287,210,'A');tag(287,250,'A')
arrow(286,238,291,217)
text(321,213,'Arrow: interior camera',2.7)
text(321,219,'toward courtyard.',2.7)
text(321,229,'No compass orientation',2.7)
text(321,235,'assigned to the site.',2.7)
text(20,251,'References informing the comfort brief (not selected suppliers or products):',2.6,fill='muted')
text(20,258,'Pilkington: insulating and solar-control glazing',2.7,fill='accent')
c.linkURL('https://www.pilkington.com/en/xx/products/product-categories/solar-control/pilkington-insulight-sun/',(20*mm,37*mm,170*mm,43*mm),relative=0)
text(20,265,'CIBSE: shading, ventilation and overheating assessment',2.7,fill='accent')
c.linkURL('https://www.cibse.org/policy-advocacy/key-policy-areas/health-and-wellbeing/overheating-position-statement/',(20*mm,30*mm,200*mm,36*mm),relative=0)
c.showPage()


def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(v):return tuple(x/sqrt(dot(v,v)) for x in v)
CAM=(13.2,16.4,1.6)
forward=unit(sub((14.35,10.7,1.95),CAM))
right=unit(cross((0,0,1),forward))
up=cross(forward,right)


def view(p):
    q=sub(p,CAM)
    return dot(q,right),dot(q,up),dot(q,forward)


def project(p):
    a,b,d=view(p)
    assert d>.05
    return 203+160*a/d,145-160*b/d


faces=[]
def face(points,fill,stroke=None):
    faces.append((points,fill,stroke))


def quad_x(x,y0,y1,z0,z1,fill):face([(x,y0,z0),(x,y1,z0),(x,y1,z1),(x,y0,z1)],fill,'frame')
def quad_y(y,x0,x1,z0,z1,fill):face([(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],fill,'frame')
def cube(x,y,z,w,d,h,fill):
    quad_y(y,x,x+w,z,z+h,fill);quad_y(y+d,x,x+w,z,z+h,fill)
    quad_x(x,y,y+d,z,z+h,fill);quad_x(x+w,y,y+d,z,z+h,fill)
    face([(x,y,z+h),(x+w,y,z+h),(x+w,y+d,z+h),(x,y+d,z+h)],fill,'frame')


header(2,'Looking from the kitchen towards the garden','Geometry-based interior perspective | Eye height 1.60 m | Diagrammatic finishes; roof frames and junctions are not specifications')
c.saveState()
p=c.beginPath();p.rect(15*mm,(297-231)*mm,390*mm,188*mm);c.clipPath(p,stroke=0)
rect(15,43,390,188,'#f0f2e8',None)
face([(8.2,0,0),(16.2,0,0),(16.2,9.3,0),(12.2,9.3,0),(12.2,12.8,0),(8.2,12.8,0)],'garden')
quad_x(8.2,0,12.8,0,3.2,'stone')
for y0 in [4.8,9.2]:quad_x(8.201,y0,y0+2,.75,2.35,'glass')
for x0,x1,y0,y1 in [(10.5,17.75,13.15,18.05),(12.55,16.55,9.65,13.15),(16.55,17.75,9.46,13.15)]:
    for i in range(10):
        a=y0+(y1-y0)*i/10;b=y0+(y1-y0)*(i+1)/10
        face([(x0,a,0),(x1,a,0),(x1,b,0),(x0,b,0)],'roof2')
for x0,x1 in [(12.55,13),(15.8,16.55)]:quad_y(9.65,x0,x1,0,2.75,'ivory')
quad_y(9.65,13,15.8,2.35,2.75,'ivory')
quad_y(9.65,13,15.8,0,2.35,None)
quad_y(9.65,14.38,14.42,0,2.35,'frame')
for y0,y1 in [(9.65,10.4),(11.9,13.15)]:quad_x(12.55,y0,y1,0,2.75,'ivory')
quad_x(12.55,10.4,11.9,0,.65,'ivory');quad_x(12.55,10.4,11.9,2.35,2.75,'ivory')
quad_x(12.55,10.4,11.9,.65,2.35,None)
for y0,y1 in [(9.46,10.35),(11.25,12.4)]:quad_x(17.75,y0,y1,0,2.6,'ivory')
quad_y(9.46,16.55,17.75,0,2.6,'ivory')
quad_y(9.465,16.7,17.6,0,2.2,'timber')
quad_y(13.15,11.6,12.55,0,3.5,'ivory')
quad_y(13.15,10.5,11.6,2.7,3.5,'ivory')
quad_y(13.15,10.5,11.6,0,2.7,None)
quad_y(13.15,16.55,17.75,2.6,3.5,'ivory')
face([(16.55,9.46,2.6),(17.75,9.46,2.6),(17.75,13.15,2.6),(16.55,13.15,2.6)],'ivory')
quad_y(13.15,12.55,16.55,HEAD,3.5,'ivory')
face([(12.55,12.8,HEAD),(16.55,12.8,HEAD),(16.55,13.15,HEAD),(12.55,13.15,HEAD)],'ivory','frame')
quad_x(16.55,9.65,12.8,2.6,3.2,'ivory')
for i in range(12):
    y0=13.15+i*(15.6-13.15)/12;y1=13.15+(i+1)*(15.6-13.15)/12
    face([(10.5,y0,ceiling(y0)),(18,y0,ceiling(y0)),(18,y1,ceiling(y1)),(10.5,y1,ceiling(y1))],'ivory')
# Framing is indicative and deliberately independent of a manufacturer's system.
for x in [12.55,13.75,14.95,16.2]:
    face([(x-.025,9.65,glass(9.65)-.08),(x+.025,9.65,glass(9.65)-.08),
          (x+.025,12.8,glass(12.8)-.08),(x-.025,12.8,glass(12.8)-.08)],'frame')
for y in [9.65,11.2,12.8]:
    face([(12.55,y-.025,glass(y)-.08),(16.2,y-.025,glass(y)-.08),
          (16.2,y+.025,glass(y)-.08),(12.55,y+.025,glass(y)-.08)],'frame')
cube(12.7,10.35,0,.75,1.6,.42,'oatmeal');cube(12.7,10.35,.42,.2,1.6,.4,'oatmeal')
cube(14.1,10.9,0,.65,.65,.4,'timber');cube(15.1,10.05,0,.8,.8,.42,'oatmeal')
cube(15.1,10.05,.42,.8,.18,.4,'oatmeal')

def near_clip(points):
    result=[]
    for a,b in zip(points,points[1:]+points[:1]):
        da,db=view(a)[2]-.3,view(b)[2]-.3
        if da>=0:result.append(a)
        if (da>=0)!=(db>=0):
            t=da/(da-db);result.append(tuple(x+t*(y-x) for x,y in zip(a,b)))
    return result


for points,fill,stroke in sorted(faces,key=lambda f:sum(view(p)[2] for p in f[0])/len(f[0]),reverse=True):
    clipped=near_clip(points)
    if len(clipped)>=3:polygon([project(p) for p in clipped],fill,stroke,.2)
c.restoreState()
line(14,238,406,238,'line')
text(20,248,'THE INTENDED EXPERIENCE',3.2,True)
para(20,257,['A plain ivory head frames the glass roof; the same floor continues into the sitting area.',
             'The right-hand opening leads to the shared hall, with the relocated guest/office door beyond.'],2.9,5.5)
text(225,248,'HOW TO READ THIS VIEW',3.2,True)
para(225,257,['Furniture outside the garden room is omitted to expose the connection.',
              'The clear corner is design intent. No post-free structure is established.'],2.9,5.5)
c.showPage();c.save()
assert project((15,10.7,1.95))[0]>project((14,10.7,1.95))[0]
assert project((17.15,11.5,1.6))[0]>project((14.5,11.5,1.6))[0]
assert HEAD<glass(12.8)-.1<3.5
assert abs(ceiling(13.15)-HEAD-.4)<1e-9
assert GLASS_LOW<GLASS_HIGH<3.7
assert 12.55<CAM[0]<13.88 and 15.33<CAM[1]<18.05
(OUT/'concept-07b-study-check.json').write_text(json.dumps({
 'plan_reference':'concept 07','main_roof_reference':'concept 06B',
 'garden_glass_low_m':GLASS_LOW,'garden_glass_high_m':GLASS_HIGH,
 'garden_roof_slope_degrees':round(degrees(atan(.6/3.5)),3),
 'opening_head_target_m':HEAD,'visible_head_band_m':.4,
 'camera_m':CAM,'structural_validation':False,'thermal_validation':False,
 'status':'Design intent with provisional section dimensions'
},indent=2)+'\n')
print(PDF)
