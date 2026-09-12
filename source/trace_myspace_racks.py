"""Separate the nine raised panel faces from their dark roof shadows.

Manual edge observations in original_wide.webp; YU11 confirms the section.
The previous threshold-mask fit merged surfaces and shadows and is retained
only as a diagnostic, not used as the final rack layout.
"""
from pathlib import Path
import json, math
from PIL import Image, ImageDraw

R=Path(__file__).resolve().parents[1]
p=R/'source/myspace_measurements.json';d=json.loads(p.read_text())
front=[826.0,453.0];a=[8.0,-9.0];b=[18.0,8.0]
g1=[18.0,-7.8];g2=[20.0,9.1]
fields=[]
for i in range(3):
 for j in range(3):
  q=[front[k]+i*g1[k]+j*g2[k] for k in range(2)]
  fields.append([q,[q[k]+a[k] for k in range(2)],
                 [q[k]+a[k]+b[k] for k in range(2)],
                 [q[k]+b[k] for k in range(2)]])
el=math.radians(json.loads((R/'source/camera_calibration.json').read_text())['elevation'])
d['solar_fields']=fields
d['solar_rack_rise']=(a[0]*g1[1]/g1[0]-a[1])/(5*math.cos(el))
d['solar_fields_method']='Raised panel-face edges manually traced separately from shadows; repeated 3 by 3 source grid. Rise derived by aligning the inclined side with the roof-grid direction. Individual edges remain under visual comparison.'
d['solar_rack_observations']={'front_low_corner':front,'inclined_side':a,'long_side':b,'roof_grid_vectors':[g1,g2],'source':'original_wide.webp; continuous rack section confirmed by YU11'}
p.write_text(json.dumps(d,indent=2)+'\n')
im=Image.open(R/'references/original_wide.webp').convert('RGB');dr=ImageDraw.Draw(im)
for q in fields:dr.line([tuple(v) for v in q+[q[0]]],fill=(255,35,25),width=1)
im.crop((805,425,940,490)).resize((1080,520),Image.Resampling.NEAREST).save(R/'matching/myspace_rack_edges_traced.png')
print('RACK_FACE_EDGES_TRACED',d['solar_rack_rise'])
