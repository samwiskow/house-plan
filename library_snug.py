"""Concept 24: a library snug with integrated television provision."""
import copy
import hashlib
import json
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,BASE=load_model()
OFFICE=json.loads((ROOT/'output/pdf/concept-23-study-check.json').read_text())
assert hashlib.sha256((ROOT/'two_workspace_office.py').read_bytes()).hexdigest()==OFFICE['source_sha256']
assert hashlib.sha256((ROOT/'garden_plant_study.py').read_bytes()).hexdigest()==OFFICE['garden_source_sha256']
state=OFFICE['model'];m.rooms=[m.Room(**r) for r in state['rooms']];m.R={r.id:r for r in m.rooms}
m.doors=[m.Door(**d) for d in state['doors']];m.windows=state['windows'];m.OUTLINE=state['outline'];m.INNER=state['inner']
ITEMS=[('Full-height library / TV wall',(17.87,9.46,4.58,.35),'cabinet'),
 ('Full-height library return',(22.15,9.81,.30,2.25),'cabinet'),
 ('Three-seat sofa allowance',(19.05,11.11,2.30,.90),'sofa'),
 ('Movable upholstered footstool',(20.35,10.56,.50,.50),'table'),
 ('Sofa side table',(18.55,11.51,.40,.40),'table')]
ROUTES={'Snug rooflight control':[(19.75,10.66),(18.55,10.66),(18.55,10.25)],
 'Snug main bookcase approach':[(18.55,10.66),(18.55,10.20),(21.75,10.20)],
 'Snug return bookcase approach':[(21.75,10.20),(21.75,11.55)]}
STATES={}
for mode,old in {**OFFICE['work_states'],'Night':OFFICE['night_state']}.items():
    m.furniture=copy.deepcopy([f for f in old['furniture'] if f['room']!='S'])
    for name,r,kind in ITEMS:m.furn('S',name,*r,kind)
    m.routes=copy.deepcopy(old['routes']);m.routes.update(ROUTES)
    issues=m.verify();assert not issues,(mode,issues)
    STATES[mode]={'furniture':copy.deepcopy(m.furniture),'routes':copy.deepcopy(m.routes),'issues':issues}
m.furniture=STATES['Professional']['furniture'];m.routes=STATES['Professional']['routes']
ROOFLIGHT=OFFICE['snug_rooflight_reservation_m']
WOOD='#564032';PANEL='#70533d';BOOKS=['#74806b','#8c6350','#c5b18b','#58656b','#8a805e','#aa9075']
OUT=ROOT/'output/pdf';PDF=OUT/'concept-24-library-snug.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 24 - antique library snug')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.75,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 24 / LIBRARY SNUG',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'DESIGN PROPOSAL | Joinery height, rooflight, equipment ventilation, lighting and acoustic construction remain to detail. Print at 100%.',2.3,fill='muted')
    text(406,287,f'{n} / 3',2.6,align='right',fill='muted')
header(1,'A small library with a comfortable place to watch TV','Snug plan 1:25 at A3 | 4.58 x 2.60 m clear | Books take the main wall and the former window wall')
p=m.Plan(30-17.87*40,75-9.46*40,40)
m.c.saveState();clip=m.c.beginPath();clip.rect(16*m.mm,(297-197)*m.mm,224*m.mm,139*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False);m.c.restoreState()
for _,r,kind in ITEMS:
    if kind=='cabinet':p.rect(*r,WOOD,'ink',.15)
p.rect(*ROOFLIGHT,None,'amber',.3);p.text(19.20,10.48,'ROOFLIGHT ABOVE',2.2,fill='amber')
p.text(20.16,9.7,'BOOKS / TV RECESS / BOOKS',2.2,fill='paper')
p.text(20.20,11.70,'2.30 m SOFA',2.6)
for points in ROUTES.values():
    for a,b in zip(points,points[1:]):p.line(a,b,'green',.25,[1,1])
p.dimension((17.87,9.46),(22.45,9.46),-.40,'4.58 m full-height library wall')
note(256,55,'THE LIBRARY CHARACTER',[
 'Dark timber, framed cupboards and a modest cornice.',
 'Full-height shelves with a central television recess.',
 'Books continue onto the wall beside the plant room.',
 'A soft sofa, footstool and warm reading light.' ])
note(256,104,'FIT WITHIN THE EXISTING ROOM',[
 'Main bookcase depth: 0.35 m.',
 'Return bookcase depth: 0.30 m.',
 'Sofa shifts 0.30 m toward the entrance side.',
 '0.80 m remains between sofa end and return shelves.',
 '0.75 m between footstool and main bookcase.' ])
note(256,160,'ROOFLIGHT AND PLANT ROOM',[
 'Retain the 1.10 m-square rooflight reservation.',
 'Provide controllable shade for books and television.',
 'Check glare, daylight, solar gain and roof structure.',
 'The plant wall needs its own acoustic construction;',
 'bookcases are not a substitute for sound isolation.' ])
note(25,224,'MEASURED CHECK',[
 f'All {len(m.routes)} sampled routes pass in both office work modes and the overnight mode, including approaches to both bookcase runs.',
 'The snug door, room size and garden-side plant proposal are retained. The side table moves away from the return shelves.',
 'Shelf depth, cornice and cupboard projections must stay within these footprints. Upper-shelf access remains to plan.' ])
m.c.showPage()

