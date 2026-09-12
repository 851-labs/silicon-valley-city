import os,sys,math,random
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from math import sin,cos,pi,atan2
from mathutils import Vector

def dish(x,y,z,r=.7,color='copper'):
 A.part('Roof aerials and dishes');vs=[];n=32
 for k in range(7):
  rr=r*k/6
  for i in range(n):vs.append((x+rr*cos(2*pi*i/n),y+rr*.4*sin(2*pi*i/n),z+rr*.85*sin(2*pi*i/n)+(rr/r)**2*.22))
 fs=[]
 for k in range(6):
  for i in range(n):a=k*n+i;b=k*n+(i+1)%n;fs.append((a,b,b+n,a+n))
 A.mesh('Parabolic satellite dish',vs,fs,color);A.rod('Dish mast',(x,y,z-r),(x,y,z),.05,'metal');A.rod('Dish feed arm',(x,y-.7,z),(x,y-.25,z+.08),.025,'metal')

def lattice(x,y,z,h=5,color='copper'):
 A.part('Lattice rooftop mast')
 for i in range(4):
  a=i*pi/2+pi/4
  A.rod('Tapered mast leg',(x+.65*cos(a),y+.65*sin(a),z),(x+.25*cos(a),y+.25*sin(a),z+h),.038,color)
 for k in range(8):
  z0=z+k*h/8;z1=z+(k+1)*h/8;r0=.65-.4*k/8;r1=.65-.4*(k+1)/8
  for i in range(4):
   a=i*pi/2+pi/4;b=(i+1)*pi/2+pi/4
   A.rod('Mast crossed brace',(x+r0*cos(a),y+r0*sin(a),z0),(x+r1*cos(b),y+r1*sin(b),z1),.020,color)
   A.rod('Mast crossed brace',(x+r0*cos(b),y+r0*sin(b),z0),(x+r1*cos(a),y+r1*sin(a),z1),.020,color)

def roof_frame(x,y,z,w,d):
 A.part('Copper roof equipment frames')
 for yy in (y-d/2,y+d/2):A.box('Copper perimeter frame',(x,yy,z+.18),(w,.35,.36),'copper')
 for xx in (x-w/2,x+w/2):A.box('Copper perimeter frame',(xx,y,z+.18),(.35,d,.36),'copper')
 for i in range(1,4):
  yy=y-d/2+i*d/4;A.box('Mechanical cross frame',(x,yy,z+.18),(w,.32,.36),'copper')
 A.box('Roof duct box',(x+.3,y+d*.32,z+.48),(1.4,1.2,.96),'copper')
 A.rod('Mechanical conduit',(x-w*.25,y-d*.25,z+.13),(x+w*.23,y-d*.25,z+.13),.14,'copper')
 dish(x,y,z+.68,.55)

