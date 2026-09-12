"""Measured stepped Zynga offices, deeply recessed coloured windows and original dog sign."""
import os,sys,json,math,random
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def guest(R,pixel,z,index):
 q=R.p(pixel,z);c=['white','red','yellow','white','orange','cyan','green'][index%7];A.part('Individually placed rooftop guests');x,y=q.x,q.y
 A.box('Guest shirt',(x,y,z+1.31),(.42,.30,.68),c);A.sphere('Guest head',(x,y,z+1.95),(.18,.18,.21),'cream',10,7)
 for dx in [-.13,.13]:A.rod('Guest trouser leg',(x+dx,y,z+.98),(x+dx*1.7,y,z+.12),.082,'dark',8)
 for side in [-1,1]:
  shoulder=(x+side*.26,y,z+1.58);elbow=(x+side*.43,y+.04,z+(1.85 if (index+side)%3==0 else 1.12));hand=(x+side*.47,y-.04,z+(2.25 if (index+side)%3==0 else .94));A.rod('Posed guest upper arm',shoulder,elbow,.063,c,8);A.rod('Posed guest forearm',elbow,hand,.055,'cream',8)

def build():
 D=json.load(open(P/'zynga_measurements.json'));A.reset('zynga','Zynga • measured stepped studios, inset windows, party deck and dog sign',['Original wide frame','YU04']);R=Reference(D['anchor'],D['crop']);random.seed(293)
 for n,c,r in [('zynga_stone',(.46,.48,.45),.88),('zynga_roof',(.74,.70,.62),.87),('zynga_reveal',(.33,.34,.32),.80),('zynga_glass',(.07,.09,.085),.45),('zynga_green',(.15,.19,.075),.56),('zynga_yellow',(.46,.31,.025),.61),('zynga_orange',(.39,.15,.045),.58),('zynga_sign_red',(.60,.027,.006),.57)]:A.material(n,c,r)
 for block in D['volumes']:
  H=block['height'];Z0=block.get('bottom',0);step=(H-Z0)/block['floors'];p=R.plan(block['roof'],H);wall=inset(p,.17);A.part(block['name']);A.polygon('Recessed inner office core',inset(wall,.73),Z0,H-Z0-.14,'zynga_reveal')
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);t=b-a;L=t.length;t/=L;n=Vector((t.y,-t.x));angle=math.atan2(t.y,t.x);N=max(2,round(L/5.0));bay=L/N;ww=bay*.68;wh=3.25
   for k in range(block['floors']):
    z=Z0+k*step;mid=(a+b)/2
    for zz,hh in [(z+.50,1.0),(z+step-.55,1.1)]:A.box('Broad solid wall above and below windows',(mid.x,mid.y,zz),(L,.40,hh),'zynga_stone',angle)
    for j in range(N+1):
     q=a+t*(j*bay);A.box('Structural pier between recessed windows',(q.x,q.y,z+step/2),(bay-ww,.4,step),'zynga_stone',angle)
    for j in range(N):
     q=a+t*((j+.5)*bay);zc=z+2.70;front=[Vector((q.x,q.y,zc))+Vector((t.x,t.y,0))*dx+Vector((0,0,dz)) for dx,dz in [(-ww/2,-wh/2),(ww/2,-wh/2),(ww/2,wh/2),(-ww/2,wh/2)]];back=[v-Vector((n.x,n.y,0))*.49 for v in front]
     A.mesh('Four deep stone window reveals',[tuple(v) for v in front+back],[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'zynga_reveal')
     mat=random.choice(['zynga_glass','zynga_green','zynga_yellow','zynga_orange','zynga_green']);A.mesh('Inset coloured studio window',[tuple(v) for v in back],[(0,1,2,3)],mat)
     q2=q-n*.45;A.box('Dark inner window jamb',(q2.x+t.x*ww*.30,q2.y+t.y*ww*.30,zc),(.16,.08,wh),'zynga_glass',angle)
   for k in range(block['floors']+1):
    mid=(a+b)/2+n*.12;A.box('Projecting pale floor edge',(mid.x,mid.y,Z0+k*step),(L+.05,.25,.20),'zynga_roof',angle)
  A.polygon('Independent measured setback roof',p,H-.10,.20,'zynga_roof')
 H=D['anchor'][2];p=R.plan(D['volumes'][1]['roof'],H);A.part('Party-roof low parapet')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2;A.box('Low party deck parapet',(q.x,q.y,H+.24),(v.length,.16,.38),'zynga_roof',math.atan2(v.y,v.x))
 A.part('Measured raised rooftop spa');quad=[[813,618],[825,612],[836,618],[824,624]];R.prism('Timber hot-tub body',quad,H+1.03,H+.12,'wood');R.prism('Hot-tub blue water',quad,H+1.08,H+1.03,'pool')
 for px in [(820,617),(827,618)]:
  q=R.p(px,H+1.08);A.sphere('Seated spa guest head',(q.x,q.y,H+1.65),(.17,.17,.20),'cream',10,7)
 for i,px in enumerate([(772,616),(775,609),(780,614),(783,604),(787,611),(792,606),(793,599),(799,605),(801,612),(805,617),(810,611),(814,609),(816,616),(795,617),(789,619),(780,619),(776,612),(788,609),(797,610)]):guest(R,px,H+.12,i)
 A.part('Original red dog billboard');a=R.facade_point(D['sign_bottom_left'],*D['sign_wall'],16.35);b=R.facade_point(D['sign_bottom_right'],*D['sign_wall'],16.35);u=(b-a).normalized();L=(b-a).length;v=Vector((0,0,D['sign_height']));n=u.cross(v).normalized();a+=n*.35;b+=n*.35;vs=[tuple(q+n*d) for d in [0,.62] for q in [a,b,b+v,a+v]];ob=A.mesh('Deep red Zynga sign cabinet',vs,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'zynga_sign_red',False);be=ob.modifiers.new('Rounded red cabinet corners','BEVEL');be.width=.20;be.segments=4
 vector_art('Historical Zynga dog and vertical wordmark',json.load(open(P/'zynga_mesh.json')),a+u*(L*.10)+Vector((0,0,D['sign_height']*.10))+n*.65,u*(L*.80),Vector((0,0,D['sign_height']*.80/.9345246567)),.045,n)
 A.COL['measurement_file']='source/zynga_measurements.json';A.COL['inferred_details']='Lowest floors extend beyond the frame; rear walls repeat the visible recessed window construction. Party poses are reconstructed from visible positions.'
 A.setup_preview(47.134,26.377,1400,1100);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('zynga')
