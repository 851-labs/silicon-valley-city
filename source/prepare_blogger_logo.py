"""Extract the Blogger rounded tile and B contours, excluding SVG shading layers."""
from pathlib import Path
from svgpathtools import Document
from shapely.geometry import Polygon
import json,math,numpy as np,mapbox_earcut
R=Path(__file__).resolve().parents[1];out=[]
for path in Document(str(R/'references/logos/blogger.svg')).paths():
 color=path.element.attrib.get('fill','').lower()
 if color not in ('#ff9800','#f1f1f1'):continue
 polys=[]
 for sub in path.continuous_subpaths():
  points=[]
  for seg in sub:
   n=max(2,math.ceil(seg.length()/.45));points.extend((seg.point(i/n).real/437.5,1-seg.point(i/n).imag/437.5) for i in range(n))
  if len(points)>3:polys.append(Polygon(points).buffer(0))
 shape=polys[0]
 for p in polys[1:]:shape=shape.symmetric_difference(p)
 for p in [shape] if shape.geom_type=='Polygon' else shape.geoms:
  rings=[list(p.exterior.coords)[:-1]]+[list(h.coords)[:-1] for h in p.interiors];vs=np.array([p for r in rings for p in r],np.float64)
  ids=mapbox_earcut.triangulate_float64(vs,np.cumsum([len(r) for r in rings]).astype(np.uint32)).reshape(-1,3)
  out.append({'material':'orange' if color=='#ff9800' else 'white','vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
(R/'source/blogger_logo_mesh.json').write_text(json.dumps(out));print('BLOGGER_SHAPES',len(out))
# Artwork attribution is maintained in references/logos/SOURCES.md.
