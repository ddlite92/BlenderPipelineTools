import bpy


coll = ['CH_BBB', 'CH_Gopal', 'CH_Qually', 'CH_Probe', 'CH_Adudu', 'CH_Roksasa', 'CH_Ochobot', 'CH_MechaGentar', 'CH_SuitBot', 'CH_CivilianBot_03', 'CH_CivilianBot_02' ]

def create_collection():
    scene = bpy.context.scene
    char = bpy.data.collections.get('CHAR')


    for colls in coll:
        char_coll = bpy.data.collections.new(colls)
        char.children.link(char_coll)

bpy.context.scene.camera.data.clip_start = 0.01
bpy.context.scene.camera.data.clip_end = 1000000000      

                                      
create_collection()
    

