import bpy

def cleanup():
    main_scn = bpy.data.scenes["Scene"]
    out_layer = main_scn.view_layers["View Layer"]
    layer_coll = out_layer.layer_collection.collection
    objects_to_unlink = [ o for o in layer_coll.all_objects if o.type == "EMPTY" and o.is_instancer]
    
    for obj in objects_to_unlink:
        bpy.data.objects.remove(obj)
    
    for coll in bpy.data.collections:
        if coll.library is not None:
            bpy.data.collections.remove(coll)
            
    for lib in bpy.data.libraries:
        bpy.data.libraries.remove(lib)