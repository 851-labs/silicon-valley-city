from pathlib import Path
from svgpathtools import Document
from shapely.geometry import Polygon
import math,json,numpy as np,mapbox_earcut
R=Path(__file__).resolve().parents[1];out=[]
for path in Document(str(R/'references/logos/linkedin_2011.svg')).paths():
 polys=[];style=path.element.attrib.get('style','');color=path.element.attrib.get('fill','')
 for sub in path.continuous_subpaths():
  pts=[]
  for seg in sub:
   n=max(2,math.ceil(seg.length()/.25));pts.extend((seg.point(i/n).real/291,(79.46-seg.point(i/n).imag)/291) for i in range(n))
  if len(pts)>3:polys.append(Polygon(pts).buffer(0))
 if not polys:continue
 shape=polys[0]
 for p in polys[1:]:shape=shape.symmetric_difference(p)
 mat='linkedin_white' if '#ffffff' in style.lower() or color.lower() in ['#fff','#ffffff','white'] else ('linkedin_blue' if any(s in style.lower()+color.lower() for s in ['#006699','#0077b5','#007bb6']) else 'linkedin_ink')
 for p in [shape] if shape.geom_type=='Polygon' else shape.geoms:
  rings=[list(p.exterior.coords)[:-1]]+[list(h.coords)[:-1] for h in p.interiors];vs=np.array([p for r in rings for p in r],np.float64)
  ids=mapbox_earcut.triangulate_float64(vs,np.cumsum([len(r) for r in rings]).astype(np.uint32)).reshape(-1,3)
  out.append({'material':mat,'vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
(R/'source/linkedin_logo_mesh.json').write_text(json.dumps(out));print('LINKEDIN_PARTS',len(out),set(x['material'] for x in out))
# Artwork attribution is maintained in references/logos/SOURCES.md.
