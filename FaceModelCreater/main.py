import os
import bpy
import bmesh
import numpy as np

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
        bpy.context.scene['file_path']['point'] = os.getcwd() + "/../input/model_point_hee.txt"
        bpy.context.scene['file_path']['eye_tex'] = os.getcwd() + "/../input/eyeball.jpg"
        bpy.context.scene['file_path']['eye_brow_tex'] = os.getcwd() + "/../input/eyebrow_left.txt"
        bpy.context.scene['file_path']['mouth_tex'] = os.getcwd() + "/../input/mouse.txt"
        bpy.context.scene['file_path']['skin_tex'] = os.getcwd() + "/../input/skin.txt"
        bpy.context.scene['file_path']['face'] = os.getcwd() + "/../input/" + model_file_name + ".ply"
        bpy.context.scene['file_path']['mouth_cavity'] = os.getcwd() + "/../input/mouth_cavity.obj"

            
        bpy.ops.import_mesh.ply(filepath=bpy.context.scene['file_path']['face'])
        bpy.ops.object.shade_smooth()


        bpy.context.scene['my_obj']['ply'] = bpy.data.objects[model_file_name]


        bpy.ops.mesh.add_eyes()
        bpy.ops.mesh.create_region_group()
        bpy.ops.mesh.apply_texturing()
        bpy.ops.mesh.mouth()
        
        
           
        return {'FINISHED'}
