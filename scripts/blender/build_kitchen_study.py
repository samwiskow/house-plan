import bpy,sys,argparse,json,math,hashlib,random
from pathlib import Path
from mathutils import Vector, Matrix
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--samples',type=int,default=96);p.add_argument('--width',type=int,default=1500);p.add_argument('--views',nargs='+');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
R=a.root.resolve();O=R/'output/blender/kitchen-study';O.mkdir(parents=True,exist_ok=True)
base=R/'output/blender/approved-room/approved-room.blend';source_hash=hashlib.sha256(base.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(base));scene=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
proposal=json.loads((R/'output/design/kitchen-selections/boot-room-option.json').read_text());plans=json.loads((R/'studies/l-house-booklet/plans.json').read_text())['default'];model=json.loads((R/'viewer-l-house/model.json').read_text())
random.seed(9);current=None;groups={}
def group(n):
 global current
 current=bpy.data.collections.new(n);scene.collection.children.link(current);groups[n]=current;return current
def link(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 current.objects.link(o);return o
def mat(n,c,r=.6,metal=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;q=m.node_tree.nodes.get('Principled BSDF');q.inputs['Base Color'].default_value=(*c,1);q.inputs['Roughness'].default_value=r;q.inputs['Metallic'].default_value=metal;return m
def box(n,pos,dim,m,b=.004):
 v=[(xx*dim[0]/2,yy*dim[1]/2,zz*dim[2]/2) for xx,yy,zz in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]];o=mesh(n,v,[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],m);o.location=pos
 if m is globals().get('wood') and 'woodbox' in globals():
  o.data.materials[0]=woodbox;uv=o.data.uv_layers.new(name='Timber grain')
  for face in o.data.polygons:
   axes=sorted(range(3),key=lambda k:max(v[i][k] for i in face.vertices)-min(v[i][k] for i in face.vertices),reverse=True)
   for li in face.loop_indices:
    co=v[o.data.loops[li].vertex_index];uv.data[li].uv=(co[axes[0]],co[axes[1]])
 if b:
  mod=o.modifiers.new('Soft arris','BEVEL');mod.width=min(b,min(dim)*.44);mod.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o
def mesh(n,v,f,m):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);current.objects.link(o);o.data.materials.append(m);return o
def curve(n,pts,r,m):
 d=bpy.data.curves.new(n,'CURVE');d.dimensions='3D';d.resolution_u=12;d.bevel_depth=r;d.bevel_resolution=4;d.use_fill_caps=True;s=d.splines.new('POLY');s.points.add(len(pts)-1)
 for v,co in zip(s.points,pts):v.co=(*co,1)
 o=bpy.data.objects.new(n,d);current.objects.link(o);o.data.materials.append(m);return o
def cyl(n,pos,r,depth,m,rot=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=pos);o=link(bpy.context.object);o.name=n;o.data.materials.append(m)
 if rot:o.rotation_euler=rot
 for f in o.data.polygons:f.use_smooth=True
 return o
