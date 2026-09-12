import os,sys,math,random
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from math import sin,cos,pi

def ring(name,cx,cy,outer,inner,z,h,mat,n=192):
 vs=[(cx+r*cos(i*2*pi/n),cy+r*sin(i*2*pi/n),zz) for zz in (z,z+h) for r in (outer,inner) for i in range(n)]
 fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,j+2*n,i+2*n),(i+n,i+3*n,j+3*n,j+n),(i+2*n,j+2*n,j+3*n,i+3*n),(i+n,j+n,j,i)])
 return A.mesh(name,vs,fs,mat)

def apple():
 A.reset('apple','Apple circular campus and courtyard sculpture',['YU14','YU18','Original wide frame'])
 A.part('Annular structural shell')
 ring('Bottom annular concrete slab',0,0,22.35,18.25,.10,.36,'cream')
 ring('Glazed annular body',0,0,22.08,18.48,.46,3.65,'glass')
 ring('Deep pale outer spandrel',0,0,22.23,21.93,1.66,.74,'cream')
 for z in (2.18,4.05):ring('Circular horizontal window rail',0,0,22.16,18.4,z,.12,'frame')
 for i in range(192):
  t=i*2*pi/192
  for r in (22.13,18.43):A.rod('Ring glazing mullion',(r*cos(t),r*sin(t),.4),(r*cos(t),r*sin(t),4.10),.029,'frame')
 ring('Wide white cantilevered ring roof',0,0,22.62,18.0,4.10,.49,'white')
 ring('Slightly raised roof edge',0,0,22.62,22.45,4.59,.14,'white')
 ring('Inner roof edge',0,0,18.17,18.0,4.59,.14,'white')
 A.part('Circular ground and garden paths')
 A.cylinder('Courtyard lawn',(0,0,.13),18.05,.25,'grass',192)
 ring('Perimeter pavement',0,0,23.65,22.6,.03,.09,'paving')
 ring('Courtyard walking path',0,0,17.2,16.3,.28,.08,'cream')
 A.part('White Apple courtyard sculpture')
 A.logo('apple',(0,0,.27),17.5,5.3,'white')
 A.part('Courtyard trees')
 random.seed(18)
 for i in range(125):
  t=random.random()*2*pi;r=8.2+random.random()*7.5
  x,y=r*cos(t),r*sin(t)
  if abs(x)<2.2 and y<0:continue
  A.tree(x,y,.30,.90+random.random()*.60,2.4+random.random()*.9)
 A.COL['artwork']='Apple vector outline, extruded as the original white courtyard object.'
 return A.setup_preview(40,32,1500,1150)

