"""Compare PV surface response at the reference and sunrise sun angles."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/ebay/ebay.blend'));s=bpy.context.scene
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=24;s.render.resolution_percentage=60
sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN')
m=bpy.data.materials['solar'];shader=m.node_tree.nodes['Principled BSDF'];brick=next(n for n in m.node_tree.nodes if n.type=='TEX_BRICK');original={key:tuple(brick.inputs[key].default_value) for key in ['Color1','Color2','Mortar']}
for name,rough,metal,spec,colours in [('existing',.30,.32,.50,None),('rougher',.58,.02,.22,None),('diffuse',.65,0,.12,[(.12,.14,.18,1),(.17,.20,.25,1),(.55,.55,.54,1)])]:
 shader.inputs['Roughness'].default_value=rough;shader.inputs['Metallic'].default_value=metal;shader.inputs['Specular IOR Level'].default_value=spec
 for key,value in zip(['Color1','Color2','Mortar'],colours if colours else original.values()):brick.inputs[key].default_value=value
 for elev in [46,20]:
  a,e=math.radians(138),math.radians(elev);v=Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)));sun.rotation_euler=(-v).to_track_quat('-Z','Y').to_euler();sun.data.color=(1,.95,.88) if elev==46 else (1,.76,.56)
  s.render.filepath=str(ROOT/'matching'/f'pv_{name}_{elev}.png');bpy.ops.render.render(write_still=True)
print('PV_RESPONSE_STUDY_DONE',flush=True)
