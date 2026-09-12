"""Adobe: measured stepped tower with projecting piers and original vector branding."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art,AZ
from build_ebay_matched import inset
from build_offices import lattice,dish
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'adobe_measurements.json'));A.reset('adobe','Adobe • measured stepped tower and vector end wall',['Original wide frame','YU11']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('adobe_stone',(.34,.34,.31),.82),('adobe_lower_rail',(.14,.23,.28),.7),('adobe_roof',(.37,.35,.31),.9),('adobe_glass',(.12,.24,.31),.5),('adobe_red',(.54,.052,.018),.8),('adobe_white',(.70,.73,.68),.82),('adobe_roof_plant',(.24,.23,.20),.83)]:A.material(n,c,r)
 m=A.MAT['adobe_glass'];nd=m.node_tree.nodes;lk=m.node_tree.links;tc=nd.new('ShaderNodeTexCoord');noise=nd.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1.5;noise.inputs['Detail'].default_value=1.0;lk.new(tc.outputs['Object'],noise.inputs['Vector']);r=nd.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.06,.14,.20,1);r.color_ramp.elements[1].color=(.22,.35,.42,1);lk.new(noise.outputs['Fac'],r.inputs[0]);lk.new(r.outputs[0],nd.get('Principled BSDF').inputs['Base Color'])
 for block in D['volumes']:
  H=block['height'];p=R.plan(block['roof'],H);wall=inset(p,.16);A.part(block['name']+' • measured curtain wall');A.polygon('Stepped glass volume',wall,0,H-.12,'adobe_glass')
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));angle=math.atan2(v.y,v.x);mid=(a+b)/2+n*.045
   px=v.x*math.cos(AZ)+v.y*math.sin(AZ);py=v.x*math.sin(AZ)-v.y*math.cos(AZ)
   flat=px*py<0 and 'Low' not in block['name'];z0=min(H,15.0) if flat else 0
   for k in range(block['floors']+1):
    z=k*H/block['floors'];lower=flat and z<z0
    A.box('Blue lower glazing band' if lower else 'Upper stone window rail',(mid.x,mid.y,z),(L+.04,.10,.16 if lower else .13),'adobe_lower_rail' if lower else 'adobe_stone',angle)
   count=max(2,round(L/1.06))
   for i in range(count+1):
    q=a.lerp(b,i/count)+n*.16
    # Broad front elevation has fine curtain-wall joints below the stepped piers.
    if H>z0:A.box('Deep stone pier above lower curtain wall',(q.x,q.y,(H+z0)/2),(.21,.36,H-z0),'adobe_stone',angle)
    if flat:
     q=a.lerp(b,i/count)+n*.04;A.box('Fine blue lower curtain-wall vertical',(q.x,q.y,z0/2),(.024,.055,z0),'adobe_lower_rail',angle)
    # Windows have a secondary slender division inside each structural bay.
    if i<count:
     q=a.lerp(b,(i+.50)/count)+n*.04
     if H>z0:A.box('Recessed upper secondary window mullion',(q.x,q.y,(H+z0)/2),(.022,.07,H-z0),'adobe_stone',angle)
     if flat:A.box('Fine blue lower secondary window mullion',(q.x,q.y,z0/2),(.016,.045,z0),'adobe_lower_rail',angle)
  A.part(block['name']+' • shallow roof cap');A.polygon('Thin grey setback roof',p,H-.12,.19,'adobe_roof')
 A.part('Individually measured rooftop equipment')
 for quad,H in [([[1191,362],[1207,355],[1214,360],[1198,367]],33.3),([[1136,434],[1147,429],[1154,433],[1143,439]],22.2)]:
  p=R.plan(quad,H+.26);A.polygon('Separate rectangular plant plinth',p,H+.09,.17,'adobe_roof_plant')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);t=b-a;q=(a+b)/2;A.box('Raised plant enclosure rim',(q.x,q.y,H+.42),(t.length,.15,.32),'adobe_stone',math.atan2(t.y,t.x))
  p=[Vector(v) for v in p]
  for f in [.32,.68]:
   q=p[0].lerp(p[1],f).lerp(p[3].lerp(p[2],f),.5);A.cylinder('Plant fan opening',(q.x,q.y,H+.45),.30,.04,'adobe_roof_plant',32)
 for line,H in [([(1210,373),(1214,375),(1220,372)],33.3),([(1153,446),(1156,448),(1161,445)],22.2)]:
  for a,b in zip(line,line[1:]):R.segment('Small bent roof pipe',a,b,H+.10,.10,.10,'adobe_stone')
 q=R.p((1239,354),33.45);lattice(q.x,q.y,33.45,5.35,'adobe_roof_plant')
 q=R.p((1254,348),34.25);dish(q.x,q.y,34.25,.64,'adobe_roof_plant')
 # Long red east-facing wall is coplanar with the main tower, from its setback downwards.
 H=D['volumes'][-1]['height'];a=R.p(D['sign_edge'][0],H);b=R.p(D['sign_edge'][1],H);u=(b-a).normalized();n=Vector((u.y,-u.x,0));view=Vector((math.sin(AZ),-math.cos(AZ),0))
 if n.dot(view)<0:n=-n
 A.part('Adobe red end wall');a+=n*.24;b+=n*.24;low=D['sign_bottom'];A.mesh('Full red end-wall panel',[(a.x,a.y,low),(b.x,b.y,low),tuple(b),tuple(a)],[(0,1,2,3)],'adobe_red');A.rod('Projecting red top coping',a+Vector((0,0,.04)),b+Vector((0,0,.04)),.10,'adobe_red',4)
 data=json.load(open(P/'adobe_1993_mesh.json'))
 for g in data:g['material']='adobe_white'
 origin=R.facade_point(D['logo_bottom_left'],*D['sign_edge'],H)+n*.28;width=(b-a).length*D['logo_width_pixels']/(D['sign_edge'][1][0]-D['sign_edge'][0][0])
 from reference_geometry import EL
 height=D['logo_height_pixels_per_svg_unit']/(5*math.cos(EL)) if 'logo_height_pixels_per_svg_unit' in D else width*.78
 vector_art('Historical Adobe symbol and wordmark',data,origin,u*width,Vector((0,0,height)),.10,n)
 A.COL['measurement_file']='source/adobe_measurements.json';A.COL['inferred_details']='Rear elevations and hidden ground entrances inferred; visible setback roof corners, structural piers and billboard plane are measured.'
 A.setup_preview(47.134,26.377,1300,1600);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('adobe','--no-render' not in sys.argv)
