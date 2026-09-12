"""Western high-rise constrained by visible ground corners and floor-band pitch."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,AZ
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'framing_tower_measurements.json'));A.reset('framing_tower','Western framed high-rise • measured ground lines and narrow projecting bay',['Original wide frame']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('framed_stone',(.39,.40,.365),.84),('framed_glass',(.17,.26,.27),.49),('framed_dark',(.07,.095,.095),.58)]:A.material(n,c,r)
 for block in D['volumes']:
  H=block['height'];p=R.plan(block['ground'],0);A.part(block['name']);A.polygon('Ground-constrained tall office volume',p,0,H,'framed_glass');step=block['step']
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));angle=math.atan2(t.y,t.x);q=(a+b)/2+n*.05
   for k in range(math.ceil(H/step)+1):A.box('Fine continuous high-rise floor band',(q.x,q.y,k*step+.20),(L,.13,.46 if block['style']=='broad' else .30),'framed_stone',angle)
   N=max(2,round(L/1.72))
   for j in range(N+1):
    qq=a+t*(j*L/N)+n*.12
    if block['style']=='broad':
     A.box('Thin lower ribbon-window joint',(qq.x,qq.y,15.5),(.018,.04,31.0),'framed_stone',angle);A.box('Deep upper extension glazing pier',(qq.x,qq.y,(H+31)/2),(.18,.23,H-31),'framed_stone',angle)
    else:A.box('Vertical high-rise glazing division',(qq.x,qq.y,H/2),(.10,.19,H),'framed_stone',angle)
   if block['style']=='pier':
    for f in [0,.5,1]:
     qq=a.lerp(b,f)+n*.25;A.box('Projected full-height narrow-bay pier',(qq.x,qq.y,H/2),(.55,.57,H),'framed_stone',angle)
   else:
    # Main broad faces have long horizontal ribbons; the upper extension is framed more densely.
    for f in [.03,.97]:
     qq=a.lerp(b,f)+n*.18;A.box('Main slab outer structural pier',(qq.x,qq.y,H/2),(.48,.40,H),'framed_stone',angle)
  A.polygon('Inferred off-frame flat tower roof',p,H,.25,'framed_stone')
 A.COL['measurement_file']='source/framing_tower_measurements.json';A.COL['inferred_details']='Roof and upper termination are outside the master frame. Only the visible slab, projecting bay, ground edges and facade rhythm can be checked against this image.'
 A.setup_preview(47.134,26.377,1100,1400);R.camera(7);return A
if __name__=='__main__':build();A.save_asset('framing_tower')
