import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'assets/youtube/youtube.blend'))
s=bpy.context.scene;p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=20;s.render.resolution_percentage=70
for name,view,look,exposure in [('standard_0','Standard','None',0),('standard_m05','Standard','None',-.5),('agx_16','AgX','AgX - Medium High Contrast',1.6),('agx_none','AgX','AgX - Base Contrast',1.0)]:
 s.view_settings.view_transform=view;s.view_settings.look=look;s.view_settings.exposure=exposure;s.render.filepath=str(R/'matching'/f'youtube_{name}.png');bpy.ops.render.render(write_still=True)
print('VIEW_TRANSFORM_STUDY_DONE',flush=True)
