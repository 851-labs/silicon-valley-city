"""Apple campus with a walkable annular terrace, inner parapet and glass guard."""
import os,sys,json,math,random
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,set_color
from build_campuses import ring
from mathutils import Vector,Matrix
from math import cos,sin,pi
import bmesh
P=Path(__file__).parent

def build():
 D=json.load(open(P/'apple_measurements.json'));F=json.load(open(P/'apple_sculpture_fit.json'));A.reset('apple','Apple • measured ring terrace, glass rail and central sculpture',['Original wide frame','YU14','YU18']);R=Reference(D['anchor'],D['crop'])
 A.material('apple_parapet',(.77,.74,.66),.85);A.material('apple_cap',(.96,.87,.76),.88);A.material('apple_deck',(.27,.28,.265),.84);A.material('apple_glass',(.13,.22,.24),.28,.08);A.material('apple_guard',(.78,.86,.88),.10,0,trans=.98);A.material('apple_frame',(.44,.48,.47),.47,.3);A.material('apple_sculpture',(.93,.95,.87),.67)
 set_color(A.MAT['grass'],(.048,.12,.004))
 A.MAT['apple_guard'].node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.25
 c=R.p(D['ring_center'],D['ring_center_height']);outer=D['outer_radius'];inner=D['inner_radius'];wall=D['inner_wall_outer_radius'];deck=D['deck_height'];top=D['parapet_top']
 def ann(name,ro,ri,z,h,mat):ring(name,c.x,c.y,ro,ri,z,h,mat,256)
 A.part('Low annular office structure');ann('Outer recessed curved glazing',outer-.22,inner+.12,.2,deck-.4,'apple_glass');ann('Bottom structural slab',outer-.10,inner,.12,.20,'apple_parapet');ann('Continuous pale spandrel',outer-.12,outer-.35,1.3,.49,'apple_parapet')
 for i in range(208):
  a=2*pi*i/208;r=outer-.15;A.rod('Fine curved-facade mullion',(c.x+r*cos(a),c.y+r*sin(a),.3),(c.x+r*cos(a),c.y+r*sin(a),deck-.1),.022,'apple_frame',6)
 A.part('Walkable annular roof terrace');ann('Terrace slab',outer,inner,deck-.20,.20,'apple_parapet');ann('Grey exposed terrace paving',outer-.05,wall,deck,.025,'apple_deck')
 A.part('Solid inner courtyard parapet');ann('Tall continuous inner wall',wall,inner,0,top,'apple_parapet');ann('Broad pale parapet cap',wall+.015,inner-.015,top,.055,'apple_cap')
 # The studio view shows horizontal panel courses on the inside of this wall.
 for z in [.72,1.50,2.28,3.06,3.84,4.62]:ann('Fine inner-wall horizontal joint',inner+.005,inner-.008,z,.016,'apple_deck')
 A.part('Outer transparent terrace railing');ann('Curved transparent guard',outer-.01,outer-.045,deck+.08,D['glass_top']-deck-.08,'apple_guard');ann('Continuous top rail',outer+.02,outer-.055,D['glass_top'],.042,'apple_frame')
 for i in range(144):
  a=2*pi*i/144;r=outer-.018;A.rod('Slender terrace-glass post',(c.x+r*cos(a),c.y+r*sin(a),deck),(c.x+r*cos(a),c.y+r*sin(a),D['glass_top']),.018,'apple_frame',5)
 A.part('Courtyard lawn and paths');A.cylinder('Round courtyard lawn',(c.x,c.y,.05),inner,.10,'grass',192)
 ann('Narrow inner walking path',inner-.10,inner-.85,.115,.04,'apple_deck')
 A.part('Central white Apple sculpture');z=D['sculpture_base']+D['sculpture_depth'];q=R.p(F['top_face_center'],z)
 A.logo('apple',(q.x,q.y,D['sculpture_base']),F['logo_height'],D['sculpture_depth'],'apple_sculpture',rot=(0,0,F['rotation']))
 # Individual source-observed crown positions replace the earlier random forest.
 random.seed(2609);bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1);bm.verts.ensure_lookup_table();base=[v.co.copy() for v in bm.verts];lookup={v:i for i,v in enumerate(bm.verts)};faces=[tuple(lookup[v] for v in f.verts) for f in bm.faces];bm.free()
 A.part('Courtyard • individually located faceted trees')
 for i,(x,y,r,h) in enumerate(D['broadleaf_crowns']):
  r*=1.16
  q=R.p((x,y),h*.78);A.cylinder('Visible russet tree trunk',(q.x,q.y,h*.34),.105,h*.68,'wood',7)
  rot=Matrix.Rotation(random.random()*2*pi,3,'Z');vs=[]
  for v in base:
   p=rot@Vector((v.x*r,v.y*r*.94,v.z*h*.34));vs.append((q.x+p.x,q.y+p.y,h*.78+p.z))
  A.mesh('Measured faceted crown',vs,faces,['tree','leaf_olive','leaf_light','leaf_dark'][i%4])
 A.part('Courtyard • individually located cypresses')
 for i,(x,y,h) in enumerate(D['cypress_tops']):
  q=R.p((x,y),h);A.cylinder('Cypress trunk',(q.x,q.y,h*.21),.055,h*.42,'wood',6)
  A.cylinder('Faceted pointed cypress',(q.x,q.y,h*.54),h*.21,h*.92,'leaf_dark' if i%3 else 'tree',8,r2=0)
 A.COL['measurement_file']='source/apple_measurements.json';A.COL['inferred_details']='The ring facade is partly hidden; terrace section is reconstructed from studio views. Plant crowns are placed from the wide image, with inferred depth.'
 A.setup_preview(47.134,26.377,1600,1000);R.camera(4);return A
if __name__=='__main__':build();A.save_asset('apple','--no-render' not in sys.argv)
