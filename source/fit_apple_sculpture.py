"""Fit the actual Apple vector's horizontal top face to the source sculpture."""
from pathlib import Path
import cv2,json,math,numpy as np
from PIL import Image
from scipy.optimize import differential_evolution
R=Path(__file__).resolve().parents[1];rect=(1009,341,1104,389);Z=6
im=np.array(Image.open(R/'references/original_wide.webp').convert('RGB').crop(rect));hsv=cv2.cvtColor(im,cv2.COLOR_RGB2HSV)
target=((im.min(2)>213)&(hsv[:,:,1]<40)).astype(np.uint8)*255
# The top face is unobscured. The grey extruded sides are deliberately excluded.
n,lab,st,_=cv2.connectedComponentsWithStats(target);keep=1+np.argmax(st[1:,cv2.CC_STAT_AREA]);target=(lab==keep).astype(np.uint8)*255
target=cv2.resize(target,None,fx=Z,fy=Z,interpolation=cv2.INTER_NEAREST);H,W=target.shape
polys=json.load(open(R/'source/logo_shapes.json'))['apple'];cal=json.load(open(R/'source/camera_calibration.json'));az=math.radians(cal['azimuth']);el=math.radians(cal['elevation'])
def mask(p):
 cx,cy,size,theta=p;out=np.zeros((H,W),np.uint8)
 for poly in polys:
  q=np.array(poly);x=size*(q[:,0]*math.cos(theta)-q[:,1]*math.sin(theta));y=size*(q[:,0]*math.sin(theta)+q[:,1]*math.cos(theta))
  xy=np.stack([cx+5*(math.cos(az)*x+math.sin(az)*y)-rect[0],cy+5*math.sin(el)*(math.sin(az)*x-math.cos(az)*y)-rect[1]],1)*Z
  cv2.fillPoly(out,[np.round(xy).astype(np.int32)],255)
 return out
def loss(p):
 a=mask(p)>0;b=target>0;return 1-(a&b).sum()/max(1,(a|b).sum())
res=differential_evolution(loss,[(1040,1068),(358,374),(13,25),(-math.pi,math.pi)],maxiter=100,popsize=12,seed=42,tol=.0004,polish=False)
data={'top_face_center':res.x[:2].tolist(),'logo_height':float(res.x[2]),'rotation':float(res.x[3]),'silhouette_loss':float(res.fun),'target':'Bright top-face pixels only; this is not a whole-asset fidelity score.'}
(R/'source/apple_sculpture_fit.json').write_text(json.dumps(data,indent=2));print('APPLE_TOP_FIT',data)
out=np.repeat(target[:,:,None],3,2);out[mask(res.x)>0]=(.50*out[mask(res.x)>0]+np.array([110,20,20])).astype(np.uint8);Image.fromarray(out).save(R/'matching/apple_sculpture_fit.png')
