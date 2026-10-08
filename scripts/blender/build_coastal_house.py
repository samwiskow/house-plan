"""Build a local coordinated house from the measured plan and approved room scene."""
import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent/'coastal'))
from model import ROOT, LEVELS, HEIGHTS, load, rect, cells, inside, walls, openings, roofs, roof_height, subtract_rect, clip

p=argparse.ArgumentParser()
p.add_argument('--interior',type=Path,required=True)
p.add_argument('--samples',type=int,default=32)
p.add_argument('--width',type=int,default=1200)
p.add_argument('--views',nargs='*',default=[])
p.add_argument('--export',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
O=ROOT/'output/blender/coastal-house';O.mkdir(parents=True,exist_ok=True)
data=load();rng=random.Random(108)
source_hash=hashlib.sha256(a.interior.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(a.interior))
scene=bpy.context.scene;scene.frame_set(1);bpy.context.view_layer.update()
bpy.context.preferences.filepaths.save_version=0
keep=set()
for c in bpy.data.collections:
    selected=c.name in ['01 Table','03 Corner sofa','04 Square footstool','05 Media cabinet proposal','Combined rooms - glazed divider and screen'] or c.name.startswith('Approved cane dining chair') or c.name.startswith(('K01','K02','K03','K04','K06','K09','K10'))
    if selected:
        keep.update(o for o in c.all_objects if not o.hide_render)
living=bpy.data.collections['Living study - detailed furniture and finishes']
keep.update(o for o in living.all_objects if not o.hide_render and not o.name.startswith(('Garden foliage','Garden daylight','West daylight','Dining daylight')))
for o in list(keep):
    parent=o.parent
    while parent:
        keep.add(parent);parent=parent.parent
for o in list(bpy.data.objects):
    if o not in keep:
        bpy.data.objects.remove(o,do_unlink=True)
for c in list(bpy.data.collections):
    if not c.all_objects:
        bpy.data.collections.remove(c)
for c in bpy.data.collections:
    c.hide_render=False;c.hide_viewport=False
for o in scene.objects:
    o.hide_set(False);o['level']='g';o['part']='interior';o['provenance']='Approved combined-room study'


def collection(name,level,part):
    c=bpy.data.collections.new(name);scene.collection.children.link(c)
    c['level']=level;c['part']=part
    return c

cols={}
for f in LEVELS:
    for part in ['walls','floors','openings','furniture','ceilings']:
        cols[f,part]=collection(f'{f.upper()} | {part}',f,part)
roofcol=collection('ROOF | skins, flashings and light wells','roof','roof')
sitecol=collection('SITE | coastal garden and arrival','site','site')
staircol=collection('STAIRS | coordinated flights and guards','stairs','stairs')
lightcol=collection('LIGHT | daylight and room fittings','light','light')
optioncol=collection('OPTION | burner awaiting flue design','g','option')
for o in list(scene.objects):
    if any(s in o.name.lower() for s in ['stove','firebox','log burner']):
        for c in list(o.users_collection):c.objects.unlink(o)
        optioncol.objects.link(o);o['part']='option';o.hide_render=True
optioncol.hide_render=True;optioncol.hide_viewport=True
col=sitecol


def mat(name,color,rough=.6,metal=0,noise=0,scale=40):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    n=m.node_tree.nodes;l=m.node_tree.links;s=n.get('Principled BSDF')
    s.inputs['Base Color'].default_value=(*color,1);s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal
    if noise:
        t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=scale;t.inputs['Detail'].default_value=3
        ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*(v*(1-noise) for v in color),1);ramp.color_ramp.elements[1].color=(*(min(1,v*(1+noise)) for v in color),1)
        l.new(t.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],s.inputs['Base Color'])
        b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.3;b.inputs['Distance'].default_value=.018 if scale<10 else .001
        l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],s.inputs['Normal'])
    return m

ivory=mat('Coastal | lime plaster',(.74,.70,.62),.85,noise=.06)
stone=mat('Coastal | warm rubble limestone',(.42,.39,.31),.9,noise=.36,scale=9)
stone2=mat('Coastal | pale paving',(.52,.48,.39),.88,noise=.19,scale=55)
oak=mat('Coastal | weathered oak',(.34,.26,.17),.65,noise=.22,scale=7)
wood=bpy.data.materials.get('Combined pale natural dining oak') or oak
fabric=mat('Coastal | oatmeal linen',(.63,.59,.49),.93,noise=.1,scale=210)
white=mat('Coastal | cotton and porcelain',(.85,.83,.76),.45,noise=.04)
olive=mat('Coastal | olive textile',(.15,.19,.095),.9,noise=.16,scale=180)
blue=mat('Coastal | slate blue textile',(.19,.29,.32),.85,noise=.14,scale=150)
metal=mat('Coastal | patinated bronze',(.16,.13,.09),.32,.75)
black=mat('Coastal | graphite',(.035,.044,.045),.5,.35)
roofmat=mat('Coastal | zinc roof',(.14,.17,.18),.52,.65,noise=.16,scale=70)
soil=mat('Coastal | shingle and soil',(.21,.18,.12),1,noise=.5,scale=90)
grassmat=mat('Coastal | short meadow',(.22,.285,.12),1,noise=.4,scale=30)
leaf=mat('Coastal | salt wind foliage',(.13,.21,.09),.85)
silver=mat('Coastal | silver foliage',(.31,.37,.24),.9)
straw=mat('Coastal | dune grass',(.43,.39,.20),.94)
flower=mat('Coastal | muted lavender',(.30,.24,.37),.95)
glass=mat('Coastal | clear glazing',(.92,.97,.96),.035)
glass.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value=1
glass.node_tree.nodes['Principled BSDF'].inputs['IOR'].default_value=1.45
mirror=mat('Coastal | mirror',(.8,.82,.8),.06,1)


def mesh(name,verts,faces,m,bevel=0):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);col.objects.link(o)
    if m:me.materials.append(m)
    o['level']=col.get('level','g');o['part']=col.get('part','interior')
    if bevel:
        mod=o.modifiers.new('Soft edges','BEVEL');mod.width=bevel;mod.segments=3
        mod=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o


