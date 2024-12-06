import bpy


coll = ['BBB', 'Gopal', 'Qually', 'Probe', 'Adudu', 'Roksasa', 'Ochobot', 'MechaGentar']

def create_collection():
    scene = bpy.context.scene
    char = bpy.data.collections.get('CHAR')


    for colls in coll:
        char_coll = bpy.data.collections.new(colls)
        char.children.link(char_coll)
        
create_collection()
    


