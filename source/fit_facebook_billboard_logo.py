"""Fit historical Facebook glyphs within the measured campus billboard."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image
from scipy.optimize import differential_evolution
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'source';box=(672,90,743,144);zoom=5
im=np.array(Image.open(ROOT/'references/original_wide.webp').crop(box).convert('RGB'));r,g,b=im.transpose(2,0,1).astype(float)
region=np.zeros(im.shape[:2],np.uint8);cv2.fillPoly(region,[np.array([[674,117],[740,92],[740,114],[674,139]])-np.array(box[:2])],255)
mask=((r>83)&(g>83)&(r/np.maximum(b,1)>.78)&(region>0)).astype(np.uint8)*255
target=cv2.resize(mask,None,fx=zoom,fy=zoom,interpolation=cv2.INTER_NEAREST)
data=json.loads((P/'facebook_2005_mesh.json').read_text());slope=-28/73
def raster(v):
 x,y,w,h=v;out=np.zeros_like(target)
 for glyph in data:
  layer=np.zeros_like(out);vs=np.array(glyph['vertices']);xy=np.column_stack((x+vs[:,0]*w,y+vs[:,0]*w*slope-vs[:,1]*h));xy=np.round((xy-np.array(box[:2]))*zoom).astype(np.int32);start=0
  for j,count in enumerate(glyph['rings']):cv2.fillPoly(layer,[xy[start:start+count]],255 if j==0 else 0);start+=count
  out|=layer
 return out
def loss(v):
 a=raster(v)>0;b=target>0
 return 1-(a&b).sum()/max(1,(a|b).sum())
res=differential_evolution(loss,[(674,680),(135,141),(59,67),(65,100)],seed=512,popsize=12,maxiter=95,tol=.0001,polish=False)
report={'scope':'White campus billboard glyph mask only; excludes building geometry, blue board, extrusion and shading.','baseline':res.x[:2].tolist(),'width_pixels':float(res.x[2]),'height_pixels_per_svg_unit':float(res.x[3]),'mask_iou':1-float(res.fun)}
(P/'facebook_billboard_logo_fit.json').write_text(json.dumps(report,indent=2))
out=cv2.resize(im,None,fx=zoom,fy=zoom,interpolation=cv2.INTER_NEAREST);hit=raster(res.x)>0;out[hit]=(out[hit]*.5+np.array([30,150,200])*.5).astype(np.uint8)
Image.fromarray(out).save(ROOT/'matching/facebook_billboard_logo_fit.png');Image.fromarray(target).save(ROOT/'matching/facebook_billboard_logo_target.png')
print('FACEBOOK_BILLBOARD_GLYPH_FIT',report,flush=True)
