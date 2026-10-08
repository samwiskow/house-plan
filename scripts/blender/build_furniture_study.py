"""Make isolated, zero-cost furniture previews without modifying the house scene."""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--samples', type=int, default=64)
parser.add_argument('--only', default='')
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
root = args.root.resolve()
out = root / 'output/blender/furniture-study'
out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.context.preferences.filepaths.save_version = 0
scene.unit_settings.system = 'METRIC'
scene.render.engine = 'CYCLES'
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'METAL'
prefs.get_devices()
for device in prefs.devices:
    device.use = device.type == 'METAL'
scene.cycles.device = 'GPU' if any(d.use for d in prefs.devices) else 'CPU'
scene.render.resolution_x = 1440
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
scene.world = bpy.data.worlds.new('Neutral studio')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.72, .77, .85, 1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = .35

with bpy.data.libraries.load(str(root / 'output/blender/living-study/living-study.blend'), link=False) as (src, dst):
    dst.materials = ['Weathered natural dining oak', 'Warm chalk brushed cotton',
                     'Plain oatmeal footstool linen', 'Cream linen upholstery',
                     'Warm ivory painted panelling', 'Brushed warm bronze']
wood, cotton, linen, seatmat, paint, brass = dst.materials

def solid(name, color, roughness=.65):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    p = mat.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = roughness
    return mat

cane = solid('Natural cane fibres', (.39, .28, .15), .72)
cord = solid('Oatmeal seam thread', (.47, .43, .36), .85)
floor = solid('Studio warm grey', (.57, .55, .51), .85)
# Rebuild the imported wood shader with bump mapping for meshes without UVs.
wood = solid('Pale weathered oak - furniture study', (.28,.19,.11), .65)
n, links = wood.node_tree.nodes, wood.node_tree.links
p = n.get('Principled BSDF')
tc=n.new('ShaderNodeTexCoord')
scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=1.15
links.new(tc.outputs['Object'],scale.inputs[0])
tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(root/'assets/living-study/oak_veneer_02_diff.jpg'),check_existing=True)
tex.image.pack();tex.projection='BOX';tex.projection_blend=.2
links.new(scale.outputs[0],tex.inputs['Vector'])
bw=n.new('ShaderNodeRGBToBW');links.new(tex.outputs['Color'],bw.inputs[0])
ramp=n.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position=.16;ramp.color_ramp.elements[0].color=(.035,.018,.008,1)
ramp.color_ramp.elements[1].position=.66;ramp.color_ramp.elements[1].color=(.28,.17,.082,1)
links.new(bw.outputs[0],ramp.inputs[0]);links.new(ramp.outputs[0],p.inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.23;bump.inputs['Distance'].default_value=.0012
links.new(bw.outputs[0],bump.inputs['Height']);links.new(bump.outputs[0],p.inputs['Normal'])
collections = {}
current = None

def collection(name):
    global current
    current = bpy.data.collections.new(name)
    scene.collection.children.link(current)
    collections[name] = current
    return current

def link(obj):
    for col in list(obj.users_collection): col.objects.unlink(obj)
    current.objects.link(obj)
    return obj

def box(name, pos, size, mat, radius=.005):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    obj = link(bpy.context.object); obj.name = name; obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    if radius:
        mod = obj.modifiers.new('Rounded edges', 'BEVEL'); mod.width = min(radius, min(size)*.45); mod.segments = 4
        obj.modifiers.new('Face normals', 'WEIGHTED_NORMAL')
    return obj

def mesh(name, verts, faces, mat, smooth=False):
    data = bpy.data.meshes.new(name); data.from_pydata(verts, [], faces); data.update()
    obj = bpy.data.objects.new(name, data); current.objects.link(obj); data.materials.append(mat)
    for poly in data.polygons: poly.use_smooth = smooth
    return obj

def curve(name, points, radius, mat, closed=False):
    data = bpy.data.curves.new(name, 'CURVE'); data.dimensions = '3D'; data.resolution_u = 16
    data.bevel_depth = radius; data.bevel_resolution = 3; data.use_fill_caps = True
    spline = data.splines.new('POLY'); spline.points.add(len(points)-1)
    for p, xyz in zip(spline.points, points): p.co = (*xyz, 1)
    spline.use_cyclic_u = closed
    obj = bpy.data.objects.new(name, data); current.objects.link(obj); data.materials.append(mat)
    return obj

def cushion(name, pos, size, mat, rotation=None):
    obj = box(name, pos, size, mat, min(size)*.42)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)
    for mod in list(obj.modifiers): obj.modifiers.remove(mod)
    sub = obj.modifiers.new('Upholstery surface', 'SUBSURF'); sub.levels = 4
    bpy.ops.object.modifier_apply(modifier=sub.name)
    axis = min(range(3), key=lambda i: size[i]); across = [i for i in range(3) if i != axis]
    for v in obj.data.vertices:
        q = [v.co[i]*2/size[i] for i in range(3)]
        full = (max(0, 1-q[across[0]]**2)*max(0, 1-q[across[1]]**2))**.65
        v.co[axis] += math.copysign(min(size)*.22*full*abs(q[axis])**6, q[axis])
        v.co[axis] += .0025*abs(q[axis])**4*(1-full)*math.sin(q[across[0]]*32+q[across[1]]*19)
    for poly in obj.data.polygons: poly.use_smooth = True
    tex = bpy.data.textures.new(name+' cloth folds', type='CLOUDS'); tex.noise_scale = .12; tex.noise_depth = 2
    dis = obj.modifiers.new('Soft fabric irregularity', 'DISPLACE'); dis.texture = tex; dis.strength = .003
    if rotation: obj.rotation_euler = rotation
    return obj

