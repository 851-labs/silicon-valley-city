"""Measured original-frame curved pavilion with Digg billboard and dry terrace."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
import build_digg_variant
from reference_geometry import Reference,set_color
from mathutils import Vector,Matrix
P=Path(__file__).parent

def build():
 D=json.load(open(P/'netscape_digg_measurements.json'));build_digg_variant.build();intrinsic=A.COL['applied_reference_proportions'];rot=Matrix.Rotation(math.radians(D['rotation']),4,'Z');front=rot@Vector(tuple(D['front_model'][i]*intrinsic[i] for i in range(3)));transform=Matrix.Translation((-front.x,-front.y,0))@rot
 for ob in A.COL.objects:
  if ob.parent is None:ob.matrix_world=transform@ob.matrix_world
 for ob in list(A.COL.objects):
  part=ob.get('part','');name=ob.name
  if part.startswith('Raised pool') or part.startswith('Netscape historical') or part.startswith('Digg original') or name.startswith(('Netscape ','N logo','Digg blue','Pool stone','Pool water','Pool raised')):A.bpy.data.objects.remove(ob,do_unlink=True)
 R=Reference(D['anchor'],D['crop']);A.part('Measured Digg billboard');A.material('digg_sign_blue',(.032,.12,.21),.76)
 bottom=R.p(D['sign_bottom_left'],D['sign_base']);right=R.p(D['sign_bottom_right'],D['sign_base']);u=(right-bottom).normalized();L=(right-bottom).length;v=Vector((0,0,D['sign_height']));n=u.cross(v).normalized()
 if n.x<0:n=-n
 vs=[tuple(p+n*z) for z in [0,.24] for p in [bottom,right,right+v,bottom+v]];A.mesh('Thick measured blue Digg board',vs,[(0,3,2,1),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],'digg_sign_blue')
 patterns={'d':['001','001','111','101','101','111','000'],'i':['1','0','1','1','1','1','0'],'g':['000','000','111','101','111','001','111']};cols=[]
 for ch in 'digg':
  p=patterns[ch]
  for i in range(len(p[0])):cols.append([p[j][i] for j in range(7)])
  cols.append(['0']*7)
 cols=cols[:-1];sx=L*.84/len(cols);sz=D['sign_height']*.68/7
 for i,col in enumerate(cols):
  for j,value in enumerate(col):
   if value=='1':
    q=bottom+u*(L*.08+i*sx)+Vector((0,0,D['sign_height']*.17+(6-j)*sz))+n*.265
    A.mesh('Raised Digg pixel',[tuple(q),tuple(q+u*sx*.98),tuple(q+u*sx*.98+Vector((0,0,sz*.98))),tuple(q+Vector((0,0,sz*.98)))],[(0,1,2,3)],'white')
 A.COL['measurement_file']='source/netscape_digg_measurements.json';A.COL['inferred_details']='The roof sail and flowing floor plates retain their studio-derived profiles; their curves require exact contour comparison in this camera.'
 R.camera(5);set_color(A.MAT['curved_shell'],(.53,.54,.51));set_color(A.MAT['curtain_glass'],(.085,.096,.088));A.flush();return A
if __name__=='__main__':build();A.save_asset('netscape_digg','--no-render' not in sys.argv)
