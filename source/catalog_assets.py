import bpy,os,json,uuid,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
groups={
 'Title architecture':['title_towers'],
 'Principal campuses':['google','facebook','youtube','netscape','netscape_digg','twitter','apple','hooli'],
 'Branded offices':['ebay','intel','yahoo_oracle','hp','legacy_hp','myspace','energy_pod','adobe','linkedin','zynga','historic_apple','pets_com','paypal'],
 'District architecture':['west_solar','terrace_office','white_corner_office','framing_tower','security_tower','stadium','small_offices'],
 'Sculptures':['blue_sculpture'],
}
ids={g:str(uuid.uuid5(uuid.NAMESPACE_URL,'silicon-valley-fidelity/'+g)) for g in groups}
(ROOT/'assets/blender_assets.cats.txt').write_text('# Blender Asset Catalog Definition File\nVERSION 1\n\n'+'\n'.join(f'{ids[g]}:{g}:{g}' for g in groups)+'\n')
manifest=[]
audit=json.loads((ROOT/'source/asset_audit.json').read_text())
ledger=json.loads((ROOT/'source/matching_status.json').read_text())['assets']
for f in sorted((ROOT/'assets').glob('*/*.blend')):
 if f.stem!=f.parent.name:continue
 bpy.ops.wm.open_mainfile(filepath=str(f));col=next(c for c in bpy.data.collections if c.name.startswith('ASSET'))
 group=next((g for g,a in groups.items() if f.stem in a),'District architecture')
 if not col.asset_data:col.asset_mark()
 col.asset_data.catalog_id=ids[group];col.asset_data.author='Silicon Valley reconstruction project'
 measured='reference_frame_anchor' in col
 col['units']='Shared reference units, five source pixels per unit in the calibrated camera. Measured instances use unit scale; physical heights remain inferred.' if measured else 'Stylized relative units. Final scale is fitted per instance to the source image.'
 for tag in ('Silicon Valley','Architecture',group):
  if tag not in col.asset_data.tags:col.asset_data.tags.new(tag)
 preview=f.parent/'preview.png'
 if preview.exists():
  with bpy.context.temp_override(id=col):bpy.ops.ed.lib_id_load_custom_preview(filepath=str(preview))
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(f),compress=True)
 profile=audit.get(f.stem,{})
 if measured:
  q=ledger.get(f.stem,{})
  profile={'changes':[col.name.removeprefix('ASSET • ')],'camera':{'anchor':list(col['reference_frame_anchor']),'crop':list(col['reference_crop']),'scale':'unit scale in the shared reference coordinate system'},'remaining':q.get('unresolved',col.get('inferred_details','Unseen elevations are inferred.'))}
 manifest.append({'id':f.stem,'label':col.name.removeprefix('ASSET • '),'category':group,'file':str(f.relative_to(ROOT)),'preview':str(preview.relative_to(ROOT)),'references':col.get('references',''),'objects':len(col.all_objects),'mesh_vertices':sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH'),'version':col.get('version'),'changes':profile.get('changes',[]),'camera':profile.get('camera'),'notes':profile.get('remaining',col.get('inferred_details','Unseen elevations are inferred.'))})
(ROOT/('asset_manifest_measured.json' if '--measured-checkpoint' in sys.argv else 'asset_manifest.json')).write_text(json.dumps(manifest,indent=2))
print('CATALOG_READY',len(manifest),'assets',flush=True)
