import os,sys,math,random
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from build_offices import dish,lattice
from build_campuses import ring
from math import sin,cos,pi,sqrt

def helicopter(x,y,z,s=1,color='white'):
 A.part('Helicopter • fuselage, rotor and landing skids')
 def p(a,b,c):return(x+a*s,y+b*s,z+c*s)
 A.sphere('Fuselage',p(0,0,1.2),(1.45*s,.67*s,.73*s),color,20,12)
 A.sphere('Cockpit glazing',p(-.65,-.03,1.36),(.88*s,.66*s,.56*s),'glass_blue',20,12)
 A.rod('Tail boom',p(1,0,1.32),p(4.1,0,1.83),.19*s,color,16)
 A.box('Tail fin',p(3.9,0,2.02),(.64*s,.08*s,1.35*s),color)
 A.rod('Main rotor mast',p(0,0,1.6),p(0,0,2.5),.055*s,'metal')
 for a in (pi/6,pi/6+pi/2):A.box('Long main rotor',p(0,0,2.53),(7.4*s,.16*s,.025*s),'frame',a)
 A.rod('Tail rotor hub',p(3.9,-.2,2.08),p(3.9,-.43,2.08),.035*s,'metal')
 for a in (pi/4,pi/4+pi/2):A.rod('Tail rotor blade',p(3.9-.59*cos(a),-.45,2.08-.59*sin(a)),p(3.9+.59*cos(a),-.45,2.08+.59*sin(a)),.025*s,'dark')
 for yy in (-.72,.72):
  A.rod('Landing skid',p(-1.6,yy,.12),p(1.5,yy,.12),.045*s,'metal')
  for xx in (-.75,.75):A.rod('Skid strut',p(xx,yy,.12),p(xx,yy*.55,.74),.042*s,'metal')

def roof_party(cx,cy,z,w,d,count=24):
 A.part('Timber roof terrace and hot tub')
 A.box('Terrace timber deck',(cx,cy,z+.075),(w,d,.15),'wood')
 for i in range(round(w/.16)):
  A.box('Timber deck plank seam',(cx-w/2+i*.16,cy,z+.157),(.021,d,.012),'copper')
 A.box('Hot tub stone surround',(cx-w*.31,cy-d*.20,z+.32),(2.7,2.3,.5),'frame')
 A.box('Hot tub turquoise water',(cx-w*.31,cy-d*.20,z+.58),(2.25,1.85,.03),'pool')
 for xx in (-.7,.7):
  for yy in (-.55,.55):A.sphere('Spa bubbles',(cx-w*.31+xx,cy-d*.20+yy,z+.615),(.08,.08,.03),'white')
 for j in range(11):
  x=cx-w*.45+j*w*.09;y=cy+d*.34
  A.box('Roof tree planter',(x,y,z+.27),(.95,1.2,.53),'stone');A.tree(x,y,z+.54,.65+random.random()*.3,2.2+random.random())
 for i in range(count):A.person(cx+random.uniform(-w*.05,w*.42),cy+random.uniform(-d*.40,d*.24),z+.17,random.choice(['white','red','yellow','purple','cyan','green']),random.random()*pi)
 for x in (cx-w/2,cx+w/2):A.box('Low terrace parapet',(x,cy,z+.39),(.25,d,.78),'white')
 for y in (cy-d/2,cy+d/2):A.box('Low terrace parapet',(cx,y,z+.39),(w,.25,.78),'white')

