class SetCamera(bpy.types.Operator):
    bl_idname =  "object.set_camera_global"
    bl_label = "Set Camera"
    
    def execute(self, context):
        '''
        Set camera from _RIM scene and set frame from data extracted from the camera
        '''
        scenes = bpy.data.scenes
        global_camera = bpy.data.scenes["_RIM"].camera
        frame_start = bpy.data.scenes["_RIM"].frame_start
        frame_end = bpy.data.scenes["_RIM"].frame_end

        for scn in bpy.data.scenes:
            scn.camera = global_camera
            scn.frame_start = frame_start
            scn.frame_end = frame_end

        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set camera done!")
        return {'FINISHED'}