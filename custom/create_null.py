## create null on selected object and export

import bpy

def create_empty_null_on_selected_objects():

    selected_objects = bpy.context.selected_objects

    for obj in selected_objects:
        empty_null.location = obj.location
        empty_null = bpy.data.objects.new(obj.name + "_Null", None)
        empty_null.empty_display_type = 'PLAIN_AXES'
        empty_null.parent = objfgvc
        bpy.context.collection.objects.link(empty_null)
        empty_null.matrix_local = obj.matrix_local.copy()
        #empty_null.matrix_world = obj.matrix_parent_inverse

# Run the script
create_empty_null_on_selected_objects()