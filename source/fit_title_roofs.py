"""Fit each studio-traced title roof independently to its original-frame outline."""
from pathlib import Path
import json,math,cv2,numpy as np,mapbox_earcut
from scipy.optimize import differential_evolution
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];P=R/'source';source=json.load(open(P/'title_footprints.json'));components=json.load(open(P/'title_master_components.json'));cal=json.load(open(P/'camera_calibration.json'));aff=np.array(cal['affine']);mapping={'front_1_V':10,'front_2_A':8,'front_3_L':6,'front_4_L':4,'front_5_E':2,'front_6_Y':1,'rear_1_S':13,'rear_2_I':12,'rear_3_L':11,'rear_4_I':9,'rear_5_C':7,'rear_6_O':5,'rear_7_N':3};out=[];reports={};zoom=5
az=math.radians(cal['azimuth']);el=math.radians(cal['elevation']);project=np.array([[5*math.cos(az),5*math.sin(az)],[5*math.sin(el)*math.sin(az),-5*math.sin(el)*math.cos(az)]]);inv=np.linalg.inv(project);anchor=aff[:,2];sx=cal['title_pixels_per_unit']/5
for item in source['letters']:
 target=components[mapping[item['id']]];c=np.array(target['center']);rings=[np.array(r)@aff[:,:2].T+aff[:,2] for r in item['rings']];allp=np.concatenate(rings);low=np.floor(np.minimum(allp.min(0),np.array(target['contour']).min(0))-7);high=np.ceil(np.maximum(allp.max(0),np.array(target['contour']).max(0))+7);wh=((high-low)*zoom).astype(int);mask=np.zeros(tuple(wh[::-1]),np.uint8)
 cv2.fillPoly(mask,[np.round((np.array(target['contour'])-low)*zoom).astype(np.int32)],255)
 for hole in target['holes']:cv2.fillPoly(mask,[np.round((np.array(hole)-low)*zoom).astype(np.int32)],0)
 def transform(p):
  dx,dy,a,b,hx,hy=p;m=np.array([[a,hx],[hy,b]]);return [(r-c)@m.T+c+np.array([dx,dy]) for r in rings]
 def render(p):
  dest=np.zeros_like(mask)
  for i,ring in enumerate(transform(p)):cv2.fillPoly(dest,[np.round((ring-low)*zoom).astype(np.int32)],255 if i==0 else 0)
  return dest
 def loss(p):
  a=render(p)>0;b=mask>0;return 1-(a&b).sum()/max(1,(a|b).sum())
 res=differential_evolution(loss,[(-4,4),(-4,4),(.93,1.07),(.93,1.07),(-.055,.055),(-.055,.055)],seed=42,popsize=8,maxiter=85,tol=.001,polish=False)
 pixel_rings=transform(res.x);normalized=[((r-anchor)@inv.T/sx).tolist() for r in pixel_rings];vertices=np.array([v for r in normalized for v in r],np.float64);ends=np.cumsum([len(r) for r in normalized],dtype=np.uint32);indices=mapbox_earcut.triangulate_float64(vertices,ends).reshape(-1,3)
 updated=dict(item);updated.update(rings=normalized,triangles=[vertices[t].tolist() for t in indices],reference_roof_rings=[r.tolist() for r in pixel_rings]);out.append(updated)
 reports[item['id']]={'roof_mask_iou':1-float(res.fun),'parameters':res.x.tolist(),'source_component':target['id']};print('TITLE_ROOF_FIT',item['id'],round(1-res.fun,4),flush=True)
 result=np.zeros((*mask.shape,3),np.uint8);result[mask>0]=[100,170,200];result[render(res.x)>0]=[225,115,75];Image.fromarray(result).save(R/'matching'/f'title_{item["id"]}_roof_fit.png')
source.update(letters=out,source='Original wide frame + YU30',method='Thirteen independent fits of the studio vector roof contours to original-frame roof masks. Small planar corrections preserve smooth studio outlines.')
(P/'title_matched_footprints.json').write_text(json.dumps(source,indent=2));(P/'title_roof_fit_report.json').write_text(json.dumps(reports,indent=2))
d={'reference':'original_wide.webp','anchor':[float(anchor[0]),float(anchor[1]),30.73*.48],'crop':[701,76,1081,328],'status':'Studio roof contours fitted individually to all thirteen original-frame letters. Nine facade storeys and parking screen retained; facade correspondence remains under comparison.'}
(P/'title_towers_measurements.json').write_text(json.dumps(d,indent=2));print('TITLE_ROOFS_READY',len(out))
