"""Fittings for the warm interior, service rooms and open stair revision."""
col=cols['g','floors']
parquet(rect(11.35,6.4,.15,.9),'Kitchen pantry continuous threshold',0)
col=cols['g','furniture']
pb('Double fridge continuous top closure',[10.925,8.025,.79,1.25],3.15,3.2,ivory)
# Replace the former fridge location with ovens and useful closed storage.
cabinet('Kitchen oven tower',[10.15,5.35,.8,.64],.04,3.13)
for zz in [1.18,1.79]:
    box('Built-in oven glass',(10.55,-6.002,zz),(.63,.032,.47),black,.018)
    box('Oven inner window',(10.55,-6.023,zz-.035),(.51,.006,.28),glass,.01)
    tube('Oven bronze handle',[(10.31,-6.065,zz+.15),(10.79,-6.065,zz+.15)],.012,metal)
    for xx in [10.32,10.78]:
        o=cyl('Oven selector',(0,0,0),.019,.020,metal);o.rotation_euler.x=math.pi/2;o.location=(xx,-6.035,zz+.20)
cabinet('Pantry preparation drawers',[12.78,7.6,.52,1.25],.04,.83,'west')
pb('Pantry preparation worktop',[12.76,7.6,.54,1.25],.87,.92,stone2,.012)
for z in [1.32,1.72,2.12]:
    pb('Pantry long oak shelf',[13.01,7.52,.28,1.32],z,z+.035,wood)
    for j in range(4):
        yy=7.66+j*.28;cyl('Pantry ceramic canister',(13.13,-yy,z+.12),.055,.20,white)
        cyl('Pantry canister lid',(13.13,-yy,z+.225),.058,.015,wood)
for j in range(3):
    yy=8.96+j*.08;pb('Pantry storage basket',[12.10,yy,.39,.067],.44,.64,fabric,.012)
for i in range(6):
    xx=12.0+i*.2;cyl('Pantry preserves jar',(xx,-9.13,1.43),.06,.21,olive if i%2 else stone2)
    cyl('Pantry jar lid',(xx,-9.13,1.545),.061,.02,wood)
col=cols['u','furniture']
for obj in list(col.objects):
    if obj.name.startswith(('U1 linen curtain','Bedroom ceramic vase')):bpy.data.objects.remove(obj,do_unlink=True)
for win in data['windows']:
    if win['floor']!='u':continue
    x,y,w=win['x'],win['y'],win['w'];h=win['axis']=='h'
    side=next((side for side in [-1,1] if inside(x+w/2 if h else x+side*.2,y+side*.2 if h else y+w/2,next(r['p'] for r in data['rooms'] if r['id']=='U1'))),None)
    if side is None:continue
    for start in [-.10,w-.21]:
        vs=[];fs=[]
        for i in range(37):
            u=start+i*.31/36;offset=side*(.225+.028*math.cos(i*math.pi/3))
            for j in range(22):
                zz=3.56+j*2.55/21;vs.append((x+u,-y-offset,zz) if h else (x+offset,-y-u,zz))
        for i in range(36):
            for j in range(21):k=i*22+j;fs.append((k,k+22,k+23,k+1))
        o=mesh('U1 full-height linen curtain',vs,fs,linen);o.modifiers.new('Soft curtain thickness','SOLIDIFY').thickness=.001
        for face in o.data.polygons:face.use_smooth=True
    curtain_start=(x-.12,-y-side*.23,6.12) if h else (x+side*.23,-y+.12,6.12)
    curtain_end=(x+w+.12,-y-side*.23,6.12) if h else (x+side*.23,-y-w-.12,6.12)
    tube('U1 recessed curtain rail',[curtain_start,curtain_end],.012,metal)
before=set(col.objects)
cyl('Parents reading side table',(1.78,-2.78,4.04),.26,.045,wood,40)
cyl('Parents side table pedestal',(1.78,-2.78,3.79),.055,.47,wood)
for j in range(2):pb('Parents reading book',[1.63,2.68,.22,.16],4.067+j*.025,4.09+j*.025,[ivory,blue][j])
for obj in set(col.objects)-before:obj['room_id']='U1'
pb('Dressing soft woven rug',[1.15,4.60,3.90,1.12],3.541,3.551,fabric,.02)
pb('Bathroom linen rug',[1.6,7.35,1.1,.56],3.542,3.552,linen,.018)
shower_door=bpy.data.objects.new('Ensuite shower door hinge',None);col.objects.link(shower_door)
shower_door.location=(2.332,-8.535,3.54);shower_door.rotation_euler.z=math.pi/2
shower_door['level']='u';shower_door['part']='shower-door';shower_door['door_type']='shower';shower_door['open_angle']=math.pi/2
leaf=box('Ensuite shower door glass',(-.486,0,1.04),(.974,.010,2.02),glass,.002);leaf.parent=shower_door
for yy in [-.036,.036]:
    o=tube('Ensuite shower door pull',[(-.87,yy,1.00),(-.87,yy,1.30)],.012,metal);o.parent=shower_door
    for zz in [1.0,1.3]:
        o=tube('Ensuite shower handle fixing',[(-.87,0,zz),(-.87,yy,zz)],.011,metal);o.parent=shower_door
