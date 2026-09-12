"""Reconstruct the season-one title shot using the measured city and Blender keyframes.

Functions can be called in small stages through Blender MCP. Running this file
in background Blender calls all stages. Reference media are never used as textures.
"""
from pathlib import Path
from collections import defaultdict
import bpy,math,json,sys,random,ast,re
from mathutils import Vector,Matrix
P=Path(__file__).resolve().parent;ROOT=P.parent
sys.path.insert(0,str(P))
import asset_core as A
from reference_geometry import unproject,AZ,EL,set_color
from blender_runtime import configure_cycles
FPS=24000/1001
CAM=json.loads((P/'intro_camera.json').read_text())
TIMING=json.loads((P/'intro_timing.json').read_text())
STATE={}

def frame(t):return round(t*FPS)+1

def key(ob,path,t,value,index=-1):
 if index>=0:getattr(ob,path)[index]=value
 else:setattr(ob,path,value)
 ob.keyframe_insert(data_path=path,frame=frame(t),index=index)

def linear(ob):
 if ob.animation_data and ob.animation_data.action:
  action=ob.animation_data.action
  for layer in action.layers:
   for strip in layer.strips:
    if hasattr(strip,'channelbags'):
     for bag in strip.channelbags:
      for curve in bag.fcurves:
       for point in curve.keyframe_points:point.interpolation='LINEAR'

def empty(name,collection=None):
 ob=bpy.data.objects.new(name,None);(collection or STATE['props']).objects.link(ob)
 ob.empty_display_type='PLAIN_AXES';ob.empty_display_size=.5
 return ob

def asset(id):return next(c for c in bpy.data.collections if c.get('asset_id')==id)
def instance(id):return next(o for o in bpy.context.scene.objects if o.get('library_asset')==id)

def group_objects(name,objects,col=None):
 root=empty(name,col)
 for ob in objects:
  if ob.parent not in objects:
   matrix=ob.matrix_world.copy();ob.parent=root;ob.matrix_world=matrix
 return root

def emit(name,fn):
 A.flush();before=set(A.COL.objects);A.part(name);fn();A.flush()
 return group_objects(name+' rig',list(set(A.COL.objects)-before))

def material(name,color,rough=.65,metal=0):return A.material(name,color,rough,metal)

def scale_window(root,start,end,enter=True,axis=None):
 values=(.0001,1.) if enter else (1.,.0001)
 if axis is None:
  for t,v in [(0,values[0]),(start,values[0]),(end,values[1])]:key(root,'scale',t,(v,v,v))
 else:
  for t,v in [(0,values[0]),(start,values[0]),(end,values[1])]:key(root,'scale',t,v,axis)
 linear(root)

def set_visible(ob,time,visible):
 key(ob,'hide_render',time,not visible);key(ob,'hide_viewport',time,not visible)

