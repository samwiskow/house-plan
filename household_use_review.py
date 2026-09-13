"""Concept 19: occupied-use scenarios, with explicit spatial failures."""
import copy
import json
from math import ceil, hypot, cos, sin, pi
from pathlib import Path
from development_model import load_model

ROOT=Path(__file__).parent
m,DATA=load_model();BASE=copy.deepcopy(m.furniture)

def check_route(points,extra=(),width=.70):
    radius=width/2
    for a,b in zip(points,points[1:]):
        count=max(1,ceil(hypot(b[0]-a[0],b[1]-a[1])/.025))
        for i in range(count+1):
            p=(a[0]+i/count*(b[0]-a[0]),a[1]+i/count*(b[1]-a[1]))
            for name,r in [(f['name'],f['rect']) for f in BASE]+list(extra):
                x,y,w,h=r;dx=max(x-p[0],0,p[0]-x-w);dy=max(y-p[1],0,p[1]-y-h)
                if dx*dx+dy*dy<radius*radius-1e-9:return {'clear':False,'obstacle':name,'point':p}
            for k in range(16):
                q=(p[0]+radius*cos(k*pi/8),p[1]+radius*sin(k*pi/8))
                if not any(m.inside(q,r.poly) for r in m.rooms) and not any(m.inside(q,d.opening) for d in m.doors):
                    return {'clear':False,'obstacle':'Wall / opening','point':p}
    return {'clear':True}

SCENARIOS=[
 {'id':'L1','name':'Laundry / both machine doors open','route':m.routes['Utility to washer'],'extra':[('Washer door',(21.15,12.23,.55,.65)),('Dryer door',(21.15,12.88,.55,.65))],'expect':True},
 {'id':'L2','name':'Laundry / basket left in the aisle','route':m.routes['Boot to laundry'],'extra':[('Laundry basket',(20.1,14.65,.65,.45))],'expect':False},
 {'id':'L3','name':'Laundry / basket stored under counter','route':m.routes['Boot to laundry'],'extra':[],'expect':True},
 {'id':'P1','name':'Shopping / pantry drawer open','route':m.routes['Boot to pantry'],'extra':[('Open pantry drawer',(14,16.05,2.35,.50))],'expect':False},
 {'id':'P2','name':'Shopping / use direct entrance-kitchen route','route':m.routes['Arrival to kitchen'],'extra':[('Open pantry drawer',(14,16.05,2.35,.50))],'expect':True},
 {'id':'K1','name':'Cooking / dishwasher open','route':m.routes['Dining to cooking aisle'],'extra':[('Dishwasher door',(11.6,16.80,.60,.65))],'expect':False},
 {'id':'K2','name':'Cooking / pass on the courtyard side','route':[(10.2,13.85),(14.85,13.85)],'extra':[('Dishwasher door',(11.6,16.80,.60,.65))],'expect':True},
 {'id':'B1','name':'School morning / occupied boot bench','route':m.routes['Boot to gym'],'extra':[('Seated person / knees',(19.4,16.8,.6,.6))],'expect':False},
 {'id':'B2','name':'School morning / pass on gym side','route':[(21.65,17.6),(21.65,16.65),(24.0,16.65)],'extra':[('Seated person / knees',(19.4,16.8,.6,.6))],'expect':True},
 {'id':'D1','name':'Ten at one table / courtyard-end chair','route':[(6.1,13.85),(9.7,13.85)],'extra':[('Extra end chair',(8.1,13.6,.5,.5))],'expect':False},
 {'id':'D2','name':'Ten at one table / rear-end chair','route':m.routes['Rear of dining'],'extra':[('Extra end chair',(8.1,17.3,.5,.5))],'expect':False},
 {'id':'F1','name':'Bath assistance / adult at bath edge','route':m.routes['Family bathroom bath'],'extra':[('Adult helping at bath',(1.25,5.8,.6,.6))],'expect':False},
]
for scenario in SCENARIOS:
    assert check_route(scenario['route'])['clear'],scenario['id']
    scenario['result']=check_route(scenario['route'],scenario['extra'])
    assert scenario['result']['clear']==scenario['expect'],scenario
