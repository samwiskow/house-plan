"""Build the consolidated house design book from the shared model and scene views."""
import hashlib
import json
from math import cos, pi, sin
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from house_design_model import load_current_model

ROOT=Path(__file__).parent
MODEL=json.loads((ROOT/'viewer/model.json').read_text())
m,_=load_current_model()
OUT=ROOT/'output/pdf/house-design-book.pdf'
VIEWS=ROOT/'output/design/book-views'
MM=72/25.4
W,H=420,297
for name,file in [('Text','Arial.ttf'),('Bold','Arial Bold.ttf'),('Title','Georgia.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/System/Library/Fonts/Supplemental/'+file))
pdfmetrics.registerFontFamily('Text',normal='Text',bold='Bold',italic='Text',boldItalic='Bold')
C=canvas.Canvas(str(OUT),pagesize=(W*MM,H*MM))
C.setTitle('The courtyard house - House Design Book 02')
C.setAuthor('House design study')
C.setSubject('Consolidated concept design, 13 September 2026')
INK='#303d33';MUTED='#68695d';PAPER='#fffdf7';LINE='#cfc8b8';GREEN='#35533d';GOLD='#9b7951'
P=MODEL['palette']
PAGE=0

def text(x,y,t,size=3.1,font='Text',color=INK,align='left'):
    C.setFillColor(HexColor(color));C.setFont(font,size*MM)
    {'left':C.drawString,'center':C.drawCentredString,'right':C.drawRightString}[align](x*MM,(H-y)*MM,t)

def rect(x,y,w,h,fill=None,stroke=None,lw=.2):
    if fill:C.setFillColor(HexColor(fill))
    if stroke:C.setStrokeColor(HexColor(stroke))
    C.setLineWidth(lw*MM);C.rect(x*MM,(H-y-h)*MM,w*MM,h*MM,fill=bool(fill),stroke=bool(stroke))

def line(a,b,color=LINE,lw=.2,dash=None):
    C.setStrokeColor(HexColor(color));C.setLineWidth(lw*MM);C.setDash(dash or [])
    C.line(a[0]*MM,(H-a[1])*MM,b[0]*MM,(H-b[1])*MM);C.setDash([])

def poly(points,fill=None,stroke=None,lw=.2):
    path=C.beginPath();path.moveTo(points[0][0]*MM,(H-points[0][1])*MM)
    for x,y in points[1:]:path.lineTo(x*MM,(H-y)*MM)
    path.close()
    if fill:C.setFillColor(HexColor(fill))
    if stroke:C.setStrokeColor(HexColor(stroke))
    C.setLineWidth(lw*MM);C.drawPath(path,fill=bool(fill),stroke=bool(stroke))

def para(x,y,w,t,size=3.25,color=MUTED,leading=1.45,font='Text'):
    style=ParagraphStyle('body',fontName=font,fontSize=size*MM,leading=size*MM*leading,textColor=HexColor(color),alignment=TA_LEFT)
    p=Paragraph(t,style);_,height=p.wrap(w*MM,1000);p.drawOn(C,x*MM,(H-y)*MM-height)
    return y+height/MM

def image(name,x,y,w,h):
    path=VIEWS/(name+'.png');im=ImageReader(str(path));iw,ih=im.getSize()
    scale=max(w/iw,h/ih);dw,dh=iw*scale,ih*scale
    C.saveState();clip=C.beginPath();clip.rect(x*MM,(H-y-h)*MM,w*MM,h*MM);C.clipPath(clip,stroke=0)
    C.drawImage(im,(x+(w-dw)/2)*MM,(H-y-h+(h-dh)/2)*MM,dw*MM,dh*MM,mask='auto');C.restoreState()

def page(chapter,title,subtitle):
    global PAGE
    PAGE+=1
    rect(0,0,W,H,PAPER)
    text(18,14,'THE COURTYARD HOUSE',2.6,'Bold',GREEN)
    text(402,14,chapter.upper(),2.5,'Text',MUTED,'right')
    text(18,32,title,8.1,'Title')
    para(18,40,382,subtitle,3.05)
    line((18,56),(402,56))
    line((18,280),(402,280))
    text(18,287,'DESIGN BOOK 02  /  13 SEPTEMBER 2026  /  CONCEPT DESIGN',2.3,'Text',MUTED)
    text(402,287,f'{PAGE:02d} / 16',2.6,'Text',MUTED,'right')
    C.bookmarkPage(f'p{PAGE}');C.addOutlineEntry(title,f'p{PAGE}',0)