def area_light(n,pos,target,power,size,color=(1,.94,.83)):
 d=bpy.data.lights.new(n,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(n,d);current.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False;return o
paint=mat('K01 warm ivory cabinetry',(.67,.63,.53),.48);plaster=mat('K01 warm lime plaster',(.76,.72,.63),.85);stone=mat('K01 quiet cream honed stone',(.70,.65,.54),.42);ceramic=mat('K01 glazed ivory ceramic',(.88,.86,.79),.18);bronze=mat('K01 brushed bronze',(.29,.19,.095),.28,.8);black=mat('K01 hob glass',(.008,.009,.008),.18,.2);glass=mat('K01 clear glazing',(.94,.98,.96),.06);glass.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value=1
wood=mat('K01 dark oak',(.12,.065,.032),.49);n=wood.node_tree.nodes;l=wood.node_tree.links;tc=n.new('ShaderNodeTexCoord');tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'assets/living-study/oak_veneer_02_diff.jpg'),check_existing=True);tex.image.pack();tex.projection='BOX';tex.projection_blend=.15;l.new(tc.outputs['Object'],tex.inputs['Vector']);bw=n.new('ShaderNodeRGBToBW');l.new(tex.outputs['Color'],bw.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.44;ramp.color_ramp.elements[0].color=(.018,.009,.004,1);ramp.color_ramp.elements[1].position=.60;ramp.color_ramp.elements[1].color=(.21,.115,.057,1);l.new(bw.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],n['Principled BSDF'].inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.001;l.new(bw.outputs[0],bump.inputs['Height']);l.new(bump.outputs[0],n['Principled BSDF'].inputs['Normal'])
woodbox=wood.copy();woodbox.name='K01 oak joinery aligned grain';next(q for q in woodbox.node_tree.nodes if q.type=='TEX_IMAGE').projection='FLAT';woodbox.node_tree.links.new(next(q for q in woodbox.node_tree.nodes if q.type=='TEX_COORD').outputs['UV'],next(q for q in woodbox.node_tree.nodes if q.type=='TEX_IMAGE').inputs['Vector'])
n=stone.node_tree.nodes;l=stone.node_tree.links;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=3;ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.62,.58,.49,1);ramp.color_ramp.elements[1].color=(.78,.74,.65,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],n['Principled BSDF'].inputs['Base Color'])
def framed(n,x,y,z,w,h,m,axis='y'):
 def b(name,xx,zz,ww,hh,depth=.025,offset=0):
  if axis=='y':return box(name,(x+xx,y-offset,z+zz),(ww,depth,hh),m,.003)
  return box(name,(x-offset,y+xx,z+zz),(depth,ww,hh),m,.003)
 b(n+' recessed field',0,0,w-.08,h-.08,.018,-.008)
 for xx in [-w/2+.032,w/2-.032]:b(n+' stile',xx,0,.064,h)
 for zz in [-h/2+.032,h/2-.032]:b(n+' rail',0,zz,w-.128,.064)
 for xx in [-w/2+.072,w/2-.072]:b(n+' inner bead',xx,0,.013,h-.13,.020,.012)
 for zz in [-h/2+.072,h/2-.072]:b(n+' inner bead',0,zz,w-.13,.013,.020,.012)
def profile_top(n,x,y,w,d,z):
 levels=[(z-.060,0),(z-.052,.006),(z-.044,.021),(z-.034,.023),(z-.025,.009),(z-.012,.004),(z,0)];verts=[];N=64
 for zz,inset in levels:
  for cx,cy,start in [(w/2-.03,-d/2+.03,-90),(w/2-.03,d/2-.03,0),(-w/2+.03,d/2-.03,90),(-w/2+.03,-d/2+.03,180)]:
   for j in range(16):
    t=math.radians(start+j*90/15);verts.append((x+cx+(.03-inset)*math.cos(t),y+cy+(.03-inset)*math.sin(t),zz))
 faces=[]
 for k in range(len(levels)-1):
  for j in range(N):faces.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
 faces+=[tuple(reversed(range(N))),tuple(range((len(levels)-1)*N,len(levels)*N))];return mesh(n,verts,faces,stone)
def tap(x,y,z):
 cyl('Provisional single lever mixer',(x,y,z+.055),.028,.11,bronze)
 pts=[(x,y,z+.05),(x,y,z+.25)]+[(x,y-.115+.115*math.cos(t),z+.25+.115*math.sin(t)) for t in [j*math.pi/32 for j in range(33)]]+[(x,y-.23,z+.205)]
 curve('Pull-out swan neck',pts,.016,bronze);cyl('Detachable rinse head',(x,y-.23,z+.18),.022,.055,bronze);curve('Mixer lever',[(x+.04,y,z+.06),(x+.10,y,z+.10)],.009,bronze)
def basin(x,y,z,w=.8,d=.57):
 o=box('Belfast ceramic sink',(x,y,z-.125),(w,d,.25),ceramic,.026);bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=o.modifiers[0].name)
 cut=box('Sink hollow',(x,y,z-.04),(w-.10,d-.10,.27),ceramic,.045);bpy.context.view_layer.objects.active=cut;bpy.ops.object.modifier_apply(modifier=cut.modifiers[0].name);bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Sink bowl','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True);cyl('Sink waste',(x,y,z-.173),.038,.004,bronze);return o
