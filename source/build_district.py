import os,sys,math,random
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from build_campuses import ring
from build_landmarks import roof_party,helicopter
from math import sin,cos,pi

def linkedin():
 A.reset('linkedin','LinkedIn stepped corner office',['Original wide frame','YU16'])
 for i,(x,y,w,d,h) in enumerate([(0,0,19,17,2.8),(-2,1.0,16,14,5.6),(-4,1.8,13,12,8.4)]):
  A.frame_facade(x,y,w,d,max(0,h-2.8),2.8,1,bay=1.16,glass='glass',slab='white',mullion=.043,band=.34)
  A.box('Terraced projecting slab',(x,y,h+.2),(w+1.0,d+1.0,.4),'white')
  A.box('Brick setback wall',(x,y+d/2,h-1.15),(w,.14,1.4),'copper')
 A.solar(-5.2,1.8,8.88,7.8,8.2,5,5)
 for x,y,w,d,h in [(0,0,19,17,2.8),(-2,1,16,14,5.6),(-4,1.8,13,12,8.4)]:
  A.part('Stepped pale parapets')
  for yy in (y-d/2-.25,y+d/2+.25):A.box('Broad solid terrace parapet',(x,yy,h+.36),(w+.8,.48,.67),'cream')
  for xx in (x-w/2-.25,x+w/2+.25):A.box('Terrace parapet return',(xx,y,h+.36),(.48,d+.8,.67),'cream')
 A.hvac(.2,4.8,8.88,1.8,1.3,.6)
 A.part('LinkedIn raised roof wordmark')
 A.text('LinkedIn dark letters','Linked',(-1,-5.4,6.1),2.05,'dark','bold',width=7.9,rot=(0,0,0),depth=.15)
 A.box('LinkedIn blue square',(5,-4.8,6.05),(2.5,2.5,.25),'blue')
 A.text('LinkedIn white in','in',(5,-5.65,6.21),2.1,'white','bold',width=1.9,rot=(0,0,0),depth=.06)
 return A.setup_preview(38,30,1400,1100)

def zynga():
 A.reset('zynga','Zynga stepped studio and roof party',['Original wide frame','YU16'])
 A.material('zynga_concrete',(.43,.45,.42),.7)
 def block(x,y,w,d,h):
  A.box('Concrete stepped block',(x,y,h/2),(w,d,h),'zynga_concrete')
  for zz in [1.65+i*3.5 for i in range(round(h/3.5))]:
   for side in (-1,1):
    for i in range(round(w/3.6)):
     xx=x-w/2+(i+.5)*w/round(w/3.6);A.box('Pale framed studio window',(xx,y+side*(d/2+.025),zz),(2.36,.22,2.27),'cream');A.box('Colored studio glass',(xx,y+side*(d/2+.142),zz),(1.65,.035,1.70),random.choice(['glass','glass_light','glass_light','glass_blue','glass_light','yellow']))
    for i in range(round(d/3.6)):
     yy=y-d/2+(i+.5)*d/round(d/3.6);A.box('Side pale window frame',(x+side*(w/2+.025),yy,zz),(.22,2.36,2.27),'cream');A.box('Side colored pane',(x+side*(w/2+.142),yy,zz),(.035,1.65,1.70),random.choice(['glass','glass_light','glass_light','glass_blue','glass_light','yellow']))
  A.box('Overhanging roof slab',(x,y,h+.15),(w+.65,d+.65,.30),'cream')
 block(-5,0,15,13,7);block(-7,1.7,10,9.6,14);block(10,4,13,12,7);block(11,6.2,9,8,10.5)
 roof_party(-7,1.7,14.32,10,9.6,15)
 A.part('Red Zynga sign cube')
 A.box('Zynga red sign',(8.5,-.75,9.32),(3.9,1.55,4.0),'red',bevel=.10)
 A.text('Zynga vertical wordmark','zynga',(8.5,-1.58,7.64),.95,'white','regular',width=3.2,depth=.045)
 # Dog silhouette on the old sign: torso, tail, muzzle and four legs.
 pts=[(-1.15,-.5),(-.95,.5),(-.28,.62),(.0,1.18),(.55,1.08),(.58,.67),(1.08,.54),(.95,.23),(.48,.22),(.36,-.66),(.12,-.66),(.0,-.1),(-.44,-.1),(-.66,-.68),(-.86,-.68),(-.77,-.06),(-1.19,-.14),(-1.45,.24),(-1.56,.78),(-1.40,.79),(-1.22,.22)]
 ob=A.polygon('Zynga dog silhouette',pts,0,.055,'white',False);ob.rotation_euler=(pi/2,0,0);ob.location=(8.5,-1.58,9.86)
 return A.setup_preview(39,29,1400,1200)

