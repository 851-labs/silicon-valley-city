# Reconstruction workflow

The current checkpoint contains 33 measured asset types placed as 51 linked
instances, plus three retained historical alternatives in the 36-asset library.
Each building has its own `.blend`, preview, script and measured features.
No building has been accepted as a perfect replica.

## Coordinate system

`source/camera_calibration.json` and `source/reference_geometry.py` define a
shared orthographic camera for the 1280 × 720 master frame. Five source pixels
correspond to one relative unit. Roof contours are unprojected at their measured
elevations, then extruded into meshes. Physical dimensions and hidden elevations
are inferred; these are not survey measurements.

`source/*_measurements.json` records roof outlines, anchors, crops and facade
features. Measured city instances use unit scale and zero rotation. Nearby
repeated buildings have separately recorded anchors. No production photograph
is projected onto the geometry.

## Editing one building

1. Read its measurements and unresolved issues in `source/matching_status.json`.
2. Edit its builder and measurement data, then rebuild that asset in Blender.
3. Generate comparison boards with the same camera and crop on both sides.
4. Inspect silhouette, roof levels, windows, signage, vegetation and shadows.
5. Update the ledger with the remaining differences. Keep feature-fit metrics
   separate from visual acceptance.
6. Refresh the catalog, linked city, standalone city and both lighting renders.
7. Commit the building's source, measurements, `.blend` and preview together.
   Commit resulting assembly changes separately when they affect multiple assets.

Most builders are named `build_<asset>_matched.py`. The complete list is in
`source/build_measured_checkpoint.py`; some builders generate multiple assets.
`build_google.py` and `build_youtube.py` are current measured builders despite
their shorter names.

## Lighting and validation

Frame 60 uses the common shadow study: sun azimuth 138°, elevation 46°, warm
directional light, cool sky fill and Standard colour management. Frame 1 is
the warmer 20° sunrise variation; frame 120 raises the sun to 58°. Only lighting
is animated.

Material fits sample documented probes. The probe reader checks the material
on the evaluated mesh, including modifiers, and optionally checks direct-sun
visibility. Agreement at selected probes is not a whole-building score.

`validate_measured_delivery.py` reopens both saved scenes and compares mesh
hashes, instances, transforms, anchor projections, fonts and external libraries.
Its PASS result means delivery integrity, not visual fidelity.

## Current limitations

The assembly still differs substantially from the intro in street details,
planting, facade patterns, rooftop equipment, reflections and colour response.
Read the per-asset ledger and [checkpoint notes](checkpoint-33b.md) before
choosing the next improvement.

The initial public commits introduce the existing checkpoint in functional
chunks. They do not reconstruct or backdate the earlier modeling session.
