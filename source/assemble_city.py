"""Linked building assembly, fitted to the original intro wide frame.

Screen anchors are measured in the 1280x720 reference. They refer to specific
modeled points, not guessed centers of building bounding boxes.
"""
import os,sys,json,math,random
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
import bpy
from mathutils import Vector,Matrix
from math import sin,cos,pi,atan2
# Start from an unnamed file so the last catalogued asset can be linked safely.
bpy.ops.wm.read_factory_settings(use_empty=True)
ROOT=A.ROOT
CHECKPOINT='--measured-checkpoint' in sys.argv
CAL=json.load(open(os.path.join(ROOT,'source','camera_calibration.json')))
AZ=math.radians(CAL['azimuth']);EL=math.radians(CAL['elevation']);S=5.0;OX,OY=640,460
PX=Vector((cos(AZ),sin(AZ)));PY=Vector((sin(AZ)*sin(EL),-cos(AZ)*sin(EL)))
def project(p):return Vector((OX+S*(PX.x*p[0]+PX.y*p[1]),OY+S*(PY.x*p[0]+PY.y*p[1]-cos(EL)*p[2])))
def unproject(p,z=0):
 u=(p[0]-OX)/S;v=((p[1]-OY)/S+cos(EL)*z)/sin(EL)
 return Vector((cos(AZ)*u+sin(AZ)*v,sin(AZ)*u-cos(AZ)*v,z))

A.reset('city_environment','City streets, landscaping and traffic',['Original wide frame','YU19','YU16'])
A.COL.asset_clear();A.COL.name='ENVIRONMENT • streets and landscaping'
A.surface_detail(A.material('asphalt',(.028,.030,.027),.90),.018,42)
A.surface_detail(A.material('sidewalk',(.24,.23,.205),.88),.012,30)
A.material('site_base',(.31,.34,.22),.9)
A.material('car_blue',(.13,.34,.57),.40)
A.material('car_red',(.61,.044,.018),.40)
A.material('car_green',(.007,.30,.22),.40)
A.material('tree_olive',(.22,.35,.032),.8)
A.material('tree_dark',(.065,.21,.016),.8)
A.material('tree_lime',(.30,.42,.05),.8)
ASSEMBLY=bpy.data.collections.new('CITY • linked building instances');bpy.context.scene.collection.children.link(ASSEMBLY)
LIBS={};PLACEMENTS=[];OCC=[]
def get_asset(id):
 if id not in LIBS:
  f=os.path.join(ROOT,'assets',id,id+'.blend')
  with bpy.data.libraries.load(f,link=True) as (src,dst):dst.collections=[n for n in src.collections if n.startswith('ASSET')]
  if len(dst.collections)!=1:raise RuntimeError('Expected one asset root in '+id)
  LIBS[id]=dst.collections[0]
 return LIBS[id]
def place(id,point,pixel,scale=1,angle=0,name=None,avoid=True,repeat_anchor=None):
 col=get_asset(id);sc=Vector((scale,)*3 if isinstance(scale,(float,int)) else scale);rot=Matrix.Rotation(math.radians(angle),3,'Z')
 intrinsic=col.get('applied_reference_proportions',[1,1,1]);point=tuple(point[i]*intrinsic[i] for i in range(3));sc=Vector(tuple(sc[i]/intrinsic[i] for i in range(3)))
 local=rot@Vector(tuple(point[i]*sc[i] for i in range(3)));base=unproject(pixel,local.z)-local
 if 'reference_frame_anchor' in col:
  # Measured assets already encode the individual roof orientations in world axes.
  # Reapplying the previous guessed rotation would undo their calibration.
  measured=repeat_anchor if repeat_anchor is not None else col['reference_frame_anchor'];base=unproject(measured[:2],measured[2]);base.z=0
  sc=Vector((1,1,1));angle=0;point=(0,0,measured[2]);pixel=measured[:2]
 ob=bpy.data.objects.new(name or id.replace('_',' ').title(),None);ASSEMBLY.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=col;ob.location=base;ob.rotation_euler.z=math.radians(angle);ob.scale=sc;ob.empty_display_type='PLAIN_AXES';ob.empty_display_size=2
 ob['source_reference']='original_wide.webp';ob['reference_anchor_px']=list(pixel);ob['model_anchor']=list(point);ob['library_asset']=id
 PLACEMENTS.append({'name':ob.name,'asset':id,'reference_pixel':list(pixel),'model_anchor':list(point),'scale':list(sc),'rotation_degrees':angle,'world_origin':list(base)})
 bpy.context.view_layer.update()
 pts=[ob.matrix_world@(q.matrix_world@Vector(c)) for q in col.all_objects if q.type in ('MESH','CURVE','FONT') for c in q.bound_box]
 if pts and avoid:
  if id in ('google','facebook'):
   chosen=[q for q in col.all_objects if q.type=='MESH' and 'measured shell' in q.get('part','') and any(m and m.name in ('google_concrete','facebook_glass') for m in q.data.materials)]
   assert chosen,('No building envelopes found for landscape clearance',id)
   if id=='facebook':chosen.extend(q for q in col.all_objects if q.type=='MESH' and q.get('part')=='Northern Like sculpture plaza')
   for q in chosen:
    pp=[ob.matrix_world@(q.matrix_world@Vector(c)) for c in q.bound_box];OCC.append((min(p.x for p in pp),max(p.x for p in pp),min(p.y for p in pp),max(p.y for p in pp),id))
  else:OCC.append((min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts),id))
 return ob

