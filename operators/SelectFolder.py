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