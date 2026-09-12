"""Build real meshes from measured orthographic reference coordinates.

Coordinates are observations in original_wide.webp (1280 x 720). A roof
contour is unprojected at its measured elevation, then extruded in 3D.
No photograph is used as a material or as rendered model geometry.
"""
import math,json,os
import bpy
from mathutils import Vector
import asset_core as A

CAL=json.load(open(os.path.join(A.ROOT,'source','camera_calibration.json')))
AZ=math.radians(CAL['azimuth']);EL=math.radians(CAL['elevation']);S=5.

def unproject(p,z=0):
 u=(p[0]-640)/S;v=((p[1]-460)/S+math.cos(EL)*z)/math.sin(EL)
 return Vector((math.cos(AZ)*u+math.sin(AZ)*v,math.sin(AZ)*u-math.cos(AZ)*v,z))

def set_color(material,color):
 p=material.node_tree.nodes.get('Principled BSDF');old=tuple(p.inputs['Base Color'].default_value)
 p.inputs['Base Color'].default_value=(*color,1);material.diffuse_color=(*color,1)
 if p.inputs['Base Color'].is_linked:
  for node in material.node_tree.nodes:
   if node.type=='VALTORGB':
    for stop in node.color_ramp.elements:
     stop.color=tuple(min(1,max(0,stop.color[i]*color[i]/max(.00001,old[i]))) for i in range(3))+(1,)
   elif node.type=='TEX_BRICK':
    for key in ('Color1','Color2','Mortar'):
     c=node.inputs[key].default_value[:]
     node.inputs[key].default_value=tuple(min(1,max(0,c[i]*color[i]/max(.00001,old[i]))) for i in range(3))+(1,)

