class SetCamera(bpy.types.Operator):
    bl_idname =  "object.set_camera_global"
    bl_label = "Set Camera"
    
    def execute(self, context):
        scenes = bpy.data.scenes
        global_camera = bpy.data.scenes["_RIM"].camera
        for scn in bpy.data.scenes:
            scn.camera = global_camera

        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set camera done!")
        return {'FINISHED'}