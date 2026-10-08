"""Small fittings executed in the house builder namespace."""
col=cols['u','furniture']
for x,y,w,d in [(1.2,1.0,4.45,2.2),(.9,10.45,2.85,2.6),(7.3,5.6,2.8,2.6),(12.4,11.25,2.85,2.7)]:
    pb('Low woven bedroom rug',[x,y,w,d],3.541,3.548,fabric,.014)
for x,y in [(1.25,1.65),(5.8,1.45)]:
    cyl('Bedroom ceramic vase',(x,-y,3.72),.09,.34,stone2)
col=cols['u','furniture']
for x in [2.325,3.075]:
    box('Ensuite bronze mirror frame',(x,-6.726,5.14),(.65,.024,.98),metal,.035)
    box('Ensuite mirror surface',(x,-6.749,5.14),(.60,.018,.93),mirror,.032)
for y in [8.60,8.81,9.02]:
    pb('Shower limestone shelf',[.365,y,.12,.17],4.8,4.825,stone2)
    cyl('Shower bottle',(.42,-y-.08,4.91),.024,.16,olive)
for x in [2.12,2.95]:
    pb('Vanity folded linen',[x,6.78,.18,.22],4.37,4.42,fabric,.018)
tube('Bath towel rail',[(1.37,-6.78,4.55),(1.85,-6.78,4.55)],.011,metal)
pb('Hanging bath linen',[1.43,6.76,.34,.032],4.04,4.53,fabric,.012)
for rid,x,y,z,w,d in [('UG',5.468,6.95,4.85,.025,.60),('G8',7.0,10.98,1.45,1.10,.025),('O4',23.6,20.40,4.50,1.1,.025)]:
    col=cols['g' if rid.startswith('G8') else 'o' if rid.startswith('O') else 'u','furniture']
    box(rid+' framed coastal study',(x,-y,z),(w,d,.70),wood,.008)
    box(rid+' muted landscape',(x+(.017 if w<.1 else 0),-y+(.017 if d<.1 else 0),z),(max(.008,w-.06),max(.008,d-.06),.64),blue,.001)
col=cols['g','furniture']
pb('Hall woven runner',[4.8,9.66,4.9,.84],.041,.049,fabric,.012)
cabinet('Arrival console',[7.6,10.55,.9,.30],.04,.78,'north')
box('Hall bronze mirror',(8.02,-10.966,1.62),(.74,.028,.90),metal,.028)
box('Hall mirror glass',(8.02,-10.94,1.62),(.68,.018,.84),mirror,.025)
for i in range(3):pb('Library reading book',[6.15+i*.055,13.25,.045,.22],.30,.57,[blue,olive,stone2][i])
cyl('Library side table',(6.67,-12.97,.52),.29,.045,wood)
tube('Library table support',[(6.67,-12.97,.04),(6.67,-12.97,.50)],.045,wood)
cyl('Library ceramic mug',(6.68,-12.97,.60),.04,.09,ivory)
col=cols['o','furniture']
chair('Office task chair',23.62,15.30,3.04,.68,.68,blue)
chair('Gaming task chair',23.55,16.17,3.04,.65,.65,black)
pb('Guest sofa bed plinth',[19.40,18.1,.9,1.9],3.18,3.34,wood,.04)
pb('Guest sofa bed back',[19.41,18.11,.17,1.86],3.34,3.92,fabric,.07)
for yy in [18.26,19.13]:pb('Guest sofa bed cushion',[19.58,yy,.65,.82],3.34,3.53,fabric,.075)
pb('Office woven rug',[20.7,17.55,3.8,2.25],3.041,3.047,fabric,.02)
col=cols['a','furniture']
pb('Workshop perforated tool board',[25.49,13.47,.026,2.08],1.03,2.11,oak)
for i in range(7):
    yy=13.65+i*.25
    tube('Hung workshop tool',[(25.46,-yy,1.36),(25.46,-yy,1.78)],.014,metal)
    box('Tool grip',(25.46,-yy,1.43),(.025,.045,.16),black,.008)
    box('Tool hook',(25.44,-yy,1.82),(.045,.020,.025),metal)
