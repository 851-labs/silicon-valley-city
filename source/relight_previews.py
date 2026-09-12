"""Apply the final measured daylight exposure consistently to all asset previews."""
import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
palette={'glass_blue':(.12,.205,.23),'glass_light':(.24,.30,.31),'cyan':(.035,.265,.37),'title_roof_red':(.95,.10,.064),'title_glass_a':(.19,.25,.24),'title_glass_b':(.24,.30,.28),'title_glass_c':(.14,.205,.20)}
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
for f in sorted((ROOT/'assets').glob('*/*.blend')):
 bpy.ops.wm.open_mainfile(filepath=str(f));s=bpy.context.scene
 for m in bpy.data.materials:
  name=m.name.split('.')[0]
  if name in palette and m.use_nodes:
   node=m.node_tree.nodes.get('Principled BSDF')
   if node:node.inputs['Base Color'].default_value=(*palette[name],1)
 s.world.node_tree.nodes['Background'].inputs[1].default_value=.38
 s.view_settings.exposure=.70
 for l in bpy.data.lights:
  if l.type=='SUN':l.color=(1,.87,.70);l.energy=3.3
 s.cycles.device='GPU';s.cycles.samples=40;s.render.filepath=str(f.parent/'preview.png')
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(f),compress=True)
 bpy.ops.render.render(write_still=True)
 print('RELIT',f.stem,flush=True)