def terrace_office():
 A.reset('terrace_office','Terraced solar office module',['Original wide frame • southeast rows'])
 A.material('terrace_brick',(.42,.17,.095),.7)
 for k in range(3):
  w=14.4-k*1.0;d=12.2-k*.8;z=k*2.55
  A.frame_facade(0,0,w,d,z,2.55,1,bay=1.08,glass='glass',slab='white',mullion=.04,band=.2)
  for y in (-d/2-.11,d/2+.11):A.box('Terracotta ribbon',(0,y,z+.52),(w,.22,.75),'terrace_brick')
  for x in (-w/2-.11,w/2+.11):A.box('Terracotta ribbon return',(x,0,z+.52),(.22,d,.75),'terrace_brick')
  A.box('Stepped white floor plate',(0,0,z+2.64),(w+1.25,d+1.25,.46),'white')
 A.solar(-1.55,.65,7.92,7.9,6.7,4,5)
 A.solar(3.5,1.8,7.92,1.45,4.3,3,1)
 A.hvac(3.8,-2.9,7.94,1.6,1.25,.61)
 for x in (-5.8,5.8):A.box('Roof side parapet',(x,0,8.14),(.18,10.6,.49),'white')
 for y in (-5.3,5.3):A.box('Roof end parapet',(0,y,8.14),(11.6,.18,.49),'white')
 return A.setup_preview(38,28,1200,1000)

def security_tower():
 A.reset('security_tower','Security tower on armored plinth',['YU11','Original wide frame'])
 A.part('Flared armored service plinth')
 for side in (-1,1):
  A.mesh('Sloping armored front panel',[(-5.5,side*5.1,0),(5.5,side*5.1,0),(4,side*3.6,4.4),(-4,side*3.6,4.4)],[(0,1,2,3)],'roof')
  A.mesh('Sloping armored side panel',[(side*5.5,-5.1,0),(side*5.5,5.1,0),(side*4,3.6,4.4),(side*4,-3.6,4.4)],[(0,1,2,3)],'roof')
 A.box('Armored upper deck',(0,0,4.47),(8.2,7.4,.30),'roof')
 for x in (-3.8,3.8):
  for y in (-4.65,4.65):
   for z in (.9,2.7):A.sphere('Large armored bolt',(x,y,z),(.12,.08,.12),'frame',10,6)
 A.frame_facade(0,0,7.2,6.8,4.6,11.2,4,bay=3.4,glass='glass_blue',slab='cream',mullion=.21,band=1.26)
 A.box('Control tower roof',(0,0,16.02),(7.9,7.5,.43),'white')
 A.cylinder('Round mechanical hatch',(0,-4.2,4.67),.66,.1,'metal',48)
 A.hvac(2,2.9,4.65,1.0,.8,.8)
 for x in (-3.6,0,3.6):
  A.rod('Armored front panel seam',(x,-5.11,.05),(x*.72,-3.62,4.37),.045,'frame',4)
 for y in (-3.3,0,3.3):A.rod('Armored side panel seam',(5.51,y,.05),(4.02,y*.72,4.37),.045,'frame',4)
 A.box('Small plinth access door',(0,-4.92,1.25),(1.55,.08,2.2),'roof')
 return A.setup_preview(40,27,1200,1400)

