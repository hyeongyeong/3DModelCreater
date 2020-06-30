import bpy
import time


class step_three(bpy.types.Operator):
    bl_idname = "step.three"
    bl_label = "Step 3"
    bl_description = "Step three"

    def execute(self,context):
        bpy.ops.mesh.hair_styler()
        return {'FINISHED'}


class step_four(bpy.types.Operator):
    bl_idname = "step.four"
    bl_label = "Step 4"
    bl_description = "Step four"


    def execute(self,context):
        tx = 0.574867 
        ty = 7.15432 
        tz = 10

        rx = 0
        ry = 0
        rz = 0



        scene = bpy.data.scenes["Scene"]



        # Set camera rotation in euler angles
        scene.camera.rotation_mode = 'XYZ'
        scene.camera.rotation_euler[0] = rx
        scene.camera.rotation_euler[1] = ry
        scene.camera.rotation_euler[2] = rz

        # Set camera translation
        scene.camera.location.x = tx
        scene.camera.location.y = ty
        scene.camera.location.z = tz

        bpy.ops.render.render(use_viewport = True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
        return {'FINISHED'}


class MY_BUTTON_OT_Button(bpy.types.Operator):
    bl_idname = "my.button"
    bl_description = "Button description"
    bl_label = "Button"

    def execute(self,context):
        start = time.time()

        bpy.ops.mesh.create_model_main()

        
        bpy.ops.mesh.hair_styler()


        tx = 0.574867 
        ty = 7.15432 
        tz = 10

        rx = 0
        ry = 0
        rz = 0



        scene = bpy.data.scenes["Scene"]



        # Set camera rotation in euler angles
        scene.camera.rotation_mode = 'XYZ'
        scene.camera.rotation_euler[0] = rx
        scene.camera.rotation_euler[1] = ry
        scene.camera.rotation_euler[2] = rz

        # Set camera translation
        scene.camera.location.x = tx
        scene.camera.location.y = ty
        scene.camera.location.z = tz

        bpy.ops.render.render(use_viewport = True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')

        print("time :", time.time() - start)

        return {'FINISHED'}