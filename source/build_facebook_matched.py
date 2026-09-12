"""Facebook campus rebuilt from nine independently measured roof outlines."""
import os,sys,json,math,random
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art,EL
from build_offices import dish,lattice
from mathutils import Vector
from math import sin,cos,pi,atan2
D=json.load(open(Path(__file__).with_name('facebook_measurements.json')))
A.reset('facebook','Facebook campus • nine measured roof contours',['Original wide frame','YU15'])
R=Reference(D['anchor'],D['crop'])
A.material('facebook_glass',(.014,.10,.155),.42,.02)
A.material('facebook_roof',(.95,.86,.76),.88)
A.material('facebook_louver',(.70,.63,.52),.79)
A.material('facebook_duct',(.58,.24,.105),.59)
A.material('facebook_lawn',(.145,.235,.018),.85)
A.surface_detail(A.MAT['facebook_roof'],.011,17)

def inside(x,y,poly):
 c=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
 return c

def foliage(poly,z,density=.33):
 p=R.plan(poly,z);area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2)
 x0,x1=min(q[0] for q in p),max(q[0] for q in p);y0,y1=min(q[1] for q in p),max(q[1] for q in p)
 placed=[]
 for i in range(round(area*density)*50):
  x=random.uniform(x0,x1);y=random.uniform(y0,y1)
  if not inside(x,y,p) or any((x-a)**2+(y-b)**2<.75**2 for a,b in placed):continue
  placed.append((x,y));h=random.uniform(1.0,1.8);r=random.uniform(.50,.78)
  if random.random()<.13:
   A.cylinder('Roof cypress trunk',(x,y,z+h*.29),.04,h*.58,'wood',6)
   A.cylinder('Roof cypress crown',(x,y,z+h*.67),r*.6,h,'tree',7,r2=.025)
  else:
   A.cylinder('Roof garden trunk',(x,y,z+h*.28),.04,h*.56,'wood',7)
   A.sphere('Faceted compact garden crown',(x,y,z+h*.77),(r,r*.90,h*.42),random.choice(['tree','leaf_olive','leaf_light']),8,5)
  if len(placed)>=round(area*density):break

for m in D['modules']:
 name=m['name'];h=m['height'];p=R.plan(m['roof'],h)
 A.part(name+' • measured shell')
 A.polygon('Glazed measured footprint',p,0,h-.18,'facebook_glass')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));mid=(a+b)/2;ang=atan2(t.y,t.x)
  long=L>10.5
  if long:
   # Close-up YU15: long sides are horizontal cream louvers; ends remain blue.
   end=min(1.0,L*.075)
   for k in range(9):
    q=mid+n*.11;zz=.20+k*(h-.62)/8
    A.box('Projecting horizontal solar louver',(q.x,q.y,zz),(L-2*end,.25,.14),'facebook_louver',ang)
   for j in range(max(2,round(L/2.1))+1):
    q=a+t*(end+j*(L-2*end)/max(2,round(L/2.1)))+n*.17
    A.box('Louver support upright',(q.x,q.y,(h-.4)/2),(.105,.27,h-.4),'facebook_louver',ang)
  for k in range(4):
   q=mid+n*.075
   A.box('Three storey cream floor edge',(q.x,q.y,.14+k*(h-.70)/3),(L+.035,.15,.17),'facebook_louver',ang)
  if not long:
   for j in range(1,max(2,round(L/2.5))):
    q=a+t*j*L/max(2,round(L/2.5))+n*.08
    A.box('Blue end elevation mullion',(q.x,q.y,(h-.5)/2),(.055,.16,h-.5),'facebook_louver',ang)
 A.part(name+' • measured roof')
 A.polygon('Flat pale roof with solid perimeter fascia',p,h-.32,.32,'facebook_roof')
 for eq in m.get('equipment',[]):
  pe=R.plan(eq,h+.01)
  longest=max(range(4),key=lambda i:(Vector(pe[(i+1)%4])-Vector(pe[i])).length)
  pe=pe[longest:]+pe[:longest]
  va,vb=Vector(pe[0]),Vector(pe[1]);vc=Vector(pe[2]);u=vb-va;v=vc-vb
  # All ducts follow the observed quadrilateral, including module-specific rotations.
  for aa,bb in zip(pe,pe[1:]+pe[:1]):
   aa,bb=Vector(aa),Vector(bb);q=(aa+bb)/2;d=bb-aa
   A.box('Low rectangular copper roof duct',(q.x,q.y,h+.13),(d.length,.32,.26),'facebook_duct',atan2(d.y,d.x))
  # Three short crossbars, one enclosure, conduit and small dish.
  for tt in (.25,.50,.75):
   q=va+u*tt;end=q+v;d=end-q
   A.box('Copper duct cross connection',tuple((Vector((q.x,q.y,h+.13))+Vector((end.x,end.y,h+.13)))/2),(d.length,.26,.25),'facebook_duct',atan2(d.y,d.x))
  q=va+u*.78+v*.5
  A.box('Rectangular rooftop enclosure',(q.x,q.y,h+.35),(1.2,.8,.60),'facebook_duct',atan2(u.y,u.x))
  q=va+u*.50+v*.45;dish(q.x,q.y,h+.54,.40,'facebook_duct')
  q=va+u*.32+v*.26;end=q+v*.47
  A.rod('Curved service conduit',(q.x,q.y,h+.17),(end.x,end.y,h+.17),.095,'facebook_duct')
 if 'mast' in m:
  q=R.p(m['mast'],h);lattice(q.x,q.y,h,2.7,'facebook_duct')
 if 'garden' in m:
  A.part(name+' • measured planting bed');R.prism('Roof planting soil',m['garden'],h+.025,h,'facebook_lawn');foliage(m['garden'],h+.03)
 for step in m.get('roof_steps',[]):
  A.part(name+' • stepped roof relief');R.prism('Raised angular roof strip',step,h+.9,h,'facebook_roof')
 if 'party' in m:
  A.part('Facebook party • measured terrace')
  pp=R.plan(m['party'],h);A.polygon('Party roof deck',pp,h,.12,'facebook_roof')
  for a,b in zip(pp,pp[1:]+pp[:1]):
   va,vb=Vector(a),Vector(b);v=vb-va;q=(va+vb)/2
   A.box('Party parapet',(q.x,q.y,h+.37),(v.length,.16,.55),'facebook_roof',atan2(v.y,v.x))
  # The party props fit the measured deck, rather than overhanging an invented box.
  for i in range(24):
   while True:
    q=(random.uniform(min(x for x,y in pp),max(x for x,y in pp)),random.uniform(min(y for x,y in pp),max(y for x,y in pp)))
    if inside(*q,pp):break
   A.person(*q,h+.13,random.choice(['white','red','yellow','purple','cyan']))
  q=R.p((644,171),h);A.box('Wood-sided hot tub',(q.x,q.y,h+.47),(1.8,1.8,.70),'wood');A.box('Hot tub water',(q.x,q.y,h+.85),(1.5,1.5,.055),'pool')
  q=R.p((618,167),h);A.box('Twister game white mat',(q.x,q.y,h+.15),(2.3,1.6,.025),'white')
  for i in range(4):
   for j in range(3):A.cylinder('Twister colored circle',(q.x+(i-1.5)*.5,q.y+(j-1)*.5,h+.17),.17,.008,['red','green','yellow','blue'][i],12)

