"""Render the editable intro to a restartable PNG sequence in background Blender."""
from pathlib import Path
import argparse,hashlib,json,struct,sys,time
import bpy
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
from blender_runtime import configure_cycles
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--frames',help='Comma-separated frame numbers; default is the complete shot')
p.add_argument('--width',type=int,default=1920);p.add_argument('--samples',type=int,default=16)
p.add_argument('--output',default='animation/frames');p.add_argument('--resume',action='store_true')
a=p.parse_args(args);scene_file=ROOT/'animation/intro.blend';bpy.ops.wm.open_mainfile(filepath=str(scene_file));s=bpy.context.scene
s.render.engine='CYCLES';device=configure_cycles(s);s.cycles.samples=a.samples;s.cycles.use_denoising=True;s.cycles.adaptive_min_samples=4;s.cycles.adaptive_threshold=.07;s.render.use_persistent_data=True;s.render.resolution_x=a.width;s.render.resolution_y=round(a.width*9/16);s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15
frames=[int(v) for v in a.frames.split(',')] if a.frames else list(range(s.frame_start,s.frame_end+1))
output=ROOT/a.output;output.mkdir(parents=True,exist_ok=True)
spec={'scene_sha256':hashlib.sha256(scene_file.read_bytes()).hexdigest(),'width':s.render.resolution_x,'height':s.render.resolution_y,'samples':a.samples,'frames':frames,'fps':s.render.fps/s.render.fps_base,'device':device}
manifest=output/'render_manifest.json'
if a.resume and manifest.exists():
 old=json.loads(manifest.read_text())
 for name in ['scene_sha256','width','height','samples','frames']:assert old[name]==spec[name],f'Resume settings differ: {name}'
manifest.write_text(json.dumps(spec,indent=2)+'\n')
started=time.monotonic()
def complete_png(path):
 if not path.is_file() or path.stat().st_size<36:return False
 with path.open('rb') as stream:
  header=stream.read(24);stream.seek(-12,2);ending=stream.read()
 return header[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',header[16:24])==(spec['width'],spec['height']) and ending==b'\x00\x00\x00\x00IEND\xaeB\x60\x82'
# Inspect the balloon, construction and held title first while the rest renders.
priority=[73,145,192]
queue=[f for f in priority if f in frames]+[f for f in frames if f not in priority]
for f in queue:
 target=output/f'frame_{f:04d}.png'
 if a.resume and complete_png(target):continue
 s.frame_set(f);s.render.filepath=str(target)
 fade=next(n for n in s.node_tree.nodes if n.bl_idname=='CompositorNodeMixRGB' and n.blend_type=='MULTIPLY')
 if max(fade.inputs[2].default_value[:3])==0:
  # A fully black compositor fade is independent of the expensive city render.
  black=bpy.data.images.new('Intro black frame',width=s.render.resolution_x,height=s.render.resolution_y,alpha=False)
  black.generated_color=(0,0,0,1);black.file_format='PNG';black.filepath_raw=str(target);black.save();bpy.data.images.remove(black)
 else:bpy.ops.render.render(write_still=True)
 assert target.is_file(),target
 print('INTRO_FRAME_DONE',f,'ELAPSED',round(time.monotonic()-started,1),flush=True)
print('INTRO_RENDER_COMPLETE',len(frames),str(output),flush=True)