def end():C.showPage()

def note(x,y,w,title,body):
    text(x,y,title,4,'Bold');return para(x,y+5,w,body)

def chip(x,y,w,color,name,description):
    rect(x,y,w,17,color)
    text(x,y+24,name,3.1,'Bold');para(x,y+28,w,description,2.7)

def plan(x,y,scale,rooms=None,labels=True,mode='Professional',court=True,bounds=None,zones=False):
    model=MODEL
    state=m if mode=='Professional' else load_current_model(mode)[0]
    transform=lambda p:(x+p[0]*scale,y+p[1]*scale)
    def rbox(r,fill,stroke=None,lw=.12):rect(x+r[0]*scale,y+r[1]*scale,r[2]*scale,r[3]*scale,fill,stroke,lw)
    C.saveState()
    if bounds:
        bx,by,bw,bh=bounds;path=C.beginPath();path.rect(bx*MM,(H-by-bh)*MM,bw*MM,bh*MM);C.clipPath(path,stroke=0)
    if court:
        poly([transform(p) for p in model['courtyard']],'#e7eddb')
        for r in model['paving']:rbox(r,'#e9dfc9')
        for bed in model['plantingBeds']:rbox(bed['rect'],'#9dab86')
        for f in model['outdoorFurniture']:rbox(f['rect'],'#cdb28a',MUTED)
    poly([transform(p) for p in model['outline']],INK)
    for room in model['rooms']:
        shade=({'family':'#d7dfc9','guest':'#d6decd','service':'#dfd3bc','circulation':'#f4edde','shared':'#f1dfbd'} if zones else {'family':'#f2eee3','guest':'#f2eee3','service':'#eee8d9','circulation':'#faf6eb','shared':'#f4e8d1'})[room['category']]
        poly([transform(p) for p in room['polygon']],shade)
    for d in state.doors:
        poly([transform(p) for p in d.opening],PAPER)
        start=(d.x,d.y+d.width if d.hinge_end else d.y) if d.vertical else (d.x+d.width if d.hinge_end else d.x,d.y)
        if d.kind=='hinged':
            closed=(d.x,d.y if d.hinge_end else d.y+d.width) if d.vertical else (d.x if d.hinge_end else d.x+d.width,d.y)
            opened=(d.x+d.side*d.width,start[1]) if d.vertical else (start[0],d.y+d.side*d.width)
            line(transform(start),transform(opened),INK,.15)
            v=(closed[0]-start[0],closed[1]-start[1]);w=(opened[0]-start[0],opened[1]-start[1])
            pts=[(start[0]+v[0]*cos(t)+w[0]*sin(t),start[1]+v[1]*cos(t)+w[1]*sin(t)) for t in [i*pi/32 for i in range(17)]]
            for a,b in zip(pts,pts[1:]):line(transform(a),transform(b),MUTED,.09)
        elif d.kind in ('sliding','pocket'):
            finish=(d.x,d.y+d.width) if d.vertical else (d.x+d.width,d.y)
            line(transform((d.x,d.y)),transform(finish),GREEN,.3,[1,1] if d.kind=='pocket' else None)
    for win in model['windows']:
        axis,wx,wy,length=win['orientation'],win['x'],win['y'],win['length']
        wr=[wx,wy if wy==0 else wy-.35,length,.35] if axis=='h' else [wx if wx in (0,12.2,16.2) else wx-.35,wy,.35,length]
        rbox(wr,'#dae5df',GREEN,.12)
    if not zones:
        for wet in model['wetZones']:rbox(wet,'#dbe8dd',GREEN,.1)
        for f in state.furniture:
            fx,fy,fw,fd=f['rect'];kind=f['kind']
            fill=P['green'] if kind=='island' else P['darkOak'] if f['room']=='S' and kind=='cabinet' else '#ded1b6'
            if kind=='glass':fill='#afc5ba'
            rbox(f['rect'],fill,MUTED)
            if kind=='bed':
                pillow=[fx+.1,fy+fd-.45,fw-.2,.32] if f['room']=='P' else [fx+.1,fy+.1,.32,fd-.2] if f['room']=='C2' else [fx+fw-.42,fy+.1,.32,fd-.2] if f['room'].startswith('C') else [fx+.1,fy+.1,fw-.2,.32]
                rbox(pillow,PAPER,MUTED,.08)
            if kind in ('bath','basin','wc'):
                C.setFillColor(HexColor(PAPER));C.setStrokeColor(HexColor(MUTED));C.setLineWidth(.1*MM)
                count=2 if 'double' in f['name'].lower() else 1
                for basin in range(count):
                    C.ellipse((x+(fx+basin*fw/count+.06)*scale)*MM,(H-y-(fy+fd-.06)*scale)*MM,(x+(fx+(basin+1)*fw/count-.06)*scale)*MM,(H-y-(fy+.06)*scale)*MM,fill=1,stroke=1)
            if kind=='sofa':
                a,b=((fx+.15,fy+.2),(fx+fw-.15,fy+.2)) if fw>fd else ((fx+fw-.2,fy+.15),(fx+fw-.2,fy+fd-.15))
                line(transform(a),transform(b),MUTED,.09)
    if labels:
        names={'P':'Parents','W':'Dressing','E':'Ensuite','FB':'Family bath','ST':'Linen / plant','C1':'Child 1','C2':'Child 2','C3':'Child 3','FH':'Family hall','G':'Guest bedroom','GS':'Storage','GB':'Guest shower','GL':'Lobby','O':'Office','S':'Library snug','GH':'Guest hall','PA':'Pantry','L':'Laundry','B':'Boot room','H':'Entrance','WC':'WC','OR':'Garden room','GY':'Gym','KL':'Kitchen / dining / living','GH2':'Hall','PL':'Plant'}
        positions={'KL':(7.8,17.85),'P':(2.3,3.9),'S':(20,10.5),'O':(19.7,8.65),'GY':(24.3,17.7),'PL':(24.8,11.25),'B':(20.6,17.7),'E':(6.2,4.15),'FB':(1.9,6.65)}
        for room in model['rooms']:
            if rooms and room['id'] not in rooms:continue
            p=positions.get(room['id'],room['labelPoint']);tx,ty=transform(p);label=names[room['id']]
            fs=2.3 if scale<13 else 2.8
            if room['id'] in ('FH','GH','GH2'):label=room['id']
            width=pdfmetrics.stringWidth(label,'Text',fs*MM)/MM
            rect(tx-width/2-.6,ty-2.2,width+1.2,3.1,PAPER)
            text(tx,ty,label,fs,align='center')
    C.restoreState()