def elevation(x,y,widths,television=False):
    scale=40;total=sum(widths);height=2.60
    m.rect(x,y,total*scale,height*scale,WOOD,'ink',.2)
    off=0
    for i,w in enumerate(widths):
        bx=x+off*scale;bw=w*scale
        m.rect(bx+2,y+86,bw-4,14,PANEL,'ink',.18)
        m.rect(bx+4,y+88,bw-8,10,None,'#aa8a61',.12)
        for z in [.50,.88,1.26,1.64,2.02,2.40]:
            if television and i==2 and z<1.64:continue
            sy=y+(height-z)*scale
            m.rect(bx+1.5,sy,bw-3,1.0,'#ae8f66',None)
            if z==2.40:continue
            for j in range(int((bw-5)/2.5)):
                bh=8+(j*3+i)%5
                m.rect(bx+2.5+j*2.5,sy-bh,1.8,bh,BOOKS[(i+j)%len(BOOKS)],None)
        off+=w
    if television:
        bx=x+sum(widths[:2])*scale
        m.rect(bx+2,y+(height-1.50)*scale,(widths[2]*scale)-4,.94*scale,'#302c28',None)
        m.rect(bx+(widths[2]-1.218)*scale/2,y+(height-1.3425)*scale,1.218*scale,.685*scale,'#202423','#a79478',.2)
        text(bx+widths[2]*scale/2,y+65,'TV ALLOWANCE',2.2,align='center',fill='#bfb6a5')
    m.rect(x-1,y-1,total*scale+2,2.4,PANEL,'ink',.15)
    m.rect(x,y+101,total*scale,3,PANEL,'ink',.15)

header(2,'The television sits within the books','South wall elevation 1:25 at A3 | Indicative 2.60 m joinery height, subject to actual ceiling and roof build-up')
elevation(28,79,[.80,.80,1.38,.80,.80],True)
m.line(28,69,211.2,69,'muted',.2);text(119.6,65,'4.58 m overall',2.7,align='center')
text(119.6,194,'0.80 / 0.80 / 1.38 / 0.80 / 0.80 m nominal bays',2.6,align='center')
note(253,55,'JOINERY LANGUAGE',[
 'Walnut-stained oak is a proposed material direction.',
 'Framed lower cupboards, slim uprights and a cornice.',
 'Adjustable shelves above; concealed storage below.',
 'Shelf spans / fixings designed for the actual book load.' ])
note(253,110,'TELEVISION PROVISION',[
 'Indicative 55-inch, 16:9 screen within a 1.38 m bay.',
 'Screen centre approximately 1.00 m above the floor.',
 'TV size, viewing height and audio equipment to select.',
 'Provide power, data, ventilation and removable access.',
 'Final clear opening depends on the joinery members.' ])
note(253,171,'LIGHTING',[
 'Dimmable reading lights near each end of the sofa.',
 'Optional small bronze picture lights on the bookcase.',
 'Warm light and separate controls for reading / TV.',
 'Check lamp positions against reflections on the screen.' ])
note(28,227,'ANTIQUE CHARACTER WITHOUT FILLING THE FLOOR',[
 'The detail is concentrated in the timber joinery, books, light fittings and upholstery. Keep the middle of this narrow room calm.',
 'Choose a compact movable step for occasional upper-shelf access; store it in a lower cupboard and keep it out of the normal routes.' ])
m.c.showPage()
header(3,'A return of books gives the room its library feeling','West / former-window wall elevation 1:25 at A3 | Joinery and material direction')
elevation(35,77,[.75,.75,.75])
text(80,193,'2.25 m return beyond the main bookcase',2.6,align='center')
note(159,55,'A QUIET, WARM PALETTE',[
 'Dark stained timber and muted bronze fittings.',
 'Warm cream or subdued moss on the remaining walls.',
 'Textured wool upholstery and a comfortable footstool.',
 'Use real material samples together before specifying.' ])
for i,(label,colour) in enumerate([('TIMBER',WOOD),('MOSS','#737a63'),('CREAM','#e7dfca'),('BRONZE','#96764e')]):
    m.rect(159+i*49,104,38,24,colour,None);text(159+i*49,134,label,2.4,fill='muted')
note(159,153,'COORDINATE BEFORE ORDERING JOINERY',[
 'Ceiling height and the meeting of both bookcase runs.',
 'Rooflight structure, shade and opening / cleaning access.',
 'Ventilation and any cooling outlet clear of the shelves.',
 'Plant noise / vibration, wall fixings and service penetrations.',
 'TV cables, equipment heat and access to sockets.' ])
note(25,231,'BRIEF UPDATE',[
 'The snug is now a library-led room with television provision. This supersedes the earlier low-storage / TV-led furnishing study.',
 'No supplier, timber finish, TV, rooflight or light fitting has been selected; the drawings reserve space and establish the design direction.' ])
m.c.showPage();m.c.save()
(OUT/'concept-24-study-check.json').write_text(json.dumps({'status':'Library snug proposal with TV provision',
 'model':state,'states':STATES,'furniture':m.furniture,'routes':m.routes,'snug_items':ITEMS,
 'snug_rooflight_reservation_m':ROOFLIGHT,'joinery_height_m':2.60,'office_source_sha256':OFFICE['source_sha256'],
 'garden_source_sha256':OFFICE['garden_source_sha256'],'base_sources':BASE['model_sources'],
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'issues':[]},indent=2)+'\n')
print(PDF);print('Library routes pass in all three office states.')