def myspace():
 A.reset('myspace','Myspace roof party and neighboring solar office',['YU11','Original wide frame'])
 A.material('myspace_band',(.21,.21,.20),.65)
 A.frame_facade(-10,0,19,20,0,13.1,5,bay=1.55,glass='glass',slab='myspace_band',mullion=.025,band=1.48)
 A.box('Main roof cornice',(-10,0,13.31),(19.7,20.7,.42),'white')
 roof_party(-10,0,13.53,19.2,20.2)
 A.part('Double height glazed entrance with steel braces')
 A.box('Entrance upper beam',(-10,-10.65,4.55),(19.0,1.3,.43),'stone')
 for i in range(7):
  x=-18.4+i*2.8
  A.rod('Entry diagonal brace',(x,-10.65,.2),(x+1.9,-10.65,4.3),.061,'metal');A.rod('Entry vertical post',(x,-10.65,0),(x,-10.65,4.35),.07,'frame')
 A.part('Historical Myspace black billboard')
 A.sign_panel('Black Myspace fascia',(-10,-10.46,10.90),19.2,3.7,'myspace_band',.32,.02)
 A.text('myspace lettering','myspace',(-8.85,-10.66,9.76),3.23,'white','regular',width=14.45,depth=.11)
 for i in range(3):
  x=-18.35+i*.79;z=11.88-i*.16
  A.sphere('Myspace icon head',(x,-10.68,z),(.28,.10,.30),'white',16,8)
  A.box('Myspace icon shoulders',(x,-10.67,z-.63),(.66,.12,.64),'white',bevel=.18)
 A.part('Cylindrical service tower')
 A.cylinder('Rounded shared stair tower',(5.75,9.22,7.4),3.1,14.8,'white',80)
 for k in range(5):A.cylinder('Cylinder blue ribbon',(5.75,9.22,2.8+k*2.7),3.116,.73,'glass_light',80)
 for i in range(56):
  t=i*2*pi/56;A.rod('Cylinder vertical panel joint',(5.75+3.13*cos(t),9.22+3.13*sin(t),0),(5.75+3.13*cos(t),9.22+3.13*sin(t),14.8),.018,'frame')
 A.part('Adjacent solar office')
 A.frame_facade(20.87,5.9,20,20,0,12.9,5,bay=1.7,glass='glass_light',slab='white',mullion=.025,band=1.57)
 A.box('Solar office broad cornice',(20.87,5.9,13.17),(20.7,20.7,.55),'white')
 A.solar(16.42,5.9,13.55,8.4,17,9,5);A.solar(25.32,5.9,13.55,8.4,17,9,5)
 return A.setup_preview(37,27,1600,1100)

def energy_pod():
 A.reset('energy_pod','EnergyPod tower and red helicopter roof',['YU11','Original wide frame'])
 A.material('pod_glass',(.12,.34,.35),.22,.1)
 A.part('Nap pod tower • curved recessed glazing')
 pts=A.rounded(0,-3,14.8,15.8,3.0,16)
 A.polygon('Rounded glass body',pts,0,23.0,'pod_glass')
 for k in range(16):
  z=.5+k*1.46;A.curve('Rounded floor rail',[(x*1.005,(y+3)*1.005-3,z) for x,y in pts],.055,'frame',True)
 for i in range(80):
  a=pts[round(i*len(pts)/80)%len(pts)];A.rod('Glass vertical frame',(a[0]*1.006,(a[1]+3)*1.006-3,0),(a[0]*1.006,(a[1]+3)*1.006-3,23),.027,'frame')
 A.part('Four projecting corner pylons')
 for x in (-6.6,6.6):
  for y in (-9.5,3.5):
   A.box('Pale structural corner',(x,y,12.25),(3.1,3.1,24.5),'white')
   for k in range(16):
    for xx in (x-.65,x+.65):A.box('Corner small window',(xx,y-1.565,.73+k*1.48),(.47,.04,.60),'glass_blue')
    for yy in (y-.65,y+.65):A.box('Corner side window',(x+1.565,yy,.73+k*1.48),(.04,.47,.60),'glass_blue')
   A.box('Green glazed tower cap',(x,y,24.75),(3.55,3.55,.40),'pod_glass')
   for k in range(9):
    A.box('Cap roof grid',(x-1.6+k*.4,y,24.965),(.026,3.3,.026),'frame');A.box('Cap cross grid',(x,y-1.6+k*.4,24.97),(3.3,.026,.026),'frame')
 A.box('Main roof platform',(0,-3,23.12),(13.1,14.2,.35),'white')
 A.part('Sculptural half-dome EnergyPod roof object')
 # A sliced ellipsoid: one pale shell and a curved glazed wedge, with explicit lattice.
 def q(t,a):return(5.05*sin(t)*cos(a),-3+5.3*sin(t)*sin(a),23.32+5.8*cos(t))
 nt,na=24,96;vs=[q(pi*j/(2*nt),2*pi*i/na) for j in range(nt+1) for i in range(na)];white=[];glass=[]
 for j in range(nt):
  for i in range(na):
   ids=(j*na+i,j*na+(i+1)%na,(j+1)*na+(i+1)%na,(j+1)*na+i)
   (glass if -pi*.18<((2*pi*(i+.5)/na+pi)%(2*pi)-pi)<pi*.29 else white).append(ids)
 A.mesh('White curved pod shell',vs,white,'white');A.mesh('Blue curved pod glazing',vs,glass,'glass')
 for i in range(17):
  a=-pi*.18+i*pi*.47/16;A.curve('Pod meridian glazing bar',[q(pi*j/(2*nt),a) for j in range(nt+1)],.022,'frame')
 for j in range(1,21):A.curve('Pod horizontal glazing bar',[q(pi*j/42,-pi*.18+i*pi*.47/40) for i in range(41)],.022,'frame')
 for i,ch in enumerate('EnergyPod'):
  xx=-3.95+i*.82;zz=25.05;yy=-3-5.3*sqrt(max(.01,1-(xx/5.05)**2-((zz-23.32)/5.8)**2))-.10
  turn=math.atan2(xx/5.05**2,-(yy+3)/5.3**2)
  A.text('EnergyPod curved letter '+str(i),ch,(xx,yy,zz-.45),1.37,'dark','regular',width=.79,rot=(pi/2,0,turn),depth=.045)
 A.part('Projecting pale pod cowl edge')
 # Visible hood overhang follows the exposed glazed sector and gives the shell its sliced profile.
 for a in (-pi*.18,pi*.29):A.curve('Pod cowl meridian edge',[q(pi*j/(2*nt),a) for j in range(nt+1)],.14,'white')
 for x in (-5.7,5.7):A.hvac(x,-1.8,23.4,1.0,1.35,.64)
 A.part('Adjacent red helipad block')
 A.frame_facade(0,14.7,15.8,17.0,0,23.05,14,bay=1.22,glass='pod_glass',slab='white',mullion=.025,band=.62)
 A.box('Helipad roof slab',(0,14.7,23.30),(16.5,17.7,.50),'white')
 A.box('Red helicopter landing surface',(0,14.7,23.575),(15.2,16.3,.055),'red')
 A.text('Large helicopter H','H',(0,11.2,23.625),8,'white','bold',width=7.0,rot=(0,0,0),depth=.015)
 helicopter(.3,15.5,23.65,.84)
 for x in (-6,6):
  for y in (7.2,22.2):A.box('Helipad raised corner parapet',(x,y,23.95),(3.2,.3,.7),'white')
 for x in (-5,0,5):A.hvac(x,21.6,23.65,1.1,.9,.6)
 return A.setup_preview(41,26,1400,1450)