def box(name,pos,dim,m,bevel=.004):
    vs=[(x*dim[0]/2,y*dim[1]/2,z*dim[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
    o=mesh(name,vs,[(0,2,6,4),(1,5,7,3),(0,4,5,1),(2,3,7,6),(0,1,3,2),(4,6,7,5)],m,min(bevel,min(dim)/4));o.location=pos
    return o


def pb(name,r,lo,hi,m,bevel=.004):
    x,y,w,d=r
    return box(name,(x+w/2,-y-d/2,(lo+hi)/2),(w,d,hi-lo),m,bevel)


def tube(name,points,radius,m):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=2
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for p,q in zip(sp.points,points):p.co=(*q,1)
    o=bpy.data.objects.new(name,cu);col.objects.link(o);cu.materials.append(m);o['level']=col.get('level');o['part']=col.get('part');return o


def cyl(name,pos,r,depth,m,vertices=24):
    vs=[(pos[0]+r*math.cos(i*math.tau/vertices),pos[1]+r*math.sin(i*math.tau/vertices),pos[2]+z*depth/2) for z in [-1,1] for i in range(vertices)]
    fs=[tuple(reversed(range(vertices))),tuple(range(vertices,2*vertices))]+[(i,(i+1)%vertices,(i+1)%vertices+vertices,i+vertices) for i in range(vertices)]
    o=mesh(name,vs,fs,m,.002)
    for face in o.data.polygons:face.use_smooth=len(face.vertices)==4
    return o


def ellipsoid(name,pos,scale,m):
    vs=[];fs=[];N=20;M=12
    for j in range(M+1):
        v=math.pi*j/M
        for i in range(N):
            u=math.tau*i/N;vs.append((pos[0]+scale[0]*math.sin(v)*math.cos(u),pos[1]+scale[1]*math.sin(v)*math.sin(u),pos[2]+scale[2]*math.cos(v)))
    for j in range(M):
        for i in range(N):fs.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
    o=mesh(name,vs,fs,m)
    for f in o.data.polygons:f.use_smooth=True
    return o


def surface(name,poly,z,m,thickness=0):
    verts=[(x,-y,z(x,y) if callable(z) else z) for x,y in reversed(poly)]
    o=mesh(name,verts,[tuple(range(len(verts)))],m)
    if thickness:
        mod=o.modifiers.new('Physical thickness','SOLIDIFY');mod.thickness=thickness;mod.offset=-1
    return o


def light(name,pos,target,power,size,color=(1,.89,.72)):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color
    o=bpy.data.objects.new(name,d);lightcol.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o


wall_records=[]
for f,base in LEVELS.items():
    col=cols[f,'walls']
    for i,(x,y,w,d,lo,hi) in enumerate(walls(data,f)):
        obj=pb(f'{f} wall {i:03}',[x,y,w,d],base+lo,base+hi,ivory,.001)
        obj['rect']=[x,y,w,d];obj['bottom']=base+lo;obj['top']=base+hi
        obj.data.materials.append(stone if f in ['g','a'] else oak)
        for face in obj.data.polygons:
            sample=obj.location+face.center+face.normal*.03
            if abs(face.normal.z)<.5 and not any(inside(sample.x,-sample.y,p) for p in data['shells'][f]):face.material_index=1
        wall_records.append(dict(floor=f,r=[x,y,w,d],lo=base+lo,hi=base+hi))
    col=cols[f,'floors']
    holes=[rect(*s['r']) for s in data['stairs'] if s['upper']==f]
    for r in cells(data['shells'][f],holes):
        pb(f'{f} floor slab',r,base-(.26 if f in ['u','o'] else .20),base+.025,stone2,0)
    for room in [r for r in data['rooms'] if r['floor']==f and r['id'] not in ['G1','G2','G9','U12','A3','O3']]:
        wet=any(s in room['name'].lower() for s in ['bath','shower','ensuite','basin','wc','garage','plant','gym'])
        if wet:
            surface(room['id']+' stone floor',room['p'],base+.04,stone2)
            x0=min(x for x,y in room['p']);x1=max(x for x,y in room['p']);y0=min(y for x,y in room['p']);y1=max(y for x,y in room['p'])
            for x in range(math.floor(x0/.6),math.ceil(x1/.6)):
                for y in range(math.floor(y0/.9),math.ceil(y1/.9)):
                    poly=rect(x*.6+.003,y*.9+.003,.594,.894)
                    for cell in cells([room['p']],[]):
                        q=poly
                        for fn in [lambda xx,yy:xx-cell[0],lambda xx,yy:cell[0]+cell[2]-xx,lambda xx,yy:yy-cell[1],lambda xx,yy:cell[1]+cell[3]-yy]:
                            q=clip(q,fn) if q else []
                        if q:surface(room['id']+' honed tile',q,base+.041,stone2)
        else:
            surface(room['id']+' floor backing',room['p'],base+.033,oak)
            for r in cells([room['p']],[]):
                x,y,w,d=r;step=.18
                for i in range(math.ceil(w/step)):
                    bw=min(step,w-i*step)-.003
                    if bw>0:pb(room['id']+' oak board',[x+i*step+.0015,y+.0015,bw,d-.003],base+.033,base+.0395,wood,.001)
    col=cols[f,'ceilings']
    for room in [r for r in data['rooms'] if r['floor']==f and r['id'] not in ['G9','A3']]:
        pieces=[room['p']]
        for r in data['rooflights'] if f=='u' else []:
            pieces=[q for p in pieces for q in subtract_rect(p,r['r'])]
        for q in pieces:
            ceiling=surface(room['id']+' ceiling',q,base+HEIGHTS[f],ivory,.04)
            ceiling.modifiers[-1].offset=1
    for room in [r for r in data['rooms'] if r['floor']==f and r['id'] not in ['G9','U12','A3','O3']]:
        x,y=room['label'];z=base+HEIGHTS[f]-.065
        light(room['id']+' soft room light',(x,-y,z),(x,-y,base),65 if f=='u' else 90,1.1)
        col=cols[f,'furniture'];shade=cyl(room['id']+' linen ceiling shade',(x,-y,z+.01),.21,.085,fabric);shade['part']='ceilings'

# Joinery follows each measured opening; the detailed garden and pantry doors are retained.
for f,base in LEVELS.items():
    col=cols[f,'openings']
    for d in data['windows']:
        if d['floor']!=f:continue
        x,y,w=d['x'],d['y'],d['w'];lo=base+d['sill'];hi=base+d['head'];horizontal=d['axis']=='h'
        def wb(n,u,z,ww,hh,depth,m):
            return box(n,(x+u,-y,z) if horizontal else (x,-y-u,z),(ww,depth,hh) if horizontal else (depth,ww,hh),m)
        for u in [.03,w-.03]:wb('Window outer jamb',u,(lo+hi)/2,.06,hi-lo,.14,oak)
        for z in [lo+.03,hi-.03]:wb('Window frame rail',w/2,z,w,.06,.14,oak)
        panes=max(1,math.ceil(w/1.1));pw=w/panes
        for i in range(panes):
            if i:wb('Window mullion',i*pw,(lo+hi)/2,.055,hi-lo,.13,oak)
            wb('Double glazing',i*pw+pw/2,(lo+hi)/2,pw-.07,hi-lo-.12,.018,glass)
            wb('Window lower casement',i*pw+pw/2,lo+.095,pw-.075,.04,.09,black)
        wb('Stone window sill',w/2,lo-.035,w+.09,.05,.40,stone2)
    for d in data['doors']:
        if d['floor']!=f or d['style']=='bifold' or d['id'] in [q[0] for q in json.loads((ROOT/'output/design/kitchen-selections/boot-room-option.json').read_text())['doors']]:continue
        x,y,w=d['x'],d['y'],d['w'];h=2.3 if f=='g' else 2.15;horizontal=d['axis']=='h'
        for u in [.025,w-.025]:
            pb(d['id']+' jamb',[x+u-.025,y-.085,.05,.17] if horizontal else [x-.085,y+u-.025,.17,.05],base,base+h,wood)
        pb(d['id']+' head',[x,y-.085,w,.17] if horizontal else [x-.085,y,.17,w],base+h-.05,base+h,wood)
        parent=bpy.data.objects.new(d['id']+' hinge',None);col.objects.link(parent);parent.location=(x,-y,base+.04);parent['opening_id']=d['id'];parent['level']=f;parent['part']='openings'
        if d['style']=='pocket':
            parent.location.x-=w+.03;angle=0
        else:
            angle=-d['side']*math.pi/2
        def doorpart(n,pos,dim,m):
            o=box(d['id']+' '+n,pos,dim,m);o.parent=parent;return o
        doorpart('framed leaf',(w/2,0,h/2-.06),(w-.07,.044,h-.12),ivory)
        for z,hh in [(.49,.66),(1.45,.92)]:doorpart('recessed field',(w/2,-.026,z),(w-.23,.012,hh),fabric)
        for z in [.12,.90,1.99]:doorpart('oak rail',(w/2,-.036,z),(w-.16,.015,.035),wood)
        doorpart('bronze lever',(w-.15,-.065,1.02),(.12,.04,.018),metal)
        if d['style']!='pocket':
            parent.rotation_euler.z=angle if horizontal else (-math.pi/2+(-math.pi/2 if d['side']<0 else math.pi/2))
        parent['closed_angle']=0 if horizontal else -math.pi/2
        parent['open_angle']=parent.rotation_euler.z
    col=cols[f,'walls']
    for room in [r for r in data['rooms'] if r['floor']==f and r['id'] not in ['G1','G2']]:
        for p0,p1 in zip(room['p'],room['p'][1:]+room['p'][:1]):
            length=math.dist(p0,p1);n=max(1,math.ceil(length/.15))
            for i in range(n):
                t=(i+.5)/n;x=p0[0]+(p1[0]-p0[0])*t;y=p0[1]+(p1[1]-p0[1])*t
                if any((abs(y-d['y'])<.21 and d['axis']=='h' and d['x']-.04<x<d['x']+d['w']+.04) or (abs(x-d['x'])<.21 and d['axis']=='v' and d['y']-.04<y<d['y']+d['w']+.04) for d in openings(data,f) if d['lo']==0):continue
                box(room['id']+' skirting',(x,-y,base+.105),(length/n,.025,.13) if abs(p0[1]-p1[1])<.01 else (.025,length/n,.13),ivory,.002)

col=staircol
for s in data['stairs']:
    x,y,w,d=s['r'];half=s['risers']//2;run=(half-1)*s['going'];mid=LEVELS[s['upper']]/2;rise=s['rise'];base=.04
    for side in [0,1]:
        for i in range(half-1):
            z=(i+1)*rise if side==0 else mid+(half-1-i)*rise
            r=[x+side*1.4,y+i*s['going'],1,s['going']]
            o=pb(s['id']+' closed tread',r,base+z-rise,base+z,wood,.004);o['stair_id']=s['id']
            pb(s['id']+' tread nosing',[r[0],r[1]-.018,1,.035],base+z-.018,base+z+.002,oak,.006)
        xx=x+1 if side==0 else x+1.4
        pts=[]
        for i in range(2*(half-1)+1):
            yy=y+i*s['going']/2;z=(1+i/2)*rise if side==0 else LEVELS[s['upper']]-(i/2)*rise
            tube(s['id']+' baluster',[(xx,-yy,base+z-.02),(xx,-yy,base+z+.90)],.012,metal);pts.append((xx,-yy,base+z+.91))
        tube(s['id']+' oak handrail',pts,.026,wood)
    pb(s['id']+' half landing',[x,y+run,2.4,d-run],base+mid-.16,base+mid,wood)
    tube(s['id']+' landing rail',[(x+1,-y-run-.48,base+mid+.91),(x+1.4,-y-run-.48,base+mid+.91)],.026,wood)
    for i in range(6):
        xx=x+.08+i*.23
        tube(s['id']+' upper guard',[(xx,-y-.01,LEVELS[s['upper']]+.04),(xx,-y-.01,LEVELS[s['upper']]+1.04)],.014,metal)
    tube(s['id']+' top guard rail',[(x,-y-.01,LEVELS[s['upper']]+1.04),(x+1.35,-y-.01,LEVELS[s['upper']]+1.04)],.026,wood)

# Roof planes share valley edges. Each light well removes the ceiling and roof skin.
col=roofcol
for poly,fn,name in roofs():
    pieces=[poly]
    if name=='House':
        for r in data['rooflights']:pieces=[q for p in pieces for q in subtract_rect(p,r['r'])]
    for i,piece in enumerate(pieces):surface(name+' zinc roof',piece,fn,roofmat,.16)
    for k in range(math.floor(min(x for x,y in poly)/.43),math.ceil(max(x for x,y in poly)/.43)):
        x=k*.43;segments=clip(poly,lambda xx,yy:xx-x)
        segments=clip(segments,lambda xx,yy:x+.014-xx) if segments else []
        pieces=[segments] if segments else []
        if name=='House':
            for r in data['rooflights']:pieces=[q for p in pieces for q in subtract_rect(p,r['r'])]
        for q in pieces:surface(name+' standing seam',q,lambda xx,yy:fn(xx,yy)+.025,roofmat,.025)
for poly,base,fn in [(data['house'],6.2,roof_height),(data['office'],5.7,lambda x,y:5.9+1.85*(1-abs(x-22.3)/3.75)),(rect(18.7,7.3,7.2,4.15),2.7,lambda x,y:2.9+1.1*(1-abs(x-22.3)/3.75)),(rect(16.2,11.35,2.5,2.4),3.2,lambda x,y:3.65-(y-11.23)*.07),(data['plant'],2.7,lambda x,y:3.10-(y-4.03)*.035),(rect(18.7,20.8,7.2,.4),2.7,lambda x,y:3.1-(y-20.8)*.16)]:
    for a0,a1 in zip(poly,poly[1:]+poly[:1]):
        steps=max(2,math.ceil(math.dist(a0,a1)/.14));profile=[]
        for i in range(steps+1):
            t=i/steps;x=a0[0]+t*(a1[0]-a0[0]);y=a0[1]+t*(a1[1]-a0[1]);profile.append((x,-y,fn(x,y)-.02))
            if 0<i<steps and fn(x,y)-base>.08:
                tube('Upper gable board seam',[(x,-y,base),(x,-y,fn(x,y)-.045)],.012,wood)
        vertices=[(a0[0],-a0[1],base),(a1[0],-a1[1],base),*reversed(profile)]
        ob=mesh('Gable and eaves closure',vertices,[tuple(range(len(vertices)))],oak)
        mod=ob.modifiers.new('Gable cladding thickness','SOLIDIFY');mod.thickness=.06
for r in data['rooflights']:
    x,y,w,d=r['r'];poly=rect(x,y,w,d)
    for region,fn,name in roofs():
        if name!='House':continue
        q=region
        for bound in [lambda xx,yy:xx-x,lambda xx,yy:x+w-xx,lambda xx,yy:yy-y,lambda xx,yy:y+d-yy]:
            q=clip(q,bound) if q else []
        if q:surface(r['id']+' rooflight glass',q,lambda xx,yy:fn(xx,yy)+.04,glass,.02)
    for p0,p1 in zip(poly,poly[1:]+poly[:1]):
        x0,y0=p0;x1,y1=p1
        points=[(x0+(x1-x0)*i/20,y0+(y1-y0)*i/20) for i in range(21)]
        vertices=[(x0,-y0,6.2),(x1,-y1,6.2)]+[(xx,-yy,roof_height(xx,yy)-.13) for xx,yy in reversed(points)]
        mesh(r['id']+' plaster light well',vertices,[tuple(range(len(vertices)))],ivory)
        tube(r['id']+' curb and flashing',[(xx,-yy,roof_height(xx,yy)+.055) for xx,yy in points],.055,black)
        tube(r['id']+' roof trimmer',[(xx,-yy,roof_height(xx,yy)-.15) for xx,yy in points],.06,oak)
for x,y,d,z in [(-.18,-.18,15.16,6.41),(6.99,-.18,5,6.46),(18.55,11.3,9.65,5.9),(26.05,11.3,9.65,5.9),(18.55,7.15,4.15,2.9),(26.05,7.15,4.15,2.9)]:
    tube('Zinc eaves gutter',[(x,-y,z),(x,-y-d,z)],.065,roofmat)
    tube('Rainwater downpipe',[(x,-y-.2,z),(x,-y-.2,.18)],.042,roofmat)
for y in [4.82,14.98]:tube('East wing gutter',[(7.08,-y,6.41),(16.38,-y,6.41)],.065,roofmat)

# Upper external boards give real facade relief while respecting the openings.
for f in ['u','o']:
    col=cols[f,'walls'];base=LEVELS[f];shell=data['shells'][f][0]
    for p0,p1 in zip(shell,shell[1:]+shell[:1]):
        length=math.dist(p0,p1);dx=(p1[0]-p0[0])/length;dy=(p1[1]-p0[1])/length
        for i in range(math.ceil(length/.14)):
            u=min(length-.04,(i+.5)*.14);x=p0[0]+dx*u;y=p0[1]+dy*u;intervals=[(base,base+2.7)]
            for d in openings(data,f):
                on=(abs(y-d['y'])<.21 and d['axis']=='h' and d['x']-.04<x<d['x']+d['w']+.04) or (abs(x-d['x'])<.21 and d['axis']=='v' and d['y']-.04<y<d['y']+d['w']+.04)
                if on:intervals=[q for l,h in intervals for q in [(l,min(h,base+d['lo'])),(max(l,base+d['hi']),h)] if q[1]-q[0]>.001]
            for lo,hi in intervals:box('Vertical oak facade batten',(x,-y,(lo+hi)/2),(.035,.045,hi-lo) if abs(dx)>.5 else (.045,.035,hi-lo),wood,.002)


def chair(name,x,y,z,w=.65,d=.65,m=fabric,turn=False):
    before=set(col.objects)
    box(name+' upholstered seat',(x+w/2,-y-d/2,z+.46),(w-.08,d-.08,.14),m,.055)
    box(name+' curved back',(x+w/2,-y-.08,z+.77),(w-.10,.10,.48),m,.045)
    for xx in [x+.10,x+w-.10]:
        for yy in [y+.10,y+d-.10]:tube(name+' tapered leg',[(xx,-yy,z),(xx,-yy,z+.40)],.025,wood)
    for xx in [x+.04,x+w-.04]:tube(name+' oak arm',[(xx,-y-.10,z+.62),(xx,-y-d+.1,z+.60)],.025,wood)

    if turn:
        matrix=Matrix.Translation((x+w/2,-y-d/2,0))@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation((-x-w/2,y+d/2,0))
        for obj in set(col.objects)-before:obj.matrix_world=matrix@obj.matrix_world

def bowl(name,x,y,z,w,d,depth,m=white):
    vs=[];fs=[];N=48
    for scale,zz in [(1,z),(.86,z+.012),(.64,z-depth*.7),(.1,z-depth)]:
        for i in range(N):
            t=i*math.tau/N;vs.append((x+w/2*scale*math.cos(t),-y+d/2*scale*math.sin(t),zz))
    for k in range(3):
        for i in range(N):fs.append((k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i))
    fs.append(tuple(range(3*N,4*N)));o=mesh(name,vs,fs,m)
    for p in o.data.polygons:p.use_smooth=True
    mod=o.modifiers.new('Ceramic shell','SOLIDIFY');mod.thickness=.018
    cyl(name+' waste',(x,-y,z-depth+.016),.022,.008,metal)


def faucet(x,y,z):
    tube('Bronze tap',[(x,-y,z),(x,-y,z+.22),(x,-y-.14,z+.22),(x,-y-.14,z+.17)],.012,metal)
    cyl('Tap lever',(x+.05,-y,z+.05),.015,.10,metal)


def cabinet(name,r,z,h=2.35,front='south',shelves=False):
    x,y,w,d=r
    long=w if w>=d else d;depth=(d if w>=d else w)-.09
    root=bpy.data.objects.new(name,None);col.objects.link(root);root['level']=col.get('level');root['part']='furniture';root['footprint']=r
    def local(n,pos,dim,m,bevel=.004):
        o=box(name+' '+n,pos,dim,m,bevel);o.parent=root;return o
    if shelves:
        for u in [.018,long-.018]:local('side',(u,0,h/2),(.036,depth,h),wood)
        for zz in [.025,h-.025]:local('top and base',(long/2,0,zz),(long,depth,.05),wood)
        local('back',(long/2,depth/2-.015,h/2),(long,.03,h),wood)
    else:
        local('carcass',(long/2,0,h/2), (long,depth-.04,h),wood)
    bays=max(1,round(long/.65));bw=long/bays
    for i in range(bays):
        u=(i+.5)*bw
        if shelves:
            local('dark recess',(u,depth/2-.030,h/2),(bw-.05,.022,h-.08),black)
            for zz in [.12,.5,.9,1.3,1.7,2.1]:
                if zz>h:continue
                local('shelf',(u,-.025,zz),(bw-.04,depth,.026),wood)
                for j in range(max(2,int(bw/.07)-2)):
                    bh=min(rng.uniform(.18,.31),h-zz-.065);xx=i*bw+.06+j*.068
                    bookmat=[olive,blue,ivory,stone2][j%4]
                    local('bound book',(xx,-depth/2+.09,zz+bh/2+.015),(.043,.16,bh),bookmat,.001)
        else:
            local('recessed door',(u,-depth/2-.003,h/2),(bw-.026,.022,h-.06),ivory)
            for xx in [i*bw+.032,(i+1)*bw-.032]:local('frame stile',(xx,-depth/2-.018,h/2),(.046,.018,h-.04),wood)
            for zz in [.035,h-.035]:local('frame rail',(u,-depth/2-.018,zz),(bw-.09,.018,.045),wood)
            local('bronze pull',(u+bw*.28,-depth/2-.04,min(1.1,h*.6)),(.014,.018,.14),metal)
        local('toe recess',(u,0,.055),(bw-.05,depth-.11,.10),black)
    if w>=d:
        root.location=(x,-y-d/2,z)
        if front=='north':root.rotation_euler.z=math.pi;root.location.x=x+w
    else:
        root.rotation_euler.z=math.pi/2 if front=='east' else -math.pi/2
        root.location=(x+w/2,-y-d if front=='east' else -y,z)
    return root


furniture_records=[]
for f in data['furniture']:
    if f['roomId'] in ['G1','G2','G3','G10']:continue
    floor=f['floor'];col=cols[floor,'furniture'];z=LEVELS[floor]+.04;x,y,w,d=f['r'];name=f['name'];kind=f['kind'];lc=name.lower()
    before=set(col.objects)
    if kind=='bed':
        along_x=w>d
        bw,bd=(d,w) if along_x else (w,d)
        parent=bpy.data.objects.new(name,None);col.objects.link(parent)
        def bedbox(n,pos,dim,m,bevel=.03):
            o=box(name+' '+n,pos,dim,m,bevel);o.parent=parent;return o
        bedbox('oak base',(bw/2,-bd/2,.26),(bw-.035,bd-.035,.30),wood,.035)
        bedbox('piped mattress',(bw/2,-bd/2,.49),(bw-.09,bd-.07,.23),white,.075)
        bedbox('linen headboard',(bw/2,-.055,.75),(bw-.04,.11,1.25),fabric,.04)
        for xx in [.07,bw-.07]:
            for yy in [.12,bd-.12]:o=cyl(name+' bed foot',(xx,-yy,.08),.04,.16,wood);o.parent=parent
        for xx in [bw*.28,bw*.72]:
            o=bedbox('piped pillow',(xx,-.39,.675),(bw*.40,.50,.15),white,.068);o.rotation_euler.z=.035 if xx<bw/2 else -.035
        vs=[];fs=[];N=26;M=32
        for j in range(M+1):
            yy=.64+(bd-.67)*j/M
            for i in range(N+1):
                xx=.025+(bw-.05)*i/N;zz=.635+.012*math.sin(xx*29+yy*7)+.007*math.sin(yy*32)
                vs.append((xx,-yy,zz))
        for j in range(M):
            for i in range(N):k=j*(N+1)+i;fs.append((k,k+1,k+N+2,k+N+1))
        o=mesh(name+' draped duvet',vs,fs,fabric);o.parent=parent
        for face in o.data.polygons:face.use_smooth=True
        mod=o.modifiers.new('Soft cloth folds','SUBSURF');mod.levels=2
        o.modifiers.new('Duvet loft','SOLIDIFY').thickness=.035
        bedbox('folded throw',(bw/2,-bd+.37,.672),(bw-.02,.55,.045),blue if floor=='u' else olive,.02)
        parent.location=(x,-y,z)
        if along_x:parent.rotation_euler.z=math.pi/2;parent.location.y=-y-d
    elif kind=='table':
        pb(name+' solid oak top',f['r'],z+.72,z+.77,wood,.016)
        for xx in [x+.07,x+w-.07]:
            for yy in [y+.07,y+d-.07]:tube(name+' trestle',[(xx,-yy,z),(xx,-yy,z+.72)],.03,metal)
        if any(q in lc for q in ['desk','worktop']):
            box(name+' monitor',(x+w/2,-y-d*.4,z+1.1),(min(.68,w*.8),.045,.38),black,.012)
            cyl('Monitor stand',(x+w/2,-y-d*.4,z+.85),.028,.18,metal)
            pb('Keyboard',[x+w*.22,y+d*.62,min(.46,w*.6),.16],z+.77,z+.79,black)
            for j in range(3):pb('Desk notebook',[x+.06,y+.05,.21,.27],z+.77+j*.022,z+.79+j*.022,[olive,ivory,blue][j])
    elif kind=='chair':chair(name,x,y,z,w,d,blue)
    elif kind=='sofa':
        pb(name+' plinth',[x+.04,y+.04,w-.08,d-.08],z+.12,z+.26,wood,.025)
        for xx in [x+.13,x+w-.13]:
            for yy in [y+.13,y+d-.13]:cyl(name+' oak foot',(xx,-yy,z+.075),.035,.15,wood)
        pb(name+' back',[x+.035,y+d-.195 if f['roomId']=='G7' else y+.025,w-.07,.17],z+.26,z+.83,fabric,.075)
        for xx in [x+.035,x+w-.165]:pb(name+' arm',[xx,y+.05,.13,d-.1],z+.26,z+.65,fabric,.05)
        for i in range(3):pb(name+' cushion',[x+.19+i*(w-.38)/3,y+.05 if f['roomId']=='G7' else y+.20,(w-.38)/3-.018,d-.25],z+.28,z+.49,olive,.075)
    elif kind=='glass':pb(name,f['r'],z,z+2.05,glass,.001)
    elif kind=='wc':
        pb(name+' concealed cistern',[x+w*.1,y,w*.8,.16],z,z+1.15,ivory,.025)
        ellipsoid(name+' pan',(x+w/2,-y-d*.52,z+.30),(w*.37,d*.42,.21),white)
        bowl(name+' seat',x+w/2,y+d*.55,z+.445,w*.71,d*.65,.085,white)
        pb(name+' flush plate',[x+w*.32,y+.165,w*.35,.012],z+.95,z+1.04,metal)
    elif kind=='basin':
        pb(name+' floating oak vanity',f['r'],z+.28,z+.80,wood,.012)
        count=2 if 'double' in lc or 'two ' in lc else 1
        for i in range(count):
            xx=x+w*(i+.5)/count
            bowl(name+' vessel',xx,y+d*.53,z+.91,min(.49,w/count-.07),min(.36,d-.045),.12)
            faucet(xx,y+.045,z+.88)
            box(name+' mirror',(xx,-y-.024,z+1.60),(min(.6,w/count-.04),.018,.9),mirror,.018)
        for i in range(max(1,round(w/.6))):
            bw=w/max(1,round(w/.6));pb(name+' drawer',[x+i*bw+.014,y+d-.035,bw-.028,.027],z+.33,z+.75,wood,.006)
            tube('Vanity handle',[(x+i*bw+.12,-y-d-.001,z+.68),(x+(i+1)*bw-.12,-y-d-.001,z+.68)],.008,metal)
    elif kind=='bath' or (kind=='wet' and lc=='bath'):
        bowl(name,x+w/2,y+d/2,z+.61,w-.025,d-.025,.49)
        pb(name+' recessed base',[x+w*.32,y+d*.32,w*.36,d*.36],z,z+.15,white,.045)
        faucet(x+w*.85,y+d*.23,z+.64)
    elif kind=='wet':
        pb(name+' flush stone tray',f['r'],z,z+.026,stone2,.01)
        pb(name+' linear drain',[x+.1,y+d-.08,w-.2,.025],z+.027,z+.030,metal,.001)
        headx=x+w*.33;yy=y+d-.05
        tube(name+' riser',[(headx,-yy,z+1.0),(headx,-yy,z+2.18),(headx,-yy+.28,z+2.18)],.012,metal)
        cyl(name+' rainfall head',(headx,-yy+.28,z+2.16),.105,.022,metal)
        pb(name+' mixer',[headx-.12,yy-.02,.24,.05],z+1.02,z+1.07,metal)
        if f['roomId']!='U3':pb(name+' fixed screen',[x,y+d*.65,.015,d*.35],z,z+2.05,glass,.001)
    elif kind=='car':
        pb('Car sculpted lower body',[x+.10,y+.08,w-.20,d-.16],z+.28,z+.78,blue,.20)
        pb('Car passenger cabin',[x+1.35,y+.22,w-2.45,d-.44],z+.75,z+1.42,black,.22)
        for xx in [x+.94,x+w-.92]:
            for yy in [y+.06,y+d-.06]:
                o=cyl('Car wheel',(0,0,0),.35,.18,black,32);o.rotation_euler.x=math.pi/2;o.location=(xx,-yy,z+.35)
                o=cyl('Alloy wheel',(0,0,0),.23,.19,metal,24);o.rotation_euler.x=math.pi/2;o.location=(xx,-yy,z+.35)
        for yy in [y+.22,y+d-.40]:pb('Car headlamp',[x+.02,yy,.06,.20],z+.64,z+.73,white)
    elif 'privacy return' in lc:pb(name,f['r'],z,z+2.2,ivory)
    elif 'rack /' in lc:
        for xx in [x+.12,x+w-.12]:
            for yy in [y+.10,y+d-.10]:pb('Rack upright',[xx,yy,.065,.065],z,z+2.3,black)
        tube('Pull-up bar',[(x+.15,-y-.13,z+2.20),(x+w-.1,-y-.13,z+2.20)],.018,metal)
        tube('Racked barbell',[(x-.01,-y-.35,z+1.3),(x+w+.01,-y-.35,z+1.3)],.015,metal)
        for xx in [x+.25,x+w-.25]:
            o=cyl('Weight plate',(0,0,0),.19,.055,black);o.rotation_euler.y=math.pi/2;o.location=(xx,-y-.35,z+1.3)
    elif lc=='bench':
        pb('Gym bench cushion',[x+.05,y+.1,w-.10,d-.20],z+.42,z+.55,black,.06)
        for xx in [x+.15,x+w-.15]:pb('Gym bench leg',[xx,y+d/2-.08,.10,.16],z,z+.42,metal)
    elif lc=='treadmill':
        pb('Treadmill belt',f['r'],z+.06,z+.21,black,.03)
        for yy in [y+.05,y+d-.05]:tube('Treadmill side rail',[(x+.30,-yy,z+.2),(x+.30,-yy,z+1.2),(x+.90,-yy,z+1.05)],.025,metal)
        pb('Treadmill console',[x+.19,y+.12,.30,d-.24],z+1.15,z+1.25,black)
    elif lc=='dumbbells':
        pb('Dumbbell rack',f['r'],z+.20,z+.68,black)
        for i in range(7):
            yy=y+.14+i*.26
            tube('Dumbbell grip',[(x+.04,-yy,z+.75),(x+w-.04,-yy,z+.75)],.016,metal)
            for xx in [x+.08,x+w-.08]:
                o=cyl('Dumbbell end',(0,0,0),.065,.07,black,12);o.rotation_euler.y=math.pi/2;o.location=(xx,-yy,z+.75)
    elif 'cylinder' in lc:
        cyl('Insulated hot water cylinder',(x+w/2,-y-d/2,z+.85),.39,1.65,white,40)
        for xx in [x+.12,x+w-.12]:tube('Cylinder pipe',[(xx,-y-.13,z+.15),(xx,-y-.13,z+2.4)],.018,metal)
    elif 'ventilation' in lc or lc=='controls':
        pb(name,f['r'],z+.35,z+1.60,ivory,.025)
        for i in range(12):pb('Vent grille',[x+.07,y+d-.001,w-.14,.009],z+.5+i*.07,z+.514+i*.07,metal,.001)
    else:
        if 'bedside' in lc:
            cabinet(name,f['r'],z,.55)
            cyl('Bedside lamp foot',(x+w/2,-y-d/2,z+.56),.075,.03,metal)
            cyl('Bedside lamp stem',(x+w/2,-y-d/2,z+.75),.022,.35,metal)
            cyl('Linen bedside shade',(x+w/2,-y-d/2,z+.94),.135,.22,fabric)
            light('Bedside glow',(x+w/2,-y-d/2,z+.86),(x+w/2,-y,z+.1),10,.15)
        elif 'bench' in lc:pb(name,f['r'],z+.38,z+.46,wood,.014)
        else:
            room=next(r for r in data['rooms'] if r['id']==f['roomId'])
            xmin=min(q[0] for q in room['p']);xmax=max(q[0] for q in room['p'])
            front='south' if w>=d else ('east' if abs(x-xmin)<abs(x+w-xmax) else 'west')
            if 'bathroom side' in lc:front='north'
            cabinet(name,f['r'],z,.90 if 'workbench' in lc else 2.32,front,any(q in lc for q in ['shel','library']))
    made=[o for o in col.objects if o not in before]
    for o in made:o['room_id']=f['roomId'];o['furniture_source']=name
    furniture_records.append(dict(name=name,room=f['roomId'],floor=floor,r=f['r'],objects=len(made)))

for room in [r for r in data['rooms'] if r['id'] in ['U1','U4','U5','U6','G5']]:
    floor=room['floor'];col=cols[floor,'furniture'];base=LEVELS[floor]
    for d in [d for d in data['windows'] if d['floor']==floor and d['axis']=='h' and any(inside(d['x']+d['w']/2,d['y']+dy,room['p']) for dy in [-.2,.2])]:
        yy=d['y']+(.22 if d['y']<8 else -.22)
        for xx in [d['x']-.05,d['x']+d['w']-.24]:
            vs=[];fs=[]
            for i in range(31):
                x=xx+i*.30/30
                for j in range(15):vs.append((x,-yy+.027*math.cos(i*math.pi/3),base+.07+j*2.53/14))
            for i in range(30):
                for j in range(14):k=i*15+j;fs.append((k,k+15,k+16,k+1))
            o=mesh(room['id']+' linen curtain',vs,fs,fabric);o.modifiers.new('Linen thickness','SOLIDIFY').thickness=.001

# Site coordinates are translated from the unchanged assumed plot.
col=sitecol
origin=data['site']['house_origin']
def sitepoly(poly):return [[x-origin[0],y-origin[1]] for x,y in poly]
def sitebox(name,r,lo,hi,m):return pb(name,[r[0]-origin[0],r[1]-origin[1],r[2],r[3]],lo,hi,m)
plot=sitepoly(rect(0,0,40,65))
surface('Assumed plot - 40 x 65 m',plot,-.12,grassmat,.15)
surface('Coastal land beyond plot',rect(-200,-160,400,220),-.32,grassmat)
sea=mat('Coastal | sea',(.085,.24,.29),.20,.15,noise=.18,scale=1.4)
surface('Sea beyond assumed dune edge',rect(-350,-500,700,435),-.65,sea)
forecourt=sitepoly(data['site']['forecourt']);surface('Permeable arrival court',forecourt,-.055,soil,.08)
for r in data['site']['visitor_bays']:sitebox('Visitor parking',r,-.07,-.045,soil)
terraces=[rect(.0,-4,16.2,4),rect(6.9,0,9.3,5),rect(16.2,9.5,2.5,2.0),rect(9.5,14.8,3.3,2.1)]
for p in terraces:
    surface('Limestone terrace base',p,-.055,stone2,.09)
    for r in cells([p],[]):
        x,y,w,d=r
        for i in range(math.ceil(w/.9)):
            for j in range(math.ceil(d/.6)):
                ww=min(.9,w-i*.9)-.006;dd=min(.6,d-j*.6)-.006
                if ww>.01 and dd>.01:pb('Honed limestone terrace slab',[x+i*.9+.003,y+j*.6+.003,ww,dd],-.045,-.014,stone2,.003)
for r in [[-2,-18,1.4,33],[16.5,-19,1.4,27],[1,-20,17,.95],[26.5,0,1.2,28],[10,16.7,2,3.0]]:surface('Gravel garden path',rect(*r),-.04,soil,.06)
for i in range(10):pb('Garden stepping stone',[5.4,-5.5-i*1.22,.9,.65],-.03,-.005,stone2,.025)
# Low stone edges and an open garden boundary keep the sea-facing side light.
for r in [[-6,-28,40,.32],[-6,-28,.32,65],[33.68,-28,.32,65],[-6,36.7,12.25,.3],[12.25,36.7,21.75,.3]]:
    pb('Rubble boundary wall',r,-.12,.65,stone,.025)
    x,y,w,d=r
    for i in range(math.ceil(max(w,d)/.55)):
        if w>d:rr=[x+i*.55,y-.03,min(.54,w-i*.55),d+.06]
        else:rr=[x-.03,y+i*.55,w+.06,min(.54,d-i*.55)]
        if min(rr[2:])>.01:pb('Boundary coping',rr,.65,.73,stone2,.025)
for x in [6.25,12.25]:pb('Arrival gate pier',[x-.23,36.40,.46,.65],-.12,1.35,stone,.025)
for x in [6.55,9.45]:
    for i in range(14):pb('Oak entrance gate slat',[x+i*.19,36.69,.13,.065],.05,1.0,wood,.008)
    for z in [.22,.86]:pb('Gate rail',[x,36.72,2.6,.065],z,z+.08,oak)


def grass_patch(name,centres,m=straw,height=.65):
    vs=[];fs=[]
    for x,y in centres:
        for j in range(28):
            ang=rng.random()*math.tau;r=rng.random()*.22;h=height*rng.uniform(.55,1.35);lean=rng.uniform(.1,.32)
            xx=x+r*math.cos(ang);yy=y+r*math.sin(ang);width=rng.uniform(.009,.022);k=len(vs)
            for t in [0,.45,.8,1]:
                xx1=xx+math.cos(ang)*lean*t*t;yy1=yy+math.sin(ang)*lean*t*t
                vs.extend([(xx1-width*(1-t),-yy1,-.02+h*t),(xx1+width*(1-t),-yy1,-.02+h*t)])
            fs.extend([(k+i*2,k+i*2+1,k+i*2+3,k+i*2+2) for i in range(3)])
    return mesh(name,vs,fs,m)


def shrub(name,x,y,r=.6,h=.7,m=leaf):
    vs=[];fs=[]
    for j in range(170):
        ang=rng.random()*math.tau;rad=r*math.sqrt(rng.random());xx=x+rad*math.cos(ang);yy=y+rad*math.sin(ang);zz=.03+h*math.sqrt(max(0,1-(rad/r)**2))*rng.uniform(.5,1.1)
        sz=rng.uniform(.035,.095);k=len(vs);tilt=rng.random()*math.tau
        vs.extend([(xx-sz*math.cos(tilt),-yy+sz*math.sin(tilt),zz),(xx,-yy,zz+.035),(xx+sz*math.cos(tilt),-yy-sz*math.sin(tilt),zz),(xx,-yy-.04,zz-.025)]);fs.append((k,k+1,k+2,k+3))
    return mesh(name,vs,fs,m)

beds=[[-4.7,-25,2.0,46],[29,-25,3.5,49],[-2.5,-24,31,2.6],[.2,-7.4,4.5,2.3],[7.2,-6.6,8.5,1.8],[17.9,-15.5,7.7,1.8],[27.6,11,1.1,19],[-2,21,3.5,12]]
for index,r in enumerate(beds):
    pb('Coastal gravel planting bed',r,-.10,-.045,soil,.06)
    x,y,w,d=r;centres=[]
    for j in range(round(w*d*3)):
        xx=x+.15+rng.random()*(w-.3);yy=y+.15+rng.random()*(d-.3);centres.append((xx,yy))
        if j%7==0:shrub('Silver windbreak shrub',xx,yy,.30,.45,silver if j%2 else leaf)
        if j%15==0:shrub('Lavender flower mound',xx,yy,.22,.32,flower)
    grass_patch('Wind-shaped coastal grasses',centres,straw,.45 if index>2 else .8)
for x,y,h in [(-3.1,-16,4.2),(-3,-7,3.4),(30,-15,4.7),(30,-4,4.0),(28,25,3.7),(-3,27,4.1)]:
    tube('Wind-shaped tree trunk',[(x,-y,0),(x+.18,-y,h*.6),(x+.6,-y-.18,h*.9)],.085,oak)
    for j in range(9):
        angle=j*math.tau/9;xx=x+.55+math.cos(angle)*.95;yy=y+math.sin(angle)*.85
        tube('Tree branch',[(x+.18,-y,h*.6),(xx,-yy,h*.85)],.028,oak)
        o=shrub('Fine coastal tree crown',xx,yy,1.0,.75,silver);o.location.z=h*.67
# Kitchen garden, storage and a sheltered outdoor wash point.
for x in [20.0,23.3]:
    for y in [-11.5,-7.9]:
        pb('Raised growing bed',[x,y,2.4,2.5],-.02,.38,oak,.02);pb('Growing compost',[x+.08,y+.08,2.24,2.34],.38,.40,soil)
        for i in range(4):
            for j in range(4):o=shrub('Kitchen garden herbs',x+.35+i*.52,y+.35+j*.53,.19,.28,leaf);o.location.z=.43
pb('Garden tool store',[27.1,1.0,2.2,3],-.02,2.15,oak)
surface('Tool store zinc roof',rect(27,0.9,2.4,3.2),lambda x,y:2.25-.1*(y-.9),roofmat,.08)
for i in range(13):pb('Store door timber board',[27.2+i*.15,.98,.13,.035],.06,1.98,wood)
tube('Outdoor shower riser',[(26.7,-5.2,.10),(26.7,-5.2,2.2),(26.4,-5.2,2.2)],.018,metal)
cyl('Outdoor shower head',(26.4,-5.2,2.17),.11,.025,metal)
pb('Outdoor shower drained base',[25.95,4.5,1.15,1.4],-.04,-.015,stone2)
for j in range(3):pb('Compost bin',[29.8+j*.95,4.7,.85,1.3],-.05,.85,oak)
# Oak pergola and dining furniture sit in the sheltered inner angle.
for x in [10.1,15.5]:
    for y in [.25,4.35]:pb('Pergola oak post',[x,y,.15,.15],-.02,2.75,wood,.01)
for y in [.32,4.42]:box('Pergola beam',(12.88,-y,2.75),(5.75,.15,.19),wood,.01)
for i in range(14):box('Pergola rafter',(10.0+i*.44,-2.38,2.89),(.075,4.7,.13),wood,.008)
pb('Outdoor dining table',[11.3,1.3,2.8,1.05],.72,.78,wood,.016)
for xx in [11.48,13.92]:
    for yy in [1.45,2.20]:pb('Outdoor table leg',[xx,yy,.10,.10],0,.72,wood)
for i in range(3):
    chair('Outdoor dining chair',11.45+i*.87,.48,0,.58,.58,fabric)
    chair('Outdoor dining chair',11.45+i*.87,2.66,0,.58,.58,fabric,True)
for x in [1.1,3.1]:
    for j in range(18):pb('Sun lounger timber slat',[x,-3.5+j*.10,.8,.083],.27,.31,wood)
    pb('Lounger linen cushion',[x+.04,-3.45,.72,1.68],.31,.38,fabric,.04)
    for xx in [x+.07,x+.65]:
        for yy in [-3.4,-2.0]:pb('Lounger foot',[xx,yy,.08,.08],0,.27,wood)
# Separate sea-view seating circle beyond the lawn.
surface('Sea view gravel seating',rect(7.8,-22,7.2,3.7),-.055,soil,.05)
for x in [8.5,10.0,12.5]:chair('Sea view oak chair',x,-21.5,0,.78,.82,fabric)
cyl('Low circular outdoor table',(11.8,19.5,.35),.58,.065,stone2,48)
for x,y in [(-1.35,-15),(-1.35,-5),(17.15,-12),(17.15,-3),(27.1,20),(10.9,18),(7.5,30),(13.6,31)]:
    pb('Shielded path bollard',[x-.045,y-.045,.09,.09],-.04,.65,black)
    pb('Warm bollard lens',[x-.032,y-.049,.064,.012],.52,.58,white)
for x,y in [(1,-4.6),(5.0,-4.6),(15.6,4.4),(10.2,15.5)]:
    cyl('Terracotta planter',(x,-y,.22),.32,.45,stone,32);o=shrub('Planter aromatic shrub',x,y,.4,.65,silver);o.location.z=.45

detail_path=Path(__file__).parent/'coastal/details.py'
exec(compile(detail_path.read_text(),str(detail_path),'exec'))

scene.world=bpy.data.worlds.new('Coastal daylight');scene.world.use_nodes=True
n=scene.world.node_tree.nodes;l=scene.world.node_tree.links
sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(32);sky.sun_rotation=math.radians(125);sky.sun_disc=False
l.new(sky.outputs['Color'],n['Background'].inputs['Color']);n['Background'].inputs['Strength'].default_value=.10
sun=bpy.data.lights.new('Coastal afternoon sun','SUN');sun.energy=2.4;sun.angle=math.radians(3);sun.color=(1,.91,.80)
o=bpy.data.objects.new(sun.name,sun);lightcol.objects.link(o);o.rotation_euler=(math.radians(27),math.radians(-26),math.radians(-32))
views={
 'arrival':([-16,-42,14],[11,-10,3],36,'all'),
 'garden':([24,22,12],[10,-6,3.5],35,'all'),
 'coastal-plot':([59,54,52],[12,-1,0],45,'all'),
 'ground-cutaway':([32,-37,33],[13,-10,0],42,'ground'),
 'first-cutaway':([32,-37,36],[13,-10,3.5],42,'first'),
 'parents-bedroom':([5.85,-3.30,5.12],[2.9,-.95,4.50],22,'all'),
 'suite-gallery':([6.0,-9.70,5.10],[5.95,-3.4,4.95],22,'all'),
 'dressing':([4.94,-5.17,5.10],[.9,-5.1,4.7],22,'all'),
 'bathroom':([3.29,-7.70,5.14],[1.10,-8.05,4.70],18,'all'),
 'bathroom-vanity':([1.40,-8.00,5.10],[2.90,-6.83,4.85],22,'all'),
 'family-bedroom':([10.6,-9.13,5.12],[8.2,-6.2,4.55],24,'all'),
 'library':([7.7,-11.6,1.65],[5.8,-13.3,1.15],22,'all'),
 'gym':([24.8,-11.15,1.65],[20.5,-8.7,1.0],24,'all'),
 'office':([19.6,-19.8,4.65],[24.6,-15.3,4.0],23,'all'),
 'combined-room':([1.2,-8.65,1.65],[8.4,-6.65,1.35],23,'all'),
 'terrace':([19,7,3.1],[9.3,-1.5,1.3],30,'all')}
cameras={}
for name,(pos,target,lens,mode) in views.items():
    d=bpy.data.cameras.new(name);d.lens=lens;d.clip_start=.035;d.clip_end=1500
    o=bpy.data.objects.new(name,d);lightcol.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();cameras[name]=o
scene.camera=cameras['garden'];scene.unit_settings.system='METRIC';scene.unit_settings.length_unit='METERS';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=a.samples;scene.cycles.use_denoising=True;scene.cycles.max_bounces=10;scene.cycles.transmission_bounces=8
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU' if any(d.type=='METAL' for d in prefs.devices) else 'CPU'
scene.render.resolution_x=a.width;scene.render.resolution_y=round(a.width*2/3);scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.4
scene['revision']='L01.1 coastal coordinated study';scene['source_hashes']=json.dumps(data['source_hashes']);scene['interior_source_sha256']=source_hash
scene['section']='House ceiling datum 3.20 m; first floor datum 3.50 m. Finished clear heights 3.16 m and 2.66 m with 40 mm floor finishes. Garage retains 3.00 m floor-to-floor.'
scene['plot']='Assumed 40 x 65 m coastal plot. Shoreline and planting are illustrative.'
for text in list(bpy.data.texts):bpy.data.texts.remove(text)
notes=bpy.data.texts.new('READ ME - coastal house')
notes.write(scene['section']+'\n'+scene['plot']+'\nMeasured source: studies/l-house-booklet/plans.json L01.1. Option D pantry and combined room furniture retained. All parts carry level and part tags. Upper suite doors are shown open. Bedroom door is in its pocket. Burner stays in hidden OPTION collection. Local licensed composite: do not publish raw blend or GLB. Floor topping is 40 mm above the structural level; finish relief is up to 25 mm. See geometry-checks.json for tested scope.')
report={'revision':scene['revision'],'source_hashes':data['source_hashes'],'interior_source_sha256':source_hash,'levels':LEVELS,'ceiling_datum_heights':HEIGHTS,'finished_clear_heights':{f:round(h-.04,2) for f,h in HEIGHTS.items()},'stairs':data['stairs'],'rooflights':data['rooflights'],'rooms':data['rooms'],'wall_solids':wall_records,'furniture':furniture_records,'views':views,'objects':len(scene.objects),'limits':['Unsurveyed plot; illustrative coast, planting and daylight.','Proposed floor zone and roof structure require design.','Burner stored as hidden option because its vertical flue conflicts with the gallery.','Product specifications, services and occupied-use checks are not construction approval.']}
(O/'model-report.json').write_text(json.dumps(report,indent=2))
(O/'coordinated-plan.json').write_text(json.dumps(data,indent=2))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'coastal-house.blend'),compress=True)
if a.export:
    from preview import export_preview
    export_preview(O/'coastal-house.glb')
for name in a.views:
    mode=views[name][3]
    for o in scene.objects:
        if o.type in ['CAMERA','LIGHT']:continue
        f=o.get('level','g');part=o.get('part','interior')
        o.hide_render=part=='option' or (mode!='all' and (part in ['roof','ceilings'] or (mode=='ground' and f in ['u','o']) or (mode=='first' and f in ['g','a'])))
    scene.camera=cameras[name];scene.render.filepath=str(O/(name+'.png'));bpy.ops.render.render(write_still=True)
assert hashlib.sha256(a.interior.read_bytes()).hexdigest()==source_hash
print('COASTAL_BUILD_COMPLETE',len(scene.objects),flush=True)
