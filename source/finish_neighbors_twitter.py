import runpy,sys
from pathlib import Path
P=Path(__file__).parent
for name in ['build_neighbors_matched.py','build_twitter_matched.py']:
 sys.argv=[name];runpy.run_path(str(P/name),run_name='__main__')
