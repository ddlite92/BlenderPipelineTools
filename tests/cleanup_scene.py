import bpy


def cleanup():
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    bg_collection = bpy.data.collections.get("BG")

    objects_to_remove = []

    for coll in bpy.data.collections:
        if coll == bg_collection:
            continue

        for obj in coll.all_objects:
            objects_to_remove.append(obj)

    for obj in objects_to_remove:
        if obj.instance_collection is not None:
            obj.instance_collection = None
        else:
            bpy.data.objects.remove(obj)

    for lib in bpy.data.libraries:
        if not lib.users:
            bpy.data.libraries.remove(lib)

'''
# preseve camera, light

for obj in scene.objects:
if obj.type not in ['CAMERA', 'LIGHT']:
scene.collection.objects.unlink(obj)
bpy.data.objects.remove(obj)

# remove in spesific collection

target_collection = bpy.data.collections['MyCollection']
for obj in target_collection.objects:
target_collection.objects.unlink(obj)
bpy.data.objects.remove(obj)


'''


