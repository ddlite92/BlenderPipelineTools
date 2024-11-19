import bpy

# in progress link function

def link_collections():
    """
    Links collections from the animation blend file to the active collection.
    """

    active_collection = bpy.context.view_layer.active_layer_collection.collection

    for coll in bpy.data.collections:
        if coll.library is not None:
            for target_name in ["CHAR", "PROP", "FX"]:
                if target_name in coll.name:
                    create_instance(coll.name, active_collection)