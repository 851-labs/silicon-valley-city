"""Western masonry office, measured against the director's wide-frame crop."""
import os,sys,math
sys.path.insert(0,os.path.dirname(__file__))
import asset_core as A
A.reset('west_solar','Western masonry office and stepped solar roof',['Original wide frame • pixels 157,364–327,481','YU09 • earlier roof variant'])
A.surface_detail(A.material('aggregate_concrete',(.40,.385,.33),.83),.045,7)
A.surface_detail(A.material('roof_membrane',(.77,.72,.60),.82),.016,65)
A.surface_detail(A.material('entry_stone',(.52,.51,.455),.8),.03,12)
A.part('Solid aggregate masonry envelope')
A.box('Continuous unglazed square masonry block',(0,0,3.32),(27,22,6.64),'aggregate_concrete')
# Fine panel joints are sparse, dark and recessed, rather than white window frames.
for yy in (-11.012,11.012):
 for x in (-9,-4.5,0,4.5,9):A.box('Vertical precast joint',(x,yy,3.2),(.013,.014,6.1),'stone')
for xx in (-13.512,13.512):
 for y in (-7.3,-3.65,0,3.65,7.3):A.box('Vertical precast return joint',(xx,y,3.2),(.014,.013,6.1),'stone')
A.part('Cream membrane and thin raised coping')
A.box('Thin pale roof edge',(0,0,6.82),(27.65,22.65,.32),'cream')
A.box('Continuous pale roof membrane',(0,0,7.0),(27.04,22.04,.07),'roof_membrane')
for x in (-13.69,13.69):A.box('Low concrete roof coping',(x,0,7.09),(.21,22.65,.20),'cream')
for y in (-11.19,11.19):A.box('Low concrete coping return',(0,y,7.09),(27.65,.21,.20),'cream')
# Source: broad near band, narrow east band, stepped west band and two separate rear blocks.
A.solar(11.65,.1,7.10,2.50,20.0,15,2,tilt=12)
A.solar(-1.6,9.76,7.10,23.8,1.45,1,17,tilt=12)
A.solar(3.2,-9.42,7.10,14.4,2.05,2,11,tilt=12)
A.solar(-7.2,-9.17,7.10,5.8,2.55,2,4,tilt=12)
A.solar(-11.65,-7.25,7.10,2.9,6.70,5,2,tilt=12)
A.solar(-11.65,8.25,7.10,2.9,4.9,4,2,tilt=12)
A.part('Low stepped projecting entry on east elevation')
A.box('Entry left shoulder',(14.35,-3.8,2.45),(3.15,1.85,4.9),'entry_stone')
A.box('Entry right shoulder',(14.35,.2,2.45),(3.15,1.85,4.9),'entry_stone')
A.box('Taller central stair landing',(14.45,-1.8,3.10),(3.35,2.25,6.2),'entry_stone')
A.box('Recessed entry door',(16.138,-1.80,.94),(.04,1.1,1.87),'dark')
A.box('Central pale landing cap',(14.45,-1.8,6.22),(3.45,2.33,.13),'cream')
for y in (-3.8,.2):A.box('Shoulder pale flat cap',(14.35,y,4.95),(3.22,1.92,.13),'cream')
A.part('Lower west annex and narrow connector')
A.box('Solid west annex',(4.5,-17.05,2.0),(8.9,8.9,4.0),'aggregate_concrete')
A.box('Pale annex roof',(4.5,-17.05,4.18),(9.45,9.45,.30),'cream')
A.solar(4.5,-17.05,4.37,8.0,8.0,6,6,tilt=12)
A.box('Lower connecting masonry block',(5.1,-12.35,1.30),(5.2,2.3,2.6),'aggregate_concrete')
A.box('Connector roof',(5.1,-12.35,2.72),(5.4,2.45,.22),'cream')
A.part('Entry apron and planted edges')
A.box('Pale entrance landing',(16.2,-1.8,.08),(2.0,4.8,.16),'cream')
for x,y,h in [(17.0,-7.0,3.4),(17.6,5.5,4.8),(19.0,-2.5,3.9)]:
 A.cylinder('Slender cypress trunk',(x,y,.8),.07,1.6,'wood',8)
 A.cylinder('Tapering cypress crown',(x,y,h*.56),.75,h*.92,'leaf_dark',12,r2=.018)
A.COL['measured_features']='Roof edges: (178,386), (291,379), (316,435), (193,447). Predominantly blank walls; six distinct PV fields; stepped entry below main roof.'
A.setup_preview(82.134,26.377,1500,1100);A.save_asset('west_solar')
