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
        ShowMessageBox("CAM Exported!")
        return {'FINISHED'}