"""Fit material response at documented source probes; this is not a whole-asset fidelity score."""
import bpy,sys,json,math,statistics,array
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from reference_geometry import set_color
from blender_runtime import configure_cycles
R=Path(__file__).resolve().parents[1];id=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'youtube'
D=json.load(open(R/'source/photometric_probes.json'))[id]
bpy.ops.wm.open_mainfile(filepath=str(R/'assets'/id/(id+'.blend')));s=bpy.context.scene
configure_cycles(s);s.cycles.samples=40;s.render.resolution_percentage=100
col=next(c for c in bpy.data.collections if c.name.startswith('ASSET'));l,t,r,b=col['reference_crop']
# Reject probe points that land on a different material in the actual scene.
from reference_geometry import unproject
from mathutils import Vector
origin=unproject(col['reference_frame_anchor'][:2],col['reference_frame_anchor'][2]);origin.z=0
direction=s.camera.matrix_world.to_quaternion()@Vector((0,0,-1));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN');toward_sun=sun.matrix_world.to_quaternion()@Vector((0,0,1))
probe_errors=[]
for material,probes in D.items():
 for probe in probes:
  x,y=probe['pixel'];p=unproject((x+.5,y+.5),0)-origin
  hit,loc,norm,face,obj,mat=s.ray_cast(deps,p-direction*500,direction)
  mesh=obj.evaluated_get(deps).data if hit else None
  actual=mesh.materials[mesh.polygons[face].material_index].name if hit else 'background'
  if hit and 'surface_normal' in probe and norm.dot(Vector(probe['surface_normal']))<.95:
   probe_errors.append(('PROBE_SURFACE_MISMATCH',id,probe['pixel'],list(norm)))
  if hit and 'sun_visible' in probe:
   blocked,_,_,_,blocker,_=s.ray_cast(deps,loc+toward_sun*.03,toward_sun)
   assert (not blocked)==probe['sun_visible'],('PROBE_LIGHTING_MISMATCH',id,probe['pixel'],blocker.name if blocked else 'direct sun')
  if actual!=material:
   candidates=[]
   for dy in range(-3,4):
    for dx in range(-3,4):
     p=unproject((x+dx+.5,y+dy+.5),0)-origin
     hit,loc,norm,face,obj,mat=s.ray_cast(deps,p-direction*500,direction)
     if hit:
      mesh=obj.evaluated_get(deps).data
      if mesh.materials[mesh.polygons[face].material_index].name==material:candidates.append([x+dx,y+dy])
   print('NEARBY_VALID_PROBES',material,candidates,flush=True)
  if actual!=material:probe_errors.append(('PROBE_MATERIAL_MISMATCH',id,probe['pixel'],material,actual))
assert not probe_errors,probe_errors
W=s.render.resolution_x;H=s.render.resolution_y
sx=W/(r-l);sy=H/(b-t)
def linear(v):v=v/255;return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
def srgb(v):return round(255*(12.92*v if v<=.0031308 else 1.055*max(v,0)**(1/2.4)-.055),2)
report={'asset':id,'method':'RGB response at fixed, documented reference image probes. Does not measure geometry or whole-image similarity.','passes':[]}
for iteration in range(3):
 s.render.image_settings.file_format='OPEN_EXR';s.render.image_settings.color_mode='RGBA';s.render.image_settings.color_depth='32';s.render.filepath=str(R/'matching'/f'{id}_calibration.exr');bpy.ops.render.render(write_still=True)
 im=bpy.data.images.load(s.render.filepath,check_existing=False);px=array.array('f',[0])*len(im.pixels);im.pixels.foreach_get(px)
 assert len(px)==W*H*4,(len(px),W,H)
 measured={};updates={}
 for material,probes in D.items():
  ratios=[];rows=[]
  for probe in probes:
   x,y=probe['pixel'];xx=int((x-l+.5)*sx);yy=int((y-t+.5)*sy);samples=[]
   for j in range(max(0,yy-round(sy)),min(H,yy+round(sy)+1)):
    for i in range(max(0,xx-round(sx)),min(W,xx+round(sx)+1)):
     k=((H-j-1)*W+i)*4
     if px[k+3]>.99:samples.append(px[k:k+3])
   assert samples,(material,probe)
   response=[statistics.median(a[c] for a in samples) for c in range(3)];target=[linear(c) for c in probe['source_rgb']]
   ratios.append([target[c]/max(.0001,response[c]) for c in range(3)])
   rows.append({'pixel':probe['pixel'],'target_rgb':probe['source_rgb'],'render_rgb':[srgb(c) for c in response]})
  m=bpy.data.materials[material];base=tuple(m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value)[:3]
  new=[min(1,max(.001,base[c]*statistics.mean(q[c] for q in ratios)**.90)) for c in range(3)]
  measured[material]={'base_color':base,'probes':rows};updates[material]=new
 report['passes'].append(measured);bpy.data.images.remove(im)
 print('COLOUR_FIT_PASS',iteration,json.dumps(measured),flush=True)
 if iteration<2:
  for name,color in updates.items():set_color(bpy.data.materials[name],color)
profile=R/'source/color_profiles.json';profiles=json.load(open(profile)) if profile.exists() else {}
profiles[id]={'materials':{name:list(bpy.data.materials[name].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value)[:3] for name in D},'probes':'source/photometric_probes.json','report':f'matching/{id}_color_fit.json'}
profile.write_text(json.dumps(profiles,indent=2));(R/'matching'/f'{id}_color_fit.json').write_text(json.dumps(report,indent=2))
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.image_settings.color_depth='8';s.render.filepath=str(R/'assets'/id/'preview.png')
bpy.data.images['Render Result'].save_render(s.render.filepath,scene=s)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'assets'/id/(id+'.blend')),compress=True)
print('COLOR_CALIBRATION_SAVED',id,flush=True)