for zz in [4.00,5.15]:box('Ensuite glass door hinge',(2.346,-8.5355,zz),(.045,.033,.085),metal,.004)
tube('Ensuite enclosure top rail',[(.35,-8.535,5.64),(3.35,-8.535,5.64)],.012,metal)
for xx in [.37,1.03,2.67,3.33]:
    for zz in [3.63,5.47]:box('Ensuite fixed glass clamp',(xx,-8.535,zz),(.036,.035,.055),metal,.004)
for i in range(5):
    for j in range(4):pb('Ensuite shower honed wall tile',[.35+i*.6,9.875,.596,.024],3.54+j*.60,3.54+(j+1)*.60-.004,stone2,.001)
glow=mat('Coastal | warm mirror light',(1,.86,.65),.4)
shader=glow.node_tree.nodes['Principled BSDF'];shader.inputs['Emission Color'].default_value=(1,.86,.65,1);shader.inputs['Emission Strength'].default_value=1.2
for xx in [2.015,2.635,2.765,3.385]:
    box('Vanity soft mirror light',(xx,-6.773,5.14),(.010,.008,.88),glow,.002)
for xx in [2.015,2.635,2.765,3.385]:
    o=light('Vanity warm face light',(xx,-6.785,5.14),(xx,-8.0,5.14),3,.01,(1,.91,.79));o.data.shape='RECTANGLE';o.data.size_y=.88
# A full-depth stringer supports each flight. The open side faces the entrance hall.
col=staircol
for s in data['stairs']:
    x,y,w,d=s['r'];half=s['risers']//2;run=(half-1)*s['going'];rise=s['rise'];upper=LEVELS[s['upper']]
    for side in [0,1]:
        lower=side==s['lower_side'];z0=.04+rise if lower else upper+.04;z1=upper/2+.04 if lower else upper/2+.04+rise
        for xx in [x+side*1.4+.025,x+side*1.4+.895]:
            vs=[(xx+dx,-yy,zz) for dx in [0,.08] for yy,zz in [(y,max(.04,z0-.28)),(y,z0),(y+run,z1),(y+run,z1-.28)]]
            mesh(s['id']+' oak stringer',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],wood,.006)
    if s['id']!='House stair':continue
    xx=x+w+.015;pts=[];count=math.ceil(run/.10)
    for i in range(count+1):
        t=i/count;yy=y+t*run;zz=.04+rise+t*(upper/2-rise)
        tube('House stair hall-side baluster',[(xx,-yy,zz),(xx,-yy,zz+.91)],.011,metal);pts.append((xx,-yy,zz+.93))
    tube('House stair hall-side oak handrail',pts,.027,wood)
    for j in range(11):
        yy=y+run+j*(d-run)/10;tube('House landing open guard',[(xx,-yy,upper/2+.04),(xx,-yy,upper/2+.97)],.011,metal)
    tube('House landing oak rail',[(xx,-y-run,upper/2+.97),(xx,-y-d,upper/2+.97)],.027,wood)
col=cols['g','furniture']
pb('Under-stair upholstered bench',[8.23,11.42,.48,.72],.38,.49,fabric,.06)
for xx in [8.25,8.66]:pb('Under-stair bench leg',[xx,11.49,.035,.58],.04,.38,wood)
col=roofcol
for x,y,w,d in [[3.29,-.18,.32,15.16],[3.45,9.74,12.93,.32]]:
    for poly,fn,name in roofs():
        if name!='House':continue
        q=poly
        for bound in [lambda xx,yy:xx-x,lambda xx,yy:x+w-xx,lambda xx,yy:yy-y,lambda xx,yy:y+d-yy]:q=clip(q,bound) if q else []
        if q:surface('House folded ridge cap',q,lambda xx,yy:fn(xx,yy)+.035,roofmat,.008)
for slope in [-1,1]:
    start=(3.45,9.9);end=(7.08,9.9+slope*5.08)
    vx,vy=end[0]-start[0],end[1]-start[1];length=math.hypot(vx,vy);nx,ny=-vy/length*.10,vx/length*.10
    for direction in [-1,1]:
        poly=[list(start),list(end),[end[0]+direction*nx,end[1]+direction*ny],[start[0]+direction*nx,start[1]+direction*ny]]
        surface('House folded valley flashing',poly,lambda xx,yy:roof_height(xx,yy)+.012,roofmat,.006)
