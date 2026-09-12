"""Fit the nine measured PV field footprints to the observed roof mask."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image,ImageDraw
from scipy.optimize import differential_evolution
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'source';d=json.loads((P/'yahoo_oracle_measurements.json').read_text());im=np.array(Image.open(ROOT/'references/original_wide.webp').convert('RGB'))
mask=np.zeros(im.shape[:2],np.uint8);cv2.fillPoly(mask,[np.array(d['volumes'][1]['roof'],np.int32)],255);mask=cv2.erode(mask,np.ones((3,3),np.uint8));mask[(im.mean(2)>205)|(im[:,:,2].astype(float)<im[:,:,0]*.92)]=0
cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);target=np.zeros_like(mask);cv2.drawContours(target,[max(cs,key=cv2.contourArea)],-1,255,-1)
origin=np.array([920,40]);size=(154,66);scale=3;target=cv2.resize(target[40:106,920:1074],(size[0]*scale,size[1]*scale),interpolation=cv2.INTER_NEAREST)>0
before=P/'oracle_pv_before_fit.json'
if not before.exists():before.write_text(json.dumps(d['panels'],indent=2))
fields=np.array(json.loads(before.read_text()),float);center=fields.reshape(-1,2).mean(0)
def transform(v):
 sx,sy,kx,ky,tx,ty=v;return (fields-center)@np.array([[sx,ky],[kx,sy]])+center+np.array([tx,ty])
def score(v):
 q=np.round((transform(v)-origin)*scale).astype(np.int32);m=np.zeros(target.shape,np.uint8)
 for poly in q:cv2.fillConvexPoly(m,poly,1)
 m=m>0;return np.count_nonzero(m&target)/np.count_nonzero(m|target)
result=differential_evolution(lambda v:1-score(v),[(.86,1.08),(.85,1.10),(-.16,.16),(-.13,.13),(-10,5),(-5,6)],popsize=12,maxiter=90,seed=631,polish=False,tol=.0001)
polys=transform(result.x);d['panels']=np.round(polys,3).tolist();(P/'yahoo_oracle_measurements.json').write_text(json.dumps(d,indent=2))
report={'scope':'PV footprint mask only. Does not measure facade, material, module cells or whole-building similarity.','before_iou':score([1,1,0,0,0,0]),'after_iou':score(result.x),'transform':result.x.tolist(),'fields':d['panels']};(P/'oracle_pv_fit.json').write_text(json.dumps(report,indent=2))
out=Image.fromarray(im);draw=ImageDraw.Draw(out)
for poly in polys:draw.line([tuple(q) for q in list(poly)+[poly[0]]],fill=(255,0,0),width=1)
out.crop((920,40,1074,106)).resize((1232,528),Image.Resampling.NEAREST).save(ROOT/'matching/oracle_pv_fitted.png');print('PV_FOOTPRINT_FIT',report['before_iou'],report['after_iou'],flush=True)
