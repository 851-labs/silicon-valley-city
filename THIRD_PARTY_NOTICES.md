# Third-party notices

The root MIT license covers this project's code, documentation and original
contributions to the models. It does not grant rights to the underlying show,
production designs, reference photographs or third-party names and artwork
reproduced in the reconstruction. This is an independent study, unaffiliated
with HBO, yU+co or the depicted companies.

## Production references

The town is reconstructed from the opening titles of HBO's *Silicon Valley*,
created by yU+co. Attribution and production material:

- [yU+co — Silicon Valley](https://www.yuco.com/works/silicon-valley)
- [HBO Silicon Valley Main Titles (Director's Cut)](https://www.behance.net/gallery/22483561/HBO-Silicon-Valley-Main-Titles-(Directors-Cut))

Production stills, footage and reference-derived comparison boards are not
included in Git. The optional reference downloader retains source URLs and
stores these materials locally, outside the tracked files. Their original
rights remain with their respective owners.

## Sign artwork

Prepared contour and triangulation data in `source/*_mesh.json`,
`source/logo_shapes.json`, title contours, and their instances in Blender
files and renders reproduce third-party artwork. They are not relicensed
under MIT. See [the artwork source list](references/logos/SOURCES.md) for
individual credits and provenance.

- **Twitter bird:** Twitter, Inc., from `twitter/opensource-website`, commit
  `2887311216d99cd0e38b16e564bcdbea3797eb63`. Apache License 2.0; a copy is in
  `LICENSES/Apache-2.0.txt`. The SVG was converted to normalized contours and
  extruded meshes; the rendered colour follows the production reference.
- **Hooli icon:** Font Awesome Free 6.4.2 by Fonticons, Inc.,
  [original icon](https://github.com/FortAwesome/Font-Awesome/blob/6.4.2/svgs/brands/hooli.svg),
  licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  The orbital swoosh was removed, the h stem and shoulder were repaired,
  and the intact second o was duplicated before triangulation and extrusion.
- Other company marks remain the artwork and trademarks of their respective
  owners. Source attribution is retained even where artwork consists of
  simple lettering or shapes.

Blender and optional Python dependencies are installed separately and retain
their own licenses. No system font files are distributed with this repository.