# Hide only superseded study elements; retain the saved source scene unchanged on disk.
for o in list(scene.objects):
 if o.name.startswith(('Ivory kitchen cabinet','Slim framed kitchen door','Recessed ivory panel','Bronze kitchen handle','Honed kitchen worktop','Forest-green island','Cream island worktop','Framed green island','Recessed green island','Kitchen stone floor')):o.hide_render=True
 if o.get('room') in ['G2','G3','G10'] or o.name.startswith(('Kitchen to pantry','Kitchen to laundry','Laundry to boot','Kitchen divider','Washer','Dryer','Laundry sink','Drying / folding','Boot bench','Coats / shoes','Pantry landing counter','Dry food cupboards','Pantry / utility divider','Island seat')):
  for q in [o,*o.children_recursive]:q.hide_render=True
 if o.parent and o.parent.name=='g' and o.type=='MESH' and o.name.startswith(('g / ivory','g / stone')):o.hide_render=True
 if o.type=='LIGHT' and 'soft ceiling' in o.name:o.hide_render=True
for name in ['House - first floor','Roofs','Ceilings']:bpy.data.collections[name].hide_render=True
for o in scene.objects:
 if o.name.startswith('Ceiling') or (o.parent and o.parent.name.startswith('Ceiling')):o.hide_render=True
# Cabinet fronts and the appliance layout are a first styling study, not a final kitchen specification.
group('K01 - sink cabinets')
for left,w in [(6.85,.65),(7.5,.65),(9.05,.55),(9.60,.55)]:
 box('Ivory cabinet carcass',(left+w/2,-5.68,.47),(w-.009,.62,.84),paint);box('Recessed plinth',(left+w/2,-5.64,.095),(w-.012,.50,.11),paint);framed('Country cabinet',left+w/2,-6.012,.49,w-.018,.73,paint);cyl('Cabinet knob',(left+w-.11,-6.045,.67),.014,.025,bronze,(math.pi/2,0,0))
box('Sink base',(8.6,-5.68,.365),(.9,.62,.63),paint);framed('Sink base door left',8.375,-6.012,.35,.43,.47,paint);framed('Sink base door right',8.825,-6.012,.35,.43,.47,paint)
profile_top('Moulded perimeter top left',7.50,-5.69,1.40,.70,.95);profile_top('Moulded perimeter top right',9.575,-5.69,1.15,.70,.95);box('Stone behind sink',(8.6,-5.38,.925),(.9,.12,.05),stone);basin(8.6,-5.755,.945);tap(8.85,-5.43,.95)
box('Integrated fridge carcass',(10.55,-5.68,1.61),(.8,.62,3.14),paint);framed('Fridge lower',10.55,-6.015,.625,.77,.99,paint);framed('Fridge upper',10.55,-6.015,1.73,.77,1.16,paint);framed('Fridge top cupboard',10.55,-6.015,2.75,.77,.80,paint);curve('Fridge bronze pull',[(10.27,-6.065,1.25),(10.27,-6.065,1.52)],.008,bronze)
box('Fridge ceiling closure',(10.55,-5.70,3.175),(.85,.70,.05),paint)
box('Fridge finished end',(10.132,-5.70,1.60),(.03,.67,3.14),paint)
box('Blind corner backing',(11.175,-5.875,1.60),(.35,1.0,3.14),paint)
box('Plain internal corner return',(10.99,-6.19,1.60),(.035,.37,3.14),paint)
y=-7.5875;w=.525
box('Shallow pantry-wall storage',(11.175,y,1.60),(.35,w,3.14),paint)
for z,h in [(.625,.99),(1.73,1.16),(2.75,.80)]:framed('Pantry-wall cupboard',10.98,y,z,w-.025,h,paint,axis='x')
curve('Pantry-wall cupboard pull',[(10.94,y+.15,1.25),(10.94,y+.15,1.46)],.007,bronze)
box('Storage above concealed pantry door',(11.19,-6.85,2.76),(.38,.90,.80),paint)
for y in [-6.625,-7.075]:framed('Over-door cupboard',10.98,y,2.75,.437,.80,paint,axis='x')
for yy in [-6.39,-7.31]:box('Pantry doorway cabinet return',(11.23,yy,1.19),(.44,.02,2.27),paint)
box('Pantry-wall ceiling closure',(11.15,-6.60,3.175),(.45,2.50,.05),paint)
group('K02 - dark oak island')
box('Island oak carcass',(8.725,-7.555,.48),(2.20,.65,.82),wood);box('Island foot plinth',(8.725,-7.555,.12),(2.24,.69,.12),wood)
for x in [7.64,9.81]:
 for y in [-7.30,-8.08]:box('Substantial oak corner post',(x,y,.475),(.12,.12,.87),wood,.008)