def detail(x,y,w,h,room_ids,bbox,mode='Professional',labels=True):
    a,b,c,d=bbox;scale=min(w/(c-a),h/(d-b));ox=x+(w-(c-a)*scale)/2-a*scale;oy=y+(h-(d-b)*scale)/2-b*scale
    plan(ox,oy,scale,room_ids,labels,mode,False,(ox+a*scale,oy+b*scale,(c-a)*scale,(d-b)*scale))
    return scale

def scale_bar(x,y,scale,length=5):
    rect(x,y,length*scale,.8,INK);text(x,y-2,'0',2.4);text(x+length*scale,y-2,f'{length} m',2.4,align='right')

def elevation(x,y,scale,direction):
    shapes=[]
    def project(vertices,fill,stroke=LINE):
        if direction=='arrival':points=[(x+a*scale,y-h*scale) for a,b,h in vertices];depth=sum(b for a,b,h in vertices)/len(vertices)
        elif direction=='courtyard':points=[(x+(27.15-a)*scale,y-h*scale) for a,b,h in vertices];depth=-sum(b for a,b,h in vertices)/len(vertices)
        else:points=[(x+b*scale,y-h*scale) for a,b,h in vertices];depth=sum(a for a,b,h in vertices)/len(vertices)
        shapes.append((depth,points,fill,stroke))
    for wall in MODEL['walls']+MODEL['roofInfill']:
        a,b,w,d=wall['rect'];lo,hi=wall['bottom'],wall['top']
        if direction=='arrival':vertices=[[a,b+d,lo],[a+w,b+d,lo],[a+w,b+d,hi],[a,b+d,hi]]
        elif direction=='courtyard':vertices=[[a,b,lo],[a+w,b,lo],[a+w,b,hi],[a,b,hi]]
        else:vertices=[[a+w,b,lo],[a+w,b+d,lo],[a+w,b+d,hi],[a+w,b,hi]]
        project(vertices,P[wall['material']],None)
    for a in [0,22.8]:project([[a,12.8,3.7],[a,15.6,MODEL['roofHeights']['main_roof_ridge_m']],[a,18.4,3.7]],P['timber'])
    for r in MODEL['roofSurfaces']:project(r['vertices'],'#a7aaa0' if r['material']=='roof' else '#c5d7ce',None if r['material']=='roof' else GREEN)
    for w in MODEL['windows']:
        a,b,l=w['x'],w['y'],w['length']
        if direction=='arrival' and w['orientation']=='h':b+=.001;project([[a,b,.82],[a+l,b,.82],[a+l,b,2.15],[a,b,2.15]],'#d6e4db',GREEN)
        if direction=='courtyard' and w['orientation']=='h':b-=.001;project([[a,b,.82],[a+l,b,.82],[a+l,b,2.15],[a,b,2.15]],'#d6e4db',GREEN)
        if direction=='west' and w['orientation']=='v':a+=.001;project([[a,b,.82],[a,b+l,.82],[a,b+l,2.15],[a,b,2.15]],'#d6e4db',GREEN)
    for d in MODEL['doors']:
        if not (d['from'] in ['OUT','COURT'] or d['to'] in ['OUT','COURT']):continue
        a,b,l=d['x'],d['y'],d['width'];h=2.6 if d['kind']=='sliding' else 2.15
        if not d['vertical']:
            b+=.19 if direction=='arrival' else -.19
            vertices=[[a,b,0],[a+l,b,0],[a+l,b,h],[a,b,h]]
        else:a+=.19;vertices=[[a,b,0],[a,b+l,0],[a,b+l,h],[a,b,h]]
        project(vertices,'#c5d7ce' if d['kind']=='sliding' else P['oak'],GREEN)
    for _,points,fill,stroke in sorted(shapes,key=lambda item:item[0]):poly(points,fill,stroke,.1)
    line((x-2,y),(x+(18.4 if direction=='west' else 27.15)*scale+2,y),INK,.3)

