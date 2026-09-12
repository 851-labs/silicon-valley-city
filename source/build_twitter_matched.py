"""Twitter/Blogger: source-measured pavilions, slot walls, roof comb and signage."""
import os,sys,json,math,random
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art,facade,AZ,EL
from build_ebay_matched import inset
from mathutils import Vector
from math import sin,cos,pi,atan2
P=Path(__file__).parent

def build():
 D=json.load(open(P/'twitter_measurements.json'));A.reset('twitter','Twitter and Blogger • measured pavilions and garden',['Original wide frame','YU13','YU11']);R=Reference(D['anchor'],D['crop'])
 for n,c,rough in [('twitter_stone',(.50,.44,.35),.87),('twitter_roof',(.43,.42,.40),.82),('twitter_slot',(.026,.025,.023),.53),('twitter_blue',(.013,.18,.26),.50),('twitter_beam',(.40,.61,.65),.45),('twitter_sign',(.87,.87,.81),.71),('twitter_pole',(.11,.16,.21),.54),('twitter_glass',(.10,.15,.14),.33),('twitter_paving',(.44,.43,.39),.9)]:A.material(n,c,rough)
 A.material('twitter_guard',(.60,.81,.82),.09,trans=.96)
 A.MAT['twitter_beam'].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.65
 A.MAT['twitter_beam'].node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.10
 A.MAT['twitter_guard'].node_tree.nodes['Principled BSDF'].inputs['IOR'].default_value=1.32
 A.material('twitter_garden_grass',(.20,.25,.008),.96)
 A.MAT['twitter_garden_grass'].node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.035
 A.material('twitter_garden_water',(.055,.13,.12),.23)
 for m in D['pavilions']:
  H=m['height'];roof=R.plan(m['roof'],H);wall=inset(roof,.12)
  A.part(m['name']+' • stone shell');A.polygon('Measured masonry envelope',wall,0,H,'twitter_stone')
  edges=list(zip(wall,wall[1:]+wall[:1]));lengths=[(Vector(b)-Vector(a)).length for a,b in edges];short=min(lengths)
  for a,b in edges:
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));angle=atan2(v.y,v.x);center=(a+b)/2+n*.025
   if (cos(AZ)*v.x+sin(AZ)*v.y)*(sin(AZ)*v.x-cos(AZ)*v.y)>0:
    A.part(m['name']+' • louvred glazed end')
    A.box('Recessed full-height end glazing',(center.x,center.y,H*.52),(L-.85,.07,H-.6),'twitter_glass',angle)
    for j in range(13):A.box('Projecting horizontal stone sunshade',(center.x+n.x*.14,center.y+n.y*.14,.42+j*(H-.62)/13),(L-.80,.42,.115),'twitter_stone',angle)
   else:
    A.part(m['name']+' • irregular vertical window slots');N=max(5,round(L/1.40))
    for j in range(N):
     q=a+t*(j+.5)*L/N+n*.045
     for k in range(3):
      if (j+2*k)%7 in (2,6):continue
      hh=1.55 if (j+k)%3 else 1.09;zz=.34+k*H/3+hh/2
      A.box('Narrow dark recessed slot',(q.x,q.y,zz),(.23 if j%3 else .39,.07,hh),'twitter_slot',angle)
      A.box('Thin stone reveal edge',(q.x+t.x*.17+n.x*.025,q.y+t.y*.17+n.y*.025,zz),(.04,.13,hh+.04),'twitter_stone',angle)
  A.part(m['name']+' • roof construction');A.polygon('Recessed flat grey roof',inset(roof,.08),H,.03,'twitter_roof')
  # Roof long axes are taken from the measured image polygon, independently of CCW reordering.
  q=[R.p(p,H+.10) for p in m['roof']]
  if m['louvres']:
   for j in range(28):
    f=(j+.5)/28;a=q[0].lerp(q[1],f);b=q[3].lerp(q[2],f);vv=b-a;c=(a+b)/2
    A.box('Closely spaced roof louvre',tuple(c),(vv.length,.065,.09),'twitter_stone',atan2(vv.y,vv.x))
   for a,b in [(q[0],q[1]),(q[3],q[2])]:
    vv=b-a;c=(a+b)/2;A.box('Broad projecting blue roof beam',tuple(c),(vv.length+.35,.72,.15),'twitter_beam',atan2(vv.y,vv.x))
  else:
   for a,b in zip(q,q[1:]+q[:1]):
    vv=b-a;c=(a+b)/2;A.box('Low raised roof edge',tuple(c),(vv.length,.10,.16),'twitter_stone',atan2(vv.y,vv.x))
 for name,pixels,h,base in [('Front projecting window bay',[[740,330],[756,324],[767,329],[751,336]],6.25,3.8),('Rear projecting window bay',[[699,302],[710,297],[721,301],[710,306]],4.8,2.6)]:
  A.part(name);p=R.plan(pixels,h);A.polygon('Projecting box enclosure',p,base,h-base,'twitter_stone');a,b=Vector(p[0]),Vector(p[1]);v=b-a;n=Vector((v.y,-v.x)).normalized();c=(a+b)/2+n*.03;A.box('Deep shaded box glazing',(c.x,c.y,(h+base)/2),(v.length-.24,.04,h-base-.30),'twitter_slot',atan2(v.y,v.x))
 A.part('Measured low glazed courtyard connectors')
 for m in D['connectors']:
  H=m['height'];p=R.plan(m['roof'],H);A.polygon('Stone connector envelope',p,0,H,'twitter_stone')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));ang=atan2(v.y,v.x);N=max(2,round(L/1.5))
   for j in range(N):
    q=a+t*(j+.5)*L/N+n*.035
    for k in range(2):A.box('Connector narrow window',(q.x,q.y,.72+k*H/2),(.29,.04,.50),'twitter_glass',ang)
  A.polygon('Blue glazed roof platform',p,H,.12,'twitter_beam')
  for a,b in zip(p,p[1:]+p[:1]):
   a,b=Vector(a),Vector(b);v=b-a;c=(a+b)/2
   A.box('Transparent glass roof guard',(c.x,c.y,H+.61),(v.length,.045,.98),'twitter_guard',atan2(v.y,v.x))
   N=max(2,round(v.length/2.3))
   for i in range(N+1):
    q=a.lerp(b,i/N);A.box('Slender pale roof-guard post',(q.x,q.y,H+.61),(.034,.055,1.02),'twitter_sign',atan2(v.y,v.x))
   A.box('Fine roof-guard top rail',(c.x,c.y,H+1.12),(v.length,.035,.035),'twitter_sign',atan2(v.y,v.x))
 # The studio view and wide frame both show a circular water garden and bridge.
 A.part('Measured Blogger courtyard water garden')
 R.prism('Irregular courtyard lawn',[[734,262],[774,241],[803,242],[833,258],[844,277],[819,289],[789,292],[754,280]],.10,.01,'twitter_garden_grass')
 q=R.p((797,267),.15)
 A.cylinder('Circular dark water channel',tuple(q),3.13,.05,'twitter_garden_water',96)
 A.cylinder('Raised circular lawn island',(q.x,q.y,.19),2.50,.05,'twitter_garden_grass',96)
 for k,r in enumerate([1.12,.91,.70]):A.cylinder('Three concentric pale garden steps',(q.x,q.y,.27+k*.12),r,.12,'twitter_stone',64)
 R.prism('Southern continuation of shallow water channel',[[785,281],[805,273],[820,280],[799,291]],.13,.09,'twitter_garden_water')
 R.prism('Measured pale bridge across the water',[[788,286],[808,278.5],[814,281.5],[792,291]],.64,.45,'twitter_sign')
 A.part('Individually positioned garden trees')
 for x,y,r,h in [[769,254,1.65,3.2],[779,251,1.7,3.6],[785,244,1.7,3.8],[824,265,2.05,3.6],[818,258,1.05,2.8],[813,251,1.3,3.0],[786,260,1.15,2.9],[774,263,1.2,2.8],[808,270,.85,2.3],[787,276,1.0,2.4]]:
  q=R.p((x,y),h*.77);A.tree(q.x,q.y,.11,r,h)
 for x,y,h in [[793,243,4.0],[802,246,4.5]]:
  q=R.p((x,y),h*.68);A.cylinder('Courtyard cypress trunk',(q.x,q.y,h*.3),.06,h*.6,'wood',8);A.cylinder('Tall pointed courtyard cypress',(q.x,q.y,h*.68),1.0,h*.95,'leaf_dark',7,r2=.01)
 m=D['blogger'];H=m['height'];p=R.plan(m['roof'],H);wall=inset(p,.08)
 A.part('Blogger • single-storey masonry and clerestory');A.polygon('Measured low Blogger body',wall,0,H,'twitter_stone');A.polygon('Pale blue Blogger roof',p,H,.08,'twitter_beam')
 for a,b in zip(wall,wall[1:]+wall[:1]):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));ang=atan2(v.y,v.x)
  for i in range(max(1,round(L/.82))):
   q=a+t*(i+.5)*.82+n*.028;A.box('Small horizontal clerestory slot',(q.x,q.y,H-.36),(.58,.055,.24),'twitter_slot',ang)
 A.part('Blogger • circular finned roof lantern');q=R.p(m['lantern_center'],H+1.0);rad=m['lantern_radius']
 A.cylinder('Truncated roof lantern',(q.x,q.y,H+.55),rad,1.0,'twitter_stone',96,r2=rad*.84);A.cylinder('Pale recessed lantern top',(q.x,q.y,H+1.04),rad*.80,.06,'twitter_sign',96)
 for i in range(36):
  a=2*pi*i/36;A.rod('Lantern sloping radial rib',(q.x+(rad+.03)*cos(a),q.y+(rad+.03)*sin(a),H+.09),(q.x+(rad*.85+.03)*cos(a),q.y+(rad*.85+.03)*sin(a),H+1.19),.052,'twitter_sign',4)
 A.part('Blogger • rounded orange and white roof artwork')
 origin=R.p((677,224),H+.12);u=R.p((707,237),H+.12)-origin;v=R.p((704,211),H+.12)-origin
 data=json.load(open(P/'blogger_logo_mesh.json'))
 for mat,z,dep in [('orange',0,.28),('white',.29,.035)]:vector_art('Blogger vector shape',[g for g in data if g['material']==mat],origin+Vector((0,0,z)),u,v,dep,(0,0,1))
 A.part('Blogger • original Google facade lettering');data=json.load(open(P/'google_logo_mesh.json'))
 for g in data:g['material']=g['color']
 edge_a,edge_b=(662,228),(726,260)
 origin=R.facade_point((682,254),edge_a,edge_b,H);u=(R.p(edge_b,H)-R.p(edge_a,H))*(40/(edge_b[0]-edge_a[0]));v=Vector((0,0,u.length));n=u.cross(v).normalized()
 view=Vector((math.sin(AZ),-math.cos(AZ),0))
 if n.dot(view)<0:n=-n
 origin+=n*.025
 vector_art('Google historical extruded glyph',data,origin,u,v,.43,n)
 A.part('Twitter • circular sign and full-height post');m=D['sign'];q=R.p(m['center'],m['center_height']);r=m['radius'];heading=m['heading'];normal=Vector((sin(heading),-cos(heading),0))
 ob=A.polygon('Thick circular white sign',[(r*cos(i*2*pi/128),r*sin(i*2*pi/128)) for i in range(128)],-m['depth']/2,m['depth'],'twitter_sign',False);ob.rotation_euler=(pi/2,0,heading);ob.location=q
 bird=A.logo('twitter',tuple(q+normal*(m['depth']/2+.03)),6.2,.13,'twitter_blue',rot=(pi/2,0,heading))
 pole=R.p((768,374),0)
 A.box('Tall rectangular sign mast',(pole.x,pole.y,(m['center_height']-1)/2),(.41,.65,m['center_height']-1),'twitter_pole',heading)
 A.box('Wider foot of sign mast',(pole.x,pole.y,.60),(.55,.79,1.2),'twitter_pole',heading)
 A.COL['measurement_file']='source/twitter_measurements.json';A.COL['inferred_details']='Slot continuation on concealed elevations; exact planting and roof parapets remain under comparison.'
 A.setup_preview(47.134,26.377,1600,1200);R.camera(4);return A
if __name__=='__main__':build();A.save_asset('twitter','--no-render' not in sys.argv)
