import bpy
import os

scene = bpy.data.scenes
LR = bpy.data.scenes["Lightray"]
RIM = bpy.data.scenes["_RIM"]

bpy.data.scenes["BG"].cycles.texture_limit_render = '2048'
bpy.data.scenes["BG"].cycles.samples = 256
bpy.data.scenes["BG"].cycles.texture_limit_render = '2048'
bpy.data.scenes["CH"].cycles.texture_limit_render = '4096'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

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



bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

bpy.ops.wm.save_mainfile(compress=True, relative_remap=True)

outliner = next(a for a in bpy.context.screen.areas if a.type == "OUTLINER") 
outliner.spaces[0].show_restrict_column_viewport = True
outliner.spaces[0].show_restrict_column_select = True
outliner.spaces[0].show_restrict_column_hide = True
outliner.spaces[0].show_restrict_column_render = True

bpy.data.collections["FG"].hide_select = True
bpy.data.collections["BG"].hide_select = False

vl_colls = bpy.context.view_layer.layer_collection.children

for coll in vl_colls:
    coll.exclude = False
    coll.holdout = False
    coll.indirect_only = False

vl_collect = bpy.data.collections
for coll in vl_collect:
    coll.hide_select = False
    coll.hide_viewport = False
    coll.hide_render = False



scene = bpy.context.scene

bpy.data.scenes.remove(bpy.data.scenes["AO"])
bpy.data.scenes.remove(bpy.data.scenes["PreComp"])
bpy.data.scenes.remove(bpy.data.scenes["NOR"])
bpy.data.scenes.remove(bpy.data.scenes["VOL"])

for vl in bpy.context.scene.view_layers: 
    if vl.name != '_CH': 
        bpy.context.scene.view_layers.remove(vl)


filepath = bpy.data.filepath

path = [p for p in os.path.splitext(filepath)]
path_edit = path[0] + "-CH.blend"

offlayers = [
     l for s in bpy.data.scenes for l in s.view_layers if "CH" not in l.name ]

for l in offlayers:
    l.use = False


scene = bpy.context.scene
world = bpy.data.worlds['World']

offoutputs = [
    n
    for n in bpy.data.scenes["PreComp"].node_tree.nodes
    if n.type == "OUTPUT_FILE" and not "CH_EXR" in n.label
]

for n in offoutputs:
    n.mute = True

bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value[:3] = (1.0, 1.0, 1.0)
bg.inputs[1].default_value = 1.0

framestart = bpy.data.scenes["PreComp"].frame_start 
frameend = bpy.data.scenes["PreComp"].frame_end
seq = ( frameend - framestart ) / 4

def traverse_tree(t):
    yield t
    for child in t.children:
        yield from traverse_tree(child)

coll_name = "BG"
layer_coll_master = bpy.context.view_layer.layer_collection

for layer_coll in traverse_tree(layer_coll_master):
    if layer_coll.collection.name == coll_name:
        layer_coll.indirect_only = True
        layer_coll.holdout = True
        break

# change view layer to active

view_layer = bpy.data.scenes['MAIN'].view_layers["_BG"]
bpy.context.window.view_layer = view_layer

for obj in bpy.context.selected_objects:  # Loop over all selected objects
    empty = bpy.data.objects.new(obj.name + "_null", None)  # Create new empty object
    obj.users_collection[0].objects.link(empty)  # Link empty to the current object's collection
    empty.empty_display_type = 'PLAIN_AXES'
    empty.location = obj.location
    empty.rotation_euler = obj.rotation_euler
    empty.scale = obj.scale
    
    empty.show_in_front = 1
    empty.instance_type = 'COLLECTION'
    
    empty.users_collection[0].objects.unlink(obj)

    render_frames = [f.frame for f in bpy.context.scene.timeline_markers]

for frame in render_frames:
    bpy.ops.render.render(animation=False, write_still=True)
#print (render_frames)