# Principal landmarks. The title's XY scale comes from its traced roof contours.
ts=CAL['title_pixels_per_unit']/S
place('title_towers',(0,0,30.73),(CAL['affine'][0][2],CAL['affine'][1][2]),(ts,ts,.48))
place('youtube',(3.14,-4.27,17.7),(627,304),1.0)
nf=json.load(open(os.path.join(ROOT,'source','netscape_fit.json')))
place('netscape_digg',(-3.1,-25,10.05),nf['front_roof_pixel'],(nf['scale_xy'],nf['scale_xy'],nf['scale_z']),nf['rotation'])
place('google',(3.1,11.25,13.6),(433,512),(1.05,1.18,.95),9)
place('facebook',(0,0,7.42),(375,262),(1.0,1.0,.64),24)
place('intel',(-7,-6,9.07),(504,432),.90)
place('ebay',(0,0,7.24),(718,508),(1.08,1.44,1.10))
place('twitter',(7.9,-3.5,14.6),(769,287),.99)
place('apple',(0,0,2.5),(1065,374),1.18)
place('yahoo_oracle',(-12.5,1.2,12.92),(875,23),1.05)
place('hooli',(0,-3.67,16.2),(1143,161),(1.07,1.0,1.30))
place('myspace',(-10,0,13.53),(750,408),.92)
place('energy_pod',(0,-3,26),(1000,530),(.86,.86,.93))
place('adobe',(14.82,0,37.35),(1241,433),1.0)
place('pets_com',(0,0,10.23),(338,324),.95)
place('paypal',(0,0,7.98),(141,308),1.1)
place('linkedin',(0,-5.4,6.1),(95,380),1.0)
place('west_solar',(0,0,7.16),(245,414),1.0,-35)
place('blue_sculpture',(0,0,.8),(978,450),1.3,avoid=False)
place('small_offices',(-10,-2,3.4),(225,357),.9)
place('zynga',(-7,1.7,14.4),(800,614),1.05)
place('legacy_hp',(2,2,31),(130,636),1.10)
place('security_tower_west',(0,0,16),(290,83),1.15,name='Western security tower')
place('security_tower',(0,0,16),(1193,238),1.10,name='Eastern security tower')
place('security_tower_north',(0,0,16),(725,-26),1.08,name='Northern security tower')
place('framing_tower',(0,0,40),(200,10),(1.15,1.15,.90))
place('stadium',(0,0,13.8),(43,55),.95)
place('white_corner_office',(0,0,19.4),(66,185),1.15)
terraces=json.load(open(os.path.join(ROOT,'source','terrace_placements_measured.json')))
for i,p in enumerate(terraces['placements']):
 place('terrace_office',(0,0,10.5),p['anchor'],name='Southeast terraced office '+str(i+1),repeat_anchor=[*p['anchor'],10.5])
