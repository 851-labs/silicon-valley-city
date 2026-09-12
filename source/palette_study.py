import bpy,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'city.blend'));bpy.ops.object.make_local(type='ALL')
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s=bpy.context.scene;s.cycles.device='GPU';s.cycles.samples=32;s.render.resolution_x=1600;s.render.resolution_y=900
palette={'glass_blue':(.12,.205,.23),'glass_light':(.24,.30,.31),'cyan':(.035,.265,.37),'title_roof_red':(.95,.075,.034),'title_glass_a':(.19,.25,.24),'title_glass_b':(.24,.30,.28),'title_glass_c':(.14,.205,.20)}
for m in bpy.data.materials:
 name=m.name.split('.')[0]
 if name in palette and m.use_nodes:
  p=m.node_tree.nodes.get('Principled BSDF')
  if p:p.inputs['Base Color'].default_value=(*palette[name],1)
for name,exp,fill in [('warm_contrast',.65,.23),('warm_lift',.90,.30)]:
 s.view_settings.exposure=exp;s.world.node_tree.nodes['Background'].inputs[1].default_value=fill
 s.render.filepath=str(ROOT/'comparisons'/f'city_{name}.png');bpy.ops.render.render(write_still=True)
 print('PALETTE_STUDY',name,flush=True)