def piping(name, cx, cy, z, width, depth, mat=cord, radius=.002):
    points=[]; r=.065
    for x,y,a in [(cx+width/2-r,cy+depth/2-r,0),(cx-width/2+r,cy+depth/2-r,90),
                  (cx-width/2+r,cy-depth/2+r,180),(cx+width/2-r,cy-depth/2+r,270)]:
        for i in range(13):
            t=math.radians(a+i*90/12); points.append((x+r*math.cos(t), y+r*math.sin(t), z))
    return curve(name, points, radius, mat, True)

def sweep(name, stations, mat, segments=20):
    verts=[]; faces=[]
    for x,y,z,rx,ry in stations:
        verts.extend((x+rx*math.cos(2*math.pi*j/segments),y+ry*math.sin(2*math.pi*j/segments),z) for j in range(segments))
    for i in range(len(stations)-1):
        for j in range(segments):
            a=i*segments+j; b=i*segments+(j+1)%segments
            faces.append((a,b,b+segments,a+segments))
    faces.extend([tuple(reversed(range(segments))), tuple((len(stations)-1)*segments+j for j in range(segments))])
    obj=mesh(name,verts,faces,mat,True)
    sub=obj.modifiers.new('Smooth shaped timber','SUBSURF'); sub.levels=2
    return obj

collection('01 Table')
with bpy.data.libraries.load(str(root/'assets/furniture-study/vendor/monastery-free.blend'), link=False) as (src,dst):
    dst.objects=src.objects
for obj in dst.objects:
    if obj.name == 'Wooden monastery table':
        bpy.data.objects.remove(obj,do_unlink=True)
        continue
    current.objects.link(obj)
    obj.scale.x*=1.1091; obj.scale.y*=1.09
    obj.location.x*=1.1091; obj.location.y*=1.09
    obj.data.materials.clear(); obj.data.materials.append(wood)
    obj['source']='Floris Smit / BlenderKit Wooden monastery table; royalty-free, downloaded free'
    obj['adaptation']='Base widened and given pale oak material; original top replaced by thick planks'
# Replace the thin single slab with six thick boards and two breadboard ends.
for i in range(6):
    plank=box('Thick oak plank %02d'%i,(0,-.455+i*.182,.732),(2.16,.180,.08),wood,.006)
    plank.location.z+=.00035*math.sin(i*2.1)
for x in (-1.15,1.15):
    end=box('Breadboard end',(x,0,.732),(.14,1.09,.08),wood,.006)
    for y in (-.34,0,.34):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.006,depth=.001,location=(x,y,.7724))
        peg=link(bpy.context.object);peg.name='Oak dowel end grain';peg.data.materials.append(cane)

