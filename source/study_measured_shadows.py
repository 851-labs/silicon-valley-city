import sys,runpy,math,bpy
from pathlib import Path
from mathutils import Vector
P=Path(__file__).parent;R=P.parent;sys.path.insert(0,str(P))
for id,script in [('ebay','build_ebay_matched.py'),('pets_com','build_western_matched.py')]:
 if id=='ebay':
  import build_ebay_matched as B;B.build()
 else:
  import build_western_matched as B;B.pets_com()
 s=bpy.context.scene;s.cycles.samples=24
 sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN')
 a,e=math.radians(138),math.radians(46);light=Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))
 sun.rotation_euler=(-light).to_track_quat('-Z','Y').to_euler();sun.data.energy=3.4
 s.render.filepath=str(R/'matching'/f'{id}_shadow_fit.png');bpy.ops.render.render(write_still=True)
 print('SHADOW_STUDY',id,flush=True)
