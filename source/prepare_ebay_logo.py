"""Extrudable eBay vector contours; colors use the 2012 identity."""
from pathlib import Path
from svgpathtools import svg2paths
from shapely.geometry import Polygon
import numpy as np,mapbox_earcut,json,math
R=Path(__file__).resolve().parents[1];paths,attrs=svg2paths(str(R/'references/logos/ebay_2012.svg'));out=[]
for path,mat in zip(paths,['yellow','red','blue','green']):
 polys=[]
 for sub in path.continuous_subpaths():
  points=[]
  for seg in sub:
   n=max(2,math.ceil(seg.length()/.7));points.extend((seg.point(i/n).real/1000,(324.89544-seg.point(i/n).imag)/1000) for i in range(n))
  if len(points)>3:polys.append(Polygon(points).buffer(0))
 shape=polys[0]
 for p in polys[1:]:shape=shape.symmetric_difference(p)
 for p in [shape] if shape.geom_type=='Polygon' else shape.geoms:
  rings=[list(p.exterior.coords)[:-1]]+[list(h.coords)[:-1] for h in p.interiors];vs=np.array([p for r in rings for p in r],np.float64)
  ids=mapbox_earcut.triangulate_float64(vs,np.cumsum([len(r) for r in rings]).astype(np.uint32)).reshape(-1,3)
  out.append({'material':mat,'vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
(R/'source/ebay_logo_mesh.json').write_text(json.dumps(out))
# Artwork attribution is maintained in references/logos/SOURCES.md.
print('EBAY_GLYPHS',len(out))