def adobe():
 A.reset('adobe','Adobe stepped Art Deco tower',['YU11','Original wide frame'])
 A.surface_detail(A.material('adobe_stone',(.42,.42,.40),.67),.022)
 def wing(x,y,w,d,h):
  A.frame_facade(x,y,w,d,0,h,round(h/2.2),bay=.91,glass='glass_blue',slab='adobe_stone',mullion=.047,band=.38)
  for xx in [x-w/2+i*1.4 for i in range(round(w/1.4)+1)]:
   for yy in (y-d/2-.13,y+d/2+.13):A.box('Deep vertical stone fin',(xx,yy,h/2),(.32,.35,h),'adobe_stone')
  for yy in [y-d/2+i*1.4 for i in range(round(d/1.4)+1)]:
   for xx in (x-w/2-.13,x+w/2+.13):A.box('Vertical fin return',(xx,yy,h/2),(.35,.32,h),'adobe_stone')
  A.box('Flat setback roof',(x,y,h+.16),(w+.55,d+.55,.32),'adobe_stone')
  A.hvac(x,y,h+.32,2.2,1.5,.4)
  A.rod('Setback roof vent riser',(x+w*.25,y+d*.25,h+.32),(x+w*.25,y+d*.25,h+1.1),.10,'frame')
 wing(0,0,33,15.5,24)
 for x,w,h in [(-13.75,5.5,29.0),(-8.25,5.5,35.2),(-2.1,6.8,42),(7.975,13.35,49.3)]:wing(x,0,w,13.8,h)
 A.part('Oversized Adobe red end wall')
 o=A.sign_panel('Red Adobe branded end',(14.82,0,37.35),13.8,23.8,'red',.30,.015);o.rotation_euler=(pi/2,0,pi/2)
 # Adobe 1993 mark: paired tapering strokes and the lower internal triangle.
 for pts in [[(-4.5,-4.1),(-.90,4.5),(-4.5,4.5)],[(.25,4.5),(4.3,-4.1),(4.3,4.5)],[(-1.5,-2.55),(.02,1.32),(2.56,-4.1),(.79,-4.1),(.16,-2.55)]]:
  ob=A.polygon('Adobe geometric A stroke',pts,0,.16,'white',False);ob.rotation_euler=(pi/2,0,pi/2);ob.location=(15.01,0,39.9)
 A.text('Adobe wordmark','Adobe',(15.03,0,28.90),3.85,'white','regular',width=10.6,rot=(pi/2,0,pi/2),depth=.10)
 A.COL['inferred_details']='Setback silhouette, fins and end signage fitted to YU11; rear elevations inferred.'
 return A.setup_preview(46,24,1500,1450)