def setup():
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/'city_measured_standalone.blend'))
 s=bpy.context.scene;s.frame_set(60)
 for ob in s.objects:
  if ob.type=='LIGHT':
   ob.animation_data_clear();ob.data.animation_data_clear()
 s.animation_data_clear();s.frame_start=1;s.frame_end=261;s.render.fps=24;s.render.fps_base=1.001
 s.name='Silicon Valley • season-one reconstructed shot'
 props=bpy.data.collections.new('INTRO • animated props');s.collection.children.link(props);STATE['props']=props
 A.COL=props;A.BATCH=defaultdict(lambda:[[],[]]);A.MAT={m.name:m for m in bpy.data.materials};A.FONTS={}
 for name,color in [('intro_yellow',(.95,.61,.006)),('intro_black',(.008,.011,.014)),('intro_white',(.86,.88,.84)),('intro_glass',(.065,.16,.20)),('intro_red',(.68,.01,.025)),('intro_blue',(.028,.22,.52)),('intro_green',(.015,.42,.21)),('intro_purple',(.12,.017,.43)),('intro_concrete',(.60,.59,.54)),('intro_brown',(.22,.095,.04)),('intro_cyan',(.012,.44,.60)),('intro_android',(.23,.72,.003))]:material(name,color)
 material('intro_chrome',(.34,.37,.40),.34,.45)
 # Match the measured projected scale and translation at every video frame.
 base=s.camera;cam=base.copy();cam.data=base.data.copy();props.objects.link(cam);cam.name='INTRO • measured moving camera';s.camera=cam
 right=base.matrix_world.col[0].xyz;up=base.matrix_world.col[1].xyz;origin=base.location.copy()
 for f in range(1,262):
  t=min((f-1)/FPS,CAM['hold_time']);k=CAM['start']['scale']+CAM['per_second']['scale']*t
  tx,ty=[a+b*t for a,b in zip(CAM['start']['translation'],CAM['per_second']['translation'])]
  dx=((640-tx)/k-640)/5;dy=-((360-ty)/k-360)/5
  cam.location=origin+right*dx+up*dy;cam.keyframe_insert(data_path='location',frame=f)
  cam.data.ortho_scale=256/k;cam.data.keyframe_insert(data_path='ortho_scale',frame=f)
 linear(cam);linear(cam.data);cam.data.dof.use_dof=False
 for m in bpy.data.materials:
  if m.name.startswith('title_roof_red'):set_color(m,(.34,.006,.029))
 sun=next(o for o in s.objects if o.type=='LIGHT' and o.data.type=='SUN')
 for t,elev,color in [(0,40,(1,.88,.75)),(7.64,46,(1,.95,.88))]:
  angle=math.radians(elev);az=math.radians(138)
  direction=Vector((math.cos(az)*math.cos(angle),math.sin(az)*math.cos(angle),math.sin(angle)))
  sun.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();sun.keyframe_insert(data_path='rotation_euler',frame=frame(t))
  sun.data.color=color;sun.data.keyframe_insert(data_path='color',frame=frame(t))
 sun.data.energy=3.4;sun.data.angle=.032;linear(sun);linear(sun.data)
 s.render.engine='CYCLES';configure_cycles(s);s.cycles.samples=16;s.cycles.use_denoising=True;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.045;s.cycles.max_bounces=4;s.cycles.diffuse_bounces=2;s.cycles.glossy_bounces=2;s.cycles.transmission_bounces=2;s.cycles.transparent_max_bounces=6
 s.render.use_persistent_data=True;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
 s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
 if hasattr(s.render,'use_motion_blur'):s.render.use_motion_blur=True;s.render.motion_blur_shutter=.22
 s.use_nodes=True;n=s.node_tree.nodes;n.clear();links=s.node_tree.links
 layers=n.new('CompositorNodeRLayers');sat=n.new('CompositorNodeHueSat');sat.inputs['Saturation'].default_value=1.0
 fade=n.new('CompositorNodeMixRGB');fade.blend_type='MULTIPLY';fade.inputs[0].default_value=1
 for f,value in [(1,1),(250,1),(258,0),(261,0)]:fade.inputs[2].default_value=(value,value,value,1);fade.inputs[2].keyframe_insert(data_path='default_value',frame=f)
 comp=n.new('CompositorNodeComposite');links.new(layers.outputs['Image'],sat.inputs['Image']);links.new(sat.outputs['Image'],fade.inputs[1]);links.new(fade.outputs[0],comp.inputs[0])
 s['intro_reference']='Season-one 261-frame source at 24000/1001 fps';s['intro_scope']='Native animated reconstruction; geometry and secondary motion remain under comparison.'
 print('INTRO_STAGE_SETUP',flush=True)

def build_height_group():
 group=bpy.data.node_groups.new('INTRO • preserve completed floors below construction height','GeometryNodeTree')
 group.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry')
 group.interface.new_socket(name='Height',in_out='INPUT',socket_type='NodeSocketFloat')
 group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
 nodes=group.nodes;links=group.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');position=nodes.new('GeometryNodeInputPosition');sep=nodes.new('ShaderNodeSeparateXYZ');combine=nodes.new('ShaderNodeCombineXYZ');clamp=nodes.new('ShaderNodeMath');clamp.operation='MINIMUM';setpos=nodes.new('GeometryNodeSetPosition')
 links.new(position.outputs[0],sep.inputs[0]);links.new(sep.outputs['X'],combine.inputs['X']);links.new(sep.outputs['Y'],combine.inputs['Y']);links.new(sep.outputs['Z'],clamp.inputs[0]);links.new(inp.outputs['Height'],clamp.inputs[1]);links.new(clamp.outputs[0],combine.inputs['Z']);links.new(combine.outputs[0],setpos.inputs['Position']);links.new(inp.outputs['Geometry'],setpos.inputs['Geometry']);links.new(setpos.outputs[0],out.inputs[0])
 return group

