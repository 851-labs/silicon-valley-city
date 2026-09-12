"""Exact-crop diagnostic boards. Never trim or rescale either side independently."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
from review_fonts import review_font
R=Path(__file__).resolve().parents[1];out=R/'matching'
out.mkdir(exist_ok=True)
ref=Image.open(R/'references/original_wide.webp').convert('RGB')
font=review_font(20)
for file in sorted((R/'source').glob('*_measurements.json')):
 id=file.stem.removesuffix('_measurements')
 d=json.loads(file.read_text())
 if 'crop' not in d:continue
 crop=d['crop'];model=Image.open(R/'assets'/id/'preview.png').convert('RGBA');
 if abs(model.width/model.height-(crop[2]-crop[0])/(crop[3]-crop[1]))>.005:
  print('SKIP_STALE_PREVIEW',id);continue
 source=ref.crop(crop).resize(model.size,Image.Resampling.NEAREST)
 white=Image.new('RGBA',model.size,'#dad7cd');white.alpha_composite(model);white=white.convert('RGB')
 overlay=source.copy().convert('RGBA');layer=model.copy();layer.putalpha(model.getchannel('A').point(lambda a:round(a*.5)));overlay.alpha_composite(layer)
 # Outline diagnostic uses the model's visible silhouette, not a claim of agreement.
 from PIL import ImageFilter,ImageChops
 alpha=model.getchannel('A').point(lambda a:255 if a>128 else 0);edge=ImageChops.subtract(alpha.filter(ImageFilter.MaxFilter(5)),alpha.filter(ImageFilter.MinFilter(5)))
 outline=source.copy().convert('RGBA');red=Image.new('RGBA',model.size,(250,45,30,255));red.putalpha(edge);outline.alpha_composite(red)
 for name,im in [('source',source),('model',white),('overlay',overlay),('outline',outline)]:im.convert('RGB').save(out/f'{id}_{name}_matched.jpg',quality=95)
 w=min(model.width,1300);h=round(model.height*w/model.width)
 board=Image.new('RGB',(w*2,h*2+84),'#f3f1ea');draw=ImageDraw.Draw(board)
 for i,(name,im) in enumerate([('SOURCE',source),('BLENDER — SAME CAMERA AND CROP',white),('50% MODEL OVERLAY',overlay),('MODEL OUTLINE ON SOURCE',outline)]):
  x=(i%2)*w;y=(i//2)*(h+42);draw.text((x+12,y+10),name,font=font,fill='#303330');board.paste(im.resize((w,h)).convert('RGB'),(x,y+42))
 board.save(out/f'{id}_comparison.jpg',quality=94)
print('MATCH_BOARDS_READY')
