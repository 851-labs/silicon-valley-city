"""Shared construction primitives. Architecture is specified separately per asset."""
import bpy, math, os, random, json
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from collections import defaultdict
from math import sin,cos,pi
from blender_runtime import configure_cycles
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COL=None; MAT={}; BATCH=defaultdict(lambda:[[],[]]); PART='Structure'

def reset(asset_id,label,refs):
 global COL,MAT,BATCH,PART,FONTS
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 for c in list(bpy.data.collections):bpy.data.collections.remove(c)
 for m in list(bpy.data.materials):bpy.data.materials.remove(m)
 for d in list(bpy.data.curves):
  if d.users==0:bpy.data.curves.remove(d)
 BATCH=defaultdict(lambda:[[],[]]);MAT={};PART='Structure';FONTS={}
 COL=bpy.data.collections.new('ASSET • '+label);bpy.context.scene.collection.children.link(COL)
 COL['asset_id']=asset_id;COL['references']=', '.join(refs);COL['units']='metres; scale inferred from floor heights';COL['version']='fidelity-3'
 COL.asset_mark();COL.asset_data.description=label+' — reconstructed from original yU+co production references.'
 palette={'stone':(.61,.58,.51),'cream':(.82,.77,.65),'white':(.88,.89,.85),'roof':(.67,.66,.61),'dark':(.035,.044,.047),'black':(.008,.01,.012),'glass':(.12,.25,.28),'glass_blue':(.12,.205,.23),'glass_light':(.24,.30,.31),'metal':(.32,.37,.39),'frame':(.73,.74,.69),'copper':(.65,.24,.11),'blue':(.015,.14,.63),'cyan':(.035,.265,.37),'red':(.78,.009,.018),'yellow':(.97,.67,.009),'green':(.04,.49,.16),'android':(.23,.72,.003),'purple':(.29,.03,.49),'facebook':(.023,.049,.16),'turquoise':(.015,.40,.30),'solar':(.008,.045,.105),'solarline':(.29,.43,.50),'grass':(.12,.32,.009),'tree':(.14,.30,.016),'wood':(.27,.12,.039),'orange':(.97,.31,.008),'pool':(.08,.38,.48),'road':(.025,.024,.023),'paving':(.35,.35,.32),'hooli':(.54,.71,.004)}
 for n,c in palette.items():material(n,c,rough=.24 if n.startswith('glass') else .52,metal=.27 if n in ('metal','frame') else 0)
 for n in ('stone','cream','white','roof','paving','turquoise','wood'):surface_detail(MAT[n],.035 if n!='wood' else .065)
 for n,c in [('leaf_olive',(.20,.29,.038)),('leaf_light',(.27,.36,.064)),('leaf_dark',(.069,.18,.022))]:
  surface_detail(material(n,c,.93),.025)
 for n in ['grass','tree','leaf_olive','leaf_light','leaf_dark']:
  shader=MAT[n].node_tree.nodes['Principled BSDF'];shader.inputs['Roughness'].default_value=.94;shader.inputs['Specular IOR Level'].default_value=.04
 # Cell seams live in panel UV space, so every tilted module has the same 6 x 10 cells.
 m=MAT['solar'];nd=m.node_tree.nodes;lk=m.node_tree.links;p=nd.get('Principled BSDF')
 uv=nd.new('ShaderNodeTexCoord');brick=nd.new('ShaderNodeTexBrick');brick.offset=0
 brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=1/6;brick.inputs['Row Height'].default_value=.1
 brick.inputs['Mortar Size'].default_value=.003;brick.inputs['Mortar Smooth'].default_value=.001
 brick.inputs['Color1'].default_value=(.026,.065,.12,1);brick.inputs['Color2'].default_value=(.041,.09,.15,1);brick.inputs['Mortar'].default_value=(.31,.38,.41,1)
 lk.new(uv.outputs['UV'],brick.inputs['Vector']);lk.new(brick.outputs['Color'],p.inputs['Base Color'])
 solar_surface(m)
 random.seed(42)
 return COL

