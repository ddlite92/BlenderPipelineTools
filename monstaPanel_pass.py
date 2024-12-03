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

path = r"M:\BBBGS2_Gentar_Arc\2_Episode\Episode_15\6_Post\3_Output\1_Render\PART B\_MONSTA"

filepath = bpy.data.filepath

mainScreen = bpy.context.window
node_tree = bpy.context.scene.node_tree
#links = node_tree.links
# path = str(pathlib.Path().home() / "folder" / "file.blend")

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
        
        report = "LGT File build done !"

        self.report({"INFO"}, f"{report}")
        return {"FINISHED"}

class SetCamera(bpy.types.Operator):
    bl_idname =  "object.set_camera_global"
    bl_label = "Set Camera"
    
    def execute(self, context):
        scenes = bpy.data.scenes
        global_camera = bpy.data.scenes["BG"].camera
        for scn in bpy.data.scenes:
            scn.camera = global_camera

        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set camera done!")
        return {'FINISHED'}

class OutputPath(bpy.types.Operator):
    # Operator to set path
    bl_idname =  "object.set_output_path"
    bl_label = "Set Output Path (WIP)"
    
    def execute(self, context):
        output_node()
        
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set path done!")
        return {'FINISHED'}
       
        
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
        
        row = layout.row()
        row.label(text= "Render Tab")
        
        col = layout.column(align=True)
        col.operator("object.clean_coll_operator", icon="TRASH")
        
        col = layout.column(align=True)
        col.operator("object.link_coll_operator", icon="PREFERENCES")
        
        col = layout.column(align=True)
        col.operator("object.set_output_path", icon="FILEBROWSER")

        col = layout.column(align=True)
        col.operator("object.set_camera_global", icon="VIEW_CAMERA")
        

classes = (
        MonstaPanel,
        PurgeSceneOperator,
        CleanOperator,
        LinkAnimFile,
        OutputPath,
        SetCamera,
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