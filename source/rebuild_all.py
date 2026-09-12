"""Regenerate the current measured library and delivery, preserving the old revision."""
import runpy,sys
from pathlib import Path
P=Path(__file__).parent
runpy.run_path(str(P/'build_measured_checkpoint.py'),run_name='__main__')
for script,flags in [('catalog_assets.py',['--measured-checkpoint']),('assemble_city.py',['--measured-checkpoint']),('make_portable_city.py',['--measured-checkpoint']),('validate_measured_delivery.py',[]),('render_measured_sunrise.py',[])]:
 sys.argv=[script,'--',*flags];runpy.run_path(str(P/script),run_name='__main__')
print('MEASURED_REBUILD_ALL_DONE',flush=True)