page('The house brief','The courtyard house','A warm, single-storey family home, with shared life gathered around a sheltered garden.')
image('courtyard',18,65,384,166)
text(18,247,'A home for five. Space to welcome more.',5.4,'Title')
para(18,255,242,'Stone wings, a continuous vaulted shared room, a glazed garden sitting area and a darker library snug. One current proposal brings the rooms, materials and everyday routines together.',3.35)
para(294,246,108,'<b>Edition 02</b><br/>Drawn layout and design intentions.<br/>Roof heights, joinery and products remain proposals.',3.1)
end()

page('01 / The house brief','The life this house makes room for','The starting point is how the household lives: together when wanted, with useful places to retreat.')
plan(22,70,7.2,labels=False,zones=True)
text(22,216,'PRIVATE ROOMS',2.6,'Bold',GREEN);text(95,216,'SHARED LIFE',2.6,'Bold',GOLD);text(164,216,'PRACTICAL SPACES',2.6,'Bold',MUTED)
para(22,227,188,'Two adults and three children, with a guest bedroom and occasional office sofa bed. The peak planning allowance is ten people; visiting children may share beds.',3.4)
notes=[('Together, with choices','Kitchen, dining and living share one vault. The garden room is part of that interior. The library offers a quieter setting for books and films.'),('Space for individual routines','Three equally sized children\'s rooms, a parents\' suite with dressing space, and one office with permanent professional and personal setups.'),('A useful service end','Boot room, separate laundry appliances, pantry and full 4 x 6 m gym. The proposed rear plant room keeps large equipment toward this end.'),('Comfort through the seasons','Wet underfloor heating, active cooling, fresh-air ventilation and external shading. Warm, layered lighting supports the house after dark.')]
for i,(title,body) in enumerate(notes):note(235,74+i*47,165,title,body)
end()

page('02 / Whole-house plan','One furnished plan','Current drawn proposal | Key dimensions in metres | South up, north down, east left, west right')
plan(24,70,10)
line((24,67),(24+27.15*10,67),MUTED,.15)
text(24+27.15*10/2,64,'27.15 m overall',2.7,align='center')
text(301,77,'18.40 m',2.7);para(301,80,20,'overall depth',2.6)
scale_bar(24,262,10)
text(110,262,'Scaled drawing: 1:100 at A3. Use the scale bar.',2.7,color=MUTED)
note(319,78,79,'Shared centre','Living, dining and kitchen form the spine. The garden room opens toward the court.')
note(319,132,79,'Two quieter wings','Family bedrooms on the left. Guests, office and library on the right.')
note(319,185,79,'The latest additions','Library joinery, two office setups and rear plant room are included.')
para(319,235,79,'Plant / linen provision remains conditional. Furniture shows size allowances, not selected products.',2.9)
end()

