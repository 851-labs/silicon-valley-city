"""Western pale office with independent rear service bar and deep perforated piers."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'white_corner_office_measurements.json'));A.reset('white_corner_office','Western pale office • measured roof, perforated piers and service bar',['Original wide frame']);R=Reference(D['anchor'],D['crop']);H=D['height']
 for n,c,r in [('corner_stone',(.65,.65,.57),.86),('corner_roof',(.83,.77,.66),.90),('corner_glass',(.12,.29,.29),.48),('corner_dark',(.065,.078,.069),.65),('corner_plant',(.25,.41,.38),.59)]:A.material(n,c,r)
 p=R.plan(D['roof'],H);wall=inset(p,.16);A.part('Eleven-storey main office body');A.polygon('Measured main curtain-wall envelope',wall,0,H-.10,'corner_glass');step=H/D['floors']
 for a,b in zip(wall,wall[1:]+wall[:1]):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((v.y,-v.x)).normalized();angle=math.atan2(v.y,v.x);q=(a+b)/2+n*.06
  for k in range(D['floors']):
   z=k*step;A.box('Pale continuous floor spandrel',(q.x,q.y,z+.38),(L+.03,.12,.76),'corner_stone',angle)
  # Deep piers are independent architectural masses with their own punched windows.
  N=2 if L>15 else 1
  for j in range(N+1):
   f=(.55 if j==1 and N==2 else .035+.93*j/N);qq=a.lerp(b,f)+n*.28;w=2.9 if j not in (0,N) else 2.6
   A.box('Projecting full-height pale pier',(qq.x,qq.y,H/2),(w,1.1,H+.16),'corner_stone',angle)
   for k in range(D['floors']):
    for dx in [-w*.24,w*.24]:
     g=qq+t*dx+n*.565;A.box('Small dark pier window',(g.x,g.y,k*step+1.08),(.32,.035,.65),'corner_dark',angle)
   # Narrow return-face perforations establish the pier depth at the oblique view.
   for side in [-1,1]:
    rr=qq+t*(side*(w/2+.018))
    for k in range(D['floors']):A.box('Pier return window',(rr.x,rr.y,k*step+1.08),(.025,.32,.65),'corner_dark',angle)
 A.part('Pale measured rooftop');A.polygon('Main pale rooftop membrane',p,H-.10,.20,'corner_roof')
 A.part('Elevated narrow rear service bar');R.prism('Tall rear service enclosure',D['rear_roof'],D['rear_height'],0,'corner_stone')
 for quad in [[[0,167],[12,160],[24,165],[13,173]],[[40,150],[51,144],[65,150],[52,157]]]:
  R.prism('Blue-green rooftop plant enclosure',quad,21.2,20.5,'corner_plant');R.prism('Pale glazed plant top',quad,21.25,21.20,'corner_glass')
 A.part('Measured main roof equipment');quad=[[68,185],[82,179],[90,183],[76,190]];R.prism('Low rectangular roof plant curb',quad,H+.28,H,'corner_stone');pp=R.plan(quad,H+.28)
 for aa,bb in zip(pp,pp[1:]+pp[:1]):A.rod('Open plant frame',(*aa,H+.8),(*bb,H+.8),.065,'corner_stone',6)
 for px in [(70,184),(83,181),(77,187)]:
  q=R.p(px,H+.25);A.rod('Roof plant vertical support',(q.x,q.y,H+.25),(q.x,q.y,H+.8),.065,'corner_stone',6)
 for px,h,r in [((32,211),3.4,.13),((36,214),.8,.35),((42,216),.65,.4)]:
  q=R.p(px,H+.1);A.cylinder('Observed small roof exhaust',(q.x,q.y,H+.1+h/2),r,h,'corner_stone',16)
 A.COL['measurement_file']='source/white_corner_office_measurements.json';A.COL['inferred_details']='Off-frame western roof limits and hidden rear windows are extrapolated. The visible eleven facade courses and major pier positions are measured.'
 A.setup_preview(47.134,26.377,1300,1400);R.camera(6);return A
if __name__=='__main__':build();A.save_asset('white_corner_office')