def solar_surface(m):
 """Muted silicon cells retain their pattern under the low reference sun."""
 p=m.node_tree.nodes['Principled BSDF'];base=(.145,.17,.215,1)
 p.inputs['Base Color'].default_value=base;m.diffuse_color=base
 p.inputs['Metallic'].default_value=0;p.inputs['Roughness'].default_value=.65;p.inputs['Specular IOR Level'].default_value=.12
 for node in m.node_tree.nodes:
  if node.type=='TEX_BRICK':
   for key,color in [('Color1',(.12,.14,.18,1)),('Color2',(.17,.20,.25,1)),('Mortar',(.55,.55,.54,1))]:node.inputs[key].default_value=color
 m['surface_version']='reference-pv-2'

def part(name):
 global PART
 PART=name

def material(name,color,rough=.5,metal=0,trans=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Transmission Weight'].default_value=trans
 MAT[name]=m
 if any(k in name for k in ('_stone','_brick','_concrete','_slab')):surface_detail(m,.025)
 return m

def surface_detail(m,amplitude=.04,scale=38):
 """Fine aggregate and broad color variation, in physical object coordinates."""
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');base=tuple(p.inputs['Base Color'].default_value)
 tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3
 l.new(tc.outputs['Object'],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB')
 r.color_ramp.elements[0].position=.12;r.color_ramp.elements[0].color=tuple(v*.82 for v in base[:3])+(1,)
 r.color_ramp.elements[1].position=.88;r.color_ramp.elements[1].color=tuple(min(1,v*1.10) for v in base[:3])+(1,)
 l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.32;bump.inputs['Distance'].default_value=amplitude
 l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 return m

def mesh(name,verts,faces,mat,batch=True,smooth=False):
 if isinstance(mat,str):mat=MAT[mat]
 if batch:
  v,f=BATCH[(PART,mat.name)];o=len(v);v.extend(verts);f.extend(tuple(i+o for i in face) for face in faces);return None
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);me.update();ob=bpy.data.objects.new(name,me);COL.objects.link(ob)
 if mat.name=='solar':
  uv=me.uv_layers.new(name='Individual module cells')
  for f in me.polygons:
   for i,j in enumerate(f.loop_indices):uv.data[j].uv=((0,0),(1,0),(1,1),(0,1))[i%4]
 if smooth:
  for p in me.polygons:p.use_smooth=True
 return ob

def box(name,loc,size,mat,rot=0,bevel=0,batch=True):
 x,y,z=loc;w,d,h=(s/2 for s in size);c,s=cos(rot),sin(rot)
 vs=[(x+a*c-b*s,y+a*s+b*c,z+k) for a,b,k in [(-w,-d,-h),(w,-d,-h),(w,d,-h),(-w,d,-h),(-w,-d,h),(w,-d,h),(w,d,h),(-w,d,h)]]
 if not batch or bevel:vs=[(vx-x,vy-y,vz-z) for vx,vy,vz in vs]
 ob=mesh(name,vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat,batch and not bevel)
 if ob:ob.location=loc
 if bevel:
  mod=ob.modifiers.new('Small architectural edge bevel','BEVEL');mod.width=bevel;mod.segments=3
  mod=ob.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return ob

def cylinder(name,loc,r,h,mat,n=48,r2=None):
 if r2 is None:r2=r
 x,y,z=loc;vs=[(x+rr*cos(i*2*pi/n),y+rr*sin(i*2*pi/n),z+zz) for rr,zz in [(r,-h/2),(r2,h/2)] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)

def rod(name,a,b,r,mat,n=10):
 a,b=Vector(a),Vector(b);t=(b-a).normalized();ref=Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0));u=t.cross(ref).normalized();v=t.cross(u)
 vs=[tuple(p+r*(cos(i*2*pi/n)*u+sin(i*2*pi/n)*v)) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)

