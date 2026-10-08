from pathlib import Path
import hashlib, json, math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'output/pdf/l-house-design-booklet.pdf'
DATA=json.loads((HERE/'plans.json').read_text())
D=DATA['default']; ENC=DATA['enclosed']
for name,file in [('Text','Arial.ttf'),('Bold','Arial Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
pdfmetrics.registerFontFamily('Text',normal='Text',bold='Bold',italic='Text',boldItalic='Bold')
INK=HexColor('#26382c'); MUTED=HexColor('#53614e'); PAPER=HexColor('#fffdf7')
WALL=HexColor('#d8c9af'); FURN=HexColor('#e8dfce'); GREEN=HexColor('#e4edda')
LAWN=HexColor('#ecf1df'); TREE=HexColor('#b8caa0'); PAVE=HexColor('#efe3ce')
BLUE=HexColor('#276c80'); ORANGE=HexColor('#a85e30'); GRID=HexColor('#b4aa96')
W,H=420,297
C=canvas.Canvas(str(OUT),pagesize=(W*mm,H*mm),pageCompression=1)
C.setTitle('L-house - Plot and floor-plan review, Edition L01.1')
C.setAuthor('House design study')
PAGE=0; audit={'pages':[],'plan_source':DATA['provenance']}

def txt(x,y,s,size=10,color=INK,bold=False,align='left'):
    C.setFillColor(color);C.setFont('Bold' if bold else 'Text',size)
    f={'left':C.drawString,'right':C.drawRightString,'center':C.drawCentredString}[align]
    f(x*mm,(H-y)*mm,str(s))

def para(x,y,w,s,size=10.5,color=INK):
    sty=ParagraphStyle('p',fontName='Text',fontSize=size,leading=size*1.42,textColor=color)
    p=Paragraph(s,sty);_,h=p.wrap(w*mm,1000)
    p.drawOn(C,x*mm,(H-y)*mm-h)
    return y+h/mm

def line(x1,y1,x2,y2,color=GRID,width=.6,dash=None):
    C.setStrokeColor(color);C.setLineWidth(width);C.setDash(dash or [])
    C.line(x1*mm,(H-y1)*mm,x2*mm,(H-y2)*mm);C.setDash([])

def rect(x,y,w,h,fill=None,stroke=GRID,width=.5):
    C.setFillColor(fill or white);C.setStrokeColor(stroke or white);C.setLineWidth(width)
    C.rect(x*mm,(H-y-h)*mm,w*mm,h*mm,fill=bool(fill),stroke=bool(stroke))

def poly(points,fill=None,stroke=GRID,width=.5):
    p=C.beginPath();p.moveTo(points[0][0]*mm,(H-points[0][1])*mm)
    for x,y in points[1:]:p.lineTo(x*mm,(H-y)*mm)
    p.close();C.setFillColor(fill or white);C.setStrokeColor(stroke or white);C.setLineWidth(width)
    C.drawPath(p,fill=bool(fill),stroke=bool(stroke))

def page(title,sub):
    global PAGE
    if PAGE:C.showPage()
    PAGE+=1
    rect(0,0,W,H,PAPER,None)
    txt(18,15,'L-HOUSE  /  DESIGN REVIEW',9,MUTED,True)
    txt(402,15,'L01.1  |  08 OCT 2026',9,MUTED,align='right')
    txt(18,29,title,23,INK,True);txt(18,39,sub,10,MUTED)
    line(18,45,402,45)
    line(18,280,402,280)
    txt(18,287,'Proposed design dimensions. Not a surveyed site or construction drawing.',8,MUTED)
    txt(402,287,f'{PAGE:02d}  /  09',9,MUTED,align='right')
    audit['pages'].append(title)

def note(x,y,w,title,body):
    txt(x,y,title,12,INK,True)
    return para(x,y+4,w,body)+9

class Plan:
    def __init__(self,x,y,bounds,denom):
        self.x,self.y,self.b,self.k=x,y,bounds,1000/denom
    def pt(self,x,y):return self.x+(x-self.b[0])*self.k,self.y+(y-self.b[1])*self.k
    def poly(self,p,fill=None,stroke=GRID,width=.5):poly([self.pt(*q) for q in p],fill,stroke,width)
    def rect(self,r,fill=None,stroke=GRID,width=.5):
        x,y,w,h=r;self.poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],fill,stroke,width)
    def line(self,x1,y1,x2,y2,color=INK,width=.5,dash=None):line(*self.pt(x1,y1),*self.pt(x2,y2),color,width,dash)
    def label(self,x,y,s,size=8.5,color=INK,align='center',bg=False):
        X,Y=self.pt(x,y)
        if bg:
            wid=pdfmetrics.stringWidth(str(s),'Text',size)/mm+2
            rect(X-wid/2,Y-size/mm*.8,wid,size/mm*1.2,PAPER,None)
        txt(X,Y,s,size,color,align=align)
    def dim(self,x1,y1,x2,y2,s):
        self.line(x1,y1,x2,y2,GRID,.45)
        a,b=self.pt(x1,y1);c,d=self.pt(x2,y2)
        if abs(y2-y1)<.01:
            line(a,b-1.2,a,b+1.2);line(c,d-1.2,c,d+1.2)
            self.label((x1+x2)/2,y1-.16,s,8,bg=True)
        else:
            line(a-1.2,b,a+1.2,b);line(c-1.2,d,c+1.2,d)
            C.saveState();C.translate((a-1.7)*mm,(H-(b+d)/2)*mm);C.rotate(90)
            C.setFont('Text',8);C.setFillColor(INK);C.drawCentredString(0,0,s);C.restoreState()
    def route(self,pts,color=BLUE,dash=None):
        clip_start(self)
        for a,b in zip(pts,pts[1:]):self.line(*a,*b,color,1.15,dash)
        for i in range(1,len(pts),max(1,len(pts)//4)):
            a,b=pts[i-1],pts[i];ang=math.atan2(b[1]-a[1],b[0]-a[0]);k=.22
            q=[b,(b[0]-k*math.cos(ang-.45),b[1]-k*math.sin(ang-.45)),(b[0]-k*math.cos(ang+.45),b[1]-k*math.sin(ang+.45))]
            self.poly(q,color,None)
        C.restoreState()
    def bar(self,x,y,n=5):
        self.dim(x,y,x+n,y,f'{n} m')


def area(p):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2)
def box(x,y,w,h):return [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
def clip_start(P):
    C.saveState();q=C.beginPath();q.rect(P.x*mm,(H-P.y-(P.b[3]-P.b[1])*P.k)*mm,(P.b[2]-P.b[0])*P.k*mm,(P.b[3]-P.b[1])*P.k*mm);C.clipPath(q,stroke=0,fill=0)
def gap(P,x,y,axis,w):P.rect([x,y-.19,w,.38] if axis=='h' else [x-.19,y,.38,w],PAPER,None)
def draw_door(P,d):
    x,y,w=d['x'],d['y'],d['w'];gap(P,x,y,d['axis'],w)
    color=BLUE if d['style'] in ['proposed','pocket'] else INK
    if d['style']=='pocket':
        P.rect([x-d['pocketLength'],y-.075,d['pocketLength'],.15],None,BLUE,.55)
        P.line(x-.95,y,x-.05,y,BLUE,.8);return
    h=d['axis']=='h';sgn=d['side']
    ex=x if h else x+sgn*w;ey=y+sgn*w if h else y
    P.line(x,y,ex,ey,color,.65)
    pts=[(x+w*math.cos(t),y+sgn*w*math.sin(t)) if h else (x+sgn*w*math.sin(t),y+w*math.cos(t)) for t in [i*math.pi/48 for i in range(25)]]
    for a,b in zip(pts,pts[1:]):P.line(*a,*b,color,.4)

def item(P,it):
    x,y,w,h=it['r'];kind=it['kind'];name=it['name']
    fill=GREEN if kind=='wet' else WALL if 'divider' in name.lower() or 'privacy return' in name.lower() else FURN
    P.rect(it['r'],fill,GRID,.4)
    if kind=='bed':P.rect([x+.08,y+.1,w-.16,.35] if h>w else [x+.1,y+.08,.35,h-.16],None,GRID,.4)
    if kind=='bath':P.rect([x+.08,y+.12,w-.16,h-.24],PAPER,GRID,.4)
    if kind=='basin':
        for q in ([.08,.55] if 'double' in name.lower() or 'two basins' in name.lower() else [.15]):
            P.rect([x+w*q,y+h*.15,w*.36,h*.65] if w>h else [x+w*.15,y+h*q,w*.65,h*.36],PAPER,GRID,.4)
    if kind=='wc':
        X,Y=P.pt(x+w*.5,y+h*.5);C.setStrokeColor(GRID);C.setLineWidth(.4)
        C.ellipse((X-w*P.k*.32)*mm,(H-Y-h*P.k*.32)*mm,(X+w*P.k*.32)*mm,(H-Y+h*P.k*.32)*mm,fill=0)
    if kind=='car':
        P.rect([x+.7,y+.12,.75,h-.24],PAPER,GRID,.4);P.rect([x+w-1.25,y+.12,.6,h-.24],PAPER,GRID,.4)

def stairs(P,x,y):
    for i in range(8):P.line(x,y+i*.27,x+1,y+i*.27,GRID);P.line(x+1.4,y+i*.27,x+2.4,y+i*.27,GRID)
    P.line(x,y+2.89,x+2.4,y+2.89,GRID)
    P.route([(x+.5,y+.2),(x+.5,y+1.7)])
    if P.b[0]<x+1.2<P.b[2] and P.b[1]<y+2.5<P.b[3]:P.label(x+1.2,y+2.5,'UP',6.5)

def draw_plan(P,data,floors,labels=True,guest=False):
    clip_start(P)
    if 'g' in floors or 'u' in floors:P.poly(data['house'],WALL,INK,.7)
    if 'a' in floors:P.poly(data['garage'],WALL,INK,.7);P.poly(data['plant'],WALL,INK,.7)
    if 'o' in floors:P.poly(data['office'],WALL,INK,.7)
    if 'g' in floors:P.rect([16.2,11.35,2.5,2.4],WALL,INK,.7)
    for r in data['rooms']:
        if r['floor'] in floors:P.poly(r['p'],PAPER,GRID,.45)
    for f in data['furniture']:
        if f['floor'] in floors:item(P,f)
    if 'o' in floors:
        item(P,dict(name='Sofa bed',r=[19.4,18.1,2.2 if guest else .9,1.9],kind='bed' if guest else 'sofa'))
        item(P,dict(name='Chair',r=[23.5,16.9,.65,.65] if guest else [23.7,15.25,.65,.65],kind='chair'))
    for op in data['openings']:
        if op[0] in floors:gap(P,*op[1:])
    if 'g' in floors:
        P.rect([6.55,5.4,.3,1.3],None,BLUE,.5)
        for x in [6.62,6.72]:P.line(x,5.45,x,6.65,BLUE,.65)
        P.line(10.75,13,12.55,13,ORANGE,.75,[2,2]);P.line(13.4,11.95,13.4,14.45,ORANGE,.75,[2,2])
    for d in data['doors']:
        if d['floor'] in floors:draw_door(P,d)
    if 'u' in floors:
        for win in DATA['suiteDaylight']['windows']:
            x,y,w=win['x'],win['y'],win['w'];h=win['axis']=='h'
            gap(P,x,y,win['axis'],w)
            for off in [-.10,.10]:
                P.line(x if h else x+off,y+off if h else y,x+w if h else x+off,y+off if h else y+w,BLUE,.7)
        for rooflight in DATA['suiteDaylight']['rooflights']:
            x,y,w,h=rooflight['r']
            for a,b in zip(box(x,y,w,h),box(x,y,w,h)[1:]+box(x,y,w,h)[:1]):P.line(*a,*b,BLUE,.6,[2,2])
    if 'g' in floors or 'u' in floors:stairs(P,8.2,11.15)
    if 'a' in floors or 'o' in floors:stairs(P,19.05,13.35)
    if 'g' in floors:
        gap(P,1.8,.175,'h',2.2)
        for y in [.14,.21]:P.line(1.8,y,4,y,BLUE,.8)
        draw_door(P,dict(x=6.725,y=3.95,axis='v',w=.95,side=1,style='proposed'))
    if labels:
        for r in data['rooms']:
            if r['floor'] in floors and P.b[0]<r['label'][0]<P.b[2] and P.b[1]<r['label'][1]<P.b[3]:P.label(*r['label'],r['id'],8,bg=True)
    C.restoreState()

def schedule(data,floor,x,y,w=176):
    txt(x,y-5,'Room',8,MUTED);txt(x+w-21,y-5,'Clear size (m)',8,MUTED,align='right');txt(x+w,y-5,'m²',8,MUTED,align='right')
    for r in data['rooms']:
        if r['floor']!=floor:continue
        txt(x,y,r['id'],8.5,MUTED)
        txt(x+12,y,r['name'],9)
        xs=[q[0] for q in r['p']];ys=[q[1] for q in r['p']]
        dims=f'{max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f}' if len(r['p'])==4 else 'L-shaped'
        txt(x+w-21,y,dims,8.5,MUTED,align='right')
        txt(x+w,y,f'{area(r["p"]):.1f}',9,align='right')
        line(x,y+2,x+w,y+2,GRID,.25);y+=8
    txt(x+w,y+2,'Clear room areas in m²',8,MUTED,align='right')
    return y+10

# Site coordinates: garden is at the top; road is at the bottom.
SITE={'width':40,'depth':65,'house_origin':[6,28],'garden_depth':28,'gate':[12.25,18.25],
      'terrace':box(6,24,16.2,4), 'forecourt':[(8.5,44.8),(24.7,44.8),(24.7,58),(20,62),(18.25,65),(12.25,65),(10,62),(8.5,58)],
      'visitor_bays':[[2.8,47.7,5.7,2.8],[2.8,50.5,5.7,2.8]]}
def translated(p):return [(x+6,y+28) for x,y in p]
def poses():
    def straight(a,end):
        x,y,h=a[-1];dx,dy=end[0]-x,end[1]-y;n=max(1,math.ceil(math.hypot(dx,dy)/.1))
        a.extend([(x+dx*i/n,y+dy*i/n,h) for i in range(1,n+1)])
    def turn(a,delta,R):
        x,y,h=a[-1];k=(1 if delta>0 else -1)/R;n=math.ceil(abs(delta)*R/.1)
        a.extend([(x+(math.sin(h+delta*i/n)-math.sin(h))/k,y+(-math.cos(h+delta*i/n)+math.cos(h))/k,h+delta*i/n) for i in range(1,n+1)])
    alpha=math.acos(1-3.75/16)
    incoming=[(15.25,65,-math.pi/2)];turn(incoming,-alpha,8);turn(incoming,alpha,8)
    straight(incoming,(11.5,53.925));turn(incoming,math.pi/2,7);straight(incoming,(28.45,46.925))
    reverse=[(28.45,46.925,0)];straight(reverse,(12,46.925))
    outgoing=[reverse[-1]];turn(outgoing,math.pi/2,7)
    straight(outgoing,(19,65-16*math.sin(alpha)));turn(outgoing,alpha,8);turn(outgoing,-alpha,8)
    return incoming,reverse,outgoing
IN,REV,EXIT=poses()
def car_polygon(p):
    x,y,h=p;return [(x+a*math.cos(h)-b*math.sin(h),y+a*math.sin(h)+b*math.cos(h)) for a,b in [(-2.55,-1.075),(2.55,-1.075),(2.55,1.075),(-2.55,1.075)]]
def sat(a,b):
    for p in [a,b]:
        for v,w in zip(p,p[1:]+p[:1]):
            axis=(v[1]-w[1],w[0]-v[0]);A=[x*axis[0]+y*axis[1] for x,y in a];B=[x*axis[0]+y*axis[1] for x,y in b]
            if max(A)<=min(B)+1e-8 or max(B)<=min(A)+1e-8:return False
    return True
buildings=[translated(box(0,0,6.9,14.8)),translated(box(6.9,5,9.3,9.8)),translated(D['plant']),translated(box(16.2,11.35,2.5,2.4))]
# Garage solid wall strips, with a gap at the inner long-side vehicle opening.
buildings += [translated(box(18.7,7.3,.35,9.95)),translated(box(18.7,20.55,.35,.65)),translated(box(25.55,7.3,.35,13.9)),translated(box(18.7,20.85,7.2,.35)),translated(box(18.7,7.3,7.2,.35)),translated(box(19.05,7.65,6.5,9.35))]
visitors=[box(3.1,48.025,5.1,2.15),box(3.1,50.825,5.1,2.15)]
failures=[]
for phase,route in [('arrival',IN),('reverse',REV),('departure',EXIT)]:
    for i,pose in enumerate(route):
        body=car_polygon(pose)
        if any(sat(body,b) for b in buildings+visitors):failures.append([phase,i,'building or parked car'])
        if any(x<0 or x>40 or y<0 for x,y in body):failures.append([phase,i,'plot boundary'])
        for a,b in zip(body,body[1:]+body[:1]):
            if (a[1]-65)*(b[1]-65)<0:
                xx=a[0]+(b[0]-a[0])*(65-a[1])/(b[1]-a[1])
                if not 12.25<=xx<=18.25:failures.append([phase,i,'gate'])
assert not failures,failures[:10]
assert abs(EXIT[-1][0]-15.25)<1e-7 and abs(EXIT[-1][1]-65)<1e-7
assert abs(EXIT[-1][2]-math.pi/2)<1e-7
SITE['vehicle_check']={'assumed_body':[5.1,2.15],'path_radii':[7,8],'step_m':.1,'poses':sum(map(len,[IN,REV,EXIT])),'failures':failures,'scope':'Illustrative tangent-body sweep; not Audi steering geometry or a highway access assessment. Arrival forward, reverse out of garage, then leave road access forward.'}
(HERE/'site.json').write_text(json.dumps(SITE,indent=2))

def site_base(P,detail=False):
    P.rect([0,0,40,65],LAWN,INK,.8)
    P.rect([0,65,40,2],PAVE,GRID,.5)
    P.rect([1,1,38,2],GREEN,None);P.rect([1,3,2,38],GREEN,None);P.rect([37,3,2,38],GREEN,None)
    P.rect([6,24,16.2,4],PAVE,GRID,.4)
    P.rect([12.9,28,9.3,5],PAVE,GRID,.4)
    P.poly(SITE['forecourt'],PAVE,GRID,.45)
    for b in SITE['visitor_bays']:P.rect(b,PAVE,GRID,.5)
    for b in visitors:P.poly(b,FURN,GRID,.5)
    P.rect([2.8,43,21.9,1.5],GREEN,GRID,.35)
    P.rect([2.8,43,1.5,4.7],GREEN,GRID,.35)
    P.rect([22.3,41.6,2.4,1.4],GREEN,GRID,.35)
    P.rect([32.5,30.5,1.5,15.5],GREEN,GRID,.35)
    for key in ['house','garage','plant']:P.poly(translated(D[key]),WALL,INK,.7)
    P.rect([22.2,39.35,2.5,2.4],WALL,INK,.7)
    for b in [(6.35,28.35,6.2,14.1),(13.05,33.35,8.8,9.1)]:P.rect(b,PAPER,None)
    P.line(24.875,45.25,24.875,48.55,PAPER,3)
    P.line(7.8,28.175,10,28.175,BLUE,1.3)
    P.line(12.725,31.95,12.725,32.9,BLUE,1.3)
    P.line(17.3,42.625,18.25,42.625,BLUE,1.1)
    P.line(23.2,41.6,24.1,41.6,BLUE,1.1)
    for x,y,r in [(5,5,1.9),(18,5,1.8),(33,6,2.3),(4.5,19,1.5),(35,19,2.1),(36,35,1.6)]:
        X,Y=P.pt(x,y);C.setFillColor(TREE);C.setStrokeColor(MUTED);C.setLineWidth(.3)
        C.circle(X*mm,(H-Y)*mm,r*P.k*mm,fill=1,stroke=1)
    if not detail:
        P.label(20,13,'OPEN REAR GARDEN',11)
        P.label(20,16,'28 m deep behind the house',9)
        P.label(20,19,'Boundary planting keeps a broad centre lawn',8)
        P.label(14,26.2,'Main terrace',8)
        P.label(17.5,30.8,'Sheltered terrace',8)
        P.label(9.5,37,'HOUSE',8.5)
        P.label(28.5,39,'GARAGE + OFFICE',8)
        P.label(29.9,34.1,'Plant',7)
        P.label(16.5,56,'ARRIVAL COURT',8.5)
        P.label(20,66,'ROAD / NORTH SIDE ASSUMED',9)
    P.line(0,65,12.25,65,INK,1);P.line(18.25,65,40,65,INK,1)
    if not detail:
        P.line(36,55,36,61,INK,1);P.poly([(36,61),(35.5,60),(36.5,60)],INK,None);P.label(36,63,'N',10)

page('A generous plot, with a clear arrival','Site proposal  |  1:300 on A3 at 100%  |  South-facing rear garden assumed')
P=Plan(23,52,[-1,0,41,67],300);site_base(P)
P.dim(0,-.7,40,-.7,'40.00 m plot width');P.dim(-1,0,-1,65,'65.00 m plot depth')
P.dim(41,0,41,28,'28.00 m rear garden');P.bar(0,67,10)
y=note(193,59,203,'A working plot, not a real-site claim','A 40 x 65 m plot provides 2,600 m² of land. The house starts 28 m from the rear boundary. The garage stays beside the house and forward of it, with the enclosed ground-floor link retained.')
y=note(193,y,203,'Room for the garden','The full-width rear strip is 1,120 m² before terrace and planting. A 4 m-deep main terrace and the sheltered recess beside dining connect to the garden. The centre remains open for lawn, play and distant views. Trees are planting zones, not selected species.')
y=note(193,y,203,'Arrival that has a purpose','One 6 m-wide road entrance opens into a broad turning court. Two visitor bays sit to the left. A 1.5 m walking path leads to the front door; the link door serves everyday arrivals and shopping. The vehicle door faces the house.')
y=note(193,y,203,'Orientation and site checks','The road is assumed to be north of the house, with the rear garden to the south. Sun, slope, drainage, boundary conditions and road sightlines need a real site. No neighbouring buildings or protected trees are assumed.')

page('Drive in, park, and leave facing forward','Arrival study  |  1:150 on A3 at 100%  |  Illustrative car envelope: 5.10 x 2.15 m')
P=Plan(20,62,[0,39,40,69],150);clip_start(P);site_base(P,True)
for route,col in [(IN,BLUE),(EXIT,ORANGE)]:
    for pose in route[::max(1,len(route)//10)]:P.poly(car_polygon(pose),None,col,.25)
    P.route([(x,y) for x,y,h in route],col)
P.route([(x,y) for x,y,h in REV],MUTED,[3,2])
P.label(11.5,43.9,'Separate walking path',8,bg=True)
P.label(5.5,46.7,'Visitor bays',8,bg=True)
P.label(28.45,46.95,'A7 allowance',8,bg=True)
P.label(21,59,'Turning court',8,bg=True)
P.label(15.25,66.9,'6.00 m entrance',8,bg=True)
C.restoreState();P.bar(1,69,5)
y=note(307,60,91,'1  Arrive','Follow the blue line. The drive bends into the court, then gives a straight approach to the garage opening.')
y=note(307,y,91,'2  Leave the garage','Reverse along the dashed line into the court. Change to forward gear, then follow the orange line to the road.')
y=note(307,y,91,'3  Keep foot access clear','Visitor spaces are 5.70 x 2.80 m each. The walking path is north of the car sweep and connects to both arrival doors.')
y=note(307,y,91,'What was checked',f'{SITE["vehicle_check"]["poses"]} body positions, at no more than 0.10 m steps, clear modelled walls, parked visitor cars and the entrance edges. The paths use assumed 7 m and 8 m radii.')
para(307,y,91,'This is a layout check, not an Audi steering simulation. The final check must use the actual vehicle, gate, road and site survey.',9.5,MUTED)

page('Ground floor: daily life and two arrivals','Main house  |  1:100 on A3 at 100%  |  Default: short pantry divider and open passage')
P=Plan(22,66,[-.8,-.8,19.1,16.2],100);draw_plan(P,D,['g'])
P.dim(0,-.45,16.2,-.45,'16.20 m');P.dim(-.45,0,-.45,14.8,'14.80 m')
P.bar(0,16.0,5)
P.label(10.4,3,'Garden terrace',9,MUTED);P.label(17.45,15.1,'From drive',8,MUTED)
y=schedule(D,'g',237,60,158)
y=note(237,y+3,158,'Pantry default','The short partition separates the dry storage and utility zones, with a 1.05 m open passage. The concealed kitchen door and boot-room shopping route both remain. See page 06 for the enclosed option.')
para(22,251,192,'Blue marks show sliding or proposed doors. Orange dashed lines mark the footwear boundaries. Room codes match the schedule. Doors and furniture use the reviewed study geometry.',9,MUTED)
para(237,y,158,'Garden doors proposed for review: a 2.20 m sliding opening from living to the main terrace, and a 950 mm outward-opening door beside dining to the sheltered terrace. Other windows follow plan approval.',9.5)

page('First floor: family rooms and a private suite','Main house  |  1:100 on A3 at 100%  |  Approved separate suite gallery')
P=Plan(22,66,[-.8,-.8,17,16.2],100);draw_plan(P,D,['u']);P.dim(0,-.45,16.2,-.45,'16.20 m');P.dim(-.45,0,-.45,14.8,'14.80 m');P.bar(0,16,5)
y=schedule(D,'u',222,60,173)
y=note(222,y+2,173,'Separate suite access','Landing > private gallery > separate bedroom, dressing and bathroom doors. The gallery stops at the rectangular bedroom. Dressing is not a through-route.')
y=note(222,y,173,'Equal child-room provision','The three rooms are each about 18.5 m². Each keeps the same bed-frame, desk and wardrobe allowance. The family WC, wet room and dry basins can be used separately.')
para(22,251,180,'Both floors keep the same stair. Blue double lines mark suite windows; dashed boxes mark rooflight zones. The bedroom garden window is 2.00 m wide; the gallery window is 0.90 m wide.',9,MUTED)

page('Garage, gym and office remain usable together','Garage ground floor and office first floor  |  1:100 on A3 at 100%  |  No upper bridge to the house')
P=Plan(25,62,[18,3.5,26.8,22],100);draw_plan(P,D,['a']);P.dim(18.7,21.65,25.9,21.65,'7.20 m');P.dim(18.15,7.3,18.15,21.2,'13.90 m');P.label(22.3,22,'GROUND FLOOR',9)
Q=Plan(137,65,[18,10.8,26.8,21.8],100);draw_plan(Q,D,['o'],guest=True);Q.dim(18.7,21.05,25.9,21.05,'7.20 m');Q.label(22.3,21.65,'OFFICE / GUEST STATE',9)
y=schedule(D,'a',249,60,146);y=schedule(D,'o',249,y+8,146)
para(137,189,91,'The guest bed is shown open. Both desks stay in place, with a route to each side of the bed and the landing shower room.',9.5)
para(137,218,91,'Ground-floor gym: 26.0 m². The workshop is beside the stair. The parked car does not block the internal route to either.',9.5)
para(249,y+5,146,'The long-side option adds 400 mm at the garage front. The upper floor stays at its earlier extent; the roof over this strip remains to design. Actual car doors, tailgate and gym operating zones need product checks.',9.5)

page('Pantry choice: connected by default, enclosed if preferred','Default kitchen and utility 1:50  |  Enclosed pantry detail 1:50  |  Both options keep direct kitchen access')
txt(20,57,'DEFAULT  /  SHORT DIVIDER',12,INK,True)
P=Plan(20,68,[5.8,4.8,16.4,10.2],50);draw_plan(P,D,['g'],labels=False);P.label(9.6,9.05,'Kitchen',8);P.dim(12.625,6.4,12.625,7.45,'1.05 m')
P.route(D['paths']['kitchen'][0]);P.route(D['paths']['kitchen'][1]);P.label(11.75,6.4,'Pantry',8,bg=True);P.label(14.25,7.7,'Utility',8,bg=True)
txt(266,57,'OPTION  /  ENCLOSED PANTRY',12,INK,True)
Q=Plan(266,68,[10.35,4.8,16.4,10.2],50);draw_plan(Q,ENC,['g'],labels=False);Q.label(11.7,6.8,'Pantry',8,bg=True);Q.label(14.2,7.7,'Utility',8,bg=True)
P.bar(6,10.4,3);Q.bar(10.5,10.4,3)
y=note(20,203,208,'Default: two zones with an open connection','A full-height, 150 mm-thick divider projects 1.05 m from the rear wall. A 1.05 m passage connects pantry and utility. Dry storage stops clear of the partition. The shopping route runs directly from boot room to utility to pantry.')
para(20,y,208,'The kitchen door has a cabinet-style face and opens into the kitchen. The 2.40 m kitchen / dining opening can close with sliding panels. The drawing shows the panels retracted.',10)
y=note(266,203,132,'Enclosed option retained','This restores the full dividing wall and the earlier pantry shelving. The pantry opens directly from the kitchen; the utility keeps its kitchen and boot-room doors.')
para(266,y,132,'Trade-off: shopping reaches the pantry through the kitchen. There is no connecting pantry / utility door in this retained option.',10)

page('Parents suite: separate access and garden light','Suite 1:75  |  Bathroom detail 1:40  |  Same external suite boundary')
P=Plan(22,65,[-.2,-.3,7.2,10.9],75);draw_plan(P,D,['u'])
for route in D['paths']['suite']:P.route(route)
P.dim(4.1,4.46,4.1,5.89,'1.43 m');P.dim(5.45,9.5,6.55,9.5,'1.10 m');P.dim(.35,-.05,6.55,-.05,'6.20 m');P.bar(0,11,3)
Q=Plan(143,65,[0,6.2,5.5,10.05],40);draw_plan(Q,D,['u']);Q.dim(1.35,8.7,2.35,8.7,'1.00 m');Q.label(.775,7.95,'Tub',8,bg=True);Q.label(1.85,9.15,'3.00 x 1.50 m shower',8,bg=True)
y=note(304,61,92,'Bathroom features retained','Two basins, compact soaking tub, screened WC and a 3.00 x 1.50 m shower. Two fixed screens retain a 1.00 m central entry.')
y=note(304,y,92,'Three separate room doors','All openings are 900 mm. The bedroom has a wall pocket; dressing and bathroom doors open into their rooms. Hardware remains provisional.')
y=note(304,y,92,'Natural light','A 2.00 m bedroom garden window and 0.90 m gallery window. Four dashed rooflight zones serve dressing, bathroom and gallery. Roof openings and light wells need design.')
para(143,177,141,'Bathroom: 4.95 x 3.20 m. Tub allowance: 0.85 x 1.10 m. Vanity: 1.50 x 0.55 m. Filled weight, entry, waterproofing and drainage remain product and construction checks.',9.5)
para(143,211,141,'The window widths and rooflight zones carry the approved daylight direction. Window sill heights, roof slopes, trimmers and light wells remain provisional.',9.5)
para(22,248,262,'Dressing: 4.95 x 2.75 m with 660 mm-deep wardrobes on three sides. Clear aisle: 1.43 m; one 0.50 m open drawer leaves 0.93 m. Bedroom: 6.20 x 3.30 m with 1.00 m at the bed foot.',9.5)

page('Family bathroom and stair assumptions','Family bathroom 1:50  |  Stair diagram 1:50  |  Heights remain design assumptions')
P=Plan(23,65,[10.6,4.8,16.5,11.1],50);draw_plan(P,D,['u']);P.route(D['paths']['bath'][0]);P.route(D['paths']['bath'][1]);P.route(D['paths']['bath'][2]);P.bar(10.8,11.25,3)
y=note(23,221,120,'Three separate activities','Separate WC, separate bath / shower room, and a shared dry basin area. The WC also has its own hand basin. Changing space stays inside the wet room.')
Q=Plan(183,75,[-.4,-.5,5.2,4],50)
Q.line(0,3,4.5,3);Q.line(0,0,.5,0);Q.line(3.39,0,4.5,0)
rise=.1875;pts=[(.5,3)]
for i in range(8):
    x=.5+i*.27;pts.append((x,3-(i+1)*rise))
    if i<7:pts.append((x+.27,3-(i+1)*rise))
pts.append((3.39,1.5))
for a,b in zip(pts,pts[1:]):Q.line(*a,*b,INK,.8)
pts=[(3.39,1.5),(2.39,1.5)]
for i in range(8):
    x=2.39-i*.27;pts.append((x,1.5-(i+1)*rise))
    if i<7:pts.append((x-.27,1.5-(i+1)*rise))
for a,b in zip(pts,pts[1:]):Q.line(*a,*b,INK,.8)
Q.dim(4.1,0,4.1,3,'3.00 m');Q.label(2,-.25,'Upper floor',8);Q.label(2,3.55,'Lower floor',8)
y=note(316,61,80,'Both stairs','16 rises of 187.5 mm. Going 270 mm. Two 1.00 m clear flights and a 1.00 m half landing.')
y=note(316,y,80,'Section assumptions','Floor to floor: 3.00 m. Floor zone: 300 mm. Clear ceiling: 2.70 m. A full opening above both flights is reserved.')
para(183,189,213,'The drawing explains the assumed stair rise and run. Final headroom needs the roof, beams, landings and floor openings to be designed together. It is not a verified building-regulation section.',10.5)
para(183,224,213,'The next design stage will establish roof shapes, windows and structure, then build the approved plan in 3D. Detailed services routes must also be reworked for two storeys.',10.5)

page('Approved suite direction for the next 3D model','Area summary, retained brief and decisions  |  L01.1 suite revision, 8 October 2026')
footprint=area(D['house'])+area(D['garage'])+area(D['plant'])+2.5*2.4
external=footprint+area(D['house'])+area(D['office'])
rows=[('Proposed plot','2,600 m²'),('Rear garden strip before terrace / planting','1,120 m²'),('House external floor area, both floors',f'{2*area(D["house"]):.2f} m²'),('Garage, gym, workshop and stair footprint',f'{area(D["garage"]):.2f} m²'),('Office external floor area',f'{area(D["office"]):.2f} m²'),('Plant and enclosed link footprints',f'{area(D["plant"])+6:.2f} m²'),('Total building footprint',f'{footprint+1e-8:.2f} m²'),('Total external floor envelopes',f'{external+1e-8:.2f} m²')]
y=62
for a,b in rows:
    txt(20,y,a,10);txt(210,y,b,10,align='right',bold=True);line(20,y+3,210,y+3,GRID,.3);y+=12
para(20,y+4,190,'External areas include walls and stairs. Room schedules use clear room polygons, so the totals differ. These are study measurements, not certified floor areas. The garden strip is not a net lawn-area claim.',9.5,MUTED)
y=note(238,61,158,'Approved suite revision','Keep the rectangular parents bedroom, separate gallery, enlarged U-shaped dressing room and retained bathroom fittings. Add the two garden windows and four rooflight zones shown on page 07.')
y=note(238,y,158,'Carry into the next stage','Warm stone, timber and ivory; no grey finish palette. Retain footwear boundaries, separate family bathroom uses, landscape views, wet underfloor heating, active cooling and solar contribution.')
y=note(238,y,158,'Resolve after floor-plan approval','Roof and window design, stair headroom, structure above the garage opening, bathroom and plant routes, ventilation, and a real-site car-turning check. The former courtyard vault and glazed garden-room roof are not resolved by this two-storey plan.')
para(20,235,190,'Full plans and room details share the same revised geometry. Suite routes have new sampled footprint checks; older layout checks apply to the original source only. Later kitchen / living render studies remain separate inputs for the next coordinated model.',9.5)
para(238,y,158,'Next: establish the vertical design and update the furnished 3D model. Coordinate the later selected kitchen and living studies with this suite. The existing courtyard model stays available for comparison.',10.5)
assert PAGE==9
C.save()
audit.update({'pdf':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'plot':SITE,'external_area_m2':external,'footprint_m2':footprint,'geometry_sha256':hashlib.sha256((HERE/'plans.json').read_bytes()).hexdigest(),'checks':'L01.1 approved suite revision; prior checks apply to the original study. Suite validation is recorded separately. Vehicle poses pass SAT intersection and gate-edge checks.'})
(HERE/'checks.json').write_text(json.dumps(audit,indent=2))
print(f'Created {OUT}\n{PAGE} pages; {SITE["vehicle_check"]["poses"]} clear vehicle poses; external floors {external+1e-8:.2f} m²')