for x in [8.0,8.725,9.45]:framed('Oak island panel',x,-7.901,.50,.69,.68,wood)
for x in [7.61,9.84]:framed('Oak island end',x,-7.59,.5,.70,.68,wood,axis='x')
profile_top('Island shaped stone edge',8.725,-7.7,2.4,1,.97)
box('Provisional induction hob',(8.72,-7.55,.975),(.64,.43,.009),black,.01)
for x in [8.55,8.88]:
 for y in [-7.43,-7.67]:curve('Hob zone',[(x+.085*math.cos(j*math.tau/64),y+.085*math.sin(j*math.tau/64),.981) for j in range(65)],.0008,bronze)
group('K03 - milk glass pendants')
def pendant(x,y):
 cyl('Bronze ceiling rose',(x,y,3.185),.055,.028,bronze);curve('Pendant flex',[(x,y,3.17),(x,y,2.28)],.0035,bronze);cyl('Bronze shade cap',(x,y,2.28),.038,.055,bronze)
 v=[];f=[];profile=[(.037,2.26),(.060,2.24),(.16,2.13),(.26,2.045),(.265,2.03),(.254,2.024),(.15,2.114),(.045,2.237)]
 for r,z in profile:
  for j in range(96):v.append((x+r*math.cos(j*math.tau/96),y+r*math.sin(j*math.tau/96),z))
 for k in range(len(profile)-1):
  for j in range(96):f.append((k*96+j,k*96+(j+1)%96,(k+1)*96+(j+1)%96,(k+1)*96+j))
 o=mesh('Milk glass conical shade',v,f,ceramic)
 for face in o.data.polygons:face.use_smooth=True
 area_light('Pendant warm pool',(x,y,2.04),(x,y,0),22,.20,(1,.79,.52))
