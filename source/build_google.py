"""Google campus: measured stepped roof volumes, terraces and courtyard."""
import os,sys,json,math,random
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from mathutils import Vector
from math import sin,cos,pi,atan2

def build():
 D=json.load(open(Path(__file__).with_name('google_measurements.json')))
 A.reset('google','Google campus • measured articulated roof plans',['Original wide frame','YU27','YU16'])
 R=Reference(D['anchor'],D['crop'])
 A.material('google_concrete',(.44,.43,.395),.80)
 A.material('google_window',(.32,.335,.32),.50,.03)
 A.material('google_pilaster',(.445,.435,.40),.78)
 A.material('google_west_glazing',(.058,.063,.068),.40)
 A.material('google_roof',(.95,.86,.76),.88)
 A.surface_detail(A.MAT['google_concrete'],.017,20)
 A.surface_detail(A.MAT['google_roof'],.009,34)
 for m in D['volumes']:
  h=m['height'];p=R.plan(m['roof'],h);A.part(m['name']+' • measured shell')
  A.polygon('Measured concrete envelope',p,0,h-.12,'google_concrete')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));ang=atan2(t.y,t.x)
   floors=m.get('windows',3);count=max(1,round(L/3.4));bay=L/count
   if floors and L>1.5:
    for j in range(count):
     q=a+t*(j+.5)*bay+n*.025
     for k in range(floors):
      z=(k+.52)*(h-.2)/floors
      glazing='google_window';wh=h/floors*.47
      if m['name']=='West office':z=2.75;wh=2.8;glazing='google_west_glazing'
      A.box('Recessed horizontal window panel',(q.x,q.y,z),(max(.15,bay-.35),.035,wh),glazing,ang)
    for j in range(count+1):
     q=a+t*j*bay+n*.075
     A.box('Broad concrete facade pier',(q.x,q.y,h/2),(.26,.23,h),'google_pilaster',ang)
  A.part(m['name']+' • roof')
  A.polygon('Pale measured flat roof',p,h-.12,.12,'google_roof')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2
   A.box('Thin raised coping',(q.x,q.y,h+.07),(v.length,.10,.16),'google_roof',atan2(v.y,v.x))
  for quad in m.get('panels',[]):R.panels(quad,h+.025,exclude=[m['roof_atrium']] if 'roof_atrium' in m else [])
  if 'roof_atrium' in m:
   A.part('Southwest roof • original party deck');pp=R.plan(m['roof_atrium'],h)
   A.polygon('Pale party area within solar field',pp,h+.004,.035,'google_roof')
   for i in range(8):
    u=random.uniform(.1,.9);v=random.uniform(.1,.9);q=Vector(pp[0]).lerp(Vector(pp[1]),u).lerp(Vector(pp[3]).lerp(Vector(pp[2]),u),v)
    A.person(q.x,q.y,h+.04,random.choice(['white','red','yellow']))
 for m in D['towers']:
  h=m['height'];p=R.plan(m['roof'],h);A.part(m['name'])
  A.polygon('Measured projecting service tower',p,0,h,'google_concrete')
  A.polygon('Pale service tower top',p,h,.09,'google_roof')
  # One narrow coloured inset, seen in the studio close-up.
  a,b=Vector(p[0]),Vector(p[1]);v=b-a;n=Vector((v.y,-v.x)).normalized();q=(a+b)/2+n*.025
  A.box('Service tower inset',(q.x,q.y,h-1.0),(.18,.04,.80),'glass_light',atan2(v.y,v.x))
 # The west wing has a circular open terrace, independent of the rectangular office.
 A.part('West office • measured circular terrace')
 p=R.plan(D['west_terrace'],D['west_terrace_height']);h=D['west_terrace_height']
 A.polygon('Curved open roof terrace',p,h-.23,.23,'google_roof')
 for i,(a,b) in enumerate(zip(p,p[1:]+p[:1])):
  if 10<=i<=11:continue
  va,vb=Vector(a),Vector(b);v=vb-va;q=(va+vb)/2
  A.box('Curved solid terrace parapet',(q.x,q.y,h+.48),(v.length+.025,.24,.96),'google_concrete',atan2(v.y,v.x))
 # Source-visible rear wedge and tall return walls support the curved cantilever.
 p=R.plan([[127,499],[144,492],[151,496],[143,511]],9.0)
 A.polygon('Circular terrace return pier',p,0,9.0,'google_concrete')
 # Front rounded entry and far-right lower terrace retain curved outlines.
 A.part('Southeast wing • rounded lower entry')
 p=R.plan([[304,632],[314,634],[322,640],[319,648],[310,652],[305,652],[302,649],[300,644],[301,638]],5.4)
 A.polygon('Rounded recessed entry',p,0,5.4,'google_concrete');A.polygon('Rounded entry cap',p,5.4,.13,'google_roof')
 A.part('Southeast wing • curved terminal terrace')
 p=R.plan([[486,678],[508,667],[515,671],[520,676],[521,680],[517,684],[509,688],[495,691]],4.1)
 A.polygon('Curved terminal terrace body',p,0,4.1,'google_concrete');A.polygon('Curved terrace roof',p,4.1,.15,'google_roof')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a
  for j in range(max(1,round(v.length/.23))):
   q=a.lerp(b,(j+.5)/max(1,round(v.length/.23)))
   A.box('Narrow timber terrace screen batten',(q.x,q.y,1.7),(.075,.075,3.3),'wood')
 # Bridges are reconstructed from visible paths with independent elevation control.
 def bridge(name,pixels,z0,z1,width):
  A.part(name);pts=[R.p(p,z0+(z1-z0)*i/(len(pixels)-1)) for i,p in enumerate(pixels)]
  vs=[]
  for i,q in enumerate(pts):
   t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]);t.z=0;t.normalize();n=Vector((-t.y,t.x,0))
   vs.extend([tuple(q-n*width/2),tuple(q+n*width/2)])
  A.mesh('Measured elevated walkway',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(pts)-1)],'google_roof')
  for side in (0,1):
   rail=[Vector(vs[2*i+side])+Vector((0,0,.43)) for i in range(len(pts))]
   A.curve('Continuous bridge guardrail',rail,.075,'google_roof')
   for i,q in enumerate(rail):A.rod('Bridge parapet support',Vector(vs[2*i+side]),q,.035,'google_concrete')
 bridge('West connecting bridge',[(130,520),(146,526),(163,533),(179,539)],6.6,7.2,1.5)
 bridge('Northwest arched courtyard bridge',[(276,586),(286,573),(301,558),(318,541),(336,526),(350,520)],5.4,8.2,1.45)
 bridge('Eastern courtyard footbridge',[(431,583),(446,571),(461,558),(480,548)],5.9,8.1,1.3)
 A.part('Google central courtyard');R.prism('Measured pale courtyard',D['courtyard'],.12,0,'google_roof')
 for px,py,color in D['parasols']:
  # The observed position is the parasol tip, not its ground attachment.
  q=R.p((px,py),2.2);A.umbrella(q.x,q.y,.10,1.05,color)
  A.cylinder('Small circular cafe table',(q.x+.4,q.y+.2,.68),.36,.09,'white',16)
 # Google wordmark remains editable vector geometry.
 A.part('Original Google roof lettering')
 fit=json.load(open(Path(A.ROOT)/'source/google_logo_extruded_fit.json'))['2013']['parameters']
 x,y,w,shear,v,extrusion_px=fit
 q=R.p((368+x+w/2,478+y+shear/2+.245*v),10.2)
 axis=R.p((w,shear),0)-R.p((0,0),0);ang=atan2(axis.y,axis.x);width=axis.length
 depth=extrusion_px/(5*abs(sin(math.radians(47.134259)-ang)))
 logo=A.colorword('Google',tuple(q),width,9.8,'serif',rot=(pi/2,0,ang),depth=depth)
 logo.scale.y=v/(width*5*cos(math.radians(26.377115)))
 A.COL['wordmark_fit']='2013 vector contour, physical extrusion and pose fitted to source colour masks; double-storey g retained.'
 for t in (-12,-7,-2,3,8,12):
  x=q.x+t*cos(ang);y=q.y+t*sin(ang)
  A.rod('Google sign narrow support',(x,y,8.2),(x,y,10.25),.052,'metal')
 # Roof planting occupies the original raised trapezoidal garden.
 A.part('Google raised eastern garden')
 garden=[[456,578],[502,555],[535,569],[516,598]];R.prism('Concrete raised garden',garden,3.4,0,'google_concrete');R.prism('Raised garden lawn',garden,3.45,3.4,'grass')
 for px,py in [(473,566),(487,568),(500,570),(514,575),(474,579),(490,582),(506,586)]:
  q=R.p((px,py),6.1);A.tree(q.x,q.y,3.45,.73,2.4)
 A.COL['measurement_file']='source/google_measurements.json'
 A.COL['variant']='Original wide-frame Google wordmark and party roof; later Alphabet sign and LED elements excluded.'
 A.COL['inferred_details']='Roof outlines behind lettering and foliage require additional-view verification. Rear service elevations follow the studio facade system.'
 A.setup_preview(47.134,26.377,1800,1150);R.camera(3)
 return A
if __name__=='__main__':build();A.save_asset('google','--no-render' not in sys.argv)
