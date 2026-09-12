"""Recover discrete PV panel groups from the reference roof, with a review overlay."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,cv2,json,math
R=Path(__file__).resolve().parents[1];im=np.array(Image.open(R/'references/original_wide.webp').convert('RGB'))
roof=np.array([[594,528],[631,466],[713,482],[836,529],[734,574]],np.int32)
mask=np.zeros(im.shape[:2],np.uint8);cv2.fillPoly(mask,[roof],255)
mask=cv2.erode(mask,np.ones((5,5),np.uint8))
blur=im.astype(np.float32)
r,g,b=[blur[:,:,i] for i in range(3)];panels=((abs(b-r)<28)&(abs(g-r)<22)&(r<181)&(b>55)&(mask>0)).astype(np.uint8)*255
panels=cv2.morphologyEx(panels,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
contours,_=cv2.findContours(panels,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# Inverse affine camera transform makes panel axes orthogonal in plan.
az=math.radians(47.134259);el=math.radians(26.377115);M=np.array([[math.cos(az)/5,math.sin(az)/(5*math.sin(el))],[math.sin(az)/5,-math.cos(az)/(5*math.sin(el))]])
inv=np.linalg.inv(M);out=[]
for c in contours:
 area=cv2.contourArea(c)
 if not 9<area<240:continue
 p=c[:,0,:].astype(np.float32);world=p@M.T
 rect=cv2.minAreaRect(world.astype(np.float32));w,h=rect[1]
 if min(w,h)<.45 or max(w,h)>7:continue
 box=cv2.boxPoints(rect)@inv.T
 out.append({'area_px':area,'corners':box.round(2).tolist()})
out.sort(key=lambda p:(min(q[1] for q in p['corners']),min(q[0] for q in p['corners'])))
a=Image.fromarray(im).crop((580,455,850,583)).resize((1350,640));d=ImageDraw.Draw(a)
for i,p in enumerate(out):
 q=[((x-580)*5,(y-455)*5) for x,y in p['corners']];d.line(q+[q[0]],fill='#ee3344',width=2);d.text(q[0],str(i),fill='#ff3333')
a.save(R/'matching/ebay_panel_detection.jpg',quality=96)
(R/'source/ebay_panel_detections.json').write_text(json.dumps({'reference':'original_wide.webp','method':'Colour segmentation; planar minimum-area rectangles. All detections require visual review.','panels':out},indent=2))
print('PANEL_CANDIDATES',len(out))
