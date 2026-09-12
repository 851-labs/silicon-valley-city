import os,sys,math,random
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from math import sin,cos,pi

def blue_sculpture():
 A.reset('blue_sculpture','Folded blue courtyard sculpture',['YU11','Original wide frame'])
 A.material('fold_blue',(.035,.065,.36),.78);A.material('fold_blue_light',(.19,.25,.68),.7)
 A.part('Rumpled blue and white sculpture')
 random.seed(983);N,M=48,12;vs=[]
 for j in range(M):
  v=j/(M-1)
  for i in range(N):
   t=i*2*pi/N;r=1-v*.9
   x=4.0*r*cos(t);y=2.4*r*sin(t)
   z=.18+v*.6+(.35+v*.75)*(sin(t*5+v*9)*.5+.5)+random.random()*.09
   vs.append((x,y,z))
 for j in range(M-1):
  for i in range(N):
   a=j*N+i;b=j*N+(i+1)%N;c=(j+1)*N+(i+1)%N;d=(j+1)*N+i
   A.mesh('Triangular folded fabric',vs,[(a,b,c),(a,c,d)],'fold_blue_light' if (i+j)%3==0 else 'fold_blue')
 for k in range(4):
  x=-2.0+k*1.3;pts=[(x+sin(t*pi)*.5,-1.1+t*2.2,.45+sin(t*pi)*(1.15+k*.2)) for t in [i/10 for i in range(11)]]
  A.curve('Raised blue fold',pts,.22,'fold_blue_light')
 A.curve('White folded edge',[(4.05*cos(i*2*pi/N),2.5*sin(i*2*pi/N),.29+.18*sin(i*10*pi/N)) for i in range(N)],.18,'white',True)
 A.setup_preview(43,31,1200,900);A.save_asset('blue_sculpture')

def pets_com():
 from build_landmarks import historic_apple
 historic_apple()
 for ob in list(A.COL.objects):
  if ob.name.lower().startswith('apple'):A.bpy.data.objects.remove(ob,do_unlink=True)
 A.COL.name='ASSET • Pets.com original masonry office';A.COL['asset_id']='pets_com';A.COL['variant']='Original wide image: Pets.com roof billboard without the later large rainbow Apple facade sculpture.'
 for c in list(A.bpy.data.collections):
  if c.name.startswith('STUDIO'):
   for o in list(c.objects):A.bpy.data.objects.remove(o,do_unlink=True)
   A.bpy.data.collections.remove(c)
 A.setup_preview(47.134,26.377,1400,1250)
 A.save_asset('pets_com')

if __name__=='__main__':blue_sculpture();pets_com()
