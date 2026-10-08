"""Create an editable Blender study from the measured L-house scene."""
import argparse
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--render', nargs='*', default=[])
parser.add_argument('--samples', type=int, default=48)
parser.add_argument('--width', type=int, default=1200)
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
source = json.loads(args.source.read_text())
args.output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'
C = Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
CI = C.inverted()

def point(v):
    return (v[0], -v[2], v[1])

def collection(name, parent=None):
    col = bpy.data.collections.new(name)
    (parent or scene.collection).children.link(col)
    return col

images = {}
for key, data in source['textures'].items():
    image = bpy.data.images.load(str(args.source.parent / data['path']))
    image.colorspace_settings.name = 'sRGB' if data['color'] else 'Non-Color'
    image.pack()
    images[key] = image

materials = {}
for key, data in source['materials'].items():
    material = bpy.data.materials.new(data['name'])
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*data['color'], 1)
    shader.inputs['Roughness'].default_value = data['roughness']
    shader.inputs['Metallic'].default_value = data['metalness']
    if data['map']:
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = images[data['map']]
        texture.location = (-500, 160)
        links.new(texture.outputs['Color'], shader.inputs['Base Color'])
    if data['normalMap']:
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = images[data['normalMap']]
        texture.location = (-500, -140)
        normal = nodes.new('ShaderNodeNormalMap')
        normal.inputs['Strength'].default_value = data['normalScale'][0]
        normal.location = (-240, -140)
        links.new(texture.outputs['Color'], normal.inputs['Color'])
        links.new(normal.outputs['Normal'], shader.inputs['Normal'])
    if data['name'] in ('glass', 'Privacy glass'):
        shader.inputs['Base Color'].default_value = (.94, .98, .97, 1)
        shader.inputs['Transmission Weight'].default_value = 1
        shader.inputs['Roughness'].default_value = .035 if data['name'] == 'glass' else .45
        shader.inputs['IOR'].default_value = 1.45
    if data['name'] == 'oatmeal':
        shader.inputs['Sheen Weight'].default_value = .3
        shader.inputs['Sheen Roughness'].default_value = .8
    material.diffuse_color = (*data['color'], 1)
    materials[key] = material
ivory = next(m for m in materials.values() if m.name == 'ivory')

meshes = {}
for key, data in source['geometries'].items():
    positions = data['position']
    vertices = [point(positions[i:i+3]) for i in range(0, len(positions), 3)]
    indices = data['index'] or list(range(len(vertices)))
    mesh = bpy.data.meshes.new(data['type'])
    mesh.from_pydata(vertices, [], [indices[i:i+3] for i in range(0, len(indices), 3)])
    if data['uv']:
        uv = mesh.uv_layers.new(name='Measured UV')
        for loop in mesh.loops:
            uv.data[loop.index].uv = data['uv'][loop.vertex_index*2:loop.vertex_index*2+2]
    if data['type'] == 'BoxGeometry':
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=.000001)
        bm.to_mesh(mesh)
        bm.free()
    elif data.get('normal') and hasattr(mesh, 'normals_split_custom_set_from_vertices'):
        for polygon in mesh.polygons:
            polygon.use_smooth = True
        normals = data['normal']
        mesh.normals_split_custom_set_from_vertices([point(normals[i:i+3]) for i in range(0, len(normals), 3)])
    mesh.update()
    meshes[key] = mesh

floor_names = {'g': 'House - ground - open pantry', 'u': 'House - first floor', 'a': 'Garage - ground', 'o': 'Garage - office - work'}
records, objects, floor_cols = [], {}, {}

