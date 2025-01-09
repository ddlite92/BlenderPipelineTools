bl_info = {
    "name": "BBBGS2_RenderSetUp",
    "blender": (3, 3, 19),
    "category": "3D View",
    "version": (1, 0),
    "author": "Animonsta_BBBGS2",
    "description": "Combine Render Setting, Render Output Setup, Append Asset",
}

import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty, PointerProperty



# Append Assets
class AppendAssetsProperties(PropertyGroup):
    blend_file_path: StringProperty(
        name="Blend File Path",
        default="",
        description="Path to the .blend file to append assets from"
    )
    collection_name: StringProperty(
        name="Collection Name",
        default="LIGHTING",
        description="Name of the collection to append"
    )
    world_names: StringProperty(
        name="World Names",
        default="World.BG,World.RIM,World.CHAR",
        description="Comma-separated list of world names to append"
    )
    material_names: StringProperty(
        name="Material Names",
        default="Fresnel",
        description="Comma-separated list of material names to append"
    )

class OpenBlendFileBrowser(Operator):
    bl_idname = "wm.open_blend_file_browser"
    bl_label = "Open Blend File Browser"
    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        context.scene.append_assets_properties.blend_file_path = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class AppendAssetsOperator(Operator):
    bl_idname = "wm.append_assets"
    bl_label = "Append Assets"

    def execute(self, context):
        props = context.scene.append_assets_properties
        blend_file_path = props.blend_file_path
        collection_name = props.collection_name
        world_names = props.world_names.split(',')
        material_names = props.material_names.split(',')

        # Append the collection
        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            if collection_name in data_from.collections:
                data_to.collections = [collection_name]
            else:
                self.report({'WARNING'}, f"Collection '{collection_name}' not found in the .blend file.")
                return {'CANCELLED'}

        if collection_name in bpy.data.collections:
            bpy.context.scene.collection.children.link(bpy.data.collections[collection_name])
        else:
            self.report({'WARNING'}, f"Collection '{collection_name}' could not be linked.")
            return {'CANCELLED'}

        # Append worlds
        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            for world_name in world_names:
                if world_name in data_from.worlds:
                    data_to.worlds.append(world_name)
                else:
                    self.report({'WARNING'}, f"World '{world_name}' not found in the .blend file.")

        # Confirm worlds were appended
        for world_name in world_names:
            if world_name in bpy.data.worlds:
                print(f"World '{world_name}' appended successfully.")
            else:
                self.report({'WARNING'}, f"World '{world_name}' not appended.")

        # Append materials
        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            for material_name in material_names:
                if material_name in data_from.materials:
                    data_to.materials.append(material_name)
                else:
                    self.report({'WARNING'}, f"Material '{material_name}' not found in the .blend file.")

        for material_name in material_names:
            if material_name in bpy.data.materials:
                print(f"Material '{material_name}' appended successfully.")
            else:
                self.report({'WARNING'}, f"Material '{material_name}' not appended.")

        return {'FINISHED'}

class AppendAssetsPanel(Panel):
    bl_label = "Append From Benchmark"
    bl_idname = "VIEW3D_PT_append_assets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Monsta_BBB"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.append_assets_properties

        row = layout.row()
        row.prop(props, "blend_file_path", text="")
        row.operator("wm.open_blend_file_browser", text="", icon='FILE_FOLDER')

        layout.prop(props, "collection_name")
        layout.prop(props, "world_names")
        layout.prop(props, "material_names")
        layout.operator("wm.append_assets")


class SetupRenderOutputOperator(bpy.types.Operator):
    bl_idname = "render.setup_output"
    bl_label = "Setup Render Output"

    def execute(self, context):
        setup_render_output()
        return {'FINISHED'}

class SetupRenderOutputPanel(bpy.types.Panel):
    bl_label = "Setup Output"
    bl_idname = "RENDER_PT_setup_output_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Monsta_BBB"

    def draw(self, context):
        layout = self.layout
        layout.operator("render.setup_output")

# Register classes
classes = [
    AppendAssetsProperties,
    OpenBlendFileBrowser,
    AppendAssetsOperator,
    AppendAssetsPanel,
    SetupRenderOutputOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.append_assets_properties = PointerProperty(type=AppendAssetsProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.append_assets_properties

if __name__ == "__main__":
    register()
