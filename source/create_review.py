# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,html,math
ROOT=Path(__file__).resolve().parents[1];Image.MAX_IMAGE_PIXELS=None
OUT=ROOT/'review_media';OUT.mkdir(exist_ok=True)
assets=json.loads((ROOT/'asset_manifest.json').read_text())
order=['title_towers','youtube','netscape','netscape_digg','google','facebook','apple','twitter','hooli','ebay','intel','yahoo_oracle','myspace','energy_pod','adobe','hp','legacy_hp','historic_apple','pets_com','paypal','linkedin','zynga','west_solar','white_corner_office','stadium','security_tower','framing_tower','terrace_office','small_offices','blue_sculpture']
assets.sort(key=lambda a:order.index(a['id']))
sources={
 'title_towers':('wide',(712,74,1095,326)),
 'youtube':('wide',(576,278,710,452)),'netscape':('YU20',None),'netscape_digg':('wide',(338,286,575,450)),
 'google':('wide',(0,448,730,720)),'facebook':('wide',(301,67,783,321)),
 'apple':('wide',(906,300,1206,460)),'twitter':('wide',(635,215,914,382)),
 'hooli':('wide',(1060,70,1280,271)),'ebay':('wide',(583,466,847,619)),'intel':('wide',(420,379,608,518)),
 'yahoo_oracle':('wide',(801,0,1073,144)),'myspace':('YU11',(0,.52,.51,1)),
 'energy_pod':('wide',(905,455,1112,656)),'adobe':('wide',(1096,322,1280,593)),
 'hp':('YU18',(.68,.23,1,.67)),'legacy_hp':('wide',(0,567,243,720)),
 'historic_apple':('YU09',(.20,.21,.48,.66)),'pets_com':('wide',(276,290,396,393)),
 'paypal':('wide',(50,270,236,379)),'linkedin':('wide',(0,327,164,436)),
 'zynga':('wide',(746,585,967,720)),'west_solar':('wide',(157,364,327,481)),
 'white_corner_office':('wide',(0,151,168,313)),'stadium':('wide',(0,0,151,165)),
 'security_tower':('wide',(238,53,359,204)),'framing_tower':('wide',(121,0,265,178)),
 'terrace_office':('wide',(1090,541,1280,702)),'small_offices':('YU09',(.027,.30,.25,.57)),
 'blue_sculpture':('YU11',(.45,.72,.60,.89)),
}
def white_image(path):
 with Image.open(path) as src:
  src.draft('RGB',(2400,1800));im=src.convert('RGBA')
 out=Image.new('RGBA',im.size,'white');out.alpha_composite(im);return out.convert('RGB')
def trim(im,bg='white'):
 diff=ImageChops.difference(im,Image.new('RGB',im.size,bg)).convert('L').point(lambda x:255 if x>24 else 0)
 b=diff.getbbox()
 if b:
  x0,y0,x1,y1=b;pad=max(4,int(max(x1-x0,y1-y0)*.025));im=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
 return im
