import bpy
import os

scene = bpy.data.scenes
LR = bpy.data.scenes["Lightray"]
RIM = bpy.data.scenes["_RIM"]

bpy.data.scenes["BG"].cycles.texture_limit_render = '1024'
bpy.data.scenes["CH"].cycles.texture_limit_render = '1024'

for window in bpy.context.window_manager.windows:
    for area in window.screen.areas: # iterate through areas in current screen
        if area.type == 'VIEW_3D':
            for space in area.spaces: # iterate through spaces in current VIEW_3D area
                if space.type == 'VIEW_3D': # check if space is a 3D view
                    space.shading.type = 'WIREFRAME'

bpy.context.window.scene = LR

coll = bpy.context.view_layer.layer_collection.children
for collection in coll:
    if collection.name == 'CHAR':
        bpy.context.view_layer.active_layer_collection = collection
        collection.exclude = True

bpy.context.window.scene = RIM

bpy.ops.wm.save_mainfile(compress=True, relative_remap=True)