# Low horizontal Like sculpture on the north campus plaza.
like=json.load(open(Path(__file__).with_name('facebook_like_measurements.json')))
A.material('facebook_like_edge',(.08,.115,.18),.81)
A.material('facebook_like_cuff',(.24,.27,.32),.86)
A.material('facebook_like_hand',(.87,.86,.80),.90)
A.material('facebook_plaza',(.48,.46,.40),.93)
A.part('Northern Like sculpture plaza')
R.prism('Measured pale paved Like plaza',[[530,94],[563,62],[595,48],[646,65],[586,88],[577,97]],.035,.01,'facebook_plaza')
A.part('Measured horizontal Facebook Like sculpture')
z=like['height']
A.polygon('Continuous blue-edged hand and cuff plinth',R.plan(like['backing_outline'],z),.08,z-.08,'facebook_like_edge')
A.polygon('Raised blue-grey sleeve cuff',R.plan(like['cuff'],z+.08),z,.08,'facebook_like_cuff')
A.polygon('Raised white thumb and folded fingers',R.plan(like['hand_outline'],z+.12),z,.12,'facebook_like_hand')
q=R.p(like['button_center'],z+.105);A.cylinder('Small white cuff button',tuple(q),.24,.045,'facebook_like_hand',32)

# Billboard geometry is fitted to all four screen corners.
A.part('Facebook billboard • measured four-corner plane')
h0=5.6;h1=h0+(144-115)/(5*math.cos(math.radians(26.377115)))
left=R.p((670,144),h0);right=R.p((743,116),h0);d=right-left;ang=atan2(d.y,d.x);mid=(left+right)/2
panel=A.sign_panel('Facebook blue billboard',(mid.x,mid.y,(h0+h1)/2),d.length,h1-h0,'facebook',.28,.015);panel.rotation_euler=(pi/2,0,ang)
normal=Vector((sin(ang),-cos(ang),0));q=mid+normal*.16
fit=json.load(open(Path(__file__).with_name('facebook_billboard_logo_fit.json')))
glyphs=json.load(open(Path(__file__).with_name('facebook_2005_mesh.json')))
A.material('facebook_letter',(.71,.74,.78),.88)
for glyph in glyphs:glyph['material']='facebook_letter'
origin=R.facade_point(fit['baseline'],(670,144),(743,116),h0)+normal*.18
width=d.length*fit['width_pixels']/73
vector_art('Original Facebook vector wordmark',glyphs,origin,d.normalized()*width,(0,0,fit['height_pixels_per_svg_unit']/(5*cos(EL))),.24,normal)
for t in (.08,.5,.92):
 q=left.lerp(right,t);A.rod('Billboard post',(q.x,q.y,4.5),(q.x,q.y,h0),.09,'metal')

# Ground planting is an independent measured strip, not a rectangular lawn around every module.
for poly in [[[390,305],[466,270],[474,255],[450,255],[417,288]],[[481,255],[581,211],[568,207],[484,239]],[[603,209],[716,157],[704,146],[603,190]]]:
 A.part('Campus road frontage planting');R.prism('Narrow planted campus frontage',poly,.01,-.025,'facebook_lawn');foliage(poly,.015,.18)
A.COL['measurement_file']='source/facebook_measurements.json'
A.COL['inferred_details']='Back faces use the observed louver system; planting is distributed within measured beds. Historical vector wordmark and Like relief are fitted to the visible source; their extrusion, colours and fine details remain under comparison.'
A.setup_preview(47.134,26.377,1600,1000)
R.camera(3)
A.save_asset('facebook','--no-render' not in sys.argv)