def twitter():
 A.reset('twitter','Twitter and Blogger garden pavilions',['YU13','YU11','YU02'])
 A.surface_detail(A.material('twitter_stone',(.64,.57,.45),.76),.018)
 A.material('twitter_blue',(.015,.24,.35),.45)
 A.material('roof_glass',(.37,.59,.63),.19,.06,trans=.12)
 def pavilion(name,x,y,w,d,h,louvres=True):
  A.part(name+' • pale masonry and vertical slots')
  A.box('Pavilion body',(x,y,h/2),(w,d,h),'twitter_stone')
  # Long side has an irregular arrangement of narrow full-depth reveals.
  for side in (-1,1):
   for i in range(round(d/1.45)):
    yy=y-d/2+.55+i*1.45
    for k in range(3):
     zz=1.35+k*2.65
     if (i+2*k)%5==2:continue
     A.box('Narrow vertical reveal',(x+side*(w/2+.022),yy,zz),(.045,.21 if i%3 else .43,1.75),'dark')
  A.part(name+' • recessed end glazing and louvers')
  for side in (-1,1):
   A.box('Dark glazed end',(x,y+side*(d/2+.03),h*.56),(w*.80,.055,h*.82),'glass')
   for k in range(10):A.box('Deep horizontal sunshade',(x,y+side*(d/2+.25),.83+k*(h-.9)/10),(w*.85,.56,.22),'cream')
  A.part(name+' • roof glazing and projecting boxes')
  A.box('Roof glass strip',(x,y,h+.04),(w-.7,d-.8,.09),'roof_glass' if louvres else 'roof')
  for yy in (y-d/2+.19,y+d/2-.19):A.box('Pale raised roof parapet',(x,yy,h+.28),(w,.38,.54),'twitter_stone')
  if louvres:
   for i in range(32):A.box('Roof louvre',(x,y-d/2+.4+i*(d-.8)/32,h+.17),(w-.7,.10,.16),'cream')
  for xx in (x-w/2+.32,x+w/2-.32):A.box('Wide roof beam',(xx,y,h+.33),(.68,d+.75,.55),'roof_glass')
  A.box('Projecting facade box',(x+w/2+.85,y-2.2,h*.53),(1.8,3.65,2.40),'stone')
  A.box('Box end window',(x+w/2+1.77,y-2.2,h*.53),(.035,3.05,1.91),'glass')
 pavilion('Main Twitter pavilion',0,-4.0,8.2,15.0,9.1)
 pavilion('Rear Twitter pavilion',-13.5,7.4,8.7,13.4,9.35,False)
 A.part('Glass courtyard connectors')
 A.frame_facade(3.6,11.5,7.3,10.5,0,4.6,2,bay=1.1,glass='glass_light',slab='twitter_stone',mullion=.05,band=.2)
 A.frame_facade(12.2,14.0,9.7,6.3,0,4.6,2,bay=1.1,glass='glass_light',slab='twitter_stone',mullion=.05,band=.2)
 for x,y,w,d in [(3.6,11.5,7.3,10.5),(12.2,14,9.7,6.3)]:
  A.box('Blue rooftop pool',(x,y,4.77),(w-.6,d-.6,.14),'pool')
  for xx in (x-w/2,x+w/2):A.box('Glass pool screen',(xx,y,5.6),(.055,d,1.8),'roof_glass')
  for yy in (y-d/2,y+d/2):A.box('Glass pool screen',(x,yy,5.6),(w,.055,1.8),'roof_glass')
 A.part('Elevated connecting walkway')
 A.box('Glass bridge',(-6.5,6.5,5.40),(5.4,3.1,2.1),'roof_glass')
 A.box('Bridge roof',(-6.5,6.5,6.50),(5.7,3.3,.14),'frame')
 A.part('Twitter circular bird sign')
 heading=0;center=(7.9,-3.5,14.6)
 # Circle is deliberately turned toward the sequence camera.
 ob=A.polygon('White circular sign',[(4.1*cos(i*2*pi/96),4.1*sin(i*2*pi/96)) for i in range(96)],-.34,.68,'white',False);ob.rotation_euler=(pi/2,0,heading);ob.location=center
 A.rod('Tall sign pole',(7.9,-3.5,0),(7.9,-3.5,13),.13,'metal',16)
 normal=(sin(heading),-cos(heading),0)
 A.logo('twitter',(center[0]+normal[0]*.39,center[1]+normal[1]*.39,center[2]),5.5,.10,'twitter_blue',rot=(pi/2,0,heading))
 A.part('Blogger low square pavilion')
 A.box('Blogger pavilion envelope',(-12.4,27.6,2.20),(21.0,14.5,4.4),'twitter_stone')
 for i in range(28):
  x=-22.4+i*.75;A.box('Blogger clerestory window',(x,20.32,3.85),(.56,.045,.31),'dark')
 A.box('Blogger blue roof',(-12.4,27.6,4.55),(21.5,15.0,.3),'roof_glass')
 A.cylinder('Circular roof lantern',(-9.4,27.8,5.08),2.4,.90,'cream',64,r2=2.05)
 for i in range(40):
  t=2*pi*i/40;A.rod('Lantern radial fin',(-9.4+2.5*cos(t),27.8+2.5*sin(t),4.65),(-9.4+1.95*cos(t),27.8+1.95*sin(t),5.8),.055,'cream')
 A.sign_panel('Blogger orange roof plaque',(-19.2,24.0,4.85),4.1,3.6,'orange',.25,.24).rotation_euler=(0,0,0)
 A.text('Blogger white B','B',(-19.2,22.8,5.06),3.0,'white','black',width=2.2,rot=(0,0,0),depth=.08)
 A.colorword('Google',(-12.7,20.23,1.15),16.0,4.4,'serif',depth=.11)
 A.part('Garden courtyards')
 for x,y,w,d in [(-8,16,8,5),(-13,39,25,4),(10,4,3,12)]:
  A.box('Planted ground patch',(x,y,-.015),(w,d,.03),'grass')
  for i in range(6):A.tree(x-w*.4+i*w*.16,y,0,.80,3.1)
 A.COL['inferred_details']='Unseen return walls; pavilions and projections fitted to YU13 and YU11. Blogger sign is included as a separate part.'
 return A.setup_preview(39,29,1500,1250)

def hooli():
 A.reset('hooli','Hooli colonnaded headquarters',['Original wide frame','YU18','YU14'])
 A.material('hooli_brick',(.50,.19,.11),.67)
 A.part('Main pale office mass')
 A.box('Hooli main envelope',(0,4,5.4),(34,24,10.8),'cream')
 A.box('Eastern annex',(23,9,4.6),(13,15,9.2),'white')
 A.box('Wide flat main roof',(0,4,11.05),(35,25,.5),'roof')
 A.box('Annex cap',(23,9,9.45),(13.8,15.8,.5),'roof')
 A.part('Brick colonnade')
 A.box('Colonnade entablature',(0,-10.1,8.20),(36,3.0,1.2),'hooli_brick')
 for i in range(9):A.box('Terracotta square column',(-16+i*4,-10.1,3.75),(1.15,1.22,7.5),'hooli_brick')
 A.box('Covered walkway floor',(0,-9.6,.15),(36,5.0,.3),'paving')
 for i in range(13):A.box('Shadowed colonnade glazing',(-15.4+i*2.55,-8.06,4.1),(2.1,.045,6.8),'glass')
 A.part('Roof plant and skylight bays')
 for x in (-10,-2,6,14):
  A.box('Raised roof skylight box',(x,7,12.1),(5.7,11,1.6),'roof')
  A.box('Skylight glazing',(x,7,12.94),(5.0,10.3,.09),'glass_light')
  for j in range(7):A.box('Skylight roof bar',(x,2.5+j*1.5,13.02),(5.15,.08,.1),'frame')
 A.part('Large lime Hooli sign')
 for x in (-11,-5,1,7,13):A.rod('Hooli sign leg',(x,-3.5,11.3),(x,-3.5,13.0),.10,'metal')
 A.text('hooli wordmark','hooli',(0,-3.67,12.3),14.0,'hooli','bold',width=32,depth=.38)
 A.COL['variant']='Colonnaded pale and brick main block visible in the original wide image.'
 from build_offices import dish
 dish(12.4,3.3,12.05,1.4,'frame')
 A.hvac(15.4,2.7,10.8,2.1,1.7,.95)
 return A.setup_preview(40,27,1500,1100)

BUILDERS={'apple':apple,'twitter':twitter,'hooli':hooli}
if __name__=='__main__':
 ids=sys.argv[sys.argv.index('--assets')+1:] if '--assets' in sys.argv else list(BUILDERS)
 for asset in ids:BUILDERS[asset]();A.save_asset(asset)
