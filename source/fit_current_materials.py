import sys,runpy
from pathlib import Path
P=Path(__file__).parent
for id,script in [('west_solar','build_west_solar_matched.py'),('ebay','build_ebay_matched.py')]:
 sys.argv=[script,'--no-render'];runpy.run_path(str(P/script),run_name='__main__')
 sys.argv=['fit_asset_colors.py','--',id];runpy.run_path(str(P/'fit_asset_colors.py'),run_name='__main__')
