"""Individually measured eastern and western control towers, from one reusable builder."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def build(id):
 D=json.load(open(P/(id+'_measurements.json')));A.reset(id,('Western' if id.endswith('west') else 'Northern' if id.endswith('north') else 'Eastern')+' control tower • measured armored base and four floors',['Original wide frame','YU11']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('control_concrete',(.48,.49,.455),.87),('control_roof',(.85,.79,.68),.9),('control_glass',(.08,.25,.30),.5),('control_top_glass',tuple(D['top_glass']),.43),('control_dark',(.18,.20,.19),.82)]:A.material(n,c,r)
 p=R.plan(D['plinth_ground'],0);top=R.plan(D['plinth_top'],D['plinth_height']);bh=D['plinth_height'];A.part('Tapered armored service plinth');vs=[(x,y,z) for poly,z in [(p,0),(top,bh)] for x,y in poly];A.mesh('Solid tapered armored base',vs,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'control_concrete');A.polygon('Broad armored top deck',top,bh,.15,'control_concrete')
 for j in range(4):
  a,b=Vector(p[j]),Vector(p[(j+1)%4]);c,d=Vector(top[j]),Vector(top[(j+1)%4]);v=b-a;n=Vector((v.y,-v.x)).normalized()
  for t in [.15,.50,.85]:
   lo=a.lerp(b,t)+n*.03;hi=c.lerp(d,t)+n*.03;A.rod('Armored panel seam',(*tuple(lo),.05),(*tuple(hi),bh),.025,'control_dark',4)
   for f in [.24,.70]:
    q=lo.lerp(hi,f);A.sphere('Small dark armored panel fastener',(q.x,q.y,bh*f),(.045,.045,.045),'control_dark',8,5)
 H=D['height'];base=D['shaft_bottom'];p=R.plan(D['roof'],H);core=inset(p,1.15);upper=inset(p,.27);top_floor=H-3.2;step=(top_floor-base)/4
 A.part('Four lower office floors and overhanging control room');A.polygon('Pale tower-to-plinth pedestal',core,bh,base-bh,'control_concrete');A.polygon('Lower narrower office shaft',core,base,top_floor-base,'control_glass');A.polygon('Wide upper control room',upper,top_floor,H-.25-top_floor,'control_top_glass')
 for wall,z0,z1,count,band in [(core,base,top_floor,4,1.52),(upper,top_floor,H-.25,1,.30)]:
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;n=Vector((v.y,-v.x)).normalized();angle=math.atan2(v.y,v.x);q=(a+b)/2+n*.04
   for k in range(count):A.box('Solid band below office ribbon',(q.x,q.y,z0+k*(z1-z0)/count+band/2),(L+.08,.17,band),'control_concrete',angle)
   for f in [0,.50,1]:
    q=a.lerp(b,f)+n*.13;A.box('Projected vertical control-tower pier',(q.x,q.y,(z0+z1)/2),(.70 if f!=.5 else .16,.29,z1-z0),'control_concrete',angle)
 A.part('Pale overhanging control-tower roof');A.polygon('Wide shallow white roof slab',p,H-.25,.30,'control_roof')
 q=R.p(D['hatch'],bh+.20);A.part('Armored deck mechanical hatch');A.cylinder('Raised circular hatch rim',tuple(q),1.0,.16,'control_concrete',64);A.cylinder('Inset hatch plate',(q.x,q.y,bh+.29),.76,.04,'control_dark',64);A.cylinder('Hatch inner cap',(q.x,q.y,bh+.325),.57,.035,'control_concrete',64)
 A.COL['measurement_file']='source/'+id+'_measurements.json';A.COL['inferred_details']='Rear armored doors are occluded. East and west towers retain independent reference geometry and upper-glass material.'
 A.setup_preview(47.134,26.377,1100,1450);R.camera(7);return A
if __name__=='__main__':
 for id in (sys.argv[sys.argv.index('--assets')+1:] if '--assets' in sys.argv else ['security_tower','security_tower_west','security_tower_north']):build(id);A.save_asset(id)
