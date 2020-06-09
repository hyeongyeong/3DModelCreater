import os
import bpy
import bmesh
import numpy as np
from .faceTexturing import texturing 

class main_Operator(bpy.types.Operator):
    bl_idname =  "mesh.create_model_main"
    bl_label = "Create Model"
    bl_description = "Create 3D Model"
        
    def execute(self,context):
        
        # get global file path

        model_file_name = "hee_f-output"    
        bpy.context.scene['file_path'] = {}
        bpy.context.scene['my_obj'] = {}
        bpy.context.scene['eyes'] = {}

        # bpy.context.scene['file_path']['point'] = os.getcwd() + "/input/model_point.txt"
        bpy.context.scene['file_path']['point'] = os.getcwd() + "/input/model_point_hee.txt"
        bpy.context.scene['file_path']['eye_tex'] = os.getcwd() + "/input/eyeball.jpg"
        bpy.context.scene['file_path']['eye_brow_tex'] = os.getcwd() + "/input/eyebrow_left.txt"
        bpy.context.scene['file_path']['mouth_tex'] = os.getcwd() + "/input/mouse.txt"
        bpy.context.scene['file_path']['skin_tex'] = os.getcwd() + "/input/skin.txt"
        # bpy.context.scene['file_path']['face'] = os.getcwd() + "/input/seok_f-output.ply"
        # bpy.context.scene['file_path']['face'] = os.getcwd() + "/input/hee_f-output.ply"
        bpy.context.scene['file_path']['face'] = os.getcwd() + "/input/" + model_file_name + ".ply"
        bpy.context.scene['file_path']['mouth_cavity'] = os.getcwd() + "/input/mouth_cavity.obj"

        

        objs = bpy.data.objects
            
        bpy.ops.import_mesh.ply(filepath=bpy.context.scene['file_path']['face'])
        bpy.ops.object.shade_smooth()


        bpy.context.scene['my_obj']['ply'] = bpy.data.objects[model_file_name]

        objs = bpy.data.objects[model_file_name]
        objs_data = objs.data

        #bpy.ops.mesh.mouth()
        bpy.ops.mesh.add_eyes()
        bpy.ops.mesh.create_region_group()
        #bpy.ops.mesh.mouth()
        texturing(objs)

        tx = 20
        ty = 20
        tz = 10000

        rx = 0
        ry = 0
        rz = 0

        fov = 50.0

        pi = 3.14159265

        scene = bpy.data.scenes["Scene"]

        scene.camera.data.angle = fov*(pi/180.0)

        # Set camera rotation in euler angles
        scene.camera.rotation_mode = 'XYZ'
        scene.camera.rotation_euler[0] = rx*(pi/180.0)
        scene.camera.rotation_euler[1] = ry*(pi/180.0)
        scene.camera.rotation_euler[2] = rz*(pi/180.0)

        # Set camera translation
        scene.camera.location.x = tx
        scene.camera.location.y = ty
        scene.camera.location.z = tz

        scene.camera.scale.x = 1.0
        scene.camera.scale.y = 1.0
        scene.camera.scale.z = 1.0

        # scene.camera.clip_start =0
        # scene.camera.clip_end = 100000

        # scene.camera.lens =1000

        camera = bpy.data.cameras["Camera"]

        camera.lens = 1000
        camera.clip_end = 100000
        camera.clip_start =0
        
        
        bpy.ops.object.light_add(type='SUN')
        light_obj             = bpy.data.objects['Sun']
        light_obj.data.energy = 5
        
        
 
        return {'FINISHED'}
