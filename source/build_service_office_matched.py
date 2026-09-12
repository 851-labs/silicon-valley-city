"""Small grey service office behind the Digg pavilion, measured as a separate asset."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from build_ebay_matched import inset
from build_offices import dish
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'service_office_measurements.json'))
 A.reset('service_office','Central service office • recessed roof, dish and entrance canopy',['Original wide frame'])
 R=Reference(D['anchor'],D['crop']);H=D['height'];roof=R.plan(D['roof'],H)
 for name,color,rough in [('service_wall',(.31,.31,.28),.88),('service_roof',(.42,.41,.36),.94),('service_window',(.09,.10,.092),.67),('service_sill',(.42,.42,.39),.9),('service_dish',(.59,.59,.56),.88)]:A.material(name,color,rough)
 A.part('Measured two-storey service building')
 A.polygon('Grey masonry enclosure',inset(roof,.12),0,H-.30,'service_wall')
 A.polygon('Recessed grey roof membrane',inset(roof,.28),H-.28,.06,'service_roof')
 for a,b in zip(roof,roof[1:]+roof[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2
  A.box('Thick raised masonry roof parapet',(q.x,q.y,H-.13),(v.length+.32,.35,.40),'service_wall',math.atan2(v.y,v.x))
  A.box('Narrow roof coping',(q.x,q.y,H+.085),(v.length+.42,.44,.08),'service_roof',math.atan2(v.y,v.x))
 a,b=[R.p(q,H) for q in D['front_edge']];u=(b-a).normalized();n=Vector((u.y,-u.x,0));center=sum([Vector((x,y,H)) for x,y in roof],Vector())/len(roof)
 if n.dot((a+b)/2-center)<0:n=-n
 angle=math.atan2(u.y,u.x)
 A.part('Individually recorded upper windows and projecting sills')
 for pixel in D['upper_windows']:
  q=R.facade_point(pixel,*D['front_edge'],H)+n*.018
  A.box('Deep upper window reveal',tuple(q),(.56,.08,1.20),'service_window',angle)
  s=q+n*.07+Vector((0,0,-.65));A.box('Projecting pale window sill',tuple(s),(.76,.26,.13),'service_sill',angle)
 A.part('Low ground entrance and canopy')
 q=R.facade_point(D['door_center'],*D['front_edge'],H)+n*.02
 A.box('Broad shaded service entrance',(q.x,q.y,1.08),(2.7,.10,2.12),'service_window',angle)
 A.box('Thin entrance head lintel',(q.x+n.x*.08,q.y+n.y*.08,2.20),(2.9,.22,.12),'service_sill',angle)
 R.prism('Low projecting flat entrance canopy',D['canopy'],D['canopy_height'],D['canopy_height']-.16,'service_roof')
 A.part('Large separately measured satellite dish')
 q=R.p(D['dish_center'],D['dish_height']);dish(q.x,q.y,D['dish_height'],D['dish_radius'],'service_dish')
 A.COL['measurement_file']='source/service_office_measurements.json'
 A.COL['inferred_details']='Rear windows and concealed lower wall sections are unknown. Visible roof corners, upper window centres, canopy and dish are recorded separately.'
 A.setup_preview(47.134,26.377,1100,900);R.camera(10)
 return A
if __name__=='__main__':build();A.save_asset('service_office')
