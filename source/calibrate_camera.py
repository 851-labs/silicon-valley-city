"""Fit the original wide-frame title roof centroids to the recovered roof plan."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image
from shapely.geometry import Polygon
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'source/title_footprints.json').read_text())
im=np.array(Image.open(ROOT/'references/original_wide.webp').convert('RGB')).astype(float)
r,g,b=im[:,:,0],im[:,:,1],im[:,:,2]
mask=((r>1.35*g)&(r>1.5*b)&(r>130)).astype('uint8')*255
mask[:80,:]=0;mask[260:,:]=0;mask[:,:715]=0;mask[:,1085:]=0
cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cs=sorted([c for c in cs if cv2.contourArea(c)>180],key=lambda c:cv2.boundingRect(c)[0])
mapping={'front_1_V':0,'front_2_A':1,'front_3_L':3,'front_4_L':5,'front_5_E':7,'front_6_Y':9,'rear_1_S':2,'rear_2_I':4,'rear_7_N':10}
X=[];Y=[]
for letter in data['letters']:
 if letter['id'] not in mapping:continue
 c=Polygon(letter['rings'][0]).centroid;X.append([c.x,c.y,1]);m=cv2.moments(cs[mapping[letter['id']]])
 Y.append([m['m10']/m['m00'],m['m01']/m['m00']])
M=np.linalg.lstsq(np.array(X),np.array(Y),rcond=None)[0].T;pred=np.array(X)@M.T
scale=np.linalg.norm(M[0,:2]);az=np.degrees(np.arctan2(M[0,1],M[0,0]));elev=np.degrees(np.arcsin(np.linalg.norm(M[1,:2])/scale))
result={'affine':M.tolist(),'azimuth':az,'elevation':elev,'title_pixels_per_unit':scale,'matches':mapping,'pixel_rmse':float(np.sqrt(np.mean((pred-Y)**2)))}
(ROOT/'source/camera_calibration.json').write_text(json.dumps(result,indent=2))
print(result)
