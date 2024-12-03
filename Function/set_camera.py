import bpy



def set_camera():
    scenes = bpy.data.scenes
    global_camera = bpy.data.scenes["BG"].camera
    for scn in bpy.data.scenes:
        scn.camera = global_camera
                
                                
set_camera()