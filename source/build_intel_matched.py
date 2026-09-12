"""Intel campus, reconstructed from source roof contours and the original vector mark."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from mathutils import Vector
from math import atan2

def build():
 D=json.load(open(Path(__file__).with_name('intel_measurements.json')))
 A.reset('intel','Intel • measured stepped wings and vector roof mark',['Original wide frame','YU16','YU09'])
 R=Reference(D['anchor'],D['crop'])
 A.material('intel_glass',(.10,.19,.285),.52,.025)
 A.material('intel_spandrel',(.75,.68,.53),.80)
 A.material('intel_roof',(.79,.73,.63),.83)
 A.material('intel_box_blue',(.075,.17,.30),.78)
 A.material('intel_mark',(.015,.33,.55),.42)
 for m in D['volumes']:
  h=m['height'];p=R.plan(m['roof'],h);A.part(m['name']+' • measured mass')
  A.polygon('Stepped blue glazed envelope',p,0,h,'intel_glass')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;n=Vector((v.y,-v.x)).normalized();q=(a+b)/2+n*.09;ang=atan2(v.y,v.x)
   for k in range(m['floors']+1):
    z=.14 if k==0 else -.20+k*(h-.25)/m['floors']
    A.box('Broad continuous cream floor band',(q.x,q.y,z),(L+.04,.28,.58),'intel_spandrel' if k else 'intel_box_blue',ang)
   for j in range(1,round(L/1.5)):
    q=a.lerp(b,j/round(L/1.5))+n*.012
    A.box('Fine blue window joint',(q.x,q.y,h/2),(.012,.02,h),'intel_box_blue',ang)
  A.part(m['name']+' • roof');A.polygon('Pale oversailing roof',p,h-.10,.23,'intel_roof')
 for m in D['boxes']:
  A.part(m['name']);p=R.plan(m['roof'],m['height'])
  A.polygon('Raised blue rooftop enclosure',p,m['base'],m['height']-m['base'],'intel_box_blue');A.polygon('Thin cream enclosure lid',p,m['height'],.075,'intel_roof')
 A.part('Intel vector rooftop wordmark and broken oval')
 logo_fit=json.load(open(Path(__file__).with_name('intel_roof_logo_fit.json')))
 quad=[R.p(p,10.31) for p in logo_fit['quad']]
 def q(x,y):return quad[0].lerp(quad[1],x).lerp(quad[3].lerp(quad[2],x),y)
 for g in json.load(open(Path(A.ROOT)/'source/intel_logo_mesh.json')):
  base=[q(x,y) for x,y in g['vertices']];n=len(base);vs=[tuple(p+Vector((0,0,z))) for z in (0,.16) for p in base];fs=[]
  for f in g['faces']:
   a,b,c=(base[i] for i in f);f=tuple(f if (b-a).cross(c-a).z>0 else reversed(f))
   fs.extend([tuple(reversed(f)),tuple(i+n for i in f)])
  off=0
  for count in g['rings']:
   fs.extend((off+j,off+(j+1)%count,off+(j+1)%count+n,off+j+n) for j in range(count));off+=count
  A.mesh('Raised original Intel glyph and swoosh',vs,fs,'intel_mark')
 A.COL['measurement_file']='source/intel_measurements.json'
 A.COL['inferred_details']='Some ground-floor edges are hidden by avenue trees. Blue enclosure side elevations follow the measured roof plan.'
 A.setup_preview(47.134,26.377,1500,1100);R.camera(5)
 return A
if __name__=='__main__':build();A.save_asset('intel','--no-render' not in sys.argv)
