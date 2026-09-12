"""Embed copies of all modular assets for a self-contained Blender handoff."""
import bpy,os,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
measured='--measured-checkpoint' in sys.argv
bpy.ops.wm.open_mainfile(filepath=str(ROOT/('city_measured.blend' if measured else 'city.blend')))
instances=[o for o in bpy.data.objects if o.instance_type=='COLLECTION' and o.instance_collection and o.instance_collection.library]
asset_count=len({o.instance_collection.as_pointer() for o in instances})
# Localize the existing dependency graph so all shared collection instances
# retain their references, including nested meshes, materials and fonts.
bpy.ops.object.make_local(type='ALL')
bpy.ops.outliner.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
bpy.context.scene['editing']='All building collections are embedded in this file. The linked working scene and individual editable models are in the project archive.'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
print('LIBRARIES', [(l.name,l.users) for l in bpy.data.libraries],flush=True)
linked=[]
for prop in bpy.data.bl_rna.properties:
 if prop.type=='COLLECTION':
  for data in getattr(bpy.data,prop.identifier):
   if getattr(data,'library',None):linked.append((prop.identifier,data.name,data.library.name))
print('LINKED_DATA',linked,flush=True)
assert not linked,'Portable file retains linked data'
for library in list(bpy.data.libraries):bpy.data.libraries.remove(library)
assert len(bpy.data.libraries)==0,'Portable file retains external libraries'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/('city_measured_standalone.blend' if measured else 'city_standalone.blend')),compress=True)
print('PORTABLE_CITY',asset_count,'embedded asset collections',len(instances),'instances',flush=True)
