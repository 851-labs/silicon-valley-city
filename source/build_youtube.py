"""YouTube: measured cantilever, glass lobby and deep historical vector sign."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
from mathutils import Vector
from math import sin,cos,pi,atan2

def build():
 D=json.load(open(Path(__file__).with_name('youtube_measurements.json')))
 A.reset('youtube','YouTube • measured cantilever and original vector lettering',['Original wide frame','YU25','YU16'])
 R=Reference(D['anchor'],D['crop'])
 A.material('youtube_slab',(.37,.37,.34),.83)
 A.material('youtube_roof',(.95,.86,.76),.85)
 A.material('youtube_glass',(.037,.043,.041),.30,.035)
 A.material('youtube_frame',(.33,.34,.32),.66,.08)
 A.material('youtube_plaza',(.25,.385,.44),.86)
 A.material('youtube_paver',(.19,.205,.195),.89)
 A.part('Plaza • measured projecting blue slab')
 p=R.plan(D['plaza'],D['plaza_height']);A.polygon('Projecting structural plaza',p,0,D['plaza_height'],'youtube_slab');A.polygon('Blue plaza surface',p,D['plaza_height'],.035,'youtube_plaza')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;q=(a+b)/2
  A.box('Pale projecting slab edge',(q.x,q.y,D['plaza_height']-.08),(v.length,.12,.17),'frame',atan2(v.y,v.x))
 for px,py,color in [(621,421,'yellow'),(658,427,'yellow'),(631,435,'dark')]:
  q=R.p((px,py),2.7);A.person(q.x,q.y,1.25,color)
 for px,py in [(579,413),(635,441),(696,414)]:
  q=R.p((px,py),1.2);A.rod('Slender plaza lamp',(q.x,q.y,1.2),(q.x,q.y,5.8),.024,'metal',8)
 A.part('Recessed ground-floor lobby')
 p=R.plan(D['lobby_base'],D['lobby_base_height']);z=D['lobby_base_height'];h=D['cantilever_bottom']-z
 A.polygon('Inset dark paving around lobby',p,z,.16,'youtube_paver');A.polygon('Recessed lobby glazing',p,z+.16,h-.16,'youtube_glass')
 for a,b in zip(p,p[1:]+p[:1]):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));ang=atan2(v.y,v.x);count=max(2,round(L/.85))
  for i in range(count+1):
   q=a+t*i*L/count+n*.035;A.box('Lobby curtain-wall vertical',(q.x,q.y,z+h/2),(.043,.07,h),'youtube_frame',ang)
  q=(a+b)/2+n*.04
  for zz in [z+.3,z+h*.74,z+h]:A.box('Lobby horizontal rail',(q.x,q.y,zz),(L,.08,.075),'youtube_frame',ang)
 # Independently measured upper plan; the lobby recedes on all four sides.
 p=R.plan(D['roof'],D['roof_height']);top=D['roof_height'];base=D['upper_glazing_bottom'];cap=D['roof_thickness']
 A.part('Heavy lower cantilever')
 A.polygon('Thick lower structural slab',p,D['cantilever_bottom'],base-D['cantilever_bottom'],'youtube_slab')
 A.part('Upper glass storeys and dense metal screen')
 A.polygon('Dark upper glazing',p,base,top-cap-base,'youtube_glass')
 for edge,(a,b) in enumerate(zip(p,p[1:]+p[:1])):
  a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));ang=atan2(v.y,v.x)
  dense=abs(n.y)>.5
  pitch=.19 if dense else .66;count=max(2,round(L/pitch))
  for i in range(count+1):
   q=a+t*i*L/count+n*.03
   A.box('Dense screen fin' if dense else 'Upper glazing mullion',(q.x,q.y,(base+top-cap)/2),(.021 if dense else .034,.14 if dense else .085,top-cap-base),'youtube_frame',ang)
  q=(a+b)/2+n*.055
  for zz in [base+.10,(base+top-cap)/2,top-cap-.05]:A.box('Upper horizontal transom',(q.x,q.y,zz),(L,.09,.055),'youtube_frame',ang)
 A.part('Roof • heavy exposed slab and pale top')
 A.polygon('Heavy roof cornice',p,top-cap,cap,'youtube_slab');A.polygon('Pale roof membrane',p,top,.035,'youtube_roof')
 # Vector sign mesh: glyph outlines, original rounded capsule and separate deep extrusion.
 A.part('Historical YouTube vector sign')
 q=R.p(D['sign_baseline'],D['sign_base_height']);width=D['sign_width']
 root=A.bpy.data.objects.new('YouTube vector sign assembly',None);A.COL.objects.link(root);root.location=q;root.rotation_euler=(pi/2,0,0)
 for g in json.load(open(Path(A.ROOT)/'source/youtube_sign_mesh.json')):
  n=len(g['vertices']);vs=[(x*width,y*width,z) for z in (g['z'],g['z']+g['depth']) for x,y in g['vertices']]
  fs=[]
  for f in g['faces']:fs.extend([tuple(reversed(f)),tuple(j+n for j in f)])
  off=0
  for count in g['rings']:
   fs.extend((off+j,off+(j+1)%count,off+(j+1)%count+n,off+j+n) for j in range(count));off+=count
  ob=A.mesh(g['name'],vs,fs,g['material'],False);ob.parent=root
 for x in (-6.7,-4.4,-1.4,1.0,6.0):
  px=q.x+x;py=q.y+.2
  A.cylinder('Flared sign post footing',(px,py,top+.19),.20,.38,'youtube_frame',20,r2=.065)
  A.rod('Roof sign post',(px,py,top+.38),(px,py,D['sign_base_height']+.55),.055,'youtube_frame',12)
 A.part('Side Google ownership letters')
 q=R.p((663,335),16.7);A.colorword('Google',tuple(q),13.0,4.25,'serif',rot=(pi/2,0,pi/2),depth=.72)
 A.COL['measurement_file']='source/youtube_measurements.json'
 A.COL['variant']='Original full-size historical YouTube sign; deep pale extrusion and old Google ownership lettering.'
 A.COL['inferred_details']='Lobby rear glazing follows the studio view; concealed interiors are not independently evidenced.'
 A.setup_preview(47.134,26.377,1300,1300);R.camera(5)
 return A
if __name__=='__main__':build();A.save_asset('youtube','--no-render' not in sys.argv)
