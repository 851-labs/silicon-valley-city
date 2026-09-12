"""Recalibrate existing PV probes after the shared surface response change."""
import runpy,sys
from pathlib import Path
P=Path(__file__).parent
for id in ['west_solar','ebay','terrace_office']:
 sys.argv=['fit_asset_colors.py','--',id];runpy.run_path(str(P/'fit_asset_colors.py'),run_name='__main__')
print('PV_PROBE_REFITS_DONE',flush=True)