def import_node(node, col, parent=None, split_floors=True):
    if split_floors and node['name'] in floor_names:
        col = collection(floor_names[node['name']], col)
        floor_cols[node['name']] = col
    if node.get('geometry'):
        mesh = meshes[node['geometry']]
        material = materials[node['material']]
        if not mesh.materials:
            mesh.materials.append(material)
        name = (parent.name + ' / ' + material.name) if parent else material.name
        obj = bpy.data.objects.new(name, mesh)
        data = source['geometries'][node['geometry']]
        if data['type'] == 'BoxGeometry' and material.name not in ('glass', 'Privacy glass', 'grass', 'soil', 'leaf'):
            lengths = [max(v.co[i] for v in mesh.vertices)-min(v.co[i] for v in mesh.vertices) for i in range(3)]
            bevel = obj.modifiers.new('Soft physical edges', 'BEVEL')
            bevel.width = min(.001 if parent and parent.get('floor_id') else .012, min(lengths) / 8)
            bevel.segments = 2
            bevel.limit_method = 'ANGLE'
        obj['source_geometry'] = data['type']
        obj['cast_shadow'] = node['castShadow']
    else:
        obj = bpy.data.objects.new(node['name'], None)
        obj.empty_display_type = 'PLAIN_AXES'
        obj.empty_display_size = .12
    col.objects.link(obj)
    obj.parent = parent
    a = node['matrix']
    obj.matrix_local = C @ Matrix([a[i::4] for i in range(4)]) @ CI
    obj['source_id'] = node['id']
    if node['name'] in floor_names:
        obj['floor_id'] = node['name']
    if node.get('room'):
        obj['room'] = node['room']
    if node.get('door'):
        door = node['door']
        obj['door_id'] = door['id']
        obj['door_style'] = door['style']
        obj['Open'] = door['progress']
        obj.id_properties_ui('Open').update(min=0, max=1, description='0 closed, 1 open')
        if door['style'] in ('door', 'proposed'):
            curve = obj.driver_add('rotation_euler', 2)
            variable = curve.driver.variables.new()
            variable.name = 'opening'
            variable.targets[0].id = obj
            variable.targets[0].data_path = '["Open"]'
            sign = -door['side'] if door['axis'] == 'h' else door['side']
            curve.driver.expression = f'{sign * math.pi / 2} * opening'
    objects[node['id']] = obj
    records.append((node, obj, parent))
    for child in node['children']:
        import_node(child, col, obj, split_floors)
    return obj

for node in source['normal']:
    import_node(node, collection(node['name']))
alternate_cols = []
for name, nodes in [('ALT - enclosed pantry ground floor', source['enclosed']), ('ALT - office guest bed', source['guest'])]:
    col = collection(name)
    for node in nodes:
        import_node(node, col, split_floors=False)
    alternate_cols.append(col)
bpy.context.view_layer.update()

