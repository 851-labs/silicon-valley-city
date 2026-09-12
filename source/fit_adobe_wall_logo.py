"""Fit the historical Adobe artwork within the measured vertical wall plane."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image
from scipy.optimize import differential_evolution
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'source';box=(1210,380,1265,466);zoom=4
im=np.array(Image.open(ROOT/'references/original_wide.webp').crop(box).convert('RGB'));r,g,b=im.transpose(2,0,1).astype(float)
mask=((r>117)&(g>106)&(b>100)&(r/g<1.25)&(b/g>.80)).astype(np.uint8)*255
_,labels,stats,_=cv2.connectedComponentsWithStats(mask);keep=[i for i in range(1,len(stats)) if stats[i,cv2.CC_STAT_AREA]>3 and stats[i,cv2.CC_STAT_TOP]>0];mask=np.isin(labels,keep).astype(np.uint8)*255
target=cv2.resize(mask,None,fx=zoom,fy=zoom,interpolation=cv2.INTER_NEAREST);data=json.loads((P/'adobe_1993_mesh.json').read_text());slope=-32/79
def raster(p):
 x,y,w,h=p;out=np.zeros_like(target)
 for glyph in data:
  layer=np.zeros_like(out);vs=np.array(glyph['vertices']);xy=np.column_stack((x+vs[:,0]*w,y+vs[:,0]*w*slope-vs[:,1]*h));xy=np.round((xy-np.array(box[:2]))*zoom).astype(np.int32);start=0
  for j,count in enumerate(glyph['rings']):cv2.fillPoly(layer,[xy[start:start+count]],255 if j==0 else 0);start+=count
  out|=layer
 return out
def loss(v):
 a=raster(v)>0;b=target>0;return 1-(a&b).sum()/max(1,(a|b).sum())
res=differential_evolution(loss,[(1220,1233),(450,468),(29,43),(35,53)],seed=221,popsize=12,maxiter=100,tol=.0001,polish=False)
report={'scope':'White symbol and wordmark mask only, excluding red wall, building, shadows and material response.','baseline':res.x[:2].tolist(),'width_pixels':float(res.x[2]),'height_pixels_per_svg_unit':float(res.x[3]),'mask_iou':1-float(res.fun)}
(P/'adobe_logo_fit.json').write_text(json.dumps(report,indent=2));d=json.loads((P/'adobe_measurements.json').read_text());d['logo_bottom_left']=report['baseline'];d['logo_width_pixels']=report['width_pixels'];d['logo_height_pixels_per_svg_unit']=report['height_pixels_per_svg_unit'];(P/'adobe_measurements.json').write_text(json.dumps(d,indent=2))
out=cv2.resize(im,None,fx=zoom,fy=zoom,interpolation=cv2.INTER_NEAREST);hit=raster(res.x)>0;out[hit]=(out[hit]*.5+np.array([20,130,190])*.5).astype(np.uint8);Image.fromarray(out).save(ROOT/'matching/adobe_logo_fit.png');Image.fromarray(target).save(ROOT/'matching/adobe_logo_target.png');print('ADOBE_ARTWORK_FIT',report,flush=True)
