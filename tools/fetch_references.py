"""Download optional production references, checking the recorded SHA-256 hashes."""
from pathlib import Path
import argparse
import hashlib
import json
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group', choices=['master', 'studio', 'director', 'all'], default='master')
    parser.add_argument('--list', action='store_true', help='List selected references without downloading')
    args = parser.parse_args()
    entries = json.loads((ROOT / 'references/download_manifest.json').read_text())
    for entry in entries:
        if args.group != 'all' and entry['group'] != args.group:
            continue
        destination = (ROOT / entry['file']).resolve()
        if not destination.is_relative_to(ROOT / 'references'):
            raise ValueError(f'Invalid reference path: {entry["file"]}')
        if args.list:
            print(entry['file'], entry['url'])
            continue
        if destination.exists():
            if hashlib.sha256(destination.read_bytes()).hexdigest() != entry['sha256']:
                raise RuntimeError(f'{destination} differs from the manifest; preserve it before replacing it')
            print('VERIFIED', entry['file'])
            continue
        request = urllib.request.Request(entry['url'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise RuntimeError(f'Remote content changed: {entry["url"]}; expected file was not written')
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix='.part', delete=False) as output:
            temporary = Path(output.name)
            output.write(data)
        try:
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        print('DOWNLOADED', entry['file'])


if __name__ == '__main__':
    main()
