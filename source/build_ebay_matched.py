"""Reference-measured eBay warehouse with separate, editable architectural systems."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from mathutils import Vector
from math import atan2,pi,cos,sin
from build_offices import lattice,dish

def inset(points,d):
 from mathutils.geometry import intersect_line_line_2d
 out=[]
 for i,b in enumerate(points):
  a=Vector(points[i-1]);b=Vector(b);c=Vector(points[(i+1)%len(points)])
  u=(b-a).normalized();v=(c-b).normalized();n=Vector((-u.y,u.x))*d;m=Vector((-v.y,v.x))*d
  p=intersect_line_line_2d(a+n,b+n,b+m,c+m);out.append(tuple(p if p is not None else b+n))
 return out

def build():
 D=json.load(open(Path(__file__).with_name('ebay_measurements.json')))
 A.reset('ebay','eBay • measured polygonal warehouse and original raised lettering',['Original wide frame','YU24','YU16'])
 R=Reference(D['anchor'],D['crop']);H=D['roof_height'];p=R.plan(D['roof'],H);wall=inset(p,.37)
 A.material('ebay_masonry',(.70,.68,.625),.86)
 A.material('ebay_cornice',(.69,.67,.61),.83)
 A.material('ebay_roof',(.82,.74,.615),.87)
 A.material('ebay_window',(.014,.063,.070),.26,.07)
 A.material('ebay_copper',(.43,.18,.07),.67,.12)
 A.part('Polygonal masonry envelope');A.polygon('Measured six-edge warehouse',wall,0,H-.75,'ebay_masonry')
 for edge,(a,b) in enumerate(zip(wall,wall[1:]+wall[:1])):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));angle=atan2(v.y,v.x);count=max(2,round(L/3.9))
  for floor,z in enumerate([1.70,5.83]):
   for i in range(count):
    q=a+t*(i+.48)*L/count+n*.02
    # The entrance replaces a pair of lower windows on the short south-west facet.
    if edge==0 and floor==0 and i==count-1:continue
    A.box('Inset blue punched window',(q.x,q.y,z),(1.52,.035,2.33),'ebay_window',angle)
    q+=n*.035;A.box('Stone window sill',(q.x,q.y,z-1.18),(1.60,.12,.055),'ebay_cornice',angle)
    q-=t*.53;A.box('Fine dark frame',(q.x,q.y,z),(.035,.045,2.33),'dark',angle)
 A.part('Layered overhanging cornice')
 A.polygon('Lower roof string course',inset(p,.24),H-.94,.14,'ebay_cornice')
 A.polygon('Recessed cornice throat',inset(p,.43),H-.80,.22,'ebay_masonry')
 lower=inset(p,.32);N=len(p)
 A.mesh('Sloping cornice fascia',[(x,y,H-.58) for x,y in lower]+[(x,y,H-.21) for x,y in p],[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],'ebay_cornice')
 A.polygon('Upper pale cornice',p,H-.21,.21,'ebay_cornice');A.polygon('Warm roof membrane',inset(p,.14),H,.022,'ebay_roof')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2
  A.box('Thin raised perimeter upstand',(q.x,q.y,H+.12),(v.length,.095,.24),'ebay_cornice',atan2(v.y,v.x))
 A.part('Individual measured solar modules')
 for quad in D['panels']:
  # Retain source corner projections even when a module tilts above the roof.
  q=[R.p(v,H+.05+(.13 if j>1 else 0)) for j,v in enumerate(quad)]
  A.mesh('Source-traced discrete PV module',[tuple(v) for v in q],[(0,1,2,3)],'solar')
  for i in range(4):A.rod('Thin aluminium module frame',q[i],q[(i+1)%4],.011,'frame',4)
 A.part('Bent copper services')
 duct=[R.p(q,H+.38) for q in D['duct']]
 for a,b in zip(duct,duct[1:]+duct[:1]):
  v=b-a;q=(a+b)/2;A.box('Angular rectangular copper duct',tuple(q),(v.length,.42,.45),'ebay_copper',atan2(v.y,v.x))
 for quad,z in [([[710,513],[716,510],[722,513],[716,516]],.16),([[720,518],[726,515],[732,518],[726,521]],.16),([[730,523],[737,520],[744,523],[737,527]],.7)]:
  A.polygon('Copper equipment enclosure',R.plan(quad,H+z),H,z,'ebay_copper')
 for q0,q1 in [((696,515),(708,510)),((724,529),(733,525))]:R.segment('Bent service branch',q0,q1,H+.45,.5,.7,'ebay_copper')
 q=R.p(D['mast_base'],H+.02);lattice(q.x,q.y,H+.02,D['mast_height'],'ebay_copper')
 A.rod('Thin aerial above lattice',(q.x,q.y,H+D['mast_height']),(q.x,q.y,H+D['mast_height']+D['mast_spike']),.043,'metal',10)
 dish(q.x-.18,q.y-.15,H+1.7,.87,'ebay_copper')
 A.part('Curved entrance canopy and glazed entry')
 # Canopy is on the shallow front facet, directly below the left edge of the sign.
 q=R.p((655,559),5.1);axis=R.p((665,541),H)-R.p((594,526),H);axis.z=0;axis.normalize();normal=Vector((axis.y,-axis.x,0));angle=atan2(axis.y,axis.x)
 # Choose the outward side facing the source camera.
 if normal.y>0:normal=-normal
 rad=3.1;pts=[tuple((q+axis*(rad*cos(t))+normal*(rad*sin(t)))[:2]) for t in [pi*i/48 for i in range(49)]]
 A.polygon('Semicircular thick entrance canopy',pts,4.5,.6,'ebay_cornice')
 e=q-normal*.08;A.box('Blue entrance doors',(e.x,e.y,2.12),(4.3,.06,4.2),'ebay_window',angle)
 for k in [-2.15,0,2.15]:
  v=e+axis*k;A.box('Entrance door mullion',(v.x,v.y,2.12),(.07,.11,4.2),'frame',angle)
 e=q+normal*1.1;A.box('Dark entrance ramp',(e.x,e.y,.1),(5.0,2.7,.2),'paving',angle)
 A.part('Original eBay extruded vector lettering')
 base=R.p(D['sign_baseline'],D['sign_base_height']);end=R.p(D['sign_end'],D['sign_base_height']);t=(end-base);W=t.length;t.normalize();normal=Vector((t.y,-t.x,0))
 for g in json.load(open(Path(A.ROOT)/'source/ebay_logo_mesh.json')):
  n=len(g['vertices']);vs=[]
  for depth in [0,1.25]:
   for x,y in g['vertices']:vs.append(tuple(base+t*(x*W)+Vector((0,0,y*W*D['sign_height_scale']))+normal*depth))
  fs=[]
  for f in g['faces']:fs.extend([tuple(reversed(f)),tuple(j+n for j in f)])
  off=0
  for count in g['rings']:
   fs.extend((off+j,off+(j+1)%count,off+(j+1)%count+n,off+j+n) for j in range(count));off+=count
  A.mesh('Deep original eBay letter',vs,fs,g['material'])
 A.COL['measurement_file']='source/ebay_measurements.json'
 A.COL['inferred_details']='Roof modules occluded by the lattice mast are completed from their visible edges; rear facade windows use the visible facade rhythm.'
 A.COL['variant']='Original wide frame warehouse; historical vector wordmark, no later LED board.'
 A.setup_preview(47.134,26.377,1400,1050);R.camera(5)
 return A
if __name__=='__main__':build();A.save_asset('ebay','--no-render' not in sys.argv)
