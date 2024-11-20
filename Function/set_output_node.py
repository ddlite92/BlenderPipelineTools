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
            

'''
##### to be merged and revised based on this code #####

def set_render_path():
    base_path = Path(r"M:\BBBGS2_Gentar_Arc\2_Episode\Episode_15\6_Post\3_Output\1_Render")
    folder_name = bpy.path.basename(bpy.context.blend_data.filepath)[:-7]  # Remove "_Render"
    scene_name = bpy.context.scene.name
    output_path = base_path / folder_name / scene_name / "Beauty" / "Beauty_"

    # Adjust path separator based on OS
    if os.name == 'nt':  # Windows
        output_path = str(output_path)
    else:  # Linux/macOS
        output_path = str(output_path).replace('\\', '/')

    bpy.context.scene.render.filepath = output_path


def create_beauty_node():
  """Creates a BeautyOutput node if it doesn't already exist."""
  node_tree = bpy.context.scene.node_tree
  links = node_tree.links

  if not node_tree.nodes.get("BeautyOutput"):
    beauty_node = node_tree.nodes.new(type="CompositorNodeOutputFile")
    beauty_node.location = 500, 1000
    beauty_node.name = "BeautyOutput"
    beauty_node.label = "Beauty"
    
    # Assuming there's a Denoise node before BeautyOutput (modify if needed)
    denoise_node = node_tree.nodes.get("Denoise")
    if denoise_node:
      input_socket = beauty_node.inputs["Image"]
      output_socket = denoise_node.outputs["Image"]
      links.new(output_socket, input_socket)
    
def configure_output_nodes():
    node_tree = bpy.context.scene.node_tree
    for node in node_tree.nodes:
        if node.type in ('OUTPUT_FILE', 'CompositorNodeOutputFile'):
            node.file_slots[0].path = ""  # Clear existing path
            label_name = node.label.split("_")[-1]

            # Check if the node is the "BeautyOutput" node
            if node.name == "BeautyOutput":
                # If it is, set the base path to the parent directory of the render path
                node.base_path = str(Path(bpy.context.scene.render.filepath).parent)
            else:
                # For other nodes, set the base path as before
                if "Emission" in node.label:
                    node.base_path = str(Path(bpy.context.scene.render.filepath).parent / node.label)
                    node.format.color_mode = "RGB"
                elif "Matte" in node.label:
                    node.base_path = str(Path(bpy.context.scene.render.filepath).parent / node.label)
                    node.format.file_format = "OPEN_EXR_MULTILAYER"
                    node.format.color_mode = "RGBA"
                    node.format.color_depth = "32"
                else:
                    node.base_path = str(Path(bpy.context.scene.render.filepath).parent / label_name)
                    node.format.file_format = "PNG"
                    node.format.color_mode = "RGBA"
                    node.format.color_depth = "16"

            node.file_slots[0].path = label_name + "_"  # Set file name

# bpy.ops.render.render(write_still=True)  # Render the image



'''