def sphere(name,loc,scale,mat,n=12,rings=8):
 x,y,z=loc;vs=[(x+scale[0]*sin(pi*(j+.5)/rings)*cos(2*pi*i/n),y+scale[1]*sin(pi*(j+.5)/rings)*sin(2*pi*i/n),z+scale[2]*cos(pi*(j+.5)/rings)) for j in range(rings) for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple((rings-1)*n+i for i in range(n))]
 for j in range(rings-1):
  for i in range(n):a=j*n+i;b=j*n+(i+1)%n;fs.append((a,b,b+n,a+n))
 return mesh(name,vs,fs,mat)

def curve(name,pts,r,mat,closed=False):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=3;d.resolution_u=24
 p=d.splines.new('POLY');p.points.add(len(pts)-1)
 for v,co in zip(p.points,pts):v.co=(*co,1)
 p.use_cyclic_u=closed;d.materials.append(MAT[mat]);ob=bpy.data.objects.new(name,d);COL.objects.link(ob);return ob

def polygon(name,pts,z,h,mat,batch=True):
 vs=[(x,y,zz) for zz in (z,z+h) for x,y in pts];n=len(pts)
 vectors=[Vector((x,y,0)) for x,y in pts];lookup={(round(v.x,5),round(v.y,5)):i for i,v in enumerate(vectors)};faces=[]
 for tri in tessellate_polygon([vectors]):
  ids=tuple(v if isinstance(v,int) else lookup[(round(v.x,5),round(v.y,5))] for v in tri);faces.extend([tuple(reversed(ids)),tuple(i+n for i in ids)])
 faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
 return mesh(name,vs,faces,mat,batch)

def rounded(cx,cy,w,d,r,steps=12):
 pts=[]
 for x,y,a in [(cx+w/2-r,cy+d/2-r,0),(cx-w/2+r,cy+d/2-r,pi/2),(cx-w/2+r,cy-d/2+r,pi),(cx+w/2-r,cy-d/2+r,3*pi/2)]:
  pts.extend((x+r*cos(a+i*pi/(2*steps)),y+r*sin(a+i*pi/(2*steps))) for i in range(steps+1))
 return pts

def logo(name,loc,height,depth,mat='white',rot=(0,0,0),rainbow=False):
 data=json.load(open(os.path.join(ROOT,'source','logo_shapes.json')))
 root=bpy.data.objects.new(name+' vector sign assembly',None);COL.objects.link(root);root.location=loc;root.rotation_euler=rot
 items=data['apple_rainbow'] if rainbow else [{'points':p,'color':mat} for p in data[name]]
 for i,item in enumerate(items):
  ob=polygon(name+' outline '+str(i),[(x*height,y*height) for x,y in item['points']],0,depth,item['color'],False);ob.parent=root
 return root

def sign_panel(name,loc,w,h,mat,depth=.25,r=.25):
 # Plane XY footprint is remapped to a vertical XZ sign, with front facing -Y.
 pts=rounded(0,0,w,h,r,8);ob=polygon(name,pts,-depth/2,depth,mat,False);ob.rotation_euler=(pi/2,0,0);ob.location=loc;return ob

FONTS={}
def font(key):
 if key not in FONTS:
  filename={'regular':'Arial.ttf','bold':'Arial Bold.ttf','black':'Arial Black.ttf','narrow':'Arial Narrow Bold.ttf','serif':'Times New Roman Bold.ttf'}[key]
  path=os.path.join(os.environ.get('BLENDER_FONT_DIR','/System/Library/Fonts/Supplemental'),filename)
  FONTS[key]=bpy.data.fonts.load(path,check_existing=True) if os.path.isfile(path) else next((f for f in bpy.data.fonts if f.filepath=='<builtin>'),None)
 return FONTS[key]

def text(name,body,loc,size,mat,fontkey='bold',width=None,rot=(pi/2,0,0),align='CENTER',depth=.06):
 d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=font(fontkey);d.size=size;d.align_x=align;d.extrude=depth;d.bevel_depth=.008;d.bevel_resolution=2;d.resolution_u=12;d.materials.append(MAT[mat]);ob=bpy.data.objects.new(name,d);COL.objects.link(ob);ob.location=loc;ob.rotation_euler=rot
 if width:
  bpy.context.view_layer.update()
  if ob.dimensions.x>0:ob.scale.x*=width/ob.dimensions.x
 return ob

