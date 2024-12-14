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