"""Build the brief-led living/dining realism benchmark from the measured scene."""
import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, default=Path('.'))
parser.add_argument('--width', type=int, default=1600)
parser.add_argument('--samples', type=int, default=128)
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
root = args.root.resolve()
out = root / 'output/blender/living-study'
out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root / 'output/blender/l-house/l-house.blend'))
bpy.context.preferences.filepaths.save_version = 0
scene = bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='METAL'
prefs.get_devices()
for device in prefs.devices:device.use=device.type=='METAL'
scene.cycles.device='GPU' if any(d.type=='METAL' for d in prefs.devices) else 'CPU'
random.seed(41)
col = bpy.data.collections.new('Living study - detailed furniture and finishes')
scene.collection.children.link(col)

def link(obj):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def colour(hex):
    a = [int(hex[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a)

def material(name, hex, rough=.6, metal=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*colour(hex),1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m

ivory=material('Warm ivory lime plaster','eee5d2',.88)
bronze=material('Brushed warm bronze','806044',.32,.78)
green=material('Forest green painted joinery','244d37',.52)
cream=material('Honed cream worktop','d9c8a9',.58)
ceramic=material('Handmade cream ceramic','d2bc94',.65)
leafm=material('Fresh foliage','49633a',.72)

# Physical-scale object coordinates retain continuous texture across furniture pieces.
def textured(name, tint, asset, scale, fabric=False):
    m=material(name,tint,.8 if fabric else .42)
    n,l=m.node_tree.nodes,m.node_tree.links;p=n.get('Principled BSDF')
    tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=scale
    l.new(tc.outputs['Object'],mapping.inputs[0])
    for kind in ('diff','nor_gl','rough'):
        t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(root/'assets/living-study'/f'{asset}_{kind}.jpg'),check_existing=True)
        t.image.colorspace_settings.name='sRGB' if kind=='diff' else 'Non-Color';t.image.pack();t.projection='BOX';t.projection_blend=.15
        l.new(mapping.outputs[0],t.inputs['Vector'])
        if kind=='diff':
            if fabric:
                bw=n.new('ShaderNodeRGBToBW');l.new(t.outputs['Color'],bw.inputs[0])
                ramp=n.new('ShaderNodeValToRGB');base=colour(tint)
                ramp.color_ramp.elements[0].position=.05;ramp.color_ramp.elements[0].color=(*(v*.52 for v in base),1)
                ramp.color_ramp.elements[1].position=.9;ramp.color_ramp.elements[1].color=(*(min(v*1.18,1) for v in base),1)
                l.new(bw.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
            else:l.new(t.outputs['Color'],p.inputs['Base Color'])
        elif kind=='nor_gl':
            normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.35 if fabric else .25
            l.new(t.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs[0],p.inputs['Normal'])
        else:
            remap=n.new('ShaderNodeMapRange');remap.inputs['To Min'].default_value=.65 if fabric else .3;remap.inputs['To Max'].default_value=.95 if fabric else .6
            l.new(t.outputs[0],remap.inputs[0]);l.new(remap.outputs[0],p.inputs['Roughness'])
    if fabric:p.inputs['Sheen Weight'].default_value=.35
    return m

oak=textured('Natural honey oak','be9b66','oak_veneer_02',1.2)
floor_oak=textured('Matte natural oak floor','be9b66','oak_veneer_02',.7)
n,l=floor_oak.node_tree.nodes,floor_oak.node_tree.links
info=n.new('ShaderNodeObjectInfo')
variation=n.new('ShaderNodeMapRange');variation.inputs['To Min'].default_value=.86;variation.inputs['To Max'].default_value=1.06
l.new(info.outputs['Random'],variation.inputs['Value'])
p=n.get('Principled BSDF');base=p.inputs['Base Color'].links[0].from_socket
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
l.new(base,mix.inputs[1]);l.new(variation.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
for remap in [node for node in n if node.type=='MAP_RANGE' and node!=variation]:
    remap.inputs['To Min'].default_value=.5;remap.inputs['To Max'].default_value=.7

oatmeal=textured('Deep oatmeal woven upholstery','bdae95','terlenka',5,True)
linen=textured('Cream linen upholstery','e4d7bd','terlenka',5,True)
forest=textured('Forest green linen accent','34553e','terlenka',5,True)
rust=textured('Muted tobacco accent','a27450','terlenka',5,True)
rugmat=textured('Muted rust woven rug','994d3c','terlenka',3,True)
panelpaint=material('Warm ivory painted panelling','d8cbb4',.66)
shutterpaint=material('Ivory plantation shutters','eee4cf',.56)
antique=textured('Aged oak dining table','8c603c','oak_veneer_02',1.2)
n,l=antique.node_tree.nodes,antique.node_tree.links;p=n.get('Principled BSDF')
base=p.inputs['Base Color'].links[0].from_socket
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.47,.34,.22,1)
l.new(base,mix.inputs[1]);l.new(mix.outputs[0],p.inputs['Base Color'])

stone=material('Warm buff limestone-effect floor','d1c0a2',.74)
n,l=stone.node_tree.nodes,stone.node_tree.links;p=n.get('Principled BSDF')
tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3;noise.inputs['Detail'].default_value=4
l.new(tc.outputs['Object'],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*colour('bcaa8c'),1);r.color_ramp.elements[1].color=(*colour('e4d4b7'),1)
l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=140;l.new(tc.outputs['Object'],fine.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.001
l.new(fine.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])

def box(name,loc,dim,mat,bevel=.008,parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=link(bpy.context.object);o.name=name;o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Soft manufactured edge','BEVEL');mod.width=min(bevel,min(dim)*.45);mod.segments=4
        mod=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    if parent:o.parent=parent;o.location=loc
    return o

def curve(name,points,radius,mat,parent=None,closed=False):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=radius;d.bevel_resolution=3;d.use_fill_caps=True
    s=d.splines.new('POLY');s.points.add(len(points)-1)
    for p,v in zip(s.points,points):p.co=(*v,1)
    s.use_cyclic_u=closed;o=bpy.data.objects.new(name,d);col.objects.link(o);o.data.materials.append(mat);o.parent=parent;return o

def cylinder(name,a,b,r,mat,parent=None,r2=None):
    a,b=Vector(a),Vector(b);v=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=r,radius2=r if r2 is None else r2,depth=v.length,location=(a+b)/2)
    o=link(bpy.context.object);o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    if parent:o.parent=parent
    return o

def group(name,loc,angle=0):
    o=bpy.data.objects.new(name,None);col.objects.link(o);o.location=loc;o.rotation_euler.z=angle;return o

def cushion(name,loc,dim,mat,parent,tilt=0):
    o=box(name,loc,dim,mat,min(dim)*.36,parent)
    bpy.context.view_layer.objects.active=o
    bpy.ops.object.modifier_apply(modifier=o.modifiers[0].name)
    for m in list(o.modifiers):o.modifiers.remove(m)
    sub=o.modifiers.new('Soft cushion surface','SUBSURF');sub.levels=2
    tex=bpy.data.textures.new(name+' cloth irregularity',type='CLOUDS');tex.noise_scale=.16;tex.noise_depth=1
    dis=o.modifiers.new('Small upholstery creases','DISPLACE');dis.texture=tex;dis.strength=.005;dis.mid_level=.5
    o.rotation_euler.x=tilt
    for p in o.data.polygons:p.use_smooth=True
    return o

def seam(name,cx,cy,z,w,d,mat,parent):
    pts=[];rad=.06
    for x,y,a in [(cx+w/2-rad,cy+d/2-rad,0),(cx-w/2+rad,cy+d/2-rad,90),(cx-w/2+rad,cy-d/2+rad,180),(cx+w/2-rad,cy-d/2+rad,270)]:
        for j in range(9):
            t=math.radians(a+j*90/8);pts.append((x+rad*math.cos(t),y+rad*math.sin(t),z))
    return curve(name,pts,.0018,mat,parent,True)

def hide_tree(o):
    o.hide_render=True;o.hide_set(True)
    for c in o.children:hide_tree(c)

source_model=json.loads((root/'viewer-l-house/model.json').read_text())
for o in list(bpy.data.objects):
    if o.parent and o.parent.name=='g' and (o.get('room')=='G1' or (o.get('room')=='G2' and not o.name.startswith('Island seat'))):hide_tree(o)
    if o.parent and o.parent.name=='g' and o.type=='MESH':
        if o.name in ('g / oak','g / oak.001'):hide_tree(o)
        if o.data.materials[0].name=='#f6e8c6' and o.location.x<7 and o.location.y>-9.4:hide_tree(o)
        for mod in o.modifiers:
            if mod.type=='BEVEL':mod.width=.0003

# Retain the measured source objects; the garden opening has a separate proposed replacement.
for mat in list(bpy.data.materials):
    if mat.name=='ivory':
        for o in bpy.data.objects:
            if o.type=='MESH' and o.parent and (o.parent.name=='g' or o.parent.name=='Ceiling g'):
                for slot in o.material_slots:
                    if slot.material==mat:slot.material=ivory

floor_random=random.Random(83)
for ix in range(33):
    x=.35+ix*.19;w=min(.19,6.55-x)
    if w<=0:continue
    z=.35-floor_random.uniform(.3,1.8)
    while z<9.3:
        end=min(z+floor_random.uniform(1.6,2.4),9.3)
        start=max(z,.35)
        if end>start:
            board=box('Natural oak floorboard',(x+w/2,-(start+end)/2,.022),(end-start-.001,w-.001,.035),floor_oak,.0006)
            board.rotation_euler.z=math.pi/2
        z=end
# The kitchen retains its proposed stone finish within the existing polygon.
original=bpy.data.objects.get('g / oak.001')
if original:
    clone=bpy.data.objects.new('Kitchen stone floor',original.data.copy());col.objects.link(clone);clone.matrix_world=original.matrix_world;clone.data.materials.clear();clone.data.materials.append(stone)

rug=box('Generous woven lounge rug',(3,-2.75,.056),(3.5,3.8,.023),rugmat,.012)
for side in (-1,1):
    for i in range(165):
        y=-4.60+i*3.70/164
        curve('Rug fringe',[(3+side*1.75,y,.064),(3+side*(1.79+random.random()*.025),y+random.uniform(-.006,.006),.052)],.0013,linen)

sofa=group('Oatmeal corner sofa',(1.2,-2.45,0),math.pi/2)
sofa['proposed_plan_bounds']=[.7,1.05,2.25,2.8]
box('Sofa upholstered base',(0,0,.29),(2.78,.98,.28),oatmeal,.09,sofa)
box('Sofa back shell',(0,.37,.69),(2.75,.20,.60),oatmeal,.07,sofa)
for x in (-1.29,):box('Soft sofa arm',(x,0,.58),(.20,.98,.58),oatmeal,.09,sofa)
for x in (-.84,0,.84):
    cushion('Seat cushion',(x,-.05,.49),(.82,.76,.20),oatmeal,sofa)
    seam('Seat piping',x,-.05,.565,.78,.71,oatmeal,sofa)
    cushion('Back cushion',(x,.27,.78),(.83,.23,.49),oatmeal,sofa,-.13)
for x in (-1.16,1.16):
    for y in (-.34,.34):cylinder('Oak sofa foot',(x,y,.04),(x,y,.20),.042,oak,sofa,r2=.033)
for x,mat,angle in [(-.96,forest,.12),(.91,rust,-.18)]:
    o=cushion('Loose accent cushion',(x,.07,.79),(.40,.18,.40),mat,sofa,-.18);o.rotation_euler.y=angle

box('Corner return upholstered base',(.91,-1.05,.29),(.98,1.35,.28),oatmeal,.09,sofa)
box('Corner return back',(1.29,-.85,.69),(.20,1.72,.60),oatmeal,.07,sofa)
box('Corner return end arm',(.91,-1.65,.58),(.98,.20,.58),oatmeal,.07,sofa)
cushion('Corner return seat',(.89,-1.08,.49),(.80,1.13,.20),oatmeal,sofa)
seam('Return seat piping',.89,-1.08,.565,.76,1.08,oatmeal,sofa)
back=cushion('Corner return back cushion',(1.19,-.96,.78),(.23,1.05,.49),oatmeal,sofa)
back.rotation_euler.y=.12
for x in (.57,1.19):cylinder('Corner return oak foot',(x,-1.5,.04),(x,-1.5,.20),.042,oak,sofa,r2=.033)

arm=group('Cream lounge armchair',(4.225,-1.075,0),0)
arm['approved_footprint']=[3.8,.65,.85,.85]
for x in (-.32,.32):
    for y in (-.3,.3):cylinder('Armchair tapered foot',(x,y,.04),(x*.88,y*.88,.39),.033,oak,arm,r2=.025)
cushion('Cream chair seat',(0,-.02,.46),(.77,.76,.19),linen,arm)
cushion('Cream chair back',(0,.29,.76),(.74,.20,.53),linen,arm,-.14)
for x in (-.38,.38):box('Upholstered arm',(x,0,.58),(.09,.73,.24),linen,.035,arm)

coffee=group('Low rounded oak coffee table',(3.25,-2.85,0))
coffee['proposed_plan_bounds']=[2.65,2.45,1.2,.8]
box('Solid oak coffee top',(0,0,.39),(1.20,.80,.045),oak,.022,coffee)
for x in (-.46,.46):
    for y in (-.26,.26):cylinder('Coffee table leg',(x,y,.045),(x*.85,y*.85,.375),.035,oak,coffee,r2=.045)

media=group('Oak media sideboard',(6.1,-2.5,0),-math.pi/2)
media['approved_footprint']=[5.9,1.1,.4,2.8]
box('Media cabinet body',(0,0,.35),(2.80,.39,.49),oak,.007,media)
for x in (-1.04,-.35,.35,1.04):
    box('Quiet oak cabinet front',(x,-.203,.35),(.676,.021,.44),oak,.002,media)
    cylinder('Bronze pull',(x+.23,-.226,.32),(x+.23,-.226,.43),.005,bronze,media)
for x in (-1.23,1.23):cylinder('Sideboard foot',(x,0,.04),(x,0,.16),.025,oak,media)
black=material('Television dark glass','151b18',.22,.15)
box('Television',(6.49,-2.50,1.37),(.04,1.63,.94),black,.012)

# The table and chairs retain their measured centres and facing directions.
dining=group('Antique-style oak dining table',(3.1,-6.6,0))
dining['approved_footprint']=[1.7,6.05,2.8,1.1]
for j in range(5):
    box('Aged oak tabletop plank',(0,-.44+j*.22,.755),(2.50,.219,.05),antique,.003,dining)
for x in (-1.325,1.325):box('Breadboard table end',(x,0,.755),(.15,1.1,.05),antique,.004,dining)
box('Antique table apron',(0,0,.655),(2.40,.77,.15),antique,.006,dining)
profile=[(.04,.032),(.07,.044),(.10,.037),(.19,.028),(.32,.033),(.40,.057),(.45,.063),(.49,.042),(.52,.031),(.56,.045),(.59,.046),(.61,.040),(.72,.040)]
for x in (-1.08,1.08):
    for y in (-.37,.37):
        verts=[];faces=[]
        for h,r in profile:
            for j in range(48):verts.append((x+r*math.cos(j*math.tau/48),y+r*math.sin(j*math.tau/48),h))
        for k in range(len(profile)-1):
            for j in range(48):faces.append((k*48+j,k*48+(j+1)%48,(k+1)*48+(j+1)%48,(k+1)*48+j))
        faces.extend([tuple(reversed(range(48))),tuple((len(profile)-1)*48+j for j in range(48))])
        mesh=bpy.data.meshes.new('Turned oak leg');mesh.from_pydata(verts,[],faces)
        leg=bpy.data.objects.new('Turned antique table leg',mesh);col.objects.link(leg);leg.parent=dining;mesh.materials.append(antique)
        for face in mesh.polygons:face.use_smooth=True

def chair(x,z,angle):
    g=group('Detailed oak dining chair',(x,-z,0),angle)
    for xx in (-.18,.18):
        for yy in (-.18,.18):cylinder('Tapered chair leg',(xx*1.13,yy*1.1,.04),(xx,yy,.45),.021,oak,g,r2=.027)
    box('Oak seat frame',(0,0,.425),(.48,.46,.055),oak,.017,g)
    cushion('Linen dining seat',(0,-.015,.47),(.46,.435,.08),linen,g)
    for xx in (-.20,.20):cylinder('Back post',(xx,.18,.41),(xx,.22,.89),.021,oak,g,r2=.018)
    pts=[]
    for i in range(33):
        xx=-.215+i*.43/32;pts.append((xx,.20+.055*(1-(xx/.215)**2),.89))
    curve('Curved oak back rail',pts,.028,oak,g)
    for xx in (-.13,0,.13):cylinder('Fine back spindle',(xx,.19,.47),(xx,.23,.87),.009,oak,g)
    return g
for f in source_model['default']['furniture']:
    if f['roomId']=='G1' and f['name']=='Dining chair':
        x,z,w,d=f['r'];angle=math.pi if z>6.6 else 0
        if x<1.7:angle=math.pi/2
        if x>4.5:angle=-math.pi/2
        g=chair(x+w/2,z+d/2,angle);g['approved_footprint']=f['r']

# Six-arm bronze chandelier with ivory shades, as specified in the styling brief.
cx,cy=3.1,-6.6
cylinder('Chandelier suspension',(cx,cy,2.68),(cx,cy,2.13),.013,bronze)
for i in range(6):
    a=i*math.tau/6;ex,ey=cx+.50*math.cos(a),cy+.50*math.sin(a)
    curve('Swept bronze chandelier arm',[(cx,cy,2.15),(cx+.18*math.cos(a),cy+.18*math.sin(a),2.0),(ex,ey,1.99),(ex,ey,2.10)],.012,bronze)
    verts=[];faces=[]
    for z,radius in [(2.08,.14),(2.32,.088)]:
        for j in range(48):verts.append((ex+radius*math.cos(j*math.tau/48),ey+radius*math.sin(j*math.tau/48),z))
    for j in range(48):faces.append((j,(j+1)%48,(j+1)%48+48,j+48))
    mesh=bpy.data.meshes.new('Open linen shade');mesh.from_pydata(verts,[],faces);o=bpy.data.objects.new('Ivory chandelier shade',mesh);col.objects.link(o);o.data.materials.append(linen)
    mod=o.modifiers.new('Shade thickness','SOLIDIFY');mod.thickness=.001
    light=bpy.data.lights.new('Warm chandelier bulb','POINT');light.energy=5;light.color=(1,.76,.48);light.shadow_soft_size=.08
    o=bpy.data.objects.new(light.name,light);col.objects.link(o);o.location=(ex,ey,2.16)

# Shutter panels sit inside the existing window reveals with open louvres.
for z,w in [(1.4,2.4),(5.8,2.2)]:
    box('Oak window sill',(.28,-z-w/2,.84),(.38,w+.13,.035),oak,.009)
    for panel in range(4):
        start=z+panel*w/4;end=start+w/4
        frame=group('Plantation shutter panel',(.405,-(start+end)/2,0))
        width=w/4-.006
        for yy in (-width/2+.017,width/2-.017):box('Shutter stile',(0,yy,1.625),(.045,.034,1.51),shutterpaint,.002,frame)
        for h in (.89,1.43,2.36):box('Shutter rail',(0,0,h),(.045,width-.068,.044),shutterpaint,.002,frame)
        for j in range(21):
            h=.963+j*.064
            if abs(h-1.43)<.045:continue
            slat=box('Plantation shutter louvre',(0,0,h),(.082,width-.072,.008),shutterpaint,.003,frame)
            slat.rotation_euler.y=math.radians(20)
        for a,b in ((.955,1.37),(1.49,2.275)):
            box('Shutter tilt rod',(.055,0,(a+b)/2),(.011,.012,b-a),shutterpaint,.003,frame)

for x in (.361,6.539):
    intervals=[(.35,9.3)] if x<1 else [(.35,3.95),(4.9,6.7),(9.1,9.3)]
    for a,b in intervals:box('Ivory skirting',(x,-(a+b)/2,.097),(.025,b-a,.125),panelpaint,.003)

def panelling(x,a,b,height):
    depth=.018;front=x+(.022 if x<1 else -.022)
    box('Painted wall panelling',(x,-(a+b)/2,(height+.15)/2),(depth,b-a,height-.15),panelpaint,.002)
    box('Panel dado cap',(front,-(a+b)/2,height),(.045,b-a,.035),panelpaint,.003)
    count=max(1,round((b-a)/.85));pitch=(b-a)/count
    for i in range(count):
        start=a+i*pitch+.095;end=a+(i+1)*pitch-.095
        for zz in (start,end):box('Panel vertical moulding',(front,-zz,(height+.15)/2),(.015,.023,height-.33),panelpaint,.003)
        for h in (.24,height-.09):box('Panel horizontal moulding',(front,-(start+end)/2,h),(.015,end-start,.023),panelpaint,.003)
for a,b in ((.42,3.88),(4.97,6.62)):panelling(6.532,a,b,1.10)
for a,b,h in ((.42,1.36,1.10),(1.40,3.8,.79),(3.84,5.76,1.10),(5.8,8,.79),(8.04,9.26,1.10)):panelling(.37,a,b,h)

# The approved garden-door study replaces only the three source ground-floor wall sections.
for name in ('g / stone','g / stone.002','g / stone.004','Living to terrace'):
    hide_tree(bpy.data.objects[name])
for x in (.275,6.625):box('Proposed garden wall return',(x,-.175,1.35),(.55,.35,2.7),ivory,.001)
box('Proposed bifold head wall',(3.45,-.175,2.55),(5.8,.35,.30),ivory,.001)
for x in (.575,6.325):box('Bifold outer jamb',(x,-.175,1.22),(.05,.105,2.36),bronze,.002)
for h in (.055,2.375):box('Bifold continuous track',(3.45,-.175,h),(5.80,.105,.05),bronze,.002)
glass=material('Bifold clear glazing','f1f6f4',.025)
glass.node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=1
glass.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.45
leafwidth=5.70/6
for side in (0,1):
    px=.60 if side==0 else 6.30;py=-.175
    for index in range(3):
        angle=math.radians((75 if index%2==0 else -75) if side==0 else (105 if index%2==0 else 255))
        door=group('Garden bifold leaf',(px,py,0),angle)
        for x in (.025,leafwidth-.025):box('Bifold leaf stile',(x,0,1.215),(.05,.065,2.27),bronze,.002,door)
        for h in (.105,2.325):box('Bifold leaf rail',(leafwidth/2,0,h),(leafwidth-.10,.065,.05),bronze,.002,door)
        box('Bifold glazing',(leafwidth/2,0,1.215),(leafwidth-.10,.018,2.17),glass,.0005,door)
        for h in (.30,1.2,2.1):cylinder('Bifold hinge',(.025,.042,h-.035),(.025,.042,h+.035),.009,bronze,door)
        if index==2:cylinder('Bifold bronze handle',(leafwidth-.075,-.052,1.05),(leafwidth-.075,-.052,1.18),.007,bronze,door)
        px+=leafwidth*math.cos(angle);py+=leafwidth*math.sin(angle)
scene['proposed_garden_opening_width']=5.8
scene['proposed_garden_opening_head']=2.4

# Simple styled objects are kept on existing furniture surfaces.
def vase(name,x,y,z,height,radius,mat):
    profile=[(0,.7),(.05,.88),(.18,1),(.6,.92),(.82,.54),(1,.47)]
    verts=[];faces=[]
    for h,r in profile:
        for j in range(48):verts.append((x+radius*r*math.cos(j*math.tau/48),y+radius*r*math.sin(j*math.tau/48),z+h*height))
    for k in range(len(profile)-1):
        for j in range(48):a=k*48+j;b=k*48+(j+1)%48;faces.append((a,b,b+48,a+48))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,mesh);col.objects.link(o);o.data.materials.append(mat)
    for p in mesh.polygons:p.use_smooth=True
    mod=o.modifiers.new('Ceramic thickness','SOLIDIFY');mod.thickness=.006
    return o
vase('Hand-thrown table vase',3.05,-6.60,.78,.24,.10,ceramic)
for i in range(5):
    x=3.05+random.uniform(-.16,.16);y=-6.60+random.uniform(-.14,.14)
    curve('Olive stem',[(3.05,-6.60,.90),(x,y,1.25),(x+.08,y+.025,1.43)],.002,bronze)
    for j in range(5):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1,location=(x+random.uniform(-.06,.06),y+random.uniform(-.05,.05),1.1+j*.065));o=link(bpy.context.object);o.name='Olive leaf';o.scale=(.045,.013,.006);o.rotation_euler=(.2,.4,random.random()*6);o.data.materials.append(leafm)
book=material('Linen book cover','80734f',.9)
box('Coffee-table book',(3.15,-2.86,.435),(.31,.23,.035),book,.003)
vase('Small ceramic bowl',3.55,-2.83,.415,.065,.085,ceramic)

# Kitchen joinery follows the brief where seen through the open divider.
for x,w in [(6.85+i*.6167,.613) for i in range(6)]:
    box('Ivory kitchen cabinet',(x+w/2,-5.685,.47),(w,.63,.88),ivory,.005)
    box('Slim framed kitchen door',(x+w/2,-6.009,.47),(w-.014,.022,.75),ivory,.002)
    box('Recessed ivory panel',(x+w/2,-6.023,.47),(w-.11,.008,.64),ivory,.002)
    cylinder('Bronze kitchen handle',(x+w-.11,-6.039,.58),(x+w-.11,-6.039,.70),.005,bronze)
box('Honed kitchen worktop',(8.7,-5.675,.925),(3.7,.67,.035),cream,.004)
box('Forest-green island body',(8.725,-7.7,.47),(2.38,.98,.88),green,.005)
box('Cream island worktop',(8.725,-7.7,.925),(2.4,1,.035),cream,.006)
for x in (7.925,8.725,9.525):
    box('Framed green island door',(x,-8.204,.47),(.78,.018,.76),green,.002)
    box('Recessed green island panel',(x,-8.216,.47),(.68,.008,.64),green,.002)

# Resolve planting seen through the windows without changing the plot layout.
foliage=[material('Garden leaf '+str(i),c,.65) for i,c in enumerate(('405a2e','566b35','71804a','354c29'))]
for old in list(bpy.data.objects):
    if old.type!='MESH' or old.get('source_geometry')!='IcosahedronGeometry':continue
    old.hide_render=True
    centre=old.matrix_world.translation
    scale=old.dimensions/2
    verts=[];faces=[];indices=[]
    for j in range(1000):
        direction=Vector((random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)))
        if direction.length>1:direction.normalize()
        pos=centre+Vector((direction.x*scale.x,direction.y*scale.y,direction.z*scale.z))
        a=random.random()*math.tau;length=random.uniform(.055,.13);width=length*.4
        axis=Vector((math.cos(a)*length,math.sin(a)*length,random.uniform(-.06,.06)))
        cross=Vector((-math.sin(a)*width,math.cos(a)*width,.006))
        start=len(verts);verts.extend([tuple(pos-axis),tuple(pos+cross),tuple(pos+Vector((0,0,.012))),tuple(pos-cross),tuple(pos+axis)])
        faces.extend([(start,start+1,start+2),(start,start+2,start+3),(start+4,start+2,start+1),(start+4,start+3,start+2)])
        indices.extend([random.randrange(4)]*4)
    mesh=bpy.data.meshes.new('Individual garden leaves');mesh.from_pydata(verts,[],faces)
    ob=bpy.data.objects.new('Garden foliage detail',mesh);col.objects.link(ob)
    for m in foliage:mesh.materials.append(m)
    for face,index in zip(mesh.polygons,indices):face.material_index=index

