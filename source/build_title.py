import os,sys,json,math,random
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from mathutils import Vector
from math import atan2

def build(data_override=None):
 A.reset('title_towers','SILICON VALLEY title architecture',['YU30','YU18','Season 1 final frame'])
 data=data_override or json.load(open(os.path.join(A.ROOT,'source','title_footprints.json')))
 A.material('title_glass_a',(.19,.25,.24),.32,.05);A.material('title_glass_b',(.24,.30,.28),.35,.03);A.material('title_glass_c',(.14,.205,.20),.30,.07);A.material('title_opaque',(.85,.80,.70),.63)
 # Warm coral in the original wide-frame grade; isolated studio art uses a deeper red.
 roof_red=A.material('title_roof_red',(.95,.10,.064) if '--studio-red' not in sys.argv else (.52,.018,.007),1.0)
 roof_red.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=0
 H=30.0;floors=9;floor=H/floors
 def cap(p,z,depth,mat):
  vs=[];fs=[]
  for t in p['triangles']:
   i=len(vs);vs.extend((x,y,zz) for zz in (z,z+depth) for x,y in t);fs.extend([(i+2,i+1,i),(i+3,i+4,i+5)])
  for ring in p['rings']:
   for a,b in zip(ring,ring[1:]+ring[:1]):
    i=len(vs);vs.extend([(a[0],a[1],z),(b[0],b[1],z),(b[0],b[1],z+depth),(a[0],a[1],z+depth)]);fs.append((i,i+1,i+2,i+3))
  A.mesh(p['id']+' slab',vs,fs,mat)
 for p in data['letters']:
  A.part(p['id']+' • structure')
  for j in range(floors+1):cap(p,j*floor,.65 if j not in (0,floors) else .55,'title_opaque')
  cap(p,H+.55,.12,'black');cap(p,H+.67,.06,'title_roof_red')
  opaque=p['id'] in ('front_4_L','front_5_E');garage=p['id']=='front_6_Y'
  for ri,ring in enumerate(p['rings']):
   area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]+ring[:1]))
   if (ri==0 and area<0) or (ri>0 and area>0):ring=list(reversed(ring))
   for a,b in zip(ring,ring[1:]+ring[:1]):
    a,b=Vector(a),Vector(b);v=b-a;length=v.length
    if length<.015:continue
    t=v/length;n=Vector((t.y,-t.x));is_opaque=opaque and n.y<-.9
    is_garage=garage and n.x>.94 and length>7
    if is_garage:
     A.part('Y • concrete parking tower with sloping glazed ramps')
     # In the photographed elevation the ramps sit behind an opaque concrete screen.
     aa=a-n*.10;bb=b-n*.10
     A.mesh('Solid parking screen above open entrance',[(aa.x,aa.y,4.6),(bb.x,bb.y,4.6),(bb.x,bb.y,H+.5),(aa.x,aa.y,H+.5)],[(0,1,2,3)],'title_opaque')
     for k in range(3):
      z0=6.4+k*7.4;start=a+t*length*.13+n*.02;end=b-t*length*.13+n*.02
      if k%2:start,end=end,start
      rise=2.2
      A.mesh('Inset sloping parking glazing',[(start.x,start.y,z0),(end.x,end.y,z0+rise),(end.x,end.y,z0+rise+2.5),(start.x,start.y,z0+2.5)],[(0,1,2,3)],'title_glass_c')
      for zz in (.0,.83,1.66,2.5):A.rod('Sloping blue window transom',(start.x,start.y,z0+zz),(end.x,end.y,z0+rise+zz),.060,'cyan',6)
      for j in range(17):
       q=start.lerp(end,j/16);zz=z0+rise*j/16
       A.rod('Parking ramp vertical mullion',(q.x,q.y,zz),(q.x,q.y,zz+2.5),.045,'frame',6)
     for q in (a+t*.3,b-t*.3):A.box('Ground entrance pier',(q.x,q.y,2.3),(.5,.5,4.6),'title_opaque')
     q=(a+b)/2+n*1.4
     A.sign_panel('Parking P backing',(q.x,q.y,2.9),2.2,2.8,'blue',.20,.05).rotation_euler=(math.pi/2,0,math.pi/2)
     A.text('Parking P','P',(q.x+.15,q.y,2.2),2.1,'white',rot=(math.pi/2,0,math.pi/2))
     A.rod('Entrance barrier',(a.x+.2,a.y+.9,1.25),(a.x-2.2,a.y+.9,1.25),.07,'yellow')
     continue
    A.part(p['id']+' • facade')
    aa=a-n*.11;bb=b-n*.11
    A.mesh('Facade backing',[(aa.x,aa.y,.1),(bb.x,bb.y,.1),(bb.x,bb.y,H+.5),(aa.x,aa.y,H+.5)],[(0,1,2,3)],'title_opaque' if is_opaque else 'title_glass_a')
    bays=max(1,round(length/(1.90 if is_opaque else .95)))
    for j in range(bays):
     q=a+t*(j+.5)*length/bays+n*.025;bay=length/bays
     if is_opaque:
      for k in range(floors):
       zz=k*floor+floor*.54
       A.box('Recess shadow around window',(q.x,q.y,zz),(bay*.61,.075,floor*.62),'dark',atan2(t.y,t.x))
       q2=q+n*.035
       A.box('Recessed square glazing',(q2.x,q2.y,zz),(bay*.50,.04,floor*.54),'title_glass_b',atan2(t.y,t.x))
       A.box('Stone window sill',(q.x+n.x*.09,q.y+n.y*.09,zz-floor*.31),(bay*.67,.22,.09),'frame',atan2(t.y,t.x))
     else:
      for k in range(floors):
       z0=k*floor+.70;z1=(k+1)*floor-.03
       left=q-t*bay*.465;right=q+t*bay*.465
       A.mesh('Individual glazed bay',[(left.x,left.y,z0),(right.x,right.y,z0),(right.x,right.y,z1),(left.x,left.y,z1)],[(0,1,2,3)],random.choice(['title_glass_a','title_glass_b','title_glass_c']))
      p0=a+t*j*length/bays+n*.065
      A.box('Continuous vertical mullion',(p0.x,p0.y,H/2),(.060,.115,H),'frame',atan2(t.y,t.x))
  A.COL[p['id']+' reference']='Roof outline traced from YU30; nine floors; façade visible in production still'
 s=A.setup_preview(data['camera']['azimuth'],data['camera']['elevation'],1800,1250,True)
 s['geometry_source']='Roof contours reconstructed directly from studio photograph; walls and garage modeled from visible reference.'
 return s

if __name__=='__main__':
 build();A.save_asset('title_towers','--no-render' not in sys.argv)
