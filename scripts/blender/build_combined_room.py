import bpy,sys,argparse,json,math,hashlib,random
from pathlib import Path
from mathutils import Vector,Matrix
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--width',type=int,default=1600);p.add_argument('--samples',type=int,default=96);p.add_argument('--views',nargs='+');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);R=a.root.resolve();O=R/'output/blender/combined-room';O.mkdir(parents=True,exist_ok=True)
base=R/'output/blender/kitchen-study/kitchen-option-d.blend';source_hash=hashlib.sha256(base.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(base));scene=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
col=bpy.data.collections.new('Combined rooms - glazed divider and screen');scene.collection.children.link(col)
def box(n,pos,dim,m):
 verts=[(x*dim[0]/2,y*dim[1]/2,z*dim[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]];me=bpy.data.meshes.new(n);me.from_pydata(verts,[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]);me.update();o=bpy.data.objects.new(n,me);col.objects.link(o);o.location=pos;me.materials.append(m);mod=o.modifiers.new('Soft edges','BEVEL');mod.width=.002;mod.segments=2;o.modifiers.new('Normals','WEIGHTED_NORMAL')
 if m==oak:
  uv=me.uv_layers.new(name='Lengthwise oak')
  for face in me.polygons:
   axes=sorted(range(3),key=lambda k:max(verts[i][k] for i in face.vertices)-min(verts[i][k] for i in face.vertices),reverse=True)
   for li in face.loop_indices:co=verts[me.loops[li].vertex_index];uv.data[li].uv=(co[axes[0]],co[axes[1]])
 return o

oak=bpy.data.materials['K01 oak joinery aligned grain'].copy();oak.name='Combined room warm oak screens';r=next(n for n in oak.node_tree.nodes if n.type=='VALTORGB');r.color_ramp.elements[0].color=(.10,.054,.025,1);r.color_ramp.elements[1].color=(.33,.22,.12,1)
glass=bpy.data.materials['Bifold clear glazing'].copy();glass.name='Combined clear divider glass';bs=glass.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(.97,.99,.98,1);bs.inputs['IOR'].default_value=1.45;bs.inputs['Roughness'].default_value=.025
bronze=bpy.data.materials['K01 brushed bronze']

dining_wood=bpy.data.materials['Pale weathered oak - furniture study'].copy();dining_wood.name='Combined pale natural dining oak'
ramp=next(n for n in dining_wood.node_tree.nodes if n.type=='VALTORGB')
ramp.color_ramp.elements[0].color=(.22,.16,.10,1);ramp.color_ramp.elements[1].color=(.59,.46,.31,1)
dining_wood.diffuse_color=(.48,.36,.23,1)
dining_cane=bpy.data.materials['Natural cane fibres'].copy();dining_cane.name='Combined pale dining cane'
dining_cane.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.53,.42,.28,1)
finish_counts={'wood':0,'cane':0}
for collection in bpy.data.collections:
 if collection.name=='01 Table' or collection.name.startswith('Approved cane dining chair'):
  for obj in collection.all_objects:
   for slot in obj.material_slots:
    if slot.material and slot.material.name in ['Pale weathered oak - furniture study','Natural cane fibres']:
     kind='wood' if slot.material.name=='Pale weathered oak - furniture study' else 'cane'
     slot.link='OBJECT';slot.material=dining_wood if kind=='wood' else dining_cane;finish_counts[kind]+=1
assert all(finish_counts.values()),finish_counts
olive_materials={};olive_parts=0
for obj in bpy.data.collections['03 Corner sofa'].all_objects:
 for slot in obj.material_slots:
  if slot.material and slot.material.name.startswith('Warm chalk brushed cotton'):
   original=slot.material
   if original.name not in olive_materials:
    olive=original.copy();olive.name='Combined earthy olive cotton'
    for node in olive.node_tree.nodes:
     if node.type=='VALTORGB':
      node.color_ramp.elements[0].color=(.0819,.1053,.0429,1);node.color_ramp.elements[1].color=(.1113,.1431,.0583,1)
    olive.diffuse_color=(.105,.135,.055,1);olive_materials[original.name]=olive
   slot.link='OBJECT';slot.material=olive_materials[original.name];olive_parts+=1
