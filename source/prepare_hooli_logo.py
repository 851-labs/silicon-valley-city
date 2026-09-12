"""Recover the intro's clean Hooli letters from the branded vector contours.

The published brand icon includes an orbital swoosh absent from the intro. The
second o, l and i are intact. The first o repeats the second; the h is repaired
using the same path's original stem and shoulder coordinates beneath the swoosh.
"""
from pathlib import Path
from svgpathtools import Document,parse_path
from shapely.geometry import Polygon
from shapely import affinity
import json,math,numpy as np,mapbox_earcut
R=Path(__file__).resolve().parents[1];subs=Document(str(R/'references/logos/hooli.svg')).paths()[0].continuous_subpaths()
def polygon(path):
 pts=[]
 for seg in path:
  n=max(2,math.ceil(seg.length()/.30));pts.extend((seg.point(i/n).real,seg.point(i/n).imag) for i in range(n))
 return Polygon(pts).buffer(0)
h=polygon(parse_path('M65.2 352 H123.1 V271.5 C123.1 264.6 124.8 253.3 133.9 253.3 C143 253.3 144.5 260.2 144.5 268.3 V352 H202.2 V252.7 C202.2 234 188.8 215.3 161.6 215.3 C145.8 215.2 131.1 223.5 123.1 237.2 V156.7 L65.2 184 Z'))
o=polygon(subs[5]).difference(polygon(subs[6]));shapes=[h,affinity.translate(o,xoff=-146),o,polygon(subs[4]),polygon(subs[3]),polygon(subs[2])];out=[]
for name,p in zip(['h','o1','o2','l','i-stem','i-dot'],shapes):
 rings=[list(p.exterior.coords)[:-1]]+[list(q.coords)[:-1] for q in p.interiors];vs=np.array([((x-65.2)/574.8,(352-y)/574.8) for r in rings for x,y in r],np.float64);ids=mapbox_earcut.triangulate_float64(vs,np.cumsum([len(r) for r in rings]).astype(np.uint32)).reshape(-1,3)
 out.append({'name':name,'material':'hooli_letter','vertices':vs.tolist(),'faces':ids.tolist(),'rings':[len(r) for r in rings]})
(R/'source/hooli_logo_mesh.json').write_text(json.dumps(out));print('HOOLI_GLYPHS',len(out))
# Artwork attribution is maintained in references/logos/SOURCES.md.
