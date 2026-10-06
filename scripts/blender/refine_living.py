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
rugmat=textured('Deep green woven rug','35594d','terlenka',3,True)
panelpaint=material('Warm ivory painted panelling','d8cbb4',.66)
shutterpaint=material('Ivory plantation shutters','eee4cf',.56)
antique=textured('Aged oak dining table','8c603c','oak_veneer_02',1.2)
n,l=antique.node_tree.nodes,antique.node_tree.links;p=n.get('Principled BSDF')
base=p.inputs['Base Color'].links[0].from_socket
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.48,.49,.47,1)
l.new(base,mix.inputs[1]);l.new(mix.outputs[0],p.inputs['Base Color'])

for node in n:
    if node.type=='MAP_RANGE':node.inputs['To Min'].default_value=.50;node.inputs['To Max'].default_value=.78
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=35;noise.inputs['Detail'].default_value=3
coord=n.new('ShaderNodeTexCoord');l.new(coord.outputs['Object'],noise.inputs['Vector'])
normal=p.inputs['Normal'].links[0].from_socket
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.0008
l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(normal,bump.inputs['Normal']);l.new(bump.outputs[0],p.inputs['Normal'])

def printed_fabric(name,file,scale):
    m=textured(name,'ded2b7','terlenka',5,True)
    n,l=m.node_tree.nodes,m.node_tree.links
    tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(root/'assets/living-study'/file),check_existing=True);tex.image.pack();tex.projection='BOX';tex.projection_blend=.04
    coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=scale
    l.new(coord.outputs['Object'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs[0]);l.new(tex.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
    return m
botanical=printed_fabric('Arts and Crafts botanical textile','botanical.png',1.25)
floral=printed_fabric('Blue cottage floral textile','floral.png',1.8)

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

rug=box('Generous woven lounge rug',(3.1,-3.10,.056),(4.0,3.9,.023),rugmat,.012)
for side in (-1,1):
    for i in range(165):
        y=-5.00+i*3.80/164
        curve('Rug fringe',[(3.1+side*2.00,y,.064),(3.1+side*(2.04+random.random()*.025),y+random.uniform(-.006,.006),.052)],.0013,linen)

sofa=group('Large oatmeal corner sofa',(1.25,-3.075,0),math.pi/2)
sofa['proposed_plan_bounds']=[.70,1.25,4.10,3.65]
box('Sofa upholstered base',(0,0,.30),(3.63,1.10,.30),oatmeal,.10,sofa)
box('Sofa back shell',(0,.42,.73),(3.60,.22,.70),oatmeal,.075,sofa)
box('Soft sofa arm',(-1.70,0,.61),(.24,1.10,.62),oatmeal,.10,sofa)
for x in (-1.22,-.41,.40,1.21):
    cushion('Seat cushion',(x,-.07,.50),(.79,.86,.21),oatmeal,sofa)
    seam('Seat piping',x,-.07,.58,.75,.82,oatmeal,sofa)
    cushion('Back cushion',(x,.30,.84),(.80,.25,.55),oatmeal,sofa,-.13)
for x in (-1.56,0,1.56):
    for y in (-.40,.40):cylinder('Oak sofa foot',(x,y,.04),(x,y,.20),.048,antique,sofa,r2=.037)
box('Corner return upholstered base',(1.275,-2.00,.30),(1.10,2.90,.30),oatmeal,.10,sofa)
box('Corner return back',(1.69,-2.00,.73),(.24,3.10,.70),oatmeal,.075,sofa)
box('Corner return end arm',(1.275,-3.45,.61),(1.10,.20,.62),oatmeal,.09,sofa)
for yy in (-1.05,-1.95,-2.85):
    cushion('Corner return seat',(1.10,yy,.50),(.85,.86,.21),oatmeal,sofa)
    seam('Return seat piping',1.10,yy,.58,.81,.82,oatmeal,sofa)
    back=cushion('Corner return back cushion',(1.56,yy,.84),(.25,.88,.55),oatmeal,sofa);back.rotation_euler.y=.12
for x in (.91,1.61):
    for y in (-1.7,-3.25):cylinder('Corner return oak foot',(x,y,.04),(x,y,.20),.048,antique,sofa,r2=.037)
for x,mat,angle in [(-1.35,botanical,.15),(-.65,floral,-.15),(.96,botanical,.08)]:
    o=cushion('Patterned scatter cushion',(x,.07,.85),(.47,.18,.47),mat,sofa,-.20);o.rotation_euler.y=angle
for yy,mat in [(-1.3,floral),(-2.6,botanical)]:
    o=cushion('Return scatter cushion',(1.27,yy,.85),(.18,.46,.46),mat,sofa);o.rotation_euler.y=.20

ottoman=group('Botanical upholstered ottoman',(3.35,-3.30,0))
ottoman['proposed_plan_bounds']=[2.525,2.75,1.65,1.10]
box('Ottoman upholstered base',(0,0,.255),(1.63,1.08,.22),botanical,.055,ottoman)
cushion('Ottoman cushioned top',(0,0,.405),(1.65,1.10,.18),botanical,ottoman)
seam('Ottoman piped edge',0,0,.463,1.58,1.03,forest,ottoman)
for x in (-.65,.65):
    for y in (-.40,.40):
        cylinder('Ottoman turned foot',(x,y,.055),(x,y,.18),.044,antique,ottoman,r2=.035)
        cylinder('Ottoman brass castor',(x-.022,y,.059),(x+.022,y,.059),.025,bronze,ottoman)

media=group('French country media cabinet',(6.31,-2.50,0),-math.pi/2)
media['proposed_plan_bounds']=[6.115,1.20,.39,2.60]
box('Painted media cabinet',(0,0,.405),(2.56,.36,.48),panelpaint,.005,media)
box('Aged oak console top',(0,0,.67),(2.60,.39,.055),antique,.01,media)
for x in (-.85,0,.85):
    box('Framed cabinet door',(x,-.189,.405),(.826,.022,.44),panelpaint,.003,media)
    box('Raised cabinet panel',(x,-.207,.405),(.66,.019,.30),panelpaint,.006,media)
    for xx in (x-.36,x+.36):box('Cabinet stile moulding',(xx,-.220,.405),(.019,.014,.37),panelpaint,.003,media)
    for h in (.22,.59):box('Cabinet rail moulding',(x,-.220,h),(.72,.014,.019),panelpaint,.003,media)
    cylinder('Bronze cabinet knob',(x+.27,-.228,.47),(x+.27,-.253,.47),.014,bronze,media)
for x in (-1.13,1.13):
    for y in (-.13,.13):curve('Curved cabinet foot',[(x,y,.19),(x*1.025,y*1.12,.11),(x*1.035,y*1.18,.04)],.033,antique,media)
black=material('Television dark glass','151b18',.22,.15)
box('Television',(6.49,-2.50,1.37),(.04,1.63,.94),black,.012)

# The table and chairs retain their measured centres and facing directions.
dining=group('French country trestle table',(3.1,-6.6,0))
dining['approved_footprint']=[1.7,6.05,2.8,1.1]
for j in range(4):
    box('Rustic oak tabletop plank',(0,-.4125+j*.275,.74),(2.50,.273,.08),antique,.008,dining)
for x in (-1.325,1.325):box('Worn breadboard table end',(x,0,.74),(.15,1.10,.08),antique,.009,dining)
box('Low oak trestle stretcher',(0,0,.23),(2.0,.12,.13),antique,.01,dining)
profile=[(.04,.35),(.10,.43),(.16,.38),(.24,.17),(.39,.09),(.51,.16),(.60,.30),(.69,.36)]
outline=[]
for i in range(len(profile)-1):
    z0,w0=profile[i];z1,w1=profile[i+1]
    for j in range(6):
        t=j/6;outline.append((z0+(z1-z0)*t,w0+(w1-w0)*(.5-.5*math.cos(math.pi*t))))
outline.append(profile[-1]);outline=[(w,h) for h,w in outline]+[(-w,h) for h,w in reversed(outline)]
for x in (-.89,.89):
    n=len(outline);verts=[(x+dx,y,z) for dx in (-.09,.09) for y,z in outline]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    mesh=bpy.data.meshes.new('Shaped French trestle');mesh.from_pydata(verts,[],faces)
    leg=bpy.data.objects.new('Shaped oak trestle support',mesh);col.objects.link(leg);leg.parent=dining;mesh.materials.append(antique)
    mod=leg.modifiers.new('Worn trestle edges','BEVEL');mod.width=.009;mod.segments=3
    leg.modifiers.new('Trestle corner normals','WEIGHTED_NORMAL')
    box('Through-tenon end',(x*1.19,0,.23),(.07,.15,.15),antique,.006,dining)
    cylinder('Dark oak fixing peg',(x,-.13,.23),(x,.13,.23),.013,antique,dining)

def chair(x,z,angle):
    g=group('French country ladder-back chair',(x,-z,0),angle)
    for xx in (-.18,.18):
        for yy in (-.18,.18):curve('Shaped country chair leg',[(xx*1.18,yy*1.12,.04),(xx*.96,yy,.21),(xx,yy,.44)],.026,antique,g)
    box('Aged oak seat frame',(0,0,.425),(.48,.46,.065),antique,.016,g)
    cushion('Floral dining seat',(0,-.015,.485),(.46,.435,.08),floral,g)
    for xx in (-.205,.205):curve('Swept chair back post',[(xx,.18,.42),(xx*1.05,.23,.76),(xx*1.08,.27,1.00)],.020,antique,g)
    for h in (.65,.79,.93):
        verts=[]
        for j in range(17):
            xx=-.22+j*.44/16;arch=.025*(1-(xx/.22)**2)
            verts.extend([(xx,.245,h+arch-.025),(xx,.245,h+arch+.025)])
        faces=[(2*j,2*j+2,2*j+3,2*j+1) for j in range(16)]
        mesh=bpy.data.meshes.new('Curved ladder slat');mesh.from_pydata(verts,[],faces)
        slat=bpy.data.objects.new('Country chair ladder slat',mesh);col.objects.link(slat);slat.parent=g;mesh.materials.append(antique)
        mod=slat.modifiers.new('Solid oak slat','SOLIDIFY');mod.thickness=.022
        mod=slat.modifiers.new('Soft slat edge','BEVEL');mod.width=.005;mod.segments=3
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
    intervals=[(.35,9.3)] if x<1 else [(.35,3.95),(9.1,9.3)]
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
for a,b in ((.42,3.88),):panelling(6.532,a,b,1.10)
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
# Artwork and lamps are placed on the remaining solid walls.
def artwork(name,file,loc,w,h,angle):
    g=group(name,loc,angle)
    paint=material(name+' canvas','ffffff',.86)
    n,l=paint.node_tree.nodes,paint.node_tree.links
    tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(root/'assets/living-study'/file),check_existing=True);tex.image.pack()
    l.new(tex.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
    verts=[(-w/2,-.032,-h/2),(w/2,-.032,-h/2),(w/2,-.032,h/2),(-w/2,-.032,h/2)]
    mesh=bpy.data.meshes.new(name+' canvas');mesh.from_pydata(verts,[],[(0,1,2,3)])
    uv=mesh.uv_layers.new()
    for loop,co in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=co
    o=bpy.data.objects.new(name+' painting',mesh);col.objects.link(o);o.parent=g;mesh.materials.append(paint)
    for xx in (-w/2-.03,w/2+.03):box('Aged oak picture frame',(xx,0,0),(.06,.075,h+.12),antique,.005,g)
    for zz in (-h/2-.03,h/2+.03):box('Aged oak picture frame',(0,0,zz),(w,.075,.06),antique,.005,g)
    for xx in (-w/2,w/2):box('Gilt frame liner',(xx,-.042,0),(.009,.009,h),bronze,.002,g)
    for zz in (-h/2,h/2):box('Gilt frame liner',(0,-.042,zz),(w,.009,.009),bronze,.002,g)
    cylinder('Picture-light arm',(0,-.02,h/2+.10),(0,-.24,h/2+.10),.011,bronze,g)
    cylinder('Bronze picture-light hood',(-.28,-.24,h/2+.10),(.28,-.24,h/2+.10),.027,bronze,g)
    data=bpy.data.lights.new(name+' picture light','AREA');data.energy=7;data.color=(1,.79,.53);data.shape='RECTANGLE';data.size=.50;data.size_y=.05
    light=bpy.data.objects.new(data.name,data);col.objects.link(light);light.parent=g;light.location=(0,-.23,h/2+.07);light.rotation_euler=Vector((0,.19,-h/2-.07)).to_track_quat('-Z','Y').to_euler()
    light.visible_camera=False;light.visible_glossy=False;light.visible_transmission=False
    return g
artwork('Large river landscape','landscape.png',(.43,-4.80,1.87),1.66,1.10,math.pi/2)
artwork('Large floral still life','still-life.png',(2.45,-9.25,1.82),1.02,1.275,math.pi)

def lampshade(name,x,y,z,r,h,power):
    verts=[];faces=[]
    for level,rad in ((z,r),(z+h,r*.65)):
        for j in range(96):
            a=j*math.tau/96;rr=rad+(.004 if j%2 else -.004);verts.append((x+rr*math.cos(a),y+rr*math.sin(a),level))
    for j in range(96):faces.append((j,(j+1)%96,(j+1)%96+96,j+96))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces)
    shade=bpy.data.objects.new(name,mesh);col.objects.link(shade);mesh.materials.append(linen)
    mod=shade.modifiers.new('Linen shade thickness','SOLIDIFY');mod.thickness=.001
    for zz,rr in ((z,r),(z+h,r*.65)):
        curve('Shade bound edge',[(x+rr*math.cos(j*math.tau/64),y+rr*math.sin(j*math.tau/64),zz) for j in range(64)],.003,linen,closed=True)
    data=bpy.data.lights.new(name+' bulb','POINT');data.energy=power;data.color=(1,.76,.47);data.shadow_soft_size=.05
    bulb=bpy.data.objects.new(data.name,data);col.objects.link(bulb);bulb.location=(x,y,z+h*.38)

cylinder('Floor lamp weighted foot',(.83,-5.14,.045),(.83,-5.14,.075),.19,bronze)
cylinder('Floor lamp bronze stem',(.83,-5.14,.075),(.83,-5.14,1.53),.015,bronze)
lampshade('Corner floor lamp',.83,-5.14,1.38,.25,.32,10)
glaze=material('Blue-green glazed lamp ceramic','657e77',.26)
vase('Console ceramic lamp base',6.31,-3.53,.698,.28,.105,glaze)
cylinder('Console lamp neck',(6.31,-3.53,.95),(6.31,-3.53,1.14),.014,bronze)
lampshade('Console table lamp',6.31,-3.53,1.02,.18,.25,7)

# This stove and its interior flue show a location option, not a specified installation.
stove=group('Log burner position study',(6.12,-5.65,0),-math.pi/2)
stove['proposal_only']=True
iron=material('Black stove enamel','222925',.32,.35)
hearth=material('Honed charcoal hearth','52564e',.82)
box('Proposed stove hearth',(6.04,-5.65,.065),(1.0,1.25,.06),hearth,.005)
box('Proposed mineral stove backing',(6.512,-5.80,1.35),(.06,1.70,2.7),stone,.003)
box('Stove back',(0,.225,.59),(.54,.035,.57),iron,.018,stove)
for x in (-.26,.26):box('Stove side',(x,0,.59),(.035,.48,.57),iron,.013,stove)
for h in (.31,.875):box('Stove plate',(0,0,h),(.56,.51,.045),iron,.012,stove)
for x in (-.21,.21):
    for y in (-.17,.17):cylinder('Cast stove foot',(x*1.07,y*1.07,.095),(x,y,.31),.023,iron,stove,r2=.03)
for x in (-.225,.225):box('Stove door stile',(x,-.259,.59),(.045,.04,.51),iron,.008,stove)
for h in (.355,.825):box('Stove door rail',(0,-.259,h),(.405,.04,.045),iron,.008,stove)
box('Stove front glass',(0,-.265,.59),(.40,.008,.425),glass,.001,stove)
cylinder('Stove door handle',(.255,-.31,.52),(.255,-.31,.67),.009,bronze,stove)
cylinder('Visible proposed stove flue',(0,.08,.90),(0,.08,2.69),.073,iron,stove)
cylinder('Stove flue collar',(0,.08,.86),(0,.08,.94),.092,iron,stove)
for y in (-.12,.075):cylinder('Firebox oak log',(-.19,y,.39),(.19,y+.02,.39),.045,antique,stove)
fire=material('Fire glow','ffad43',.8);shader=fire.node_tree.nodes.get('Principled BSDF');shader.inputs['Emission Color'].default_value=(1,.24,.025,1);shader.inputs['Emission Strength'].default_value=3
for i in range(5):
    x=-.16+i*.08;h=.15+.06*math.sin(i*1.7)
    mesh=bpy.data.meshes.new('Small flame');mesh.from_pydata([(x-.035,-.19,.42),(x+.035,-.19,.42),(x+.01,-.175,.42+h),(x-.008,-.185,.51)],[],[(0,1,2,3)])
    o=bpy.data.objects.new('Firebox flame',mesh);col.objects.link(o);o.parent=stove;mesh.materials.append(fire)
data=bpy.data.lights.new('Stove ember light','POINT');data.energy=6;data.color=(1,.33,.06);data.shadow_soft_size=.1
light=bpy.data.objects.new(data.name,data);col.objects.link(light);light.parent=stove;light.location=(0,-.18,.55);light.visible_camera=False;light.visible_glossy=False;light.visible_transmission=False
scene['stove_status']='Location study only. Flue route above the ceiling, hearth construction and model-specific clearances remain unresolved.'

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
camera.location=(5.25,-8.8,1.60);camera.rotation_euler=(Vector((2.75,-2.9,1.22))-camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=args.width;scene.render.resolution_y=round(args.width*2/3);scene.render.resolution_percentage=100
scene.cycles.samples=args.samples;scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.02;scene.cycles.max_bounces=12
scene.cycles.use_light_tree=True
scene.view_settings.exposure=.15
scene.view_settings.look='AgX - Medium High Contrast'
scene['design_revision']='L01 living/dining interior base 03'
scene['style_source']='MATERIALS-BRIEF.md: agreed shared-space palette and supporting proposals'
scene['scope_note']='G1 country interior: larger sofa, patterned ottoman, shallow console, art and layered light; 5.8 m bifolds and log-burner location are proposals. Source plan and browser not revised.'
scene['units_note']='Metres. Source transforms retained; garden opening, furniture and log-burner location revised as proposals.'
notes=bpy.data.texts.get('READ ME - L-house study')
notes.clear();notes.write((root/'scripts/blender/LIVING-STUDY.md').read_text())
bpy.ops.wm.save_as_mainfile(filepath=str(out/'living-study.blend'),compress=True)
scene.render.filepath=str(out/'living-dining.png');bpy.ops.render.render(write_still=True)
camera.location=(5.65,-5.0,1.50);camera.rotation_euler=(Vector((2.65,-2.85,.95))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=30
scene.render.filepath=str(out/'seating-detail.png');bpy.ops.render.render(write_still=True)
camera.location=(1.8,-.83,1.65);camera.rotation_euler=(Vector((4.3,-5.8,1.15))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=24
scene.render.filepath=str(out/'hearth-dining.png');bpy.ops.render.render(write_still=True)
report={'sourceModelSha256':hashlib.sha256((root/'viewer-l-house/model.json').read_bytes()).hexdigest(),'brief':'MATERIALS-BRIEF.md','objectsAdded':len(col.objects),'furnitureFootprints':{o.name:list(o['approved_footprint']) for o in col.objects if 'approved_footprint' in o},'proposedGardenOpening':{'width':5.8,'head':2.4,'leaves':6},'proposedFurniture':{o.name:list(o['proposed_plan_bounds']) for o in col.objects if 'proposed_plan_bounds' in o},'samples':args.samples,'width':args.width,'renderer':'Cycles','device':scene.cycles.device,'textures':'Poly Haven CC0 oak_veneer_02 and terlenka; original generated textiles and art'}
(out/'study-report.json').write_text(json.dumps(report,indent=2))
print('LIVING_STUDY',json.dumps(report))
