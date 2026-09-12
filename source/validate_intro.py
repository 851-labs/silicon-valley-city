"""Validate the saved animated shot, camera fit, construction and portable resources."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
from reference_geometry import unproject
camera=json.loads((ROOT/'source/intro_camera.json').read_text());manifest=json.loads((ROOT/'animation/manifest.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'animation/intro.blend'));s=bpy.context.scene
assert s.frame_start==1 and s.frame_end==261
assert abs(s.render.fps/s.render.fps_base-24000/1001)<1e-5
assert not bpy.data.libraries,'Animation retains external libraries'
assert all(f.filepath=='<builtin>' or f.packed_file for f in bpy.data.fonts if f.users)
assert s.render.filepath.startswith('//')
controllers={o.name.removeprefix('BUILD • '):o for o in bpy.data.objects if o.name.startswith('BUILD • ')}
assert len(controllers)==13
cars=[o for o in s.objects if o.type=='EMPTY' and 'moving vehicle' in o.name]
assert len(cars)==49
camera_errors=[];heights={id:[] for id in controllers};points=[([400,300],0),([860,120],15),([1000,280],6)]
for f in [1,24,48,72,96,120,144,168,185,200,240,261]:
 s.frame_set(f);t=min((f-1)/(24000/1001),camera['hold_time']);scale=camera['start']['scale']+t*camera['per_second']['scale'];tx,ty=[x+t*v for x,v in zip(camera['start']['translation'],camera['per_second']['translation'])]
 for pixel,z in points:
  projected=world_to_camera_view(s,s.camera,unproject(pixel,z));expected=(scale*pixel[0]+tx,scale*pixel[1]+ty);observed=(projected.x*1280,(1-projected.y)*720);error=math.dist(expected,observed);camera_errors.append(error);assert error<.01,(f,expected,observed,error)
 for id,controller in controllers.items():heights[id].append(controller['construction_height'])
 for car in cars:assert all(math.isfinite(v) for v in car.location)
for item in manifest['title_buildings']:
 values=heights[item['letter']];assert abs(values[0])<1e-6 and values[-1]>=item['height'];assert all(b>=a-1e-6 for a,b in zip(values,values[1:])),item['letter']
s.frame_set(200);held=s.camera.matrix_world.copy();scale=s.camera.data.ortho_scale;s.frame_set(250);assert max(abs(held[i][j]-s.camera.matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6;assert abs(scale-s.camera.data.ortho_scale)<1e-6
report={'result':'PASS','scope':'Animation structure, saved resources and camera projection; not a visual fidelity approval.','frames':261,'fps':24000/1001,'duration_seconds':261/(24000/1001),'camera_max_projection_error_pixels_1280':max(camera_errors),'construction_controllers':len(controllers),'moving_vehicles':len(cars),'external_libraries':len(bpy.data.libraries),'resolution':[s.render.resolution_x,s.render.resolution_y]}
(ROOT/'animation/validation.json').write_text(json.dumps(report,indent=2)+'\n');print('INTRO_VALIDATED',json.dumps(report),flush=True)
