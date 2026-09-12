"""Compare both Google wordmark contours to the coloured source glyphs."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image,ImageDraw
from scipy.optimize import differential_evolution,minimize
R=Path(__file__).resolve().parents[1];N=600;ZOOM=4
C=['blue','red','yellow','green'];bounds=(368,478,509,561)
source=np.array(Image.open(R/'references/original_wide.webp').convert('RGB'))
hsv=cv2.cvtColor(source,cv2.COLOR_RGB2HSV)
regions={'blue':[(374,482,420,525),(449,508,483,556)],'red':[(409,493,448,539),(476,514,504,554)],'yellow':[(432,502,468,546)],'green':[(468,495,491,549)]}
def masks(im,alpha=None):
 h=cv2.cvtColor(im,cv2.COLOR_RGB2HSV);sat=h[:,:,1]>70
 hh=h[:,:,0]
 ans=[((hh>95)&(hh<135)),((hh<16)|(hh>170)),((hh>17)&(hh<38)),((hh>40)&(hh<92))]
 return [(q&sat&(alpha>128 if alpha is not None else True)).astype(np.uint8)*255 for q in ans]
target=masks(source)
for i,k in enumerate(C):
 valid=np.zeros(source.shape[:2],np.uint8)
 for l,t,r,b in regions[k]:valid[t:b,l:r]=255
 target[i]&=valid
 target[i]=cv2.resize(target[i][bounds[1]:bounds[3],bounds[0]:bounds[2]],None,fx=ZOOM,fy=ZOOM,interpolation=cv2.INTER_NEAREST)
# 2013 geometry is available as triangulated original vector artwork.
old=[np.zeros((240,N),np.uint8) for _ in C]
for g in json.loads((R/'source/google_logo_mesh.json').read_text()):
 pts=np.array([[(x+.5)*N,(.245-y)*N] for x,y in g['vertices']],np.int32)
 for f in g['faces']:cv2.fillConvexPoly(old[C.index(g['color'])],pts[f],255)
new=np.array(Image.open(R/'references/logos/google_2015.png').convert('RGBA'));new=masks(new[:,:,:3],new[:,:,3]);new=[cv2.resize(q,(N,round(q.shape[0]*N/q.shape[1])),interpolation=cv2.INTER_NEAREST) for q in new]
H,W=target[0].shape
def warped(template,p):
 x,y,w,s,v=p
 m=np.array([[w*ZOOM/N,0,x*ZOOM],[s*ZOOM/N,v*ZOOM/N,y*ZOOM]],np.float32)
 return [cv2.warpAffine(q,m,(W,H),flags=cv2.INTER_NEAREST) for q in template]
def objective(p,template):
 qs=warped(template,p);loss=[]
 for a,b in zip(qs,target):
  # A small symmetric tolerance allows source antialiasing and shallow extrusion.
  union=np.logical_or(a,b).sum();inter=np.logical_and(a,b).sum()
  loss.append(1-inter/max(1,union))
 return float(np.mean(loss))
results={}
for name,tpl in [('2013',old),('2015',new)]:
 result=differential_evolution(lambda p:objective(p,tpl),[(0,22),(-8,20),(105,145),(28,55),(95,175)],seed=42,popsize=8,maxiter=55,tol=.002,polish=False,workers=1)
 results[name]={'loss':float(result.fun),'parameters':result.x.tolist()};print(name,results[name],flush=True)
 out=np.full((H,W,3),230,np.uint8)
 colors=[(50,95,220),(220,55,30),(235,190,20),(30,140,70)]
 for q,c in zip(warped(tpl,result.x),colors):out[q>0]=c
 Image.fromarray(out).save(R/'matching'/f'google_logo_{name}_fit.png')
out=np.full((H,W,3),230,np.uint8)
for q,c in zip(target,[(50,95,220),(220,55,30),(235,190,20),(30,140,70)]):out[q>0]=c
Image.fromarray(out).save(R/'matching/google_logo_source_mask.png')
(R/'matching/google_logo_fit.json').write_text(json.dumps(results,indent=2))