def colorword(word,loc,width,height,fontkey='regular',rot=(pi/2,0,0),depth=.13):
 if word=='Google' and os.path.exists(os.path.join(ROOT,'source','google_logo_mesh.json')):
  root=bpy.data.objects.new('Google 2013 vector sign assembly',None);COL.objects.link(root);root.location=loc;root.rotation_euler=rot
  for i,g in enumerate(json.load(open(os.path.join(ROOT,'source','google_logo_mesh.json')))):
   vs=[(x*width,y*width,z) for z in (0,depth) for x,y in g['vertices']];N=len(g['vertices']);fs=[]
   for t in g['faces']:fs.extend([tuple(reversed(t)),tuple(j+N for j in t)])
   off=0
   for count in g['rings']:
    fs.extend((off+j,off+(j+1)%count,off+(j+1)%count+N,off+j+N) for j in range(count));off+=count
   ob=mesh('Google original glyph '+str(i),vs,fs,g['color'],False);ob.parent=root
  return root
 colors=['blue','red','yellow','blue','green','red'] if word=='Google' else ['red','blue','yellow','green']
 obs=[];cursor=0
 for i,ch in enumerate(word):
  ob=text(word+' glyph '+str(i),ch,(0,0,0),height,colors[i%len(colors)],fontkey,align='LEFT',depth=depth,rot=(0,0,0));bpy.context.view_layer.update();w=ob.dimensions.x;obs.append((ob,cursor));cursor+=w+height*.008
 ratio=width/cursor
 # Parent keeps each glyph editable and supports placement on any facade.
 root=bpy.data.objects.new(word+' sign assembly',None);COL.objects.link(root);root.location=loc;root.rotation_euler=rot
 for ob,c in obs:ob.location=(c*ratio-width/2,0,0);ob.scale.x=ratio;ob.parent=root
 return root

def frame_facade(x,y,w,d,z,h,floors,bay=1.15,glass='glass',slab='cream',mullion=.065,band=.30):
 part('Glazing and facade frames')
 box('Glazed volume',(x,y,z+h/2),(w,d,h),glass)
 for k in range(floors+1):
  zz=z+k*h/floors;box('Front horizontal spandrel',(x,y-d/2-.035,zz),(w+.10,.10,band),slab);box('Rear horizontal spandrel',(x,y+d/2+.035,zz),(w+.10,.10,band),slab)
  box('West horizontal spandrel',(x-w/2-.035,y,zz),(.10,d,band),slab);box('East horizontal spandrel',(x+w/2+.035,y,zz),(.10,d,band),slab)
 for i in range(round(w/bay)+1):
  xx=x-w/2+i*w/max(1,round(w/bay))
  for yy in (y-d/2-.055,y+d/2+.055):box('Vertical glazing mullion',(xx,yy,z+h/2),(mullion,.13,h),slab)
 for i in range(round(d/bay)+1):
  yy=y-d/2+i*d/max(1,round(d/bay))
  for xx in (x-w/2-.055,x+w/2+.055):box('Vertical glazing mullion',(xx,yy,z+h/2),(.13,mullion,h),slab)

def hvac(x,y,z,w=1.5,d=1,h=.55):
 part('Rooftop mechanical equipment');box('AHU casing',(x,y,z+h/2),(w,d,h),'roof')
 for i in range(7):box('AHU louvre',(x-w*.42+i*w*.14,y-d/2-.012,z+h*.48),(.065,.03,h*.70),'dark')
 cylinder('Roof fan',(x,y,z+h+.018),min(w,d)*.29,.03,'metal',32)
 for i in range(5):box('Fan grille',(x,y+(i-2)*d*.085,z+h+.04),(w*.45,.018,.025),'dark')