pb('Workshop vice base',[24.93,14.34,.5,.30],.94,1.06,black)
for i in range(5):pb('Labelled storage crate',[21.66,13.45+i*.30,.39,.27],.10,.35,olive,.02)
for j in range(4):tube('Gym wall rail',[(22.15+j*.14,-7.67,.30),(22.15+j*.14,-7.67,2.30)],.02,wood)
col=sitecol
for i in range(24):
    y=-23+rng.random()*42;x=(-4.3 if i%2 else 30.2)+rng.uniform(-.4,.4)
    ellipsoid('Weathered coastal boulder',(x,-y,.02),(.2+rng.random()*.4,.20+rng.random()*.25,.12+rng.random()*.22),stone)
for side in [-1,1]:
    vs=[];fs=[];N=22;M=15
    cx=-3.6 if side<0 else 30.7
    for j in range(M+1):
        y=-26+j*24/M
        for i in range(N+1):
            x=cx-1.1+2.2*i/N;h=.32*math.sin(math.pi*i/N)*math.sin(math.pi*j/M)
            vs.append((x,-y,-.11+h))
    for j in range(M):
        for i in range(N):k=j*(N+1)+i;fs.append((k,k+1,k+N+2,k+N+1))
    o=mesh('Low planted dune berm',vs,fs,soil)
    for f in o.data.polygons:f.use_smooth=True
for j in range(15):box('Tool store side lap',(29.31,-2.5,.08+j*.14),(.035,3,.13),wood,.004)
box('Tool store bronze latch',(28.28,-.955,1.08),(.15,.04,.024),metal)
pb('Outdoor rinse timber screen',[27.3,4.42,.065,1.65],0,2.15,oak)
for i in range(10):pb('Rinse screen slat',[27.28,4.43+i*.17,.10,.065],0,2.15,wood)
col=cols['a','openings']
for j in range(7):pb('Garage door overhead panel',[19.0+j*.32,17.27,.305,3.25],2.43,2.475,oak,.006)
for y in [17.24,20.56]:
    tube('Garage door track',[(18.96,-y,.05),(18.96,-y,2.18),(19.10,-y,2.45),(21.35,-y,2.45)],.018,metal)
col=sitecol
surface('Assumed coastal access road',rect(-90,37.15,180,5.5),-.10,black)
for y in [37.30,42.40]:tube('Road edge', [(-90,-y,-.08),(90,-y,-.08)],.015,stone2)
sitebox('Gate threshold',[12.25,64.7,6,.65],-.07,-.015,stone2)
for f in ['g','a']:
    col=cols[f,'walls'];vs=[];fs=[]
    for rec in wall_records:
        if rec['floor']!=f:continue
        x,y,w,d=rec['r'];lo=rec['lo'];hi=rec['hi']
        for axis,pos,start,length,norm in [('h',y,x,w,-1),('h',y+d,x,w,1),('v',x,y,d,-1),('v',x+w,y,d,1)]:
            sx,sy=(start+length/2,pos+norm*.03) if axis=='h' else (pos+norm*.03,start+length/2)
            if any(inside(sx,sy,p) for p in data['shells'][f]):continue
            for j in range(math.floor(lo/.22),math.ceil(hi/.22)):
                z0=max(lo,j*.22)+.006;z1=min(hi,(j+1)*.22)-.006
                if z1-z0<.015:continue
                pitch=.43;offset=.215*(j%2)
                for i in range(math.floor((start-offset)/pitch),math.ceil((start+length-offset)/pitch)):
                    s0=max(start,i*pitch+offset)+.005;s1=min(start+length,(i+1)*pitch+offset)-.005
                    if s1-s0<.015:continue
                    rr=[s0,pos-.006 if norm<0 else pos,s1-s0,.016] if axis=='h' else [pos-.006 if norm<0 else pos,s0,.016,s1-s0]
                    xx,yy,ww,dd=rr;k=len(vs)
                    vs.extend([(xx,-yy,z0),(xx+ww,-yy,z0),(xx+ww,-yy-dd,z0),(xx,-yy-dd,z0),(xx,-yy,z1),(xx+ww,-yy,z1),(xx+ww,-yy-dd,z1),(xx,-yy-dd,z1)])
                    fs.extend(tuple(k+i for i in face) for face in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
    mesh(f+' limestone coursing',vs,fs,stone,.003)
