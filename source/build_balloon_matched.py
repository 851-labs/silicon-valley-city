"""Measured collapsed balloon cloth: actual folded mesh with separate blue and white fabric."""
import os,sys,json
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference
P=Path(__file__).parent
def build():
 D=json.load(open(P/'blue_sculpture_measurements.json'));M=json.load(open(P/'balloon_fold_mesh.json'));A.reset('blue_sculpture','Collapsed balloon • measured cloth crests and white fabric patches',['Original wide frame','YU11']);R=Reference(D['anchor'],D['crop'])
 A.material('balloon_blue',(.075,.081,.31),.65);A.material('balloon_white',(.75,.72,.67),.79);A.part('Sculpted collapsed fabric shell');vs=[tuple(R.p((x,y),z)) for x,y,z in M['vertices']]
 faces=[tuple(reversed(f)) for f in M['faces']['blue']+M['faces']['white']];ob=A.mesh('Continuous blue and white folded balloon fabric',vs,faces,'balloon_blue',False,True);ob.data.materials.append(A.MAT['balloon_white'])
 for poly in list(ob.data.polygons)[len(M['faces']['blue']):]:poly.material_index=1
 sub=ob.modifiers.new('Smooth cloth curvature','SUBSURF');sub.levels=1;sub.render_levels=1;solid=ob.modifiers.new('Thin double-sided balloon skin','SOLIDIFY');solid.thickness=.025
 A.COL['measurement_file']='source/blue_sculpture_measurements.json';A.COL['inferred_details']='Cloth hidden by trees and roof edges is inferred. Visible crests, outer limits and white markings are measured against the original and studio close-up.'
 A.setup_preview(47.134,26.377,1200,800);R.camera(12);return A
if __name__=='__main__':build();A.save_asset('blue_sculpture')
