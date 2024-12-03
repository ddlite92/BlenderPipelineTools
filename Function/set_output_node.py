import bpy
import os
import logging
from os import path
from pathlib import Path
context = bpy.context
filepath =  bpy.data.filepath

def get_1st_lvl():
    filepath =  bpy.data.filepath
    curr_folder = os.path.dirname(filepath)
    fifth_curr_folder = os.path.dirname(curr_folder)
    four_curr_folder = os.path.dirname(fifth_curr_folder)
    three_curr_folder = os.path.dirname(four_curr_folder)
    two_curr_folder = os.path.dirname(three_curr_folder)
    first_level = os.path.dirname(two_curr_folder)
    return(first_level)    

def get_workpath():
    #filepath = bpy.data.filepath
    #blendpath = '\\'.join(filepath.split('\\')[7:9]) + '\\'
    blendpath = '\\'.join(filepath.split('\\')[7:8]) + '\\'
    return(blendpath)   

def get_shotname():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    return new_basename

def get_folder():
    #filepath =  bpy.data.filepath
    curr_folder = os.path.dirname(filepath)
    return curr_folder
        
def set_renderpath():
    set_out = r"6_Post\3_Output\1_Render"
    #set_out = r"3_Output\1_Render"
    final = os.path.join(get_1st_lvl(), set_out, get_workpath(), get_shotname())
    return(final)

def set_main_node():
    scene = context.scene
    renderpath = set_renderpath()
    shotname = get_shotname()
    #bg_layer = scene.view_layers['_BG']   
    #main_sc = bpy.data.scenes.get("MAIN")

    local_scenes = [s for s in bpy.data.scenes if not s.library]
    
    scenes = [s for s in local_scenes]
    for scn in scenes:
            scn.render.filepath = path.join(renderpath + '\\' + shotname)
    
    output_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "OUTPUT_FILE"]
    for node in output_nodes:
        if "_Matte" in node.label:
            label_name = node.label.split("_Matte")[0]
            pass_name = 'Matte'
            splitOutput = os.path.join(renderpath + '\\' + shotname + '_')
            node.base_path = os.path.join(renderpath + '\\' + label_name + '\\' + pass_name + '\\')
            node.format.file_format = "OPEN_EXR_MULTILAYER"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "32"
        
        elif "_Emission" in node.label:
            label_name = node.label.split("_Emission")[0]
            pass_name = node.label.split("_")[1]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '\\' + label_name + '\\' + pass_name + '\\')
            node.base_path = node_output
            node.file_slots[filename].path = pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_mode = "RGB"
            node.format.color_depth = "16"
        
        elif "RIM_" in node.label:
            #label_name = node.label
            pass_name = node.label.split("_")[0]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '\\' + pass_name + '\\')
            node.base_path = node_output
            node.file_slots[filename].path = pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "16"
        
        elif "Lightray_" in node.label:
            #label_name = node.label
            pass_name = node.label.split("_")[0]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '\\' + pass_name + '\\')
            node.base_path = node_output
            node.file_slots[filename].path = pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_mode = "RGBA"
            node.format.color_depth = "16"
                                
        else:
            label_name = node.label.split(".")[1]
            label_name = node.label.split("_")[0]
            pass_name = node.label.split("_")[1]
            filename = node.file_slots.keys()[0]
            node_output = os.path.join(renderpath + '\\' + label_name + '\\' + pass_name + '\\')
            node.base_path = node_output
            node.file_slots[filename].path = pass_name + '_'
            node.format.file_format = "PNG"
            node.format.color_depth = "16" 
                

set_main_node()


'''

naming T&C :

main BG = BG.Main_## passes ##
        = BG.Main_Beauty

main CH = CH.Main_## passes ##
        = CH.Main_Beauty 

Lightray = Lightray_
RIM = RIM_

the rest accordingly .. eg :

inner BG = BG.Inner_Beauty
Gopal CH = CH.Gopal_Beauty
Lighray 2 = Lightray2_]

'''