def contain(im,size,bg='white'):
 out=Image.new('RGB',size,bg);im=im.copy();im.thumbnail((size[0]-24,size[1]-24),Image.Resampling.LANCZOS);out.paste(im,((size[0]-im.width)//2,(size[1]-im.height)//2));return out
models={}
for a in assets:
 id=a['id'];model=trim(white_image(ROOT/a['preview']));models[id]=model
 contain(model,(1100,800)).save(OUT/(id+'_model.jpg'),quality=93)
 key,crop=sources[id]
 path=ROOT/'references/original_wide.webp' if key=='wide' else next((ROOT/'references/studio').glob(key+'_*'))
 with Image.open(path) as f:
  f.draft('RGB',(2400,1800));ref=f.convert('RGB')
 if crop:
  if max(crop)<=1:crop=tuple(int(v*(ref.width if i%2==0 else ref.height)) for i,v in enumerate(crop))
  ref=ref.crop(crop)
 elif key in ('YU20','YU24','YU25','YU26','YU27'):ref=trim(ref,'black')
 ref.thumbnail((1600,1100),Image.Resampling.LANCZOS);ref.save(OUT/(id+'_source.jpg'),quality=94)
 before=trim(white_image(ROOT/'comparisons/v2'/f'{id}.png'))
 contain(before,(1100,800)).save(OUT/(id+'_previous.jpg'),quality=90)
 a['review_previous']='review_media/'+id+'_previous.jpg'
 a['source_key']=key;a['review_model']='review_media/'+id+'_model.jpg';a['review_source']='review_media/'+id+'_source.jpg'

font_root=Path('/System/Library/Fonts/Supplemental')
def font(size,bold=False):return ImageFont.truetype(str(font_root/('Arial Bold.ttf' if bold else 'Arial.ttf')),size)
labels={'title_towers':'SILICON VALLEY towers','netscape_digg':'Digg pavilion • original variant','netscape':'Netscape / Android','youtube':'YouTube','google':'Google campus','facebook':'Facebook campus','yahoo_oracle':'Yahoo / Oracle','historic_apple':'Historic Apple / Pets.com','pets_com':'Pets.com • original variant','legacy_hp':'Hewlett Packard','energy_pod':'EnergyPod tower','white_corner_office':'Western pale office','terrace_office':'Terraced office module'}
def board(ids,cols,cellw,cellh,title,subtitle):
 rows=math.ceil(len(ids)/cols);im=Image.new('RGB',(cols*cellw+64,rows*cellh+166),(244,243,239));d=ImageDraw.Draw(im)
 d.text((35,30),title,font=font(36,True),fill=(29,33,35));d.text((36,85),subtitle,font=font(18),fill=(92,94,94))
 for i,id in enumerate(ids):
  x=32+(i%cols)*cellw;y=134+(i//cols)*cellh
  d.rounded_rectangle((x+5,y+5,x+cellw-5,y+cellh-6),radius=10,fill='white')
  thumb=contain(models[id],(cellw-30,cellh-64));im.paste(thumb,(x+15,y+10))
  label=labels.get(id,id.replace('_',' ').title());d.text((x+17,y+cellh-43),label,font=font(17,True),fill=(37,42,44))
 return im
board(order,5,400,320,'SILICON VALLEY / BUILDING LIBRARY','30 editable Blender assets • original production references • separate architectural parts').save(ROOT/'renders/building_library.jpg',quality=94)
board(['title_towers','youtube','netscape','google','facebook','myspace'],3,600,455,'MODELING THE CITY, ONE BUILDING AT A TIME','Individual asset renders from the modular reconstruction').save(ROOT/'renders/building_closeups.jpg',quality=95)

cards=[]
for a in assets:
 id=a['id'];title=labels.get(id,a['label']);e=html.escape
 cards.append(f'''<details class="asset" data-category="{e(a['category'])}" data-search="{e((title+' '+id+' '+a['category']).lower())}" id="{id}">
 <summary><img loading="lazy" src="{a['review_model']}" alt="Blender model of {e(title)}"><div><b>{e(title)}</b><span>{e(a['category'])}</span></div></summary>
 <div class="expanded"><div class="comparison"><figure><img loading="lazy" src="{a['review_source']}" alt="Production reference for {e(title)}"><figcaption>Source · {e(a['source_key'])}</figcaption></figure><figure><img loading="lazy" src="{a['review_model']}" alt="Modeled {e(title)}"><figcaption>Blender reconstruction</figcaption></figure></div>
 <div class="revision"><b>Rebuilt in this pass</b><ul>{''.join('<li>'+e(v)+'</li>' for v in a.get('changes',[]))}</ul><p class="muted">Camera: {a.get('camera',[0,0])[0]:.1f}° azimuth / {a.get('camera',[0,0])[1]:.1f}° elevation. References: {e(a['references'])}.</p><p class="muted">Still approximate: {e(a['notes'])}</p></div><details class="previous"><summary>Compare with the previous model</summary><img loading="lazy" src="{a['review_previous']}" alt="Previous version of {e(title)}"><p class="muted">Revision 2 — before this rebuild</p></details><p><a class="button" href="{a['file']}" download>Open building file ↓</a> <a href="{a['preview']}">Full render</a></p></div></details>''')
categories=sorted({a['category'] for a in assets})
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Silicon Valley — building library</title>
<style>
:root{font-family:Arial,Helvetica,sans-serif;color:#222b30;background:#f3f2ee;font-size:16px}*{box-sizing:border-box}body{margin:0}a{color:#b54530;text-underline-offset:4px}header,main,footer{max-width:1420px;margin:auto;padding:36px 38px}header{padding-bottom:24px;border-bottom:1px solid #d8d8d0}nav{display:flex;gap:24px;font-size:14px;margin-top:25px}h1{font-size:clamp(30px,4.2vw,60px);letter-spacing:-2px;line-height:1.02;margin:12px 0 20px;max-width:1000px}h2{font-size:29px;letter-spacing:-.6px;margin:32px 0 15px}p{line-height:1.6;max-width:1000px}.eyebrow{color:#a04a35;font-size:12px;letter-spacing:2px;font-weight:700}.muted{color:#657077;font-size:14px}.count{display:inline-block;background:#fff;border:1px solid #dedfd9;border-radius:20px;padding:7px 12px;margin-right:7px;font-size:12px}.wipe{position:relative;aspect-ratio:16/9;overflow:hidden;background:#d9dedb;border-radius:10px}.wipe img{position:absolute;width:100%;height:100%;object-fit:cover}.wipe .original{clip-path:inset(0 50% 0 0)}.divider{position:absolute;left:50%;top:0;height:100%;width:2px;background:white;box-shadow:0 0 4px #333}.pill{position:absolute;top:14px;padding:7px 10px;border-radius:4px;background:#fffE;font-size:12px;z-index:2}.pill.left{left:14px}.pill.right{right:14px}.slider{display:flex;align-items:center;gap:15px;font-size:13px;padding:12px 0}input[type=range]{width:100%;accent-color:#c85337}.toolbar{display:flex;gap:12px;margin:22px 0}input[type=search],select{border:1px solid #cbd0cf;border-radius:6px;padding:13px;background:white;font-size:15px}input[type=search]{flex:1;min-width:100px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.asset{background:white;border:1px solid #dfe2df;border-radius:9px;overflow:hidden}.asset summary{list-style:none;cursor:pointer}.asset summary::-webkit-details-marker{display:none}.asset summary img{width:100%;height:245px;object-fit:contain}.asset summary div{padding:14px 18px 19px}.asset summary span{display:block;color:#788082;font-size:12px;margin-top:7px}.asset[open]{grid-column:1/-1}.asset[open] summary img{display:none}.asset[open] summary div{padding-bottom:10px}.asset[open] summary b:after{content:' −';color:#b54530}.expanded{padding:0 20px 18px}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:16px}.comparison figure{margin:0;border:1px solid #e7e8e4}.comparison img{width:100%;height:430px;object-fit:contain}.comparison figcaption{padding:10px 14px;font-size:12px;border-top:1px solid #e7e8e4;color:#637077}.expanded p{font-size:14px}.button{display:inline-block;padding:10px 15px;background:#263238;color:white;border-radius:5px;text-decoration:none;margin-right:14px}.asset[hidden]{display:none}.revision{background:#f6f5f0;padding:17px 22px;margin-top:18px;border-radius:5px}.revision li{font-size:14px;line-height:1.6}.previous{margin:20px 0}.previous summary{color:#a04a35;padding:12px 0;cursor:pointer}.previous img{width:100%;max-height:460px;object-fit:contain}.featured{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.featured figure{margin:0;background:white;padding:10px;border:1px solid #dfe2df}.featured img{width:100%;height:280px;object-fit:contain}.featured figcaption{font-size:13px;color:#627078;padding:8px}.look-controls{display:flex;gap:8px;flex-wrap:wrap}.look-controls button{border:1px solid #c8cdca;background:white;padding:9px 13px;border-radius:5px;cursor:pointer}.look-controls button.active{background:#283a3f;color:white}.study{width:100%;border-radius:8px;margin:12px 0}.videos{display:grid;grid-template-columns:1fr 1fr;gap:20px}video{width:100%;border-radius:8px;background:#111}.notice{border-left:3px solid #c46742;padding-left:15px;color:#596367;font-size:14px}.downloads{display:flex;gap:18px;flex-wrap:wrap;margin:15px 0}footer{font-size:13px;color:#66716f;border-top:1px solid #d8d8d0}@media(max-width:850px){header,main,footer{padding:24px 18px}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.comparison{grid-template-columns:1fr}.featured{grid-template-columns:1fr}.featured img{height:250px}.comparison img{height:340px}.videos{grid-template-columns:1fr}.asset summary img{height:190px}}@media(max-width:530px){.grid{grid-template-columns:1fr}.toolbar{flex-direction:column}h1{letter-spacing:-1px}.asset summary img{height:235px}}
</style>
<header><div class="eyebrow">REVISION 3 / ARCHITECTURE + MORNING LIGHT</div><h1>Silicon Valley.<br>A city built from individual models.</h1><p>A rebuild of the individual buildings, with corrected proportions, roof details, materials and directional morning light. Inspect the changes against the original and the previous model.</p><span class="count">30 reusable assets</span><span class="count">45 city instances</span><span class="count">30 studio images</span><nav><a href="#assembly">Compare the city</a><a href="#library">Inspect the buildings</a><a href="#references">Watch the references</a></nav></header>
<main><section id="benchmark"><h2>The building that prompted the rebuild</h2><p class="muted">Corrected camera direction, solid masonry, an interrupted panel layout, a lower stepped entrance and the annex on the proper side.</p><div class="featured"><figure><img src="review_media/west_solar_source.jpg" alt="Original western office"><figcaption>Original production image</figcaption></figure><figure><img src="review_media/west_solar_previous.jpg" alt="Previous western office"><figcaption>Previous model · revision 2</figcaption></figure><figure><img src="review_media/west_solar_model.jpg" alt="Rebuilt western office"><figcaption>Rebuilt model · revision 3</figcaption></figure></div></section><section id="assembly"><h2>Source / reconstruction</h2><p class="muted">Drag the divider to compare the original wide frame and the Blender reference camera.</p><div class="wipe"><img src="renders/city_reference.png" alt="Blender city reconstruction"><img class="original" id="original" src="references/original_wide.webp" alt="Original Silicon Valley intro frame"><div class="divider" id="divider"></div><span class="pill left">Original opening</span><span class="pill right">Blender model</span></div><label class="slider">Blender<input id="wipe" type="range" min="0" max="100" value="50" aria-label="Source comparison">Source</label><p class="notice">Geometry is compared with the director’s original wide image. The lighting uses the warmer directional light seen in the moving sequence. This is still an approximation: campus footprints, some lettering and hidden elevations retain visible differences. Every building below records its changes and remaining uncertainty.</p><div class="downloads"><a href="city_standalone.blend" download>Self-contained Blender city ↓</a><a href="renders/city_reference.png">4K render</a><a href="BUILDING_INVENTORY.md">Fidelity notes</a><a href="README.md">Editing instructions</a></div></section>
<section id="lighting"><h2>Morning light and cast shadows</h2><p class="muted">The same geometry under the editable Blender sun rig. The main render uses the middle setting; the low sun casts longer shadows.</p><div class="look-controls"><button data-light="renders/morning_early.jpg">Low sun · 20°</button><button class="active" data-light="renders/morning_match.jpg">Main render · 32°</button><button data-light="renders/morning_late.jpg">Higher sun · 46°</button></div><img class="study" id="morning" src="renders/morning_match.jpg" alt="Morning lighting study of the reconstructed city"></section><section id="library"><h2>Building library</h2><p class="muted">Open a card for its source image, model render and individual Blender file. Architectural parts remain editable within each asset.</p><div class="toolbar"><input id="search" type="search" placeholder="Find a building…" aria-label="Find a building"><select id="category" aria-label="Asset category"><option value="">All categories</option>'''+''.join('<option>'+html.escape(x)+'</option>' for x in categories)+'''</select></div><p class="muted" id="shown">30 assets</p><div class="grid">'''+''.join(cards)+'''</div></section>
<section id="references"><h2>Production references</h2><p><a href="https://www.yuco.com/works/silicon-valley">yU+co project page</a> · <a href="https://www.youtube.com/watch?v=DNp1ullIXP4">HBO original opening</a> · <a href="references/studio_manifest.json">Image source manifest</a></p><div class="videos"><div><video controls preload="metadata" src="references/season1_intro.mp4"></video><p class="muted">Original opening</p></div><div><video controls preload="metadata" src="references/behind_the_scenes.mp4"></video><p class="muted">Production behind the scenes</p></div></div><p class="muted">The 12K title-building still supplies the traced roof outlines. Later images provide close-up architectural evidence; the library keeps several signage variants separate.</p></section></main><footer>Reference imagery: HBO / yU+co. Reconstruction geometry and assembly are contained in the project. Source artwork credits: <a href="references/logos/SOURCES.md">vector sources</a>.</footer>
<script>
document.querySelectorAll('[data-light]').forEach(b=>b.addEventListener('click',()=>{document.getElementById('morning').src=b.dataset.light;document.querySelectorAll('[data-light]').forEach(x=>x.classList.toggle('active',x===b))}));
const range=document.getElementById('wipe');range.addEventListener('input',()=>{document.getElementById('original').style.clipPath=`inset(0 ${100-range.value}% 0 0)`;document.getElementById('divider').style.left=range.value+'%'});
const search=document.getElementById('search'),category=document.getElementById('category'),cards=[...document.querySelectorAll('.asset')];function filter(){let n=0;cards.forEach(card=>{const show=card.dataset.search.includes(search.value.toLowerCase())&&(!category.value||card.dataset.category===category.value);card.hidden=!show;if(show)n++});document.getElementById('shown').textContent=n+(n===1?' asset':' assets')}search.addEventListener('input',filter);category.addEventListener('change',filter);
</script></html>'''
(ROOT/'review.html').write_text(page)
(ROOT/'review_manifest.json').write_text(json.dumps(assets,indent=2))
print('REVIEW_READY',len(assets),'assets')
