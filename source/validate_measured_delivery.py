"""Reopen the saved linked and embedded checkpoint; validate delivery, not visual fidelity."""
import bpy,json,math,hashlib,array,ast
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1]
placements=json.loads((ROOT/'source/city_placements_measured.json').read_text())
expected={q['name']:q for q in placements};expected_ids={q['asset'] for q in placements}
report={'scope':'Saved geometry, dependencies, reference transforms and packed resources. This is not a fidelity approval.','scenes':{}}
for filename in ['city_measured.blend','city_measured_standalone.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/filename));s=bpy.context.scene
 objects={o.name:o for o in bpy.data.objects if o.get('library_asset')}
 assert objects.keys()==expected.keys(),('Unexpected instance list',filename)
 assets={o['library_asset']:o.instance_collection for o in objects.values()}
 assert assets.keys()==expected_ids
 for library in bpy.data.libraries:
  assert library.filepath.startswith('//') and Path(bpy.path.abspath(library.filepath)).is_file(),library.filepath
 fonts=[f for f in bpy.data.fonts if f.users and f.filepath!='<builtin>'];assert all(f.packed_file for f in fonts)
 geometry={};errors=[]
 for name,o in objects.items():
  q=expected[name];assert o.instance_collection and o.instance_collection['asset_id']==q['asset']
  assert 'reference_frame_anchor' in o.instance_collection,('Unmeasured instance',name)
  assert max(abs(x-1) for x in o.scale)<1e-6 and max(abs(x) for x in o.rotation_euler)<1e-6
  assert max(abs(o.location[i]-q['world_origin'][i]) for i in range(3))<1e-4
  assert all(math.isfinite(x) for row in o.matrix_world for x in row)
  pixel=world_to_camera_view(s,s.camera,o.matrix_world@__import__('mathutils').Vector(q['model_anchor']))
  err=math.dist((pixel.x*1280,(1-pixel.y)*720),q['reference_pixel']);errors.append(err);assert err<.003,(name,err)
 for id,c in assets.items():
  hashes=[];vertices=0
  for o in c.all_objects:
   if o.type!='MESH':continue
   m=o.data;v=array.array('f',[0])*(len(m.vertices)*3);m.vertices.foreach_get('co',v)
   loops=array.array('i',[0])*len(m.loops);m.loops.foreach_get('vertex_index',loops)
   transform=array.array('f',[x for row in o.matrix_world for x in row])
   hashes.append(hashlib.sha256(v.tobytes()+loops.tobytes()+transform.tobytes()).hexdigest());vertices+=len(m.vertices)
  assert hashes,(id,'Empty geometry')
  geometry[id]={'mesh_vertices':vertices,'mesh_hashes':sorted(hashes),'objects':len(c.all_objects)}
 if filename.endswith('_standalone.blend'):assert len(bpy.data.libraries)==0
 report['scenes'][filename]={'instances':len(objects),'unique_assets':len(assets),'external_libraries':len(bpy.data.libraries),'packed_fonts':len(fonts),'max_anchor_projection_error_pixels':max(errors),'geometry':geometry}
assert report['scenes']['city_measured.blend']['geometry']==report['scenes']['city_measured_standalone.blend']['geometry']
manifest=json.loads((ROOT/'asset_manifest_measured.json').read_text())
for item in manifest:
 for key in ['file','preview']:assert (ROOT/item[key]).is_file(),item[key]
 if item['id'] in expected_ids:assert item['version']=='fidelity-4-measured'
for p in (ROOT/'source').glob('*.py'):ast.parse(p.read_text(),filename=str(p))
report['library_assets']=len(manifest);report['result']='PASS: linked and portable geometry agree; references, unit transforms and packed fonts verified.'
(ROOT/'validation_measured.json').write_text(json.dumps(report,indent=2));print('MEASURED_DELIVERY_VALIDATED',report['result'],flush=True)
