import bpy
import os
import logging
from os import path
from pathlib import Path


path = r"M:\BBBGS2_Gentar_Arc\2_Episode\Episode_15\6_Post\3_Output\1_Render\PART B\_MONSTA"

mainScreen = bpy.context.window
node_tree = bpy.context.scene.node_tree
world_node = bpy.context.scene.world.node_tree

bg_startFrame = bpy.data.scenes["BG"].frame_start
bg_endFrame = bpy.data.scenes["BG"].frame_end
bg_currentFrame = bpy.data.scenes["BG"].frame_current
bg_cam = bpy.data.scenes["BG"].camera

filepath = bpy.data.filepath
print("filepath is: ", filepath)

def _get_finaling_file(filepath):
    dirpath = os.path.dirname(filepath)
    lgtpath = os.path.dirname(dirpath)
    scnpath = os.path.dirname(lgtpath)
    print('dirpath: ', dirpath)
    print('lgtpath: ', lgtpath)
    print('scnpath: ', scnpath)

def filename():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    filename = filename.split('.')[0].split('_')[:-1]
    print('filename is : ', filename)
    return filename

def folder():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    basename, extension = os.path.splitext(filename)
    new_basename = basename[:-7]  # Remove "_Render"
    print('folder is : ', new_basename)
    return new_basename

def scene_name():
    scene_names = [scene.name for scene in bpy.data.scenes]
    for scene_name in scene_names:
        scene = bpy.data.scenes.get(scene_name)
        print('scene : ', scene)
        return scene_names[1]

_get_finaling_file(filepath)    
filename()
folder()
scene_name()

'''
# get render file
def render_file():
    current_path = bpy.data.filepath
    render_file_dir = os.path.dirname(current_path)
    for file in os.listdir(render_file_dir) :
        if file.endswith("_RENDER.blend") : 
            anim_file = os.path.join(render_file_dir, file)
            return anim_file


cycles_sc = ['BG', 'CHAR', 'Lightray', 'RIM' ]
eevee_sc = ['FX_Trail']

for scene in cycles_sc:
    scene.render.engine = 'BLENDER_CYCLES'

for scene in eevee_sc:
    scene.render.engine = 'BLENDER_EEVEE'

    
'''

# set output node


'''
def main():
    file_name_without_extension = get_file_name_without_extension(bpy.data.filepath)
    base_output_directory = Path(r"V:\BBB_Galaxy_S2\output\2_Render\1_Episode\Episode_12\PART B\_MONSTA/")
    blender_file_name = get_file_name_without_extension(bpy.data.filepath)
    scene_names = [scene.name for scene in bpy.data.scenes]

    for scene_name in scene_names:
        scene = bpy.data.scenes.get(scene_name)
        if scene:
            scene_directory = create_output_directories(base_output_directory, blender_file_name, scene_name)
            set_node_output_paths(scene, scene_directory, file_name_without_extension)

if __name__ == "__main__":
    main()
'''