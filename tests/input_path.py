import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Path"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, 'input')


def register():
    bpy.utils.register_class(HelloWorldPanel)
    bpy.types.Scene.input = bpy.props.StringProperty\
      (
      name = "Path",
      default = "",
      description = "Define the root path of the project",
      subtype = 'DIR_PATH'
      )

def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)
    
    del bpy.types.Scene.input


if __name__ == "__main__":
    register()
        
     