page('02 / Room schedule','The size of the house','Clear room areas are separate from the internal envelope and the external footprint. All three use the existing model convention.')
rooms=MODEL['rooms']
for col,subset in enumerate([rooms[:13],rooms[13:]]):
    x=18+col*198
    text(x,68,'ROOM',2.6,'Bold');text(x+183,68,'m²',2.7,'Bold',align='right')
    for i,r in enumerate(subset):
        yy=77+i*12.4
        text(x,yy,r['name'],3.1,'Bold');text(x+183,yy,f"{r['area']:.2f}",3.1,align='right')
        dims=r['dimensions']
        if r['id']=='KL':dims='Stepped plan; main clear depth 4.90 m'
        if r['id']=='L':dims='L-shape; 4.58 x 3.15 m envelope'
        para(x,yy+2,173,escape(dims),2.65)
        line((x,yy+8),(x+183,yy+8),LINE,.1)
for x,value,label in [(18,MODEL['metadata']['giaM2'],'INTERNAL ENVELOPE'),(150,MODEL['metadata']['externalFootprintM2'],'EXTERNAL FOOTPRINT'),(282,MODEL['metadata']['clearRoomM2'],'SUM OF CLEAR ROOMS')]:
    text(x,251,f'{value:.2f} m²',6.6,'Title');text(x,259,label,2.6,'Bold',MUTED)
para(18,266,383,'The internal envelope includes partitions. The footprint includes external walls. Courtyard, carport, external works and plot area are excluded; these are not cost or valuation measurements.',2.8)
end()

page('03 / Outside and roof','The house from three sides','Stone wings and a timber shared block. Openings follow the current plan; colour and roof edges show the intended character.')
text(20,70,'ARRIVAL / NORTH',2.8,'Bold');elevation(20,128,6.5,'arrival')
text(218,70,'COURTYARD / SOUTH',2.8,'Bold');elevation(218,128,6.5,'courtyard')
text(20,153,'GARDEN / WEST',2.8,'Bold');elevation(20,213,8.4,'west')
image('arrival',218,145,184,102)
para(20,230,177,'The rear plant room continues the gym volume. Its garden-facing location avoids the declined arrival projection. The library side window is replaced by a rooflight.',3.1)
para(218,254,184,'Elevation silhouettes and perspective use the same roof heights and footprint. Low-roof falls, edge profiles and material samples remain to develop.',2.8)
end()

page('03 / Outside and roof','A high shared roof and lower wings','Three rooflights over the main room and two along the family hall add daylight openings to the retained library rooflight.')
ox,oy,s=23,77,8
for surface in MODEL['roofSurfaces']:
    poly([(ox+x*s,oy+y*s) for x,y,h in surface['vertices']], '#dbe8e0' if surface['material']=='glass' else '#bcbcae',GREEN if surface['material']=='glass' else None,.2)
for label,x,y in [('Family wing',4.1,5),('Guest / library',19.5,5),('Shared vault',11.4,14.3),('Gym + plant',25,14)]:text(ox+x*s,oy+y*s,label,3,align='center')
line((ox,oy+15.6*s),(ox+22.8*s,oy+15.6*s),GREEN,.45)
text(ox+14.2*s,oy+11.4*s,'GLASS',2.3,'Bold',GREEN,'center')
line((ox+19.2*s,oy+10.5*s),(250,175),GOLD,.25)
text(250,181,'Library rooflight',2.8,'Bold',GOLD)
text(ox+4.1*s,oy+8.5*s,'HALL',2.2,'Bold',GREEN,'center')
text(ox+8.35*s,oy+18.9*s,'THREE MAIN-SPACE ROOFLIGHTS',2.4,'Bold',GREEN,'center')
image('garden',267,70,135,94)
note(267,190,133,'Study heights','Main roof edge 3.70 m; ridge 5.32 m. Lower roof envelopes 3.20 m. These carry forward the height study; they are not fixed construction dimensions.')
para(23,246,221,'Proposed plan openings: three at 0.90 x 1.20 m over living, dining and kitchen; two at 0.65 x 0.90 m along the family hall. The library retains its 1.10 m square opening. Product sizes, shading and roof details remain open.',3.1)
para(267,250,133,'Keep the courtyard roof slope clear for the PV study. Confirm the actual orientation, solar exposure and shading once a plot is known.',2.9)
end()