def solar(x,y,z,w,d,rows=3,cols=6,rot=0,tilt=9):
 part('Photovoltaic roof panels')
 ca,sa=cos(rot),sin(rot);a=math.radians(tilt)
 for j in range(rows):
  for i in range(cols):
   xx=-w/2+(i+.5)*w/cols;yy=-d/2+(j+.5)*d/rows;ww=w/cols*.95;dd=d/rows*.87
   def q(u,v,h=0):
    u+=xx;v0=v*cos(a)+yy
    return(x+u*ca-v0*sa,y+u*sa+v0*ca,z+.045+(v+dd/2)*sin(a)+h)
   corners=[q(-ww/2,-dd/2),q(ww/2,-dd/2),q(ww/2,dd/2),q(-ww/2,dd/2)]
   mesh('Sixty-cell tilted photovoltaic module',corners,[(0,1,2,3)],'solar')
   for k in range(4):rod('Aluminium module perimeter',corners[k],corners[(k+1)%4],.018,'frame',4)
   for u in (-ww*.32,ww*.32):
    b=q(u,dd*.34,-.025);rod('Rear mounting leg',(b[0],b[1],z-.01),b,.023,'metal',4)

def umbrella(x,y,z,r=1.2,color='yellow'):
 part('Terrace furniture');rod('Parasol mast',(x,y,z),(x,y,z+1.8),.035,'metal');cylinder('Parasol foot',(x,y,z+.05),.18,.1,'dark',20)
 n=8;vs=[(x,y,z+2.1)]+[(x+r*cos(i*2*pi/n),y+r*sin(i*2*pi/n),z+1.75) for i in range(n)]
 mesh('Parasol fabric',vs,[(0,i+1,(i+1)%n+1) for i in range(n)],color)

def person(x,y,z,color='white',angle=0):
 part('People');box('Torso',(x,y,z+.93),(.32,.21,.51),color,angle);sphere('Head',(x,y,z+1.37),(.145,.145,.17),'cream',8,5)
 for dx in (-.10,.10):rod('Leg',(x+dx,y,z+.70),(x+dx,y,z+.10),.065,'dark',8)
 for dx in (-.24,.24):rod('Arm',(x+dx,y,z+1.12),(x+dx,y,z+.69),.05,'cream',8)

_TREE_SHAPE=None
def tree(x,y,z=0,r=1.1,h=3):
 global _TREE_SHAPE
 if _TREE_SHAPE is None:
  import bmesh
  bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1);bm.verts.ensure_lookup_table();lookup={v:i for i,v in enumerate(bm.verts)}
  _TREE_SHAPE=([tuple(v.co) for v in bm.verts],[tuple(lookup[v] for v in f.verts) for f in bm.faces]);bm.free()
 # A local seed keeps the tree's canopy stable when neighbouring props change.
 rng=random.Random(round(x*1931+y*781+z*31));angle=rng.uniform(0,2*pi);ca,sa=cos(angle),sin(angle)
 part('Trees');cylinder('Tapered russet trunk',(x,y,z+h*.30),max(.065,r*.075),h*.60,'wood',8,r2=.035)
 for i in range(3):
  a=angle+i*2*pi/3;rod('Forked crown branch',(x,y,z+h*.40),(x+r*.42*cos(a),y+r*.42*sin(a),z+h*.69),max(.025,r*.035),'wood',6)
 vs=[]
 for px,py,pz in _TREE_SHAPE[0]:
  rr=rng.uniform(.95,1.06);xx=px*r*rr;yy=py*r*.96*rr
  vs.append((x+xx*ca-yy*sa,y+xx*sa+yy*ca,z+h*.77+pz*h*.31))
 mesh('Single faceted broadleaf crown',vs,_TREE_SHAPE[1],rng.choice(['tree','leaf_olive','leaf_light','leaf_dark']))

def flush():
 for (group,mat),(vs,fs) in BATCH.items():
  if vs:
   ob=mesh(group+' • '+mat,vs,fs,MAT[mat],False);ob['part']=group
 BATCH.clear();bpy.context.view_layer.update()

