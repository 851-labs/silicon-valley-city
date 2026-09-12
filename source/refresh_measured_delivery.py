"""Run delivery steps sequentially, rejecting Blender's silent script failures."""
from pathlib import Path
import argparse
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tag', nargs='?', default='local', help='Log filename suffix')
    parser.add_argument('--blender', default=os.environ.get('BLENDER', 'blender'),
                        help='Blender 4.5 executable (or set BLENDER)')
    parser.add_argument('--build-assets', action='store_true', help='Rebuild all measured assets first')
    parser.add_argument('--validate-only', action='store_true', help='Check saved files without rendering')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.tag):
        parser.error('tag must contain only letters, digits, underscores or hyphens')
    if args.build_assets and args.validate_only:
        parser.error('--build-assets and --validate-only cannot be combined')
    executable = shutil.which(os.path.expanduser(args.blender))
    if not executable:
        parser.error('Blender was not found; pass --blender or set BLENDER')
    steps = [
        ('catalog_assets.py', ['--measured-checkpoint'], 'catalog'),
        ('assemble_city.py', ['--measured-checkpoint'], 'city'),
        ('make_portable_city.py', ['--measured-checkpoint'], 'portable'),
        ('validate_measured_delivery.py', [], 'validate'),
        ('render_measured_sunrise.py', [], 'sunrise'),
    ]
    if args.validate_only:
        steps = [steps[3]]
    elif args.build_assets:
        steps.insert(0, ('build_measured_checkpoint.py', [], 'assets'))
    environment = os.environ.copy()
    for name in ('PYTHONHOME', 'PYTHONPATH'):
        environment.pop(name, None)
    (ROOT / 'matching').mkdir(exist_ok=True)
    for script, flags, label in steps:
        log = ROOT / 'matching' / f'{label}_measured_{args.tag}.log'
        command = [executable, '--background', '--factory-startup', '--python-exit-code', '1',
                   '--python', str(ROOT / 'source' / script)]
        if flags:
            command += ['--', *flags]
        print('START', script, flush=True)
        with log.open('w') as output:
            result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                                    env=environment, cwd=ROOT)
        contents = log.read_text(errors='replace')
        if result.returncode or 'Traceback (most recent call last)' in contents:
            raise RuntimeError(f'{script} failed: {log}\n{contents[-4000:]}')
        print('DONE', script, flush=True)
    print('MEASURED_DELIVERY_REFRESHED', args.tag, flush=True)


if __name__ == '__main__':
    main()