def titles():
 col=asset('title_towers');inst=instance('title_towers');parts=defaultdict(list)
 for ob in list(col.objects):
  if ob.type!='MESH':continue
  m=re.match(r'(front_\d+_[A-Z]|rear_\d+_[A-Z])',ob.get('part',ob.name))
  id=m.group(1) if m else 'front_6_Y';parts[id].append(ob)
 group=build_height_group();socket=next(i for i in group.interface.items_tree if i.name=='Height' and i.in_out=='INPUT').identifier
 summary=[]
 for id,objects in parts.items():
  root=empty('BUILD • '+id,col);start,end=TIMING['title'][id]
  maxz=max((ob.matrix_world@v.co).z for ob in objects for v in ob.data.vertices)
  root['construction_height']=0.
  for t,h in [(0,0),(start,0),(start+.14,maxz*.035),((start+end)/2,maxz*.5),(end,maxz+.5)]:
   root['construction_height']=h;root.keyframe_insert(data_path='["construction_height"]',frame=frame(t))
  linear(root)
  for ob in objects:
   # Normalize mesh coordinates before clamping; completed facade courses retain their height.
   ob.data=ob.data.copy();ob.data.transform(ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
   mod=ob.modifiers.new('Construction elevation','NODES');mod.node_group=group;mod[socket]=0
   curve=mod.driver_add('["'+socket+'"]');variable=curve.driver.variables.new();variable.name='height';variable.type='SINGLE_PROP';variable.targets[0].id=root;variable.targets[0].data_path='["construction_height"]';curve.driver.expression='height'
   set_visible(ob,0,False);set_visible(ob,start,True)
   if any(m and m.name.startswith('title_roof_red') for m in ob.data.materials):
    set_visible(ob,start,False);set_visible(ob,end-.10,True)
  center=sum((ob.matrix_world@Vector(c) for ob in objects for c in ob.bound_box),Vector())/(len(objects)*8)
  summary.append({'letter':id,'start':start,'end':end,'height':maxz,'world_center':list(inst.matrix_world@Vector((center.x,center.y,0)))})
 STATE['title_summary']=summary
 from mathutils.geometry import convex_hull_2d
 points=[Vector((v[0],v[1])) for q in summary for v in [q['world_center']]]
 hull=convex_hull_2d(points);center=sum(points,Vector((0,0)))/len(points)
 outline=[tuple(center+(points[i]-center)*1.13) for i in hull]
 A.part('Early title-site green');lawn=A.polygon('Early title-site grass',outline,-.078,.006,'grass',False)
 set_visible(lawn,0,True);set_visible(lawn,3.88,False)
 # Low pavilions occupy the future title plot before redevelopment.
 for i,(pix,w,d) in enumerate([((808,132),17,12),((869,108),19,12),((936,153),19,12),((885,204),17,12)]):
  def office():
   A.box('Early site office', (0,0,1.8),(w,d,3.6),'intro_concrete')
   for z in (1.0,2.3):
    A.box('Low office glazing',(0,-d/2-.015,z),(w-.3,.035,.7),'intro_glass');A.box('Return glazing',(w/2+.015,0,z),(.035,d-.3,.7),'intro_glass')
   A.box('Office pale flat roof',(0,0,3.68),(w+.4,d+.4,.20),'intro_white')
  root=emit('Former title-site pavilion '+str(i+1),office);root.location=unproject(pix,0);scale_window(root,3.1+i*.18,3.65+i*.18,False,2)
 print('INTRO_STAGE_TITLES',len(parts),flush=True)

def brands():
 # YouTube grows from a small roof mark and a lower office to its late-shot height.
 col=asset('youtube');objects=list(col.objects);rig=group_objects('YouTube rising office',objects,col)
 for t,v in [(0,.65),(.9,.65),(3.15,1)]:key(rig,'scale',t,v,2)
 linear(rig)
 sign=next(o for o in objects if o.type=='EMPTY' and o.name.startswith('YouTube vector sign'))
 for t,v in [(0,.26),(.9,.26),(2.3,1)]:key(sign,'scale',t,(v,v,v))
 linear(sign)
 for ob in objects:
  if 'Google' in ob.name:set_visible(ob,0,False);set_visible(ob,2.2,True)
 # Google emerges from the preceding SGI identity.
 col=asset('google');objects=[o for o in col.objects if 'Google' in o.name or 'Original Google roof lettering' in o.get('part','')]
 for ob in objects:set_visible(ob,0,False);set_visible(ob,2.1,True)
 A.COL=STATE['props'];q=unproject((432,497),14.1)
 def sgi():
  ob=A.text('SGI historical roof letters','sgi',(0,0,0),10,'intro_purple',width=17,depth=.22);ob.data.shear=.03
 root=emit('SGI to Google transition',sgi);root.location=q;scale_window(root,1.65,2.12,False)
 # Apple rainbow sign becomes the Pets.com roof sign.
 col=asset('pets_com')
 for ob in col.objects:
  if 'billboard' in ob.get('part','').lower():set_visible(ob,0,False);set_visible(ob,1.4,True)
 def rainbow():A.logo('apple',(0,0,0),9,.4,'intro_white',(math.pi/2,0,0),rainbow=True)
 root=emit('Historical rainbow Apple billboard',rainbow);root.location=unproject((295,352),7.9);scale_window(root,.75,1.4,False)
 # Digg replaces Netscape; the earlier Android roof figure leaves with it.
 col=asset('netscape_digg')
 for ob in col.objects:
  if 'billboard' in ob.get('part','').lower() or 'Digg board' in ob.name:set_visible(ob,0,False);set_visible(ob,1.85,True)
 def netscape():
  A.box('Netscape blue sign backing',(0,.12,1.9),(17,.6,4.5),'intro_glass');A.text('Netscape sign','Netscape',(0,-.25,.45),3.2,'intro_white',width=16,depth=.07)
 root=emit('Netscape to Digg sign',netscape);root.location=unproject((455,367),6.5);scale_window(root,1.25,1.85,False)
 def android():
  A.box('Android torso',(0,0,3.7),(3.0,.55,3.2),'intro_android',bevel=.20)
  A.sphere('Android domed head',(0,0,5.5),(1.6,.42,1.15),'intro_android',24,12)
  for x in (-1,1):
   A.rod('Android antenna',(x*.72,0,6.0),(x*1.30,0,7.0),.10,'intro_android');A.rod('Android arm',(x*1.95,0,4.8),(x*1.95,0,2.6),.32,'intro_android');A.rod('Android leg',(x*.83,0,2.2),(x*.83,0,.4),.34,'intro_android');A.sphere('Android eye',(x*.57,-.42,5.57),(.12,.07,.12),'intro_white')
 root=emit('Early Android roof figure',android);root.location=unproject((475,312),11);scale_window(root,1.30,1.95,False)
 # Purple Myspace billboard transitions to the dark later identity.
 for m in bpy.data.materials:
  if m.name.startswith('myspace_sign'):
   shader=m.node_tree.nodes.get('Principled BSDF')
   for t,color in [(0,(.12,.015,.48,1)),(2.85,(.12,.015,.48,1)),(3.6,(.045,.052,.054,1))]:shader.inputs['Base Color'].default_value=color;shader.inputs['Base Color'].keyframe_insert(data_path='default_value',frame=frame(t))
 # The circular Apple structure rises after the construction-field phase.
 root=instance('apple');scale_window(root,*TIMING['apple_ring'],True,2)
 cloth=instance('blue_sculpture')
 for t,v in [(0,.0001),(4.1,.0001),(4.7,1)]:key(cloth,'scale',t,(v,v,v))
 linear(cloth)
 print('INTRO_STAGE_BRANDS',flush=True)

def crane(name,pixel,height,length,phase):
 base=emit(name+' tower',lambda:None);base.location=unproject(pixel,0)
 def mast():
  for x,y in [(-.48,-.48),(.48,-.48),(.48,.48),(-.48,.48)]:A.rod('Crane mast chord',(x,y,0),(x,y,height),.065,'intro_yellow',6)
  for z in range(0,math.ceil(height),2):
   for a,b in [((-.48,-.48),(.48,-.48)),((.48,-.48),(.48,.48)),((.48,.48),(-.48,.48)),((-.48,.48),(-.48,-.48))]:
    A.rod('Mast diagonal',(*a,z),(*b,min(z+2,height)),.043,'intro_yellow',5);A.rod('Mast crossbar',(*a,z),(*b,z),.045,'intro_yellow',5)
  A.box('Crane footing',(0,0,.25),(2.3,2.3,.5),'intro_concrete')
 mastroot=emit(name+' lattice mast',mast);mastroot.parent=base
 def jib():
  for y,z in [(-.48,0),(.48,0),(0,.85)]:A.rod('Triangular jib chord',(-5,y,z),(length,y,z),.06,'intro_yellow',6)
  for x in range(-5,math.ceil(length),2):
   for y in (-.48,.48):A.rod('Jib cross bracing',(x,y,0),(min(x+2,length),0,.85),.035,'intro_yellow',5)
  A.box('Counterweight',(-4.1,0,.65),(2.4,1.8,1.3),'intro_concrete');A.box('Operator cabin',(1.0,-.9,-.42),(2,1.3,1.3),'intro_yellow');A.box('Cab glazing',(1,-1.57,-.38),(1.7,.03,.87),'intro_glass');A.rod('Stay post',(0,0,.4),(0,0,4.4),.09,'intro_yellow');A.rod('Forward support cable',(0,0,4.4),(length*.8,0,.8),.028,'intro_black');A.rod('Rear support cable',(0,0,4.4),(-5,0,.8),.025,'intro_black')
 top=emit(name+' rotating jib',jib);top.parent=base;top.location.z=height
 def hook():A.rod('Hoist cable',(0,0,0),(0,0,-6),.027,'intro_black',5);A.box('Yellow hook block',(0,0,-6.1),(.46,.42,.65),'intro_yellow')
 trolley=emit(name+' moving hoist',hook);trolley.parent=top;trolley.location.x=length*.55
 for t in [0,2,4,6,8,10.9]:
  key(top,'rotation_euler',t,phase+.65*math.sin(t*1.4+phase),2);key(trolley,'location',t,length*(.5+.25*math.sin(t*1.1+phase)),0)
 initial=1. if phase>2.8 else .0001
 for t,v in [(0,initial),(2.8+phase*.04,initial),(4.3+phase*.04,1),(6.8+phase*.1,1),(8.15+phase*.05,.0001)]:key(base,'scale',t,(v,v,v))
 linear(top);linear(trolley);linear(base)
 return base

def props():
 A.COL=STATE['props']
 for i,(pixel,h,l) in enumerate([((840,167),31,24),((912,152),35,22),((984,228),28,22),((874,269),30,21),((1025,354),25,19),((1120,368),22,17)]):crane('Construction crane '+str(i+1),pixel,h,l,i*.73)
 # The purple balloon inflates, rises and collapses onto the measured cloth position.
 def balloon():
  A.sphere('Purple balloon envelope',(0,0,0),(3.6,3.4,5.3),'intro_purple',40,28)
  A.sphere('Pale face on balloon',(0,-2.94,-.1),(2.6,.65,3.05),'intro_white',32,20)
  for x in (-1,1):A.sphere('Purple eyebrow',(x*1.1,-3.51,.75),(1.15,.20,.40),'intro_purple',16,10)
  A.sphere('Purple mouth',(0,-3.53,-1.0),(1.15,.20,.45),'intro_purple',20,10)
  A.box('Balloon basket',(0,0,-7.3),(1.55,1.35,1.15),'intro_brown')
  for x,y in [(-.67,-.56),(.67,-.56),(.67,.56),(-.67,.56)]:A.rod('Basket suspension',(x*2,y*2,-4.2),(x,y,-6.8),.033,'intro_brown',5)
 root=emit('Purple balloon flight',balloon);p=unproject((983,451),0);root.location=p;root.rotation_euler.z=AZ-math.pi/4
 for t,z,v in [(0,1,.001),(1.85,1,.001),(2.55,16,1),(3.30,20,1),(3.85,17,.95),(4.25,9,.55),(4.65,.4,.001)]:
  key(root,'location',t,z,2);key(root,'scale',t,(v,v,v))
 linear(root)
 # Mobile articulated machines occupy the green ring construction site.
 for i,pixel in enumerate([(969,363),(1010,404),(1075,384),(1116,357),(1023,339),(939,401)]):
  def machine():
   A.box('Tracked chassis',(0,0,.7),(3.1,2.1,1.2),'intro_yellow');A.box('Black crawler left',(0,-1.1,.43),(3.5,.65,.65),'intro_black');A.box('Black crawler right',(0,1.1,.43),(3.5,.65,.65),'intro_black');A.box('Cabin glass',(-.45,0,1.65),(1.4,1.5,1.1),'intro_glass')
  machine_root=emit('Excavator '+str(i+1),machine);machine_root.location=unproject(pixel,0);machine_root.rotation_euler.z=i*1.17
  def arm():A.rod('Hydraulic main boom',(0,0,0),(3.3,0,4.1),.25,'intro_yellow');A.rod('Hydraulic piston',(0,0,.6),(2.5,0,3.4),.11,'intro_chrome');A.rod('Dipper',(3.3,0,4.1),(5.0,0,1.4),.22,'intro_yellow');A.box('Excavator bucket',(5.2,0,1.0),(1.3,1.4,.9),'intro_yellow')
  boom=emit('Excavator arm '+str(i+1),arm);boom.parent=machine_root;boom.location.z=1.3
  for t in [0,1,2,3,4,5,6,7,8,10.9]:key(boom,'rotation_euler',t,.28*math.sin(t*4+i),1)
  linear(boom)
  for t,v in [(0,1),(6.3+i*.07,1),(7.4+i*.07,.001)]:key(machine_root,'scale',t,(v,v,v))
  linear(machine_root)
 print('INTRO_STAGE_CRANES_BALLOON_MACHINES',flush=True)

def catmull(points,n=20):
 p=[Vector(x) for x in points];out=[]
 for i in range(len(p)-1):
  a,b,c,d=p[max(0,i-1)],p[i],p[i+1],p[min(len(p)-1,i+2)]
  for j in range(n):
   t=j/n;out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 out.append(p[-1]);return out

def traffic():
 # Replace batched static traffic with independently animated vehicles.
 for ob in list(bpy.context.scene.objects):
  if ob.get('part','').startswith('Traffic') or ob.name.startswith('Traffic •'):bpy.data.objects.remove(ob,do_unlink=True)
 tree=ast.parse((P/'assemble_city.py').read_text());roads=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ROAD_DATA' for t in n.targets))
 random.seed(851);num=0
 for road_index,(name,pixels,width) in enumerate(roads[:7]):
  points=catmull([unproject(p,0) for p in pixels]);lengths=[0]
  for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+(b-a).length)
  for vehicle in range(7):
   color=['intro_blue','intro_red','intro_green','intro_white','intro_yellow'][vehicle%5];van=vehicle%4==0
   def model():
    A.box('Car body',(0,0,.52),(2.85,1.25,.68),color,bevel=.13)
    A.box('Car glazing',(-.13,0,1.02),(1.75,1.13,.57),'intro_glass',bevel=.15)
    A.box('Painted roof',(-.12,0,1.34),(1.35,1.0,.12),color,bevel=.06)
    if van:A.box('Van cargo body',(-.55,0,1.25),(1.8,1.3,1.12),color,bevel=.08)
    for x in (-.90,.92):
     for side in (-1,1):A.rod('Rubber tire',(x,side*.52,.35),(x,side*.72,.35),.32,'intro_black',12);A.rod('Wheel hub',(x,side*.73,.35),(x,side*.75,.35),.13,'intro_chrome',10)
    for y in (-.40,.40):A.box('Headlight',(1.44,y,.65),(.03,.23,.13),'intro_white');A.box('Tail lamp',(-1.44,y,.66),(.025,.20,.13),'intro_red')
   car=emit(name+' moving vehicle '+str(vehicle+1),model);offset=random.uniform(0,lengths[-1]);speed=random.uniform(10,19);lane=-1 if vehicle%2 else 1
   import bisect
   for f in range(1,262):
    distance=(offset+lane*speed*(f-1)/FPS)%lengths[-1];j=max(0,min(len(points)-2,bisect.bisect_right(lengths,distance)-1));t=(distance-lengths[j])/max(1e-6,lengths[j+1]-lengths[j]);direction=(points[j+1]-points[j]).normalized();pos=points[j].lerp(points[j+1],t)+Vector((-direction.y,direction.x,0))*width*.23*lane
    car.location=pos;car.rotation_euler.z=math.atan2(direction.y,direction.x)+(math.pi if lane<0 else 0);car.keyframe_insert(data_path='location',frame=f);car.keyframe_insert(data_path='rotation_euler',frame=f,index=2)
   linear(car);num+=1
 STATE['moving_vehicles']=num
 print('INTRO_STAGE_TRAFFIC',num,flush=True)

