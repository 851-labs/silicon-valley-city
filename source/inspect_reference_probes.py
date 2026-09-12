"""Inspect material and sun visibility at a grid of source-camera coordinates."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from reference_geometry import unproject
R=Path(__file__).resolve().parents[1];args=sys.argv[sys.argv.index('--')+1:];asset,material=args[:2];x0,y0,x1,y1,step=map(int,args[2:]);bpy.ops.wm.open_mainfile(filepath=str(R/'assets'/asset/(asset+'.blend')));s=bpy.context.scene;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();col=next(c for c in bpy.data.collections if c.name.startswith('ASSET'));a=col['reference_frame_anchor'];origin=unproject(a[:2],a[2]);origin.z=0;view=s.camera.matrix_world.to_quaternion()@Vector((0,0,-1));sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN');light=sun.matrix_world.to_quaternion()@Vector((0,0,1));out=[]
for y in range(y0,y1+1,step):
 for x in range(x0,x1+1,step):
  p=unproject((x+.5,y+.5),0)-origin;hit,loc,norm,face,obj,_=s.ray_cast(deps,p-view*500,view)
  if not hit:continue
  m=obj.data.materials[obj.data.polygons[face].material_index].name
  if m!=material:continue
  blocked,_,_,_,blocker,_=s.ray_cast(deps,loc+light*.03,light)
  out.append({'pixel':[x,y],'sun_visible':not blocked,'blocker':blocker.name if blocked else None,'surface_z':round(loc.z,3)})
print('REFERENCE_PROBES',json.dumps(out),flush=True)
