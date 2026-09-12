"""Hooli headquarters: heavy roof fascia, brick colonnade and deep green sign."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art,AZ
from build_ebay_matched import inset
from build_offices import dish
from mathutils import Vector
P=Path(__file__).parent
def build():
 D=json.load(open(P/'hooli_measurements.json'));F=json.load(open(P/'hooli_logo_fit.json'));A.reset('hooli','Hooli • measured colonnade, roof plant and vector letters',['Original wide frame','YU18','YU14']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('hooli_fascia',(.39,.40,.38),.86),('hooli_roof',(.70,.66,.58),.90),('hooli_brick',(.34,.13,.083),.89),('hooli_glass',(.028,.043,.038),.40),('hooli_vent',(.29,.28,.26),.86),('hooli_vent_cover',(.45,.42,.38),.90),('hooli_letter',(.44,.59,.002),.60)]:A.material(n,c,r)
 A.MAT['hooli_letter'].node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.035
 H=D['roof_height'];p=R.plan(D['main_roof'],H);aa,bb=[R.p(q,H) for q in D['front_edge']];u=(bb-aa).normalized();L=(bb-aa).length;n=Vector((u.y,-u.x,0));view=Vector((math.sin(AZ),-math.cos(AZ),0))
 if n.dot(view)<0:n=-n
 # Brick coordinates run along the facade and vertically, independent of batching.
 mat=A.MAT['hooli_brick'];nd=mat.node_tree.nodes;lk=mat.node_tree.links;pos=nd.new('ShaderNodeTexCoord');dot=nd.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=tuple(u);lk.new(pos.outputs['Object'],dot.inputs[0]);sep=nd.new('ShaderNodeSeparateXYZ');lk.new(pos.outputs['Object'],sep.inputs[0]);comb=nd.new('ShaderNodeCombineXYZ');lk.new(dot.outputs['Value'],comb.inputs[0]);lk.new(sep.outputs['Z'],comb.inputs[1]);brick=nd.new('ShaderNodeTexBrick');lk.new(comb.outputs[0],brick.inputs['Vector']);brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=.43;brick.inputs['Row Height'].default_value=.17;brick.inputs['Mortar Size'].default_value=.006;brick.inputs['Color1'].default_value=(.34,.13,.083,1);brick.inputs['Color2'].default_value=(.30,.10,.064,1);brick.inputs['Mortar'].default_value=(.26,.12,.08,1);lk.new(brick.outputs['Color'],nd.get('Principled BSDF').inputs['Base Color'])
 A.part('Recessed dark-glazed main enclosure');wall=inset(p,1.5);A.polygon('Recessed ground-floor glazing behind colonnade',wall,0,D['fascia_bottom'],'hooli_glass')
 for a,b in zip(wall,wall[1:]+wall[:1]):
  a,b=Vector(a),Vector(b);v=b-a;nn=Vector((v.y,-v.x)).normalized();N=max(1,round(v.length/2.1));angle=math.atan2(v.y,v.x)
  for i in range(N+1):
   q=a.lerp(b,i/N)+nn*.03;A.box('Fine recessed glazing mullion',(q.x,q.y,D['fascia_bottom']/2),(.065,.08,D['fascia_bottom']),'hooli_fascia',angle)
 A.part('Deep cantilevered main roof fascia');A.polygon('Heavy solid grey upper fascia',p,D['fascia_bottom'],H-D['fascia_bottom'],'hooli_fascia');A.polygon('Pale main roof membrane',p,H,.05,'hooli_roof')
 A.part('Main roof raised side and rear parapets')
 for j in [0,1,2]:
  a=R.p(D['main_roof'][j],H);b=R.p(D['main_roof'][(j+1)%4],H);b=a.lerp(b,.82) if j==2 else b;v=b-a;q=(a+b)/2;A.box('Low grey roof perimeter wall',(q.x,q.y,H+.36),(v.length,.20,.72),'hooli_fascia',math.atan2(v.y,v.x))
 A.part('Measured brick colonnade');a=aa+n*1.15;b=bb+n*1.15;mid=(a+b)/2;ang=math.atan2(u.y,u.x);bh=D['beam_top']-D['beam_bottom']
 A.box('Long brick entablature',(mid.x,mid.y,(D['beam_top']+D['beam_bottom'])/2),(L+.85,2.05,bh),'hooli_brick',ang)
 for i in range(D['columns']):
  q=a.lerp(b,(i+.3)/(D['columns']-.4));A.box('Square brick colonnade pier',(q.x,q.y,D['beam_bottom']/2),(1.52,1.70,D['beam_bottom']),'hooli_brick',ang)
 A.box('Covered pale entrance walkway',(mid.x,mid.y,.12),(L+1.0,5.1,.24),'hooli_roof',ang)
 A.part('Lower eastern annex');ah=D['annex_height'];p=R.plan(D['annex_roof'],ah);A.polygon('Stepped grey eastern service annex',p,0,ah,'hooli_fascia');A.polygon('Lower annex roof',p,ah,.09,'hooli_roof')
 for m in D['vent_boxes']:
  h=m['height'];p=R.plan(m['roof'],h);A.part('Roof plant • separate finned enclosure');A.polygon('Raised grey mechanical enclosure',p,H+.05,h-H-.05,'hooli_vent');A.polygon('Flat plant enclosure cover',p,h,.04,'hooli_vent_cover')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;nn=Vector((v.y,-v.x)).normalized();N=max(2,round(v.length/.21));angle=math.atan2(v.y,v.x)
   for j in range(N):
    q=a.lerp(b,(j+.5)/N)+nn*.05;A.box('Dense vertical plant-screen blade',(q.x,q.y,(h+H)/2),(.062,.15,h-H+.16),'hooli_fascia',angle)
 A.part('Measured open-mesh rooftop satellite dish');q=R.p((1255,156),18.3);rad=2.2
 def dp(t,a):return (q.x+rad*t*math.cos(a),q.y+rad*t*.4*math.sin(a),18.3+rad*t*.85*math.sin(a)+t*t*.22)
 for i in range(16):
  angle=i*2*math.pi/16;A.curve('Fine radial dish lattice',[dp(j/24,angle) for j in range(25)],.012,'frame')
 for j in range(1,9):A.curve('Circular dish lattice',[dp(j/8,i*2*math.pi/80) for i in range(81)],.012 if j<8 else .032,'frame')
 A.rod('Dish support post',(q.x,q.y,17.1),(q.x,q.y,18.3),.06,'frame',8)
 A.rod('Dish receiver stalk',(q.x,q.y,18.3),(q.x,q.y-.85,18.95),.035,'frame',8)
 A.part('Deep fitted Hooli vector sign');data=json.load(open(P/'hooli_logo_mesh.json'))
 for g in data:
  if g['name'] in ('h','l'):
   for q in g['vertices']:
    if q[1]>.238:q[1]=.238+(q[1]-.238)*F.get('stem_scale',1)
 origin=R.p(F['baseline'],D['sign_base']);width=F['screen_width']/(5*math.cos(AZ));vector_art('Hooli raised green glyph',data,origin,(width,0,0),(0,0,width),F['depth'],(0,-1,0))
 A.COL['measurement_file']='source/hooli_measurements.json';A.COL['inferred_details']='Rear limits partly outside source crop. Sign stems are fitted to the intro variant; original brand swoosh is absent.'
 A.setup_preview(47.134,26.377,1500,1300);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('hooli','--no-render' not in sys.argv)
