import bpy,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'city.blend'))
s=bpy.context.scene;s.render.resolution_percentage=50;s.cycles.samples=24
bpy.ops.render.render()
for transform,look,exposure,name in [('Standard','None',0,'standard'),('AgX','AgX - Medium High Contrast',0,'agx'),('AgX','AgX - Medium High Contrast',1,'agx_plus1'),('AgX','AgX - Medium High Contrast',1.5,'agx_plus15')]:
 s.view_settings.view_transform=transform
 try:s.view_settings.look=look
 except:s.view_settings.look='None'
 s.view_settings.exposure=exposure
 bpy.data.images['Render Result'].save_render(str(ROOT/'renders'/('color_'+name+'.png')),scene=s)