assert check_route([(0,0),(1,0)])['clear'] is False
assert check_route(m.routes['Boot to laundry'],[('Blocking object',(20.55,14.4,.7,.7))])['clear'] is False
OUT=ROOT/'output/pdf';PDF=OUT/'concept-19-everyday-use-review.pdf'
m.c=m.canvas.Canvas(str(PDF),pagesize=(420*m.mm,297*m.mm));m.c.setTitle('Concept 19 - everyday use review')
def text(x,y,t,size=3,bold=False,**kw):m.text(x,y,t,size,'Helvetica-Bold' if bold else 'Helvetica',**kw)
def note(x,y,title,lines):
    text(x,y,title,3.3,True);m.paragraph(x,y+8,lines,size=2.8,step=5.1)
def header(n,title,sub):
    m.rect(0,0,420,297,'paper',None);text(14,12,'COURTYARD HOUSE / CONCEPT 19 / EVERYDAY USE',2.7,fill='muted')
    text(14,23,title,6,True);text(14,31,sub,2.75,fill='muted');m.line(14,37,406,37,'line',.25)
    m.line(14,280,406,280,'line',.25);text(14,287,'USE REVIEW | Synthetic occupied-use reservations. Failed routes are findings, not adopted furniture. No human-use or accessibility certification.',2.3,fill='muted')
    text(406,287,f'{n} / 3',2.6,align='right',fill='muted')
def crop(p,r):
    x,y,w,h=r;m.c.saveState();clip=m.c.beginPath();clip.rect(x*m.mm,(297-y-h)*m.mm,w*m.mm,h*m.mm);m.c.clipPath(clip,stroke=0);p.draw(labels=False);m.c.restoreState()
def draw_case(p,id):
    s=next(s for s in SCENARIOS if s['id']==id)
    for name,r in s['extra']:
        p.rect(*r,None,'amber',.5);x,y,w,h=r;p.text(x+w/2,y+h/2,id,2.7,fill='amber')
header(1,'The rooms fit; some activities need their own space','Review against the consolidated daytime furniture and the concept 18 night arrangement')
rows=[
 ('Laundry','Open machine doors pass; an aisle basket blocks the route.','Store baskets under the folding run; retain working floor.'),
 ('Shopping','An open pantry drawer blocks the through-pantry route.','Use the direct hall-to-kitchen route while drawers are open.'),
 ('Cooking','An open dishwasher obstructs the sampled cooking route.','Keep passing traffic on the courtyard side of the island.'),
 ('School morning','A person at the boot bench obstructs the original gym route.','A gym-side bypass passes; test the family together at full scale.'),
 ('Meal for ten','Adding end chairs blocks front and rear dining routes.','Current table has eight chairs; two island places are separate.'),
 ('Bath time','A helping adult occupies the tested bath approach.','Sequence bathing / basin use; no multi-person bathroom fit claimed.'),
 ('Overnight guests','Two guest-bed places + two office places + one shared child bed.','Office work pauses; far-side sofa-bed sleeper crosses the mattress.'),
]
for i,(name,finding,action) in enumerate(rows):
    y=55+i*27;m.line(20,y+21,400,y+21,'line',.15);text(20,y,name.upper(),3.1,True);text(83,y,finding,2.8);text(83,y+8,action,2.8,fill='muted')
