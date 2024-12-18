class OutputPath(bpy.types.Operator):
    # Operator to set path
    bl_idname =  "object.set_output_path"
    bl_label = "Set Output Path"
    
    def execute(self, context):
        scene = context.scene
        renderpath = set_renderpath()
        shotname = get_shotname()

        local_scenes = [s for s in bpy.data.scenes if not s.library]
        
        scenes = [s for s in local_scenes]
        for scn in scenes:
                scn.render.filepath = path.join(renderpath + '\\' + shotname + '_')
        
        output_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "OUTPUT_FILE"]
        for node in output_nodes:
            if "_Matte" in node.label:
                pass_name = 'Matte'
                node_name = node.name
                node.base_path = os.path.join(renderpath + '\\' + node_name + '\\' + pass_name + '\\')
                node.format.file_format = "OPEN_EXR_MULTILAYER"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "32"
            
            elif "_Emission" in node.label:
                label_name = node.label.split("_Emission")[0]
                pass_name = node.label.split("_")[1]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + label_name + '\\' + pass_name + '\\')
                node.base_path = node_output
                node.file_slots[filename].path = pass_name + '_'
                node.format.file_format = "PNG"
                node.format.color_mode = "RGB"
                node.format.color_depth = "16"
            
            elif "RIM_" in node.label:
                #label_name = node.label
                pass_name = node.label.split("_")[0]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + pass_name + '\\')
                node.base_path = node_output
                node.file_slots[filename].path = pass_name + '_'
                node.format.file_format = "PNG"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "16"
            
            elif "Lightray_" in node.label:
                #label_name = node.label
                pass_name = node.label.split("_")[0]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + pass_name + '\\')
                node.base_path = node_output
                node.file_slots[filename].path = pass_name + '_'
                node.format.file_format = "PNG"
                node.format.color_mode = "RGBA"
                node.format.color_depth = "16"
                                    
            else:
                label_name = node.label.split(".")[1]
                label_name = node.label.split("_")[0]
                pass_name = node.label.split("_")[1]
                filename = node.file_slots.keys()[0]
                node_output = os.path.join(renderpath + '\\' + label_name + '\\' + pass_name + '\\')
                node.base_path = node_output
                node.file_slots[filename].path = label_name + pass_name + '_'
                node.format.file_format = "PNG"
                node.format.color_depth = "16"
        
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set path done!")
        return {'FINISHED'}