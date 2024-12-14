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

# First Script: Render Settings
class RENDER_OT_Setup(bpy.types.Operator):
    bl_idname = "render.setup"
    bl_label = "Render Settings"
    bl_description = "Setup render settings"

    def execute(self, context):
        scene = context.scene
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'
        scene.cycles.use_adaptive_sampling = True
        scene.cycles.samples = 256
        scene.cycles.preview_samples = 256
        scene.cycles.preview_denoising = 'OPTIX'
        scene.cycles.adaptive_threshold = 0.0005
        scene.cycles.use_adaptive_sampling = True
        scene.cycles.max_bounces = 32
        scene.cycles.diffuse_bounces = 32
        scene.cycles.glossy_bounces = 4
        scene.cycles.transparent_max_bounces = 16
        scene.cycles.transmission_bounces = 4
        scene.world.light_settings.distance = 2
        scene.cycles.blur_glossy = 10
        scene.render.use_stamp_note = False
        scene.render.use_stamp = False
        scene.render.use_stamp_camera = False
        scene.render.film_transparent = True
        scene.render.use_persistent_data = True
        scene.view_settings.look = 'Medium High Contrast'
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.cycles.texture_limit = '1024'
        scene.cycles.texture_limit_render = '4096'
        scene.cycles.denoiser = 'OPTIX'
        scene.cycles.preview_denoiser = 'OPTIX'
        scene.render.use_file_extension = True
        scene.render.use_simplify = True
        scene.render.simplify_subdivision = 0
        scene.render.simplify_subdivision_render = 6
        scene.cycles.denoising_input_passes = 'RGB_ALBEDO'
        scene.cycles.use_denoising = False
        scene.cycles.use_preview_adaptive_sampling = True
        scene.view_layers["ViewLayer"].use_pass_z = True
        scene.view_layers["ViewLayer"].use_pass_cryptomatte_asset = True
        scene.view_layers["ViewLayer"].use_pass_cryptomatte_material = True
        scene.view_layers["ViewLayer"].use_pass_cryptomatte_object = True
        scene.view_layers["ViewLayer"].use_pass_emit = True
        scene.view_layers["ViewLayer"].use_pass_ambient_occlusion = True
        scene.view_layers["ViewLayer"].cycles.use_denoising = True
        scene.cycles.use_preview_denoising = True
        scene.render.image_settings.color_depth = '16'

        return {'FINISHED'}

class RENDER_PT_SetupPanel(bpy.types.Panel):
    bl_label = "Render Settings"
    bl_idname = "RENDER_PT_setup_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Monsta_BBB"

    def draw(self, context):
        layout = self.layout
        layout.operator("render.setup")

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

