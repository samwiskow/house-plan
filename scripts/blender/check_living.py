"""Check the realism study keeps the source geometry and furniture reservations."""
import json
import sys
from pathlib import Path

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
assert len(reservations)==13,len(reservations)
seats=[o for o in bpy.data.objects if o.parent and o.parent.name=='g' and o.name.startswith('Island seat') and o.type=='EMPTY']
assert len(seats)==2 and all(not o.hide_render for o in seats),'Retain both island seats'
assert all(not child.hide_render for o in seats for child in o.children)
for colname in ('ALT - enclosed pantry ground floor','ALT - office guest bed'):
    assert bpy.data.collections[colname].hide_render
result={'retainedSourceObjects':count,'furnitureCentresChecked':len(reservations),'chandelierShades':6,'packedTextures':True,'alternativesRetained':True}
(root/'output/blender/living-study/validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
