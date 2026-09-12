"""Fit the turquoise vector roof mark in the common camera's roof plane."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image
from scipy.optimize import differential_evolution
R=Path(__file__).resolve().parents[1];P=R/'source';box=(474,410,537,440);zoom=5
im=np.array(Image.open(R/'references/original_wide.webp').crop(box).convert('RGB'));r,g,b=im.transpose(2,0,1).astype(float)
mask=((g-r>11)&(b-r>8)&(g>85)).astype(np.uint8)*255
# Blue enclosure walls also meet the colour threshold, but lie outside this
# manually bounded region around the turquoise roof artwork.
region=np.zeros_like(mask)
cv2.fillPoly(region,[np.array([[476,418],[486,412],[510,416],[537,429],[536,437],[517,441],[483,433],[475,425]])-np.array(box[:2])],255)
mask[region==0]=0
target=cv2.resize(mask,None,fx=zoom,fy=zoom,interpolation=cv2.INTER_NEAREST)>0
data=json.loads((P/'intel_logo_mesh.json').read_text())
def raster(v):
 x,y,w,h=v;out=np.zeros(target.shape,np.uint8)
 for glyph in data:
  vs=np.array(glyph['vertices']);xy=np.array([x,y])+vs[:,0,None]*np.array([w,w*.435])+vs[:,1,None]*np.array([-h,h*.505]);xy=np.round((xy-box[:2])*zoom).astype(np.int32);layer=np.zeros_like(out);offset=0
  for j,count in enumerate(glyph['rings']):cv2.fillPoly(layer,[xy[offset:offset+count]],255 if j==0 else 0);offset+=count
  out|=layer
 return out>0
def loss(v):
 a=raster(v);return 1-(a&target).sum()/max(1,(a|target).sum())
res=differential_evolution(loss,[(490,503),(407,418),(38,56),(16,29)],seed=208,popsize=12,maxiter=130,tol=.0001,polish=False)
x,y,w,h=res.x;quad=[[x,y],[x+w,y+w*.435],[x+w-h,y+w*.435+h*.505],[x-h,y+h*.505]]
report={'scope':'Turquoise lettering and oval mask only; excludes height, extrusion, colour response, roof and building fidelity.','quad':quad,'parameters':res.x.tolist(),'feature_mask_iou':1-res.fun}
(P/'intel_roof_logo_fit.json').write_text(json.dumps(report,indent=2)+'\n')
out=cv2.resize(im,None,fx=zoom,fy=zoom,interpolation=cv2.INTER_NEAREST);hit=raster(res.x);out[hit]=(out[hit]*.5+np.array([255,40,30])*.5).astype(np.uint8)
Image.fromarray(out).save(R/'matching/intel_roof_logo_fit.png');Image.fromarray(target.astype(np.uint8)*255).save(R/'matching/intel_roof_logo_target.png')
print('INTEL_ROOF_LOGO_FIT',report,flush=True)