assert olive_parts>5,olive_parts
rug=bpy.data.objects['Generous woven lounge rug'];rug_material=rug.active_material.copy();rug_material.name='Combined faded ivory Persian woven rug'
nodes,links=rug_material.node_tree.nodes,rug_material.node_tree.links
texture=nodes.new('ShaderNodeTexImage');texture.name='Reference inspired faded Persian pattern';texture.image=bpy.data.images.load(str(R/'assets/furniture-study/faded-persian-rug.png'),check_existing=True);texture.extension='EXTEND';texture.image.pack()
coordinates=nodes.new('ShaderNodeTexCoord');links.new(coordinates.outputs['Generated'],texture.inputs['Vector']);links.new(texture.outputs['Color'],nodes['Principled BSDF'].inputs['Base Color'])
rug.material_slots[0].link='OBJECT';rug.material_slots[0].material=rug_material
# Keep the source scene untouched and record the few placement changes in this copy.
for c in bpy.data.collections:
 if c.name=='01 Table' or c.name.startswith('Approved cane dining chair'):
  for o in c.objects:
   if o.parent is None:o.matrix_world=Matrix.Translation((0,-.60,0))@o.matrix_world
for o in scene.objects:
 if any(s in o.name.lower() for s in ['chandelier']):o.matrix_world=Matrix.Translation((0,-.60,0))@o.matrix_world
for n in ['K02 - dark oak island','K03 - milk glass pendants','K09 - curved oak stools']:
 for o in bpy.data.collections[n].objects:
  if o.parent is None:o.matrix_world=Matrix.Translation((.075,.10,-.0105 if n=='K09 - curved oak stools' else 0))@o.matrix_world
for o in bpy.data.collections['K10 - herringbone floor'].objects:
 for v in o.data.vertices:v.co.z=.0395
for v in bpy.data.objects['Revised floor G2'].data.vertices:v.co.z=.030
removed=[]
for o in bpy.data.collections['K05 - revised ground shell'].objects:
 if o.name.startswith('Measured wall') and abs(o.location.x-6.625)<.02 and -9.1<o.location.y<-6.7 and o.location.z>2.4:o.hide_render=True;o.hide_set(True);removed.append(o.name)
assert len(removed)==7
for o in scene.objects:
 if o.name.startswith(('Proposed taller ', 'Proposed 3.2 m room ceiling', 'Proposed garden wall return', 'Proposed bifold head wall', 'Closed side garden doorway')) or (o.name.startswith('Measured wall') and min(o.dimensions)<.0001):o.hide_render=True;o.hide_set(True)

for y in [-6.68,-9.12]:box('Divider oak jamb',(6.625,y,1.62),(.12,.045,3.16),oak)
box('Divider upper track',(6.625,-7.9,2.425),(.14,2.44,.065),oak)
box('Divider ceiling rail',(6.625,-7.9,3.175),(.12,2.44,.05),oak)
for y in [-7.3,-7.9,-8.5]:box('Transom mullion',(6.625,y,2.805),(.075,.035,.71),oak)
for y in [-7,-7.6,-8.2,-8.8]:box('Fixed clear transom',(6.625,y,2.805),(.008,.557,.71),glass)
previous=None;hinges=[]
for i in range(4):
 hinge=bpy.data.objects.new('Folding divider hinge %d'%(i+1),None);col.objects.link(hinge);hinge.parent=previous;hinge.location=(6.625,-9.10,0) if previous is None else (0,.60,0);hinges.append(hinge);previous=hinge
 for y in [.023,.577]:o=box('Folding oak stile',(0,y,1.22),(.055,.046,2.34),oak);o.parent=hinge
 for z in [.076,2.364]:o=box('Folding oak rail',(0,.30,z),(.055,.508,.052),oak);o.parent=hinge
 o=box('Folding clear glass',(0,.30,1.22),(.008,.508,2.234),glass);o.parent=hinge
 o=box('Fine oak midrail',(0,.30,1.06),(.045,.508,.028),oak);o.parent=hinge
 if i==3:
  for x in [-.045,.045]:o=box('Divider bronze pull',(x,.53,1.13),(.017,.015,.19),bronze);o.parent=hinge
 for frame,angle in [(1,[-85,170,-170,170][i]),(60,0)]:hinge.rotation_euler.z=math.radians(angle);hinge.keyframe_insert(data_path='rotation_euler',frame=frame)
scene.frame_start=1;scene.frame_end=60;scene.timeline_markers.new('OPEN - connected rooms',frame=1);scene.timeline_markers.new('CLOSED - glazed kitchen',frame=60)
for j in range(12):box('Living dining oak slat',(.405+j*.10,-5.52,1.62),(.035,.075,3.16),oak)
for z in [.067,3.175]:box('Slat screen end rail',(.955,-5.52,z),(1.17,.09,.055),oak)
for obj in scene.objects:
 if obj.name.startswith('Natural oak floorboard'):obj.hide_render=True;obj.hide_set(True)
