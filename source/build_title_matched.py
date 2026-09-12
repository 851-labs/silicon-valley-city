"""Rebuild all thirteen title buildings using individually matched roof contours."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
import build_title
from reference_geometry import Reference,set_color
from mathutils import Vector
P=Path(__file__).parent
def build():
 D=json.load(open(P/'title_towers_measurements.json'));data=json.load(open(P/'title_matched_footprints.json'));build_title.build(data)
 R=Reference(D['anchor'],D['crop']);A.COL['measurement_file']='source/title_towers_measurements.json';A.COL['roof_fit_report']='source/title_roof_fit_report.json';A.COL['inferred_details']='Nine visible facade courses; concealed rear elevations and parking interiors remain inferred.'
 # The Y roof sits on a parking volume whose broad front screen bridges the
 # letter's stem and right branch. It is not a screen on a short Y-shaped wall.
 for ob in list(A.COL.objects):
  name=ob.name
  if name.startswith('Y •') or name.startswith('front_6_Y • facade') or name.startswith('front_6_Y • structure • title_opaque') or name.startswith('Parking P') or name.startswith('Entrance barrier'):
   A.bpy.data.objects.remove(ob,do_unlink=True)
 A.part('Y parking volume • measured broad screen')
 H=14.60;pixels=[[916,240],[979,214],[1004,233],[936,250]];p=R.plan(pixels,H)
 A.material('title_parking_stone',(.40,.41,.39),.83);A.material('title_parking_glass',(.10,.23,.27),.34);A.material('title_parking_grid',(.34,.57,.60),.47)
 body=A.polygon('Y parking enclosure with cut-through ramp windows',p,0,H,'title_parking_stone',False)
 a=R.p((936,250),H);b=R.p((1004,233),H);u=(b-a).normalized();length=(b-a).length;n=Vector((u.y,-u.x,0))
 # Ensure the screen normal points towards the comparison camera.
 from reference_geometry import AZ,EL
 view=Vector((math.sin(AZ),-math.cos(AZ),0))
 if n.dot(view)<0:n=-n
 def point(s,z,d=0):return Vector((a.x,a.y,z))+u*s+n*d
 for k in range(3):
  f0,f1,z,rise,hh=[(.53,.94,1.8,.36,1.55),(.08,.62,5.8,1.0,1.75),(.53,.94,10.1,.36,1.55)][k];lo,hi=length*f0,length*f1
  q=[(lo,z),(hi,z+rise),(hi,z+rise+hh),(lo,z+hh)];vs=[tuple(point(s,zz,d)) for d in (-2.4,.6) for s,zz in q]
  cutter=A.mesh('Temporary sloping window cutter',vs,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'dark',False)
  mod=body.modifiers.new('True recessed ramp opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;A.bpy.context.view_layer.objects.active=body
  A.bpy.ops.object.modifier_apply(modifier=mod.name);A.bpy.data.objects.remove(cutter,do_unlink=True)
  A.mesh('Recessed sloping blue ramp glazing',[tuple(point(s,zz,-.22)) for s,zz in q],[(0,1,2,3)],'title_parking_glass')
  for f in (0,.33,.66,1):A.rod('Sloping cyan glazing rail',point(lo,z+hh*f,-.16),point(hi,z+rise+hh*f,-.16),.025,'title_parking_grid',5)
  for j in range(17):
   s=lo+(hi-lo)*j/16;zz=z+rise*j/16;A.rod('Vertical ramp window mullion',point(s,zz,-.15),point(s,zz+hh,-.15),.024,'title_parking_grid',5)
  A.rod('Projecting pale window sill',point(lo,z,.045),point(hi,z+rise,.045),.042,'title_opaque',5)
 A.part('Y parking volume • overhanging roof slab');A.polygon('Grey terrace beneath Y roof letter',p,H-.08,.11,'title_parking_stone')
 mid=(a+b)/2+n*.08;A.box('Projecting white front roof ledge',(mid.x,mid.y,H+.05),(length+.30,.83,.16),'title_opaque',math.atan2(u.y,u.x))
 # Narrow side returns keep the stacked office-floor glazing visible.
 for i in [0,1,3]:
  aa=R.p(pixels[i],H);bb=R.p(pixels[(i+1)%4],H);v=bb-aa;nn=Vector((v.y,-v.x,0)).normalized();mid=(aa+bb)/2+nn*.02;ang=math.atan2(v.y,v.x)
  center=sum((Vector((x,y,0)) for x,y in p),Vector())/len(p)
  if nn.dot((aa+bb)/2-center)<0:nn=-nn
  mid=(aa+bb)/2+nn*.03
  for k in range(9):A.box('Parking side ribbon glazing',(mid.x,mid.y,.40+k*1.59),(v.length,.03,1.02),'title_glass_a',ang)
 R.camera(4);set_color(A.MAT['title_roof_red'],(.95,.185,.11));A.flush();return A
if __name__=='__main__':build();A.save_asset('title_towers','--no-render' not in sys.argv)
