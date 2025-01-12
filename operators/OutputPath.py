def get_1st_lvl():
    filepath =  bpy.data.filepath
    full_path = os.path.dirname(filepath)
    #print("full path: ", full_path)
    return(full_path)  

def get_workpath():
    #filepath = bpy.data.filepath
    if sys.platform.startswith("win32"): 
         blendpath = '\\'.join(filepath.split('\\')[7:8]) + '\\'
    else:
         blendpath = '/'.join(filepath.split('/')[7:8]) + '/'
    #print('blendpath: ', blendpath)
    return(blendpath)   

def get_shotname():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    #print('new_basename: ', new_basename)
    return new_basename
        
def set_renderpath():
    final = os.path.join(get_1st_lvl())
    final = final.replace("2_Work", "3_Output")
    #print('final: ', final)
    return(final)

def set_pr():
    filepath = bpy.data.filepath
    if sys.platform.startswith("win32"): 
         pr_path = '\\'.join(filepath.split('\\')[:8]) + '\\'
    else:
         pr_path = '/'.join(filepath.split('/')[:15]) + '/'
    #print(pr_path)
    return(pr_path)

'''
node naming t&C
node name = passes eg Beauty, AO, Depth, Emission, Matte,
node label = folder eg BG.Main, CH.Main, CH.Adudu, RIM, Lightray
node doesnt have passes leave it as Node eg Node.001, Node.002, Node.003
PR Node Name only : PR_BG , PR_CH
'''
class OutputPath(bpy.types.Operator):
    # Operator to set path
    bl_idname =  "object.set_output_path"
    bl_label = "Set Output Path"
    
    def execute(self, context):
        scene = bpy.context.scene
        renderpath = set_renderpath()
        shotname = get_shotname()
        pr_folder = set_pr()
        owner = 'DD'
        prerender = 'PreRender'

        local_scenes = [s for s in bpy.data.scenes if not s.library]

        scenes = [s for s in local_scenes]
        for scn in scenes:
                if sys.platform.startswith("win32"): 
                    scn.render.filepath = path.join(renderpath + '\\' + shotname + '_')
                else:
                    scn.render.filepath = path.join(renderpath + '/' + shotname + '_')

        output_nodes = [n for s in scenes for n in s.node_tree.nodes if n.type == "OUTPUT_FILE"]
        for node in output_nodes:
            node.format.file_format = "PNG"
            node.format.color_depth = "16"
            #node.format.color_mode = "RGBA"
            if sys.platform.startswith("win32"): # windows platform
                if "Matte" in node.name:
                    pass_name = 'Matte'
                    node_name = node.label.split("_")[0]
                    node.base_path = os.path.join(renderpath + '\\' + node_name + '\\' + pass_name + '\\')
                    node.format.file_format = "OPEN_EXR_MULTILAYER"
                    node.format.color_mode = "RGBA"
                    node.format.color_depth = "32"
                
                elif "PR" in node.name:
                    name = node.name.split("_")[1]
                    filename = node.file_slots.keys()[0]
                    node_output = os.path.join(pr_folder +  prerender )
                    node.base_path = node_output
                    node.file_slots[filename].path = shotname + '_' + owner + '_' + name + '_'
                
                elif "Node" in node.name:
                    folder = node.label
                    filename = node.file_slots.keys()[0]
                    node_output = os.path.join(renderpath + '\\' + folder + '\\')
                    node.base_path = node_output
                    node.file_slots[filename].path = folder + '_'
                                        
                else:
                    folder = node.label.split("_")[0]
                    pass_name = node.name.split(".")[0]
                    filename = node.file_slots.keys()[0]
                    node_output = os.path.join(renderpath + '\\' + folder +  '\\' + pass_name + '\\' )
                    node.base_path = node_output
                    node.file_slots[filename].path = os.path.join(folder + pass_name + '_')

            # linux, etc platform
            else:
                if "Matte" in node.name:
                    pass_name = 'Matte'
                    node_name = node.label.split("_")[0]
                    node.base_path = os.path.join(renderpath + '/' + node_name + '/' + pass_name + '/')
                    node.format.file_format = "OPEN_EXR_MULTILAYER"
                    node.format.color_mode = "RGBA"
                    node.format.color_depth = "32"
                
                elif "PR" in node.name:
                    name = node.name.split("_")[1]
                    filename = node.file_slots.keys()[0]
                    node_output = os.path.join(pr_folder +  prerender )
                    node.base_path = node_output
                    node.file_slots[filename].path = shotname + '_' + owner + '_' + name + '_'
                
                elif "Node" in node.name:
                    folder = node.label
                    filename = node.file_slots.keys()[0]
                    node_output = os.path.join(renderpath + '/' + folder + '/')
                    node.base_path = node_output
                    node.file_slots[filename].path = folder + '_'
                                                        
                else:
                    folder = node.label.split("_")[0]
                    pass_name = node.name.split(".")[0]
                    filename = node.file_slots.keys()[0]
                    node_output = os.path.join(renderpath + '/' + folder +  '/' + pass_name + '/' )
                    node.base_path = node_output
                    node.file_slots[filename].path = os.path.join(folder + pass_name + '_')
                    
        
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

                def draw(self, context):
                    self.layout.label(text=message)

                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon) 
        ShowMessageBox("Set path done!")
        return {'FINISHED'}