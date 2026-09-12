import os,sys,runpy,bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.argv=['study_city_v3.py','--no-render']
runpy.run_path(str(ROOT/'source/assemble_city.py'),run_name='__main__')
s=bpy.context.scene;s.render.resolution_x=1600;s.render.resolution_y=900;s.cycles.samples=32
for name,exp in [('exposure_045',.45),('exposure_070',.70),('exposure_095',.95)]:
 s.view_settings.exposure=exp;s.render.filepath=str(ROOT/'comparisons'/f'city_{name}.png');bpy.ops.render.render(write_still=True)
 print('EXPOSURE_STUDY',name,flush=True)