def stadium():
 A.reset('stadium','Western open stadium with deep seating bowl',['Original wide frame'])
 A.material('stadium_seats',(.37,.31,.22),.82)
 def oval(r,ratio,z):return[(r*cos(i*2*pi/160),r*ratio*sin(i*2*pi/160),z) for i in range(160)]
 def annulus(name,r0,r1,z0,z1,mat):
  vs=oval(r0,.70,z0)+oval(r1,.70,z1)
  A.mesh(name,vs,[(i,(i+1)%160,(i+1)%160+160,i+160) for i in range(160)],mat)
 A.part('Open structural bowl')
 annulus('Tapered outer stadium wall',23.0,23.5,0,10.8,'cream')
 for k in range(4):
  z=1.6+k*2.55;annulus('Broad exterior concourse band',23.42,23.42,z,z+.57,'roof')
 A.polygon('Sunken playing field',[(x,y) for x,y,z in oval(10.3,.70,0)],.30,.10,'grass')
 A.part('Twenty-two stepped seating terraces')
 for k in range(22):
  r=10.2+k*.42;z=.6+k*.44
  annulus('Seating tread',r,r+.43,z,z,'stadium_seats')
  annulus('Vertical seating riser',r+.43,r+.43,z,z+.44,'stone')
 for i in range(24):
  a=i*pi/12
  for k in range(22):
   r=10.4+k*.42;A.box('Radial aisle step',(r*cos(a),r*.70*sin(a),.63+k*.44),(.5,.57,.07),'cream',a)
 A.part('White tensile roof with open elliptical center')
 annulus('Pale segmented roof',23.5,17.5,13.8,13.63,'white')
 for r in (23.5,17.5):A.curve('Roof edge fascia',oval(r,.70,13.72),.16,'cream',True)
 for i in range(48):
  t=i*2*pi/48;p=(23.4*cos(t),16.38*sin(t));q=(17.5*cos(t),12.25*sin(t))
  A.rod('Exterior structural column',(*p,0),(*p,13.8),.15,'frame')
  A.rod('Roof sloping truss',(*p,10.4),(*q,13.63),.10,'frame')
  A.rod('Roof radial upper chord',(*p,13.8),(*q,13.63),.07,'frame')
  for j in range(4):
   a=j/4;b=(j+1)/4
   p0=(p[0]*(1-a)+q[0]*a,p[1]*(1-a)+q[1]*a,10.4+3.23*a)
   p1=(p[0]*(1-b)+q[0]*b,p[1]*(1-b)+q[1]*b,13.8-.17*b)
   A.rod('Triangulated roof web',p0,p1,.05,'frame')
 return A.setup_preview(47.134,26.377,1500,1050)

def framing_tower():
 A.reset('framing_tower','Western tall framed office tower',['Original wide frame'])
 A.material('tower_stone',(.41,.42,.38),.65)
 A.frame_facade(0,0,13,16,0,39,19,bay=1.15,glass='glass',slab='tower_stone',mullion=.10,band=.30)
 for x in (-6.55,6.55):
  for y in (-6,0,6):A.box('Projected side pier',(x,y,21.0),(.50,.42,42),'tower_stone')
 for x in (-4.9,0,4.9):
  A.box('Tall front pier',(x,-8.3,21.8),(.52,.50,43.6),'tower_stone')
  A.box('Tall rear pier',(x,8.3,21.8),(.52,.50,43.6),'tower_stone')
 A.box('Setback upper glass volume',(0,0,42),(10.4,13.6,6),'glass_light')
 A.box('Stepped upper cornice',(0,0,45.25),(11.2,14.3,.5),'tower_stone')
 A.hvac(0,0,45.52,3,3,1.2)
 for x in (-4.4,4.4):
  for j in range(8):A.box('Upper mechanical louvre',(x,-3.0+j*.8,45.97),(.08,.55,.7),'tower_stone')
 return A.setup_preview(40,26,1200,1500)

def legacy_hp():
 A.reset('legacy_hp','Hewlett Packard foreground slab towers',['Original wide frame'])
 for x,y,w,d,h in [(-12,0,13,16,30),(1,1,12.6,16,30.03),(13,4,11.6,16,30.06),(-6,-6,7,7,25.5),(7,-3,7,7,25.53),(20,6,6.3,7,25.56)]:
  A.frame_facade(x,y,w,d,0,h,round(h/2),bay=.92,glass='glass_blue',slab='cream',mullion=.035,band=.18)
  A.box('Pale flat tower roof',(x,y,h+.2),(w+.22,d+.22,.4),'cream')
  A.hvac(x,y,h+.45,1.25,1,.45)
 A.part('Historical rooftop HP branding')
 ring('HP dark roof circle',-13,3,3.2,2.96,30.30,.18,'dark',80)
 A.text('Roof hp monogram','hp',(-13,1.4,30.49),3.3,'dark','regular',width=4,rot=(0,0,0),depth=.15)
 A.text('Hewlett name','HEWLETT',(2,4.0,30.51),2.75,'dark','bold',width=19,rot=(0,0,0),depth=.35)
 A.text('Packard name','PACKARD',(2,.4,30.52),2.75,'dark','bold',width=19,rot=(0,0,0),depth=.35)
 return A.setup_preview(40,29,1550,1250)

