import os,sys,math
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
import build_netscape
from math import pi
def build():
 build_netscape.build(original=True)
 # Retain the modeled pavilion; swap the season-dependent sign assembly.
 for ob in list(A.COL.objects):
  if 'Android' in ob.name or 'android' in ob.name:A.bpy.data.objects.remove(ob,do_unlink=True)
 A.COL.name='ASSET • Digg curved pavilion • original wide frame'
 A.COL['asset_id']='netscape_digg';A.COL['variant']='Original wide-frame Digg billboard on the curved pavilion; separate Android version retained in library.'
 A.part('Digg original blue billboard')
 x,y,z=9.37,15.0,8.20
 ob=A.sign_panel('Digg blue billboard',(x,y,z),10.7,5.7,'glass_blue',.25,.16);ob.rotation_euler=(pi/2,0,pi/2)
 patterns={'d':['001','001','111','101','101','111','000'],'i':['1','0','1','1','1','1','0'],'g':['000','000','111','101','111','001','111']}
 cols=[]
 for ch in 'digg':
  p=patterns[ch]
  for i in range(len(p[0])):cols.append([p[j][i] for j in range(7)])
  cols.append(['0']*7)
 cell=.58;start=y-len(cols)*cell/2
 for i,col in enumerate(cols):
  for j,v in enumerate(col):
   if v=='1':A.box('Digg white pixel',(x+.175,start+(i+.5)*cell,z+2.05-(j+.5)*cell),(.09,cell*.98,cell*.98),'white')
 A.flush()
 # Reframe after the variant swap and apply its independently fitted proportions.
 for c in list(A.bpy.data.collections):
  if c.name.startswith('STUDIO'):
   for o in list(c.objects):A.bpy.data.objects.remove(o,do_unlink=True)
   A.bpy.data.collections.remove(c)
 del A.COL['applied_reference_proportions']
 A.setup_preview(42.531,26.377,1600,1050)
 return A
if __name__=='__main__':build();A.save_asset('netscape_digg')
