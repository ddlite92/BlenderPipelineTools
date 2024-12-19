import bpy 

tree = bpy.context.scene.node_tree
#layer_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "Render Layers"]
scene = bpy.data.scenes["RIM"]
for sc in scene.node_tree.nodes:
    if sc.name == 'Render Layers.002':
        sc.mute = False
    elif sc.name == 'Render Layers.012':
        sc.mute = False
    elif sc.name == 'Render Layers.003':
        sc.mute == True
    elif sc.name == 'Render Layers.001':
        sc.mute == True
    elif sc.name == 'Render Layers.012':
        sc.mute == True
    elif sc.name == 'Render Layers.013':
        sc.mute == True
        