class Reference:
 def __init__(self,anchor,crop):
  self.anchor=anchor;self.origin=unproject(anchor[:2],anchor[2]);self.origin.z=0
  self.crop=crop
  A.COL['measured_frame']='original_wide.webp'
  A.COL['reference_frame_anchor']=list(anchor)
  A.COL['reference_crop']=list(crop)
  A.COL['applied_reference_proportions']=[1.,1.,1.]
  A.COL['version']='fidelity-4-measured'

 def p(self,pixel,z):return unproject(pixel,z)-self.origin
 def facade_point(self,pixel,edge_a,edge_b,edge_height):
  """Intersect an observed pixel with a vertical facade below a measured edge.

  Choosing an arbitrary elevation can preserve the image position while floating
  the sign metres away from its wall. The edge fixes that otherwise hidden depth.
  """
  dx=edge_b[0]-edge_a[0]
  if abs(dx)<.001:raise ValueError('Facade edge is end-on to the camera')
  f=(pixel[0]-edge_a[0])/dx;edge_y=edge_a[1]+f*(edge_b[1]-edge_a[1])
  z=edge_height+(edge_y-pixel[1])/(S*math.cos(EL))
  return self.p(pixel,z)
 def plan(self,points,z):
  p=[tuple(self.p(q,z))[:2] for q in points]
  if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse()
  return p

 def prism(self,name,points,roof,z0=0,mat='white',batch=True):
  return A.polygon(name,self.plan(points,roof),z0,roof-z0,mat,batch)

 def segment(self,name,a,b,z,width,height,mat):
  p=self.p(a,z);q=self.p(b,z);v=q-p
  A.box(name,tuple((p+q)/2),(v.length,width,height),mat,math.atan2(v.y,v.x))

 def panels(self,quad,z,rows=None,cols=None,tilt=9,exclude=None):
  """PV field fitted to four observed roof corners, each module with its own UVs."""
  p=[self.p(q,z) for q in quad]
  if rows is None:rows=max(1,round((p[3]-p[0]).length/.95))
  if cols is None:cols=max(1,round((p[1]-p[0]).length/.78))
  A.part('Photovoltaic arrays • measured field boundaries')
  def point(u,v):return p[0].lerp(p[1],u).lerp(p[3].lerp(p[2],u),v)
  exclusions=[self.plan(poly,z) for poly in (exclude or [])]
  def inside(q,poly):
   c=False
   for a,b in zip(poly,poly[1:]+poly[:1]):
    if (a[1]>q.y)!=(b[1]>q.y) and q.x<(b[0]-a[0])*(q.y-a[1])/(b[1]-a[1])+a[0]:c=not c
   return c
  for j in range(rows):
   for i in range(cols):
    u0=(i+.055)/cols;u1=(i+.945)/cols;v0=(j+.075)/rows;v1=(j+.925)/rows
    q=[point(u0,v0),point(u1,v0),point(u1,v1),point(u0,v1)]
    if any(inside(sum(q,Vector())/4,poly) for poly in exclusions):continue
    rise=(q[3]-q[0]).length*math.sin(math.radians(tilt))
    for k in range(4):q[k].z+=.028+(rise if k>1 else 0)
    A.mesh('Measured tilted PV module',[tuple(v) for v in q],[(0,1,2,3)],'solar')
    for k in range(4):A.rod('PV module aluminium perimeter',q[k],q[(k+1)%4],.009,'frame',4)

 def solar_racks(self,quads,base,rise=1.50,cell_columns=12,cell_rows=8,material_name='rack_cells'):
  """Continuous inclined panel racks whose visible corners remain at source pixels.

  Corners 0 and 3 are the low edge; 1 and 2 are raised. Cell lines are UV
  geometry-independent, while perimeter, rear legs and braces are real meshes.
  """
  A.part('Continuous inclined photovoltaic racks')
  solar=A.MAT['solar'].copy();solar.name=material_name;A.MAT[solar.name]=solar
  for node in solar.node_tree.nodes:
   if node.type=='TEX_BRICK':
    node.inputs['Brick Width'].default_value=1/cell_columns;node.inputs['Row Height'].default_value=1/cell_rows
    node.inputs['Mortar Size'].default_value=.003
  for quad in quads:
   q=[self.p(pixel,base+(rise if i in (1,2) else 0)) for i,pixel in enumerate(quad)]
   ob=A.mesh('Continuous photovoltaic rack',[tuple(v) for v in q],[(0,3,2,1)],solar,batch=False)
   uv=ob.data.uv_layers.new(name='Individual silicon cells');coords=[(0,0),(0,1),(1,1),(1,0)]
   for loop in ob.data.loops:uv.data[loop.index].uv=coords[loop.vertex_index]
   for i in range(4):A.rod('Pale rack perimeter',q[i],q[(i+1)%4],.024,'frame',4)
   for f in [.15,.85]:
    front=q[0].lerp(q[3],f);back=q[1].lerp(q[2],f);foot=back.copy();foot.z=base-.05
    A.rod('Inclined rack underside rail',front,back,.035,'metal',6)
    A.rod('Rack rear supporting leg',foot,back,.035,'metal',6)
    A.rod('Rack triangular brace',front,foot,.025,'metal',6)

 def camera(self,multiplier=3):
  s=bpy.context.scene;A.flush()
  l,t,r,b=self.crop;target=unproject(((l+r)/2,(t+b)/2),0)-self.origin
  direction=Vector((math.sin(AZ)*math.cos(EL),-math.cos(AZ)*math.cos(EL),math.sin(EL)))
  cam=s.camera;cam.location=target+direction*500
  cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
  cam.data.type='ORTHO';cam.data.ortho_scale=max(r-l,b-t)/S;cam.data.clip_end=2000
  s.render.resolution_x=round((r-l)*multiplier);s.render.resolution_y=round((b-t)*multiplier)
  s.render.resolution_percentage=100;s.render.film_transparent=True
  # Initial direction fit from roadside shadows, checked with facade colour probes.
  # This is shared by all measured assets so their material comparisons agree.
  rig=json.load(open(os.path.join(A.ROOT,'source','lighting_measurements.json')))
  s['reference_light_version']=rig['version']
  sky=s.world.node_tree.nodes.get('Background')
  sky.inputs[0].default_value=(*rig['world_color'],1);sky.inputs[1].default_value=rig['world_strength']
  sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN')
  a,e=math.radians(rig['sun_azimuth']),math.radians(rig['sun_elevation'])
  light=Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))
  sun.rotation_euler=(-light).to_track_quat('-Z','Y').to_euler()
  sun.data.energy=rig['sun_energy'];sun.data.color=rig['sun_color'];sun.data.angle=rig['sun_angle']
  s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
  profiles=os.path.join(A.ROOT,'source','color_profiles.json')
  if os.path.exists(profiles):
   profile=json.load(open(profiles)).get(A.COL.get('asset_id'),{})
   for name,color in profile.get('materials',{}).items():
    if name in A.MAT:set_color(A.MAT[name],color)
  bpy.context.view_layer.update()
  from bpy_extras.object_utils import world_to_camera_view
  errors=[]
  for pixel,z in [((l,t),0),((r,b),0),(((l+r)/2,(t+b)/2),7),((l+12,t+13),23)]:
   q=world_to_camera_view(s,cam,self.p(pixel,z))
   reconstructed=(l+q.x*(r-l),t+(1-q.y)*(b-t))
   errors.append(math.hypot(reconstructed[0]-pixel[0],reconstructed[1]-pixel[1]))
  assert max(errors)<.002,('Reference camera projection failed',errors)
  s['projection_check_max_error_px']=max(errors)
  s['comparison_method']='Identical source crop and calibrated projection, without image registration after rendering.'
  return s

def facade(points,z,h,glass='glass_blue',solid='cream',style='ribbon',floors=3,band=.22,bay=2.0):
 """Facade strips on an arbitrary measured footprint; preserves concave corners."""
 A.polygon('Measured structural envelope',points,z,h,glass)
 for a,b in zip(points,points[1:]+points[:1]):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length
  if L<.04:continue
  t=v/L;n=Vector((t.y,-t.x));mid=(a+b)/2+n*.035;angle=math.atan2(t.y,t.x)
  for k in range(floors+1):
   A.box('Horizontal floor fascia',(mid.x,mid.y,z+k*h/floors),(L+.025,.12,band),solid,angle)
  for j in range(round(L/bay)+1):
   p=a+t*j*L/max(1,round(L/bay))+n*.10
   A.box('Vertical window division',(p.x,p.y,z+h/2),(.045,.17,h),solid,angle)

def vector_art(name,data,origin,u,v,depth,normal):
 """Extrude triangulated artwork along an explicit 3D plane, preserving holes."""
 origin,u,v,normal=map(Vector,(origin,u,v,normal))
 for g in data:
  n=len(g['vertices']);vs=[tuple(origin+u*x+v*y+normal*z) for z in (0,depth) for x,y in g['vertices']];fs=[]
  for f in g['faces']:fs.extend([tuple(reversed(f)),tuple(j+n for j in f)])
  off=0
  for count in g['rings']:
   fs.extend((off+j,off+(j+1)%count,off+(j+1)%count+n,off+j+n) for j in range(count));off+=count
  A.mesh(name,vs,fs,g['material'])
