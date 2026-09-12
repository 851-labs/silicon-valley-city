from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FONT=Path('/System/Library/Fonts/Supplemental')
def font(n,bold=False):return ImageFont.truetype(str(FONT/('Arial Bold.ttf' if bold else 'Arial.ttf')),n)
def composite(p):
 im=Image.open(p).convert('RGBA');out=Image.new('RGBA',im.size,'white');out.alpha_composite(im);return out.convert('RGB')
def contain(im,w,h):
 im=im.copy();im.thumbnail((w,h),Image.Resampling.LANCZOS);out=Image.new('RGB',(w,h),'white');out.paste(im,((w-im.width)//2,(h-im.height)//2));return out
source=Image.open(ROOT/'references/original_wide.webp').convert('RGB').crop((157,364,327,481));source=source.resize((680,468),Image.Resampling.LANCZOS)
imgs=[source,composite(ROOT/'comparisons/v2/west_solar.png'),composite(ROOT/'assets/west_solar/preview.png')]
board=Image.new('RGB',(2000,765),'#f1f0eb');d=ImageDraw.Draw(board)
d.text((36,30),'WESTERN SOLAR OFFICE — REBUILD COMPARISON',font=font(30,True),fill='#233038')
d.text((36,77),'Roof layout, masonry, entrance massing, annex position and camera direction',font=font(20),fill='#606c70')
for i,(im,title) in enumerate(zip(imgs,['Original production image','Previous model · revision 2','Rebuilt model · revision 3'])):
 x=25+i*655;d.rectangle((x,125,x+640,710),fill='white');board.paste(contain(im,622,515),(x+9,136));d.text((x+17,667),title,font=font(22,True),fill='#31424a')
d.text((36,732),'Reference: HBO / yU+co · geometry remains editable in Blender',font=font(15),fill='#606c70')
board.save(ROOT/'renders/western_office_comparison.jpg',quality=96)
print('BENCHMARK_READY')