for x in [8.02,9.43]:pendant(x,-7.7)
group('K09 - curved oak stools')
stoolwood=wood.copy();stoolwood.name='K01 lighter aged oak stools';r=next(n for n in stoolwood.node_tree.nodes if n.type=='VALTORGB');r.color_ramp.elements[0].color=(.055,.026,.009,1);r.color_ramp.elements[1].color=(.32,.20,.11,1)
legwood=stoolwood.copy();legwood.name='K01 stool leg lengthwise grain';next(q for q in legwood.node_tree.nodes if q.type=='TEX_IMAGE').projection='FLAT';ln=legwood.node_tree.nodes;ll=legwood.node_tree.links;mapping=ln.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value[2]=math.pi/2;ll.new(next(q for q in ln if q.type=='TEX_COORD').outputs['UV'],mapping.inputs['Vector']);ll.new(mapping.outputs['Vector'],next(q for q in ln if q.type=='TEX_IMAGE').inputs['Vector'])
def stool(cx,cy):
 for xx in [-1,1]:
  for yy in [-1,1]:
   start=Vector((cx+xx*.245,cy+yy*.225,.055));end=Vector((cx+xx*.18,cy+yy*.145,.665));d=end-start
   bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.021,radius2=.029,depth=d.length,location=(start+end)/2);o=link(bpy.context.object);o.name='Splayed tapered oak stool leg';o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(legwood)
 for yy in [-.20,.20]:curve('Stool foot rail',[(cx-.225,cy+yy,.26),(cx+.225,cy+yy,.26)],.016,stoolwood)
 for xx in [-.225,.225]:curve('Stool side rail',[(cx+xx,cy-.20,.29),(cx+xx,cy+.20,.29)],.014,stoolwood)
 vs=[];fs=[]
 for radius,z in [(0,.668),(.65,.669),(1,.692),(1,.644),(.65,.632),(0,.632)]:
  for j in range(64):t=j*math.tau/64;vs.append((cx+.25*radius*math.cos(t),cy+.225*radius*math.sin(t),z))
 for k in range(5):
  for j in range(64):fs.append((k*64+j,k*64+(j+1)%64,(k+1)*64+(j+1)%64,(k+1)*64+j))
 o=mesh('Shaped solid oak stool seat',vs,fs,stoolwood)
 for f in o.data.polygons:f.use_smooth=True
 for xx in [-1,1]:curve('Stool back support',[(cx+xx*.17,cy-.12,.65),(cx+xx*.185,cy-.15,.80),(cx+xx*.205,cy-.17,.97)],.022,stoolwood)
 vs=[];fs=[]
 for rr,z in [(.292,.94),(.292,1.025),(.260,1.025),(.260,.94)]:
  for j in range(49):t=math.radians(200+140*j/48);vs.append((cx+rr*math.cos(t),cy+.03+rr*math.sin(t),z))
 for k in range(4):
  for j in range(48):fs.append((k*49+j,k*49+j+1,((k+1)%4)*49+j+1,((k+1)%4)*49+j))
 fs.extend([(0,49,98,147),(48,97,146,195)]);o=mesh('Broad curved oak stool back',vs,fs,stoolwood);mod=o.modifiers.new('Rounded timber edges','BEVEL');mod.width=.005;mod.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL')
for x in [8.05,9.4]:stool(x,-8.5)
group('K04 - enclosed pantry and utility')
for x,w in [(11.95,.9),(12.85,.9)]:box('Pantry base',(x,-5.67,.47),(w-.015,.60,.84),paint);framed('Pantry cabinet',x,-5.985,.48,w-.025,.73,paint)
box('Pantry landing counter',(12.4,-5.65,.92),(1.8,.60,.05),wood)
for z in [1.35,1.75,2.15]:box('Pantry oak open shelf',(12.4,-5.53,z),(1.78,.35,.035),wood)
for z in [.4,.85,1.3,1.75,2.2]:box('Opposite dry food shelf',(12.4,-7.67,z),(1.78,.35,.032),wood)
for x in [11.8,12.15,12.5,12.85]:
 for z in [1.37,1.77]:cyl('Pantry storage jar',(x,-5.53,z+.10),.065,.18,ceramic);cyl('Jar oak lid',(x,-5.53,z+.20),.07,.022,wood)
for x in [13.825,14.525]:
 box('Laundry appliance',(x,-5.68,.47),(.64,.64,.86),ceramic,.02);cyl('Laundry machine door',(x,-6.01,.49),.21,.045,black,(math.pi/2,0,0));cyl('Machine selector',(x+.2,-6.025,.78),.023,.02,bronze,(math.pi/2,0,0))
box('Utility sink base',(15.275,-5.68,.46),(.75,.63,.83),paint);basin(15.275,-5.7,.94,.70,.55);tap(15.45,-5.42,.94)
box('Utility folding counter',(15.55,-7.45,.94),(.6,2.1,.055),wood)
for y in [-6.78,-7.46,-8.13]:framed('Utility folding cupboard',15.23,y,.49,.66,.73,paint,axis='x')
box('Tall broom cupboard',(13.75,-8.60,1.23),(.6,1,2.38),paint);framed('Broom door',14.06,-8.60,1.25,.96,2.25,paint,axis='x')
box('Boot room bench',(14.5,-13.825,.47),(1.8,.45,.075),wood)
for x in [13.68,15.32]:box('Bench end support',(x,-13.825,.25),(.075,.40,.42),paint)
box('Coat cupboard',(13.75,-11.75,1.2),(1.5,.60,2.32),paint)
for x in [13.375,14.125]:framed('Coat cupboard door',x,-12.055,1.22,.735,2.20,paint)
# Generate walls from the selected measured polygons, with real openings at both pantry connections.
group('K05 - revised ground shell')
rooms=[dict(r) for r in plans['rooms'] if r['floor']=='g' and r['id']!='L']
for r in rooms:
 if r['id'] in proposal['room_polygons']:r['p']=proposal['room_polygons'][r['id']]
