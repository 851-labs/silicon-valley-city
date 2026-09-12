"""Compare four remaining major roof materials at fixed, verified source probes."""
import runpy,sys
from pathlib import Path
P=Path(__file__).parent
for asset in ['facebook','google','intel','twitter']:
 sys.argv=['fit_asset_colors.py','--',asset]
 runpy.run_path(str(P/'fit_asset_colors.py'),run_name='__main__')
print('PRIMARY_ROOF_FITS_DONE',flush=True)
