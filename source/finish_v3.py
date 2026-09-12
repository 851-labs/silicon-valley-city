import runpy,sys
from pathlib import Path
ROOT=Path(__file__).parent
scripts=['build_title.py','build_facebook_matched.py','relight_previews.py','build_west_solar.py','catalog_assets.py','assemble_city.py','final_render.py','make_portable_city.py','validate_delivery.py']
if '--start' in sys.argv:scripts=scripts[scripts.index(sys.argv[sys.argv.index('--start')+1]):]
for name in scripts:
 print('FINISH_START',name,flush=True)
 sys.argv=[name,'--no-render'] if name=='assemble_city.py' else [name]
 runpy.run_path(str(ROOT/name),run_name='__main__')
 print('FINISH_COMPLETE',name,flush=True)
print('V3_FINISHED',flush=True)