rooms.append({'id':'G4','p':proposal['room_polygons']['G4']})
def inside(x,y,p):
 c=False
 for a,b in zip(p,p[1:]+p[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
 return c
opens=[]
for d in plans['doors']:
 if d['floor']=='g' and d['x']<16.2 and d['id'] not in ['Kitchen to pantry','Kitchen to laundry','Laundry to boot']:opens.append((d['x'],d['y'],d['axis'],d['w'],0,2.3))
for _,x,y,axis,w in proposal['doors']:opens.append((x,y,axis,w,0,2.3))
for f,x,y,axis,w in plans['openings']:
 if f=='g' and x<16.2:opens.append((x,y,axis,w,0,2.4))
for w in model['windows']:
 if w['floor']=='g':opens.append((w['x'],w['y'],w['axis'],w['w'],w['sill'],w['head']))
opens.append((.55,.175,'h',5.8,0,2.4))
shell=plans['house'];xs={p[0] for r in rooms for p in r['p']}|{p[0] for p in shell};ys={p[1] for r in rooms for p in r['p']}|{p[1] for p in shell};gaps=[]
for x,y,axis,w,lo,hi in opens:
 rr=(x,y-.2,w,.4) if axis=='h' else(x-.2,y,.4,w);gaps.append((rr,lo,hi));xs.update([rr[0],rr[0]+rr[2]]);ys.update([rr[1],rr[1]+rr[3]])
xs=sorted(xs);ys=sorted(ys)
for x0,x1 in zip(xs,xs[1:]):
 for y0,y1 in zip(ys,ys[1:]):
  x=(x0+x1)/2;y=(y0+y1)/2
  if not inside(x,y,shell) or any(inside(x,y,r['p']) for r in rooms):continue
  intervals=[(0,3.2)]
  for (gx,gy,w,h),lo,hi in gaps:
   if gx<=x<=gx+w and gy<=y<=gy+h:intervals=[q for l,u in intervals for q in [(l,min(u,lo)),(max(l,hi),u)] if q[1]-q[0]>.001]
  for lo,hi in intervals:box('Measured wall',(x,-y,(lo+hi)/2),(x1-x0,y1-y0,hi-lo),plaster,0)
for r in rooms:
 pts=r['p'];mesh('Ceiling '+r['id'],[(x,-y,3.2) for x,y in pts],[tuple(range(len(pts)))],plaster)
 if r['id'] in ['G2','G3','G4','G10']:
  m=bpy.data.materials.get('Matte natural oak floor') if r['id']=='G2' else stone
  mesh('Revised floor '+r['id'],[(x,-y,.045) for x,y in pts],[tuple(range(len(pts)))],m)
group('K10 - herringbone floor')
floormat=stoolwood.copy();floormat.name='K01 pale oak herringbone';r=next(n for n in floormat.node_tree.nodes if n.type=='VALTORGB');r.color_ramp.elements[0].color=(.14,.095,.055,1);r.color_ramp.elements[1].color=(.43,.32,.20,1)
tex=next(n for n in floormat.node_tree.nodes if n.type=='TEX_IMAGE');tex.projection='FLAT';tc=next(n for n in floormat.node_tree.nodes if n.type=='TEX_COORD');floormat.node_tree.links.new(tc.outputs['UV'],tex.inputs['Vector'])
def clip(poly,axis,bound,sign):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=sign*(a[axis]-bound)>=0;ib=sign*(b[axis]-bound)>=0
  if ia:out.append(a)
  if ia!=ib:
   t=(bound-a[axis])/(b[axis]-a[axis]);out.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
 return out
verts=[];faces=[];uvs=[];root2=math.sqrt(.5)
rects=[(6.85,5.35,11.35,8),(6.7,8,13.3,9.3),(6.7,6.7,6.85,8)]
for i in range(-14,15):
 for j in range(-75,76):
  ox=(6*i-j)*.12;oy=(4*i+j)*.12
  for x,y,w,h in [(ox,oy,.60,.12),(ox+.60,oy,.12,.60)]:
   points=[(x+.001,y+.001),(x+w-.001,y+.001),(x+w-.001,y+h-.001),(x+.001,y+h-.001)]
   poly=[(9+(px-py)*root2,7+(px+py)*root2) for px,py in points]
   if max(p[0] for p in poly)<6.7 or min(p[0] for p in poly)>13.3 or max(p[1] for p in poly)<5.35 or min(p[1] for p in poly)>9.3:continue
   for x0,y0,x1,y1 in rects:
    q=poly
    for axis,bound,sgn in [(0,x0,1),(0,x1,-1),(1,y0,1),(1,y1,-1)]:
     if q:q=clip(q,axis,bound,sgn)
    if len(q)<3:continue
    k=len(verts);verts.extend((px,-py,.053) for px,py in q);faces.append(tuple(range(k,k+len(q))));u0=random.random();v0=random.random()
    for px,py in q:
     rx=((px-9)+(py-7))*root2-x;ry=((py-7)-(px-9))*root2-y;uvs.append((u0+(rx if w>h else ry),v0+(ry if w>h else rx)))
o=mesh('Individual herringbone boards',verts,faces,floormat);uv=o.data.uv_layers.new(name='Physical oak grain')
for loop in o.data.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]

# Closed connecting door; a second render opens it to show the route.
group('K06 - pantry connecting doors')
box('Concealed kitchen pantry door',(11.015,-6.85,1.19),(.045,.885,2.27),paint)
for y in [-6.625,-7.075]:
 for z,h in [(.625,.99),(1.73,1.16)]:framed('Concealed kitchen pantry door panel',10.98,y,z,.437,h,paint,axis='x')
for y in [-6.80,-6.90]:curve('Concealed kitchen pantry door pull',[(10.94,y,1.25),(10.94,y,1.46)],.007,bronze)
box('Concealed kitchen pantry door plinth',(11.03,-6.85,.085),(.025,.875,.07),paint)
x=13.375;y=-6.85;w=1.05;name='Utility pantry connecting door'
door=box(name,(x,y,1.175),(.045,w-.015,2.28),paint);framed(name+' upper',x-.03,y,1.66,w-.065,1.18,paint,axis='x');framed(name+' lower',x-.03,y,.57,w-.065,.79,paint,axis='x');curve(name+' handle',[(x-.07,y+.28,.92),(x-.07,y+.28,1.12)],.007,bronze)
for yy in [y-w/2-.025,y+w/2+.025]:box('Pantry door casing',(x-.055,yy,1.19),(.035,.065,2.38),paint)
box('Pantry door head casing',(x-.055,y,2.37),(.035,w+.12,.065),paint)
group('K07 - kitchen daylight')
area_light('Kitchen window soft daylight',(8.7,-5.22,1.95),(8.7,-8.2,1.0),280,2.3,(.88,.94,1));area_light('Utility window daylight',(16,-7.2,1.9),(13.9,-7.2,.9),180,1.6,(.88,.94,1));area_light('Pantry ceiling light',(12.4,-6.5,3.08),(12.4,-6.5,0),65,1.0);area_light('Kitchen task fill',(10.5,-8.8,3.05),(9,-6.4,.8),90,1.8)
scene['kitchen_layout']='Option D, enclosed pantry with utility connecting door';scene['kitchen_finish']='Ivory country cabinets; dark oak island; shaped pale stone edge; milk-glass pendants';scene['unresolved']='Exact tap; edge construction; appliance positions; stool clearance; first-floor coordination; upper storage access'
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=True;scene.render.resolution_x=a.width;scene.render.resolution_y=round(a.width*2/3);scene.render.resolution_percentage=100
scene.camera.location=(7.1,-9.03,1.65);scene.camera.rotation_euler=(Vector((9.5,-5.85,1.4))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.lens=23
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'kitchen-option-d.blend'),compress=True)
report={'layout':'D enclosed pantry with connecting door','base_sha256':source_hash,'areas_m2':proposal['areas_m2'],'asset_cost':0,'stools':'Custom curved oak stools based on user reference; not an exact retail model','tap':'provisional single lever pull-out rinse','first_floor_coordinated':False,'pantry_wall_storage_depth_m':.35,'island_to_storage_face_m':1.055,'upper_cabinets':'Tall fridge and pantry bank to 3.2 m; no cupboards around sink window','views':[]}
if a.views and (O/'validation.json').exists():report['views']=json.loads((O/'validation.json').read_text())['views']
def render(sc,name,pos,target,lens):
 if a.views and name not in a.views:return
 sc.camera.location=pos;sc.camera.rotation_euler=(Vector(target)-sc.camera.location).to_track_quat('-Z','Y').to_euler();sc.camera.data.lens=lens;sc.camera.data.dof.use_dof=False;sc.render.filepath=str(O/(name+'.png'));bpy.ops.render.render(write_still=True,scene=sc.name);report['views']=list(dict.fromkeys([*report['views'],name+'.png']));(O/'validation.json').write_text(json.dumps(report,indent=2))