def hp():
 A.reset('hp','HP office slab with raised helipad',['YU18','Original wide frame'])
 A.frame_facade(-4.5,0,32,18,0,17.6,8,bay=1.36,glass='glass_blue',slab='cream',mullion=.065,band=.44)
 A.box('Long office roof',(-4.5,0,17.88),(32.7,18.7,.55),'cream')
 A.frame_facade(16,1.2,10.5,15.6,0,23.0,10,bay=1.36,glass='glass_blue',slab='cream',mullion=.065,band=.44)
 A.box('Raised east roof',(16,1.2,23.25),(11.3,16.4,.5),'cream')
 A.part('Circular raised helipad')
 ring('Helipad white circle',16,1.2,4.6,4.39,23.54,.055,'white',96)
 A.text('HP roof landing H','H',(16,-.8,23.58),5.0,'white','bold',width=4.1,rot=(0,0,0),depth=.02)
 A.part('Blue rooftop plant')
 for x in (-13,-6,1):
  A.box('Blue raised roof skylight',(x,3.7,18.57),(4.7,3.2,.80),'cyan')
  A.box('Skylight pale frame',(x,3.7,19.0),(5.0,3.5,.13),'frame')
  A.box('Skylight pane',(x,3.7,19.08),(4.3,2.8,.05),'glass_light')
 for j in range(5):A.box('Blue long roof pipe',(-5,-3.8+j*.48,18.4),(15,.2,.28),'cyan')
 lattice(-16.5,3,18.15,3,'cyan');helicopter(-9,-.7,18.20,.75,'yellow')
 for x in (-13,-6,1):
  for y in (2.15,5.25):A.rod('Skylight support frame',(x-2.2,y,18.2),(x+2.2,y,18.2),.065,'metal')
 A.part('HP circular roof-front sign')
 ob=A.polygon('White HP roundel',[(3*cos(i*2*pi/96),3*sin(i*2*pi/96)) for i in range(96)],-.11,.22,'white',False);ob.rotation_euler=(pi/2,0,0);ob.location=(5,-9.44,16.4)
 t=A.text('hp letters','hp',(5,-9.60,14.6),5.45,'cyan','regular',width=4.5,depth=.12);t.data.shear=.18
 return A.setup_preview(40,28,1500,1100)

