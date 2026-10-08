"""Place the approved furniture in a copy of the living study and render it."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,required=True)
parser.add_argument('--width',type=int,default=1800)
parser.add_argument('--samples',type=int,default=128)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
root=args.root.resolve();out=root/'output/blender/approved-room';out.mkdir(parents=True,exist_ok=True)
base=root/'output/blender/living-study/living-study.blend'
bpy.ops.wm.open_mainfile(filepath=str(base))
bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene
source={o['source_id']:(o.matrix_local.copy(),len(o.data.vertices) if o.type=='MESH' else None) for o in bpy.data.objects if 'source_id' in o}
oldchairs=[o for o in scene.objects if o.name.startswith('French country ladder-back chair') and o.type=='EMPTY']
chair_positions=[(o.location.copy(),o.rotation_euler.z,list(o['approved_footprint'])) for o in oldchairs]
assert len(chair_positions)==8
runner=bpy.data.objects['Cream linen table runner']
old_groups=[bpy.data.objects[n] for n in ('French country trestle table','Large oatmeal corner sofa','Oatmeal upholstered ottoman','French country media cabinet')]+oldchairs
for group in old_groups:
    for obj in [group,*group.children_recursive]:obj.hide_render=True;obj.hide_set(True)

names=['01 Table','02 Cane chair','03 Corner sofa','04 Square footstool','05 Media cabinet proposal']
with bpy.data.libraries.load(str(root/'output/blender/furniture-study/furniture-study.blend'),link=False) as (src,dst):
    dst.collections=names
assets={col.name:col for col in dst.collections}
for col in assets.values():scene.collection.children.link(col)

def place(col,origin,target,angle=0):
    bpy.context.view_layer.update()
    matrix=Matrix.Translation(Vector(target))@Matrix.Rotation(angle,4,'Z')@Matrix.Translation(-Vector(origin))
    col.hide_render=False;col.hide_viewport=False
    for obj in col.objects:
        obj.hide_render=False;obj.hide_set(False)
        if obj.parent is None:obj.matrix_world=matrix@obj.matrix_world
    bpy.context.view_layer.update()

floor=.0395
place(assets['01 Table'],(-3,0,0),(3.1,-6.6,floor))
place(assets['03 Corner sofa'],(2,1.5,0),(1.25,-3.075,floor),math.pi/2)
place(assets['04 Square footstool'],(1,-.5,0),(3.35,-3.40,.068))
place(assets['05 Media cabinet proposal'],(-3,2,0),(6.29,-2.50,floor),-math.pi/2)
newchairs=[]
chair_template=assets['02 Cane chair']
for i,(position,angle,reservation) in enumerate(chair_positions):
    col=bpy.data.collections.new('Approved cane dining chair %02d'%(i+1));scene.collection.children.link(col)
    for original in chair_template.objects:
        obj=original.copy();col.objects.link(obj)
        obj['chair_number']=i+1
    position.z=floor
    place(col,(-3,-1.1,0),position,angle)
    newchairs.append(col)
scene.collection.children.unlink(chair_template)
chair_template.hide_render=True;chair_template.hide_viewport=True

newrunner=runner.copy();newrunner.data=runner.data.copy();assets['01 Table'].objects.link(newrunner)
newrunner.name='Approved table linen runner';newrunner.parent=None
newrunner.matrix_world=Matrix.Translation((3.1,-6.6,floor+.773-.780))
for vertex in newrunner.data.vertices:vertex.co.x*=2.44/2.8
newrunner.hide_render=False;newrunner.hide_set(False)

# Keep the lamp supported by the shorter cabinet and match its new top height.
for obj in list(scene.objects):
    if obj.name.startswith(('Console ceramic lamp base','Console lamp neck','Console table lamp')):
        obj.location+=Vector((-.02,.18,-.0115))
    elif obj.name.startswith('Shade bound edge'):
        points=[obj.matrix_world@Vector(corner) for corner in obj.bound_box]
        centre=sum(points,Vector())/8
        if abs(centre.x-6.31)<.05 and abs(centre.y+3.53)<.05:
            obj.location+=Vector((-.02,.18,-.0115))

bpy.context.view_layer.update()
def world_points(col):
    deps=bpy.context.evaluated_depsgraph_get();points=[]
    for obj in col.objects:
        if obj.type in ('MESH','CURVE'):
            evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh()
            points.extend(evaluated.matrix_world@v.co for v in mesh.vertices)
            evaluated.to_mesh_clear()
    return points

def bounds(col):
    points=world_points(col)
    return [[min(p[i] for p in points),max(p[i] for p in points)] for i in range(3)]

table_points=[p for obj in assets['01 Table'].objects if obj!=newrunner and obj.type=='MESH' for p in (obj.matrix_world@Vector(c) for c in obj.bound_box)]
table_dimensions=[max(p[i] for p in table_points)-min(p[i] for p in table_points) for i in range(3)]
assert all(abs(a-b)<.003 for a,b in zip(table_dimensions,(2.44,1.09,.773))),('Table import dimensions',table_dimensions)
sofa=assets['03 Corner sofa'];ottoman=assets['04 Square footstool'];cabinet=assets['05 Media cabinet proposal']
sofa_base=next(o for o in sofa.objects if o.name.startswith('Sofa upholstered base'))
polygon=[(sofa_base.matrix_world@v.co).xy for v in sofa_base.data.vertices[:6]]
ob=bounds(ottoman)
rectangle=[Vector((x,y)) for x,y in [(ob[0][0],ob[1][0]),(ob[0][1],ob[1][0]),(ob[0][1],ob[1][1]),(ob[0][0],ob[1][1])]]
def distance(p,a,b):
    t=max(0,min(1,(p-a).dot(b-a)/(b-a).length_squared));return (p-a-t*(b-a)).length
clearance=min(distance(p,a,b) for shape,other in [(polygon,rectangle),(rectangle,polygon)] for p in shape for a,b in zip(other,other[1:]+other[:1]))
route=bounds(cabinet)[0][0]-bounds(sofa)[0][1]
assert clearance>=.35,('Footstool to sofa',clearance)
assert route>=1.20,('Sofa to cabinet',route)
assert all(any(o.name.startswith('Fixed upholstered seat') for o in col.objects) for col in newchairs)
assert not any(o.name.startswith(('Fitted cream upholstered seat','Seat welt')) for col in newchairs for o in col.objects)
for obj in bpy.data.objects:
    if 'source_id' not in obj:continue
    matrix,vertices=source[obj['source_id']]
    assert max(abs(matrix[i][j]-obj.matrix_local[i][j]) for i in range(4) for j in range(4))<.00001,obj.name
    if vertices is not None:assert len(obj.data.vertices)==vertices,obj.name
assert sum('source_id' in o for o in bpy.data.objects)==len(source)
assert all(i.packed_file for i in bpy.data.images if i.source=='FILE')
assert scene['proposed_ceiling_height']==3.2
for name in ('ALT - enclosed pantry ground floor','ALT - office guest bed'):assert bpy.data.collections[name].hide_render

prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for device in prefs.devices:device.use=device.type=='METAL'
scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
scene.render.resolution_x=args.width;scene.render.resolution_y=round(args.width*2/3);scene.render.resolution_percentage=100
scene.cycles.samples=args.samples;scene.cycles.use_denoising=True
scene['design_revision']='Approved furniture direction - 7 October 2026'
scene['scope_note']='Approved monastery table, fitted cane chairs, corner sofa, square oatmeal footstool and media cabinet in the existing living study. 3.2 m ceiling remains an interior proposal.'
report={'revision':scene['design_revision'],'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
    'source_objects_unchanged':len(source),'dining_chairs':len(newchairs),'fixed_upholstered_seats':True,
    'table_m':[round(v,3) for v in table_dimensions],'square_footstool_m':[1.25,1.25],
    'sofa_footstool_clearance_m':round(clearance,3),'sofa_cabinet_route_m':round(route,3),
    'ceiling_m':3.2,'packed_textures':True,'first_floor_coordinated':False,'asset_cost':0,
    'source_table':'https://www.blendkit.com/asset-gallery-detail/6f6bf86f-e227-42ba-a3eb-646081d93a0d/',
    'source_license':'BlenderKit Royalty Free; editable scene stays local',
    'website_changed':False,'views':[]}
camera=scene.camera
views=[('living-dining',(5.25,-8.8,1.60),(2.75,-2.9,1.40),24),
       ('hearth-dining',(1.8,-.83,1.65),(4.3,-5.8,1.15),24),
       ('seating-detail',(5.65,-5.0,1.50),(2.65,-2.85,.95),30)]
for name,location,target,lens in views:
    camera.location=location;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=lens
    if name=='living-dining':
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=str(out/'approved-room.blend'),compress=True)
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    report['views'].append(name+'.png')
(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('APPROVED_ROOM',json.dumps(report))