for obj in scene.objects:
    if obj.type=='LIGHT' and 'soft ceiling light' in obj.name:obj.hide_render=True
for name,position,target,power,size in [('Garden daylight',(2.9,.0,1.9),(2.9,-4,1.1),150,2),('West daylight',(.05,-2.6,1.8),(3.5,-2.6,1.0),180,2),('Dining daylight',(.05,-6.8,1.8),(3.5,-6.8,1),140,1.7)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=(1,.94,.83)
    o=bpy.data.objects.new(name,data);col.objects.link(o);o.location=position;o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.09
sun=bpy.data.objects.get('Afternoon sun');sun.data.energy=2;sun.data.angle=math.radians(6)
sun.location=(-12,10,22);sun.rotation_euler=(Vector((4,-3,0))-sun.location).to_track_quat('-Z','Y').to_euler()

camera=scene.camera;camera.name='Living dining realism benchmark';camera.data.lens=24;camera.data.dof.use_dof=False
camera.location=(5.9,-8.8,1.60);camera.rotation_euler=(Vector((2.75,-2.9,1.22))-camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=args.width;scene.render.resolution_y=round(args.width*2/3);scene.render.resolution_percentage=100
scene.cycles.samples=args.samples;scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.02;scene.cycles.max_bounces=12
scene.cycles.use_light_tree=True
scene.view_settings.exposure=.15
scene.view_settings.look='AgX - Medium High Contrast'
scene['design_revision']='L01 living/dining interior base 02'
scene['style_source']='MATERIALS-BRIEF.md: agreed shared-space palette and supporting proposals'
scene['scope_note']='G1 interior revision: corner sofa, moved coffee table and proposed 5.8 m garden bifolds. Source objects retained; source plan and browser not revised.'
scene['units_note']='Metres. Source transforms retained; garden opening, sofa and coffee table revised as proposals.'
notes=bpy.data.texts.get('READ ME - L-house study')
notes.clear();notes.write((root/'scripts/blender/LIVING-STUDY.md').read_text())
bpy.ops.wm.save_as_mainfile(filepath=str(out/'living-study.blend'),compress=True)
scene.render.filepath=str(out/'living-dining.png');bpy.ops.render.render(write_still=True)
camera.location=(5.2,-4.65,1.45);camera.rotation_euler=(Vector((1.65,-2.45,.95))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=30
scene.render.filepath=str(out/'seating-detail.png');bpy.ops.render.render(write_still=True)
report={'sourceModelSha256':hashlib.sha256((root/'viewer-l-house/model.json').read_bytes()).hexdigest(),'brief':'MATERIALS-BRIEF.md','objectsAdded':len(col.objects),'furnitureFootprints':{o.name:list(o['approved_footprint']) for o in col.objects if 'approved_footprint' in o},'proposedGardenOpening':{'width':5.8,'head':2.4,'leaves':6},'proposedFurniture':{o.name:list(o['proposed_plan_bounds']) for o in col.objects if 'proposed_plan_bounds' in o},'samples':args.samples,'width':args.width,'renderer':'Cycles','device':scene.cycles.device,'textures':'Poly Haven CC0 oak_veneer_02 and terlenka'}
(out/'study-report.json').write_text(json.dumps(report,indent=2))
print('LIVING_STUDY',json.dumps(report))
