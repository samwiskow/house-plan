"""Export the local browser scene with explicit Blender material fallbacks."""
import bpy


def export_preview(path):
    scene=bpy.context.scene
    original=[]
    object_materials=[]
    for obj in scene.objects:
        if obj.type not in ['MESH','CURVE'] or not any(slot.link=='OBJECT' for slot in obj.material_slots):continue
        slots=[(slot.link,slot.material) for slot in obj.material_slots]
        object_materials.append((obj,obj.data,slots))
        obj.data=obj.data.copy()
        for slot,(_,material) in zip(obj.material_slots,slots):
            slot.link='DATA';slot.material=material
    for material in list(bpy.data.materials):
        if not material.use_nodes:continue
        shader=material.node_tree.nodes.get('Principled BSDF')
        if not shader:continue
        socket=shader.inputs['Base Color']
        if not socket.is_linked or socket.links[0].from_node.type=='TEX_IMAGE':continue
        source=socket.links[0].from_socket
        original.append((material,socket,source,socket.default_value[:]))
        color=material.diffuse_color[:]
        if not material.name.startswith('Coastal |'):
            ramps=[n for n in material.node_tree.nodes if n.type=='VALTORGB']
            color=ramps[0].color_ramp.evaluate(.5)[:] if ramps else socket.default_value[:]
        for link in list(socket.links):material.node_tree.links.remove(link)
        socket.default_value=color
    for obj in list(scene.objects):
        if obj.type in ['CAMERA','LIGHT'] or obj.hide_render or obj.parent is not None:continue
        key=(obj.get('level','g'),obj.get('part','interior'))
        name='VIEW | '+key[0]+' | '+key[1]
        parent=bpy.data.objects.get(name)
        if parent is None:
            parent=bpy.data.objects.new(name,None);scene.collection.objects.link(parent)
            parent['level']=key[0];parent['part']=key[1]
        world=obj.matrix_world.copy();obj.parent=parent;obj.matrix_world=world
    bpy.context.view_layer.update()
    try:
        bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_visible=True,use_renderable=True,export_apply=True,export_extras=True,export_cameras=False,export_lights=False,export_animations=False,export_image_format='AUTO')
    finally:
        for material,socket,source,color in original:
            socket.default_value=color;material.node_tree.links.new(source,socket)
        for obj,data,slots in object_materials:
            temporary=obj.data;obj.data=data
            for slot,(link,material) in zip(obj.material_slots,slots):
                slot.link=link
                if link=='OBJECT':slot.material=material
            if isinstance(temporary,bpy.types.Mesh):bpy.data.meshes.remove(temporary)
            else:bpy.data.curves.remove(temporary)
