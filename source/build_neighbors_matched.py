"""Measured LinkedIn terraces and neighboring helicopter/office pavilions."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art,facade
from build_ebay_matched import inset
from build_landmarks import helicopter
from mathutils import Vector
from math import atan2,pi,cos,sin
P=Path(__file__).parent

def linkedin():
 D=json.load(open(P/'linkedin_measurements.json'));A.reset('linkedin','LinkedIn • measured stepped wings and original rooftop wordmark',['Original wide frame','YU16']);R=Reference(D['anchor'],D['crop'])
 A.material('linkedin_roof',(.75,.71,.63),.87);A.material('linkedin_fascia',(.57,.565,.515),.83)
 A.material('linkedin_glass',(.075,.085,.075),.33,.025);A.material('linkedin_brown_glass',(.14,.074,.035),.37,.035)
 A.material('linkedin_ink',(.068,.059,.041),.71);A.material('linkedin_blue',(.018,.089,.185),.57);A.material('linkedin_white',(.79,.83,.80),.65)
 for m in D['volumes']:
  H=m['height'];N=m['floors'];B=m['band'];p=R.plan(m['roof'],H);wall=inset(p,.24);A.part(m['name']+' • mass');A.polygon('Continuous glazing envelope',wall,0,H-.18,'linkedin_glass')
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));q=(a+b)/2+n*.03;ang=atan2(v.y,v.x);brown=abs(n.y)>.55
   for k in range(N):
    z=k*H/N
    A.box('Broad horizontal pale spandrel',(q.x,q.y,z+B/2),(L+.12,.14,B),'linkedin_fascia',ang)
    if brown:A.box('Warm reflected glass ribbon',(q.x,q.y,z+(H/N+B)/2),(L,.04,max(.25,H/N-B)),'linkedin_brown_glass',ang)
   bays=max(2,round(L/1.25))
   for i in range(bays+1):
    q=a+t*i*L/bays+n*.065;A.box('Slender curtain-wall vertical',(q.x,q.y,H/2),(.025,.10,H),'linkedin_fascia',ang)
  A.part(m['name']+' • overhanging flat terrace');A.polygon('Thick pale roof fascia',p,H-.18,.23,'linkedin_fascia');A.polygon('Pale roof membrane',inset(p,.025),H+.05,.02,'linkedin_roof')
 # Two independently measured photovoltaic fields on the highest wing.
 for field in D['panels']:R.panels(field,D['volumes'][0]['height']+.10,3,11,tilt=3)
 A.part('Original LinkedIn roof artwork')
 z=D['volumes'][1]['height']+.09;origin=R.p((70,390),z);u=R.p((119,368),z)-origin;v=(R.p((64,384),z)-origin)/.273
 data=json.load(open(P/'linkedin_logo_mesh.json'))
 for material,dz,depth in [('linkedin_blue',0,.12),('linkedin_white',.125,.02),('linkedin_ink',0,.24)]:
  vector_art('Raised historical LinkedIn glyph',[g for g in data if g['material']==material],origin+Vector((0,0,dz)),u,v,depth,(0,0,1))
 A.COL['measurement_file']='source/linkedin_measurements.json';A.COL['inferred_details']='Lowest storeys are partly screened by trees; window courses continue beneath those occlusions.'
 A.setup_preview(47.134,26.377,1400,1300);R.camera(6);return A

def small_offices():
 D=json.load(open(P/'small_offices_measurements.json'));A.reset('small_offices','Western pavilions • measured helipad and single-pitch office',['Original wide frame','YU09']);R=Reference(D['anchor'],D['crop'])
 A.material('pavilion_frame',(.57,.55,.49),.85);A.material('pavilion_roof',(.86,.77,.63),.86);A.material('pavilion_glass',(.047,.055,.049),.39);A.material('pad_orange',(.86,.28,.015),.76)
 m=D['helipad'];H=m['height'];p=R.plan(m['roof'],H);wall=inset(p,.10)
 A.part('Two-storey helipad pavilion');facade(wall,0,H-.3,'pavilion_glass','pavilion_frame',floors=2,band=1.0,bay=1.8)
 A.polygon('Wide overhanging helipad slab',p,H-.3,.3,'pavilion_frame');A.polygon('Cream helipad surface',p,H,.025,'pavilion_roof')
 q=R.p(m['circle_center'],H+.1);rad=m['radius'];A.cylinder('Orange circular landing pad',tuple(q),rad,.14,'pad_orange',96);A.cylinder('White circular pad inset',(q.x,q.y,H+.18),rad*.76,.035,'white',96)
 q=R.p((226,351),H+.21);A.cylinder('Orange inner landing emblem',tuple(q),rad*.48,.025,'pad_orange',64)
 A.part('Measured miniature helicopter');q=R.p((224,351),H+.20);helicopter(q.x,q.y,H+.20,.60,'white')
 m=D['office'];rear=m['rear_height'];front=m['eave_height'];floor=m['floor_height'];q=[R.p(px,rear if i<2 else front) for i,px in enumerate(m['roof'])];p=[tuple(v)[:2] for v in q]
 # Preserve CCW plan while retaining the height of each observed eave corner.
 if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))<0:p.reverse();q.reverse()
 A.part('Open lower level and structural posts');A.polygon('Raised upper-office floor',p,floor-.26,.26,'pavilion_frame')
 for a in p:A.box('Slender ground-floor corner support',(a[0],a[1],floor/2),(.26,.26,floor),'pavilion_frame')
 center=sum((Vector(v) for v in p),Vector((0,0)))/4
 A.box('Recessed lower service core',(center.x,center.y+.8,(floor-.2)/2),(2.4,1.8,floor-.2),'pavilion_glass')
 A.part('Upper glazed room');facade(p,floor,front-floor-.2,'pavilion_glass','pavilion_frame',floors=1,band=1.30,bay=1.8)
 for a,b in zip(q,q[1:]+q[:1]):
  A.mesh('Upper wall beneath sloping eave',[(a.x,a.y,front-.2),(b.x,b.y,front-.2),(b.x,b.y,b.z-.17),(a.x,a.y,a.z-.17)],[(0,1,2,3)],'pavilion_frame')
 A.part('Measured single-pitch pale roof');vs=[tuple(v-Vector((0,0,.17))) for v in q]+[tuple(v) for v in q];A.mesh('Solid inclined roof plate',vs,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'pavilion_roof')
 A.COL['measurement_file']='source/small_offices_measurements.json';A.COL['inferred_details']='Rear structure is partly concealed by parked vehicles; the isolated brown service block is not part of these two pavilions.'
 A.setup_preview(47.134,26.377,1400,1100);R.camera(8);return A
BUILDERS={'linkedin':linkedin,'small_offices':small_offices}
if __name__=='__main__':
 ids=sys.argv[sys.argv.index('--assets')+1:] if '--assets' in sys.argv else list(BUILDERS)
 for id in ids:BUILDERS[id]();A.save_asset(id)