north_offices=json.load(open(os.path.join(ROOT,'source','north_office_placements_measured.json')))
for i,p in enumerate(north_offices['placements']):
 place('north_solar_office',(0,0,8.0),p['anchor'],name=p.get('name','Northern solar office '+str(i+1)),repeat_anchor=[*p['anchor'],8.0])

place('northeast_campus',(0,0,5.4),(1118,84),name='Northeast courtyard campus')
place('northeast_house',(0,0,3.3),(998,29),name='Northeast olive house')
place('service_office',(0,0,4.9),(477,293),name='Central service office behind Digg')

def occupied(p,margin=.5):return any(a-margin<p.x<b+margin and c-margin<p.y<d+margin for a,b,c,d,id in OCC)
def polygon_px(name,points,z,h,mat):A.polygon(name,[(unproject(p).x,unproject(p).y) for p in points],z,h,mat)

A.part('Continuous terrain and city paving')
polygon_px('Continuous green terrain',[(-350,-250),(1700,-250),(1700,1120),(-350,1120)],-.50,.15,'site_base')
polygon_px('City paved ground',[(-50,140),(475,-100),(1040,-80),(1410,190),(1480,840),(150,925),(-160,490)],-.29,.20,'sidewalk')

# Roads are fitted to visible centerlines, then continued below occluding buildings.
ROAD_DATA=[
 ('Facebook perimeter avenue',[(161,137),(169,190),(205,234),(310,276),(382,309),(472,348),(573,389),(686,438),(835,503),(953,554),(1070,607),(1390,748)],8.2),
 ('Northern approach',[(-30,278),(184,185),(404,89),(646,-12),(925,-130)],8.5),
 ('Central diagonal',[(182,587),(234,550),(326,508),(419,465),(515,423),(611,381),(710,338),(813,295),(912,252),(1048,191),(1230,110),(1400,36)],7.1),
 ('Campus boulevard',[(274,323),(387,272),(508,218),(627,166),(746,114),(836,77),(965,27)],7.0),
 ('Blogger curved street',[(492,379),(552,348),(578,323),(564,288),(576,259),(614,232),(680,204),(755,172)],7.3),
 ('Apple western boulevard',[(841,493),(868,471),(864,439),(859,409),(874,381),(922,352),(999,319),(1089,278),(1120,247),(1110,215)],7.4),
 ('eBay eastern loop',[(683,666),(754,647),(819,620),(872,594),(881,577),(867,555),(825,532),(777,510)],6.8),
 ('Google front boulevard',[(-50,536),(60,581),(176,631),(299,684),(420,735),(553,792),(680,843)],8.5),
 ('Western district road',[(-80,415),(38,467),(143,512),(252,559),(333,595)],6.9),
 ('Historic district connector',[(17,264),(86,293),(183,336),(267,373),(361,414),(430,444)],6.1),
 ('Southeast lane A',[(996,716),(1077,678),(1160,640),(1245,600),(1370,544)],5.9),
 ('Southeast lane B',[(1097,758),(1181,719),(1266,679),(1404,618)],5.9),
 ('East transverse',[(872,569),(975,614),(1082,661),(1186,707),(1328,769)],6.3),
]
ROADS=[]
def catmull(points,n=14):
 p=[Vector(x) for x in points];out=[]
 for i in range(len(p)-1):
  a=p[max(0,i-1)];b=p[i];c=p[i+1];d=p[min(len(p)-1,i+2)]
  for j in range(n):
   t=j/n;out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 out.append(p[-1]);return out
def ribbon(name,pts,width,z,mat):
 vs=[]
 for i,p in enumerate(pts):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();n=Vector((-t.y,t.x,0));vs.extend([tuple(p+n*width/2+Vector((0,0,z))),tuple(p-n*width/2+Vector((0,0,z)))])
 A.mesh(name,vs,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(pts)-1)],mat)
for ri,(name,pixels,w) in enumerate(ROAD_DATA):
 pts=catmull([unproject(p) for p in pixels]);ROADS.append((name,pts,w));A.part('Roads • '+name)
 ribbon(name+' concrete curb bed',pts,w+1.05,-.073+ri*.0013,'white');ribbon(name+' asphalt',pts,w,-.042+ri*.0013,'asphalt')
 for side in (-1,1):
  offset=[]
  for i,p in enumerate(pts):
   t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();offset.append(p+Vector((-t.y,t.x,0))*side*(w/2-.45))
  ribbon(name+' continuous lane edge',offset,.105,-.025+ri*.0013,'white')
  edge=[]
  for i,p in enumerate(pts):
   t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();edge.append(p+Vector((-t.y,t.x,0))*side*(w/2+.18))
  ribbon(name+' raised cream curb top',edge,.35,.14+ri*.0013,'cream')
  vs=[(p.x,p.y,z) for p in edge for z in (-.04,.14+ri*.0013)]
  A.mesh(name+' vertical curb reveal',vs,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(len(edge)-1)],'stone')

