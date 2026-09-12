"""Reopen both delivery scenes and verify their actual saved dependencies."""
import bpy, json, math, ast
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
report={'blender_version':bpy.app.version_string,'scenes':{}}
for filename in ('city.blend','city_standalone.blend'):
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/filename))
 instances=[o for o in bpy.data.objects if o.get('library_asset')]
 assert len(instances)==45,(filename,len(instances))
 assert all(o.instance_collection and len(o.instance_collection.all_objects)>0 for o in instances)
 for library in bpy.data.libraries:
  assert library.filepath.startswith('//'),library.filepath
  assert Path(bpy.path.abspath(library.filepath)).is_file(),library.filepath
 fonts=[f for f in bpy.data.fonts if f.filepath!='<builtin>' and f.users]
 assert all(f.packed_file for f in fonts),'Unpacked font'
 assert all(math.isfinite(v) for o in instances for row in o.matrix_world for v in row)
 assets={o['library_asset']:o.instance_collection for o in instances}
 geometry={id:{'objects':len(c.all_objects),'mesh_vertices':sum(len(o.data.vertices) for o in c.all_objects if o.type=='MESH')} for id,c in sorted(assets.items())}
 transforms={o.name:[list(row) for row in o.matrix_world] for o in instances}
 report['scenes'][filename]={'instances':len(instances),'unique_assets':len(assets),'external_libraries':len(bpy.data.libraries),'packed_fonts':len(fonts),'geometry':geometry,'transforms':transforms,'camera':bpy.context.scene.camera.name}
 assert len(assets)==27
 if filename=='city_standalone.blend':assert len(bpy.data.libraries)==0
assert report['scenes']['city.blend']['geometry']==report['scenes']['city_standalone.blend']['geometry']
assert report['scenes']['city.blend']['transforms']==report['scenes']['city_standalone.blend']['transforms']
manifest=json.loads((ROOT/'asset_manifest.json').read_text())
assert len(manifest)==30
for item in manifest:
 assert item.get('version')=='fidelity-3',(item['id'],item.get('version'))
 assert item.get('changes') and item.get('camera'),item['id']
 for key in ('file','preview'):assert (ROOT/item[key]).is_file(),item[key]
for p in (ROOT/'source').glob('*.py'):ast.parse(p.read_text(),filename=str(p))
report['asset_files']=len(manifest)
report['result']='PASS: linked and embedded building geometry agree; all referenced files and packed fonts verified.'
(ROOT/'validation.json').write_text(json.dumps(report,indent=2))
print('DELIVERY_VALIDATED',report['result'],flush=True)
