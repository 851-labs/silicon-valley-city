"""Fit rack tilt independently of the roof-grid spacing, preserving source gaps."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image,ImageDraw
from scipy.optimize import differential_evolution
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'source';d=json.loads((P/'myspace_measurements.json').read_text())
image=np.array(Image.open(ROOT/'references/original_wide.webp').convert('RGB'));rgb=image.astype(float)
mask=np.zeros(image.shape[:2],np.uint8);cv2.fillPoly(mask,[np.array(d['solar_roof'],np.int32)],255);mask=cv2.erode(mask,np.ones((3,3),np.uint8))
mask[(rgb.mean(2)>202)|(rgb[:,:,2]<rgb[:,:,0]*.90)]=0
# Do not fill external contours: that erases the narrow gaps between racks.
num,labels,stats,_=cv2.connectedComponentsWithStats(mask)
mask=np.isin(labels,[i for i in range(1,num) if stats[i,cv2.CC_STAT_AREA]>12]).astype(np.uint8)*255
origin=np.array([805,425]);scale=4;target=cv2.resize(mask[425:490,805:940],(540,260),interpolation=cv2.INTER_NEAREST)>0
def fields(v):
 center=np.array(v[:2]);g1=np.array(v[2:4]);g2=np.array(v[4:6]);a=np.array(v[6:8]);b=np.array(v[8:10]);out=[]
 for i in range(3):
  for j in range(3):
   c=center+i*g1+j*g2;out.append([c-(a+b)/2,c+(a-b)/2,c+(a+b)/2,c+(-a+b)/2])
 return np.array(out)
def iou(polys):
 out=np.zeros(target.shape,np.uint8)
 for p in np.round((polys-origin)*scale).astype(np.int32):cv2.fillConvexPoly(out,p,1)
 out=out>0
 return np.count_nonzero(out&target)/max(1,np.count_nonzero(out|target))
bounds=[(837,843),(448,454),(15,19),(-9,-6),(16,21),(7,11),(8,16),(-15,-8),(15,22),(6,10)]
res=differential_evolution(lambda v:1-iou(fields(v)),bounds,seed=923,popsize=14,maxiter=180,polish=False,tol=.0001)
polys=fields(res.x)
report={'scope':'Nine inclined surface silhouettes with independent roof-grid spacing. Threshold preserves inter-rack gaps. This score excludes cell pattern, colour, support structure and building fidelity.','previous_iou':iou(np.array(d['solar_fields'])),'fitted_iou':iou(polys),'parameters':res.x.tolist(),'fields':np.round(polys,3).tolist()}
(P/'myspace_rack_layout_fit.json').write_text(json.dumps(report,indent=2))
o=Image.fromarray(image);dr=ImageDraw.Draw(o)
for p in polys:dr.line([tuple(q) for q in list(p)+[p[0]]],fill=(255,0,0),width=1)
o.crop((805,425,940,490)).resize((1080,520),Image.Resampling.NEAREST).save(ROOT/'matching/myspace_rack_layout_fitted.png')
Image.fromarray(target.astype(np.uint8)*255).save(ROOT/'matching/myspace_rack_layout_target.png')
print('RACK_LAYOUT_FIT',report['previous_iou'],report['fitted_iou'],flush=True)