def facebook():
 A.reset('facebook','Facebook branching campus',['YU15','YU16','YU02'])
 A.material('facebook_glass',(.015,.16,.25),.22,.15)
 def H(cx,cy,w=24,d=21,stem=8,bridge=5,h=6.5):
  a=w/2;b=d/2;i=a-stem;j=bridge/2
  coords=[(-a,-b),(-i,-b),(-i,-j),(i,-j),(i,-b),(a,-b),(a,b),(i,b),(i,j),(-i,j),(-i,b),(-a,b)]
  pts=[(cx+x,cy+y) for x,y in coords]
  A.part('H campus module • glazed structure');A.polygon('H-shaped glazed envelope',pts,0,h,'facebook_glass')
  for aa,bb in zip(pts,pts[1:]+pts[:1]):
   v=Vector(bb)-Vector(aa);L=v.length;t=v/L;n=Vector((t.y,-t.x));c=(Vector(aa)+Vector(bb))/2+n*.055;angle=atan2(t.y,t.x)
   for k in range(1,8):A.box('Cream facade horizontal rail',(c.x,c.y,k*h/7),(L,.12,.11),'cream',angle)
   for k in range(round(L/1.65)+1):
    q=Vector(aa)+t*min(L,k*1.65)+n*.080;A.box('Tall slender facade mullion',(q.x,q.y,h/2),(.065,.15,h),'cream',angle)
  A.part('H campus module • sloping roof')
  inset=1.22;ii=i+inset;aa=a-inset;bb=b-inset;jj=j-inset
  inner=[(-aa,-bb),(-ii,-bb),(-ii,-jj),(ii,-jj),(ii,-bb),(aa,-bb),(aa,bb),(ii,bb),(ii,jj),(-ii,jj),(-ii,bb),(-aa,bb)]
  inner=[(cx+x,cy+y) for x,y in inner]
  vs=[(x,y,h) for x,y in pts]+[(x,y,h+.92) for x,y in inner];N=len(pts)
  A.mesh('Broad hipped roof border',vs,[(k,(k+1)%N,(k+1)%N+N,k+N) for k in range(N)],'cream')
  A.polygon('Inset flat rooftop',inner,h+.92,.04,'cream')
  for x in (cx-a+stem/2,cx+a-stem/2):roof_frame(x,cy,h+.97,3.9,d-6)
  return h+.98
 # Four linked modules, with a small offset to avoid coincident connector faces.
 for x,y,h in [(-13,-23,6.5),(13,-1.5,6.52),(-13,20.0,6.54),(13,41.5,6.56)]:
  H(x,y,h=h)
 for y in (-12.25,9.25,30.75):
  A.frame_facade(0,y,2.2,4.0,0,4.7,3,bay=1.0,glass='facebook_glass',slab='cream',mullion=.04,band=.14)
  A.box('Campus connecting bridge roof',(0,y,4.85),(2.45,4.2,.3),'cream')
 A.part('Campus planted strips')
 for x,y,w,d in [(-13,-23,27,24),(13,-1.5,27,24),(-13,20,27,24),(13,41.5,27,24)]:
  A.box('Lawn plot',(x,y,-.055),(w,d,.10),'grass')
  for xx in (x-w/2+.8,x+w/2-.8):
   for i in range(7):A.tree(xx,y-d/2+1+i*(d-2)/6,0,.72,2.8)
 A.part('Facebook main roof sign')
 A.sign_panel('Facebook blue backing',(-8,18.7,11.8),33,6.7,'facebook',.35,.12)
 A.text('Facebook white lettering','facebook',(-8,18.47,9.6),6.1,'white','bold',width=30.7,depth=.07)
 for x in (-19,-8,3):A.rod('Main sign support',(x,18.8,7.5),(x,18.8,9),.085,'metal')
 A.part('Rear roof garden annex')
 A.frame_facade(-21,44,17,17,0,4.5,3,bay=2.8,glass='facebook_glass',slab='cream',mullion=.08,band=.19)
 A.box('Garden roof rim',(-21,44,4.68),(17.5,17.5,.4),'cream');A.box('Roof garden soil',(-21,44,4.91),(15.8,15.8,.1),'grass')
 for i in range(24):A.tree(-27+random.random()*12,38+random.random()*12,4.97,.55,1.8)
 A.COL['inferred_details']='Module arrangement is fitted to the campus views. Rear roof garden and invisible service connections require final city-view comparison.'
 return A.setup_preview(38,30,1600,1250)