def near_road(p,margin=0):
 for name,pts,w in ROADS:
  if any((p-q).length<w/2+margin for q in pts[::2]):return True
 return False

# Planted pockets are hand-fitted to the reference, not a random grid of city lots.
PARKS=[
 ('Twitter garden',[(702,371),(808,323),(906,326),(931,346),(854,387),(809,420),(734,405)],90),
 ('Hooli front garden',[(1056,245),(1120,231),(1289,284),(1250,342),(1159,328),(1084,298)],85),
 ('Google eastern garden',[(501,590),(583,554),(704,585),(757,623),(727,658),(628,659),(540,637)],150),
 ('Google foreground garden',[(399,690),(500,641),(612,663),(733,714),(691,798),(545,810),(428,762)],190),
 ('Northwest Google garden',[(116,453),(187,423),(301,459),(308,504),(253,534),(161,501)],55),
 ('Facebook campus green',[(292,280),(379,150),(490,82),(636,65),(742,129),(683,190),(421,303)],98),
 ('North roadside garden',[(242,79),(516,-44),(626,0),(331,137)],30),
 ('Eastern belt',[(1211,359),(1306,310),(1461,420),(1379,527),(1272,493)],65),
 ('Apple southern garden',[(930,429),(1047,441),(1128,460),(1105,486),(1028,477),(980,456)],48),
]
def inside(p,poly):
 c=False;x,y=p
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if ((a[1]>y)!=(b[1]>y)) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
 return c
random.seed(814)
for name,poly,count in PARKS:
 A.part('Landscape • '+name);polygon_px(name,poly,-.083,.025,'grass')
 x0,x1=min(p[0] for p in poly),max(p[0] for p in poly);y0,y1=min(p[1] for p in poly),max(p[1] for p in poly)
 placed=0
 for attempt in range(count*80):
  pix=(random.uniform(x0,x1),random.uniform(y0,y1));q=unproject(pix)
  if not inside(pix,poly) or occupied(q,.15) or near_road(q,.4):continue
  A.part('Landscape • '+name);h=random.uniform(2.9,4.6);r=random.uniform(1.3,1.85)
  if random.random()<.19:
   A.cylinder('Cypress trunk',(q.x,q.y,h*.3),.08,h*.6,'wood',9)
   A.cylinder('Tapered cypress crown',(q.x,q.y,h*.62),r*.61,h*.98,'tree_dark',12,r2=.025)
  else:A.tree(q.x,q.y,0,r,h)
  placed+=1
  if placed>=count:break

# Regular rows of slender russet-trunk trees are a strong feature of the source.
for name,start,end,n in [
 ('Facebook avenue tree row',(383,309),(752,152),37),
 ('Twitter and title tree row',(781,380),(971,291),24),
 ('Northern avenue tree row',(385,110),(603,19),23),
 ('Google front tree row',(498,704),(745,702),27)]:
 a,b=unproject(start),unproject(end)
 for i in range(n):
  p=a.lerp(b,i/max(1,n-1))
  if occupied(p,.0):continue
  A.part('Landscape • '+name);h=3.2+random.random()*1.7;A.tree(p.x,p.y,0,.88,h)

