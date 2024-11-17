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


# path = str(pathlib.Path().home() / "folder" / "file.blend")

def get_anim_blendfile():
    current_path = bpy.data.filepath
    anim_file_dir = os.path.dirname(current_path)
    for file in os.listdir(anim_file_dir) :
        if file.endswith("_ANIM.blend") : 
            anim_file = os.path.join(anim_file_dir, file)
            return anim_file
    
def link_coll():
    anim_file = get_anim_blendfile()
    # master_collection = bpy.context.scene.collection
    master_collection = bpy.data.collections['MAIN']

    with bpy.data.libraries.load(anim_file) as (data_from, data_to):
        data_to.collections = data_from.collections


    for new_coll in data_to.collections:
        instance = bpy.data.objects.new(new_coll.name, None)
        instance.instance_type = 'COLLECTION'
        instance.instance_collection = new_coll
        master_collection.objects.link(instance)

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
    bl_label = "Clean Setup"
    
    def execute(self, context):
        main_scn = bpy.data.scenes["Scene"]
        out_layer = main_scn.view_layers["View Layer"]
        layer_coll = out_layer.layer_collection.collection
        
        objects_to_unlink = [ o for o in layer_coll.all_objects if o.type == "EMPTY" and o.is_instancer]
        
        for obj in objects_to_unlink:
            bpy.data.objects.remove(obj)
        
        for coll in bpy.data.collections:
            if coll.library is not None:
                bpy.data.collections.remove(coll)
                
        for lib in bpy.data.libraries:
            bpy.data.libraries.remove(lib)
           
        return {'FINISHED'}


class LinkAnimFile(bpy.types.Operator):
     # Operator to link collections form anim file
    bl_idname = "object.link_coll_operator"
    bl_label = "Build Setup"
    
    def execute(self, context):
        get_anim_blendfile()
        link_coll()
        
        report = "LGT File build done !"

        self.report({"INFO"}, f"{report}")
        return {"FINISHED"}
       
        
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
        col.operator("object.purge_scene_operator", icon="MESH_CUBE")
        
        row = layout.row()
        row.label(text= "Render Tab")
        
        col = layout.column(align=True)
        col.operator("object.clean_coll_operator", icon="MESH_CUBE")
        
        col = layout.column(align=True)
        col.operator("object.link_coll_operator", icon="MESH_CUBE")
        

classes = (
        MonstaPanel,
        PurgeSceneOperator,
        CleanOperator,
        LinkAnimFile,
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