collection('02 Cane chair')
# A rounded crown and a gently reclined back; no decorative crest.
def back_y(z): return .18 + (z-.48)*.20
outline=[]
# Rounded rectangular back, narrower at its foot, with an arched crown.
for i in range(41):
    theta=math.pi*i/40
    outline.append((.205*math.cos(theta), .805+.15*math.sin(theta)))
outline += [(-.203,.76),(-.198,.68),(-.189,.58),(-.174,.535),(-.14,.522),(.14,.522),(.174,.535),(.189,.58),(.198,.68),(.203,.76)]
# Smooth the closed outline with Catmull-Rom interpolation.
smooth=[]
for i,p1 in enumerate(outline):
    p0=Vector(outline[(i-1)%len(outline)]);p1=Vector(p1);p2=Vector(outline[(i+1)%len(outline)]);p3=Vector(outline[(i+2)%len(outline)])
    for j in range(5):
        t=j/5;v=.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)
        smooth.append(tuple(v))
curve('Solid rounded oak back frame',[(x,back_y(z),z) for x,z in smooth],.023,wood,True)
curve('Fine inner back moulding',[(x*.92,back_y(z)-.009,.738+(z-.738)*.94) for x,z in smooth],.004,wood,True)
curve('Outer back moulding',[(x*1.07,back_y(z)-.004,.738+(z-.738)*1.03) for x,z in smooth],.0035,wood,True)

def inside(x,z):
    if z<.544 or z>.928:return False
    width=.164+(min(z,.80)-.544)*.09
    if z>.80:width=.182*math.sqrt(max(0,1-((z-.80)/.128)**2))
    return abs(x)<width
# Model cane strands with real gaps so the back remains open in close views.
verts=[]; faces=[]
for angle, spacing, strand_width in [(0,.012,.0020),(math.pi/2,.012,.0020),(math.pi/4,.017,.0015),(-math.pi/4,.017,.0015)]:
    dx,dz=math.cos(angle),math.sin(angle);nx,nz=-dz,dx
    for k in range(-65,66):
        valid=[]
        for j in range(241):
            t=(j-120)*.004
            x=nx*k*spacing+dx*t; z=.735+nz*k*spacing+dz*t
            if inside(x,z):valid.append((x,z,t))
        if len(valid)<2:continue
        start=len(verts)
        for j,(x,z,t) in enumerate(valid):
            y=back_y(z)+.002*math.sin(t*2*math.pi/.024+k*math.pi)
            for sign in (-1,1):verts.append((x+sign*nx*strand_width/2,y,z+sign*nz*strand_width/2))
            if j:faces.append((start+2*j-2,start+2*j-1,start+2*j+1,start+2*j))
web=mesh('Open woven cane webbing',verts,faces,cane)
solidify=web.modifiers.new('Cane ribbon thickness','SOLIDIFY');solidify.thickness=.0006
for sx in (-1,1):
    sweep('Cabriole front leg',[(sx*.245,-.235,.025,.022,.021),(sx*.25,-.23,.04,.023,.022),
        (sx*.224,-.216,.16,.016,.018),(sx*.224,-.204,.27,.019,.02),
        (sx*.25,-.208,.365,.03,.028),(sx*.231,-.20,.43,.027,.024)],wood)
    sweep('Swept back leg and post',[(sx*.208,.27,.02,.018,.021),(sx*.20,.255,.055,.018,.021),
        (sx*.185,.205,.32,.019,.022),(sx*.18,.192,.48,.021,.022),(sx*.183,back_y(.65),.65,.017,.02)],wood)
    curve('Seat side rail',[(sx*.225,-.23,.418),(sx*.23,-.10,.405),(sx*.20,.19,.418)],.022,wood)
curve('Scalloped front apron',[(-.257,-.23,.417),(-.19,-.242,.425),(-.09,-.253,.402),(0,-.256,.398),(.09,-.253,.402),(.19,-.242,.425),(.257,-.23,.417)],.025,wood)
box('Rear seat rail',(0,.183,.42),(.37,.043,.055),wood)
# The cover wraps into the seat frame; there is no separate cushion or lower welt.
verts=[(0,-.025,.475)];faces=[];segments=96
for radius in (.25,.5,.75,.9,1):
    for j in range(segments):
        t=2*math.pi*j/segments
        c,s=math.cos(t),math.sin(t)
        x=math.copysign(abs(c)**.48,c)
        y=math.copysign(abs(s)**.48,s)
        halfwidth=.230-.009*y
        z=.475-.035*radius**4
        verts.append((radius*x*halfwidth,-.025+radius*y*.235,z))
