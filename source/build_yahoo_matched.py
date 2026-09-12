"""Yahoo and Oracle: separately measured four-floor corrugated office slabs."""
import os,sys,json,math
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
from reference_geometry import Reference,vector_art
from build_ebay_matched import inset
from mathutils import Vector
P=Path(__file__).parent

def build():
 D=json.load(open(P/'yahoo_oracle_measurements.json'));A.reset('yahoo_oracle','Yahoo and Oracle • measured four-storey office pair',['Original wide frame','YU26']);R=Reference(D['anchor'],D['crop'])
 for n,c,r in [('paired_roof',(.76,.71,.62),.88),('paired_band',(.40,.43,.41),.85),('paired_flute',(.44,.47,.44),.84),('paired_glass',(.32,.40,.40),.65),('paired_frame',(.29,.33,.32),.72),('yahoo_purple',(.43,.20,.41),.79),('yahoo_white',(.91,.88,.79),.86)]:A.material(n,c,r)
 # Soft irregular glass reflections break up the ribbon without adding fake window panes.
 m=A.MAT['paired_glass'];nodes=m.node_tree.nodes;links=m.node_tree.links;noise=nodes.new('ShaderNodeTexNoise');tc=nodes.new('ShaderNodeTexCoord');links.new(tc.outputs['Object'],noise.inputs['Vector']);noise.inputs['Scale'].default_value=.67;noise.inputs['Detail'].default_value=1.2;ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.2;ramp.color_ramp.elements[0].color=(.24,.34,.38,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(.53,.52,.42,1);links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],nodes.get('Principled BSDF').inputs['Base Color'])
 for block in D['volumes']:
  name=block['name'];H=block['height'];band=block['band'];p=R.plan(block['roof'],H);wall=inset(p,.18);A.part(name+' • measured glazed envelope');A.polygon('Four-storey glazing mass',wall,0,H-.25,'paired_glass')
  for a,b in zip(wall,wall[1:]+wall[:1]):
   a,b=Vector(a),Vector(b);v=b-a;L=v.length;t=v/L;n=Vector((t.y,-t.x));angle=math.atan2(v.y,v.x);mid=(a+b)/2+n*.09
   # Broad bands sit above each glazed floor, with actual raised narrow flutes.
   for k in range(1,5):
    z=k*H/4-band/2-.18;A.part(name+' • fluted horizontal floor bands');A.box('Continuous pale floor spandrel',(mid.x,mid.y,z),(L+.05,.18,band),'paired_band',angle)
    N=max(2,round(L/.20))
    for i in range(N):
     q=a.lerp(b,(i+.5)/N)+n*.192;A.box('Fine vertical flute on horizontal band',(q.x,q.y,z),(.065,.026,band-.04),'paired_band',angle)
   A.part(name+' • fine glazing divisions');N=max(2,round(L/.96))
   for i in range(N+1):
    q=a.lerp(b,i/N)+n*.065;A.box('Slender vertical window mullion',(q.x,q.y,H/2),(.028,.09,H),'paired_frame',angle)
  A.part(name+' • overhanging pale flat roof');A.polygon('Thin projecting roof slab',p,H-.20,.20,'paired_band');A.polygon('Warm roof membrane',p,H,.045,'paired_roof')
 # Circular stair joins the two independently oriented rectangular buildings.
 A.part('Shared round stair core');H=D['core_height'];q=R.p(D['core_center'],H);rad=D['core_radius'];A.cylinder('Round cream stair tower',(q.x,q.y,H/2),rad,H,'paired_band',128)
 for k in range(4):
  z=k*3.4+2.45;A.cylinder('Round core glass ribbon',(q.x,q.y,z),rad+.01,1.70,'paired_glass',128)
 for i in range(72):
  a=i*2*math.pi/72;x=q.x+(rad+.035)*math.cos(a);y=q.y+(rad+.035)*math.sin(a);A.rod('Fine stair curtain-wall division',(x,y,0),(x,y,H-.2),.018,'paired_frame',4)
 A.cylinder('Pale circular core roof',(q.x,q.y,H+.04),rad+.16,.11,'paired_roof',128)
 # Artwork follows independently observed coordinates on the Yahoo roof.
 z=D['volumes'][0]['height']+.13;A.part('Original Yahoo rooftop roundel');symbol=json.load(open(P/'yahoo_symbol_contours.json'))
 A.polygon('Measured tilted oval purple plaque',R.plan(symbol['roundel_outline'],z),z,.16,'yahoo_purple')
 A.polygon('Traced white serif Yahoo Y',R.plan(symbol['y_outline'],z+.17),z+.17,.035,'yahoo_white')
 A.polygon('Separate purple exclamation stem',R.plan([[897,34.9],[891.8,32.9],[916.9,22.9],[924.9,28.0]],z),z,.18,'yahoo_purple')
 A.polygon('Separate purple exclamation point',R.plan([[884.1,35.7],[889.9,33.5],[894.4,36.7],[888.7,39.3]],z),z,.18,'yahoo_purple')
 R.solar_racks(D['panels'],D['volumes'][1]['height']+.20,1.25,12,8,'oracle_rack_cells')
 A.COL['measurement_file']='source/yahoo_oracle_measurements.json';A.COL['inferred_details']='Far upper roof corners extend beyond the source image; ground floors are partly occluded by the title district. No Oracle plaque is visible on this version of the source facade.'
 A.setup_preview(47.134,26.377,1600,1200);R.camera(5);return A
if __name__=='__main__':build();A.save_asset('yahoo_oracle','--no-render' not in sys.argv)
