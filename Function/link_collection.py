import bpy

# in progress link function

def link_coll():
    anim_file = get_anim_blendfile()
    # master_collection = bpy.context.scene.collection
    master_collection = bpy.data.collections['MAIN']

    with bpy.data.libraries.load(anim_file) as (data_from, data_to):
        data_to.collections = data_from.collections


    for new_coll in data_to.collections:
        instance = bpy.data.objects.new(new_coll.name, None)
        instance.instance_type = 'COLLECTION'
        instance.instance_collection = new_coll
        master_collection.objects.link(instance)


"""
def create_instance(instance_name, parent_coll):

    null = bpy.data.objects.new(instance_name, None)

    linked_col = bpy.data.collections.get(instance_name)

    parent_coll.objects.link(null)
    null.instance_type = "COLLECTION"
    null.instance_collection = linked_col

def create_link_to_scene(coll_name, parent_coll):
    return parent_coll.children.link(bpy.data.collections[coll_name])

def create_ob_link_to_scene(coll_name, parent_coll):
    return parent_coll.objects.link(bpy.data.objects.get(coll_name))

def link_coll():
    CHAR = bpy.data.collections.get("CHAR")
    PROP = bpy.data.collections.get("PROP")
    
    for coll in bpy.data.collections:
        try:
            if "CHAR" in coll.name and coll.library is not None:
                create_instance(coll.name, CHAR)
                create_link_to_scene(coll.name, CHAR)
                create_ob_link_to_scene(coll.name, CHAR)
            elif coll.name == "PROP" and coll.library is not None:
                create_instance(coll.name, PROP)
                create_link_to_scene(coll.name, PROP)
                create_ob_link_to_scene(coll.name, PROP)
                
        except RuntimeError:
            pass

"""