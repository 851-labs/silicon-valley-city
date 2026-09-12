"""Triangulate historical publisher vector artwork into reusable extrusion meshes."""
from pathlib import Path
from svgpathtools import Document
from shapely.geometry import Polygon
import json,math,numpy as np,mapbox_earcut
R=Path(__file__).resolve().parents[1]
for name in ['myspace_2013','adobe_1993','digg_2010','zynga','hp_wordmark','hp_1954','hp_1979','facebook_2005']:
 paths=Document(str(R/'references/logos'/f'{name}.svg')).paths();paths=[p for p in paths if p.element.tag.split('}')[-1]in ('path','polygon','rect')]
 if name=='zynga':paths=[p for p in paths if p.element.get('fill')=='#fff']
 if name=='facebook_2005':paths=[p for p in paths if p.element.get('fill')=='#FFFFFF' and p.bbox()[0]<238]
 if name=='adobe_1993':paths=[p for p in paths if p.bbox()[0]<260] # remove the tiny registration symbol
 bounds=[p.bbox() for p in paths];left=min(q[0] for q in bounds);right=max(q[1] for q in bounds);top=min(q[2] for q in bounds);bottom=max(q[3] for q in bounds);width=right-left;out=[]
 for path in paths:
  polys=[]
  for sub in path.continuous_subpaths():
   pts=[]
   for seg in sub:
    n=max(2,math.ceil(seg.length()/.20));pts.extend(((seg.point(i/n).real-left)/width,(bottom-seg.point(i/n).imag)/width) for i in range(n))
   if len(pts)>3:polys.append(Polygon(pts).buffer(0))
  if not polys:continue
  if name=='hp_1954' and 'fill:none' in path.element.get('style',''):
   polys=[p.boundary.buffer(.86/width) for p in polys]
  shape=polys[0]
  for p in polys[1:]:shape=shape.symmetric_difference(p)
  for p in [shape] if shape.geom_type=='Polygon' else shape.geoms:
   if p.geom_type!='Polygon':continue
   rings=[list(p.exterior.coords)[:-1]]+[list(q.coords)[:-1] for q in p.interiors];vs=np.array([q for r in rings for q in r],np.float64);ids=mapbox_earcut.triangulate_float64(vs,np.cumsum([len(r) for r in rings]).astype(np.uint32)).reshape(-1,3)
   out.append({'material':'white','vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
 (R/'source'/f'{name}_mesh.json').write_text(json.dumps(out));print(name,len(out),'aspect',(bottom-top)/width)
