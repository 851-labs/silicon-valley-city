"""Measured EnergyPod corner tower, sliced roof shell and red helicopter roof."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,facade
from build_ebay_matched import inset
from build_landmarks import helicopter
from mathutils import Vector
P=Path(__file__).parent

def rounded_quad(points,cut=.15):
 out=[]
 for i,b in enumerate(points):
  a=Vector(points[i-1]);b=Vector(b);c=Vector(points[(i+1)%len(points)]);start=b.lerp(a,cut);end=b.lerp(c,cut)
  for j in range(13):
   t=j/12;q=start*(1-t)**2+b*2*t*(1-t)+end*t*t;out.append(tuple(q))
 return out

def build():
 D=json.load(open(P/'energy_pod_measurements.json'));A.reset('energy_pod','EnergyPod • measured rounded tower, pylons and sliced roof shell',['Original wide frame','YU11']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('pod_frame',(.53,.54,.50),.84),('pod_glass',(.08,.20,.19),.43),('pod_pale',(.76,.72,.64),.85),('pod_shell',(.64,.66,.63),.69),('pod_cowl_dark',(.024,.031,.032),.79),('pod_mesh_glass',(.11,.21,.25),.36),('pad_red',(.94,.17,.085),.88)]:A.material(n,c,r)
 H=D['main_height'];p=R.plan(D['main_roof'],H);wall=rounded_quad(inset(p,.45),.18);A.part('Rounded tower curtain wall');A.polygon('Continuous curved green glazing',wall,0,H-.15,'pod_glass')
 for k in range(15):A.curve('Curved horizontal floor fascia',[(x,y,.75+k*1.29) for x,y in wall],.070,'pod_frame',True)
 for i,(a,b) in enumerate(zip(wall,wall[1:]+wall[:1])):
  a,b=Vector(a),Vector(b);v=b-a;n=Vector((v.y,-v.x)).normalized();N=max(1,round(v.length/.75))
  for j in range(N):
   q=a.lerp(b,j/N)+n*.04;A.rod('Rounded facade slender vertical',(q.x,q.y,0),(q.x,q.y,H),.027,'pod_frame',5)
 A.part('Pale roof around the pod');A.polygon('Broad pale roof platform',rounded_quad(p,.12),H-.15,.32,'pod_pale')
 for index,pixels in enumerate(D['pylon_roofs']):
  H=D['pylon_height'] if index<3 else D['main_height'];p=R.plan(pixels,H);A.part('Projecting structural corner pylon');A.polygon('Pale square corner shaft',p,0,H-.45,'pod_frame');A.polygon('Green tiled pylon roof',p,H-.45,.50,'pod_glass' if index<3 else 'pod_pale')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));ang=math.atan2(v.y,v.x)
   from reference_geometry import AZ
   sx=v.x*math.cos(AZ)+v.y*math.sin(AZ);sy=v.x*math.sin(AZ)-v.y*math.cos(AZ);glazed=sx*sy>0
   if glazed:
    q=(a+b)/2+n*.025;A.box('Broad green pylon window face',(q.x,q.y,(H-.75)/2),(L-.19,.035,H-.75),'pod_glass',ang)
    for k in range(14):A.box('Pylon glazing floor rail',(q.x,q.y,.85+k*1.39),(L-.13,.065,.14),'pod_frame',ang)
   for k in range(14 if not glazed else 0):
    for f in [.28,.72]:
     q=a.lerp(b,f)+n*.018;A.box('Small punched pylon window',(q.x,q.y,.9+k*1.39),(.27,.04,.46),'pod_cowl_dark',ang)
  # Orthogonal fine grid on each small cap, following its measured skewed plane.
  q=[R.p(px,H+.06) for px in pixels]
  for i in range(11 if index<3 else 0):
   t=i/10;A.rod('Cap transverse tiled seam',q[0].lerp(q[1],t),q[3].lerp(q[2],t),.013,'pod_frame',4);A.rod('Cap longitudinal tiled seam',q[0].lerp(q[3],t),q[1].lerp(q[2],t),.013,'pod_frame',4)
 H=D['helipad_height'];p=R.plan(D['helipad_roof'],H);A.part('Rear red helipad office');facade(inset(p,.14),0,H-.15,'pod_glass','pod_frame',floors=14,band=.46,bay=.85);A.polygon('White helicopter roof slab',p,H-.15,.27,'pod_pale');A.polygon('Measured coral-red landing pad',inset(p,.43),H+.12,.035,'pad_red')
 # Landing H consists of three flat white bars in the observed roof plane.
 z=H+.18
 for quad in [[[978,487],[983,484],[1009,496],[1004,499]],[[1008,476],[1013,474],[1045,488],[1040,491]],[[992,490],[1019,478],[1024,480],[997,493]]]:A.polygon('White roof landing H stroke',R.plan(quad,z),z,.025,'white')
 q=R.p((1004,488),H+.22);helicopter(q.x,q.y,H+.22,.86,'white')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2;A.box('Low segmented helipad rim',(q.x,q.y,H+.45),(v.length,.18,.5),'pod_frame',math.atan2(v.y,v.x))
 # Sculptural roof pod: pale shell, thick sliced cowl, and recessed curved glass.
 A.part('Large sliced roof pod');z=D['pod_base'];center=R.p(D['pod_center'],z);rad=D['pod_radius'];hh=D['pod_height'];nt,na=32,144;start,end=-math.pi*.18,math.pi*.31
 def q(t,a,shrink=0):return(center.x+(rad-shrink)*math.sin(t)*math.cos(a),center.y+(rad-shrink)*1.05*math.sin(t)*math.sin(a),z+(hh-min(.25,shrink))*math.cos(t))
 vs=[q(math.pi*j/(2*nt),2*math.pi*i/na) for j in range(nt+1) for i in range(na)];pale=[];glass=[]
 for j in range(nt):
  for i in range(na):
   angle=(2*math.pi*(i+.5)/na+math.pi)%(2*math.pi)-math.pi;face=(j*na+i,j*na+(i+1)%na,(j+1)*na+(i+1)%na,(j+1)*na+i)
   (glass if start<angle<end else pale).append(face)
 A.mesh('Pale ellipsoidal pod shell',vs,pale,'pod_shell');A.mesh('Recessed curved pod glazing',[q(math.pi*j/(2*nt),2*math.pi*i/na,2.0) for j in range(nt+1) for i in range(na)],glass,'pod_mesh_glass')
 for i in range(25):
  a=start+(end-start)*i/24;A.curve('Pod glazing meridian',[q(math.pi*j/(2*nt),a,1.97) for j in range(nt+1)],.021,'pod_frame')
 for j in range(1,25):A.curve('Pod glazing horizontal subdivision',[q(math.pi*j/(2*nt),start+(end-start)*i/48,1.97) for i in range(49)],.021,'pod_frame')
 for a in [start,end]:
  # Thick cut surfaces expose the dark lining beneath the pale hood.
  verts=[q(math.pi*j/(2*nt),a,shrink) for shrink in [0,2.0] for j in range(nt+1)];A.mesh('Exposed dark pod cowl cut',verts,[(j,j+1,j+1+nt+1,j+nt+1) for j in range(nt)],'pod_cowl_dark');A.curve('Fine pale outer cowl lip',[q(math.pi*j/(2*nt),a) for j in range(nt+1)],.11,'pod_shell')
 A.part('Raised curved EnergyPod name')
 # Conform every glyph vertex to the ellipsoid so the word never floats at the sides.
 ob=A.text('EnergyPod surface-conforming wordmark','EnergyPod',(center.x-.2,center.y,z+2.4),1.85,'pod_cowl_dark','regular',width=10.8,rot=(math.pi/2,0,0),depth=.09)
 import bpy
 bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(deps));matrix=ob.matrix_world.copy()
 for vertex in mesh.vertices:
  w=matrix@vertex.co;xx=w.x-center.x;zz=w.z-z;extrusion=w.y-center.y;w.y=center.y-rad*1.05*math.sqrt(max(.005,1-(xx/rad)**2-(zz/hh)**2))+extrusion-.025;vertex.co=w
 label=bpy.data.objects.new('EnergyPod glyphs attached to curved shell',mesh);A.COL.objects.link(label);label['part']=A.PART;bpy.data.objects.remove(ob,do_unlink=True)
 for x,y in [(1029,552),(925,519)]:
  q=R.p((x,y),D['main_height']+.2);A.hvac(q.x,q.y,D['main_height']+.2,1.8,1.2,.5)
 for x,y,h in [(1070,512,6.3),(1024,557,6.2)]:
  q=R.p((x,y),D['main_height']+.2);A.rod('Narrow rooftop equipment mast',(q.x,q.y,D['main_height']+.2),(q.x,q.y,D['main_height']+h),.095,'pod_frame',6)
 A.COL['measurement_file']='source/energy_pod_measurements.json';A.COL['inferred_details']='Pod shell curvature and hidden rear corner require comparison from a second view; source locations fix roof and pylon arrangement.'
 A.setup_preview(47.134,26.377,1400,1450);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('energy_pod','--no-render' not in sys.argv)
