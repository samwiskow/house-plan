"""Check the saved Blender study against its measured scene export."""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Matrix

root = Path(sys.argv[sys.argv.index('--') + 1]).resolve()
source = json.loads((root / 'tmp/blender-source/scene.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(root / 'output/blender/l-house/l-house.blend'))
C = Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
expected = {}

def visit(node, parent=Matrix.Identity(4), parent_name=''):
    a = node['matrix']
    world = parent @ Matrix([a[i::4] for i in range(4)])
    expected[node['id']] = (node, C @ world @ C.inverted(), parent_name)
    for child in node['children']:
        visit(child, world, node['name'])

for key in ('normal', 'enclosed', 'guest'):
    for node in source[key]:
        visit(node)
for col in bpy.data.collections:
    col.hide_viewport = False
bpy.context.view_layer.update()
checked = doors = geometry = 0
for obj in bpy.data.objects:
    if 'source_id' not in obj:
        continue
    node, matrix, parent_name = expected[obj['source_id']]
    if parent_name != 'Site' and not obj.get('study_detail'):
        actual = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world
        assert max(abs(actual[i][j]-matrix[i][j]) for i in range(4) for j in range(4)) < .00001, obj.name
        checked += 1
    if node.get('geometry') and not obj.get('study_detail'):
        data = source['geometries'][node['geometry']]['position']
        vertices = {(round(data[i], 5), round(-data[i+2], 5), round(data[i+1], 5)) for i in range(0, len(data), 3)}
        actual_vertices = {tuple(round(v, 5) for v in vertex.co) for vertex in obj.data.vertices}
        assert vertices == actual_vertices, obj.name
        geometry += 1
    if node.get('door') and node['door']['style'] in ('door', 'proposed'):
        before = obj['Open']
        obj['Open'] = 0
        obj.update_tag()
        bpy.context.view_layer.update()
        assert abs(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).rotation_euler.z) < .00001, obj.name
        obj['Open'] = before
        obj.update_tag()
        bpy.context.view_layer.update()
        doors += 1
assert bpy.context.scene.unit_settings.scale_length == 1
assert bpy.context.scene['source_model_sha256'] == source['provenance']['modelSha256']
assert all(image.packed_file for image in bpy.data.images if image.source == 'FILE')
for name in ('ALT - enclosed pantry ground floor', 'ALT - office guest bed'):
    col = bpy.data.collections[name]
    assert col.hide_render and len(col.all_objects) > 10
assert len([obj for obj in bpy.data.objects if obj.type == 'CAMERA']) == 6
assert len(expected) == len([obj for obj in bpy.data.objects if 'source_id' in obj])
print(json.dumps({'checkedTransforms': checked, 'geometryPreserved': geometry, 'hingedDoorControls': doors, 'sourceObjects': len(expected), 'packedTextures': True, 'hiddenAlternatives': True}))
