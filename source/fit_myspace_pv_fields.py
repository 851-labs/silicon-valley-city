"""Fit the nine Myspace roof-field footprints; no source image is used as a model texture."""
from pathlib import Path
import json, cv2, numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import differential_evolution

ROOT=Path(__file__).resolve().parents[1];P=ROOT/'source'
d=json.loads((P/'myspace_measurements.json').read_text())
im=np.array(Image.open(ROOT/'references/original_wide.webp').convert('RGB'))
mask=np.zeros(im.shape[:2],np.uint8)
cv2.fillPoly(mask,[np.array(d['solar_roof'],np.int32)],255)
mask=cv2.erode(mask,np.ones((5,5),np.uint8))
rgb=im.astype(float)
mask[(rgb.mean(2)>200)|(rgb[:,:,2]<rgb[:,:,0]*.94)]=0
mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((2,2),np.uint8))
cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
target=np.zeros_like(mask)
cv2.drawContours(target,[c for c in cs if cv2.contourArea(c)>12],-1,255,-1)
origin=np.array([805,425]);size=(135,65);scale=3
target=cv2.resize(target[425:490,805:940],(size[0]*scale,size[1]*scale),interpolation=cv2.INTER_NEAREST)>0
fields=[]
for i in range(3):
 for j in range(3):
  x=828+18*i+15*j;y=455-8*i+8*j
  fields.append([[x,y],[x+17,y-7],[x+30,y-1],[x+13,y+6]])
fields=np.array(fields,float);center=fields.reshape(-1,2).mean(0)
def transform(v):
 sx,sy,kx,ky,tx,ty=v
 return (fields-center)@np.array([[sx,ky],[kx,sy]])+center+np.array([tx,ty])
def score(v):
 q=np.round((transform(v)-origin)*scale).astype(np.int32);m=np.zeros(target.shape,np.uint8)
 for poly in q:cv2.fillConvexPoly(m,poly,1)
 m=m>0
 return np.count_nonzero(m&target)/max(1,np.count_nonzero(m|target))
result=differential_evolution(lambda v:1-score(v),[(.88,1.20),(1.,1.55),(-.32,.32),(-.20,.20),(-12,5),(-9,5)],popsize=14,maxiter=130,seed=915,polish=False,tol=.0001)
polys=transform(result.x)
report={'scope':'Thresholded PV field footprint only. Does not measure cells, colour, facade or whole-asset fidelity.','before_iou':score([1,1,0,0,0,0]),'after_iou':score(result.x),'transform':result.x.tolist(),'fields':np.round(polys,3).tolist()}
(P/'myspace_pv_fit.json').write_text(json.dumps(report,indent=2))
out=Image.fromarray(im);draw=ImageDraw.Draw(out)
for poly in polys:draw.line([tuple(q) for q in list(poly)+[poly[0]]],fill=(255,0,0),width=1)
out.crop((805,425,940,490)).resize((1080,520),Image.Resampling.NEAREST).save(ROOT/'matching/myspace_pv_fitted.png')
Image.fromarray(target.astype(np.uint8)*255).save(ROOT/'matching/myspace_pv_target.png')
print('MYSPACE_PV_FIT',report['before_iou'],report['after_iou'],flush=True)
