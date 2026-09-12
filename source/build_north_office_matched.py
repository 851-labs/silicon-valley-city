"""Northern repeated solar office: distinct two-floor block measured from the source."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'north_solar_office_measurements.json'));A.reset('north_solar_office','Northern solar office • measured two-storey row module',['Original wide frame']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('north_roof',(.84,.77,.64),.90),('north_stone',(.48,.49,.44),.86),('north_brick',(.24,.12,.066),.88),('north_glass',(.073,.084,.072),.53)]:A.material(n,c,r)
 H=D['height'];p=R.plan(D['roof'],H);wall=inset(p,.23);A.part('Two-storey glazed office body');A.polygon('Northern office brick enclosure',wall,0,H-.15,'north_brick')
 for a,b in zip(wall,wall[1:]+wall[:1]):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;n=Vector((v.y,-v.x)).normalized();angle=math.atan2(v.y,v.x);q=(a+b)/2+n*.08
  for k in range(2):
   z=k*H/2;A.box('Wide pale floor spandrel',(q.x,q.y,z+.58),(L+.05,.13,1.16),'north_stone',angle)
   A.box('Tall continuous northern window ribbon',(q.x,q.y,z+1.90),(L-.26,.04,1.55),'north_glass',angle)
   N=max(2,round(L/1.3))
   for j in range(N+1):
    q2=a.lerp(b,j/N)+n*.13;A.box('Slender full-height shopfront mullion',(q2.x,q2.y,z+1.90),(.055,.12,1.57),'north_stone',angle)
  for f in [0,1]:
   q=a.lerp(b,f)+n*.13;A.box('Brick corner pier',(q.x,q.y,H/2),(.34,.26,H-.14),'north_brick',angle)
 A.part('Pale overhanging flat roof');A.polygon('Thin pale office roof slab',p,H-.15,.22,'north_roof')
 for quad in D['panels']:R.panels(quad,H+.13,5,5,tilt=3)
 A.COL['measurement_file']='source/north_solar_office_measurements.json';A.COL['inferred_details']='Rear entrances are hidden by the northern row. Individual city placements are measured separately.'
 A.setup_preview(47.134,26.377,1250,1100);R.camera(8);return A
if __name__=='__main__':build();A.save_asset('north_solar_office')
