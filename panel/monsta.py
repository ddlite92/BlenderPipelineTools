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
        col.operator("object.purge_scene_operator", icon="FILE_REFRESH")
        
        row = layout.row()
        row.label(text= "Render Tab")
        
        col = layout.column(align=True)
        col.operator("object.clean_coll_operator", icon="TRASH")
        
        col = layout.column(align=True)
        col.operator("object.link_coll_operator", icon="PREFERENCES")
        
        col = layout.column(align=True)
        col.operator("object.set_output_path", icon="FILEBROWSER")

        col = layout.column(align=True)
        col.operator("object.set_camera_global", icon="VIEW_CAMERA")
        

classes = (
        MonstaPanel,
        PurgeSceneOperator,
        CleanOperator,
        LinkAnimFile,
        OutputPath,
        SetCamera,
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