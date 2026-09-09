from dataclasses import dataclass
from math import cos, sin, pi, hypot
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Helvetica', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Helvetica-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))

ROOT = Path(__file__).parent
OUT = ROOT / 'output' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / 'u-home-dimensioned-concept.pdf'

def polygon_area(p):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))) / 2

def inside(p, poly):
    x,y=p
    result=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>y)!=(b[1]>y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            result=not result
    return result

def box(x,y,w,h):
    return [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]

@dataclass
class Room:
    id: str
    name: str
    poly: list
    category: str
    target: float
    label: tuple
    lines: tuple
    dimensions: str
    @property
    def area(self): return polygon_area(self.poly)

rooms=[]
def room(id,name,x,y,w,h,cat,target,label=None,lines=None):
    r=Room(id,name,box(x,y,w,h),cat,target,label or (x+w/2,y+h/2),lines or (name,),f'{w:.2f} x {h:.2f} m')
    rooms.append(r)
    return r

OUTLINE=[(0,0),(8.2,0),(8.2,12.8),(12.2,12.8),(12.2,9.3),(16.2,9.3),(16.2,0),(22.8,0),(22.8,11.7),(27.15,11.7),(27.15,18.4),(0,18.4)]
INNER=[(.35,.35),(7.85,.35),(7.85,13.15),(12.55,13.15),(12.55,9.65),(16.55,9.65),(16.55,.35),(22.45,.35),(22.45,12.05),(26.8,12.05),(26.8,18.05),(.35,18.05)]
GIA=polygon_area(INNER)
GEA=polygon_area(OUTLINE)
room('P','Parents bedroom',.35,.35,4.2,4,'family',16,(2.25,3.13),('Parents',))
room('W','Walk-in wardrobe',4.67,.35,3.18,2.1,'service',7,(6.26,1.35),('Walk-in',))
room('E','Parents ensuite',4.67,2.57,3.18,1.78,'service',6,(6.05,3.70),('Ensuite',))
room('FB','Family bathroom',.35,4.47,3.03,2.68,'service',8,(1.85,5.85),('Family bath',))
room('ST','Linen / plant',.35,7.27,3.03,1.42,'service',4.5,(1.85,8.40),('Linen / plant',))
room('C3','Child 3',4.82,4.47,3.03,4.22,'family',13,(6.03,6.87))
room('C2','Child 2',.35,8.81,3.03,4.22,'family',13,(2.05,11.10))
room('C1','Child 1',4.82,8.81,3.03,4.22,'family',13,(6.03,11.10))
room('FH','Family hall',3.5,4.47,1.2,8.56,'circulation',10.5,(4.1,10.65),('1.20 m','hall'))
guest_poly=[(16.55,.35),(22.45,.35),(22.45,3.65),(17.87,3.65),(17.87,1.87),(16.55,1.87)]
rooms.append(Room('G','Guest bedroom',guest_poly,'guest',15,(19.9,3.18),('Guest bedroom',),'4.58 x 3.30 m + wardrobe recess'))
room('GS','Guest storage',17.87,3.77,2.36,.95,'service',2.5,(19.05,4.26),('Guest storage',))
room('GB','Guest shower',20.35,3.77,2.1,2.4,'service',5,(21.4,5.40),('Guest shower',))
room('GL','Shower lobby',17.87,4.84,2.36,1.33,'circulation',2,(18.93,5.53),('Lobby',))
room('O','Office / gaming',17.87,6.29,4.58,3.05,'guest',14,(20.0,8.45),('Office / gaming',))
room('S','Snug',17.87,9.46,4.58,2.6,'shared',12,(19.4,10.6),('Snug',))
room('GH','Guest hall',16.55,1.99,1.2,11.16,'circulation',11.5,(17.15,8.0),('1.20 m','hall'))
room('PA','Pantry',14,15.45,2.35,2.6,'service',6,(15.17,16.45),('Pantry',))
laundry_poly=[(20.22,12.18),(22.45,12.18),(22.45,15.33),(17.87,15.33),(17.87,13.70),(20.22,13.70)]
rooms.append(Room('L','Laundry',laundry_poly,'service',10.5,(20.45,14.65),('Laundry',),'L-shape: 4.58 x 3.15 m envelope'))
room('B','Boot room',19.15,15.45,3.3,2.6,'service',8,(20.6,17.2),('Boot room',))
room('H','Entrance hall',16.47,15.45,2.56,2.6,'circulation',6.7,(17.6,17.35),('Entrance hall',))
room('WC','Visitor WC',17.87,12.18,2.23,1.4,'service',3,(18.80,12.95),('WC',))
room('OR','Corner orangery',12.55,9.65,3.65,3.15,'shared',11.5,(14.25,11.65),('Orangery',))
room('GY','Indoor gym',22.8,12.05,4,6,'guest',24,(24.1,15.75),('Indoor gym',))
open_poly=[(.35,13.15),(17.75,13.15),(17.75,15.33),(13.88,15.33),(13.88,18.05),(.35,18.05)]
rooms.append(Room('KL','Kitchen / dining / living',open_poly,'shared',72,(8.0,17.4),('OPEN KITCHEN / DINING / LIVING',),'Main clear depth 4.90 m; stepped kitchen / entrance edge'))
R={r.id:r for r in rooms}

@dataclass
class Door:
    id: str
    a: str
    b: str
    x: float
    y: float
    width: float
    vertical: bool
    kind: str='hinged'
    hinge_end: bool=False
    side: int=1
    pocket_direction: int=1
    thickness: float=.12
    @property
    def opening(self):
        return box(self.x-self.thickness/2-.01,self.y,.02+self.thickness,self.width) if self.vertical else box(self.x,self.y-self.thickness/2-.01,self.width,self.thickness+.02)

doors=[
    Door('D01','FH','P',3.58,4.41,.90,False,hinge_end=True,side=-1),
    Door('P01','P','W',4.61,1.40,.85,True,'pocket',pocket_direction=-1),
    Door('D02','P','E',4.61,3.15,.85,True,hinge_end=True,side=1),
    Door('D03','FH','FB',3.44,4.80,.90,True,side=-1),
    Door('D04','FH','ST',3.44,7.45,.90,True,side=-1),
    Door('D05','FH','C3',4.76,4.70,.90,True,side=1),
    Door('D06','FH','C2',3.44,9.0,.90,True,side=-1),
    Door('D07','FH','C1',4.76,9.0,.90,True,side=1),
    Door('D08','KL','FH',3.50,13.09,.90,False,side=-1),
    Door('D09','GH','G',17.81,2.15,.90,True,side=1),
    Door('O01','GH','GL',17.81,5.1,1.0,True,'opening'),
    Door('C01','GL','GS',18.1,4.78,1.6,False,'sliding'),
    Door('D10','GL','GB',20.29,5.13,.90,True,hinge_end=True,side=1),
    Door('D11','GH','O',17.81,8.2,.90,True,hinge_end=True,side=1),
    Door('D12','GH','S',17.81,10.35,.90,True,side=1),
    Door('O02','GH','KL',16.60,13.15,1.10,False,'opening',thickness=.01),
    Door('P02','KL','PA',13.94,16.05,.90,True,'pocket',pocket_direction=1),
    Door('P03','PA','H',16.41,16.05,.90,True,'pocket',pocket_direction=1),
    Door('P04','L','B',20.45,15.39,.90,False,'pocket',pocket_direction=1),
    Door('D13','H','B',19.09,16.2,.90,True,side=1),
    Door('O03','KL','H',16.65,15.39,.95,False,'opening'),
    Door('D14','GH','WC',17.81,12.40,.85,True,side=1),
    Door('D15','OUT','H',17.60,18.225,1.0,False,hinge_end=False,side=-1,thickness=.35),
    Door('D16','OUT','B',21.15,18.225,1.0,False,side=-1,thickness=.35),
    Door('O04','COURT','KL',9.0,12.975,2.6,False,'sliding',thickness=.35),
    Door('O05','OR','KL',14.7,12.975,1.1,False,'sliding',thickness=.35),
    Door('D17','GH','OR',16.375,11.2,.9,True,hinge_end=True,side=-1,thickness=.35),
    Door('O06','COURT','OR',13.0,9.475,2.8,False,'sliding',thickness=.35),
    Door('D18','B','GY',22.625,16.2,.9,True,side=1,thickness=.35),
]

furniture=[]
def furn(room_id,name,x,y,w,h,kind='cabinet'):
    furniture.append(dict(room=room_id,name=name,rect=[x,y,w,h],kind=kind))

furn('P','King bed frame',1.35,.65,1.65,2.1,'bed')
furn('P','Bedside',.88,.8,.4,.4)
furn('P','Bedside',3.08,.8,.4,.4)
furn('P','Low storage buffer',.50,3.75,2.8,.6)
furn('W','Wardrobes',4.67,.35,.6,1.0)
furn('W','Wardrobes',7.25,.35,.6,2.1)
furn('W','Wardrobes',5.27,.35,1.98,.6)
furn('E','Shower',6.75,2.57,1.1,.9,'shower')
furn('E','WC',5.67,2.64,.65,.72,'wc')
furn('E','Basin',4.87,2.57,.7,.5,'basin')
furn('FB','Bath',.55,4.60,1.7,.75,'bath')
furn('FB','Shower',.5,6.0,1.0,1.0,'shower')
furn('FB','WC',2.45,6.30,.65,.72,'wc')
furn('FB','Basin',1.65,6.65,.55,.5,'basin')
furn('ST','Plant allowance',.5,7.40,.85,.85,'plant')
furn('ST','Linen shelving',1.6,7.40,.65,1.2)
for id,y,left in [('C3',4.7,False),('C2',9.05,True),('C1',9.05,False)]:
    furn(id,'Single bed',.55 if left else 6.65,y,1.0,2.1,'bed')
    furn(id,'Wardrobe',2.78 if left else 4.82,y+1.0,.6,1.5)
    furn(id,'Desk',1.7 if left else 5.6,12.38 if y>8 else 8.04,1.4,.65,'desk')
    furn(id,'Desk chair',2.1 if left else 6.0,11.78 if y>8 else 7.44,.55,.55,'chair')
furn('G','Double bed',20.3,.65,1.6,2.1,'bed')
furn('G','Bedside',19.80,.85,.4,.4)
furn('G','Bedside',22.0,.85,.4,.4)
furn('G','Wardrobe recess',16.55,.35,.6,1.52)
furn('GS','Luggage shelving',17.87,3.77,2.36,.5)
furn('GB','Shower',20.45,3.87,.9,1.1,'shower')
furn('GB','WC',21.65,3.87,.65,.72,'wc')
furn('GB','Basin',21.95,5.25,.5,.65,'basin')
furn('O','Desk',19.25,6.29,2.6,.75,'desk')
furn('O','Chair',20.15,7.18,.65,.65,'chair')
furn('O','Bookcase',22.05,7.55,.4,1.65)
furn('S','Sofa',19.95,11.1,2.1,.9,'sofa')
furn('S','Books / toys',22.05,9.6,.4,1.2)
furn('S','Coffee table',20.4,10.1,.65,.6,'table')
furn('PA','Pantry counter',14,15.45,2.35,.50)
furn('PA','Pantry shelves',14,17.65,2.35,.40)
furn('L','Appliances / sink counter',21.80,12.18,.65,3.15,'laundry')
furn('L','Folding counter',17.87,13.70,2.20,.60)
furn('B','Coat storage',19.15,17.3,.6,.75)
furn('B','Bench / shoes',20.05,17.55,.8,.5,'bench')
furn('H','Coat storage',16.47,17.50,.80,.55)
furn('WC','WC',19.25,12.50,.72,.65,'wc')
furn('WC','Basin',18.75,12.18,.40,.35,'basin')
furn('OR','Small sofa',12.70,10.35,.75,1.60,'sofa')
furn('OR','Coffee table',14.10,10.90,.65,.65,'table')
furn('OR','Armchair',15.10,10.05,.80,.80,'chair')
furn('GY','Combined rack / cables',23.05,12.30,2.40,1.10)
furn('GY','Bench',24.05,13.70,.70,1.50,'bench')
furn('GY','Treadmill',25.55,13.25,1.00,2.05)
furn('GY','Dumbbells',23.05,17.40,2.00,.40)
furn('KL','Media / books',.35,14.5,.4,3.1)
furn('KL','Sofa',4.6,14.85,1.0,2.8,'sofa')
furn('KL','Armchair',1.3,14.7,.85,.85,'chair')
furn('KL','Armchair',1.3,16.8,.85,.85,'chair')
furn('KL','Coffee table',3.0,15.5,.8,1.2,'table')
furn('KL','Dining table',7.15,15.2,2.4,1.0,'table')
for x in [7.3,8.1,8.9]:
    furn('KL','Dining chair',x,14.65,.5,.5,'chair')
    furn('KL','Dining chair',x,16.25,.5,.5,'chair')
furn('KL','Dining chair',6.6,15.45,.5,.5,'chair')
furn('KL','Dining chair',9.6,15.45,.5,.5,'chair')
furn('KL','Island',10.95,14.5,2.8,1.0,'island')
for x in [11.3,12.1,12.9]: furn('KL','Island stool',x,15.6,.5,.5,'chair')
furn('KL','Kitchen counter',10.0,17.45,2.8,.6,'kitchen')
furn('KL','Fridge / freezer',12.80,17.25,.8,.8,'kitchen')

windows=[('h',.8,0,2.4),('v',0,1.0,1.6),('v',8.2,2.9,.85),
 ('v',0,4.65,1.3),('v',0,9.2,2.0),('v',8.2,4.8,2.0),('v',8.2,9.2,2.0),
 ('h',19,0,2.6),('v',22.8,4.2,1.0),('v',22.8,6.65,1.8),('v',22.8,9.8,1.5),
 ('v',27.15,13.3,2.4),('v',12.2,10.4,1.5),('h',1.1,18.4,3.1),('h',6.6,18.4,3.0),('h',10.5,18.4,2.0)]

routes={
 'Arrival to kitchen':[(18.05,17.5),(17.2,16.4),(17.125,15.8),(17.125,14.5),(16.3,14.25)],
 'Boot to pantry':[(20.25,17.1),(20.25,16.65),(18.5,16.65),(17.3,16.5),(15.2,16.5),(13.94,16.5),(13.15,16.7)],
 'Boot to laundry':[(20.25,17.1),(20.9,16.2),(20.9,14.0)],
 'Family to living':[(4.1,4.8),(4.1,12.0),(3.95,12.6),(3.95,13.7),(6.1,13.85)],
 'Guests to living':[(19.0,3.0),(18.1,2.6),(17.15,2.6),(17.15,13.75),(16.5,13.85),(9.7,13.85)],
 'Hall through orangery to living':[(17.15,10.8),(17.15,11.65),(16.375,11.65),(15.25,11.65),(15.25,13.8)],
 'Boot to gym':[(20.25,17.1),(21.0,16.65),(22.625,16.65),(24.0,16.65)],
}

def overlap(a,b):
    x,y,w,h=a; X,Y,W,H=b
    return max(0,min(x+w,X+W)-max(x,X))*max(0,min(y+h,Y+H)-max(y,Y))

def verify():
    issues=[]
    for r in rooms:
        for a,b in zip(r.poly,r.poly[1:]+r.poly[:1]):
            midpoint=((a[0]+b[0])/2,(a[1]+b[1])/2)
            centre=(sum(p[0] for p in r.poly)/len(r.poly),sum(p[1] for p in r.poly)/len(r.poly))
            p=(midpoint[0]+(centre[0]-midpoint[0])*1e-5,midpoint[1]+(centre[1]-midpoint[1])*1e-5)
            if not inside(p,INNER): issues.append(f'Room outside internal envelope: {r.id}')
    for i,r in enumerate(rooms):
        for rr in rooms[i+1:]:
            xs=sorted(set(p[0] for p in r.poly+rr.poly)); ys=sorted(set(p[1] for p in r.poly+rr.poly))
            area=sum((b-a)*(d-c) for a,b in zip(xs,xs[1:]) for c,d in zip(ys,ys[1:]) if inside(((a+b)/2,(c+d)/2),r.poly) and inside(((a+b)/2,(c+d)/2),rr.poly))
            if area>1e-7: issues.append(f'Room overlap {r.id}/{rr.id}: {area}')
    for f in furniture:
        x,y,w,h=f['rect']
        if not all(inside(p,R[f['room']].poly) for p in [(x+.001,y+.001),(x+w-.001,y+.001),(x+.001,y+h-.001),(x+w-.001,y+h-.001)]):
            issues.append(f'Furniture outside room: {f["room"]} {f["name"]}')
    for i,f in enumerate(furniture):
        for g in furniture[i+1:]:
            if overlap(f['rect'],g['rect'])>1e-7: issues.append(f'Furniture overlap {f["name"]}/{g["name"]} ({f["room"]})')
    for d in doors:
        if d.a in R and d.b in R:
            eps=d.thickness/2+.025
            pts=[(d.x-eps,d.y+d.width/2),(d.x+eps,d.y+d.width/2)] if d.vertical else [(d.x+d.width/2,d.y-eps),(d.x+d.width/2,d.y+eps)]
            if not ((inside(pts[0],R[d.a].poly) and inside(pts[1],R[d.b].poly)) or (inside(pts[1],R[d.a].poly) and inside(pts[0],R[d.b].poly))):
                issues.append(f'Door does not connect declared rooms: {d.id} {d.a}/{d.b}')
        if d.kind=='pocket':
            start=(d.y if d.vertical else d.x)
            length=d.width+.1
            a=start-length if d.pocket_direction<0 else start+d.width
            reserve=box(d.x-d.thickness/2,a,d.thickness,length) if d.vertical else box(a,d.y-d.thickness/2,length,d.thickness)
            for other in doors:
                if other==d: continue
                if any(inside(p,reserve) for p in other.opening): issues.append(f'Pocket overlaps another opening: {d.id}/{other.id}')
        if d.kind=='hinged':
            hinge=(d.x,d.y+d.width if d.hinge_end else d.y) if d.vertical else (d.x+d.width if d.hinge_end else d.x,d.y)
            closed=(0,-1 if d.hinge_end else 1) if d.vertical else (-1 if d.hinge_end else 1,0)
            opened=(d.side,0) if d.vertical else (0,d.side)
            for f in furniture:
                if f['room'] not in [d.a,d.b]: continue
                xx,yy,ww,hh=f['rect']; collision=False
                for i in range(int(ww/.025)+1):
                    for j in range(int(hh/.025)+1):
                        dx=xx+i*.025-hinge[0];dy=yy+j*.025-hinge[1]
                        if dx*closed[0]+dy*closed[1]>.015 and dx*opened[0]+dy*opened[1]>.015 and hypot(dx,dy)<d.width-.015:
                            collision=True;break
                    if collision:break
                if collision:issues.append(f'Door swing hits furniture: {d.id} / {f["name"]} ({f["room"]})')
    for name,pts in routes.items():
        failed=False
        for a,b in zip(pts,pts[1:]):
            length=hypot(b[0]-a[0],b[1]-a[1])
            for k in range(int(length/.025)+1):
                t=k/max(1,int(length/.025)); p=(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
                if not any(inside(p,r.poly) for r in rooms) and not any(inside(p,d.opening) for d in doors):
                    issues.append(f'Route crosses wall: {name} at {p}'); break
                if any(inside(p,box(*f['rect'])) for f in furniture): issues.append(f'Route crosses furniture: {name} at {p}'); break
                for k in range(16):
                    q=(p[0]+.35*cos(k*pi/8),p[1]+.35*sin(k*pi/8))
                    if (not any(inside(q,r.poly) for r in rooms) and not any(inside(q,d.opening) for d in doors)) or any(inside(q,box(*f['rect'])) for f in furniture):
                        issues.append(f'Route 0.70 m envelope obstructed: {name} at {q}')
                        failed=True;break
                if failed:break
            if failed:break
    return issues

PALETTE={'family':'#e6ede8','guest':'#e8edf0','shared':'#f4eadb','service':'#efeeea','circulation':'#ffffff','wall':'#343b38','ink':'#25332c','muted':'#58665e','furniture':'#d7d8d0','garden':'#e5eedf'}
PW,PH=420,297
c=canvas.Canvas(str(PDF),pagesize=(PW*mm,PH*mm))
c.setTitle('U home - dimensioned concept 05')
c.setAuthor('House plan working study')

def color(v): return HexColor(PALETTE.get(v,v))
def text(x,y,t,size=3.0,font='Helvetica',align='left',fill='ink'):
    c.setFillColor(color(fill)); c.setFont(font,size*mm)
    {'left':c.drawString,'center':c.drawCentredString,'right':c.drawRightString}[align](x*mm,(PH-y)*mm,t)
def line(x1,y1,x2,y2,fill='ink',width=.2,dash=None):
    c.setStrokeColor(color(fill)); c.setLineWidth(width*mm); c.setDash(dash or [])
    c.line(x1*mm,(PH-y1)*mm,x2*mm,(PH-y2)*mm); c.setDash([])
def rect(x,y,w,h,fill=None,stroke='ink',lw=.2):
    c.setLineWidth(lw*mm)
    if fill: c.setFillColor(color(fill))
    if stroke: c.setStrokeColor(color(stroke))
    c.rect(x*mm,(PH-y-h)*mm,w*mm,h*mm,fill=bool(fill),stroke=bool(stroke))
def poly(points,fill=None,stroke='ink',lw=.2):
    p=c.beginPath(); p.moveTo(points[0][0]*mm,(PH-points[0][1])*mm)
    for x,y in points[1:]: p.lineTo(x*mm,(PH-y)*mm)
    p.close(); c.setLineWidth(lw*mm)
    if fill: c.setFillColor(color(fill))
    if stroke: c.setStrokeColor(color(stroke))
    c.drawPath(p,fill=bool(fill),stroke=bool(stroke))

class Plan:
    def __init__(self,ox,oy,s,detail=False): self.ox,self.oy,self.s,self.detail=ox,oy,s,detail
    def xy(self,p): return self.ox+p[0]*self.s,self.oy+p[1]*self.s
    def rect(self,x,y,w,h,fill=None,stroke='ink',lw=.15):
        X,Y=self.xy((x,y)); rect(X,Y,w*self.s,h*self.s,fill,stroke,lw)
    def poly(self,pts,fill=None,stroke='ink',lw=.15): poly([self.xy(p) for p in pts],fill,stroke,lw)
    def line(self,a,b,fill='ink',lw=.15,dash=None): line(*self.xy(a),*self.xy(b),fill,lw,dash)
    def text(self,x,y,t,size=2.3,align='center',fill='ink',font='Helvetica'):
        text(*self.xy((x,y)),t,size,font,align,fill)
    def dimension(self,a,b,offset,label=None,vertical=False):
        if vertical:
            p=(a[0]+offset,a[1]); q=(b[0]+offset,b[1])
        else:
            p=(a[0],a[1]+offset); q=(b[0],b[1]+offset)
        self.line(a,p,'muted',.10); self.line(b,q,'muted',.10); self.line(p,q,'muted',.12)
        for u in [p,q]: self.line((u[0]-.10,u[1]-.10),(u[0]+.10,u[1]+.10),'muted',.15)
        value=label or f'{hypot(b[0]-a[0],b[1]-a[1]):.2f} m'
        if vertical:
            X,Y=self.xy(((p[0]+q[0])/2-.2,(p[1]+q[1])/2)); c.saveState(); c.translate(X*mm,(PH-Y)*mm); c.rotate(90); c.setFont('Helvetica',2.4*mm); c.setFillColor(color('muted')); c.drawCentredString(0,0,value); c.restoreState()
        else: self.text((p[0]+q[0])/2,p[1]-.17,value,2.4,fill='muted')
    def opening(self,d):
        self.poly(d.opening,'#ffffff',None)
        if d.kind=='pocket':
            start=d.y if d.vertical else d.x
            length=d.width+.1
            a=start-length if d.pocket_direction<0 else start+d.width
            pts=((d.x,a),(d.x,a+length)) if d.vertical else ((a,d.y),(a+length,d.y))
            self.line(*pts,'#168271',.4,[1.0,0.6])
        elif d.kind=='hinged':
            start=(d.x,d.y+d.width if d.hinge_end else d.y) if d.vertical else (d.x+d.width if d.hinge_end else d.x,d.y)
            closed=(d.x,d.y if d.hinge_end else d.y+d.width) if d.vertical else (d.x if d.hinge_end else d.x+d.width,d.y)
            opened=(d.x+d.side*d.width,start[1]) if d.vertical else (start[0],d.y+d.side*d.width)
            self.line(start,opened,'ink',.15)
            v=(closed[0]-start[0],closed[1]-start[1]); w=(opened[0]-start[0],opened[1]-start[1])
            pts=[(start[0]+v[0]*cos(t)+w[0]*sin(t),start[1]+v[1]*cos(t)+w[1]*sin(t)) for t in [i*pi/32 for i in range(17)]]
            for a,b in zip(pts,pts[1:]): self.line(a,b,'muted',.08)
        elif d.kind=='sliding':
            self.line((d.x,d.y-.05),(d.x+d.width,d.y-.05),'#498780',.35)
            self.line((d.x+d.width*.48,d.y+.05),(d.x+d.width,d.y+.05),'#498780',.35)
    def draw(self,labels=True,include=None):
        self.poly(OUTLINE,'wall',None)
        for r in rooms: self.poly(r.poly,r.category,None)
        for d in doors: self.opening(d)
        for orientation,x,y,w in windows:
            if orientation=='h':
                self.rect(x,y-.01 if y==0 else y-.35,w,.36,'#ffffff',None)
                self.line((x,y-.01 if y==0 else y-.17),(x+w,y-.01 if y==0 else y-.17),'#498780',.35)
            else:
                left=x if x in [0,12.2,16.2] else x-.35
                self.rect(left,y,.35,w,'#ffffff',None)
                self.line((left+.17,y),(left+.17,y+w),'#498780',.35)
        for f in furniture:
            x,y,w,h=f['rect']; kind=f['kind']
            self.rect(x,y,w,h,'furniture','muted',.12)
            if kind=='bed':
                self.rect(x+.08,y+.08,w-.16,.40,'#f9f8f4','muted',.08)
                self.line((x,y+.6),(x+w,y+.6),'muted',.08)
            elif kind=='shower':
                self.line((x,y),(x+w,y+h),'muted',.08); self.line((x+w,y),(x,y+h),'muted',.08)
            elif kind in ['wc','basin','bath']:
                X,Y=self.xy((x+.08,y+.08)); c.setStrokeColor(color('muted')); c.setFillColor(color('#ffffff')); c.ellipse(X*mm,(PH-Y-(h-.16)*self.s)*mm,(X+(w-.16)*self.s)*mm,(PH-Y)*mm,fill=1,stroke=1)
            elif kind=='laundry':
                for yy in [y+.2,y+.95,y+2.0]: self.rect(x+.06,yy,w-.12,.6,'#f9f8f4','muted',.08)
            elif kind=='sofa':
                if w>h: self.line((x+.15,y+.22),(x+w-.15,y+.22),'muted',.09)
                else: self.line((x+w-.22,y+.15),(x+w-.22,y+h-.15),'muted',.09)
            elif kind=='island': self.rect(x+.45,y+.18,.65,.45,'#f9f8f4','muted',.08)
        if labels:
            for r in rooms:
                if include and r.id not in include: continue
                x,y=r.label
                if r.category=='circulation' and r.id in ['FH','GH']:
                    for i,t in enumerate(r.lines): self.text(x,y+i*.27,t,2.0,fill='muted')
                    continue
                lines=list(r.lines)
                if r.id not in ['ST','GS','GL']: lines.append(f'{r.area:.1f} m2')
                fs=2.4 if self.detail else 2.25
                widths=[c.stringWidth(t,'Helvetica',fs*mm)/mm for t in lines]
                X,Y=self.xy((x,y)); rect(X-max(widths)/2-.7,Y-2.1,max(widths)+1.4,len(lines)*2.7+.1,'#ffffff',None)
                for i,t in enumerate(lines): self.text(x,y+i*2.7/self.s,t,fs,fill='ink')
        return self

def header(kicker,title,sub):
    text(14,12,kicker,2.7,fill='muted')
    text(14,23,title,6.7,font='Helvetica-Bold')
    text(14,31,sub,3.0,fill='muted')
    line(14,36,406,36,'#bcc8bf',.3)
def footer(page):
    line(14,281,406,281,'#bcc8bf',.2)
    text(14,287,'CONCEPT 05 | Proposed dimensions. Not for construction. Roof and site design pending.',2.55,fill='muted')
    text(406,287,f'{page} / 4',2.55,align='right',fill='muted')
def paragraph(x,y,lines,step=4.6,size=2.8):
    for t in lines: text(x,y,t,size); y+=step
    return y

def courtyard(p,labels=True):
    p.rect(8.2,0,8,12.8,'garden',None)
    p.rect(8.2,6.3,8,6.5,'#eee9dc',None)
    p.rect(9.05,8.2,2.4,1.0,'furniture','muted',.15)
    for xx in [9.2,10.0,10.8]:
        p.rect(xx,7.65,.5,.5,'furniture','muted',.1)
        p.rect(xx,9.25,.5,.5,'furniture','muted',.1)
    if labels:
        p.text(12.2,2.0,'MAIN GARDEN BEYOND',3.0)
        p.text(12.2,5.0,'88.4 m2 open courtyard',3.0)
        p.text(10.1,10.8,'4.0 m open strip',2.5)

def roof_allowances(p):
    for x,y,w,h in [(13.2,10.1,2.2,1.7),(20.6,12.6,.8,1.0)]:
        for a,b in zip(box(x,y,w,h),box(x,y,w,h)[1:]+box(x,y,w,h)[:1]):
            p.line(a,b,'#168271',.15,[1,.7])
    for a,b in zip(box(25.35,15.45,1.35,2.2),box(25.35,15.45,1.35,2.2)[1:]+box(25.35,15.45,1.35,2.2)[:1]):
        p.line(a,b,'muted',.15,[1,.7])

issues=verify()
metrics={'gia_m2':GIA,'external_footprint_m2':GEA,'outer_width_m':27.15,'outer_depth_m':18.4,'courtyard_original_recess_m2':102.4,'open_courtyard_m2':88.4,'orangery_external_allocation_m2':14,'clear_room_area_m2':sum(r.area for r in rooms),'partitions_and_thresholds_m2':GIA-sum(r.area for r in rooms),'rooms':[dict(id=r.id,name=r.name,area=round(r.area,4),target=r.target,dimensions=r.dimensions) for r in rooms],'checked_routes':list(routes),'checks':issues}
(OUT/'area-check.json').write_text(json.dumps(metrics,indent=2)+'\n')
if issues: raise ValueError('\n'.join(issues))

header('SINGLE-STOREY / FIVE BEDROOMS / CORNER ORANGERY','A garden room at the heart of the U','1:100 at A3, printed at 100% | Metres | 350 mm external walls and 120 mm internal partitions assumed')
p=Plan(22,67,10)
courtyard(p)
p.draw()
roof_allowances(p)
p.dimension((0,0),(27.15,0),-1.85,'27.15 m overall including gym')
p.dimension((0,0),(8.2,0),-.75,'8.20 m')
p.dimension((8.2,0),(16.2,0),-.75,'8.00 m courtyard')
p.dimension((16.2,0),(22.8,0),-.75,'6.60 m')
p.dimension((22.8,11.7),(27.15,11.7),-.6,'4.35 m addition')
p.dimension((0,0),(0,18.4),-.8,'18.40 m overall',True)
p.text(2.5,19.3,'5 m scale bar',2.4,fill='muted')
for a in range(5): p.rect(a,19.5,1,.12,'wall' if a%2==0 else '#ffffff','ink',.12)
text(310,53,f'{GIA:.1f} m2 GIA',6.5,font='Helvetica-Bold')
text(310,61,f'{GEA:.1f} m2 external footprint',2.9,fill='muted')
text(310,76,'The agreed additions',3.5,font='Helvetica-Bold')
paragraph(310,85,[
 'Orangery: 4.00 x 3.50 m footprint;',
 '3.65 x 3.15 m / 11.5 m2 inside.',
 'Hall and living connections;',
 'direct hall/living route retained.',
 '',
 'Gym: 4.00 x 6.00 m clear,',
 'entered through the boot room.',
 'Rack/cables, bench, dumbbells',
 'and treadmill shown indicatively.',
 '',
 'Pantry beside fridge and counter.',
 'Smaller hall; wider laundry.',
 'Visitor WC off the guest hall.'
],step=5.2,size=2.9)
text(310,166,'Courtyard and roof',3.5,font='Helvetica-Bold')
paragraph(310,175,[
 '88.4 m2 remains open to the sky.',
 '4 m separates the orangery',
 'from the bedroom wing.',
 'Direct living/courtyard doors',
 'remain beside the orangery.',
 '',
 'Dashed teal: rooflight proposals',
 'for orangery and laundry.',
 'Heating, shading and ventilation',
 'are not yet specified.'
],step=5.2,size=2.9)
paragraph(310,239,[
 'Furniture and nominated routes',
 'checked; equipment-specific',
 'clearances still need confirmation.'
],step=5,size=2.8)
footer(1);c.showPage()

header('ROOM SCHEDULE / FAMILY WING','Space accounted for','Family detail at 1:60 on A3 | Net room areas include fitted furniture; GIA includes partitions')
c.saveState();clip=c.beginPath();clip.rect(14*mm,(PH-263)*mm,143*mm,222*mm);c.clipPath(clip,stroke=0)
fp=Plan(17,43,1000/60,True);fp.draw(include=['P','W','E','FB','ST','C1','C2','C3','FH'])
c.restoreState()
text(17,268,'Family grouping retained from concept 04',2.8,fill='muted')
sx=170
text(sx,48,'ROOM',2.8,font='Helvetica-Bold');text(262,48,'CLEAR SIZE (m)',2.8,font='Helvetica-Bold');text(399,48,'m2',2.8,font='Helvetica-Bold',align='right')
groups=[('Shared living',['KL']),('Parents bedroom',['P']),('Walk-in wardrobe',['W']),('Parents ensuite',['E']),('Children: 3 rooms',['C1','C2','C3']),('Family bathroom',['FB']),('Guest bedroom',['G']),('Guest shower',['GB']),('Office / gaming',['O']),('Snug',['S']),('Corner orangery',['OR']),('Indoor gym',['GY']),('Pantry',['PA']),('Boot room',['B']),('Laundry',['L']),('Visitor WC',['WC']),('Linen / plant / guest storage',['ST','GS']),('Entrance hall',['H']),('Other circulation',['FH','GH','GL'])]
y=57
for name,ids in groups:
    actual=sum(R[i].area for i in ids)
    dimensions=R[ids[0]].dimensions.replace(' m','')
    if ids==['KL']: dimensions='4.90 deep / stepped'
    if ids==['G']: dimensions='4.58 x 3.30 + wardrobe recess'
    if ids==['L']: dimensions='L-shape; 4.58 x 3.15 envelope'
    if ids==['C1','C2','C3']: dimensions='Each 3.03 x 4.22 / 12.79 m2'
    if ids==['ST','GS']: dimensions='Two storage zones'
    if ids==['FH','GH','GL']: dimensions='1.20-wide halls + shower lobby'
    text(sx,y,name,2.8);text(262,y,dimensions,2.65);text(399,y,f'{actual:.2f}',2.8,align='right')
    line(sx,y+2,403,y+2,'#d8dfd9',.1);y+=7.1
text(sx,y+2,'Partitions + doorway thresholds',2.8)
text(399,y+2,f'{metrics["partitions_and_thresholds_m2"]:.2f}',2.8,align='right')
text(sx,y+12,'TOTAL GIA',3.4,font='Helvetica-Bold');text(399,y+12,f'{GIA:.2f}',3.4,font='Helvetica-Bold',align='right')
paragraph(sx,224,[
 'Concept 04: 279.81 m2 GIA. This revision adds 40.10 m2.',
 'Gym: 24.00 m2 clear plus 2.10 m2 of retained dividing wall.',
 'Orangery: 11.50 m2 clear plus 2.50 m2 of wall / thresholds.',
 f'Open living remains {R["KL"].area:.2f} m2; hall reduces to {R["H"].area:.2f} m2.',
 'A 0.90 m pantry shift recovers 2.34 m2 of kitchen area',
 'compared with the preceding exploratory pantry option.'
],step=6,size=2.9)
footer(2);c.showPage()

header('ORANGERY / KITCHEN / SERVICE ROOMS / GYM','Making the connections work','Enlarged corner at 1:60 on A3 | Teal routes are checked with a sampled 0.70 m walking envelope')
c.saveState();clip=c.beginPath();clip.rect(15*mm,(PH-207)*mm,390*mm,164*mm);c.clipPath(clip,stroke=0)
sp=Plan(24-9*(1000/60),48-9.0*(1000/60),1000/60,True)
courtyard(sp,False);sp.draw(include=['OR','GY','PA','L','B','H','WC']);roof_allowances(sp)
for name in ['Arrival to kitchen','Boot to pantry','Boot to laundry','Hall through orangery to living','Boot to gym']:
    for a,b in zip(routes[name],routes[name][1:]):sp.line(a,b,'#168271',.4,[2,1])
c.restoreState()
text(18,217,'Everyday connections',3.8,font='Helvetica-Bold')
paragraph(18,226,[
 'Boot room > hall > pantry > kitchen; direct hall/kitchen access remains.',
 'Orangery doors meet along its clear south/east edge, beside the seating.',
 'The smaller hall retains coat storage and access to boot room / kitchen.',
 'Laundry gains a folding counter; its daylight is now via a rooflight.',
 'Pantry and laundry pocket doors require clear wall cavities.'
],step=6,size=2.9)
text(224,217,'Gym and design limits',3.8,font='Helvetica-Bold')
paragraph(224,226,[
 'Combined rack/cable unit and equipment are illustrative footprints.',
 'Dashed grey zone: 1.35 x 2.20 m treadmill rear allowance.',
 'Check the chosen machines, barbell handling, height and anchoring.',
 'Acoustics, structures, drainage, rooflight/shading design and',
 'building compliance require detailed work; these are concept checks.'
],step=6,size=2.9)
footer(3);c.showPage()

header('ILLUSTRATIVE PLOT / ARRIVAL / GARDEN','The wider house on the same test plot','1:200 at A3, printed at 100% | Hypothetical 35 x 45 m plot | Orientation and boundary clearances unassigned')
site=Plan(21,44,5)
site.rect(0,0,35,45,'garden','ink',.3)
site.rect(0,45,35,1.5,'#d6d8d5',None)
site.rect(18,38.7,12.5,6.0,'#ece8df',None)
site.rect(22,44.7,5,.3,'#ece8df',None)
site.rect(18,30.9,1.0,7.6,'#ece8df',None)
site.rect(19,30.9,11.45,1.4,'#ece8df',None)
hp=Plan(21+3.3*5,44+12.5*5,5)
courtyard(hp,False);hp.draw(labels=False)
site.text(16.5,7.5,'MAIN REAR GARDEN',3.2)
site.text(16.5,8.5,'Approx. 12.5 m deep before the house',2.8)
site.rect(19,32.3,6.8,6.2,'#dce5e2','ink',.25)
for a,b in [((18.8,32.1),(26.0,32.1)),((26.0,32.1),(26.0,38.7)),((26.0,38.7),(18.8,38.7)),((18.8,38.7),(18.8,32.1))]:
    site.line(a,b,'#168271',.2,[1,1])
for xx in [18.8,25.8]:
    for yy in [32.1,38.5]:site.rect(xx,yy,.2,.2,'wall',None)
site.line((22.4,32.3),(22.4,38.5),'muted',.15)
for xx in [19.7,23.1]:
    site.rect(xx,33.0,2.0,4.9,'#bec6c2','muted',.2)
    site.rect(xx+.12,33.8,1.76,1.3,'#edf2ee','muted',.1)
site.rect(26.5,32.3,3.2,6.0,'#ece8df','ink',.2)
site.rect(27.1,33.0,2.0,4.9,'#bec6c2','muted',.2)
site.text(22.4,31.8,'Carport: 6.8 x 6.2 m clear',2.6)
site.text(28.1,31.2,'Guest bay',2.6)
site.text(24,41.2,'6.0 m clear manoeuvring apron',2.7)
site.dimension((0,0),(35,0),-1.0,'35.0 m')
site.dimension((0,0),(0,45),-1.1,'45.0 m',True)
text(215,50,'1,575 m2 illustrative plot',6.0,font='Helvetica-Bold')
text(215,59,'Approximately 0.39 acres',3.1,fill='muted')
paragraph(215,73,[
 f'House including gym and orangery: {GEA:.1f} m2 external footprint.',
 'Open courtyard: 88.4 m2; approximately 38 m2 paved.',
 'Orangery allocation: 14 m2 within the original courtyard.',
 'Gym is inside the house; the detached studio is removed.',
 'Carport: 42.2 m2 clear; provisional roof envelope 47.5 m2.',
 'Guest bay: 3.2 x 6.0 m, independent of the carport.'
],step=7,size=3.0)
text(215,128,'Arrival and boundary assumptions',3.8,font='Helvetica-Bold')
paragraph(215,138,[
 'The gym leaves 4.55 m to the right test boundary.',
 'A 1.4 m strip separates the house and parking allocations.',
 'Cars shown as 2.0 x 4.9 m bodies, excluding mirrors.',
 'The 6 m manoeuvring apron remains clear of structures.',
 'Chosen vehicles require a proper swept-path check.',
 'Carport columns sit outside its clear parking allocation.'
],step=5.5,size=3.0)
text(215,184,'Before choosing a plot',3.8,font='Helvetica-Bold')
paragraph(215,194,[
 'Test orientation, winter sunlight, privacy and overheating.',
 'Check access rights, local planning, drainage and services.',
 'Allow for topography, trees and boundary constraints.',
 'This rectangle demonstrates a fit; it is not a minimum',
 'plot size or evidence that a particular site is buildable.'
],step=5.5,size=3.0)
text(215,235,'Area convention',3.4,font='Helvetica-Bold')
paragraph(215,244,[
 'GIA is measured to the internal faces of external walls.',
 'Gym and orangery are included, with internal partitions.',
 'Room areas include fitted joinery footprints; carport',
 'and remaining open courtyard are additional.'
],step=4.8,size=2.8)
footer(4);c.save()

print(f'GIA: {GIA:.2f} m2; external footprint: {GEA:.2f} m2')
print(f'Checks: {len(issues)} issues across {len(routes)} routes')
print(PDF)
