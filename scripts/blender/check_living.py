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
assert len(reservations)==9,len(reservations)
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
ottoman=plan_bounds('Ottoman cushioned top')
for name in ('Sofa upholstered base','Corner return upholstered base'):
    sofa=plan_bounds(name)
    assert ottoman[0]>=sofa[1]+.35 or ottoman[2]>=sofa[3]+.35 or sofa[0]>=ottoman[1]+.35 or sofa[2]>=ottoman[3]+.35,'Ottoman clearance from '+name
assert len([o for o in col.objects if o.name in ('Large river landscape','Large floral still life')])==2
assert bpy.data.objects['Log burner position study']['proposal_only']
assert not any(o.name=='Cream lounge armchair' for o in col.objects)
sofa_end=plan_bounds('Corner return end arm')[1]
console_front=min(plan_bounds(o.name)[0] for o in col.objects if o.type=='MESH' and o.parent and o.parent.name=='French country media cabinet')
assert console_front-sofa_end>=1.2,'Garden route beside sofa and console'
result={'retainedSourceObjects':count,'unchangedFurnitureCentresChecked':len(reservations),'chandelierShades':6,'packedTextures':True,'alternativesRetained':True,'gardenBifoldLeaves':6,'plantationShutterPanels':8,'gardenOpeningWidth':5.8,'ottomanClearanceAtLeast':.35,'gardenRouteWidthAtLeast':1.2,'largeArtworks':2,'stoveInstallationVerified':False}
(root/'output/blender/living-study/validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
