# Reference material

Production: [yU+co — Silicon Valley](https://www.yuco.com/works/silicon-valley)
and the [Director's Cut](https://www.behance.net/gallery/22483561/HBO-Silicon-Valley-Main-Titles-(Directors-Cut)).
The sequence contains seasonal variants. Current measurements target the
1280 × 720 `original_wide.webp` master, not every variant simultaneously.

`download_manifest.json` records the exact files, URLs and SHA-256 hashes used
in this study. The master is preserved on the project's Hunk review site;
additional stills come directly from the production studio and Behance CDN.
`studio_manifest.json` and `director/manifest.json` preserve their original IDs.

From the repository root:

```sh
python3 tools/fetch_references.py                 # master only
python3 tools/fetch_references.py --group studio  # 30 studio stills
python3 tools/fetch_references.py --group director
```

The script verifies existing files and refuses content whose checksum differs
from the recorded reference. Downloaded images and video are ignored by Git.
Normal geometry builds use prepared data in `source/` and require no downloads.

The original logo files used for optional retracing are listed in
[`logos/SOURCES.md`](logos/SOURCES.md). Their prepared contour data are included
under `source/`. Source artwork keeps its original rights; see
[third-party notices](../THIRD_PARTY_NOTICES.md).
