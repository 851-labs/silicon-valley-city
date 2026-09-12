import bpy,os,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'city.blend'))
try:
 p=bpy.context.preferences.addons['cycles'].preferences
 p.compute_device_type='METAL';p.get_devices()
 if any(d.type=='METAL' for d in p.devices):
  for d in p.devices:d.use=d.type=='METAL'
  bpy.context.scene.cycles.device='GPU'
except (TypeError,RuntimeError):
 bpy.context.scene.cycles.device='CPU'
s=bpy.context.scene;s.render.resolution_x=3840;s.render.resolution_y=2160;s.render.resolution_percentage=100;s.cycles.samples=64
s.render.filepath=str(ROOT/'renders/city_reference.png')
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.shading.use_scene_world=True;area.spaces.active.shading.use_scene_lights=True
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'city.blend'),compress=True)
bpy.ops.render.render(write_still=True)
s.render.resolution_x=1600;s.render.resolution_y=900;s.cycles.samples=40
s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=94
for name,frame in [('early',1),('match',60),('late',120)]:
 s.frame_set(frame);s.render.filepath=str(ROOT/f'renders/morning_{name}.jpg');bpy.ops.render.render(write_still=True)
s.frame_set(60);s.render.image_settings.file_format='PNG'
s.camera=bpy.data.objects['03 • Title and eastern landmarks'];s.render.resolution_x=2000;s.render.resolution_y=1350;s.cycles.samples=48;s.render.filepath=str(ROOT/'renders/eastern_detail.png')
bpy.ops.render.render(write_still=True)
print('FINAL_RENDERS_READY',flush=True)
