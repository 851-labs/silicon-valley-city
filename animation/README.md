# Animated intro reconstruction

`intro.blend` contains an editable, self-contained 261-frame reconstruction of
the season-one title shot, at 24000/1001 frames per second (10.886 seconds).
`intro.mp4` is the rendered 1920 × 1080 visual reconstruction. The public video
is silent; production music is not included in the repository.

The animation was built and inspected through the Blender MCP connection to
Blender 4.5. Rendering uses a separate Blender process launched through MCP,
so the interactive scene remains available while the sequence renders.

## What moves

- A measured orthographic camera pans and zooms for 7.638 seconds, then holds.
- Thirteen title buildings rise independently. Geometry Nodes preserve completed
  facade floors below a moving construction height; the red roofs appear last.
- YouTube grows; SGI becomes Google and AOL becomes Facebook. Pets.com rises
  above the rainbow Apple sign; Android and Chrome use the moving shot's variant.
- Myspace changes colour, Oracle gains a rooftop terrace and sign, and Blogger's
  roof and facade identities grow near the end of the shot.
- Six cranes slew their jibs and move their hoists. Six articulated excavators,
  the inflating/deflating purple balloon, and the Apple ring animate separately.
- Forty-nine vehicles follow the modeled streets. Their rotations are unwrapped
  to avoid a full spin when a road tangent crosses the Euler-angle boundary.
- Warm directional lighting evolves slightly, with the reference's five opening
  black frames and closing fade.

The HP office and smaller Hooli campus reproduce the moving reference's variant.
The static city files and original asset library are retained separately.

## Rebuild and render

These commands use Blender 4.5 and FFmpeg. The normal geometry build needs no
reference photographs or third-party Python packages.

```sh
blender --background --factory-startup --python-exit-code 1 \
  --python source/build_intro.py
blender --background --factory-startup --python-exit-code 1 \
  --python source/validate_intro.py
blender --background --factory-startup --python-exit-code 1 \
  --python source/render_intro.py -- --width 1920 --samples 16
python3 tools/encode_intro.py
```

Rendering writes PNGs under `animation/frames/`, checking frames 73, 145 and 192
first before filling the sequence. Add `--resume`
to continue an interrupted sequence with the same saved scene and settings.
Use `--frames 1,72,132,192 --output animation/previews` for selected checks.
`BLENDER_DEVICE` selects a Cycles device as documented in the project README.

`source/analyze_intro.py` optionally recomputes camera measurements from the
locally available master still and `references/season1_intro.mp4`. It requires
the research environment. `source/intro_camera.json` includes the observations
and fit residuals; `source/intro_timing.json` holds editable event timings.

For a local comparison with the original soundtrack, `tools/encode_intro.py
--reference-audio` creates an additional ignored MP4 using the locally available
reference audio. That soundtrack retains its original rights.

For synchronized side-by-side playback, with slow motion and frame stepping:

```sh
python3 source/create_intro_review.py
python3 -m http.server 8000
```

Open `http://localhost:8000/animation/compare.html`. This local review needs the
reference clip at `references/season1_intro.mp4`; its provenance and checksum are
recorded in `references/intro_manifest.json`.

## Comparison status

This is an animated reconstruction, not a frame-perfect copy. The camera fit has
approximately one-pixel median residual at 1280 × 720; that measures reference
feature alignment, not building accuracy. Building silhouettes, facade details,
parking layouts, planting, actor shapes and secondary event timings still differ.
Several hidden dimensions and motions are inferred from the visible reference.

`validation.json` checks saved resources, the camera projection, title growth,
vehicle count and the final hold. It is not a visual fidelity approval.
`video_validation.json` records the final video dimensions, decoded frame count,
render settings and scene/video SHA-256 hashes. The encoder checks every frame
header and decodes the complete MP4 before publishing it, then copies frame 192
as `poster.png` for the review page.
