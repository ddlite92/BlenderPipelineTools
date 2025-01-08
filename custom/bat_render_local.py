import bpy

scene = bpy.data.scenes
BG = bpy.data.scenes["BG"]
  
bpy.data.scenes["BG"].cycles.texture_limit_render = '2048'
bpy.data.scenes["BG"].cycles.samples = 256

for sc in scene:
    if sc.name == '_RIM':
        continue
    if sc.name == 'RIM':
        RIM = bpy.data.scenes["RIM"]   
        RIM.name = '_RIM'


bpy.context.window.scene = BG

for window in bpy.context.window_manager.windows:
    for area in window.screen.areas: # iterate through areas in current screen
        if area.type == 'VIEW_3D':
            for space in area.spaces: # iterate through spaces in current VIEW_3D area
                if space.type == 'VIEW_3D': # check if space is a 3D view
                    space.shading.type = 'WIREFRAME'

RIM = bpy.data.scenes["_RIM"] 
bpy.context.window.scene = RIM

bpy.ops.wm.save_mainfile(compress=True, relative_remap=True)