def car(p,heading,color='car_blue',van=False):
 A.part('Traffic • '+('vans' if van else 'cars'))
 c,s=cos(heading),sin(heading)
 def q(x,y,z):return(p.x+c*x-s*y,p.y+s*x+c*y,z)
 A.box('Painted car body',q(0,0,.48),(2.75,1.22,.63),color,heading)
 # Four side panels and the roof make a sloping glazed cabin.
 vs=[q(x,y,z) for x,y,z in [(-.97,-.58,.79),(.64,-.58,.79),(.36,-.52,1.43),(-.61,-.52,1.43),(-.97,.58,.79),(.64,.58,.79),(.36,.52,1.43),(-.61,.52,1.43)]]
 A.mesh('Glazed car cabin',vs,[(0,1,2,3),(4,7,6,5),(0,3,7,4),(1,5,6,2)],'glass_light')
 A.mesh('Painted cabin roof',vs,[(3,2,6,7)],color)
 for side in (-1,1):
  A.rod('Door frame',q(-.1,side*.59,.77),q(-.1,side*.53,1.43),.03,color,8)
  for xx in (-.87,.85):
   A.rod('Black tire',q(xx,side*.53,.31),q(xx,side*.71,.31),.31,'dark',12);A.rod('Silver wheel hub',q(xx,side*.715,.31),q(xx,side*.728,.31),.15,'metal',12)
 for yy in (-.4,.4):A.box('Front headlight',q(-1.384,yy,.61),(.03,.24,.16),'white',heading)
 A.box('Front bumper',q(-1.39,0,.30),(.08,1.15,.11),'frame',heading)
 if van:
  A.box('Van cargo box',q(.5,0,1.08),(1.65,1.27,1.08),color,heading)
  for side in (-1,1):A.box('Van side window',q(.50,side*.646,1.31),(1.29,.023,.43),'glass',heading)

A.part('Roadside lamps and traffic')
random.seed(47)
for ri,(name,pts,w) in enumerate(ROADS):
 distance=0;nextcar=random.uniform(4,10);nextlamp=10
 for i in range(1,len(pts)):
  p=pts[i];distance+=(p-pts[i-1]).length;t=(p-pts[i-1]).normalized();n=Vector((-t.y,t.x,0))
  if distance>=nextcar:
   lane=random.choice([-1,1]);q=p+n*w*.22*lane
   if not occupied(q,.25):car(q,atan2(t.y,t.x)+(pi if lane<0 else 0),random.choice(['car_blue','car_blue','car_red','yellow','white','car_green']),random.random()<.20)
   nextcar=distance+random.uniform(5.0,13.5)
  if distance>=nextlamp:
   side=-1 if int(distance/15)%2 else 1;q=p+n*(w/2+.6)*side
   if not occupied(q,.2):
    A.part('Roadside streetlights');A.rod('Thin streetlight pole',(q.x,q.y,0),(q.x,q.y,5.3),.035,'metal');end=q-n*1.4*side
    A.rod('Light cantilever',(q.x,q.y,5.3),(end.x,end.y,5.3),.035,'metal');A.sphere('Streetlight luminaire',(end.x,end.y,5.30),(.32,.15,.075),'white',10,6)
   nextlamp=distance+18

# Zebra crossings at intersections that remain visible in the reference camera.
A.part('Parking-lot bays')
for start,end,n in [((173,236),(303,292),18),((19,577),(296,698),27),((321,93),(550,-9),23)]:
 a,b=unproject(start),unproject(end);t=(b-a).normalized();normal=Vector((-t.y,t.x,0));angle=atan2(normal.y,normal.x)
 for i in range(n):
  p=a.lerp(b,i/max(1,n-1))
  A.box('White parking-space divider',(p.x,p.y,-.001),(3.7,.04,.016),'white',angle)
  if i<n-1:
   q=p+(b-a)/(n-1)*.5
   if not occupied(q,.1):car(q,angle,random.choice(['yellow','yellow','car_blue','white','car_red']),False)
A.part('Pedestrian crossings')
for pix,ang in [((346,439),0),((588,400),0),((650,459),90),((930,328),0),((865,564),0),((287,311),0),((737,68),90)]:
 q=unproject(pix);t=Vector((cos(math.radians(ang)),sin(math.radians(ang)),0));n=Vector((-t.y,t.x,0))
 for i in range(9):
  p=q+n*(i-4)*.51;A.box('Zebra stripe',(p.x,p.y,-.015),(2.3,.22,.018),'white',math.radians(ang))