def inside(x, y, polygon):
    result = False
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if (a[1] > y) != (b[1] > y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            result = not result
    return result

paving_layer = 0
for node, obj, parent in records:
    if obj.type != 'MESH' or not parent or parent.name != 'Site':
        continue
    if obj.data.materials[0].name == 'floor':
        obj.location.z += paving_layer * .0003
        paving_layer += 1
    if obj.data.materials[0].name == 'grass' and obj.dimensions.x > 100:
        obj.scale.x *= 20
        obj.scale.y *= 20
bpy.context.view_layer.update()

roof_objects = [obj for node, obj, parent in records if obj.type == 'MESH' and parent and parent.name == 'Roofs' and obj.data.materials[0].name == 'roof']
closed_gables = 0
for node, obj, parent in records:
    if obj.type != 'MESH' or not parent or parent.name != 'Roofs' or obj.data.materials[0].name != 'timber' or len(obj.data.vertices) != 3:
        continue
    vertices = sorted([obj.matrix_world @ v.co for v in obj.data.vertices], key=lambda v: v.z)
    left, right, apex = vertices
    base = math.floor(left.z / 3) * 3 + 2.9
    tops = []
    for corner in (left, right):
        hits = []
        origin = Vector((corner.x, corner.y, 20))
        for roof in roof_objects:
            inverse = roof.matrix_world.inverted()
            hit, location, normal, index = roof.ray_cast(inverse @ origin, inverse.to_3x3() @ Vector((0, 0, -1)))
            if hit:
                height = (roof.matrix_world @ location).z
                if height <= apex.z + .001:
                    hits.append(height)
        if not hits:
            raise ValueError('Gable edge does not meet roof')
        tops.append(max(hits))
    points = [(left.x, left.y, base), (right.x, right.y, base), (right.x, right.y, tops[1]), tuple(apex), (left.x, left.y, tops[0])]
    mesh = bpy.data.meshes.new('Closed gable cladding')
    mesh.from_pydata(points, [], [(0, 1, 2, 3, 4)])
    mesh.materials.append(obj.data.materials[0])
    uv = mesh.uv_layers.new(name='Measured UV')
    axis = 0 if abs(left.x-right.x) > .1 else 1
    for loop in mesh.loops:
        v = mesh.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = (v[axis]/.6, v.z/2.4)
    obj.data = mesh
    obj.matrix_world = Matrix.Identity(4)
    obj['study_detail'] = 'Gable cladding meets the existing roof slope; room geometry unchanged.'
    closed_gables += 1

painted_faces = 0
for node, obj, parent in records:
    if obj.type != 'MESH' or not parent or parent.get('floor_id') not in floor_names or obj.data.materials[0].name not in ('stone', 'timber'):
        continue
    rooms = [r['p'] for r in source['model']['default']['rooms'] if r['floor'] == parent['floor_id']]
    obj.data.materials.append(ivory)
    for polygon in obj.data.polygons:
        sample = obj.matrix_world @ polygon.center + (obj.matrix_world.to_3x3() @ polygon.normal) * .035
        if any(inside(sample.x, -sample.y, room) for room in rooms):
            polygon.material_index = 1
            painted_faces += 1

for col in alternate_cols:
    col.hide_render = True
    col.hide_viewport = True
bpy.context.view_layer.update()

lighting = collection('Studio - daylight and cameras')
world = bpy.data.worlds.new('Daylight sky')
world.use_nodes = True
scene.world = world
nodes, links = world.node_tree.nodes, world.node_tree.links
sky = nodes.new('ShaderNodeTexSky')
sky.sky_type = 'MULTIPLE_SCATTERING'
sky.sun_elevation = math.radians(35)
sky.sun_rotation = math.radians(140)
sky.sun_disc = False
links.new(sky.outputs['Color'], nodes.get('Background').inputs['Color'])
nodes.get('Background').inputs['Strength'].default_value = .07
sun = bpy.data.lights.new('Afternoon sun', 'SUN')
sun.energy = 2.5
sun.color = (1, .88, .72)
sun.angle = math.radians(4)
sun_obj = bpy.data.objects.new('Afternoon sun', sun)
lighting.objects.link(sun_obj)
sun_obj.location = (-18, 28, 35)
sun_obj.rotation_euler = (Vector((10, -7, 0))-sun_obj.location).to_track_quat('-Z', 'Y').to_euler()

for name, position, power, size in [
    ('Living', (3.5, 2.55, 3), 180, 2),
    ('Dining', (3.5, 2.55, 6.6), 140, 1.5),
    ('Kitchen', (8.8, 2.55, 7.3), 160, 1.6),
    ('Parents', (3.4, 5.55, 2.3), 140, 1.5),
    ('Office', (23, 5.55, 17), 180, 2),
]:
    light = bpy.data.lights.new(name + ' soft ceiling light', 'AREA')
    light.energy, light.size, light.color = power, size, (1, .92, .8)
    obj = bpy.data.objects.new(light.name, light)
    lighting.objects.link(obj)
    obj.location = point(position)

camera_specs = {
    'arrival': ([-13, 12, 39], [12, 2.8, 10], 30),
    'garden': ([14, 7, -15], [9, 3, 6], 28),
    'living': ([3.35, 1.65, 8.75], [3.3, 1.3, 1], 22),
    'kitchen': ([10.25, 1.65, 8.85], [8.1, 1.25, 5.7], 22),
    'parents': ([5.6, 4.65, 3.9], [2.8, 4.2, 1.3], 24),
    'office': ([21.95, 4.65, 19.75], [24.2, 4.15, 15.8], 23),
}
cameras = {}
for name, (position, target, lens) in camera_specs.items():
    camera_data = bpy.data.cameras.new(name.title())
    camera_data.lens = lens
    camera_data.clip_start = .03
    camera_data.clip_end = 400
    obj = bpy.data.objects.new(name.title(), camera_data)
    lighting.objects.link(obj)
    obj.location = point(position)
    obj.rotation_euler = (Vector(point(target))-obj.location).to_track_quat('-Z', 'Y').to_euler()
    cameras[name] = obj
scene.camera = cameras['arrival']
scene.render.engine = 'CYCLES'
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 10
scene.cycles.transmission_bounces = 8
prefs = bpy.context.preferences.addons['cycles'].preferences
try:
    prefs.compute_device_type = 'METAL'
    prefs.get_devices()
    for device in prefs.devices:
        device.use = device.type == 'METAL'
    if any(d.type == 'METAL' for d in prefs.devices):
        scene.cycles.device = 'GPU'
except TypeError:
    pass
scene.render.resolution_x = args.width
scene.render.resolution_y = round(args.width * 2 / 3)
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.view_settings.exposure = .4
scene['source_model_sha256'] = source['provenance']['modelSha256']
scene['design_revision'] = 'L01 Blender study 01'
scene['units_note'] = 'Metres; model positions and approved footprints are retained.'
notes = bpy.data.texts.new('READ ME - L-house study')
notes.write('L01 Blender study\n\nMeasured geometry comes from the corrected browser model.\nRoom layouts and furniture footprints are unchanged.\nStone and timber remain outside; room-facing wall surfaces are ivory plaster.\n\nCollections separate the building, floors, ceilings, roof and site.\nTo view enclosed pantry: hide House - ground - open pantry, then enable ALT - enclosed pantry ground floor.\nTo view guest bed: hide Garage - office - work, then enable ALT - office guest bed.\nHinged-door empty objects have an Open custom property: 0 closed, 1 open.\nOther door types retain their measured open pose and named component objects.\n\nCameras: Arrival, Garden, Living, Kitchen, Parents, Office.\nRoof gable cladding is closed to its existing roof slope.\nRender: Cycles with daylight and soft ceiling lights; these are proposed finishes, not specifications.\nBrowser export: default open pantry and work office; static review model.\nRoof form, windows and 40 x 65 m site remain design assumptions.\n')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
            area.spaces.active.clip_end = 500
bpy.ops.wm.save_as_mainfile(filepath=str(args.output / 'l-house.blend'), compress=True)
bpy.ops.export_scene.gltf(filepath=str(args.output / 'l-house.glb'), export_format='GLB', use_visible=True, use_renderable=True, export_apply=True, export_extras=True, export_cameras=False, export_lights=False, export_animations=False)
report = {'source': source['provenance'], 'objects': len(bpy.data.objects), 'meshes': len(bpy.data.meshes), 'materials': len(materials), 'paintedInteriorFaces': painted_faces, 'closedGables': closed_gables, 'renderer': scene.render.engine, 'device': scene.cycles.device, 'cameras': camera_specs}
(args.output / 'build-report.json').write_text(json.dumps(report, indent=2))
for name in args.render:
    scene.camera = cameras[name]
    scene.view_settings.exposure = .3 if name in ('living', 'kitchen', 'parents', 'office') else .4
    scene.render.filepath = str(args.output / (name + '.png'))
    bpy.ops.render.render(write_still=True)
print('L_HOUSE_BUILD', json.dumps(report))
