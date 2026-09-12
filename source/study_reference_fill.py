import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'assets/youtube/youtube.blend'))
s=bpy.context.scene;p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=24
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
bg=s.world.node_tree.nodes['Background'];bg.inputs[1].default_value=.55
sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN');sun.data.energy=3.8;sun.data.color=(1,.95,.88)
for name,c in {'youtube_roof':(1,1,1),'youtube_glass':(.05,.040,.035),'youtube_plaza':(.10,.185,.225),'youtube_slab':(.37,.35,.325)}.items():
 bpy.data.materials[name].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*c,1)
s.render.filepath=str(R/'matching/youtube_fill_055.png');bpy.ops.render.render(write_still=True)
print('FILL_STUDY_DONE')