def ebay():
 A.reset('ebay','eBay two-storey warehouse',['YU24','YU16','YU02'])
 A.part('Warehouse shell and punched windows')
 A.box('Two-storey pale envelope',(0,0,3.25),(32,21,6.5),'white')
 for k in range(2):
  z=1.62+k*3.0
  for i in range(11):
   x=-14.5+i*2.9
   for side in (-1,1):
    if side==-1 and abs(x+3)<1.7 and k==0:continue
    A.box('Recessed blue window',(x,side*10.518,z),(1.66,.04,2.03),'glass_blue')
    A.box('Window bottom sill',(x,side*10.56,z-1.04),(1.78,.12,.07),'frame')
  for i in range(7):
   y=-9+i*3.0
   for side in (-1,1):A.box('Side window',(side*16.018,y,z),(.04,1.54,2.03),'glass_blue')
 A.box('Glazed entrance doors',(-3,-10.54,1.50),(3.1,.08,3.0),'glass_blue')
 A.box('Entrance ramp',(-3,-11.6,.12),(3.8,2.4,.24),'roof')
 A.part('Curved entrance canopy')
 pts=[(-3+2.35*cos(pi*i/32),-10.9-2.35*sin(pi*i/32)) for i in range(33)];A.polygon('Semicircular entry awning',pts,3.38,.37,'white')
 A.part('Stepped cornice and roof')
 A.box('Wide roof cornice',(0,0,6.75),(32.9,21.9,.45),'cream')
 A.box('Upper roof lip',(0,0,7.1),(33.35,22.35,.26),'white')
 A.box('Dark roof membrane',(0,0,7.245),(32.7,21.7,.035),'roof')
 for x in (-16.62,16.62):A.box('Roof parapet side',(x,0,7.45),(.20,22.35,.47),'white')
 for y in (-11.08,11.08):A.box('Roof parapet front',(0,y,7.45),(33.35,.20,.47),'white')
 # The original arrays leave an angular equipment corridor through a near-continuous field.
 for x in (-12.6,-8.1,-3.6,.9,5.4,9.9,14.0):
  for y in (-7.0,6.8):A.solar(x,y,7.31,3.8,6.4,4,3,tilt=11)
 for x in (-13.1,12.9):A.solar(x,0,7.31,3.6,5.9,4,3,tilt=11)
 # Bent copper ducts, discrete raised boxes and a narrow open mast.
 A.part('Angular copper rooftop services')
 path=[(-8.4,3.1),(-8.4,-.1),(-3.2,-.1),(-3.2,-2.5),(7.8,-2.5),(7.8,1.5),(2.9,1.5),(2.9,3.1),(-8.4,3.1)]
 for a,b in zip(path,path[1:]):A.rod('Rectangular copper duct run',(a[0],a[1],7.65),(b[0],b[1],7.65),.23,'copper',4)
 for x,y in [(6.2,-.9),(3.5,-1.0),(-5.8,1.4)]:A.box('Copper equipment enclosure',(x,y,7.72),(1.65,1.3,.68),'copper')
 lattice(-8.4,3.1,7.3,7.2);dish(-8.1,1.8,8.7,.62)
 A.part('Raised multicolored lowercase eBay sign')
 A.colorword('ebay',(4.4,-11.24,4.45),24.0,10.0,'regular',depth=.31)
 A.COL['variant']='Season 1 warehouse and current-at-the-time lowercase eBay wordmark; no later LED facade.'
 return A.setup_preview(31,23,1500,1100)

def intel():
 A.reset('intel','Intel stepped blue and cream campus',['YU09','YU16','YU02'])
 blocks=[(-7,-6,14,14,6.6),(6.9,4.6,13.4,18.0,9.0),(-7,7.9,14,10.3,9.02)]
 for i,(x,y,w,d,h) in enumerate(blocks):
  A.part('Intel wing '+str(i+1))
  A.frame_facade(x,y,w,d,0,h,3 if h<8 else 4,bay=2.5,glass='glass_blue',slab='cream',mullion=.021,band=.99)
  A.box('Oversailing roof slab',(x,y,h+.19),(w+.60,d+.6,.38),'cream')
  A.box('Blue rooftop volume',(x,y,h+1.335),(w*.69,d*.60,1.90),'cyan')
  A.box('Rooftop volume cap',(x,y,h+2.33),(w*.72,d*.63,.13),'cream')
 A.part('Intel raised roof logo')
 z=9.07
 A.text('intel roof letters','intel',(-7,-7.3,z),3.25,'cyan','bold',width=9.2,rot=(0,0,0),depth=.08)
 pts=[(-7+5.95*cos(t),-6.0+3.32*sin(t),z+.02) for t in [(.16+i*1.83*pi/100) for i in range(101)]]
 A.curve('Intel elliptical swoosh',pts,.16,'cyan')
 A.part('Small entry steps')
 for i in range(3):A.box('Wide shallow entrance step',(-7,-13.5-i*.40,.12+i*.13),(8.0,1.25,.24),'cream')
 for x,y in [(-15,-11),(-15,-7),(-15,-3)]:A.tree(x,y,0,.85,3.6)
 return A.setup_preview(36,31,1300,1100)

