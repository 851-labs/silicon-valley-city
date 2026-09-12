"""Myspace party building, braced entrance and neighboring solar office."""
import os,sys,json,math,random
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art,facade
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'myspace_measurements.json'));A.reset('myspace','Myspace • measured roof party, braced entrance and solar office',['Original wide frame','YU11']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('myspace_roof',(.75,.70,.61),.9),('myspace_band',(.34,.35,.32),.8),('myspace_glass',(.21,.28,.28),.5),('myspace_sign',(.12,.13,.13),.85),('myspace_deck',(.25,.115,.054),.87)]:A.material(n,c,r)
 A.MAT['myspace_deck'].node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.10
 # Glazing varies broadly like the reflected planting in the production render.
 m=A.MAT['myspace_glass'];nd=m.node_tree.nodes;lk=m.node_tree.links;tc=nd.new('ShaderNodeTexCoord');no=nd.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=.7;no.inputs['Detail'].default_value=1.3;lk.new(tc.outputs['Object'],no.inputs['Vector']);r=nd.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.17;r.color_ramp.elements[0].color=(.16,.25,.28,1);r.color_ramp.elements[1].position=.83;r.color_ramp.elements[1].color=(.35,.39,.28,1);lk.new(no.outputs['Fac'],r.inputs[0]);lk.new(r.outputs[0],nd.get('Principled BSDF').inputs['Base Color'])
 for name,key in [('Myspace','party'),('Solar neighbor','solar')]:
  H=D[key+'_height'];p=R.plan(D[key+'_roof'],H);wall=inset(p,.22);A.part(name+' • four glazed floors');A.polygon('Measured four-storey enclosure',wall,0,H,'myspace_glass')
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));angle=math.atan2(v.y,v.x);mid=(a+b)/2+n*.07
   for k in range(1,5):
    z=k*H/4-.82;A.box('Broad grey floor band',(mid.x,mid.y,z),(L+.05,.15,1.40),'myspace_band',angle)
    for i in range(max(2,round(L/.20))):
     q=a.lerp(b,(i+.5)/round(L/.20))+n*.156;A.box('Subtle narrow vertical band flute',(q.x,q.y,z),(.06,.022,1.36),'myspace_band',angle)
   for i in range(round(L/1.1)+1):
    q=a.lerp(b,i/round(L/1.1))+n*.05;A.box('Fine glass mullion',(q.x,q.y,H/2),(.025,.10,H),'myspace_band',angle)
  A.part(name+' • shallow roof slab');A.polygon('Pale roof slab',p,H-.12,.24,'myspace_roof')
 H=D['party_height'];p=R.plan(D['party_roof'],H);A.part('Timber roof-party terrace');A.polygon('Roof deck',inset(p,.24),H+.12,.05,'myspace_deck')
 a,b,c,d=[R.p(q,H+.18) for q in D['party_roof']];N=round((b-a).length/.16)
 for i in range(N+1):
  t=i/N;A.rod('Narrow individual timber plank seam',a.lerp(b,t),d.lerp(c,t),.012,'wood',4)
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2;A.box('Low pale roof-party coping',(q.x,q.y,H+.36),(v.length,.23,.47),'myspace_roof',math.atan2(v.y,v.x))
 # Spa footprint is a separately measured rooftop quad, not a generic centered pool.
 rim=R.plan([[716,393],[727,388],[739,393],[728,400]],H+.8);A.part('Measured terrace hot tub');A.polygon('Raised square spa surround',rim,H+.18,.65,'myspace_band');A.polygon('Blue spa water',inset(rim,.22),H+.845,.025,'pool')
 for x,y,r in D['party_tree_crowns']:
  q=R.p((x,y+17),H+.18);A.box('Small roof planter',(q.x,q.y,H+.38),(1.35,1.35,.40),'myspace_band');A.tree(q.x,q.y,H+.6,r,3.0)
 random.seed(512)
 A.part('Individually located roof-party guests')
 for x,y in D['people_pixels']:
  q=R.p((x,y),H+.18);A.person(q.x,q.y,H+.18,random.choice(['white','red','yellow','purple','cyan','green']),random.random()*math.pi)
 # Tall ground-floor structural braces project in front of the glazed facade.
 edge0,edge1=D['party_roof'][0],D['party_roof'][3];a=R.p(edge0,H);b=R.p(edge1,H);u=(b-a).normalized();L=(b-a).length;n=Vector((u.y,-u.x,0));n=-n if n.y>0 else n;ang=math.atan2(u.y,u.x)
 A.part('Double-height entrance glazing and braces')
 for i in range(7):
  q=a.lerp(b,(i+.30)/7)+n*.65;A.box('Projecting entrance pier',(q.x,q.y,3.3),(.19,.25,6.6),'myspace_band',ang);A.rod('Diagonal entrance steel brace',q+Vector((0,0,-H+.3)),q+u*2.2+Vector((0,0,6.3-H)),.055,'frame',6)
 q=(a+b)/2+n*.67;A.box('Entrance head beam',(q.x,q.y,6.65),(L,.8,.40),'myspace_band',ang)
 A.part('Historical Myspace vector billboard');origin=R.facade_point((695,432),edge0,edge1,H)+n*.78;right=R.facade_point((767,464),edge0,edge1,H)+n*.78;v=Vector((0,0,5.50));A.mesh('Solid dark billboard face',[tuple(origin),tuple(right),tuple(right+v),tuple(origin+v)],[(0,1,2,3)],'myspace_sign');A.rod('Billboard top lip',origin+Vector((0,0,5.50)),right+Vector((0,0,5.50)),.07,'myspace_band',4)
 data=json.load(open(P/'myspace_2013_mesh.json'));o=R.facade_point((702,430),edge0,edge1,H)+n*.85;end=R.facade_point((758,455),edge0,edge1,H)+n*.85;width=(end-o).length;vector_art('Raised historical Myspace glyph',data,o,u*width,(0,0,width),.16,n)
 A.part('Round shared stair');H=D['core_height'];q=R.p(D['core_center'],H);rad=D['core_radius'];A.cylinder('Cylindrical pale stair',(q.x,q.y,H/2),rad,H,'myspace_band',128)
 for k in range(4):A.cylinder('Stair glass ribbon',(q.x,q.y,3.35+k*3.6),rad+.015,1.30,'myspace_glass',128)
 A.cylinder('Round pale stair roof',(q.x,q.y,H+.05),rad+.12,.12,'myspace_roof',128)
 for i in range(80):
  a=i*2*math.pi/80;A.rod('Round stair fine vertical seam',(q.x+(rad+.027)*math.cos(a),q.y+(rad+.027)*math.sin(a),0),(q.x+(rad+.027)*math.cos(a),q.y+(rad+.027)*math.sin(a),H),.012,'myspace_band',4)
 # YU11 shows nine continuous inclined racks, each with a 12 by 8 cell grid.
 # The recorded corners describe the visible inclined surface. Unproject each
 # corner at its own height so changing the section preserves that silhouette.
 R.solar_racks(D['solar_fields'],D['solar_height']+.24,D.get('solar_rack_rise',1.50),12,8,'myspace_rack_cells')
 A.COL['measurement_file']='source/myspace_measurements.json';A.COL['inferred_details']='Roof-party guest poses and obscured rear tree trunks are inferred from the wide frame; individual locations are measured.'
 A.setup_preview(47.134,26.377,1600,1200);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('myspace','--no-render' not in sys.argv)
