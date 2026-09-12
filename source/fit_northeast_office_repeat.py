"""Locate a repeated source roof, including its off-frame part. Not a model-fidelity score."""
from pathlib import Path
import json,cv2,numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];d=json.loads((ROOT/'source/north_solar_office_measurements.json').read_text())
im=np.array(Image.open(ROOT/'references/original_wide.webp').convert('RGB'));gray=cv2.cvtColor(im,cv2.COLOR_RGB2GRAY).astype(float)
mask=np.zeros(gray.shape,np.uint8);cv2.fillPoly(mask,[np.array(d['roof'],np.int32)],1);mask=cv2.erode(mask,np.ones((3,3),np.uint8));yy,xx=np.where(mask);a=d['anchor'];rows=[]
for y in range(103,127):
 for x in range(1260,1296):
  dx=x-a[0];dy=y-a[1];tx=xx+dx;ty=yy+dy;valid=(tx>=0)&(tx<1280)&(ty>=0)&(ty<720)
  if valid.mean()<.35:continue
  p=gray[yy[valid],xx[valid]];q=gray[ty[valid],tx[valid]];score=float(np.corrcoef(p,q)[0,1]);rows.append({'anchor':[x,y],'score':score,'coverage':float(valid.mean())})
rows.sort(key=lambda q:-q['score']);(ROOT/'source/northeast_office_repeat_fit.json').write_text(json.dumps({'method':'Source-to-source normalized grey correlation inside the northern module roof outline. This locates a repeated source roof; it does not compare Blender geometry.','candidates':rows[:12]},indent=2))
best=rows[0];out=Image.fromarray(im);draw=ImageDraw.Draw(out);delta=np.array(best['anchor'])-np.array(a[:2]);points=(np.array(d['roof'])+delta).tolist();draw.line([tuple(q) for q in points+[points[0]]],fill=(255,45,25),width=1);out.crop((1190,60,1280,150)).resize((720,720),Image.Resampling.NEAREST).save(ROOT/'matching/northeast_office_repeat_fit.png')
print('SOURCE_ROOF_CANDIDATES',json.dumps(rows[:5]))
