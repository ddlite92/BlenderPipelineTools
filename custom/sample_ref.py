import bpy
import os

scene = bpy.data.scenes
LR = bpy.data.scenes["Lightray"]
RIM = bpy.data.scenes["_RIM"]

bpy.data.scenes["BG"].cycles.texture_limit_render = '2048'
bpy.data.scenes["BG"].cycles.samples = 256

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


bpy.data.scenes["_RIM"].node_tree.nodes["Render Layers"].mute = True
bpy.data.scenes["_RIM"].node_tree.nodes["Render Layers.001"].mute = True

bpy.ops.wm.save_mainfile(compress=True, relative_remap=True)



folder = bpy.data.filepath
full_path = os.path.dirname(folder)
filename = bpy.path.basename(bpy.context.blend_data.filepath)
basename, extension = os.path.splitext(filename)
filepath = os.path.join(full_path + '\\' + basename + "_LRBG.blend")

bpy.ops.wm.save_as_mainfile(filepath=filepath)



scene = bpy.data.scenes
scene_del = ['CH_Adudu','CH_BBB','CH_Gopal','CH_Ochobot','CH_Probe','CH_Qually','CH_Roksasa','FX_Smoke','Lightray','Outer City']

for sc in scene:
    if sc.name in scene_del:
        bpy.data.scenes.remove(sc, do_unlink=True)

bpy.data.scenes["BG"].cycles.texture_limit_render = '2048'
bpy.data.scenes["CH"].cycles.texture_limit_render = '4096'

bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

bpy.ops.wm.save_mainfile(compress=True, relative_remap=True)