page('04 / Space and height','How the house changes in section','The shared room has a continuous vault; private and service rooms have lower ceilings. Vertical dimensions remain study allowances.')
text(22,72,'A / THROUGH THE FAMILY WING AND SHARED ROOM',2.8,'Bold')
ox,base,s=23,139,13
pts=lambda values:[(ox+x*s,base-h*s) for x,h in values]
poly(pts([(0,3.2),(12.8,3.2),(12.8,2.6),(0,2.6)]),'#d8d5c8',INK)
poly(pts([(12.8,3.7),(15.6,5.3166),(18.4,3.7),(18.05,3.5),(15.6,4.9145),(13.15,3.5)]),'#b4b5a8',INK)
line((ox,base),(ox+18.4*s,base),INK,.4)
for a,b in [(0,.35),(4.35,4.47),(7.15,7.27),(8.69,8.81),(13.03,13.15),(18.05,18.4)]:
    height=3.5 if a>=13 else 2.6
    rect(ox+a*s,base-height*s,(b-a)*s,height*s,INK)
rect(ox+12.8*s,base-3.7*s,.23*s,.5*s,P['timber'],INK)
for x,label in [(1.8,'Private rooms'),(7.4,'Family wing'),(15.6,'Shared room')]:text(ox+x*s,base+7,label,3,align='center')
line((ox+15.6*s,base-4.9145*s),(260,83),GOLD,.2)
para(286,80,114,'<b>Continuous shared vault</b><br/>The study ceiling rises from 3.50 m at the sides to 4.91 m at the centre. Final heights depend on roof and structure.',3.2)
text(22,169,'B / THROUGH THE GARDEN ROOM INTO THE SHARED VAULT',2.8,'Bold')
ox,base,s=23,254,14
pts=lambda values:[(ox+(x-9.3)*s,base-h*s) for x,h in values]
poly(pts([(9.3,2.85),(12.8,3.45),(12.8,3.50),(9.3,2.90)]),'#c9dbd1',GREEN)
poly(pts([(12.8,3.7),(15.6,5.3166),(18.4,3.7),(18.05,3.5),(15.6,4.9145),(13.15,3.5)]),'#b4b5a8',INK)
line((23,base),(23+9.1*s,base),INK,.4)
rect(23+(18.05-9.3)*s,base-3.5*s,.35*s,3.5*s,INK)
rect(23+(12.8-9.3)*s,base-3.7*s,.14*s,.25*s,P['timber'],INK)
line((23,base),(23,base-2.85*s),GREEN,.8)
rect(23+(13.08-9.3)*s,base-3.5*s,.14*s,.4*s,P['ivory'],INK)
text(48,base+8,'Glazed sitting area',3,align='center');text(111,base+8,'Shared room',3,align='center')
para(200,188,200,'<b>A broad, plain opening</b><br/>The garden room continues the shared floor and palette beneath a shallow glazed roof. A 3.10 m opening head is the working intention.',3.2)
para(200,228,200,'The section establishes spatial character. It does not demonstrate a post-free structure, roof build-up or weatherproof junction. Shading and high vents need to fit the selected system.',3.1)
end()

page('05 / Interior character','Warm, quiet and naturally textured','The shared space is light and warm: ivory, forest green, honey oak and muted bronze, with one dining chandelier.')
image('living',18,65,260,164)
note(298,78,104,'A continuous room','The lounge, dining and kitchen share one vault. Three modest rooflights punctuate its arrival-side slope, with openings modelled through the ceiling.')
note(298,153,104,'Materials to carry forward','Warm ivory cabinetry, a definite forest-green island, creamy worktops and warm hard flooring. The log burner is a reserved location to develop.')
for i,(col,name,desc) in enumerate([(P['ivory'],'Warm ivory','Painted kitchen'),(P['green'],'Forest green','Island'),(P['oak'],'Honey oak','Furniture / joinery'),(P['bronze'],'Muted bronze','Lights / details'),(P['floor'],'Warm stone tone','Floor / worktop')]):chip(18+i*78,239,69,col,name,desc)
end()

page('05 / Interior character','A darker room for books and films','The library snug has a distinct character within the house: dark timber, framed storage, full-height books and warm reading light.')
image('library',18,65,258,169)
detail(293,74,108,72,['S'],(17.7,9.3,22.8,12.18),labels=False)
text(293,155,'4.58 x 2.60 m',4,'Title')
para(293,165,108,'The library wall runs 4.58 m, with a 2.25 m return and a central TV recess. The 2.30 m sofa retains a nominal 0.80 m passage to the return.',3.15)
para(293,222,108,'The rooflight replaces the covered side window. Daylight quality, blackout and the detailed joinery remain to review.',3.05)
para(18,246,257,'Dark timber is the intended atmosphere. The model makes the bookcase and TV relationship visible; mouldings, book loads, fittings and the precise finish remain to select.',3.25)
end()