floor_material=bpy.data.materials['K01 pale oak herringbone']
box('Parquet joint backing',(3.45,-4.825,.020),(6.20,8.95,.024),floor_material)
def clip_floor(poly,axis,bound,sign):
 out=[]
 for first,last in zip(poly,poly[1:]+poly[:1]):
  inside_first=sign*(first[axis]-bound)>=0;inside_last=sign*(last[axis]-bound)>=0
  if inside_first:out.append(first)
  if inside_first!=inside_last:
   t=(bound-first[axis])/(last[axis]-first[axis]);out.append((first[0]+t*(last[0]-first[0]),first[1]+t*(last[1]-first[1])))
 return out
vertices=[];faces=[];uvs=[];root2=math.sqrt(.5);floor_random=random.Random(19)
for i in range(-20,21):
 for j in range(-90,91):
  ox=(6*i-j)*.12;oy=(4*i+j)*.12
  for x,y,w,h in [(ox,oy,.60,.12),(ox+.60,oy,.12,.60)]:
   poly=[(9+(px-py)*root2,7+(px+py)*root2) for px,py in [(x+.001,y+.001),(x+w-.001,y+.001),(x+w-.001,y+h-.001),(x+.001,y+h-.001)]]
   if max(q[0] for q in poly)<.35 or min(q[0] for q in poly)>6.7 or max(q[1] for q in poly)<.35 or min(q[1] for q in poly)>9.3:continue
   for x0,y0,x1,y1 in [(.35,.35,6.55,9.3),(6.55,6.7,6.7,9.1)]:
    clipped=poly
    for axis,bound,sign in [(0,x0,1),(0,x1,-1),(1,y0,1),(1,y1,-1)]:
     if clipped:clipped=clip_floor(clipped,axis,bound,sign)
    if len(clipped)<3:continue
    k=len(vertices);vertices.extend((px,-py,.0395) for px,py in clipped);faces.append(tuple(reversed(range(k,k+len(clipped)))));u0=floor_random.random();v0=floor_random.random()
    for px,py in clipped:
     rx=((px-9)+(py-7))*root2-x;ry=((py-7)-(px-9))*root2-y;uvs.append((u0+(rx if w>h else ry),v0+(ry if w>h else rx)))
mesh=bpy.data.meshes.new('Continuous living dining parquet');mesh.from_pydata(vertices,[],faces);mesh.update();obj=bpy.data.objects.new('Kitchen parquet extended through living and dining',mesh);col.objects.link(obj);mesh.materials.append(floor_material);uv=mesh.uv_layers.new(name='Physical oak grain')
for loop in mesh.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
assert len(faces)>500,len(faces)
curtain_material=bpy.data.materials['Cream linen upholstery']
box('Garden ceiling curtain track',(3.45,-.43,3.175),(6.20,.036,.026),bpy.data.materials['Warm ivory painted panelling'])
for start in [.36,5.82]:
 vertices=[];faces=[]
 for j in range(81):
  x=start+j*.72/80;wave=math.cos(j*math.tau/10)
  for k in range(25):
   t=k/24;vertices.append((x,-.43+.038*wave*(1+.08*(1-t)),.060+t*3.10+.004*math.sin(j*math.tau/10)*(1-t)))
 for j in range(80):
  for k in range(24):
   i=j*25+k;faces.append((i,i+25,i+26,i+1))
 mesh=bpy.data.meshes.new('Full height garden curtain folds');mesh.from_pydata(vertices,[],faces);mesh.update();obj=bpy.data.objects.new('Garden bifold full height linen curtain',mesh);col.objects.link(obj);mesh.materials.append(curtain_material)
 for face in mesh.polygons:face.use_smooth=True
 modifier=obj.modifiers.new('Linen fabric thickness','SOLIDIFY');modifier.thickness=.0015
# Lights are kept consistent across the open and closed comparisons.
for o in scene.objects:
 if o.type=='LIGHT':o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=True;scene.render.resolution_x=a.width;scene.render.resolution_y=round(a.width*2/3);scene.render.resolution_percentage=100;scene.camera.data.dof.use_dof=False
scene.frame_set(1);bpy.context.view_layer.update()
def bounds(objects):
 points=[o.matrix_world@Vector(c) for o in objects if o.type in ['MESH','CURVE'] and not o.hide_render for c in o.bound_box]
 return [[round(min(p[i] for p in points),4),round(max(p[i] for p in points),4)] for i in range(3)]
