"""Historical PayPal vectors and traced Pets.com sign artwork, with real counters."""
from pathlib import Path
from svgpathtools import Document
from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np,mapbox_earcut,json,math,cv2
from PIL import Image
R=Path(__file__).resolve().parents[1]
def triangulate(shape,material,out):
 for p in [shape] if shape.geom_type=='Polygon' else shape.geoms:
  if p.area<1e-8:continue
  rings=[list(p.exterior.coords)[:-1]]+[list(h.coords)[:-1] for h in p.interiors]
  vs=np.array([p for r in rings for p in r],np.float64);ids=mapbox_earcut.triangulate_float64(vs,np.cumsum([len(r) for r in rings]).astype(np.uint32)).reshape(-1,3)
  out.append({'material':material,'vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
# Document.paths applies every nested SVG transform, unlike svg2paths.
paths=Document(str(R/'references/logos/paypal_2012.svg')).paths();out=[]
for path in paths:
 if path.element.attrib.get('style','').find('fill:#')<0:continue
 if path.bbox()[0]>275:continue
 polys=[]
 for sub in path.continuous_subpaths():
  pts=[]
  for seg in sub:
   n=max(2,math.ceil(seg.length()/.18));pts.extend(((seg.point(i/n).real-2)/271.54,(78-seg.point(i/n).imag)/271.54) for i in range(n))
  if len(pts)>3:polys.append(Polygon(pts).buffer(0))
 if not polys:continue
 shape=polys[0]
 for p in polys[1:]:shape=shape.symmetric_difference(p)
 mat='paypal_light_blue' if '#336699' in path.element.attrib['style'] else 'paypal_dark_blue';triangulate(shape,mat,out)
(R/'source/paypal_logo_mesh.json').write_text(json.dumps(out));print('PAYPAL_MESHES',len(out))
# Paw and glyph contours are geometry, rather than a photograph applied to the building.
im=np.array(Image.open(R/'references/logos/pets_com.png').convert('RGB'));m=np.uint8(np.max(im,axis=2)<100)*255
contours,h=cv2.findContours(m,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE);out=[]
for i,c in enumerate(contours):
 if h[0,i,3]!=-1 or cv2.contourArea(c)<1:continue
 ext=[(x/203,(42-y)/203) for x,y in c[:,0,:]];holes=[];k=h[0,i,2]
 while k!=-1:
  holes.append([(x/203,(42-y)/203) for x,y in contours[k][:,0,:]]);k=h[0,k,0]
 shape=Polygon(ext,holes).buffer(0);triangulate(shape,'pets_green' if min(p[0] for p in ext)>.20 else 'pets_ink',out)
(R/'source/pets_logo_mesh.json').write_text(json.dumps(out));print('PETS_MESHES',len(out))
# Artwork attribution is maintained in references/logos/SOURCES.md.
