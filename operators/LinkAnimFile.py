class LinkAnimFile(bpy.types.Operator):
     # Operator to link collections form anim file
    bl_idname = "object.link_coll_operator"
    bl_label = "Build Setup (WIP)"
    
    def execute(self, context):
        load_anim_lib()
        get_anim_blendfile()
        link_collections()
        
        report = "LGT File build done !"

        self.report({"INFO"}, f"{report}")
        return {"FINISHED"}