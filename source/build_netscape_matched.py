"""Original-frame Digg pavilion rebuilt from its independently traced curved edges."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art,AZ,S
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def spline(points,subdivisions=8,closed=True):
 points=[Vector(p) for p in points];out=[];N=len(points)
 for i in range(N if closed else N-1):
  a=points[(i-1)%N] if closed or i>0 else points[i];b=points[i];c=points[(i+1)%N];d=points[(i+2)%N] if closed or i+2<N else c
  for j in range(subdivisions):
   t=j/subdivisions;out.append((2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)*.5)
 if not closed:out.append(points[-1])
 return out

def build():
 D=json.load(open(P/'netscape_digg_measurements.json'));A.reset('netscape_digg','Digg • measured sinuous floor plates and swept glass sail',['Original wide frame','YU09','YU20']);R=Reference(D['anchor'],D['crop']);H=D['anchor'][2]
 for n,c,r,tr in [('curved_shell',(.55,.55,.50),.73,0),('curtain_glass',(.053,.064,.063),.55,0),('canopy_glass',(.80,.86,.86),.12,.94),('canopy_frame',(.68,.72,.71),.62,0),('digg_sign_blue',(.038,.12,.21),.8,0)]:A.material(n,c,r,trans=tr)
 A.material('curved_roof',(.80,.74,.65),.88)
 # Thin clear glazing transmits sunlight; the structural ribs cast the grid
 # visible on the terrace. Cycles' default opaque refractive shadow concealed it.
 glass=A.MAT['canopy_glass'];nd=glass.node_tree.nodes;lk=glass.node_tree.links
 glass.node_tree.nodes['Principled BSDF'].inputs['IOR'].default_value=1.32
 lightpath=nd.new('ShaderNodeLightPath');transparent=nd.new('ShaderNodeBsdfTransparent');mix=nd.new('ShaderNodeMixShader')
 transparent.inputs['Color'].default_value=(.70,.72,.74,1)
 lk.new(lightpath.outputs['Is Shadow Ray'],mix.inputs[0]);lk.new(nd['Principled BSDF'].outputs[0],mix.inputs[1]);lk.new(transparent.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],nd.get('Material Output').inputs['Surface'])
 outline=[tuple(p) for p in spline(D['roof_outline'],8)];plan=R.plan(outline,H);inside=inset(plan,.35)
 for k in range(3):
  z=.3+k*3.2;A.part('Measured sinuous floor '+str(k+1));p=plan
  if k==0:
   # The ground floor terminates beneath the raised rear terrace.
   def clip(poly,limit):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
     ina=a[0]<=limit;inb=b[0]<=limit
     if ina:out.append(a)
     if ina!=inb:
      t=(limit-a[0])/(b[0]-a[0]);out.append((limit,a[1]+t*(b[1]-a[1])))
    return out
   p=R.plan(clip(outline,454),H)
  A.polygon('Flowing continuous floor plate',p,z,.43,'curved_shell');wall=inset(p,.28)
  A.polygon('Dark recessed curved glazing',wall,z+.43,1.25,'curtain_glass')
  fascia=A.polygon('Deep pale curved spandrel',p,z+1.68,1.52,'curved_shell',batch=False)
  bevel=fascia.modifiers.new('Rounded source fascia edges','BEVEL');bevel.width=.13;bevel.segments=3
  fascia.modifiers.new('Weighted smooth fascia normals','WEIGHTED_NORMAL')
  # The wide frame shows broad solid wall sections interrupting the top two
  # curved window ribbons. These are masonry, not continuous tinted glazing.
  interruption={1:(378,405),2:(386,399)}.get(k)
  if interruption:
   for a,b in zip(p,p[1:]+p[:1]):
    a,b=Vector(a),Vector(b);q=(a+b)/2;v=b-a
    if v.length<.001:continue
    n=Vector((v.y,-v.x)).normalized();world=q+Vector((R.origin.x,R.origin.y))
    px=640+S*(math.cos(AZ)*world.x+math.sin(AZ)*world.y)
    toward_camera=Vector((math.sin(AZ),-math.cos(AZ)))
    if interruption[0]<=px<=interruption[1] and n.dot(toward_camera)>.15:
     A.mesh('Measured solid interruption in window ribbon',[(a.x,a.y,z+.43),(b.x,b.y,z+.43),(b.x,b.y,z+1.68),(a.x,a.y,z+1.68)],[(0,1,2,3)],'curved_shell')
  A.curve('Softened curved floor edge',[(x,y,z+.28) for x,y in p],.12,'curved_shell',True)
  length=0
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length
   if L<.001:continue
   n=Vector((v.y,-v.x)).normalized()
   old=length;length+=L
   if int(old/.70)!=int(length/.70):
    q=b+n*.02;A.rod('Fine curved glass division',(q.x,q.y,z+.45),(q.x,q.y,z+1.67),.016,'canopy_frame',4)
 A.part('Measured continuous dry rooftop');A.polygon('Pale sinuous roof surface',plan,H,.08,'curved_roof');rim=inset(plan,.26);A.curve('Roof parapet soft coping',[(x,y,H+.40) for x,y in rim],.085,'curved_shell',True)
 for a,b in zip(rim,rim[1:]+rim[:1]):A.mesh('Low continuous rooftop parapet',[(a[0],a[1],H+.08),(b[0],b[1],H+.08),(b[0],b[1],H+.40),(a[0],a[1],H+.40)],[(0,1,2,3)],'curved_shell')
 # Three independent observed curves define the foot rails and the sail's apex.
 left=[R.p(q,H+.23) for q in D['canopy_left']];right=[R.p(q,H+.23) for q in D['canopy_right']];apex=[R.p(q,z) for q,z in zip(D['canopy_apex'],D['canopy_apex_heights'])]
 left=spline(left,12,False);right=spline(right,12,False);apex=spline(apex,12,False)
 def q(j,u):
  a,b,p=left[j],right[j],apex[j];control=2*p-(a+b)*.5;return a*(1-u)**2+control*2*u*(1-u)+b*u*u
 A.part('Swept transparent sail • measured edge and apex curves');N=len(left);M=36;vs=[tuple(q(j,i/M)) for j in range(N) for i in range(M+1)];faces=[]
 for j in range(N-1):
  for i in range(M):a=j*(M+1)+i;faces.append((a,a+1,a+M+2,a+M+1))
 skin=A.mesh('Measured swept glass canopy skin',vs,faces,'canopy_glass',False,True)
 skin.modifiers.new('Thin laminated glass section','SOLIDIFY').thickness=.016
 for j in range(0,N,4):A.curve('Sail transverse arch rib',[tuple(q(j,i/48)) for i in range(49)],.035,'canopy_frame')
 for i in range(15):A.curve('Sail longitudinal lattice',[tuple(q(j,i/14)) for j in range(N)],.023,'canopy_frame')
 A.curve('Open leading arch frame',[tuple(q(0,i/64)) for i in range(65)],.067,'canopy_frame')
 for pts in [left,right]:A.curve('Canopy white sill rail',[tuple(q) for q in pts],.065,'curved_shell')
 A.part('Rear sun terrace');p=R.p((500,330),H+.10);A.umbrella(p.x,p.y,H+.10,2.4,'yellow')
 for x,y,c in [(539,315,'green'),(548,313,'orange')]:
  A.part('Tubular chaise lounge with reclining guest');p=R.p((x,y),H+.18)
  u=(R.p((x+5,y+3),H+.18)-p).normalized();side=Vector((-u.y,u.x,0))
  def chair_point(t,w,z):return p+u*t+side*w+Vector((0,0,z))
  for w in [-.39,.39]:
   A.rod('Pale tubular chaise side rail',chair_point(-1.12,w,.39),chair_point(.35,w,.39),.045,'white',8)
   A.rod('Angled chaise back frame',chair_point(.35,w,.39),chair_point(1.00,w,1.18),.045,'white',8)
   for t in [-.82,.26]:A.rod('Folding chaise leg',chair_point(t,w,.05),chair_point(t+.18,w,.39),.035,'white',8)
  for t,z,tt,zz in [(-1.12,.40,.35,.40),(.35,.40,1.00,1.17)]:
   A.mesh('Coloured stretched chaise fabric',[tuple(chair_point(t,-.34,z)),tuple(chair_point(t,.34,z)),tuple(chair_point(tt,.34,zz)),tuple(chair_point(tt,-.34,zz))],[(0,1,2,3)],c)
  for w in [-.11,.11]:A.rod('Reclining guest bare leg',chair_point(-.91,w,.53),chair_point(.06,w,.55),.085,'cream',8)
  A.rod('Reclining guest torso',chair_point(.06,0,.61),chair_point(.52,0,1.03),.19,'white',8)
  A.sphere('Reclining guest head',tuple(chair_point(.67,0,1.16)),(.15,.15,.17),'cream',12,8)
  for w in [-.24,.24]:A.rod('Guest arm resting along chair',chair_point(.40,w,.93),chair_point(-.05,w,.58),.058,'cream',8)
 A.part('Foosball under glass canopy')
 for px in [(376,376),(402,351),(425,329)]:
  p=R.p(px,H+.12);A.box('Small blue foosball table',(p.x,p.y,H+.86),(1.8,1,.3),'blue');A.box('Foosball green field',(p.x,p.y,H+1.02),(1.6,.8,.025),'green')
  for i in range(5):A.rod('Foosball cross-rod',(p.x-1.1,p.y-.3+i*.15,H+1.09),(p.x+1.1,p.y-.3+i*.15,H+1.09),.019,'metal',5)
  for dx in [-.65,.65]:
   for dy in [-.3,.3]:A.rod('Table leg',(p.x+dx,p.y+dy,H),(p.x+dx,p.y+dy,H+.85),.05,'dark',5)
 # Flat lower terrace and guard are measured separately from the flowing upper plate.
 p=R.plan([[447,382],[473,392],[572,351],[547,340]],2.0);A.part('Lower eastern terrace');A.polygon('Thin projecting terrace slab',p,1.9,.30,'curved_shell')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2;A.box('Low terrace parapet',(q.x,q.y,2.6),(v.length,.12,.80),'curved_shell',math.atan2(v.y,v.x))
 A.part('Measured Digg billboard');bottom=R.p(D['sign_bottom_left'],D['sign_base']);right=R.p(D['sign_bottom_right'],D['sign_base']);u=(right-bottom).normalized();L=(right-bottom).length;v=Vector((0,0,D['sign_height']));n=u.cross(v).normalized()
 if n.x<0:n=-n
 # The frame projects beyond the outside roof edge; lettering is on its outward face.
 vs=[tuple(p+n*z) for z in [0,.65] for p in [bottom,right,right+v,bottom+v]];sign=A.mesh('Thick measured blue Digg board',vs,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'digg_sign_blue',batch=False)
 bevel=sign.modifiers.new('Softened blue billboard corners','BEVEL');bevel.width=.32;bevel.segments=4
 sign.modifiers.new('Weighted billboard normals','WEIGHTED_NORMAL')
 vector_art('Original Digg vector wordmark',json.load(open(P/'digg_2010_mesh.json')),bottom+u*(L*.08)+Vector((0,0,D['sign_height']*.14))+n*.68,u*(L*.84),Vector((0,0,D['sign_height']*.73/.60)),.07,n)
 A.COL['measurement_file']='source/netscape_digg_measurements.json';A.COL['inferred_details']='Occluded rear access beneath the curved building remains inferred. Sinuous roof and canopy edges are directly measured in the source frame.'
 A.setup_preview(47.134,26.377,1600,1100);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('netscape_digg','--no-render' not in sys.argv)
