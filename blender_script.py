import bpy
import os

def get_anim_blendfile():
    """
    Finds the animation blend file based on the current file's location.
    """

    current_path = bpy.data.filepath
    anim_file_dir = os.path.dirname(current_path)
    for file in os.listdir(anim_file_dir):
        if file.endswith("_ANIM.blend"):
            anim_file = os.path.join(anim_file_dir, file)
            return anim_file

def load_anim_lib():
    """
    Loads and links specific collections from the animation blend file.
    """

    anim_file = get_anim_blendfile()
    collset = {"CHAR", "PROP", "FX"}

    with bpy.data.libraries.load(anim_file, link=True) as (data_from, data_to):
        for collname in data_from.collections:
            if any(cname in collname for cname in collset):
                data_to.collections.append(collname)

def create_instance(instance_name, parent_collection):
    """
    Creates an empty object as an instance of the linked collection.
    """

    null_object = bpy.data.objects.new(instance_name, None)
    linked_collection = bpy.data.collections.get(instance_name)

    if linked_collection:
        parent_collection.objects.link(null_object)
        null_object.instance_type = 'COLLECTION'
        null_object.instance_collection = linked_collection
    else:
        print(f"Collection '{instance_name}' not found in linked library.")

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

def main():
    """
    Main entry point for linking collections.
    """

    load_anim_lib()
    link_collections()

if __name__ == "__main__":
    main()