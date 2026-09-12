"""Foreground Hewlett Packard slabs, independently measured roof levels and vector signs."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art
from build_ebay_matched import inset
from build_offices import lattice
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'legacy_hp_measurements.json'));A.reset('legacy_hp','Hewlett Packard • measured foreground slab roofs and original vector signs',['Original wide frame']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('hp_stone',(.46,.46,.405),.84),('hp_roof',(.70,.58,.43),.89),('hp_glass',(.10,.24,.30),.47),('hp_mullion',(.54,.56,.52),.70),('hp_copper',(.33,.14,.058),.73),('hp_letters',(.025,.021,.014),.70)]:A.material(n,c,r)
 A.material('hp_letter_tops',(.46,.39,.28),.77)
 for block in D['volumes']:
  H=block['height'];p=R.plan(block['roof'],H);wall=inset(p,.11);A.part(block['name']);A.polygon('Separate measured HP glass slab',wall,0,H-.13,'hp_glass')
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));angle=math.atan2(t.y,t.x);q=(a+b)/2+n*.04
   # Narrow horizontal joints run through the glass; the upper storeys have deep fins.
   for k in range(math.ceil(H/1.55)):
    z=H-.27-k*1.55;A.box('Fine HP floor course',(q.x,q.y,z),(L,.10,.13),'hp_stone',angle)
   N=max(2,round(L/1.30))
   for j in range(N+1):
    qq=a+t*(j*L/N)+n*.075;A.box('Thin full-height HP glazing mullion',(qq.x,qq.y,H/2),(.032,.08,H),'hp_mullion',angle)
    A.box('Deep upper HP vertical fin',(qq.x+n.x*.14,qq.y+n.y*.14,H-5.5),(.14,.36,10.8),'hp_stone',angle)
   for f in [0,1]:
    qq=a.lerp(b,f)+n*.09;A.box('Pale slab corner',(qq.x,qq.y,H/2),(.25,.18,H),'hp_stone',angle)
  A.polygon('Measured warm HP rooftop',p,H-.13,.24,'hp_roof')
 A.part('Historical HP roof monogram and wordmark')
 for key,file,aspect in [('wordmark','hp_wordmark_mesh.json',.3140648011),('monogram','hp_1979_mesh.json',.6220078765)]:
  q=D[key];z=q['height'];origin=R.p(q['origin'],z);u=R.p(q['u_end'],z)-origin;v=(R.p(q['v_end'],z)-origin)/aspect;data=json.load(open(P/file))
  for g in data:g['material']='hp_letters'
  vector_art('Raised historical HP '+key,data,origin,u,v,.37,Vector((0,0,1)))
 A.part('Individually located copper roof plant')
 for pixel,z,h in [((48,587),30.65,4.0),((61,582),30.65,3.2),((73,647),26.2,3.6),((87,641),26.2,1.35),((0,606),26.2,3.0)]:
  q=R.p(pixel,z);lattice(q.x,q.y,z,h,'hp_copper')
 for quad,z in [([[25,628],[31,625],[46,631],[39,635]],26.2),([[48,621],[54,618],[63,622],[57,626]],26.2),([[101,666],[109,662],[121,667],[113,672]],26.2),([[126,661],[132,658],[141,662],[135,665]],26.2)]:
  R.prism('Small HP copper roof equipment box',quad,z+.45,z,'hp_copper');p=R.plan(quad,z+.45)
  for a,b in zip(p,p[1:]+p[:1]):A.rod('Equipment box pale upper frame',(*a,z+.50),(*b,z+.50),.065,'hp_roof',6)
 A.COL['measurement_file']='source/legacy_hp_measurements.json';A.COL['inferred_details']='The lower tower heights and rear elevations lie outside the master crop. Visible roof positions, setback limits, upper facade rhythm and raised lettering are reconstructed independently.'
 A.flush()
 for ob in A.COL.all_objects:
  if ob.type=='MESH' and any(m.name=='hp_letters' for m in ob.data.materials):
   ob.data.materials.append(A.MAT['hp_letter_tops'])
   for poly in ob.data.polygons:
    if poly.normal.z>.5:poly.material_index=1
 A.setup_preview(47.134,26.377,1450,1000);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('legacy_hp')
