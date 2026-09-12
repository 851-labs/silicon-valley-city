"""Fit a real extruded Hooli vector sign to the original green silhouette."""
from pathlib import Path
import cv2,numpy as np,json,math
from PIL import Image
from scipy.optimize import differential_evolution
R=Path(__file__).resolve().parents[1];rect=(1068,92,1201,211);zoom=4;im=np.array(Image.open(R/'references/original_wide.webp').crop(rect).convert('RGB'));hsv=cv2.cvtColor(im,cv2.COLOR_RGB2HSV)
mask=((hsv[:,:,0]>23)&(hsv[:,:,0]<40)&(hsv[:,:,1]>140)&(hsv[:,:,2]>55)).astype(np.uint8)*255
n,lab,stats,_=cv2.connectedComponentsWithStats(mask);valid=[i for i in range(1,n) if stats[i,cv2.CC_STAT_AREA]>40];mask=np.isin(lab,valid).astype(np.uint8)*255;target=cv2.resize(mask,None,fx=zoom,fy=zoom,interpolation=cv2.INTER_NEAREST);HH,WW=target.shape
data=json.load(open(R/'source/hooli_logo_mesh.json'));cal=json.load(open(R/'source/camera_calibration.json'));az=math.radians(cal['azimuth']);el=math.radians(cal['elevation']);slope=math.tan(az)*math.sin(el);ratio=math.cos(el)/math.cos(az);dn=np.array([-5*math.sin(az),5*math.sin(el)*math.cos(az)])
def raster(p):
 x,y,w,depth,stem=p;ans=np.zeros_like(target)
 # A stack of planar masks reproduces the silhouette of the real extrusion.
 for shift in np.linspace(0,depth,10):
  layer=np.zeros_like(target)
  for g in data:
   vs=np.array(g['vertices'])
   if g['name'] in ('h','l'):vs[:,1]=np.where(vs[:,1]>.238,.238+(vs[:,1]-.238)*stem,vs[:,1])
   xy=np.stack([x+w*vs[:,0],y+w*slope*vs[:,0]-w*ratio*vs[:,1]],1)+dn*shift-np.array(rect[:2]);xy=np.round(xy*zoom).astype(np.int32);offset=0
   for i,count in enumerate(g['rings']):cv2.fillPoly(layer,[xy[offset:offset+count]],255 if i==0 else 0);offset+=count
  ans|=layer
 return ans
def loss(p):
 a=raster(p)>0;b=target>0;return 1-(a&b).sum()/max(1,(a|b).sum())
res=differential_evolution(loss,[(1078,1098),(145,165),(94,114),(.25,3.5),(1.0,2.1)],popsize=9,maxiter=75,seed=42,tol=.0007,polish=False)
d={'baseline':res.x[:2].tolist(),'screen_width':float(res.x[2]),'depth':float(res.x[3]),'stem_scale':float(res.x[4]),'mask_iou':1-float(res.fun),'method':'Original green silhouette compared against an extruded vector. This score excludes the building and materials.'};(R/'source/hooli_logo_fit.json').write_text(json.dumps(d,indent=2));print('HOOLI_SIGN_FIT',d)
out=np.repeat(target[:,:,None],3,2);out[raster(res.x)>0]=(.5*out[raster(res.x)>0]+np.array([90,30,20])).astype(np.uint8);Image.fromarray(out).save(R/'matching/hooli_sign_fit.png');Image.fromarray(target).save(R/'matching/hooli_sign_target.png')
