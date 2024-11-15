bl_info = {
    "name": "Monsta",
    "description": "Monsta Addon",
    "author": "Monsta",
    "version": (1, 0),
    "blender": (3, 3, 3),
    "category": "Render",
}

import bpy

class PurgeSceneOperator(bpy.types.Operator):
    """Operator to perform purge functionality"""
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

class MonstaPanel(bpy.types.Panel):
    """ Displayy panel in 3D view"""
    bl_category = "Monsta"
    bl_label = "Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("object.purge_scene_operator", icon="MESH_CUBE")

classes = (
        MonstaPanel,
        PurgeSceneOperator,
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
