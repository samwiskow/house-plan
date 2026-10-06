"""Check the realism study keeps the source geometry and furniture reservations."""
import json
import sys
from pathlib import Path
from mathutils import Vector

import bpy

root=Path(sys.argv[sys.argv.index('--')+1]).resolve()
bpy.ops.wm.open_mainfile(filepath=str(root/'output/blender/l-house/l-house.blend'))
source={o['source_id']:(o.matrix_local.copy(),len(o.data.vertices) if o.type=='MESH' else None) for o in bpy.data.objects if 'source_id' in o}
bpy.ops.wm.open_mainfile(filepath=str(root/'output/blender/living-study/living-study.blend'))
count=0
for o in bpy.data.objects:
    if 'source_id' not in o:continue
    matrix,vertices=source[o['source_id']]
    assert max(abs(matrix[i][j]-o.matrix_local[i][j]) for i in range(4) for j in range(4))<.00001,o.name
    if vertices is not None:assert len(o.data.vertices)==vertices,o.name
    count+=1
assert count==len(source)
assert all(i.packed_file for i in bpy.data.images if i.source=='FILE')
col=bpy.data.collections['Living study - detailed furniture and finishes']
assert len([o for o in col.objects if o.name.startswith('Ivory chandelier shade')])==6
reservations=[]
for o in col.objects:
    if 'approved_footprint' not in o:continue
    x,z,w,d=o['approved_footprint']
    assert abs(o.location.x-(x+w/2))<.0001 and abs(-o.location.y-(z+d/2))<.0001,o.name
    reservations.append(o.name)
assert len(reservations)==11,len(reservations)
seats=[o for o in bpy.data.objects if o.parent and o.parent.name=='g' and o.name.startswith('Island seat') and o.type=='EMPTY']
assert len(seats)==2 and all(not o.hide_render for o in seats),'Retain both island seats'
assert all(not child.hide_render for o in seats for child in o.children)
for colname in ('ALT - enclosed pantry ground floor','ALT - office guest bed'):
    assert bpy.data.collections[colname].hide_render
assert len([o for o in col.objects if o.name.startswith('Garden bifold leaf')])==6
assert len([o for o in col.objects if o.name.startswith('Plantation shutter panel')])==8
assert all(bpy.data.objects[name].hide_render for name in ('g / stone','g / stone.002','g / stone.004','Living to terrace'))
assert abs(bpy.context.scene['proposed_garden_opening_width']-5.8)<.001
bpy.context.view_layer.update()
def plan_bounds(name):
    o=bpy.data.objects[name]
    points=[o.matrix_world@Vector(p) for p in o.bound_box]
    return (min(p.x for p in points),max(p.x for p in points),min(-p.y for p in points),max(-p.y for p in points))
coffee=plan_bounds('Solid oak coffee top')
for name in ('Sofa upholstered base','Corner return upholstered base'):
    sofa=plan_bounds(name)
    assert coffee[0]>=sofa[1]+.35 or coffee[2]>=sofa[3]+.35 or sofa[0]>=coffee[1]+.35 or sofa[2]>=coffee[3]+.35,'Coffee table clearance from '+name
result={'retainedSourceObjects':count,'unchangedFurnitureCentresChecked':len(reservations),'chandelierShades':6,'packedTextures':True,'alternativesRetained':True,'gardenBifoldLeaves':6,'plantationShutterPanels':8,'gardenOpeningWidth':5.8,'coffeeTableClearanceAtLeast':.35}
(root/'output/blender/living-study/validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