def yahoo_oracle():
 A.reset('yahoo_oracle','Yahoo and Oracle paired office slabs',['YU26','YU18','YU16'])
 def block(name,x,y,w,d,h):
  A.part(name+' • glazed floors');A.frame_facade(x,y,w,d,0,h,4,bay=.95,glass='glass_light',slab='frame',mullion=.027,band=.10)
  A.part(name+' • broad corrugated spandrels')
  for k in range(1,5):
   z=k*h/4-.40
   for yy in (y-d/2-.07,y+d/2+.07):
    A.box('White floor band',(x,yy,z),(w+.18,.17,1.20),'white')
    for i in range(round(w/.48)):
     xx=x-w/2+(i+.5)*w/round(w/.48);A.box('Slightly raised facade flute',(xx,yy+(0.03 if yy>y else -.03),z),(.24,.14,1.17),'frame')
   for xx in (x-w/2-.07,x+w/2+.07):
    A.box('White floor band return',(xx,y,z),(.17,d,1.2),'white')
    for i in range(round(d/.48)):
     yy=y-d/2+(i+.5)*d/round(d/.48);A.box('Raised band flute',(xx+(0.03 if xx>x else -.03),yy,z),(.14,.24,1.17),'frame')
  A.box('Roof slab',(x,y,h+.18),(w+.6,d+.6,.36),'white')
  for yy in (y-d/2,y+d/2):A.box('Rooftop parapet',(x,yy,h+.80),(w,.3,1.2),'white')
  for xx in (x-w/2,x+w/2):A.box('Rooftop parapet return',(xx,y,h+.80),(.3,d,1.2),'white')
 block('Yahoo',-12.5,1.2,16.2,16.3,12.2);block('Oracle',10.8,-1.4,19.0,17.3,12.3)
 A.part('Cylindrical shared service core')
 A.cylinder('Cream circular stair tower',(-1.9,7.8,6.8),3.2,13.6,'white',72)
 for z in (3.0,7.0,11.0):A.cylinder('Cylindrical ribbon window',(-1.9,7.8,z),3.215,.70,'glass_light',72)
 for i in range(48):
  t=2*pi*i/48;x=-1.9+3.235*cos(t);y=7.8+3.235*sin(t);A.rod('Cylinder facade mullion',(x,y,0),(x,y,13.6),.027,'frame')
 A.part('Oracle logo plaque')
 A.sign_panel('Oracle white sign',(10.8,-10.25,10.44),16.1,3.0,'white',.20,.02);A.text('Oracle red lettering','ORACLE',(10.8,-10.40,9.56),2.35,'red','regular',width=14.9,depth=.045)
 A.part('Yahoo historical roof roundel')
 A.cylinder('Purple Yahoo roof roundel',(-12.5,1.2,12.72),4.7,.28,'purple',96)
 A.text('Yahoo Y exclamation','Y!',(-12.5,-.8,12.92),5.5,'white','serif',width=5.8,rot=(0,0,0),depth=.06)
 A.part('Oracle photovoltaic roof')
 A.solar(10.8,-1.4,12.76,16.0,14.4,8,10)
 A.COL['variant']='Original wide frame: Yahoo roof roundel and adjacent solar roof. Alibaba billboard and later climbing-wall gag omitted.'
 return A.setup_preview(37,25,1600,1150)

BUILDERS={'facebook':facebook,'ebay':ebay,'intel':intel,'yahoo_oracle':yahoo_oracle}
if __name__=='__main__':
 ids=sys.argv[sys.argv.index('--assets')+1:] if '--assets' in sys.argv else list(BUILDERS)
 for asset in ids:BUILDERS[asset]();A.save_asset(asset)
