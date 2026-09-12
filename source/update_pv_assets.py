"""Propagate the inspected PV surface to measured libraries and render fresh previews."""
import sys,json,bpy
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P));import asset_core as A
ROOT=P.parent;ledger=json.loads((P/'matching_status.json').read_text());report=[]
for id,q in sorted(ledger['assets'].items()):
 if q['status']!='rebuild_under_comparison':continue
 file=ROOT/'assets'/id/(id+'.blend');bpy.ops.wm.open_mainfile(filepath=str(file))
 col=next(c for c in bpy.data.collections if c.name.startswith('ASSET'));m=bpy.data.materials.get('solar')
 if not m or not any(o.type=='MESH' and m in list(o.data.materials) for o in col.all_objects):continue
 A.solar_surface(m);col['solar_surface_version']='reference-pv-2';s=bpy.context.scene
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
 for device in prefs.devices:device.use=device.type=='METAL'
 s.cycles.device='GPU';s.render.filepath=str(file.parent/'preview.png');s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.resolution_percentage=100
 bpy.ops.render.render(write_still=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(file),compress=True)
 report.append(id);print('PV_ASSET_UPDATED',id,flush=True)
(ROOT/'matching/pv_update_report.json').write_text(json.dumps({'surface':'reference-pv-2','assets':report},indent=2));print('PV_LIBRARY_UPDATED',len(report),flush=True)
