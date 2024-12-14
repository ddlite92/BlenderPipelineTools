import bpy 

tree = bpy.context.scene.node_tree
#layer_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "Render Layers"]
scene = bpy.data.scenes["BG"]
for sc in scene.node_tree.nodes:
    if sc.name == 'BG':
        sc.mute = False
    elif sc.name == 'CH':
        sc.mute = False
    else:
        sc.mute = True
        