page('06 / Living in the house','Bedrooms that support everyday life','A settled parents\' suite and three equally sized children\'s rooms. Furniture represents the agreed size allowances.')
detail(20,71,197,120,['P','W','E'],(0,0,8.2,4.47))
detail(256,71,112,155,['C1'],(4.7,8.69,8.2,13.15))
text(23,209,'Parents\' suite / selected Option A',4.2,'Title')
para(23,219,194,'A 180 x 200 cm super king, dressing room and ensuite with two basins and a generous shower. The bath alternative was declined to protect dressing space.',3.25)
text(242,238,'Children / 12.79 m² each',4.2,'Title')
para(242,248,160,'Each room allows a small double, 1.80 m wardrobe and 1.40 m desk. The layouts mirror where needed; actual bed frames and window use need checking.',3.1)
para(23,257,194,'Bedroom finishes can stay warm and calm, with personal colour and textiles. No full bedroom finish scheme has been selected.',2.9)
end()

page('06 / Living in the house','Bathing without unnecessary compromises','The family bathroom keeps a bath and separate shower. The parents\' ensuite gives priority to two basins and a generous shower.')
for x,title,room,bbox in [(20,'FAMILY BATHROOM','FB',(0.2,4.35,3.5,7.27)),(152,'PARENTS\' ENSUITE','E',(4.55,2.45,7.97,4.47)),(284,'GUEST SHOWER','GB',(20.23,3.65,22.57,6.29))]:
    text(x,73,title,2.9,'Bold');detail(x,86,116,112,[room],bbox,labels=False)
note(20,216,115,'Bath + shower + two basins','A 1.70 m bath, 1.20 x 1.20 m shower and double vanity. The family bathroom door has moved to clear the vanity.')
note(152,216,115,'Selected suite arrangement','Two basins and a 1.10 x 1.78 m shower zone. A bath is intentionally absent from this option.')
note(284,216,115,'Independent guest use','Separate guest shower room with a 1.20 x 1.00 m shower, basin and WC. The guest lobby separates storage and washing.')
end()

page('06 / Living in the house','Working here, and welcoming guests','One continuous L-shaped worktop connects two permanent setups. The 50 cm corner gap is closed; the sofa bed still opens.')
text(20,73,'OFFICE / WORKING',2.8,'Bold');detail(20,86,181,113,['O'],(17.7,6.17,22.57,9.46),labels=False)
text(221,73,'OFFICE / OVERNIGHT',2.8,'Bold');detail(221,86,181,113,['O'],(17.7,6.17,22.57,9.46),mode='Night',labels=False)
note(20,219,177,'A continuous L-shaped desk','A 1.60 m arm meets a 2.30 m return, both 0.75 m deep. The return closes the former corner gap. Two setups share one chair.')
note(221,219,181,'An occasional extra bedroom','Both sleepers have a connected route at the foot of the bed, with a nominal 0.78 m gap. The chair parks at the personal desk; the sofa mechanism remains to select.')
para(20,265,382,'Guest capacity uses the separate guest double, occasional office bed and visiting children sharing beds. It is not five additional adult beds. Dining currently assumes eight at the table plus two at the island.',2.9)
end()

page('06 / Living in the house','The practical rooms earn their space','Arrival, coats, food storage and laundry have places of their own, close to the kitchen and the gym.')
detail(20,72,239,153,['H','B','L','PA','WC'],(13.76,12.06,22.8,18.4))
note(282,80,116,'Arrival and boot room','Visitor coats and a keys ledge at the entrance. Family coats, bags, bench and shoe bays in the boot room.')
note(282,140,116,'A separate laundry','Side-by-side washer and dryer, sink, sorting, folding and modest air-drying provision. The direct kitchen door is retained.')
note(282,212,116,'Pantry and gym','Useful pantry shelving sits between kitchen and entrance. The full 24 m² gym remains beside the boot room.')
para(20,241,239,'The rear plant room is intended to protect the laundry and gym. Its equipment layout remains a space reservation. Final equipment, maintenance access and the family linen cupboard are still linked decisions.',3.2)
end()