def small_offices():
 A.reset('small_offices','Western service offices and helipad connector',['Original wide frame','YU09'])
 A.part('Open lower storey and gabled upper office')
 # This is a two-level structure; the gabled glass room overhangs an open ground level.
 A.box('Lower service core',(0,2.6,1.55),(7.7,2.5,3.1),'stone')
 for x in (-5.75,5.75):
  for y in (-3.6,3.6):A.box('Ground floor support',(x,y,1.55),(.38,.38,3.1),'cream')
 A.box('Raised office floor',(0,0,3.14),(12.7,8.5,.3),'cream')
 A.part('Low gable and storefront')
 A.frame_facade(0,0,12,8,3.3,3.0,1,bay=1.2,glass='glass',slab='white',mullion=.10,band=.6)
 A.mesh('Pale shallow gable roof',[(-6.6,-4.5,6.4),(6.6,-4.5,6.4),(6.6,0,8.3),(-6.6,0,8.3),(-6.6,4.5,6.4),(6.6,4.5,6.4)],[(0,1,2,3),(3,2,5,4)],'white')
 A.frame_facade(-10,-2,7,8,0,2.9,1,bay=1.3,glass='glass',slab='white',mullion=.06,band=.2)
 A.box('Small helipad slab',(-10,-2,3.11),(7.6,8.6,.40),'white')
 A.cylinder('Orange pad',(-10,-2,3.36),3,.065,'orange',80);A.cylinder('White pad',(-10,-2,3.403),2.45,.05,'white',80)
 helicopter(-10,-2,3.45,.42)
 A.part('Rear masonry service office')
 A.box('Rear service building',(9,12,3.2),(10,6,6.4),'stone')
 for x in (5.4,7.2,9,10.8,12.6):
  pts=[(x-.33,4.05),(x+.33,4.05),(x+.33,5.10)]+[(x+.33*cos(pi*j/16),5.10+.33*sin(pi*j/16)) for j in range(17)]
  o=A.polygon('Arched service window',pts,0,.065,'dark',False);o.location=(0,8.95,0);o.rotation_euler=(pi/2,0,0)
  A.box('Small window sill',(x,8.86,4.05),(.8,.20,.12),'white')
 A.box('Flat rear roof',(9,12,6.55),(10.5,6.5,.3),'roof');A.hvac(9,12,6.7,1.5,1.1,.6)
 return A.setup_preview(40,28,1450,1150)

def white_corner_office():
 A.reset('white_corner_office','Western pale office with projecting window bays',['Original wide frame'])
 A.frame_facade(0,0,18,18,0,19,12,bay=1.1,glass='glass_blue',slab='white',mullion=.03,band=.75)
 for x in (-8,8):
  for y in (-8,8):
   A.box('Wide pale corner pier',(x,y,9.5),(3.5,3.5,19),'white')
   for k in range(12):
    for xx in (x-.8,x+.8):A.box('Small corner front window',(xx,y-1.77,.75+k*1.55),(.42,.04,.62),'glass_blue')
    for yy in (y-.8,y+.8):A.box('Small corner side window',(x+1.77,yy,.75+k*1.55),(.04,.42,.62),'glass_blue')
 A.part('Central projecting facade piers')
 for side in (-1,1):
  A.box('Central front masonry pier',(0,side*9.38,9.5),(3.3,.85,19),'white')
  A.box('Central side masonry pier',(side*9.38,0,9.5),(.85,3.3,19),'white')
  for k in range(12):
   for dx in (-.78,.78):
    A.box('Central pier punched window',(dx,side*9.825,.75+k*1.55),(.34,.04,.63),'glass')
    A.box('Side pier punched window',(side*9.825,dx,.75+k*1.55),(.04,.34,.63),'glass')
 A.box('Wide flat office roof',(0,0,19.2),(19.4,19.4,.4),'roof')
 for x,y in [(-6,-6),(6,-6),(-6,6),(6,6)]:A.hvac(x,y,19.41,1.8,1.2,.8)
 for x in (-9.3,9.3):A.box('Roof parapet return',(x,0,19.70),(.2,18.8,.6),'cream')
 for y in (-9.3,9.3):A.box('Roof parapet',(0,y,19.70),(18.8,.2,.6),'cream')
 return A.setup_preview(38,28,1400,1250)

BUILDERS={'linkedin':linkedin,'zynga':zynga,'terrace_office':terrace_office,'security_tower':security_tower,'stadium':stadium,'framing_tower':framing_tower,'legacy_hp':legacy_hp,'small_offices':small_offices,'white_corner_office':white_corner_office}
if __name__=='__main__':
 ids=sys.argv[sys.argv.index('--assets')+1:] if '--assets' in sys.argv else list(BUILDERS)
 for asset in ids:BUILDERS[asset]();A.save_asset(asset)