def setup_preview(azimuth=35,elevation=25,width=1400,height=1050,white=False):
 # Asset cameras use the same local direction as the selected production view.
 profiles=os.path.join(ROOT,'source','asset_audit.json');profile={}
 if os.path.exists(profiles):
  profile=json.load(open(profiles)).get(COL.get('asset_id'),{})
  azimuth,elevation=profile.get('camera',[azimuth,elevation])
  COL['revision_notes']='; '.join(profile.get('changes',[]));COL['remaining_uncertainty']=profile.get('remaining','')
 s=bpy.context.scene;flush()
 intrinsic=profile.get('geometry_scale',[1,1,1])
 if 'applied_reference_proportions' not in COL:
  for ob in COL.objects:
   if ob.parent is None:
    for i in range(3):ob.location[i]*=intrinsic[i];ob.scale[i]*=intrinsic[i]
  COL['applied_reference_proportions']=intrinsic
  bpy.context.view_layer.update()
 points=[ob.matrix_world@Vector(c) for ob in COL.all_objects if ob.type in ('MESH','CURVE','FONT') for c in ob.bound_box]
 low=Vector(tuple(min(p[i] for p in points) for i in range(3)));high=Vector(tuple(max(p[i] for p in points) for i in range(3)));center=(low+high)/2
 studio=bpy.data.collections.new('STUDIO • cameras and light');s.collection.children.link(studio)
 a,e=math.radians(azimuth),math.radians(elevation);direction=Vector((sin(a)*cos(e),-cos(a)*cos(e),sin(e)))
 cd=bpy.data.cameras.new('Reference comparison camera');cam=bpy.data.objects.new('Reference comparison camera',cd);studio.objects.link(cam);cam.location=center+direction*max((high-low).length*2,100);cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.clip_end=5000;s.camera=cam
 inv=cam.rotation_euler.to_matrix().transposed();pro=[inv@(p-center) for p in points];ww=max(p.x for p in pro)-min(p.x for p in pro);hh=max(p.y for p in pro)-min(p.y for p in pro);cd.ortho_scale=max(ww,hh*width/height)*1.17
 world=bpy.data.worlds.new('Cool ambient sky');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.62,.74,1,1);world.node_tree.nodes['Background'].inputs[1].default_value=.38;s.world=world
 ld=bpy.data.lights.new('Low warm sun','SUN');ld.energy=3.3;ld.color=(1,.87,.70);ld.angle=.035;lo=bpy.data.objects.new('Low warm sun',ld);studio.objects.link(lo)
 # Key appears above the left of the image, with legible shadows on the right.
 sun=Vector((-cos(a)*.80-sin(a)*.18,-sin(a)*.80+cos(a)*.18,.66));lo.rotation_euler=(-sun).to_track_quat('-Z','Y').to_euler()
 s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
 configure_cycles(s)
 s.render.resolution_x=width;s.render.resolution_y=height;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=not white
 if white:
  n=world.node_tree.nodes;l=world.node_tree.links;camera_bg=n.new('ShaderNodeBackground');camera_bg.inputs[0].default_value=(1,1,1,1);camera_bg.inputs[1].default_value=20
  ray=n.new('ShaderNodeLightPath');mix=n.new('ShaderNodeMixShader');l.new(ray.outputs['Is Camera Ray'],mix.inputs[0]);l.new(n.get('Background').outputs[0],mix.inputs[1]);l.new(camera_bg.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n.get('World Output').inputs['Surface'])
 s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.70;s.render.fps=24
 s['reference_camera_angles']=f'azimuth {azimuth} degrees, elevation {elevation} degrees';s['asset_bounds']=list(low)+list(high)
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False;area.spaces.active.shading.type='MATERIAL';area.spaces.active.clip_end=5000
 bpy.ops.object.select_all(action='DESELECT');bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
 return s

def save_asset(asset_id,render=True):
 s=bpy.context.scene;out=os.path.join(ROOT,'assets',asset_id);os.makedirs(out,exist_ok=True)
 s.render.filepath='//preview.png';bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,asset_id+'.blend'),compress=True,relative_remap=False)
 print('ASSET_SAVED',asset_id,flush=True)
 if render:bpy.ops.render.render(write_still=True)
