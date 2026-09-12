"""Measured solid-masonry western office, preserving its asymmetric array layout."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from mathutils import Vector
from build_ebay_matched import inset

def build():
 D=json.load(open(Path(__file__).with_name('west_solar_measurements.json')))
 A.reset('west_solar','Western solar office • measured masonry and six roof fields',['Original wide frame','YU09'])
 R=Reference(D['anchor'],D['crop']);H=D['roof_height'];p=R.plan(D['roof'],H)
 A.surface_detail(A.material('aggregate_concrete',(.45,.415,.36),.88),.040,6.5)
 A.surface_detail(A.material('roof_membrane',(.78,.725,.62),.87),.012,60)
 A.material('entry_stone',(.52,.49,.43),.85);A.material('coping',(.69,.65,.57),.85)
 A.part('Uninterrupted aggregate envelope');wall=inset(p,.17);A.polygon('Measured blank masonry walls',wall,0,H-.20,'aggregate_concrete')
 for a,b in zip(wall,wall[1:]+wall[:1]):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;n=Vector((v.y,-v.x)).normalized()
  for i in range(1,round(L/4.5)):
   q=a.lerp(b,i/round(L/4.5))+n*.006
   A.box('Hairline precast joint',(q.x,q.y,(H-.7)/2),(.009,.012,H-.7),'entry_stone',math.atan2(v.y,v.x))
 A.part('Pale roof and fine coping');A.polygon('Thin roof edge',p,H-.20,.20,'coping');A.polygon('Unbroken pale roof membrane',inset(p,.12),H,.025,'roof_membrane')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2;A.box('Fine perimeter coping',(q.x,q.y,H+.045),(v.length,.095,.09),'coping',math.atan2(v.y,v.x))
 for field in D['arrays']:R.panels(field['quad'],H+.06,field['rows'],field['cols'],tilt=7)
 for m in D['annexes']+D['entry']:
  A.part(m['name']);h=m['height'];p=R.plan(m['roof'],h);A.polygon(m['name']+' walls',inset(p,.04),0,h-.13,'entry_stone' if m in D['entry'] else 'aggregate_concrete');A.polygon('Pale flat cap',p,h-.13,.13,'coping')
  if m.get('panels'):R.panels(m['panels'],h+.04,4,8,tilt=7)
 A.part('Measured narrow cypresses')
 for px,py,h,r in [(210,477,3.8,.57),(249,485,4.7,.70),(290,477,5.3,.74)]:
  q=R.p((px,py),0);A.cylinder('Cypress trunk',(q.x,q.y,.8),.07,1.6,'wood',8)
  A.cylinder('Tapered cypress crown',(q.x,q.y,h*.57),r,h*.89,'leaf_dark',12,r2=.014)
 A.COL['measurement_file']='source/west_solar_measurements.json';A.COL['inferred_details']='Windowless elevations are visible in the source; rear service access is occluded.'
 A.setup_preview(47.134,26.377,1500,1100);R.camera(5)
 return A
if __name__=='__main__':build();A.save_asset('west_solar','--no-render' not in sys.argv)
