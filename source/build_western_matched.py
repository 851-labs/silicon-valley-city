"""Measured western commercial blocks; architecture and signs remain separate meshes."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art
from build_ebay_matched import inset
from mathutils import Vector
from math import pi,sin,cos,atan2
P=Path(__file__).parent

def pets_com():
 D=json.load(open(P/'pets_com_measurements.json'));A.reset('pets_com','Pets.com • measured teal masonry and original sign',['Original wide frame','YU09']);R=Reference(D['anchor'],D['crop']);H=D['height'];p=R.plan(D['roof'],H)
 A.surface_detail(A.material('pets_masonry',(.014,.255,.208),.88),.018,30)
 A.material('pets_window',(.04,.05,.049),.38);A.material('pets_frame',(.085,.14,.116),.85)
 A.material('pets_ink',(.007,.009,.004),.60);A.material('pets_green',(.11,.37,.035),.74);A.material('pets_roof',(.83,.79,.695),.87)
 A.part('Measured teal masonry envelope');A.polygon('Three-storey masonry body',p,0,H,'pets_masonry')
 for edge,(a,b) in enumerate(zip(p,p[1:]+p[:1])):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));ang=atan2(v.y,v.x);N=max(4,round(L/3.3))
  for j in range(N):
   q=a+t*(j+.50)*L/N+n*.015
   for k,z in enumerate([5.8,8.0]):
    A.box('Upper rectangular window reveal',(q.x,q.y,z),(1.1,.04,1.18),'pets_frame',ang)
    w=q+n*.026;A.box('Inset dark glazing',(w.x,w.y,z),(.90,.025,1.03),'pets_window',ang)
    w=q+n*.07;A.box('Small projecting sill',(w.x,w.y,z-.64),(1.18,.18,.10),'pets_masonry',ang)
    if (j+k)%3==0:
     o=A.box('Open casement pane',(w.x,w.y,z),(.9,.055,1.02),'pets_window',rot=ang,batch=False);o.rotation_euler.x=.23
   # Tall ground-floor arches; plane faces outward at this particular facet.
   w=.64;shoulder=2.90
   curve=[(-w,.04),(w,.04),(w,shoulder)]+[(w*cos(pi*i/32),shoulder+w*sin(pi*i/32)) for i in range(33)]
   vs=[tuple((q+t*x).to_3d()+Vector((0,0,z))) for x,z in curve];A.mesh('Tall arched ground-floor reveal',vs,[tuple(range(len(vs)))],'pets_window')
 A.part('Pale roof and stepped teal parapets');A.polygon('Recessed cream roof',inset(p,.63),H-.10,.12,'pets_roof')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;t=v.normalized();L=v.length;ang=atan2(v.y,v.x);q=(a+b)/2
  A.box('Continuous teal parapet',(q.x,q.y,H+.18),(L,.29,.36),'pets_masonry',ang)
  for f,w,h in [(.17,L*.18,.31),(.50,L*.32,.69),(.83,L*.18,.31)]:
   q=a+t*f*L;A.box('Stepped parapet crest',(q.x,q.y,H+.34+h/2),(w,.29,h),'pets_masonry',ang)
 A.part('Original Pets.com billboard')
 d=D['sign'];base=R.p(d['left'],d['bottom_height']);end=R.p(d['right'],d['bottom_height']);u=end-base;W=u.length;t=u.normalized();n=Vector((t.y,-t.x,0));ang=atan2(t.y,t.x);h=d['height'];q=(base+end)/2+Vector((0,0,h/2))
 A.box('Green rectangular sign edge',tuple(q),(W,.38,h),'pets_green',ang)
 q+=n*.215;A.box('Pale inset sign face',tuple(q),(W-.25,.035,h-.30),'white',ang)
 origin=base+n*.25+t*.35+Vector((0,0,1.15));u=t*(W-.70);v=Vector((0,0,W-.70))
 vector_art('Historical paw and letter contours',json.load(open(P/'pets_logo_mesh.json')),origin,u,v,.033,n)
 for f in [.20,.77]:
  q=base+t*f*W-n*.08;A.cylinder('Billboard wide foot',(q.x,q.y,H+.57),.35,1.14,'pets_window',20)
  A.rod('Billboard support post',(q.x,q.y,H+1.1),(q.x,q.y,d['bottom_height']+.35),.15,'pets_window',16)
 A.COL['measurement_file']='source/pets_com_measurements.json';A.COL['inferred_details']='Small windows on hidden elevations follow the visible two upper courses; no later Apple sculpture in this original-wide variant.'
 A.setup_preview(47.134,26.377,1300,1400);R.camera(5);return A

def paypal():
 D=json.load(open(P/'paypal_measurements.json'));A.reset('paypal','PayPal • measured chamfered block and historical roof letters',['Original wide frame','YU09']);R=Reference(D['anchor'],D['crop']);H=D['height'];p=R.plan(D['roof'],H)
 A.material('paypal_concrete',(.52,.485,.425),.87);A.material('paypal_roof',(.72,.655,.55),.88)
 A.material('paypal_band',(.46,.435,.39),.88);A.material('paypal_yellow',(.62,.43,.003),.76)
 A.material('paypal_dark_blue',(.026,.047,.07),.55);A.material('paypal_light_blue',(.062,.125,.18),.48)
 A.part('Chamfered solid office');A.polygon('Measured irregular corner cuts',inset(p,.13),0,H-.20,'paypal_concrete');A.polygon('Thin continuous roof edge',p,H-.20,.20,'paypal_concrete');A.polygon('Pale flat roof',inset(p,.055),H,.03,'paypal_roof')
 for edge,(a,b) in enumerate(zip(p,p[1:]+p[:1])):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));q=(a+b)/2+n*.016;ang=atan2(v.y,v.x)
  for z in [.8,2.05,3.35,4.70,6.55,8.4]:A.box('Fine horizontal masonry course',(q.x,q.y,z),(L,.035,.055),'paypal_band',ang)
  # Yellow recessed windows occupy only the long return elevations.
  if L>13 and abs(t.x)<.65:
   for z in [5.95,8.55]:
    A.box('Recessed yellow horizontal window',(q.x,q.y,z),(L*.66,.045,.83),'paypal_yellow',ang)
  for i in range(1,max(2,round(L/4))):
   q=a+t*i*L/max(2,round(L/4))+n*.016;A.box('Vertical block joint',(q.x,q.y,5),(.012,.025,9.7),'paypal_band',ang)
 A.part('Projecting lower entrance and masonry hood')
 lower=R.plan([[106,343],[111,340],[158,339],[165,342],[159,347],[110,348]],5.6)
 A.polygon('Projecting chamfered entrance body',lower,.2,5.4,'paypal_concrete');A.polygon('Broad pale entrance hood',lower,5.6,.24,'paypal_roof')
 a,b=Vector(lower[0]),Vector(lower[1]);front=max(zip(lower,lower[1:]+lower[:1]),key=lambda ab:(Vector(ab[1])-Vector(ab[0])).length)
 a,b=Vector(front[0]),Vector(front[1]);v=b-a;t=v.normalized();n=Vector((t.y,-t.x));q=(a+b)/2+n*.03
 A.material('paypal_entry_glass',(.15,.119,.081),.42);A.box('Broad recessed brown entrance glazing',(q.x,q.y,2.85),(v.length*.91,.07,2.85),'paypal_entry_glass',atan2(v.y,v.x))
 for f in [-.4,-.2,0,.2,.4]:
  q=(a+b)/2+t*f*v.length+n*.08;A.box('Entrance vertical frame',(q.x,q.y,2.85),(.05,.10,2.85),'paypal_band',atan2(v.y,v.x))
 A.part('Measured rooftop ventilation')
 for m in D['vents']:
  q=R.plan(m['roof'],m['height']);A.polygon('Raised box vent',q,H,m['height']-H,'paypal_band')
  a,b=Vector(q[0]),Vector(q[1]);v=b-a;angle=atan2(v.y,v.x);mid=(a+b)/2
  for z in [H+.25,H+.5,H+.75]:A.box('Vent louvre',(mid.x,mid.y,z),(v.length,.06,.08),'paypal_dark_blue',angle)
 m=D['service'];q=R.plan(m['roof'],m['height']);A.polygon('Large back service enclosure',q,H,m['height']-H,'paypal_band');A.polygon('Service box pale top',q,m['height'],.12,'paypal_roof')
 # Sloped access ramp against the rooftop enclosure, with short pipe outlets.
 a,b=Vector(q[0]),Vector(q[1]);v=b-a;t=v.normalized();n=Vector((t.y,-t.x));start=(a+b)/2+n*2.6
 A.mesh('Sloping service enclosure cover',[(a.x,a.y,m['height']),(b.x,b.y,m['height']),(start.x+t.x*v.length/2,start.y+t.y*v.length/2,H),(start.x-t.x*v.length/2,start.y-t.y*v.length/2,H)],[(0,1,2,3)],'paypal_band')
 c=sum((Vector(q) for q in q),Vector((0,0)))/len(q)
 for dx in [-.7,.7]:A.cylinder('Service vent pipe',(c.x+dx,c.y,m['height']+.23),.13,.46,'paypal_dark_blue',12)
 d=D['yellow_dome'];q=R.p(d['center'],H+.30);rad=d['radius']
 A.cylinder('Dome base ring',(q.x,q.y,H+.12),rad,.24,'paypal_yellow',64)
 vs=[(q.x+rad*sin(pi*j/48)*cos(2*pi*i/64),q.y+rad*sin(pi*j/48)*sin(2*pi*i/64),H+.22+rad*.58*cos(pi*j/48)) for j in range(25) for i in range(64)]
 fs=[(j*64+i,j*64+(i+1)%64,(j+1)*64+(i+1)%64,(j+1)*64+i) for j in range(24) for i in range(64)];A.mesh('Flattened yellow roof dome',vs,fs,'paypal_yellow')
 A.part('Roof-edge dark baffles')
 for aa,bb,z,h in [((64,304),(81,311),11.4,2.9),((166,311),(181,305),12.9,2.9),((202,297),(218,292),12.6,2.6)]:
  a=R.p(aa,z);b=R.p(bb,z);v=b-a;q=(a+b)/2;A.box('Upright dark roof screen',tuple(q-Vector((0,0,h/2))),(v.length,.16,h),'paypal_band',atan2(v.y,v.x))
 A.part('Raised historical PayPal roof lettering')
 z=H+D['letter_depth'];origin=R.p((110,315),z);u=R.p((168,290),z)-origin;v=(R.p((101,306),z)-origin)/.28
 vector_art('Extruded PayPal historical glyph',json.load(open(P/'paypal_logo_mesh.json')),origin,u,v,-D['letter_depth'],(0,0,1))
 A.COL['measurement_file']='source/paypal_measurements.json';A.COL['inferred_details']='Rear edges behind the high-rise and the unseen service-box side are completed from visible roof evidence.'
 A.setup_preview(47.134,26.377,1500,1100);R.camera(5);return A
BUILDERS={'pets_com':pets_com,'paypal':paypal}
if __name__=='__main__':
 ids=sys.argv[sys.argv.index('--assets')+1:] if '--assets' in sys.argv else list(BUILDERS)
 for id in ids:BUILDERS[id]();A.save_asset(id)
