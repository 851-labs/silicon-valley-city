"""Small northeast olive house, measured independently from the surrounding offices."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'northeast_house_measurements.json'));A.reset('northeast_house','Northeast olive house • measured eaves, hipped roof and chimney',['Original wide frame']);R=Reference(D['anchor'],D['crop']);H=D['eave_height']
 for n,c,r in [('house_wall',(.39,.40,.17),.89),('house_roof',(.047,.042,.033),.94),('house_frame',(.18,.15,.061),.88),('house_glass',(.22,.24,.11),.65),('house_grass',(.20,.28,.031),.93)]:A.material(n,c,r)
 A.part('Measured small house enclosure');p=R.plan(D['eaves'],H);A.polygon('Pale olive single-storey walls',p,0,H,'house_wall')
 e=[R.p(v,H) for v in D['eaves']];ra,rb=[R.p(v,D['ridge_height']) for v in D['ridge']]
 A.mesh('Dark hipped roof end planes',[tuple(v) for v in [e[0],e[3],ra,e[1],e[2],rb]],[(0,1,2),(3,5,4)],'house_roof')
 A.part('Separate dark pitched roof planes')
 for points in [[e[0],e[1],rb,ra],[ra,rb,e[2],e[3]]]:
  vs=[tuple(v+Vector((0,0,z))) for z in [-.09,.07] for v in points]
  A.mesh('Thick dark roof plane',vs,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'house_roof')
 for a,b in [(e[0],e[1]),(e[3],e[2])]:A.rod('Dark projecting eave gutter',a,b,.045,'house_roof',6)
 A.rod('Raised dark ridge cap',ra+Vector((0,0,.08)),rb+Vector((0,0,.08)),.09,'house_roof',8)
 A.part('Measured framed windows on the long elevation')
 a,b=e[3],e[2];u=(b-a).normalized();n=Vector((u.y,-u.x,0));center=sum(e,Vector())/4
 if n.dot((a+b)/2-center)<0:n=-n
 angle=math.atan2(u.y,u.x)
 for f in [.16,.37,.61,.83]:
  q=a.lerp(b,f)+n*.02;z=H-1.35
  A.box('Recessed olive house window',(q.x,q.y,z),(.90,.06,1.36),'house_glass',angle)
  for dx in [-.48,0,.48]:
   qq=q+u*dx+n*.05;A.box('Narrow brown window jamb',(qq.x,qq.y,z),(.085,.10,1.51),'house_frame',angle)
  for dz in [-.73,.73]:A.box('Brown window head and sill',(q.x+n.x*.05,q.y+n.y*.05,z+dz),(1.02,.10,.085),'house_frame',angle)
 A.part('Tall dark rectangular roof chimney');q=R.p(D['chimney_top'],D['chimney_height']);base=D['chimney_height']-2.3
 A.box('Rectangular chimney shaft',(q.x,q.y,(base+D['chimney_height'])/2),(.48,.67,D['chimney_height']-base),'house_roof',angle)
 A.box('Projecting chimney cap',(q.x,q.y,D['chimney_height']+.045),(.64,.82,.11),'house_roof',angle)
 A.COL['measurement_file']='source/northeast_house_measurements.json';A.COL['inferred_details']='Rear roof extends beyond the master frame and the east wall is concealed by the courtyard campus. The visible eaves, ridge, chimney and framed windows are measured.'
 A.setup_preview(47.134,26.377,1200,800);R.camera(10);return A
if __name__=='__main__':build();A.save_asset('northeast_house')
