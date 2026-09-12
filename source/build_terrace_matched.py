"""Terraced southeast office: measured stepped L plan and contrasting facade systems."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,AZ
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'terrace_office_measurements.json'));A.reset('terrace_office','Terraced office • measured L roof and brick return walls',['Original wide frame']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('terrace_roof',(.78,.73,.64),.9),('terrace_stone',(.52,.54,.52),.88),('terrace_brick',(.31,.13,.054),.9),('terrace_glass',(.071,.09,.092),.47)]:A.material(n,c,r)
 H=D['height'];h=D['floor_height']
 for k in range(3):
  roof=[q[:] for q in D['roof']]
  # The left wing steps out by one bay at each lower storey.
  for j in [0,1,4,5]:roof[j][0]-=(2-k)*6.5
  p=R.plan(roof,H);wall=inset(p,.19);z=k*h;A.part('Measured terraced floor '+str(k+1));A.polygon('Brick and glass storey core',wall,z,h-.22,'terrace_brick')
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;n=Vector((v.y,-v.x)).normalized();ang=math.atan2(v.y,v.x);q=(a+b)/2+n*.04;sx=v.x*math.cos(AZ)+v.y*math.sin(AZ);sy=v.x*math.sin(AZ)-v.y*math.cos(AZ)
   if sx*sy<0:
    # Front elevation has two deep horizontal openings split by a brick pier.
    A.box('Pale recessed front backing',(q.x,q.y,z+(h-.22)/2),(L,.08,h-.22),'terrace_stone',ang)
    for ff in [.015,.50,.985]:
     qq=a.lerp(b,ff)+n*.092;A.box('Short brick pier between front windows',(qq.x,qq.y,z+2.30),(.43,.08,1.40),'terrace_brick',ang)
    A.box('Broad pale front sill band',(q.x,q.y,z+.73),(L,.14,1.46),'terrace_stone',ang)
    for f0,f1 in [(.04,.46),(.54,.96)]:
     aa=a.lerp(b,f0);bb=a.lerp(b,f1);mid=(aa+bb)/2+n*.11;A.box('Deep paired front window bay',(mid.x,mid.y,z+2.30),((bb-aa).length,.045,1.32),'terrace_glass',ang)
     for j in range(5):
      qq=aa.lerp(bb,j/4)+n*.14;A.box('Fine mullion inside window bay',(qq.x,qq.y,z+2.30),(.027,.035,1.30),'terrace_stone',ang)
   else:
    # Brick side is nearly solid, with one narrow inset glazing course below the slab.
    A.box('Long recessed side glazing slit',(q.x,q.y,z+1.06),(L-.28,.035,.43),'terrace_glass',ang)
    A.box('Pale horizontal side floor course',(q.x,q.y,z+.46),(L+.035,.13,.73),'terrace_stone',ang)
  A.part('Projecting pale L floor plate');A.polygon('Measured L-shaped overhanging slab',p,z+h-.22,.22,'terrace_roof')
 A.part('Pale roof around four panel fields');A.polygon('Measured cream rooftop membrane',R.plan(D['roof'],H),H,.04,'terrace_roof')
 for quad in D['panels']:R.panels(quad,H+.08,4,5,tilt=5)
 A.COL['measurement_file']='source/terrace_office_measurements.json';A.COL['inferred_details']='Hidden rear entrances are inferred; the stepped west wing and broad glazed front bays are visible in the source.'
 A.setup_preview(47.134,26.377,1250,1100);R.camera(8);return A
if __name__=='__main__':build();A.save_asset('terrace_office')
