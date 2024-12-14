def get_workpath():
    #filepath = bpy.data.filepath
    blendpath = '\\'.join(filepath.split('\\')[7:8]) + '\\'
    print('blendpath: ', blendpath)
    return(blendpath)  