def shot_details():
 """Reconstruct the office/sign variant visible behind the finished title."""
 A.COL=STATE['props']
 for ob in asset('twitter').objects:
  if 'Google' in ob.get('part',''):ob.hide_render=True;ob.hide_viewport=True
 for mat in bpy.data.materials:
  if mat.name.startswith('asphalt'):set_color(mat,(.008,.009,.008))
  elif mat.name.startswith('grass'):set_color(mat,(.085,.34,.003))
  elif mat.name.startswith('title_roof_red'):
   shader=mat.node_tree.nodes.get('Principled BSDF')
   for link in list(shader.inputs['Base Color'].links):mat.node_tree.links.remove(link)
   shader.inputs['Base Color'].default_value=(.42,.013,.049,1);mat.diffuse_color=(.42,.013,.049,1)
 # Intro-only HP office. Roof corners are observed in the video through the fitted camera.
 height=23.0;roof=[[1046,121],[1076,107],[1163,154],[1133,167]]
 points=[unproject(p,height) for p in roof];foot=[(p.x,p.y) for p in points]
 def hp_building():
  A.polygon('HP office glazing envelope',foot,0,height,'intro_glass')
  for a,b in zip(points,points[1:]+points[:1]):
   v=b-a;u=v.normalized();normal=Vector((u.y,-u.x,0));mid=(a+b)/2;angle=math.atan2(u.y,u.x)
   for k in range(9):
    z=k*height/8;A.box('HP cream floor band',(mid.x,mid.y,z),(v.length+.06,.24,.72),'intro_white',angle)
   bays=max(2,round(v.length/1.35))
   for j in range(bays+1):
    q=a.lerp(b,j/bays)+normal*.03;A.box('HP narrow vertical pier',(q.x,q.y,height/2),(.075,.26,height),'intro_white',angle)
  A.polygon('HP broad pale roof',foot,height,.28,'intro_white')
  for j in range(5):
   a=points[0].lerp(points[3],(j+.6)/6);b=points[1].lerp(points[2],(j+.6)/6);mid=(a+b)/2;angle=math.atan2((b-a).y,(b-a).x)
   A.box('HP stepped rooftop rooflight',(mid.x,mid.y,height+.38),((b-a).length*.62,1.45,.22),'intro_cyan',angle)
 hp=emit('HP office beside the title',hp_building)
 # Raised cyan hp on a pale circular sign, with real letter geometry.
 a,b=points[0],points[3];u=(b-a).normalized();normal=Vector((u.y,-u.x,0));q=a.lerp(b,.24)+normal*.24
 def hp_sign():
  A.sphere('HP round white sign',(0,0,0),(3.3,.22,3.3),'intro_white',40,24)
  ob=A.text('HP cyan monogram','hp',(0,-.30,-2.45),5.6,'intro_cyan',width=5.5,depth=.18);ob.data.shear=.20
 sign=emit('HP circular facade identity',hp_sign);sign.location=(q.x,q.y,height-4.1);sign.rotation_euler.z=math.atan2(u.y,u.x)
 # Oracle replaces the intermediate solar roof with a white parapet, sign and occupied terrace.
 col=asset('yahoo_oracle')
 for ob in col.objects:
  if 'photovoltaic' in ob.name.lower() or 'racks' in ob.get('part','').lower():
   set_visible(ob,0,True);set_visible(ob,4.1,False)
 d=json.loads((P/'yahoo_oracle_measurements.json').read_text());H=13.6;roof=d['volumes'][1]['roof'];corners=[unproject(p,H) for p in roof]
 def terrace():
  for a,b in zip(corners,corners[1:]+corners[:1]):
   mid=(a+b)/2;A.box('Oracle rooftop white parapet',(mid.x,mid.y,H+.6),((b-a).length,.26,1.2),'intro_white',math.atan2((b-a).y,(b-a).x))
  for i in range(7):
   q=corners[0].lerp(corners[1],.2+.09*i).lerp(corners[3].lerp(corners[2],.2+.09*i),.35+.04*(i%3));A.person(q.x,q.y,H+.07,['red','white','blue'][i%3],i)
  q=sum(corners,Vector())/4;A.box('Oracle rooftop meeting table',(q.x,q.y,H+.7),(4.5,1.8,.15),'intro_brown')
 deck=emit('Oracle late-shot rooftop terrace',terrace)
 for ob in deck.children:set_visible(ob,0,False);set_visible(ob,4.1,True)
 a,b=corners[0],corners[3];u=(b-a).normalized();q=(a+b)/2+Vector((u.y,-u.x,0))*.28;angle=math.atan2(u.y,u.x)
 def oracle_sign():
  A.box('Oracle white fascia',(0,0,1.35),((b-a).length,.32,2.7),'intro_white');ob=A.text('Oracle red roof fascia letters','ORACLE',(0,-.19,.28),2.15,'intro_red',width=(b-a).length*.88,depth=.04);ob.data.space_character=1.15
 sign=emit('Oracle identity reveal',oracle_sign);sign.location=(q.x,q.y,H+.1);sign.rotation_euler.z=angle;scale_window(sign,3.8,4.15,True,2)
 print('INTRO_STAGE_HP_ORACLE_AND_PALETTE',flush=True)

