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