page('07 / Garden and comfort','A courtyard for daytime and evening','Dining, sitting and planted edges support different uses, with warm light when the courtyard is occupied.')
image('courtyard',18,65,187,117);image('evening-court',215,65,187,117)
text(18,197,'DAYLIGHT',2.8,'Bold');para(18,204,184,'The selected layout has an outdoor dining area and a separate sitting pad. Keep the approach routes clear and maintain privacy at bedroom windows.',3.3)
text(215,197,'AFTER DARK',2.8,'Bold');para(215,204,184,'Warm wall lighting and four bronze pillars support the occupied courtyard. Indoors, lamps, concealed light and the dining chandelier create separate scenes.',3.3)
para(18,250,382,'The site remains illustrative. A real plot will establish arrival, parking / carport, boundaries, wider garden use and maintenance access. The views show atmosphere, not measured daylight or lighting performance.',3.1)
end()

page('07 / Garden and comfort','Comfort is part of the house brief','Wet underfloor heating is confirmed. Cooling, ventilation and hot water need a coordinated arrangement that respects the architecture.')
plan(21,73,7.4,labels=False,zones=True)
for label,point in [('FAMILY',(4.2,6)),('GUEST / SERVICE',(20,6)),('SHARED',(9,16)),('PLANT',(25,10.5))]:
    text(21+point[0]*7.4,73+point[1]*7.4,label,2.65,'Bold',GREEN,'center')
para(21,229,205,'The rear plant location is the current direction. Two local ventilation units are recommended for further design, but are not selected. The existing family-side plant / linen reservation is retained until the package is resolved.',3.2)
for i,(title,body) in enumerate([('Winter warmth','Wet underfloor heating, with the proposed heat-pump and hot-water arrangement to develop.'),('Summer comfort','Active cooling in all bedrooms, shared / garden room, office, library and gym. Solar is intended to contribute; battery and grid use remain open.'),('Fresh air and glass','Coordinate rooflight blinds, glass and opening controls with cooling and ventilation. Retain external garden-roof shading and high vents.'),('Hot water and storage','Design for two simultaneous high-flow rain showers. Pipe delays, storage and maintenance access still need resolution.')]):note(248,76+i*48,152,title,body)
end()

page('08 / Decisions still open','What to settle next','This book is a coherent working proposal. The remaining choices can now be considered against the whole house.')
items=[('01','Exterior form','Review the low roof edges, stone / timber distribution and rear plant roof together. Review the proposed main-space and family-hall rooflights with shading, solar panels and the actual site orientation.'),('02','Services that affect rooms','Resolve ventilation without an unwanted visible band across the vault. Confirm the family cupboard / linen trade-off, hot-water distribution and the plant maintenance space.'),('03','Site and budget','Use the actual plot to settle orientation, arrival, parking, privacy and wider garden. A broad budget should guide the next level of refinement.'),('04','Materials and room character','Compare flooring and worktop samples; decide how timber should weather. Develop bedrooms and bathrooms without treating the shared-room palette as a finished scheme for every room.'),('05','Products and everyday use','Check the actual sofa bed, beds, appliances, chairs, wardrobe fronts and gym equipment against the drawn allowances before fixing joinery.')]
for i,(number,title,body) in enumerate(items):
    yy=76+i*35
    text(19,yy,number,5.5,'Title',GOLD);text(39,yy,title,3.7,'Bold');para(39,yy+5,359,body,3.05)
line((18,250),(402,250))
para(18,258,236,'<b>One current set.</b> Layout from concepts 22-25, with the L-desk and rooflight proposal of edition 02; roof direction from 06B / 07B; courtyard and lighting from 09 / 10; services updated through 26 / 27. Earlier alternatives stay in the archive.',2.75)
para(274,258,128,'<b>Companion model</b><br/>Open the companion viewer and choose Whole house, Arrival, Courtyard or an interior. Roof and office-use controls make the main relationships inspectable.',2.75)
end()
assert PAGE==16
C.save()
manifest={'revision':MODEL['revision'],'pages':PAGE,'model_sha256':hashlib.sha256((ROOT/'viewer/model.json').read_bytes()).hexdigest(),'source_layout':'concept-24 snapshot / concept-25 whole-house proposal','book':str(OUT.relative_to(ROOT)),'views':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(VIEWS.glob('*.png'))},'limitations':['Concept design, not construction documentation','Roof and joinery heights are illustrative study dimensions','Plot and budget are not defined','Ventilation recommendation remains unselected']}
(ROOT/'output/design/design-book-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Created {OUT}: {PAGE} pages')
