class CleanOperator(bpy.types.Operator):
     # Operator to clean the collections
    bl_idname = "object.clean_coll_operator"
    bl_label = "Clean Setup (WIP)"
    
    def execute(self, context):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
           
        return {'FINISHED'}