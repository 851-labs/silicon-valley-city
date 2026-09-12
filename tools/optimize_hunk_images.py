#!/usr/bin/env python3
"""Compress staged website images without changing repository originals.

Usage: python tools/optimize_hunk_images.py ../silicon_valley_hunk --github-ref COMMIT
The Hunk CLI embeds file contents in JSON; leave room for server memory overhead.
"""
import argparse
from pathlib import Path
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--github-ref', help='Already-pushed commit containing the full video and city renders')
    args = parser.parse_args()
    root = args.directory.resolve()
    if not (root / '.hunk/config.json').is_file():
        parser.error('Expected an existing Hunk staging directory')
    if (root / '.git').exists():
        parser.error('Use a staging directory, not a Git checkout')
    pages = {p: p.read_text() for p in root.glob('*.html')}
    # Keep large, already-published native artifacts on GitHub's LFS CDN.
    # It supports byte ranges, which the browser needs for video seeking.
    if args.github_ref:
        base = f'https://media.githubusercontent.com/media/851-labs/silicon-valley-city/{args.github_ref}/'
        for relative in ('animation/intro.mp4', 'animation/poster.png',
                         'renders/city_measured.png', 'renders/city_measured_sunrise.png'):
            candidates = [relative]
            if relative.endswith('.png'):
                candidates.append(str(Path(relative).with_suffix('.webp')))
            for candidate in candidates:
                if not (root / candidate).is_file():
                    continue
                pages = {p: page.replace(candidate, base + relative) for p, page in pages.items()}
                (root / candidate).unlink()
    count = 0
    saved = 0
    for original in sorted(root.rglob('*')):
        if original.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
            continue
        relative = original.relative_to(root).as_posix()
        if not any(relative in page for page in pages.values()):
            continue
        target = original.with_suffix('.webp')
        if target.exists():
            continue
        with Image.open(original) as picture:
            picture.save(target, 'WEBP', quality=96, method=6)
            with Image.open(target) as check:
                assert check.size == picture.size
        if target.stat().st_size >= original.stat().st_size:
            target.unlink()
            continue
        replacement = target.relative_to(root).as_posix()
        pages = {p: page.replace(relative, replacement) for p, page in pages.items()}
        saved += original.stat().st_size - target.stat().st_size
        original.unlink()
        count += 1
    for path, page in pages.items():
        path.write_text(page)
    files = [p for p in root.rglob('*') if p.is_file() and '.hunk' not in p.parts]
    raw_bytes = sum(p.stat().st_size for p in files)
    encoded_bytes = sum(4 * ((p.stat().st_size + 2) // 3) for p in files)
    print(f'{count} images optimized; {saved / 1048576:.2f} MiB saved')
    print(f'{len(files)} files; {raw_bytes / 1048576:.2f} MiB raw; '
          f'{encoded_bytes / 1000000:.2f} MB base64, before JSON metadata')
    if encoded_bytes > 60_000_000:
        raise SystemExit('Deployment still exceeds the conservative request budget')


if __name__ == '__main__':
    main()
