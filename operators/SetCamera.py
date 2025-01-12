import bpy
import os

class SetCamera(bpy.types.Operator):
    bl_idname =  "object.set_camera_global"
    bl_label = "Set & Export Cam_Frame"
    
    def execute(self, context):
        scenes = bpy.data.scenes
        global_camera = bpy.data.scenes["_RIM"].camera
        frame_start = bpy.data.scenes["_RIM"].frame_start
        frame_end = bpy.data.scenes["_RIM"].frame_end
        bpy.context.view_layer.objects.active = bpy.context.scene.camera
        
        for scn in bpy.data.scenes:
            scn.camera = global_camera
            scn.frame_start = frame_start
            scn.frame_end = frame_end
        
        # Define the export path (adjust as needed)
        directory = os.path.dirname(bpy.data.filepath)  
        file = os.path.join(directory, "cam.jsx")

        # Execute the export operator
        bpy.ops.export.jsx(filepath=file)

        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set and Export done!")
        return {'FINISHED'}