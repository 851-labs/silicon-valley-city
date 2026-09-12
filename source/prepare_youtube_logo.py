"""Convert historical YouTube vector contours into separate editable sign parts."""
from pathlib import Path
from svgpathtools import svg2paths
from shapely.geometry import Polygon
import numpy as np,mapbox_earcut,json,math
R=Path(__file__).resolve().parents[1]
paths,attrs=svg2paths(str(R/'references/logos/youtube_2013.svg'))
output=[]
def emit(name,path,mat,depth,z):
 rings=[]
 for sub in path.continuous_subpaths():
  pts=[]
  for seg in sub:
   n=max(2,math.ceil(seg.length()/.04))
   pts.extend(((seg.point(i/n).real-28)/56,(24-seg.point(i/n).imag)/56) for i in range(n))
  if len(pts)>3:rings.append(Polygon(pts).buffer(0))
 # Even-odd compound contours preserve the counters inside each letter.
 shape=rings[0]
 for ring in rings[1:]:shape=shape.symmetric_difference(ring)
 for j,poly in enumerate([shape] if shape.geom_type=='Polygon' else shape.geoms):
  rings=[list(poly.exterior.coords)[:-1]]+[list(q.coords)[:-1] for q in poly.interiors]
  vs=np.array([p for ring in rings for p in ring],dtype=np.float64);end=np.cumsum([len(q) for q in rings]).astype(np.uint32)
  ids=mapbox_earcut.triangulate_float64(vs,end).reshape(-1,3)
  output.append({'name':name+str(j),'material':mat,'vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(q) for q in rings],'depth':depth,'z':z})
# Source production sign has pale, deep extrusion behind the red and black front faces.
emit('You pale letter extrusion',paths[0],'white',.8,-.8)
emit('You black letter face',paths[0],'black',.025,0)
subs=paths[2].continuous_subpaths();emit('Tube deep pale capsule',subs[0],'white',1.8,-1.8);emit('Tube red capsule',subs[0],'red',.04,0)
for i,sub in enumerate(subs[1:]):emit('Tube white glyph '+str(i),sub,'white',.025,.041)
emit('Tube red counters',paths[1],'red',.029,.043)
(R/'source/youtube_sign_mesh.json').write_text(json.dumps(output))
# Artwork attribution is maintained in references/logos/SOURCES.md.
print('YOUTUBE_SIGN_PARTS',len(output))