footprints={n:bounds(bpy.data.collections[n].all_objects) for n in ['01 Table','03 Corner sofa','04 Square footstool','05 Media cabinet proposal','K02 - dark oak island','K09 - curved oak stools']+[f'Approved cane dining chair {i:02}' for i in range(1,9)]}
folded=bounds([o for h in hinges for o in h.children if o.type in ['MESH','CURVE']]);print('FOLDED',folded);assert folded[0][1]<7.30 and folded[1][1]<-8.75,folded
screen=bounds([o for o in col.objects if o.name.startswith(('Living dining oak slat','Slat screen end rail'))]);sofa=footprints['03 Corner sofa'];assert screen[1][1]<sofa[1][0]-.5
island=footprints['K02 - dark oak island'];stools=footprints['K09 - curved oak stools'];northchairs=[footprints[f'Approved cane dining chair {i:02}'] for i in [1,3,5]]
checks={'island_to_sink_front':round(island[1][1]*-1-6.04,3),'island_to_pantry_front':round(10.933-island[0][1],3),'island_west_side':round(island[0][0]-6.7,3),'behind_stool_geometry':round(9.3+stools[1][0],3),'dining_chair_to_sofa':round(min(-b[1][1] for b in northchairs)+sofa[1][0],3),'dining_chair_to_sofa_after_400mm_pullout':round(min(-b[1][1] for b in northchairs)-.4+sofa[1][0],3),'east_dining_route_after_400mm_pullout':round(6.55-footprints['Approved cane dining chair 08'][0][1]-.4,3),'rear_dining_chair_after_400mm_pullout':round(9.3+footprints['Approved cane dining chair 02'][1][0]-.4,3),'folded_divider_clear_opening':round(-folded[1][1]-6.7025,3)}
assert checks['island_to_sink_front']>1 and checks['island_west_side']>.89 and checks['dining_chair_to_sofa_after_400mm_pullout']>.70
report={'source_sha256':source_hash,'ceiling_m':3.2,'first_floor_coordinated':False,'placements':{'dining_group_south_m':.6,'island_east_m':.075,'island_north_m':.1},'clearances_m':checks,'footprints':footprints,'divider':'Four glazed folding leaves; frame 1 open, frame 60 closed; mechanisms and stove installation require detailed design','screen':'1.17 m partial oak screen; 500+ mm clear of sofa','not_resolved':['Through-route behind occupied island stools','Pantry door swing with people or cabinet doors open','Access to high cupboards','Construction and first-floor level'],'views':[]}
if a.views and (O/'validation.json').exists():report['views']=json.loads((O/'validation.json').read_text())['views']
scene['combined_room_notes']=json.dumps(report['placements']);scene['divider_states']='Frame 1 open; frame 60 closed';scene['scope_note']='Coordinated Option D kitchen, approved dining/living furniture, folding glass divider and partial oak screen. A design study, not a construction model.'
views=[('dining-kitchen-open',(1.2,-8.65,1.65),(8.4,-6.65,1.35),23,1),('dining-kitchen-closed',(1.2,-8.65,1.65),(8.4,-6.65,1.35),23,60),('kitchen-dining',(10.65,-8.83,1.65),(2.7,-6.1,1.25),22,1),('living-dining-kitchen',(1.8,-.90,1.65),(4.5,-6.5,1.35),22,1),('arrival-living',(5.40,-9.07,1.65),(3.0,-3.3,1.35),23,1)]
for name,pos,target,lens,frame in views:
 if a.views and name not in a.views:continue
 scene.frame_set(frame);scene.camera.location=pos;scene.camera.rotation_euler=(Vector(target)-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.lens=lens;scene.render.filepath=str(O/(name+'.png'));bpy.ops.render.render(write_still=True);report['views']=list(dict.fromkeys([*report['views'],name+'.png']));(O/'validation.json').write_text(json.dumps(report,indent=2))
scene.frame_set(1);scene.camera.location=(1.2,-8.65,1.65);scene.camera.rotation_euler=(Vector((8.4,-6.65,1.35))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.lens=23;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'combined-kitchen-dining-living.blend'),compress=True)
assert hashlib.sha256(base.read_bytes()).hexdigest()==source_hash
(O/'validation.json').write_text(json.dumps(report,indent=2));print('COMBINED_COMPLETE',json.dumps(checks))
