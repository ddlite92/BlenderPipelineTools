def get_1st_lvl():
    filepath =  bpy.data.filepath
    full_path = os.path.dirname(filepath)
    print("full path: ", full_path)
    return(full_path)  