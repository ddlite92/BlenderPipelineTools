import bpy
import os

def export_jsx_from_script():

    bpy.context.view_layer.objects.active = bpy.context.scene.camera

    directory = os.path.dirname(bpy.data.filepath)  
    file = os.path.join(directory, "cam.jsx")

    try:
        # Execute the export operator
        bpy.ops.export.jsx(filepath=file)
        print(f"Exported JSX to: {filepath}")

    except Exception as e:
        print(f"Error during export: {e}")

# Run the script
export_jsx_from_script()
                                      

    

