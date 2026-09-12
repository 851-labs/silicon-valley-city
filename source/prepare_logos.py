from pathlib import Path
import json,math
from svgpathtools import svg2paths
from shapely.geometry import Polygon,box
ROOT=Path(__file__).resolve().parents[1]
result={}
for name in ('twitter','apple'):
 paths,_=svg2paths(str(ROOT/'references/logos'/f'{name}.svg'));polys=[]
 for path in paths:
  for sub in path.continuous_subpaths():
   pts=[]
   for seg in sub:
    n=max(3,math.ceil(seg.length()/3))
    pts.extend([[(p:=seg.point(i/n)).real,-p.imag] for i in range(n)])
   if len(pts)>3:polys.append(pts)
 minx=min(p[0] for poly in polys for p in poly);maxx=max(p[0] for poly in polys for p in poly);miny=min(p[1] for poly in polys for p in poly);maxy=max(p[1] for poly in polys for p in poly)
 scale=1/(maxy-miny);cx=(minx+maxx)/2;cy=(miny+maxy)/2
 result[name]=[[[(x-cx)*scale,(y-cy)*scale] for x,y in poly] for poly in polys]
rainbow=[]
colors=['cyan','purple','red','orange','yellow','green']
for pts in result['apple']:
 p=Polygon(pts).buffer(0)
 for i,c in enumerate(colors):
  q=p.intersection(box(-1,-.5+i/6,1,-.5+(i+1)/6))
  for g in ([q] if q.geom_type=='Polygon' else getattr(q,'geoms',[])):
   if not g.is_empty and g.area>.00001:rainbow.append({'color':c,'points':list(map(list,list(g.exterior.coords)[:-1]))})
result['apple_rainbow']=rainbow
(ROOT/'source/logo_shapes.json').write_text(json.dumps(result))
# Artwork attribution is maintained in references/logos/SOURCES.md.
print({k:len(v) for k,v in result.items()})
