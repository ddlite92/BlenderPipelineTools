bl_info = {
    "name": "Monsta",
    "description": "Monsta Addon",
    "author": "Monsta",
    "version": (1, 0),
    "blender": (3, 3, 3),
    "category": "Render",
}

import bpy
import os
import sys
import ast
import addon_utils
import subprocess
from bpy.types import PropertyGroup, Scene, Panel, Operator, Space
from bpy.props import StringProperty, PointerProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from math import ceil
from os import path, listdir
from bpy.app.handlers import persistent
from bpy.utils import previews, register_class, unregister_class
from pathlib import Path

# --------------- render setup

# ---------------- render set path

def get_1st_lvl():
    filepath =  bpy.data.filepath
    full_path = os.path.dirname(filepath)
    print("full path: ", full_path)
    return(full_path)  

def get_workpath():
    #filepath = bpy.data.filepath
    blendpath = '\\'.join(filepath.split('\\')[7:8]) + '\\'
    print('blendpath: ', blendpath)
    return(blendpath)   

def get_shotname():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    print('new_basename: ', new_basename)
    return new_basename
        
def set_renderpath():
    final = os.path.join(get_1st_lvl())
    final = final.replace("2_Work", "3_Output")
    print('final: ', final)
    return(final)

def set_pr():
    filepath = bpy.data.filepath
    pr_path = '/'.join(filepath.split('/')[:8]) + '/'
    print(pr_path)
    return(pr_path)

'''
node naming t&C
node name = passes eg Beauty, AO, Depth, Emission, Matte,
node label = folder eg BG.Main, CH.Main, CH.Adudu
node doesnt have passes leave it as Node eg Node.001, Node.002, Node.003
'''
class OutputPath(bpy.types.Operator):
    # Operator to set path
    bl_idname =  "object.set_output_path"
    bl_label = "Set Output Path"
    
    def execute(self, context):
        scene = context.scene
        renderpath = set_renderpath()
        shotname = get_shotname()
        pr_folder = set_pr()
        owner = 'DD'
        prerender = 'PreRender'

        local_scenes = [s for s in bpy.data.scenes if not s.library]
        
        scenes = [s for s in local_scenes]
        for scn in scenes:
                scn.render.filepath = path.join(renderpath + '\\' + shotname + '_')
        
        output_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "OUTPUT_FILE"]
        for node in output_nodes:
            if "Matte" in node.name:
                pass_name = 'Matte'
                node_name = node.label.split("_")[0]
                node.base_path = os.path.join(renderpath + '\\' + node_name + '\\' + pass_name + '\\')
                node.format.file_format = "OPEN_EXR_MULTILAYER"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "32"
            
            elif "PR" in node.name:
                name = node.name.split("_")[1]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(pr_folder +  prerender )
                node.base_path = node_output
                node.file_slots[filename].path = shotname + '_' + owner + '_' + name + '_'
                node.format.file_format = "PNG"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "16"
            
            elif "Node" in node.name:
                folder = node.label
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + folder + '\\')
                node.base_path = node_output
                node.file_slots[filename].path = folder + '_'
                node.format.file_format = "PNG"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "16"
                                    
            else:
                folder = node.label.split("_")[0]
                pass_name = node.name.split(".")[0]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + folder +  '\\' + pass_name + '\\' )
                node.base_path = node_output
                node.file_slots[filename].path = os.path.join(folder + pass_name + '_')
                node.format.file_format = "PNG"
                node.format.color_depth = "16"
        
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set path done!")
        return {'FINISHED'}
    
# Property group for folder path
class BasePath(PropertyGroup):
    base_output_directory: StringProperty(
        name="Base Path",
        description="Path to the base output directory",
        default=""
    )

# Operator to open the folder picker
class SelectFolder(Operator):
    bl_idname = "wm.select_output_folder"
    bl_label = "Select Output Folder"
    directory: StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        context.scene.base_path_props.base_output_directory = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
                 
# ----------------- addon stuff

class PurgeSceneOperator(bpy.types.Operator):
     # Operator to perform purge functionality
    bl_idname = "object.purge_scene_operator"
    bl_label = "Purge Scene"

    def execute(self, context):
        scene = context.scene
        
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        # Execute the purge function
        # purge_orphans(local_ids, linked_ids, recursive)
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Orphan data purged successfully!")
        return {'FINISHED'}

class SetCamera(bpy.types.Operator):
    bl_idname =  "object.set_camera_global"
    bl_label = "Set & Export Cam_Frame"
    
    def execute(self, context):
        scenes = bpy.data.scenes
        global_camera = bpy.data.scenes["_RIM"].camera
        frame_start = bpy.data.scenes["_RIM"].frame_start
        frame_end = bpy.data.scenes["_RIM"].frame_end
        bpy.context.view_layer.objects.active = bpy.context.scene.camera
        
        for scn in bpy.data.scenes:
            scn.camera = global_camera
            scn.frame_start = frame_start
            scn.frame_end = frame_end
        
        # Define the export path (adjust as needed)
        directory = os.path.dirname(bpy.data.filepath)  
        file = os.path.join(directory, "cam.jsx")

        # Execute the export operator
        bpy.ops.export.jsx(filepath=file)

        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set and Export done!")
        return {'FINISHED'}

class NullOperator(bpy.types.Operator):
     # Operator to perform purge functionality
    bl_idname = "object.export_null_operator"
    bl_label = "Export Null"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        if not selected_objects:
            print("No objects selected.")
            return
    
        bpy.context.view_layer.objects.active = selected_objects[0]   
        directory = os.path.dirname(bpy.data.filepath)  
        file = os.path.join(directory, "null.jsx")

        try:
            # Execute the export operator
            bpy.ops.export.jsx(filepath=file)
            print(f"Exported JSX to: {filepath}")

        except Exception as e:
            print(f"Error during export: {e}")


        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Null Exported!")
        return {'FINISHED'}
               
# ----------------- PANEL

class MonstaPanel(bpy.types.Panel):
     # Displayy panel in 3D view
    bl_category = "Monsta"
    bl_label = "Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.base_path_props
        
        col = layout.column(align=True)
        col.operator("object.purge_scene_operator", icon="FILE_REFRESH")

        col = layout.column(align=True)
        col.operator("object.export_null_operator", icon="OUTLINER_OB_EMPTY")
        
        row = layout.row()
        row.label(text= "Render Tab")
        
        row = layout.row()
        row.label(text= "Setup")

        col = layout.column(align=True)
        col.operator("object.set_output_path", icon="FILEBROWSER")

        col = layout.column(align=True)
        col.operator("object.set_camera_global", icon="VIEW_CAMERA")
        
        row = layout.row()
        row.label(text= "Custom")

        row.prop(props, "base_output_directory")
        row.operator("wm.select_output_folder", text="", icon='FILE_FOLDER')
        

classes = (
        MonstaPanel,
        PurgeSceneOperator,
        OutputPath,
        SetCamera,
        NullOperator,
        SelectFolder,
        BasePath,
        )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.base_path_props = PointerProperty(type=BasePath)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.base_path_props


if __name__ == "__main__":
    register()