def polish_motion():
 """Match season-one branding scale and keep vehicle rotations continuous."""
 from bpy_extras.object_utils import world_to_camera_view
 s=bpy.context.scene;s.frame_set(192)
 # Hooli is a smaller, more distant campus in this version of the moving shot.
 hooli=instance('hooli');hooli.scale=(.5,.5,.5);bpy.context.view_layer.update()
 pts=[world_to_camera_view(s,s.camera,hooli.matrix_world@ob.matrix_world@v.co) for ob in hooli.instance_collection.objects if 'sign' in ob.get('part','').lower() and ob.type=='MESH' for v in ob.data.vertices]
 center=((min(q.x for q in pts)+max(q.x for q in pts))*640,(2-min(q.y for q in pts)-max(q.y for q in pts))*360)
 target=((1436+1613)/3,(40+202)/3);k=CAM['end']['scale']
 delta=unproject((640+(target[0]-center[0])/k,460+(target[1]-center[1])/k),0)-unproject((640,460),0)
 hooli.location+=delta;hooli['intro_variant']='Half-size campus; sign aligned to the season-one held frame.'
 for mat in bpy.data.materials:
  if mat.name.startswith('title_roof_red'):
   shader=mat.node_tree.nodes.get('Principled BSDF')
   for link in list(shader.inputs['Base Color'].links):mat.node_tree.links.remove(link)
   color=(.599695,.007324,.032020,1);shader.inputs['Base Color'].default_value=color;mat.diffuse_color=color
 hpglass=material('intro_hp_glass',(.25,.39,.42),.55)
 for ob in STATE['props'].objects:
  if ob.name.startswith('HP office beside') and ob.type=='MESH':
   for i,mat in enumerate(ob.data.materials):
    if mat.name.startswith('intro_glass'):ob.data.materials[i]=hpglass
 balloon=next(o for o in STATE['props'].objects if o.name=='Purple balloon flight rig');balloon.rotation_euler.z=AZ
 col=asset('twitter')
 for label,selector,begin,end,startscale in [
  ('Blogger roof identity',lambda o:'rounded orange' in o.get('part',''),6.65,7.65,.30),
  ('Blogger Google facade identity',lambda o:'Google' in o.get('part',''),7.0,7.6,.001)]:
  objects=[o for o in col.objects if selector(o)]
  points=[o.matrix_world@v.co for o in objects if o.type=='MESH' for v in o.data.vertices]
  center=Vector(tuple((min(v[i] for v in points)+max(v[i] for v in points))/2 for i in range(3)))
  root=empty(label+' rig',col);root.matrix_world=Matrix.Translation(center)
  for ob in objects:
   matrix=ob.matrix_world.copy();ob.parent=root;ob.matrix_world=matrix
   if 'Google' in label:set_visible(ob,0,False);set_visible(ob,begin,True)
  for t,v in [(0,startscale),(begin,startscale),(end,1.)]:key(root,'scale',t,(v,v,v))
  linear(root)
 for ob in STATE['props'].objects:
  if 'moving vehicle' not in ob.name or not ob.animation_data or not ob.animation_data.action:continue
  for layer in ob.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for curve in bag.fcurves:
      if curve.data_path!='rotation_euler' or curve.array_index!=2:continue
      previous=None
      for point in curve.keyframe_points:
       angle=point.co.y
       if previous is not None:
        while angle-previous>math.pi:angle-=2*math.pi
        while angle-previous<-math.pi:angle+=2*math.pi
       point.co.y=angle;previous=angle
      curve.update()
 print('INTRO_STAGE_BRAND_SCALE_AND_CONTINUOUS_MOTION',flush=True)

def finish():
 s=bpy.context.scene
 # New sign curves are converted so the scene remains independent of system fonts.
 bpy.ops.object.select_all(action='DESELECT')
 texts=[o for o in s.objects if o.type=='FONT']
 for ob in texts:ob.select_set(True)
 if texts:bpy.context.view_layer.objects.active=texts[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.select_all(action='DESELECT')
 (ROOT/'animation/frames').mkdir(parents=True,exist_ok=True)
 s.frame_set(180);s.render.filepath='//frames/frame_';bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'animation/intro.blend'),compress=True,relative_remap=False)
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
 report={'frame_start':1,'frame_end':261,'fps':FPS,'duration':261/FPS,'title_buildings':STATE['title_summary'],'moving_vehicles':STATE['moving_vehicles'],'external_libraries':len(bpy.data.libraries),'camera':'Measured affine camera path from production still/video feature correspondences','status':'Animated reconstruction under visual comparison; secondary detail is inferred.'}
 (ROOT/'animation/manifest.json').write_text(json.dumps(report,indent=2)+'\n')
 print('INTRO_SCENE_SAVED',str(ROOT/'animation/intro.blend'),flush=True)

if __name__=='__main__':
 setup();titles();brands();props();traffic();shot_details();polish_motion();finish()
