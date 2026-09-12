"""Rebuild all 30 source-driven assets, with progress and resumable checkpoints."""
import runpy,os,sys,json
from pathlib import Path
ROOT=Path(__file__).parent
scripts=['build_title.py','build_youtube.py','build_netscape.py','build_google.py','build_offices.py','build_campuses.py','build_landmarks.py','build_district.py','build_west_solar.py','build_props.py','build_digg_variant.py','build_facebook_matched.py','catalog_assets.py']
start=sys.argv[sys.argv.index('--start')+1] if '--start' in sys.argv else scripts[0]
scripts=scripts[scripts.index(start):]
for script in scripts:
 print('V3_BUILD_START',script,flush=True)
 runpy.run_path(str(ROOT/script),run_name='__main__')
 print('V3_BUILD_COMPLETE',script,flush=True)
print('V3_LIBRARY_COMPLETE',flush=True)
