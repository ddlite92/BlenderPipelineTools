import bpy
import os

bpy.context.view_layer.objects.active = bpy.context.scene.camera

# Define the export path (adjust as needed)
directory = os.path.dirname(bpy.data.filepath)  
file = os.path.join(directory, "cam.jsx")

try:
    # Execute the export operator
    bpy.ops.export.jsx(filepath=file)
    print(f"Exported JSX to: {filepath}")

except Exception as e:
    print(f"Error during export: {e}")              

    