for j in range(segments):faces.append((0,1+j,1+(j+1)%segments))
for ring in range(4):
    for j in range(segments):
        a=1+ring*segments+j;b=1+ring*segments+(j+1)%segments
        faces.append((a,a+segments,b+segments,b))
start=len(verts)
for j in range(segments):
    x,y,z=verts[1+4*segments+j]
    verts.append((x*.986,-.025+(y+.025)*.986,.395))
for j in range(segments):
    a=1+4*segments+j;b=1+4*segments+(j+1)%segments
    faces.append((a,start+j,start+(j+1)%segments,b))
faces.append(tuple(reversed(range(start,start+segments))))
fixed_seat=mesh('Fixed upholstered seat',verts,faces,seatmat,True)
fixed_seat['construction']='Shallow crowned upholstery wrapped into the timber seat frame; not a loose pad'

collection('03 Corner sofa')
# Use the existing custom sofa as the base, with no loose scatter cushions.
with bpy.data.libraries.load(str(root/'output/blender/living-study/living-study.blend'),link=False) as (src,dst):
    dst.objects=src.objects
loaded=[o for o in dst.objects if o]
sofa=next(o for o in loaded if o.name=='Large oatmeal corner sofa')
keep=set([sofa]); pending=[sofa]
while pending:
    obj=pending.pop()
    children=[o for o in loaded if o.parent==obj]
    keep.update(children);pending.extend(children)
for obj in loaded:
    if obj in keep:current.objects.link(obj)
    else:bpy.data.objects.remove(obj,do_unlink=True)
sofa.location=(0,0,0);sofa.rotation_euler=(0,0,0)
for obj in keep:
    if obj.name=='Corner return end arm':
        obj.scale.x*=1.018
        obj.scale.y*=1.072
    if obj.type=='MESH' and ('cushion' in obj.name.lower()):
        obj['status']='Custom reference-based approximation, not a Frankof or Loaf downloaded product model'
# A neutral studio orientation puts the open corner towards the camera.

collection('04 Square footstool')
box('Upholstered square base',(0,0,.245),(1.21,1.21,.24),linen,.07)
cushion('Full square cushion',(0,0,.393),(1.25,1.25,.18),linen)
piping('Top edge piping',0,0,.393,1.225,1.225,linen,.0018)
for x in (-.48,.48):
    for y in (-.48,.48):
        sweep('Short turned oak foot',[(x,y,.025,.026,.026),(x,y,.045,.037,.037),(x,y,.075,.031,.031),(x,y,.11,.04,.04),(x,y,.14,.04,.04)],wood)

collection('05 Media cabinet proposal')
# Simple country joinery is provisional; the rejected catalogue cabinet is not used.
box('Inset backing',(0,.197,.39),(2.02,.025,.45),wood)
for x in (-1.01,1.01):box('Solid cabinet side',(x,0,.38),(.045,.416,.48),wood)
for z in (.155,.605):box('Oak cabinet bottom or top rail',(0,0,z),(2.04,.42,.04),wood)
box('Thick overhanging oak top',(0,0,.645),(2.14,.46,.045),wood,.008)
for x in (-.325,.325):box('Compartment upright',(x,0,.39),(.03,.41,.46),wood)
box('Open central shelf',(0,0,.365),(.62,.405,.027),wood)
for x in (-.674,.674):
    # Recessed panel with separate rails and stiles.
    box('Recessed door field',(x,-.183,.39),(.57,.025,.345),paint,.002)
    for side in (-1,1):box('Oak door stile',(x+side*.287,-.209,.39),(.055,.032,.43),wood,.003)
    for z in (.202,.578):box('Oak door rail',(x,-.209,z),(.519,.032,.055),wood,.003)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.014,location=(x+(.23 if x<0 else -.23),-.239,.50))
    knob=link(bpy.context.object);knob.name='Small aged brass knob';knob.data.materials.append(brass)
