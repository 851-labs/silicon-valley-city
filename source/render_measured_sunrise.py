"""Render the editable sunrise variation without changing the reference comparison frame."""
import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
from blender_runtime import configure_cycles
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'city_measured.blend'));s=bpy.context.scene
configure_cycles(s);s.frame_set(1);s.render.filepath=str(ROOT/'renders/city_measured_sunrise.png')
bpy.ops.render.render(write_still=True);print('MEASURED_SUNRISE_RENDERED',flush=True)
