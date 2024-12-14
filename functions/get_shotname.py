def get_shotname():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    print('new_basename: ', new_basename)
    return new_basename