import bpy

scene = bpy.data.scenes

for sc in scene:
    sc.cycles.tile_size = 8192

BG = bpy.data.scenes["BG"]
RIM = bpy.data.scenes["RIM"]   

bpy.context.window.scene = BG
bpy.data.objects["Fill Light.003"].visible_transmission = False
bpy.data.objects["Sun"].visible_transmission = False
bpy.data.scenes["BG"].cycles.texture_limit_render = '2048'
bpy.data.scenes["BG"].cycles.samples = 256
bpy.context.window.scene = RIM

bpy.ops.wm.save_mainfile(compress=True, relative_remap=True)

"""
etc
#bpy.context.view_layer.layer_collection.children["L.CH"].exclude = True
#bpy.context.view_layer.layer_collection.children["L.LIGHTRAY"].exclude = True
#bpy.context.view_layer.layer_collection.children["LIGHTING"].exclude = True
#bpy.context.view_layer.layer_collection.children["LIGHTING"].exclude = False


"""