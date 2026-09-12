from pathlib import Path
from svgpathtools import svg2paths
from shapely.geometry import Polygon
import math,json,numpy as np,mapbox_earcut
R=Path(__file__).resolve().parents[1];paths,attrs=svg2paths(str(R/'references/logos/intel_2006.svg'))
polys=[]
for sub in paths[0].continuous_subpaths():
 points=[]
 for seg in sub:
  n=max(2,math.ceil(seg.length()/.35));points.extend((seg.point(i/n).real,seg.point(i/n).imag) for i in range(n))
 if len(points)>3:polys.append(Polygon(points).buffer(0))
shape=polys[0]
for p in polys[1:]:shape=shape.symmetric_difference(p)
x0,y0,x1,y1=shape.bounds;out=[]
for poly in [shape] if shape.geom_type=='Polygon' else shape.geoms:
 rings=[list(poly.exterior.coords)[:-1]]+[list(h.coords)[:-1] for h in poly.interiors]
 vs=np.array([[(x-x0)/(x1-x0),(y-y0)/(y1-y0)] for ring in rings for x,y in ring],np.float64)
 ids=mapbox_earcut.triangulate_float64(vs,np.cumsum([len(r) for r in rings]).astype(np.uint32)).reshape(-1,3)
 out.append({'vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
(R/'source/intel_logo_mesh.json').write_text(json.dumps(out))
# Artwork attribution is maintained in references/logos/SOURCES.md.
print('INTEL_LOGO_MESHES',len(out))
