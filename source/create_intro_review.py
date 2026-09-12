"""Create a local synchronized source/Blender player from the available videos."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT/'animation/intro.mp4', ROOT/'references/season1_intro.mp4'):
    if not path.is_file():
        raise FileNotFoundError(path)

page = '''<!doctype html>
<html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Silicon Valley — synchronized shot comparison</title>
<style>
:root{font:16px Arial,sans-serif;color:#26332f;background:#f4f2e9}
*{box-sizing:border-box}body{margin:0;padding:30px;max-width:1920px;margin-inline:auto}
h1{font-size:clamp(28px,3.5vw,48px);letter-spacing:-1.5px;margin:12px 0}
p{line-height:1.6;max-width:1050px}a{color:#436e56;text-underline-offset:4px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:28px 0 20px}
figure{margin:0}video{width:100%;aspect-ratio:16/9;display:block;background:#111}
figcaption{padding:12px 0;font-size:14px}.controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
button,select{font:inherit;color:inherit;background:#fff;border:1px solid #b6c5b7;border-radius:4px;padding:10px 14px}
button{cursor:pointer}#play{background:#254a3a;color:white;min-width:100px}
.scrub{display:flex;gap:16px;align-items:center;margin:20px 0}input[type=range]{flex:1;accent-color:#254a3a}
output{min-width:165px;font-variant-numeric:tabular-nums;font-size:14px}
.muted{font-size:13px;color:#637366}button:focus-visible,input:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #db9b3b;outline-offset:3px}
@media(max-width:850px){body{padding:20px}.pair{grid-template-columns:1fr}.controls{gap:8px}button,select{font-size:14px}}
</style>
<body><p class="muted">SILICON VALLEY / SHOT COMPARISON</p>
<h1>Compare the moving shot.</h1>
<p>Play both versions together, slow them down, or step through individual frames. Building details and secondary motion remain under comparison.</p>
<div class="pair">
<figure><video id="source" preload="auto" playsinline muted data-src="../references/season1_intro.mp4" aria-label="Original production reference"></video><figcaption>Original production reference · yU+co / HBO</figcaption></figure>
<figure><video id="model" preload="auto" playsinline muted data-src="intro.mp4" aria-label="Blender reconstruction"></video><figcaption>Blender reconstruction · identical elapsed time</figcaption></figure>
</div>
<div class="controls">
<button id="play">Play both</button><button id="previous" aria-label="Previous frame">← Frame</button><button id="next" aria-label="Next frame">Frame →</button><button id="restart">Restart</button>
<label>Speed <select id="speed"><option value="1">1×</option><option value="0.5">0.5×</option><option value="0.25">0.25×</option></select></label>
<label><input type="checkbox" id="sound"> Reference audio</label>
</div>
<label class="scrub"><span>Frame</span><input type="range" id="frame" min="0" max="260" step="1" value="5" aria-label="Comparison frame"><output id="time">006 / 261 · 0.209 s</output></label>
<p id="status" class="muted" role="status">Loading both videos…</p>
<p class="muted"><a href="../measured_review.html">Individual building comparisons</a> · <a href="https://www.yuco.com/works/silicon-valley">Production credits and references</a></p>
<script>
const fps=24000/1001,total=261,$=id=>document.getElementById(id),model=$('model'),source=$('source');
let ready=0,playing=false;const mediaUrls=[];
function currentFrame(){return Math.min(260,Math.max(0,Math.floor(model.currentTime*fps+1e-6)))}
function display(){const frame=currentFrame();$('frame').value=frame;$('time').textContent=String(frame+1).padStart(3,'0')+' / 261 · '+(frame/fps).toFixed(3)+' s'}
function pause(){playing=false;model.pause();source.pause();$('play').textContent='Play both'}
function seek(frame){pause();const time=Math.min(260,Math.max(0,frame))/fps+.0001;model.currentTime=time;source.currentTime=time;display()}
async function play(){if(ready<2)return;if(playing){pause();return}if(model.currentTime>=(total-1)/fps)seek(0);source.currentTime=model.currentTime;playing=true;$('play').textContent='Pause both';try{await Promise.all([source.play(),model.play()]);$('status').textContent='Synchronized playback · 23.976 frames per second'}catch(error){pause();$('status').textContent='Playback could not start: '+error.message}}
for(const video of [model,source]){
 video.addEventListener('loadedmetadata',()=>{ready++;if(ready===2){seek(5);$('status').textContent='Ready · use the frame control for exact still comparisons'}});
 video.addEventListener('error',()=>{pause();$('status').textContent='A video could not load. Serve this project from its root and check the local reference file.'});
 // Blob URLs preserve seeking even on simple static servers without HTTP Range.
 fetch(video.dataset.src).then(response=>{if(!response.ok)throw new Error(response.status+' '+video.dataset.src);return response.blob()}).then(blob=>{const url=URL.createObjectURL(blob);mediaUrls.push(url);video.src=url;video.load()}).catch(error=>{$('status').textContent='Could not load a comparison video: '+error.message});
}
window.addEventListener('pagehide',()=>mediaUrls.forEach(url=>URL.revokeObjectURL(url)));
model.addEventListener('ended',pause);model.addEventListener('seeked',display);
$('play').addEventListener('click',play);$('previous').addEventListener('click',()=>seek(currentFrame()-1));$('next').addEventListener('click',()=>seek(currentFrame()+1));$('restart').addEventListener('click',()=>seek(0));$('frame').addEventListener('input',event=>seek(Number(event.target.value)));
$('speed').addEventListener('change',event=>{model.playbackRate=source.playbackRate=Number(event.target.value)});$('sound').addEventListener('change',event=>{source.muted=!event.target.checked});
function tick(){if(playing){display();if(Math.abs(source.currentTime-model.currentTime)>1/fps)source.currentTime=model.currentTime}requestAnimationFrame(tick)}requestAnimationFrame(tick);
</script></body></html>'''

target=ROOT/'animation/compare.html'
target.write_text(page)
print('INTRO_COMPARISON_READY',target)
