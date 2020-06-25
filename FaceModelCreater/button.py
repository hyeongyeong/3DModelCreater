import bpy
import time

class MY_BUTTON_OT_Button(bpy.types.Operator):
    bl_idname = "my.button"
    bl_description = "Button description"
    bl_label = "Button"

    def execute(self,context):
        start = time.time()

        bpy.ops.mesh.create_model_main()
        bpy.ops.mesh.hair_styler()

        print("time :", time.time() - start)

        return {'FINISHED'}