# Function to set up render output and compositing nodes
def setup_render_output():
    # Set the render engine to Cycles
    bpy.context.scene.render.engine = 'CYCLES'

    # Enable use nodes in the compositing
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    existing_nodes = {node.name: node for node in tree.nodes}

    if 'Render Layers' not in existing_nodes:
        render_layers = tree.nodes.new('CompositorNodeRLayers')
    else:
        render_layers = existing_nodes['Render Layers']
    render_layers.location = 0, 0

    view_layer = bpy.context.view_layer
    view_layer.use_pass_z = True
    view_layer.use_pass_cryptomatte_asset = True
    view_layer.use_pass_cryptomatte_material = True
    view_layer.use_pass_cryptomatte_object = True
    view_layer.use_pass_emit = True
    view_layer.use_pass_ambient_occlusion = True
    view_layer.cycles.denoising_store_passes = True
    view_layer.cycles.use_denoising = True

    def ensure_link(output_socket, input_socket):
        # Check if a link already exists between the sockets
        for link in output_socket.links:
            if link.to_socket == input_socket:
                return
        # If no link exists, create a new link
        tree.links.new(output_socket, input_socket)

    # 1 - BEAUTY PASS
    if 'Composite' not in existing_nodes:
        composite = tree.nodes.new('CompositorNodeComposite')
    else:
        composite = existing_nodes['Composite']
    composite.location = 700, 100

    if 'Denoise Beauty' not in existing_nodes:
        denoise_node1 = tree.nodes.new('CompositorNodeDenoise')
        denoise_node1.name = 'Denoise Beauty'
    else:
        denoise_node1 = existing_nodes['Denoise Beauty']
    denoise_node1.location = 500, 100
    denoise_node1.hide = False

    ensure_link(render_layers.outputs['Image'], denoise_node1.inputs['Image'])
    ensure_link(denoise_node1.outputs['Image'], composite.inputs['Image'])
    ensure_link(render_layers.outputs['Denoising Normal'], denoise_node1.inputs['Normal'])
    ensure_link(render_layers.outputs['Denoising Albedo'], denoise_node1.inputs['Albedo'])

    # 2 - DEPTH PASS
    if 'Map Range' not in existing_nodes:
        map_range_node = tree.nodes.new('CompositorNodeMapRange')
    else:
        map_range_node = existing_nodes['Map Range']
    map_range_node.location = 500, -120
    map_range_node.inputs['From Max'].default_value = 100

    if 'Denoise Depth' not in existing_nodes:
        denoise_node2 = tree.nodes.new('CompositorNodeDenoise')
        denoise_node2.name = 'Denoise Depth'
    else:
        denoise_node2 = existing_nodes['Denoise Depth']
    denoise_node2.location = 700, -120
    denoise_node2.hide = False

    if 'DepthOutput' not in existing_nodes:
        output_node2 = tree.nodes.new('CompositorNodeOutputFile')
        output_node2.name = 'DepthOutput'
        output_node2.label = 'Depth'
    else:
        output_node2 = existing_nodes['DepthOutput']
    output_node2.location = 900, -150
    output_node2.format.file_format = 'PNG'
    output_node2.format.color_mode = 'RGBA'
    output_node2.format.color_depth = '16'
    output_node2.base_path = 'M:/BBBGS2_Gentar_Arc/2_Episode'
    output_node2.file_slots[0].path = 'Depth_'

    ensure_link(render_layers.outputs['Depth'], map_range_node.inputs['Value'])
    ensure_link(map_range_node.outputs['Value'], denoise_node2.inputs['Image'])
    ensure_link(denoise_node2.outputs['Image'], output_node2.inputs['Image'])

    # 3 - EMISSION PASS
    if 'EmitOutput' not in existing_nodes:
        output_node3 = tree.nodes.new('CompositorNodeOutputFile')
        output_node3.name = 'EmitOutput'
        output_node3.label = 'Emit'
    else:
        output_node3 = existing_nodes['EmitOutput']
    output_node3.location = 900, -300
    output_node3.format.file_format = 'PNG'
    output_node3.format.color_mode = 'RGBA'
    output_node3.format.color_depth = '16'
    output_node3.base_path = 'M:/BBBGS2_Gentar_Arc/2_Episode'
    output_node3.file_slots[0].path = 'Emission_'

    ensure_link(render_layers.outputs['Emit'], output_node3.inputs['Image'])

    # 4 - AO PASS
    if 'Denoise AO' not in existing_nodes:
        denoise_node4 = tree.nodes.new('CompositorNodeDenoise')
        denoise_node4.name = 'Denoise AO'
    else:
        denoise_node4 = existing_nodes['Denoise AO']
    denoise_node4.location = 500, -350
    denoise_node4.hide = False

    if 'AOOutput' not in existing_nodes:
        output_node4 = tree.nodes.new('CompositorNodeOutputFile')
        output_node4.name = 'AOOutput'
        output_node4.label = 'AO'
    else:
        output_node4 = existing_nodes['AOOutput']
    output_node4.location = 900, -450
    output_node4.format.file_format = 'PNG'
    output_node4.format.color_mode = 'RGBA'
    output_node4.format.color_depth = '16'
    output_node4.base_path = 'M:/BBBGS2_Gentar_Arc/2_Episode'
    output_node4.file_slots[0].path = 'AO_'

    ensure_link(render_layers.outputs['AO'], denoise_node4.inputs['Image'])
    ensure_link(denoise_node4.outputs['Image'], output_node4.inputs['Image'])

    # 5 - CRYPTOMATTE PASS
    if 'MatteOutput' not in existing_nodes:
        output_node5 = tree.nodes.new('CompositorNodeOutputFile')
        output_node5.name = 'MatteOutput'
        output_node5.label = 'Cryptomatte'
    else:
        output_node5 = existing_nodes['MatteOutput']
    output_node5.location = 900, -600
    output_node5.use_custom_color = True
    output_node5.color = (1, 0.343274, 0.407046)
    output_node5.format.file_format = 'OPEN_EXR_MULTILAYER'
    output_node5.format.color_mode = 'RGBA'
    output_node5.format.color_depth = '32'
    output_node5.format.exr_codec = 'ZIPS'
    output_node5.base_path = 'M:/BBBGS2_Gentar_Arc/2_Episode'

    desired_slots = ['CryptoObject00', 'CryptoObject01', 'CryptoObject02','CryptoMaterial00', 'CryptoMaterial01', 'CryptoMaterial02', 'CryptoAsset00', 'CryptoAsset01', 'CryptoAsset02']
    existing_slots = {slot.path for slot in output_node5.file_slots}

    for slot_name in desired_slots:
        if slot_name not in existing_slots:
            output_node5.file_slots.new(slot_name)

    cryptomatte_outputs = [
        ('CryptoObject00', 'CryptoObject00'),
        ('CryptoObject01', 'CryptoObject01'),
        ('CryptoObject02', 'CryptoObject02'),
        ('CryptoAsset00', 'CryptoAsset00'),
        ('CryptoAsset01', 'CryptoAsset01'),
        ('CryptoAsset02', 'CryptoAsset02'),
        ('CryptoMaterial00', 'CryptoMaterial00'),
        ('CryptoMaterial01', 'CryptoMaterial01'),
        ('CryptoMaterial02', 'CryptoMaterial02')
    ]

    for output_name, slot_name in cryptomatte_outputs:
        if output_name in render_layers.outputs and slot_name in output_node5.inputs:
            ensure_link(render_layers.outputs[output_name], output_node5.inputs[slot_name])
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
    RENDER_OT_Setup,
    RENDER_PT_SetupPanel,
    AppendAssetsProperties,
    OpenBlendFileBrowser,
    AppendAssetsOperator,
    AppendAssetsPanel,
    SetupRenderOutputOperator,
    SetupRenderOutputPanel
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
