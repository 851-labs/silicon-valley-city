"""Recover roof footprints from the studio's 12K title model image."""
from pathlib import Path
import cv2,numpy as np,json,math,mapbox_earcut
from shapely.geometry import Polygon
from shapely.ops import triangulate
ROOT=Path(__file__).resolve().parents[1]
image=cv2.imread(str(next((ROOT/'references/studio').glob('YU30_*'))))
image=cv2.resize(image,(4000,2700));b,g,r=cv2.split(image)
mask=((r.astype(float)>1.9*g)&(r.astype(float)>1.9*b)&(r>120)).astype('uint8')*255
contours,hierarchy=cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
# Long straight roof edges measured in the image: +25.6 and -23.5 degrees.
sx,sy=math.tan(math.radians(25.6)),math.tan(math.radians(23.5))
e=math.asin(math.sqrt(sx*sy));a=math.atan(sx/math.sin(e))
projection=np.array([[math.cos(a),math.sin(a)],[math.sin(e)*math.sin(a),-math.sin(e)*math.cos(a)]])
inverse=np.linalg.inv(projection)
def ring(c):return (cv2.approxPolyDP(c,2.10,True).reshape(-1,2)@inverse.T).tolist()
polys=[]
for i,c in enumerate(contours):
 if cv2.contourArea(c)<500 or hierarchy[0][i][3]!=-1:continue
 holes=[];child=hierarchy[0][i][2]
 while child!=-1:
  if cv2.contourArea(contours[child])>100:holes.append(ring(contours[child]))
  child=hierarchy[0][child][0]
 poly=Polygon(ring(c),holes).buffer(0);polys.append(poly)
assert len(polys)==13,len(polys)
minx=min(p.bounds[0] for p in polys);maxx=max(p.bounds[2] for p in polys);miny=min(p.bounds[1] for p in polys);maxy=max(p.bounds[3] for p in polys)
scale=132/(maxx-minx);origin=np.array([(minx+maxx)/2,(miny+maxy)/2])
ordered=sorted(polys,key=lambda p:p.centroid.y);cut=max(range(1,13),key=lambda i:ordered[i].centroid.y-ordered[i-1].centroid.y)
front,rear=ordered[:cut],ordered[cut:];assert (len(front),len(rear))==(6,7)
result=[]
for row,items,word in [('front',front,'VALLEY'),('rear',rear,'SILICON')]:
 for i,(p,letter) in enumerate(zip(sorted(items,key=lambda p:p.centroid.x),word)):
  def transform(coords):return ((np.array(coords)[:-1]-origin)*scale).tolist()
  rings=[transform(p.exterior.coords)]+[transform(r.coords) for r in p.interiors]
  shape=Polygon(rings[0],rings[1:]);vertices=np.array([p for r in rings for p in r],dtype=np.float64)
  ends=np.cumsum([len(r) for r in rings],dtype=np.uint32)
  indices=mapbox_earcut.triangulate_float64(vertices,ends).reshape(-1,3)
  tris=[vertices[t].tolist() for t in indices]
  result.append({'id':row+'_'+str(i+1)+'_'+letter,'letter':letter,'row':row,'rings':rings,'triangles':tris,'bounds':list(shape.bounds),'area':shape.area})
out={'source':'YU30','method':'Red roof silhouettes traced from 12001×8100 studio image; parallel roof edges determine affine rectification. Overall scale inferred.','camera':{'azimuth':math.degrees(a),'elevation':math.degrees(e)},'width_m':132,'letters':result}
(ROOT/'source/title_footprints.json').write_text(json.dumps(out,indent=2))
# A plan drawing is an inspection artifact, with the recovered contours labeled.
from PIL import Image,ImageDraw
canvas=Image.new('RGB',(1800,850),'#f2eee4');draw=ImageDraw.Draw(canvas)
for p in result:
 points=[(900+x*12,425-y*12) for x,y in p['rings'][0]];draw.polygon(points,fill='#d83124',outline='#181818',width=2)
 for hole in p['rings'][1:]:draw.polygon([(900+x*12,425-y*12) for x,y in hole],fill='#f2eee4',outline='#181818',width=2)
canvas.save(ROOT/'references/title_recovered_plan.png')
print('Recovered 13 roof footprints. Camera:',out['camera'])
print([(p['id'],[round(v,2) for v in p['bounds']]) for p in result])
