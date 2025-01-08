import bpy
import os
import sys
import ast
import addon_utils
import subprocess

from bpy.types import PropertyGroup, Scene, Panel, Operator, Space
from bpy.app.handlers import persistent
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty 
from bpy.utils import previews, register_class, unregister_class

from pathlib import Path
from re import findall, search
from math import ceil
from os import path, listdir, mkdir



def get_1st_lvl():
    filepath =  bpy.data.filepath
    full_path = os.path.dirname(filepath)
    print("full path: ", full_path)
    return(full_path)  

def get_workpath():
    filepath = bpy.data.filepath
    blendpath = '\\'.join(filepath.split('\\')[7:8]) + '\\'
    print('blendpath: ', blendpath)
    return(blendpath)   

def get_shotname():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    print('new_basename: ', new_basename)
    return new_basename
        
class OutputPath(bpy.types.Operator):
    # Operator to set path
    bl_idname =  "object.set_pr_path"
    bl_label = "Set PreRender Path"
    
    def execute(self, context):
        scene = context.scene
        workpath = get_workpath()
        shotname = get_shotname()
        owner = 'DD'

        local_scenes = [s for s in bpy.data.scenes if not s.library]

        prerender = 'prerender'.lower()
        
        scenes = [s for s in local_scenes]
        for scn in scenes:
                scn.render.filepath = path.join(workpath + '\\' + shotname + '_')
        
        output_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "OUTPUT_FILE"]

        for node in output_nodes:
            if "PR" in node.label:
                label_name = node.label
                #pass_name = node.label.split("_")[1]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(workpath + '\\' + prerender )
                node.base_path = node_output
                node.file_slots[filename].path = shotname + owner + '_' + label_name
                node.format.file_format = "PNG"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "16"