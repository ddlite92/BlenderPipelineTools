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