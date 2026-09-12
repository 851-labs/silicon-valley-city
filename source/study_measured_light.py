import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/google/google.blend'))
s=bpy.context.scene
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=20
sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN')
s.render.image_settings.file_format='PNG';s.render.resolution_percentage=60
for name,az,alt,sky,energy,color in [('light_a',192,35,.22,3.3,(1,.87,.72)),('light_b',195,40,.15,3.8,(1,.88,.72)),('light_c',185,40,.22,3.8,(1,.88,.76)),('light_d',195,50,.17,3.6,(1,.88,.75))]:
 a=math.radians(az);e=math.radians(alt);direction=Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))
 sun.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();sun.data.energy=energy;sun.data.color=color
 bg=s.world.node_tree.nodes['Background'];bg.inputs[0].default_value=(.72,.76,.82,1);bg.inputs[1].default_value=sky
 s.render.filepath=str(ROOT/'matching'/f'google_{name}.png');bpy.ops.render.render(write_still=True)
print('LIGHT_STUDIES_DONE',flush=True)