for x in (-.94,.94):
    for y in (-.155,.155):box('Short tapered-style cabinet foot',(x,y,.09),(.07,.07,.14),wood,.008)

collection('Studio')
box('Studio floor',(0,0,-.05),(200,200,.1),floor,.002)
bpy.ops.object.camera_add();camera=link(bpy.context.object);camera.name='Furniture review camera';scene.camera=camera
camera.data.type='ORTHO';camera.data.lens=50
for name,pos,power,size in [('Large left softbox',(-3,-4,6),1000,5),('Right fill',(4,1,4),600,4),('Back rim',(-2,4,4),700,3)]:
    bpy.ops.object.light_add(type='AREA',location=pos);light=link(bpy.context.object);light.name=name
    light.data.energy=power;light.data.shape='DISK';light.data.size=size
    light.rotation_euler=(Vector((0,0,.4))-light.location).to_track_quat('-Z','Y').to_euler()

for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    for node in list(mat.node_tree.nodes):
        if node.type=='NORMAL_MAP':
            for output in node.outputs:
                for edge in list(output.links):mat.node_tree.links.remove(edge)

views=[('table','01 Table',(3.2,-4.4,2.6),(0,0,.39),3.30),
       ('chair','02 Cane chair',(1.25,-1.9,1.27),(0,.05,.49),1.78),
       ('sofa','03 Corner sofa',(-5.5,-7.4,4.6),(0,-1.5,.35),6.1),
       ('footstool','04 Square footstool',(2,-2.5,1.7),(0,0,.22),2.03),
       ('media-cabinet','05 Media cabinet proposal',(2.7,-4,2.1),(0,0,.32),2.9)]
report={'cost':0,'scope':'Isolated furniture study; house scene unchanged','renderer':'Cycles',
        'source_table':'https://www.blendkit.com/asset-gallery-detail/6f6bf86f-e227-42ba-a3eb-646081d93a0d/',
        'table_license':'BlenderKit royalty-free; source and editable study kept local',
        'custom_models':['Cane chair','Square footstool','Corner sofa adapted from existing custom study','Media cabinet proposal'],
        'sofa_note':'Approved custom sofa; no downloaded Frankof or Loaf product model',
        'dimensions_m':{},'renders':[]}
for name,colname,position,target,scale in views:
    for key,col in collections.items():col.hide_render=key not in (colname,'Studio');col.hide_viewport=col.hide_render
    bpy.context.view_layer.update()
    points=[]
    deps=bpy.context.evaluated_depsgraph_get()
    for obj in collections[colname].objects:
        if obj.type in ('MESH','CURVE'):
            evaluated=obj.evaluated_get(deps)
            surface=evaluated.to_mesh()
            points.extend(evaluated.matrix_world @ v.co for v in surface.vertices)
            evaluated.to_mesh_clear()
    min_z=min(p.z for p in points)
    for obj in collections[colname].objects:
        if obj.parent is None:obj.location.z-=min_z
    bpy.context.view_layer.update()
    report['dimensions_m'][name]=[round(max(p[i] for p in points)-min(p[i] for p in points),3) for i in range(3)]
    camera.location=position;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=scale
    if not args.only or args.only==name:
        scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    if (out/(name+'.png')).exists():report['renders'].append(name+'.png')
# Save a tidy scene with each review piece separated, while retaining real dimensions.
for key,col in collections.items():col.hide_render=False;col.hide_viewport=False
for key,offset in [('01 Table',(-3,0,0)),('02 Cane chair',(-3,-1.1,0)),('03 Corner sofa',(2,1.5,0)),('04 Square footstool',(1,-.5,0)),('05 Media cabinet proposal',(-3,2,0))]:
    for obj in collections[key].objects:
        if obj.parent is None:obj.location+=Vector(offset)
scene['review_scope']='Separate furniture studies. Furniture direction approved 7 October 2026; chair seat fixed into frame. Room integration is a separate file.'
camera.location=(9,-12,11)
camera.rotation_euler=(Vector((0,-.5,.3))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.ortho_scale=12
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'furniture-study.blend'),compress=True)
(out/'report.json').write_text(json.dumps(report,indent=2))
print('FURNITURE_REPORT',json.dumps(report))
