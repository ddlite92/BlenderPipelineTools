import bpy
import os
import logging
from os import path
from pathlib import Path
context = bpy.context
filepath =  bpy.data.filepath

def get_1st_lvl():
    filepath =  bpy.data.filepath
    full_path = os.path.dirname(filepath)
    base_path = "Documents/ScriptPY/Monsta/Blender/Path_Testing"
    relative_path = os.path.relpath(full_path, base_path)
    return(relative_path)  

def get_workpath():
    #filepath = bpy.data.filepath
    blendpath = '/'.join(filepath.split('/')[7:8]) + '/'
    return(blendpath)   

def get_shotname():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    return new_basename
       
def set_renderpath():
    final = os.path.join(get_1st_lvl())
    final = final.replace("2_Work", "3_Output")
    return(final)


def set_main_node():
    scene = context.scene
    renderpath = set_renderpath()
    shotname = get_shotname()

    local_scenes = [s for s in bpy.data.scenes if not s.library]
    
    scenes = [s for s in local_scenes]
    for scn in scenes:
            scn.render.filepath = path.join(renderpath + '/' + shotname + '_')
    
    output_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "OUTPUT_FILE"]
    for node in output_nodes:
        if "_Matte" in node.label:
            label_name = node.label.split("_Matte")[0]
            pass_name = 'Matte'
            splitOutput = os.path.join(renderpath + '/' + shotname + '_')
            node.base_path = os.path.join(renderpath + '/' + label_name + '/' + pass_name + '/')
            node.format.file_format = "OPEN_EXR_MULTILAYER"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "32"
        
        elif "_Emission" in node.label:
            label_name = node.label.split("_Emission")[0]
            pass_name = node.label.split("_")[1]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '/' + label_name + '/' + pass_name + '/')
            node.base_path = node_output
            node.file_slots[filename].path = pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_mode = "RGB"
            node.format.color_depth = "16"
        
        elif "RIM_" in node.label:
            #label_name = node.label
            pass_name = node.label.split("_")[0]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '/' + pass_name + '/')
            node.base_path = node_output
            node.file_slots[filename].path = pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "16"
        
        elif "Lightray_" in node.label:
            #label_name = node.label
            pass_name = node.label.split("_")[0]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '/' + pass_name + '/')
            node.base_path = node_output
            node.file_slots[filename].path = pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "16"
                                
        else:
            label_name = node.label.split(".")[1]
            print('label_name1: ', label_name)
            label_name = node.label.split("_")[0]
            print('label_name2: ', label_name)
            pass_name = node.label.split("_")[1]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '/' + label_name + '/' + pass_name + '/')
            node.base_path = node_output
            node.file_slots[filename].path = label_name +  pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_depth = "16" 
                
set_main_node()
            