def historic_apple():
 A.reset('historic_apple','Historic Apple masonry block and Pets.com sign',['YU09','Original wide frame'])
 A.part('Turquoise masonry block')
 A.box('Historic office envelope',(0,0,5.1),(13.0,12.6,10.2),'turquoise')
 A.box('Bright recessed flat roof',(0,0,10.23),(11.9,11.5,.18),'white')
 for x in (-6.35,6.35):A.box('Stepped side parapet',(x,0,10.54),(.31,12.6,.78),'turquoise')
 for y in (-6.15,6.15):
  A.box('Main parapet',(0,y,10.48),(13,.31,.65),'turquoise')
  for x,w,h in [(-4.6,2.8,.35),(0,4.6,.85),(4.6,2.8,.35)]:A.box('Stepped parapet rise',(x,y,10.8+h/2),(w,.31,h),'turquoise')
 A.part('Square upper windows and arched ground openings')
 for k in range(2):
  for i in range(5):
   x=-5.1+i*2.55;z=5.1+k*2.5
   for y in (-6.317,6.317):A.box('Upper masonry inset',(x,y,z),(1.1,.04,1.32),'glass')
   for xx in (-6.517,6.517):A.box('Side upper inset',(xx,x,z),(.04,1.1,1.32),'glass')
 for i in range(5):
  c=-5.1+i*2.55;pts=[(c-.57,0),(c+.57,0),(c+.57,2.72)]+[(c+.57*cos(pi*j/24),2.72+.57*sin(pi*j/24)) for j in range(25)]
  ob=A.polygon('Ground floor arched opening',pts,0,.055,'dark',False);ob.location=(0,-6.34,.05);ob.rotation_euler=(pi/2,0,0)
  ob=A.polygon('Side ground floor arch',pts,0,.055,'dark',False);ob.location=(6.54,0,.05);ob.rotation_euler=(pi/2,0,pi/2)
 A.part('Window reveals and partially open awning panes')
 for k in range(2):
  for i in range(5):
   x=-5.1+i*2.55;z=5.1+k*2.5
   A.box('Deep window sill',(x,-6.43,z-.68),(1.27,.27,.12),'turquoise')
   A.box('Dark inner glazing',(x,-6.355,z),(.90,.06,1.12),'dark')
   if (i+k)%3==0:
    o=A.box('Partly opened projecting window',(x,-6.53,z+.04),(.90,.055,1.05),'glass',batch=False);o.rotation_euler.x=-.28
 A.part('Historical rainbow Apple facade sculpture')
 A.logo('apple',(-2.9,-6.51,6.2),8.3,.52,rot=(pi/2,0,0),rainbow=True)
 A.part('Pets.com rooftop sign')
 for x in (-3.7,3.7):A.rod('Sign support pole',(x,0,10.3),(x,0,14.0),.15,'metal');A.cylinder('Sign foot',(x,0,10.65),.42,1.25,'metal',24)
 A.sign_panel('Pets.com green edge',(0,-.03,14.8),12.1,3.5,'green',.26,1.35)
 A.sign_panel('Pets.com white inset',(0,-.18,14.8),11.7,3.13,'white',.12,1.18)
 A.text('pets.com lettering','pets.com',(1,-.30,13.87),2.0,'green','black',width=8.3,depth=.06)
 A.sphere('Pets paw pad',(-4.65,-.30,14.45),(.44,.08,.37),'dark')
 for x,z in [(-5.25,14.97),(-4.88,15.29),(-4.39,15.3),(-4.07,14.97)]:A.sphere('Paw toe',(x,-.30,z),(.20,.075,.23),'dark')
 return A.setup_preview(41,25,1400,1250)

def paypal():
 A.reset('paypal','PayPal pale chamfered office',['YU09','Original wide frame'])
 A.part('Chamfered office envelope')
 pts=[(-8.5,-7),(-5.9,-9.5),(5.9,-9.5),(8.5,-7),(8.5,6.9),(5.9,9.2),(-5.9,9.2),(-8.5,6.9)]
 A.polygon('Eight-sided office',pts,0,7.6,'cream');A.polygon('Chamfered roof slab',[(x*1.055,y*1.055) for x,y in pts],7.6,.38,'white')
 for z in (2.0,5.1):
  for x in (-8.52,8.52):A.box('Yellow horizontal side recess',(x,0,z),(.06,10.7,.54),'yellow')
  for y in (-9.52,9.22):A.box('Yellow horizontal front recess',(0,y,z),(9.8,.06,.54),'yellow')
 A.part('Broad recessed horizontal facade courses')
 for z in (1.18,3.32,5.44):
  for a,b in zip(pts,pts[1:]+pts[:1]):
   aa=(a[0]*1.001,a[1]*1.001);bb=(b[0]*1.001,b[1]*1.001)
   A.mesh('Pale projecting masonry belt',[(aa[0],aa[1],z),(bb[0],bb[1],z),(bb[0],bb[1],z+.34),(aa[0],aa[1],z+.34)],[(0,1,2,3)],'stone')
 A.part('Raised PayPal lettering and roof vents')
 A.text('PayPal roof letters','PayPal',(0,-2.5,8.04),3.4,'glass_blue','bold',width=13.6,rot=(0,0,0),depth=.20)
 for x,y in [(-5,4.2),(5.1,4.2),(-5.0,-5.5),(5.0,-5.5)]:A.hvac(x,y,8.0,2.6,2.2,1.35)
 A.cylinder('Yellow round roof vent',(-3.3,5.1,8.48),.85,.85,'yellow',40)
 return A.setup_preview(38,31,1400,1100)

BUILDERS={'myspace':myspace,'energy_pod':energy_pod,'adobe':adobe,'hp':hp,'historic_apple':historic_apple,'paypal':paypal}
if __name__=='__main__':
 ids=sys.argv[sys.argv.index('--assets')+1:] if '--assets' in sys.argv else list(BUILDERS)
 for asset in ids:BUILDERS[asset]();A.save_asset(asset)
