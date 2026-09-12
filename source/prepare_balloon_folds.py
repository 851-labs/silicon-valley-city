"""Sample a sculpted cloth surface from measured boundary, fold crests and white patches."""
from pathlib import Path
import json,math,numpy as np
from scipy.spatial import Delaunay
from shapely.geometry import Polygon,Point
P=Path(__file__).parent;d=json.load(open(P/'blue_sculpture_measurements.json'));boundary=Polygon(d['boundary']);patches=[Polygon(q) for q in d['white_patches']];pts=[]
for a,b in zip(d['boundary'],d['boundary'][1:]+d['boundary'][:1]):
 n=max(2,math.ceil(math.dist(a,b)/.6))
 for j in range(n):pts.append([a[0]+(b[0]-a[0])*j/n,a[1]+(b[1]-a[1])*j/n])
for y in np.arange(434,457,.65):
 for x in np.arange(931,994,.65):
  if boundary.contains(Point(x,y)):pts.append([float(x),float(y)])
vertices=[]
for x,y in pts:
 z=.18+.06*math.sin(x*2.1+y*1.8)+.06*math.sin(x*.7-y*1.3)
 for ridge in d['ridges']:
  a=np.array(ridge['a']);b=np.array(ridge['b']);v=b-a;t=float(np.clip(np.dot(np.array([x,y])-a,v)/np.dot(v,v),0,1));dist=np.linalg.norm(np.array([x,y])-a-v*t)
  z+=ridge['height']*math.exp(-(dist/ridge['width'])**2)*math.sin(math.pi*t)**.45
 edge=boundary.boundary.distance(Point(x,y));z=.15+(z-.15)*min(1,edge/1.2);vertices.append([x,y,max(.07,z)])
faces={'blue':[],'white':[]}
for tri in Delaunay(np.array(pts)).simplices:
 q=np.array([pts[i] for i in tri]);c=q.mean(axis=0)
 if not boundary.covers(Point(*c)):continue
 if not boundary.buffer(.01).covers(Polygon(q)):continue
 mat='white' if any(p.covers(Point(*c)) for p in patches) else 'blue';faces[mat].append([int(i) for i in tri])
(P/'balloon_fold_mesh.json').write_text(json.dumps({'vertices':vertices,'faces':faces}));print('BALLOON_FOLDS_READY',len(vertices),{k:len(v) for k,v in faces.items()})
