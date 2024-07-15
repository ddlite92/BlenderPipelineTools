bl_info = {
    "name": "Monsta",
    "description": "Monsta Addon",
    "author": "Monsta",
    "version": (1, 0),
    "blender": (3, 3, 3),
    # "location": "View3D > Add > Mesh > New Object",
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

class SamplePanel(bpy.types.Panel):
    """ Displayy panel in 3D view"""
    bl_label = "Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("object.purge_scene_operator", icon="MESH_CUBE")

classes = (
        SamplePanel,
        PurgeSceneOperator,
        )

def register():
    bpy.utils.register_class(SamplePanel)
    bpy.utils.register_class(PurgeSceneOperator)
    # bpy.utils.register_class(msgBox)


def unregister():
    bpy.utils.unregister_class(SamplePanel)
    bpy.utils.register_class(PurgeSceneOperator)
    # bpy.utils.register_class(msgBox)


if __name__ == "__main__":
    register()
