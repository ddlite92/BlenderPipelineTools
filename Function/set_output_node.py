import bpy
import os
import logging
from os import path
from pathlib import Path

"""

Still WIP
- iterate node label
- function to get 
    - filename ( to be test )
    - folder ( to be test )
    - scene ( done )
- scene_names function get the first scene only, need to change to index 1,2,3,4 respectively ( fixed )
- function filename removed due non use
"""
path = r"M:\BBBGS2_Gentar_Arc\2_Episode\Episode_15\6_Post\3_Output\1_Render\PART B\_MONSTA"

filepath = bpy.data.filepath

mainScreen = bpy.context.window
node_tree = bpy.context.scene.node_tree
links = node_tree.links

def folder():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    return new_basename

def scene_name():
    scene_names = [scene.name for scene in bpy.data.scenes]
    for scene_name in scene_names:
        scene = bpy.context.scene.name
        return scene
    
bpy.context.scene.render.filepath = os.path.join(path, folder(), scene_name(), "Beauty", "Beauty_" )

def output_node():
    for node in mainScreen.scene.node_tree.nodes:
        nodeBeauty = node_tree.nodes.get("BeautyOutput")
        current_scene_name = scene_name()
        if not nodeBeauty:
            beautyNode = node_tree.nodes.new(type="CompositorNodeOutputFile")
            beautyNode.location = 500, 1000
            beautyNode.name = 'BeautyOutput'
            beautyNode.label = 'Beauty'
            beauty_node = node_tree.nodes['BeautyOutput']
            input_socket = beauty_node.inputs['Image']
            denoise_node = node_tree.nodes['Denoise']
            output_socket = denoise_node.outputs['Image']
            links.new(output_socket, input_socket)
                       
        elif "Emission" in node.label:
            node.file_slots[0].path = ''
            filename = node.file_slots.keys()[0]
            label_name = node.label.split("_")[-1]
            node.file_slots[filename].path = label_name + '_'
            node.base_path = path + "\\" + folder() + "\\" + current_scene_name + "\\" + node.label + "\\"
            node.format.color_mode = "RGB" 
        
        elif "Matte" in node.label:
            node.file_slots[0].path = ''
            filename = node.file_slots.keys()[0]
            label_name = node.label.split("_")[-1]
            node.file_slots[filename].path = label_name + '_'
            node.base_path = path + "\\" + folder() + "\\" + current_scene_name  + "\\" + node.label + "\\"
            node.format.file_format = "OPEN_EXR_MULTILAYER"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "32"

        elif node.type == 'OUTPUT_FILE':
            node.file_slots[0].path = ''
            filename = node.file_slots.keys()[0]
            label_name = node.label.split("_")[-1]
            node.file_slots[filename].path = label_name + '_'
            node.base_path = path + "\\" + folder() + "\\" + current_scene_name + "\\" + node.label + "\\"
            node.format.file_format = "PNG"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "16"

            
        else:
            print("check node name")
            