from pathlib import Path
import json,math
import numpy as np,mapbox_earcut
from svgpathtools import svg2paths
from shapely.geometry import Polygon
ROOT=Path(__file__).resolve().parents[1]
paths,attrs=svg2paths(str(ROOT/'references/logos/google_2013.svg'))
output=[]
for path,attr in zip(paths,attrs):
 shapes=[]
 for sub in path.continuous_subpaths():
  pts=[]
  for seg in sub:
   n=max(2,math.ceil(seg.length()/.65))
   pts.extend((seg.point(i/n).real,55-seg.point(i/n).imag) for i in range(n))
  if len(pts)>3:shapes.append(Polygon(pts).buffer(0))
 shape=shapes[0]
 for q in shapes[1:]:shape=shape.symmetric_difference(q)
 color={'#FA472F':'red','#009D53':'green','#0065EA':'blue','#FFBA00':'yellow'}.get(attr.get('fill'))
 if color is None:
  h=attr['fill'].lstrip('#');rgb=[int(h[i:i+2],16) for i in (0,2,4)];color='yellow' if rgb[0]>150 and rgb[1]>100 else 'red' if rgb[0]>rgb[1] and rgb[0]>rgb[2] else 'green' if rgb[1]>rgb[2] else 'blue'
 for poly in ([shape] if shape.geom_type=='Polygon' else shape.geoms):
  rings=[list(poly.exterior.coords)[:-1]]+[list(r.coords)[:-1] for r in poly.interiors]
  vs=np.array([[(x-113.913)/227.826,y/227.826] for ring in rings for x,y in ring]);ends=np.cumsum([len(r) for r in rings]).astype(np.uint32)
  ids=mapbox_earcut.triangulate_float64(vs,ends).reshape(-1,3)
  output.append({'color':color,'vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
(ROOT/'source/google_logo_mesh.json').write_text(json.dumps(output))
# Artwork attribution is maintained in references/logos/SOURCES.md.
print('Prepared',len(output),'Google glyph meshes')
