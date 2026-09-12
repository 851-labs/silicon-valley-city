"""Create a clean local handoff archive after validate_delivery.py passes."""
import json,zipfile
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlparse
ROOT=Path(__file__).resolve().parents[1]
assert json.loads((ROOT/'validation.json').read_text())['result'].startswith('PASS')
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ('src','href') or not value or value.startswith('#'):continue
   if urlparse(value).scheme:continue
   assert (ROOT/unquote(value.split('#')[0])).is_file(),value
Links().feed((ROOT/'review.html').read_text())
top={'city.blend','city_standalone.blend','README.md','BUILDING_INVENTORY.md','review.html','asset_manifest.json','review_manifest.json','validation.json'}
renders={'city_reference.png','eastern_detail.png','building_library.jpg','building_closeups.jpg','morning_early.jpg','morning_match.jpg','morning_late.jpg','western_office_comparison.jpg'}
files=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(ROOT)
 if '__pycache__' in rel.parts or p.name.startswith('.') or p.suffix=='.blend1':continue
 if (len(rel.parts)==1 and p.name in top or rel.parts[0] in ('assets','references','review_media') or rel.parts[:2]==('comparisons','v2') or rel.parts[0]=='source' and p.suffix in ('.py','.json') and p.name not in ('color_study.py','study_city_v3.py','palette_study.py','finish_v3.py') or rel.parts[0]=='renders' and p.name in renders):files.append(p)
out=ROOT.parent/'silicon_valley_fidelity_v3.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for p in files:archive.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(out) as archive:
 assert archive.testzip() is None
 assert len([n for n in archive.namelist() if '/assets/' in n and n.endswith('.blend')])==30
print('PACKAGE_READY',out,len(files),'files',round(out.stat().st_size/1024**2,1),'MiB')