# The studio scenes link the same fitted objects used in the room.
studio=bpy.data.scenes.new('Kitchen isolated furniture study');studio.render.engine='CYCLES';studio.cycles.device='GPU';studio.cycles.samples=a.samples;studio.cycles.use_denoising=True;studio.render.resolution_x=a.width;studio.render.resolution_y=round(a.width*.75);studio.render.resolution_percentage=100;studio.view_settings.view_transform='AgX';studio.world=bpy.data.worlds.new('Kitchen studio world');studio.world.use_nodes=True;studio.world.node_tree.nodes['Background'].inputs[0].default_value=(.73,.77,.83,1);studio.world.node_tree.nodes['Background'].inputs[1].default_value=.4
group('K08 - studio only');studio.collection.children.link(current);scene.collection.children.unlink(current)
box('Studio ground',(9,-7,-.015),(200,200,.1),mat('Kitchen studio floor',(.52,.50,.45),.8),0)
area_light('Studio key',(5,-9,6),(9,-6,.5),700,5);area_light('Studio edge',(12,-3,5),(9,-6,.8),550,4)
camera=bpy.data.objects.new('Kitchen studio camera',bpy.data.cameras.new('Kitchen studio camera'));current.objects.link(camera);studio.camera=camera
for collection,name,pos,target,lens in [('K02 - dark oak island','island-study',(11.7,-11.8,2.75),(8.725,-7.7,.6),48),('K01 - sink cabinets','cabinet-study',(5.6,-12.7,3.25),(9.35,-6.25,1.5),43),('K09 - curved oak stools','stool-study',(10.6,-11.6,1.8),(8.7,-8.5,.61),53),('K03 - milk glass pendants','pendant-study',(9.6,-10.9,2.75),(8.6,-7.7,2.45),48)]:
 studio.collection.children.link(groups[collection])
 extra=[obj for obj in groups['K06 - pantry connecting doors'].objects if obj.name.startswith('Concealed kitchen pantry door') or (obj.name.startswith('Pantry door') and obj.location.x<12)] if collection=='K01 - sink cabinets' else []
 for obj in extra:studio.collection.objects.link(obj)
 render(studio,name,pos,target,lens)
 for obj in extra:studio.collection.objects.unlink(obj)
 studio.collection.children.unlink(groups[collection])
render(scene,'kitchen-room',(7.1,-9.03,1.65),(9.5,-5.85,1.4),23)
bpy.context.view_layer.update()
hinge=Vector((13.375,-7.375,0));turn=Matrix.Translation(hinge)@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation(-hinge)
for obj in groups['K06 - pantry connecting doors'].objects:
 if obj.name.startswith('Utility pantry connecting door'):obj.matrix_world=turn@obj.matrix_world
render(scene,'pantry-utility',(11.73,-7.25,1.63),(13.5,-5.75,1.3),20)
assert hashlib.sha256(base.read_bytes()).hexdigest()==source_hash
(O/'validation.json').write_text(json.dumps(report,indent=2));print('KITCHEN_COMPLETE',json.dumps(report))
