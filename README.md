# Silicon Valley City

A modular Blender reconstruction of the town in HBO's *Silicon Valley* opening
sequence. Buildings are modeled individually from production references, then
assembled with a shared camera and lighting rig.

[Explore the live comparison](https://silicon-valley-hunk.hunk.851.sh/)
· [Reconstruction workflow](docs/workflow.md)
· [Remaining differences](source/matching_status.json)

![Current city reconstruction in sunrise lighting](renders/city_measured_sunrise.png)

**Work in progress:** 33 measured asset types, 51 placed building instances and
36 editable library assets, including three historical alternatives. Geometry,
materials, planting and street details still differ from the show. No asset is
marked as a perfect replica.

## Open in Blender

Install Git LFS, then clone with the binary assets:

```sh
git lfs install
git clone https://github.com/851-labs/silicon-valley-city.git
cd silicon-valley-city
git lfs pull
```

Use **Blender 4.5 LTS**. Other Blender releases have not been validated.

| File | Purpose |
| --- | --- |
| `city_measured_standalone.blend` | Complete editable city with embedded building collections and no external libraries |
| `city_measured.blend` | Working city linked to the individual files in `assets/` |
| `assets/<building>/<building>.blend` | An individual editable building |
| `assets/blender_assets.cats.txt` | Catalog for adding `assets/` as a Blender Asset Library |
| `renders/city_measured.png` | City rendered with the reference lighting |
| `renders/city_measured_sunrise.png` | Low-sun lighting variation |

Frame 60 is the reference lighting; frame 1 is sunrise. The timeline animates
lighting only. Modeling uses Blender's Python API, native meshes and Cycles.

## Rebuild

Geometry uses Blender's bundled Python and the prepared JSON data in `source/`.
Reference photographs and additional Python packages are not needed to build it.
Use Python 3.10+ for the command-line wrapper. Put `blender` on your PATH, or pass
its executable path with `--blender` (the `BLENDER` environment variable also works):

```sh
# Check the saved linked and standalone files without rendering.
python3 source/refresh_measured_delivery.py --validate-only

# Rebuild the measured assets, catalog, linked city, standalone city and renders.
python3 source/refresh_measured_delivery.py --build-assets

# Refresh the assembly and renders after editing individual asset files.
python3 source/refresh_measured_delivery.py
```

On macOS, for example:

```sh
python3 source/refresh_measured_delivery.py --validate-only \
  --blender /Applications/Blender.app/Contents/MacOS/Blender
```

The current pipeline selects an available Cycles GPU, with CPU fallback. Set
`BLENDER_DEVICE=CPU` for CPU rendering, or select `METAL`, `OPTIX`, `CUDA`, `HIP`
or `ONEAPI` explicitly. Full renders can take substantial time on a CPU.
Each step writes a log under `matching/`; script failures stop the pipeline.

To run one builder directly, use Blender's Python interface:

```sh
blender --background --factory-startup --python-exit-code 1 \
  --python source/build_intel_matched.py
```

See [the workflow](docs/workflow.md) for coordinates, lighting, building edits and
validation. [The source map](source/README.md) distinguishes current entry points
from retained research and earlier revision utilities.

## Generate the comparison page

The public repository includes model previews and the comparison generator.
Production stills, video and generated source-image boards remain optional
local reference material. Their provenance is recorded in `references/`.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python tools/fetch_references.py
python source/match_boards.py
python source/create_measured_review.py
python -m http.server 8000
```

Open `http://localhost:8000/measured_review.html`. The page provides paired
source/model views, adjustable overlays, outline diagnostics, per-building
issues and both city lighting renders. Use the live Hunk page to view the
published comparison without downloading reference material.

The downloader retrieves the exact 1280 × 720 working master, verified by SHA-256.
Use `--group studio` or `--group director` for additional production stills.
Optional tracing and fitting scripts need `requirements-research.txt`; original
sign files can be obtained from [the artwork source list](references/logos/SOURCES.md).
Prepared contours are already included, so retracing is not part of a normal build.

## License and credits

[MIT](LICENSE) for the project code, documentation and original contributions.
The original sequence and production designs are by
[yU+co for HBO](https://www.yuco.com/works/silicon-valley).
Third-party imagery, designs and brand artwork retain their original rights;
see [third-party notices](THIRD_PARTY_NOTICES.md).

Blender scenes, previews and renders use Git LFS. Keep commits focused on a
building or a coherent pipeline change, with the corresponding measurements
and generated assets together.
