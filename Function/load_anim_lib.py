import bpy

def load_anim_lib():
    anim_file = get_anim_blendfile()
    collset = {"CHAR", "PROP"} # "VHC", "CAM",

    with bpy.data.libraries.load(anim_file, link=True) as (data_from, data_to,):
        # data_to.objects = data_from.objects
        # data_to.collections = data_from.collections
        for collname in data_from.collections:
                if any(cname in collname for cname in collset):
                    data_to.collections.append(collname)