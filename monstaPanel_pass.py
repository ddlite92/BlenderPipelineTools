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
from math import ceil
from os import path, listdir
from bpy.app.handlers import persistent
from bpy.utils import previews, register_class, unregister_class
from pathlib import Path

context = bpy.context
filepath =  bpy.data.filepath

mainScreen = bpy.context.window
node_tree = bpy.context.scene.node_tree
#links = node_tree.links
# path = str(pathlib.Path().home() / "folder" / "file.blend")

# merge clean setup and build setup in 1 setup eg Clean and Build button

# --------------- render setup

def get_anim_blendfile():
    current_path = bpy.data.filepath
    anim_file_dir = os.path.dirname(current_path)
    for file in os.listdir(anim_file_dir) :
        if file.endswith("_ANIM.blend") : 
            anim_file = os.path.join(anim_file_dir, file)
            return anim_file

def load_anim_lib():
    anim_file = get_anim_blendfile()
    collset = {"CHAR", "PROP"} # "VHC", "CAM",

    with bpy.data.libraries.load(anim_file, link=True) as (data_from, data_to,):
        # data_to.objects = data_from.objects
        # data_to.collections = data_from.collections
        for collname in data_from.collections:
                if any(cname in collname for cname in collset):
                    data_to.collections.append(collname)

def create_instance(instance_name, parent_collection):
    null_object = bpy.data.objects.new(instance_name, None)
    linked_collection = bpy.data.collections.get(instance_name)

    if linked_collection:
        parent_collection.objects.link(null_object)
        null_object.instance_type = 'COLLECTION'
        null_object.instance_collection = linked_collection
    else:
        print(f"Collection '{instance_name}' not found in linked library.")

def link_collections():
    active_collection = bpy.context.view_layer.active_layer_collection.collection

    for coll in bpy.data.collections:
        if coll.library is not None:
            for target_name in ["CHAR", "PROP", "FX"]:
                if target_name in coll.name:
                    create_instance(coll.name, active_collection)

# ---------------- render set path

def get_1st_lvl():
    filepath =  bpy.data.filepath
    full_path = os.path.dirname(filepath)
    print("full path: ", full_path)
    return(full_path)  

get_1st_lvl()

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
    pr_path = '\\'.join(filepath.split('\\')[:15]) + '\\'
    print(pr_path)
    return(pr_path)

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
            if "_Matte" in node.label:
                pass_name = 'Matte'
                node_name = node.name
                node.base_path = os.path.join(renderpath + '\\' + node_name + '\\' + pass_name + '\\')
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
            
            elif "RIM" in node.label:
                #label_name = node.label
                pass_name = node.label.split("_")[0]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + pass_name + '\\')
                node.base_path = node_output
                node.file_slots[filename].path = pass_name + '_'
                node.format.file_format = "PNG"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "16"
            
            elif "Lightray" in node.label:
                #label_name = node.label
                pass_name = node.label.split("_")[0]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + pass_name + '\\')
                node.base_path = node_output
                node.file_slots[filename].path = pass_name + '_'
                node.format.file_format = "PNG"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "16"
            
            elif "PR" in node.name:
                name = node.name.split("_")[1]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(pr_folder +  prerender )
                node.base_path = node_output
                node.file_slots[filename].path = shotname + '_' + owner + '_' + name + '_'
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
                node.file_slots[filename].path = label_name + pass_name + '_'
                node.format.file_format = "PNG"
                node.format.color_depth = "16"
        
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set path done!")
        return {'FINISHED'}
            
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

class CleanOperator(bpy.types.Operator):
     # Operator to clean the collections
    bl_idname = "object.clean_coll_operator"
    bl_label = "Clean Setup (WIP)"
    
    def execute(self, context):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
           
        return {'FINISHED'}


class LinkAnimFile(bpy.types.Operator):
     # Operator to link collections form anim file
    bl_idname = "object.link_coll_operator"
    bl_label = "Build Setup (WIP)"
    
    def execute(self, context):
        load_anim_lib()
        get_anim_blendfile()
        link_collections()
        
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        # Execute the purge function
        # purge_orphans(local_ids, linked_ids, recursive)
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Orphan data purged successfully!")
        return {'FINISHED'}

class CleanOperator(bpy.types.Operator):
     # Operator to clean the collections
    bl_idname = "object.clean_coll_operator"
    bl_label = "Clean Setup (WIP)"
    
    def execute(self, context):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
           
        return {'FINISHED'}


class LinkAnimFile(bpy.types.Operator):
     # Operator to link collections form anim file
    bl_idname = "object.link_coll_operator"
    bl_label = "Build Setup (WIP)"
    
    def execute(self, context):
        load_anim_lib()
        get_anim_blendfile()
        link_collections()
       
        report = "LGT File build done !"

        self.report({"INFO"}, f"{report}")
        return {"FINISHED"}

class SetCamera(bpy.types.Operator):
    bl_idname =  "object.set_camera_global"
    bl_label = "Set Camera"
    
    def execute(self, context):
        scenes = bpy.data.scenes
        global_camera = bpy.data.scenes["_RIM"].camera
        frame_start = bpy.data.scenes["_RIM"].frame_start
        frame_end = bpy.data.scenes["_RIM"].frame_end
        
        for scn in bpy.data.scenes:
            scn.camera = global_camera
            scn.frame_start = frame_start
            scn.frame_end = frame_end

        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set camera done!")
        return {'FINISHED'}
    
class ExportCamOperator(bpy.types.Operator):
     # Operator to perform purge functionality
    bl_idname = "object.export_cam_operator"
    bl_label = "Export CAM"

    def execute(self, context):
        bpy.context.view_layer.objects.active = bpy.context.scene.camera

        # Define the export path (adjust as needed)
        directory = os.path.dirname(bpy.data.filepath)  
        file = os.path.join(directory, "cam.jsx")

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
        ShowMessageBox("CAM Exported!")
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
        
        col = layout.column(align=True)
        col.operator("object.purge_scene_operator", icon="FILE_REFRESH")

        col = layout.column(align=True)
        col.operator("object.export_cam_operator", icon="SPHERE")

        col = layout.column(align=True)
        col.operator("object.export_null_operator", icon="SPHERE")
        
        row = layout.row()
        row.label(text= "Render Tab")
        
        col = layout.column(align=True)
        col.operator("object.clean_coll_operator", icon="TRASH")
        
        col = layout.column(align=True)
        col.operator("object.link_coll_operator", icon="PREFERENCES")
        
        row = layout.row()
        row.label(text= "Setup")
        
        col = layout.column(align=True)
        col.operator("object.set_output_path", icon="FILEBROWSER")

        col = layout.column(align=True)
        col.operator("object.set_camera_global", icon="VIEW_CAMERA")
        
        row = layout.row()
        row.label(text= "Custom")
        

classes = (
        MonstaPanel,
        PurgeSceneOperator,
        CleanOperator,
        LinkAnimFile,
        OutputPath,
        SetCamera,
        ExportCamOperator,
        NullOperator,
        )

# register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
