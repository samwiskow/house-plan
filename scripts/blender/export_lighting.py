"""Export the study's Cycles sky as a linear HDR browser environment."""
import math
import sys
from pathlib import Path

import bpy

root = Path(sys.argv[sys.argv.index('--') + 1]).resolve()
bpy.ops.wm.open_mainfile(filepath=str(root / 'output/blender/l-house/l-house.blend'))
scene = bpy.context.scene
for obj in scene.objects:
    obj.hide_render = True
camera = scene.camera
camera.hide_render = False
camera.data.type = 'PANO'
camera.data.panorama_type = 'EQUIRECTANGULAR'
camera.rotation_euler = (math.pi / 2, 0, 0)
scene.render.resolution_x = 1024
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.cycles.samples = 16
scene.render.image_settings.file_format = 'HDR'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0
scene.render.filepath = str(root / 'output/blender/l-house/daylight.hdr')
bpy.ops.render.render(write_still=True)