text(20,259,'Most important layout decision: is a single table seating ten a requirement, or is eight plus island seating acceptable?',3.2,True)
m.c.showPage()
header(2,'Protect the laundry aisle and the route past the boot bench','Service-end plan 1:35 at A3 | Amber outlines are temporary objects / users, shown together for location only')
p=m.Plan(26-17.5*(1000/35),59-12.05*(1000/35),1000/35);crop(p,(18,49,169,185))
for id in ['L1','L2','B1']:draw_case(p,id)
for a,b in zip(SCENARIOS[8]['route'],SCENARIOS[8]['route'][1:]):p.line(a,b,'green',.35,[1,1])
note(225,55,'LAUNDRY',[
 'L1: each machine door projects 0.55 m into the aisle.',
 'A 0.70 m sampled approach remains clear behind them.',
 'L2: a 0.65 x 0.45 m basket obstructs the boot-to-laundry route.',
 'L3: removing the basket restores the sampled route.',
 'Basket storage under the counter is an operating proposal.' ])
note(225,116,'BOOT ROOM',[
 'B1: a 0.60 m-square seated-person / knee reservation.',
 'The original route to the gym passes too close to it.',
 'Green: the alternative via the gym side clears the reservation.',
 'This is a single moving person, not five people getting ready.',
 'Coats, school bags and opening cupboard fronts need a mock-up.' ])
note(225,178,'LIMITS OF THESE CHECKS',[
 'Existing joinery and gym equipment are retained.',
 'Body and basket sizes are scenario inputs, not measured users.',
 'The routes sample a 0.70 m-wide moving envelope.',
 'Door timing, bending, lifting and simultaneous passing are not simulated.',
 'A wider basket-carrying envelope needs separate testing.' ])
note(25,246,'DESIGN IMPLICATION',[
 'The full laundry remains valuable. Option A plant would take away the counter / storage that helps keep this floor clear.' ])
m.c.showPage()
header(3,'Ten dining seats need a layout decision','Kitchen / dining plan 1:40 at A3 | Additional end chairs and open dishwasher shown as temporary conflict tests')
p=m.Plan(28-6.3*25,67-13.15*25,25);crop(p,(17,52,228,137))
for id in ['D1','D2','K1']:draw_case(p,id)
for a,b in zip(SCENARIOS[6]['route'],SCENARIOS[6]['route'][1:]):p.line(a,b,'green',.35,[1,1])
p.text(8.35,15.6,'8 SEATS',2.6);p.text(12.25,15.6,'ISLAND',2.6)
note(268,55,'D1 / D2: END CHAIRS',[
 'Current dining arrangement has eight seats.',
 'Two extra 0.50 m chairs obstruct front / rear cross-routes.',
 'There is no verified ten-place table arrangement yet.',
 'Eight at the table plus two at the island is possible',
 'as separate seating, not ten dining together.' ])
note(268,113,'K1: DISHWASHER',[
 '0.65 m open-door projection tested.',
 'The sampled cooking-aisle route is obstructed.',
 'Green: courtyard-side passing route remains clear.',
 'A person unloading adds another occupied area.',
 'Selected appliance hinges and doors still need checking.' ])
note(25,218,'FOLLOW THROUGH INTO THE NEXT PLAN',[
 'Keep the eight-seat dining arrangement as the current proposal. Do not silently add ten seats to a furnished drawing.',
 'If ten at one table matters, develop table position, chair pull-out and both circulation edges as one measured change.',
 'Two simultaneous high-flow showers remain a services requirement; geometry checks do not prove pressure or hot-water capacity.',
 'No new partitions or furniture changes are adopted by this review. The JSON preserves all 12 reproducible scenarios.' ])
m.c.showPage();m.c.save()
(OUT/'concept-19-study-check.json').write_text(json.dumps({'status':'Use review; conflicts intentionally retained as findings','route_width_m':.7,
 'scenarios':SCENARIOS,'model_changed':False,'dining_seats':8,'five_visitors_depend_on_child_sharing':True,
 'limitations':['Synthetic body and object sizes','No multi-agent movement or occupied bathroom simulation','No accessibility validation','No water pressure or hot-water capacity test']},indent=2)+'\n')
print(PDF)
for s in SCENARIOS:print(s['id'],s['result'])