# Original freestanding Facebook parking-lot billboard.
A.part('Western Facebook roadside billboard')
q=unproject((211,170),13.7)
A.sign_panel('Facebook billboard',(q.x,q.y,13.7),18.4,4.9,'facebook',.28,.06)
from reference_geometry import vector_art
glyphs=json.load(open(os.path.join(ROOT,'source','facebook_2005_mesh.json')))
vector_art('Historical Facebook roadside wordmark',glyphs,(q.x-8.1,q.y-.19,12.02),(16.2,0,0),(0,0,16.2),.18,(0,-1,0))
for x in (q.x-6.8,q.x+6.8):A.rod('Billboard pole',(x,q.y,0),(x,q.y,11.3),.12,'metal')
A.flush()

# Lighting and cameras are separate from the linked asset instances.
s=bpy.context.scene;studio=bpy.data.collections.new('CAMERAS AND LIGHT');s.collection.children.link(studio)
def camera(name,az,el,target,scale):
 d=Vector((sin(az)*cos(el),-cos(az)*cos(el),sin(el)));cd=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,cd);studio.objects.link(ob);ob.location=Vector(target)+d*650;ob.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=scale;cd.clip_end=3000;return ob
cam=camera('01 • Original intro reference camera',AZ,EL,unproject((640,360)),1280/S);s.camera=cam
camera('02 • Full city overview',math.radians(40),math.radians(48),unproject((670,335)),355)
camera('03 • Title and eastern landmarks',AZ,math.radians(31),unproject((939,301),7),138)
rig=json.load(open(os.path.join(ROOT,'source','lighting_measurements.json')))
world=bpy.data.worlds.new('Shared reference sky fill');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(*rig['world_color'],1);world.node_tree.nodes['Background'].inputs[1].default_value=rig['world_strength'];s.world=world
ld=bpy.data.lights.new('Animated morning sun','SUN');ld.energy=rig['sun_energy'];ld.color=rig['sun_color'];ld.angle=rig['sun_angle'];lo=bpy.data.objects.new('Animated morning sun',ld);studio.objects.link(lo)
for frame,alt,color in [(1,20,(1,.76,.56)),(60,rig['sun_elevation'],rig['sun_color']),(120,58,(1,.97,.94))]:
 a=math.radians(alt);az=math.radians(rig['sun_azimuth']);d=Vector((cos(az)*cos(a),sin(az)*cos(a),sin(a)))
 lo.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();lo.keyframe_insert(data_path='rotation_euler',frame=frame)
 ld.color=color;ld.keyframe_insert(data_path='color',frame=frame)
s.frame_start=1;s.frame_end=120;s.frame_set(60);s.render.fps=24
s['lighting_reference']='Frame 60 uses the same shadow-fitted sun direction, sky and colour transform as the measured asset comparisons. Editable sunrise variation is retained at frames 1 and 120.'
s['reference_light_version']=rig['version'];s['version']='fidelity-4-in-progress';s['measured_asset_count']=sum('reference_frame_anchor' in c for c in LIBS.values())
s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True;s.cycles.max_bounces=6
A.configure_cycles(s)
s.render.resolution_x=2560;s.render.resolution_y=1440;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
s['reference']='HBO original intro wide frame; reference camera calibrated from the title roofs.'
s['calibration_rmse_pixels']=CAL['pixel_rmse'];s['asset_count']=len(LIBS);s['building_instance_count']=len(PLACEMENTS)
s['editing']='Buildings are linked collection instances. Open their individual files in assets/ to edit geometry; reload libraries to update this assembly.'
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False;area.spaces.active.clip_end=3000
bpy.ops.object.select_all(action='DESELECT');bpy.context.preferences.filepaths.save_version=0
os.makedirs(os.path.join(ROOT,'renders'),exist_ok=True)
json.dump(PLACEMENTS,open(os.path.join(ROOT,'source','city_placements_measured.json' if CHECKPOINT else 'city_placements.json'),'w'),indent=2)
s.render.filepath=os.path.join(ROOT,'renders','city_measured.png' if CHECKPOINT else 'city_reference.png')
destination=os.path.join(ROOT,'city_measured.blend' if CHECKPOINT else 'city.blend')
bpy.ops.wm.save_as_mainfile(filepath=destination,compress=True)
bpy.ops.file.make_paths_relative();bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=destination,compress=True)
if '--no-render' not in sys.argv:bpy.ops.render.render(write_still=True)
print('CITY_READY',len(LIBS),'unique assets',len(PLACEMENTS),'instances',flush=True)
