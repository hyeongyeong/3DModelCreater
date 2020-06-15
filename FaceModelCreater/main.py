import os
import bpy
import bmesh
import numpy as np
from .merge import *
from .createRegionGroup import duplicate_obj
from mathutils import Matrix

ModelFileName = "seok_f-output" 
body_file_name = "Man"

def setGlobalFilePath():
    # set global file path
    bpy.context.scene['file_path'] = {}
    bpy.context.scene['my_obj'] = {}
    bpy.context.scene['vertex_group_index'] = {}
    bpy.context.scene['body_obj'] = {}

    # bpy.context.scene['file_path']['point'] = os.getcwd() + "/input/model_point_hee.txt"
    bpy.context.scene['file_path']['point'] = os.getcwd() + "/input/model_point.txt"
    bpy.context.scene['file_path']['eye_tex'] = os.getcwd() + "/input/eyeball.jpg"
    bpy.context.scene['file_path']['eye_brow_tex'] = os.getcwd() + "/input/eyebrow_left.txt"
    bpy.context.scene['file_path']['mouth_tex'] = os.getcwd() + "/input/mouse.txt"
    bpy.context.scene['file_path']['skin_tex'] = os.getcwd() + "/input/skin.txt"
    bpy.context.scene['file_path']['face'] = os.getcwd() + "/input/" + ModelFileName + ".ply"
    bpy.context.scene['file_path']['mouth_cavity'] = os.getcwd() + "/input/mouth_cavity.obj"
    bpy.context.scene['file_path']['body'] = os.getcwd() + "/input/" + body_file_name + ".dae"


             
class main_Operator(bpy.types.Operator):
    bl_idname =  "mesh.create_model_main"
    bl_label = "Create Model"
    bl_description = "Create 3D Model"
        
    def execute(self,context):

        # get global file path
        setGlobalFilePath()
        
        bpy.ops.import_mesh.ply(filepath=bpy.context.scene['file_path']['face'])
        bpy.ops.object.shade_smooth()

        bpy.context.scene['my_obj']['ply'] = bpy.data.objects[ModelFileName]
        face = bpy.context.scene['my_obj']['ply']

        extract_nose(face) # this function should be called before any modification

        bpy.ops.wm.collada_import(filepath=bpy.context.scene['file_path']['body'])
        bpy.ops.object.shade_smooth()
        bpy.context.scene['body_obj']['dae'] = bpy.data.objects[body_file_name]

        
        body_objs = bpy.data.objects[body_file_name]
        body_objs_data = body_objs.data
        
        store_boundary_loop(face)

        bpy.ops.mesh.add_eyes()
        bpy.ops.mesh.create_region_group()

        bpy.ops.mesh.apply_texturing()
        bpy.ops.mesh.mouth()
                   
        return {'FINISHED'}
