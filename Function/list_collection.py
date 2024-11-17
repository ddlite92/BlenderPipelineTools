import bpy

def traverse_tree(t):
    yield t
    for child in t.children:
        yield from traverse_tree(child)


def list_collections(context):
    scene_colls = context.scene.collection

    # Get names of collections and sort them
    collections = [c for c in traverse_tree(scene_colls)]
    collection_names = [c.name for c in traverse_tree(scene_colls)]
    collection_names = sorted(collection_names)

    # Get Collections from Collection names, but still sorted.
    collections = []
    for c in collection_names:
        # Ignore 'Master Collection' or 'Scene Collection' (Blender 3.0), adding it as scene.collection)
        if c not in {"Master Collection", "Scene Collection"}:
            collections.append(bpy.data.collections[c])
        else:
            collections.append(context.scene.collection)
    return collections