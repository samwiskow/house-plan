"""Refresh the local GLB without rebuilding or rendering the native scene."""
import sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).parent/'coastal'))
from preview import export_preview
root=Path(__file__).resolve().parents[2]
output=root/'output/blender/coastal-house'
bpy.ops.wm.open_mainfile(filepath=str(output/'coastal-house.blend'))
export_preview(output/'coastal-house.glb')
