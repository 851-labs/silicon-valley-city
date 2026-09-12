"""Measured western stadium roof, offset aperture, seating bowl and external frame."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'stadium_measurements.json'));A.reset('stadium','Western stadium • measured roof aperture, stepped bowl and open structure',['Original wide frame']);R=Reference(D['anchor'],D['crop']);H=D['height'];N=192
 for n,c,r in [('bowl_stone',(.62,.56,.455),.88),('bowl_white',(.89,.84,.74),.88),('bowl_seat',(.56,.38,.19),.87),('bowl_dark',(.23,.23,.19),.78),('bowl_field',(.19,.25,.035),.91)]:A.material(n,c,r)
 def ellipse(spec):
  x,y=spec['center'];rx,ry=spec['radii'];a=math.radians(spec['rotation_degrees']);return [R.p((x+rx*math.cos(t)*math.cos(a)-ry*math.sin(t)*math.sin(a),y+rx*math.cos(t)*math.sin(a)+ry*math.sin(t)*math.cos(a)),H) for t in [i*2*math.pi/N for i in range(N)]]
 outer,inner=ellipse(D['outer_ellipse']),ellipse(D['inner_ellipse']);center=sum(outer,Vector())/N
 def level(points,z,scale=1):return [(center.x+(q.x-center.x)*scale,center.y+(q.y-center.y)*scale,z) for q in points]
 def band(name,p0,p1,mat):A.mesh(name,p0+p1,[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],mat)
 A.part('Offset white annular roof');band('Measured broad white roof',level(outer,H),level(inner,H-.08),'bowl_white');band('Outer roof vertical fascia',level(outer,H),level(outer,H-.17),'bowl_white');band('Inner opening roof fascia',level(inner,H-.08),level(inner,H-.25),'bowl_white')
 A.part('Open upper concourse and concrete outer bowl');body=level(outer,0,1.055);bodypoints=[Vector(p) for p in body]
 band('Curved pale stadium wall',level(bodypoints,0),level(bodypoints,13.2),'bowl_stone')
 for z in [2.0,5.5,9.0,12.6]:band('Broad exterior concourse course',level(bodypoints,z,1.004),level(bodypoints,z+.62,1.004),'bowl_white')
 # The solid outer wall has isolated low concourse openings, not continuous dark stripes.
 for i in range(18):
  ids=[round((i+.12+j*.064)*N/18)%N for j in range(11)]
  v=[level(bodypoints,z,1.006)[j] for z in (2.0,3.5) for j in ids]
  A.mesh('Separate lower concourse opening',v,[(j,j+1,j+12,j+11) for j in range(10)],'bowl_dark')
 A.part('Stepped brown seating bowl')
 for k in range(25):
  scale=.36+.0176*k;z=1.0+.40*k;p0=level(outer,z,scale);p1=level(outer,z,scale+.0176);band('Individual seating tread',p0,p1,'bowl_seat');band('Individual seating riser',p1,level(outer,z+.40,scale+.0176),'bowl_stone')
 for i in range(32):
  j=round(i*N/32)%N;q=outer[j];t=(q-center).normalized();angle=math.atan2(t.y,t.x)
  for k in range(25):
   v=center+(q-center)*(.369+k*.0176);A.box('Radial stepped seating aisle',(v.x,v.y,1.04+.40*k),(.62,.44,.08),'bowl_stone',angle)
 A.polygon('Low oval field',[(p[0],p[1]) for p in level(outer,.28,.40)],.20,.08,'bowl_field')
 band('Inner upper bowl wall',level(inner,10.8,1.04),level(inner,12.1,1.04),'bowl_stone')
 A.part('Exposed upper structure and radial roof trusses')
 # The aperture also has a vertical trussed ring. Radial roof trusses alone
 # remain hidden above the aperture and cannot reproduce the visible back web.
 for z in [11.8,13.0,15.7]:
  pts=level(inner,z,1.015)
  for a,b in zip(pts,pts[1:]+pts[:1]):A.rod('Inner truss ring chord',a,b,.055,'bowl_stone',6)
 for i in range(20):
  j=round(i*N/20)%N;k=round((i+1)*N/20)%N
  a=Vector(level(inner,15.7,1.015)[j]);b=Vector(level(inner,11.8,1.015)[j]);c=Vector(level(inner,15.7,1.015)[k]);d=Vector(level(inner,11.8,1.015)[k])
  A.rod('Inner aperture upright',a,b,.12,'bowl_stone',8)
  mid=b.lerp(d,.5);mid.z=13.0
  A.rod('Inner aperture triangular truss',a,mid,.07,'bowl_stone',6);A.rod('Inner aperture triangular truss',mid,c,.07,'bowl_stone',6)
 for i in range(28):
  j=round(i*N/28)%N;q=Vector(body[j]);a=Vector(level(outer,H-.13,1.005)[j]);b=Vector(level(inner,H-.18)[j]);c=a.copy();c.z=13.25
  A.rod('Tall outer stadium column',(q.x,q.y,0),a,.12,'bowl_stone',8)
  A.rod('Radial upper roof chord',a,b,.085,'bowl_stone',8);A.rod('Diagonal roof support',c,b,.075,'bowl_stone',8)
  for f in [.25,.5,.75]:
   lower=c.lerp(b,f);upper=a.lerp(b,min(1,f+.25));A.rod('Roof truss triangular web',lower,upper,.045,'bowl_stone',6)
 A.COL['measurement_file']='source/stadium_measurements.json';A.COL['inferred_details']='Western off-frame oval arcs and field lines are inferred; the visible roof opening and external concourse system are independently reconstructed.'
 A.setup_preview(47.134,26.377,1200,1350);R.camera(6);return A
if __name__=='__main__':build();A.save_asset('stadium')
