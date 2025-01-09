bl_info = {
    "name": "BBBGS2_OutputRenamer",
    "blender": (3, 3, 19),
    "category": "3D View",
    "version": (1, 0),
    "author": "Animonsta_BBBGS2",
    "description": "Setup Render For Beauty And Auto Rename all path",
}

import bpy
from bpy.props import StringProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup
from pathlib import Path

# Helper functions
def get_file_name_without_extension(filepath):
    file_name = Path(filepath).stem
    if file_name.endswith("_RENDER"):
        file_name = file_name[:-len("_RENDER")]
    return file_name

def create_output_directories(base_output_directory, blender_file_name, scene_name):
    scene_directory = base_output_directory / blender_file_name / scene_name
    scene_directory.mkdir(parents=True, exist_ok=True)
    return scene_directory

def set_node_output_paths(scene, scene_directory, file_name_without_extension):
    nodes = scene.node_tree.nodes
    for node in nodes:
        if node.type == 'OUTPUT_FILE':
            # Ensure Cryptomatte files are saved into the correct Cryptomatte folder
            if "Cryptomatte" in node.label:
                output_directory = scene_directory / "Cryptomatte_"
                output_directory.mkdir(parents=True, exist_ok=True)
                node.base_path = str(output_directory)
                node.file_slots[0].path = file_name_without_extension + "_Cryptomatte_"
            elif node.label in {'Depth', 'Emit', 'AO'}:
                output_directory = scene_directory / node.label
                output_directory.mkdir(parents=True, exist_ok=True)
                node.base_path = str(output_directory)
                node.file_slots[0].path = file_name_without_extension + "_"
            else:
                output_directory = scene_directory / node.label
                output_directory.mkdir(parents=True, exist_ok=True)
                node.base_path = str(output_directory)
                node.file_slots[0].path = node.label + "_"
            print(f"Final output path for '{node.name}' in scene '{scene.name}': {output_directory / file_name_without_extension}")


def set_output_properties_path(scene, scene_directory, file_name_without_extension):
    output_directory = scene_directory / "Beauty"
    output_directory.mkdir(parents=True, exist_ok=True)
    
    scene.render.filepath = str(output_directory / file_name_without_extension) + "_"
    print(f"Render output path set to: {scene.render.filepath}")

def main(base_output_directory):
    file_name_without_extension = get_file_name_without_extension(bpy.data.filepath)
    blender_file_name = get_file_name_without_extension(bpy.data.filepath)
    scene_names = [scene.name for scene in bpy.data.scenes]

    for scene_name in scene_names:
        scene = bpy.data.scenes.get(scene_name)
        if scene:
            # Set node output paths
            scene_directory = create_output_directories(base_output_directory, blender_file_name, scene_name)
            set_node_output_paths(scene, scene_directory, file_name_without_extension)
            
            # Ensure Cryptomatte output is redirected to the correct folder
            ensure_cryptomatte_output(scene_directory, file_name_without_extension)

            # Update output properties path for Beauty pass
            set_output_properties_path(scene, scene_directory, file_name_without_extension)

# Property group for folder path
class OutputRenamerProperties(PropertyGroup):
    base_output_directory: StringProperty(
        name="Base Output Directory",
        description="Path to the base output directory",
        default=""
    )

# Operator to open the folder picker
class OT_SelectFolder(Operator):
    bl_idname = "wm.select_output_folder"
    bl_label = "Select Output Folder"
    directory: StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        context.scene.output_renamer_props.base_output_directory = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# UI panel
class PT_OutputRenamerPanel(Panel):
    bl_label = "Output Renamer"
    bl_idname = "VIEW3D_PT_output_renamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Monsta_BBB"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.output_renamer_props

        layout.prop(props, "base_output_directory")
        layout.operator("wm.select_output_folder", text="Select Folder", icon='FILE_FOLDER')
        layout.operator("wm.run_output_renamer", text="Run Output Renamer", icon='PLAY')

# Registering all classes
def register():
    bpy.utils.register_class(OutputRenamerProperties)
    bpy.utils.register_class(OT_SelectFolder)
    bpy.utils.register_class(PT_OutputRenamerPanel)
    bpy.types.Scene.output_renamer_props = PointerProperty(type=OutputRenamerProperties)

def unregister():
    bpy.utils.unregister_class(OutputRenamerProperties)
    bpy.utils.unregister_class(OT_SelectFolder)
    bpy.utils.unregister_class(PT_OutputRenamerPanel)
    del bpy.types.Scene.output_renamer_props

if __name__ == "__main__":
    register()
