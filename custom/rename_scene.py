import bpy

scene = bpy.data.scenes

bpy.data.scenes["BG"].cycles.texture_limit_render = '4096'
bpy.data.scenes["BG"].cycles.samples = 512

for sc in scene:
    if sc.name == '_RIM':
        continue
    if sc.name == 'RIM':
        RIM = bpy.data.scenes["RIM"]   
        RIM.name = '_RIM'

bpy.ops.wm.save_mainfile(compress=True, relative_remap=True)