"""Re-render the assets measured so far, using one calibrated camera and light rig."""
import sys,runpy,os,json
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P))
for script in ['build_google.py','build_facebook_matched.py','build_youtube.py','build_intel_matched.py','build_ebay_matched.py','build_west_solar_matched.py','build_western_matched.py','build_neighbors_matched.py','build_twitter_matched.py','build_apple_matched.py','build_title_matched.py','build_hooli_matched.py','build_yahoo_matched.py','build_myspace_matched.py','build_adobe_matched.py','build_energy_matched.py','build_netscape_matched.py','build_security_matched.py','build_terrace_matched.py','build_north_office_matched.py','build_northeast_matched.py','build_white_corner_matched.py','build_stadium_matched.py','build_framing_matched.py','build_zynga_matched.py','build_legacy_hp_matched.py','build_balloon_matched.py','build_gabled_house_matched.py','build_service_office_matched.py']:
 sys.argv=[script];runpy.run_path(str(P/script),run_name='__main__')
 print('CHECKPOINT_SCRIPT_DONE',script,flush=True)
