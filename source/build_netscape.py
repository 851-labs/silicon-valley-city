import os,sys,math,random,json
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from math import sin,cos,pi,sqrt,tanh

def build(original=False):
 A.reset('netscape','Netscape and Android curved pavilion',['YU20','YU09','YU16'])
 A.material('curved_shell',(.73,.74,.71),.32,.05)
 A.material('canopy_glass',(.78,.86,.90),.13,.02,trans=.90)
 A.material('curtain_glass',(.16,.26,.28),.18,.2)
 def cx(y):return 3.1*tanh((y-1)/4.6)
 def warp(y):return 1.25*sin(pi*(y+25)/50)-.65*sin(2*pi*(y+25)/50)
 def curved_plate(name,ring,z,h,mat):
  ob=A.polygon(name,ring,z,h,mat,False)
  for v in ob.data.vertices:v.co.z+=warp(v.co.y)
  bevel=ob.modifiers.new('Rounded continuous fascia edges','BEVEL');bevel.width=.075;bevel.segments=3
  ob.modifiers.new('Smooth architectural normals','WEIGHTED_NORMAL')
  ob['part']=A.PART
  return ob
 def width(y):return 5.75*sqrt(max(0,1-(y/25)**2))*(.64+.36*min(1,abs(y)/10))
 ys=[-24.97+i*49.94/120 for i in range(121)]
 boundary=[(cx(y)+width(y),y) for y in ys]+[(cx(y)-width(y),y) for y in reversed(ys)]
 A.part('Curved floor plates and rounded rims')
 for k in range(4):
  z=.20+k*3.05
  ring=boundary if k else [(x,y) for x,y in boundary if y<=3]
  curved_plate('Continuous sinuous floor plate',ring,z,.58,'curved_shell')
  A.curve('Soft rounded slab lip',[(x,y,z+.29+warp(y)) for x,y in ring],.27,'curved_shell',True)
  if k<3:
   curved_plate('Broad white upper facade fascia',ring,z+2.19,.86,'curved_shell')
   inner=[(cx(y)+(x-cx(y))*.94,y*.996) for x,y in ring]
   vs=[];faces=[]
   for i,(x,y) in enumerate(inner):vs.extend([(x,y,z+.63+warp(y)),(x,y,z+2.19+warp(y))])
   for i in range(len(inner)):j=(i+1)%len(inner);faces.append((2*i,2*j,2*j+1,2*i+1))
   A.mesh('Continuous curved curtain wall',vs,faces,'curtain_glass')
   A.curve('Recessed curved transom',[(x,y,z+1.45+warp(y)) for x,y in inner],.022,'metal',True)
   for i in range(0,len(inner),3):
    x,y=inner[i];A.rod('Curved facade mullion',(x,y,z+.63+warp(y)),(x,y,z+2.19+warp(y)),.027,'frame')
 roof=10.05
 A.part('Inset rooftop parapet')
 inner=[(cx(y)+(x-cx(y))*.88,y*.972) for x,y in boundary]
 A.curve('Raised roof coping',[(x,y,roof+.40+warp(y)) for x,y in inner],.15,'curved_shell',True)
 for a,b in zip(inner,inner[1:]+inner[:1]):A.mesh('Solid low roof parapet',[(a[0],a[1],roof+warp(a[1])),(b[0],b[1],roof+warp(b[1])),(b[0],b[1],roof+.4+warp(b[1])),(a[0],a[1],roof+.4+warp(a[1]))],[(0,1,2,3)],'curved_shell')
 A.part('Raised pool and sun terrace')
 pool_y=[3+i*13/40 for i in range(41)];pool=[(cx(y)+width(y)*.63,y) for y in pool_y]+[(cx(y)-width(y)*.63,y) for y in reversed(pool_y)]
 water=A.material('Rooftop rippling water',(.13,.43,.52),.12,.2,trans=.12)
 nodes=water.node_tree.nodes;links=water.node_tree.links;noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=8;noise.inputs['Detail'].default_value=2;bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.065;links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs[0],nodes.get('Principled BSDF').inputs['Normal'])
 A.polygon('Pool raised stone basin',pool,roof+.0,1.52,'curved_shell');A.polygon('Pool water',pool,roof+1.535,.025,'Rooftop rippling water');A.curve('Pool stone coping',[(x,y,roof+1.62) for x,y in pool],.10,'white',True)
 A.umbrella(cx(19)-2,19,roof+warp(19),2.1,'yellow')
 for y,color in [(19,'orange'),(21,'green')]:
  x=cx(y)+1.1
  A.box('Deck-chair seat',(x,y,roof+.36),(1.4,.58,.11),color)
  ob=A.box('Deck-chair reclined back',(x+.75,y,roof+.74),(1.15,.58,.1),color,batch=False);ob.rotation_euler.y=-.65
  for yy in (y-.27,y+.27):
   A.rod('Deck-chair frame',(x-.62,yy,roof+.10),(x+.77,yy,roof+.10),.033,'frame');A.rod('Chair front leg',(x-.48,yy,roof),(x-.48,yy,roof+.38),.035,'frame')
  A.sphere('Sunbather head',(x+.84,y,roof+1.17),(.14,.14,.15),'cream',10,6)
  A.box('Sunbather torso',(x+.48,y,roof+.74),(.65,.35,.18),'cream');A.rod('Sunbather legs',(x+.2,y,roof+.55),(x-.45,y,roof+.42),.11,'cream')
 A.part('Swept glass canopy')
 # Longitudinally increasing arches reproduce the rising sail, not a dome.
 def canopy(t,u):
  if original:
   fit=json.load(open(os.path.join(A.ROOT,'source','netscape_fit.json')))
   y=-21+(fit['canopy_end_y']+21)*t;peak=fit['canopy_peak_z']-roof-.45
  else:y=-15.8+19.0*t;peak=8.6
  w=width(y)*.82;x=cx(y)+(2*u-1)*w
  z=roof+.45+warp(y)+sin(pi*u)*(3.4+(peak-3.4)*t)
  return (x,y,z)
 nx,ny=24,36;vs=[canopy(j/ny,i/nx) for j in range(ny+1) for i in range(nx+1)];fs=[]
 for j in range(ny):
  for i in range(nx):a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1))
 A.mesh('Swept translucent canopy skin',vs,fs,'canopy_glass',False,True)
 for j in range(29):A.curve('Canopy arch rib',[canopy(j/28,i/40) for i in range(41)],.045,'frame')
 for i in range(25):A.curve('Canopy longitudinal glazing bar',[canopy(j/48,i/24) for j in range(49)],.028,'frame')
 for u in (0,1):A.curve('Thick canopy sill beam',[canopy(j/60,u) for j in range(61)],.083,'white')
 A.part('Foosball roof terrace')
 for y in (-20,-13.4,-7.4):
  roof=10.05+warp(y);x=cx(y)
  A.box('Blue foosball table',(x,y,roof+.88),(1.9,1.08,.32),'blue');A.box('Green playing field',(x,y,roof+1.055),(1.62,.87,.035),'green')
  for dx in (-.7,.7):
   for dy in (-.38,.38):A.rod('Table leg',(x+dx,y+dy,roof),(x+dx,y+dy,roof+.83),.075,'dark')
  for j in range(5):
   yy=y-.35+j*.175;A.rod('Foosball rod',(x-1.17,yy,roof+1.10),(x+1.17,yy,roof+1.10),.019,'metal')
   for dx in (-.40,0,.4):A.box('Foosball figure',(x+dx,yy,roof+1.13),(.07,.07,.18),'red' if j%2 else 'yellow')
  for side in (-1,1):
   for dy in (-.45,.5):A.person(x+side*1.35,y+dy,roof,random.choice(['red','white','green','purple']))
 roof=10.05
 A.part('Android flat facade figure')
 y=15.0;x=cx(y)+width(y)+.80;z=6.9
 def panel(name,yy,zz,w,h):
  o=A.sign_panel(name,(x,yy,zz),w,h,'android',.22,min(w,h)*.20);o.rotation_euler=(pi/2,0,pi/2);return o
 panel('Android rounded torso',y,z,3.6,3.65)
 for dy in (-2.25,2.25):panel('Android arm',y+dy,z+.15,.65,3.25)
 for dy in (-.95,.95):panel('Android leg',y+dy,z-2.45,.69,2.20)
 pts=[(-1.84,0),(1.84,0)]+[(1.84*cos(i*pi/40),1.84*sin(i*pi/40)) for i in range(41)]
 ob=A.polygon('Android semicircular head',pts,-.11,.22,'android',False);ob.rotation_euler=(pi/2,0,pi/2);ob.location=(x,y,z+2.09)
 for dy in (-.88,.88):
  A.sphere('Android eye',(x+.13,y+dy,z+3.11),(.04,.13,.17),'white',16,8)
  A.rod('Android antenna',(x,y+dy*1.45,z+3.37),(x,y+dy*1.78,z+4.10),.065,'android',12)
 A.part('Netscape historical signage')
 yy=-14.6;xx=cx(yy)+width(yy)+.52
 o=A.sign_panel('N logo panel',(xx,yy-5.7,3.3),3.3,3.3,'turquoise',.25,.06);o.rotation_euler=(pi/2,0,pi/2)
 A.text('Netscape serif N','N',(xx+.19,yy-5.7,2.2),3.1,'white','serif',rot=(pi/2,0,pi/2),depth=.09)
 A.text('Netscape wordmark','Netscape',(xx+.15,yy+3.7,2.3),3.5,'black','black',width=14.3,rot=(pi/2,0,pi/2),depth=.18)
 A.part('Attached lower terrace')
 A.box('Side terrace slab',(8.7,16.8,3.10),(7.2,12.3,.38),'curved_shell')
 for y in (10.7,22.9):A.box('Terrace parapet',(8.8,y,3.52),(7.4,.19,.8),'curved_shell')
 A.box('Terrace parapet return',(12.4,16.8,3.52),(.19,12.4,.8),'curved_shell')
 A.COL['inferred_details']='Plan reconstructed from two oblique production views. Rear service details are inferred; no later LED message board in the Season 1 variant.'
 return A.setup_preview(52,26,1600,1050)

if __name__=='__main__':build();A.save_asset('netscape','--no-render' not in sys.argv)
