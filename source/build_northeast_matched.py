"""Northeast courtyard campus, reconstructed as separate measured building wings."""
import os,sys,json,math,bpy
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,AZ
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'northeast_campus_measurements.json'));A.reset('northeast_campus','Northeast courtyard campus • measured wings, open cowls and garden',['Original wide frame']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('court_stone',(.43,.405,.36),.90),('court_roof',(.39,.53,.51),.82),('court_pale',(.67,.63,.55),.87),('court_dark',(.09,.10,.092),.76),('court_glass',(.17,.29,.29),.43),('court_grass',(.30,.35,.004),.93)]:A.material(n,c,r)
 A.MAT['court_grass'].node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.035
 A.part('Measured central lawn');A.polygon('Courtyard yellow-green lawn',R.plan(D['lawn'],.06),0,.12,'court_grass')
 # Curved source paths meet the circular walk tangentially rather than
 # crossing its central lawn. Control points are in the reference image.
 for pixels in [[(1149,40),(1150,37),(1153,34),(1152,31),(1156,28)],[(1165,50),(1171,50),(1179,46),(1187,42)],[(1152,59),(1161,60),(1169,56),(1175,55)]]:
  points=[R.p(p,.18) for p in pixels];path=[]
  for i in range(len(points)-1):
   a,b,c,d=points[max(0,i-1)],points[i],points[i+1],points[min(len(points)-1,i+2)]
   for j in range(12):
    t=j/12;path.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
  path.append(points[-1]);vs=[]
  for i,p in enumerate(path):
   tangent=(path[min(len(path)-1,i+1)]-path[max(0,i-1)]).normalized();n=Vector((-tangent.y,tangent.x,0))*.30;vs.extend([tuple(p+n),tuple(p-n)])
  A.mesh('Measured curved courtyard path',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(path)-1)],'court_pale')
 q=R.p((1148,49),.18);A.cylinder('Circular courtyard path',tuple(q),3.4,.10,'court_pale',96);A.cylinder('Round central lawn inset',(q.x,q.y,.24),2.75,.04,'court_grass',96);A.cylinder('Small central stone garden disc',(q.x,q.y,.30),1.22,.14,'court_stone',64)
 A.part('Small garden pool and shade shelter');R.prism('Shallow blue rectangular garden basin',[[1122,32],[1133,27],[1144,31],[1133,36]],.16,.05,'court_glass');R.prism('Pale flat shade canopy',[[1133,20],[1151,12],[1165,17],[1147,25]],2.1,1.92,'court_pale')
 for px in [(1135,20),(1148,24)]:
  q=R.p(px,1.92);A.rod('Slender garden canopy support',(q.x,q.y,0),(q.x,q.y,1.94),.055,'court_dark',6)
 for block in D['volumes']:
  H=block['height'];p=R.plan(block['roof'],H);wall=inset(p,.16);A.part(block['name']+' • measured volume')
  has_cowls='cowl' in block['name'];body=A.polygon('Separate grey courtyard building',wall,0,H-.12,'court_stone',batch=not has_cowls)
  roof=A.polygon('Separate measured flat roof',p,H-.12,.19,block.get('roof_material','court_roof' if block['style']!='slots' else 'court_pale'),batch=not has_cowls)
  if has_cowls:
   for i,pixels in enumerate(D['cowls']):
    opening=inset(R.plan(pixels,D['cowl_top']),.85)
    cutter=A.polygon('Temporary recessed cowl opening',opening,D['cowl_floor']-.01,3.0,'court_dark',batch=False)
    for ob in [body,roof]:
     mod=ob.modifiers.new('True roof aperture '+str(i+1),'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
     bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;n=Vector((v.y,-v.x)).normalized();ang=math.atan2(v.y,v.x);q=(a+b)/2+n*.025
   if block['style']=='punched':
    N=max(2,round(L/2.3))
    for k in range(block['floors']):
     for j in range(N):
      qq=a.lerp(b,(j+.5)/N)+n*.035;A.box('Small rear-slab window reveal',(qq.x,qq.y,1.0+k*H/block['floors']),(.38,.035,.88),'court_dark',ang)
   elif block['style']=='slots':
    sx=v.x*math.cos(AZ)+v.y*math.sin(AZ);sy=v.x*math.sin(AZ)-v.y*math.cos(AZ)
    if sx*sy>0:
     for k in range(8):A.box('Pavilion end horizontal louvre',(q.x,q.y,1.0+k*.56),(L,.12,.14),'court_pale',ang)
    else:
     for f in [.13,.39,.67,.88]:
      qq=a.lerp(b,f)+n*.05;A.box('Long raised pavilion wall rib',(qq.x,qq.y,H-1.6),(.13,.15,3.0),'court_pale',ang)
   elif block['style']=='glass':
    A.box('Recessed rear gallery glazing',(q.x,q.y,H*.48),(L-.25,.035,H*.78),'court_glass',ang)
    for k in range(4):A.box('Rear gallery horizontal frame',(q.x,q.y,.3+k*H/3),(L,.065,.19),'court_pale',ang)
   else:
    for k in range(1,3):A.box('Fine horizontal masonry joint',(q.x,q.y,k*H/3),(L,.06,.065),'court_pale',ang)
    for f in [.18,.75]:
     qq=a.lerp(b,f)+n*.026;A.box('Sparse high factory window',(qq.x,qq.y,H-1.6),(.64,.035,.85),'court_dark',ang)
 # Raised, splayed roof cowls continue through actual holes in the slab.
 for pixels in D['cowls']:
  top=D['cowl_top'];bottom=D['cowl_floor'];p=R.plan(pixels,top);outer_base=inset(p,-.30);inner=inset(p,.85);inner_base=inset(p,1.08);A.part('Splayed blue-green rooftop cowl');N=len(p)
  vs=[(x,y,5.45) for x,y in outer_base]+[(x,y,bottom) for x,y in inner_base]+[(x,y,top) for x,y in p]+[(x,y,top) for x,y in inner];faces=[]
  for i in range(N):
   j=(i+1)%N;faces.extend([(i,j,2*N+j,2*N+i),(N+i,3*N+i,3*N+j,N+j),(2*N+i,2*N+j,3*N+j,3*N+i)])
  A.mesh('Sloped outer hood and recessed inner walls',vs,faces,'court_roof');A.polygon('Recessed shadowed cowl floor',inner_base,bottom,.025,'court_dark')
 A.COL['measurement_file']='source/northeast_campus_measurements.json';A.COL['inferred_details']='Far rear wall limits and obscured doors are extrapolated; the visible roof outlines and courtyard features are independently measured.'
 A.setup_preview(47.134,26.377,1600,1000);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('northeast_campus')
