import os
import bpy
import bmesh
import numpy as np
from .texturing import texturing 

class main_Operator(bpy.types.Operator):
    bl_idname =  "mesh.create_face_main"
    bl_label = "Simple operator"
    bl_description = "Center 3d cursor"

    def delete_nose_hole(objs_data):
        f= open(bpy.context.scene['file_path']['point'],"r")
        my_object =objs_data
        faces = my_object.vertices
        iter =0
        

        temp_x = []
        temp_y = []
        temp_z = []

        temp_x2 = []
        temp_y2 = []
        temp_z2 = []

        while True:
            line = f.readline()
        
            if not line:
                break
            split = line.split()
            iter= iter+1

            if iter ==23 or iter ==28:
                temp_x2.append(float(split[0]))
                temp_y2.append(float(split[1]))
                temp_z2.append(float(split[2]))


            if iter>=15 and iter<=20 :#eyebrow left 5媛�
                temp_x.append(float(split[0]))
                temp_y.append(float(split[1]))
                temp_z.append(float(split[2]))

        f.close()

        temp_x[1]= temp_x2[0]
        temp_x[5]= temp_x2[1]


        temp1 = [[0]*3 for i in range(4)]
        k=0
        for i in range(0,2): #mouse
            for j in range(0,2):
                if(i==1):
                    j= 1-j

                temp1[k][0] = temp_x[j+1]+ (temp_x[0]- temp_x[j+1])*((i+1)/3) 
                temp1[k][1] = temp_y[j+1]+ (temp_y[0]- temp_y[j+1])*((i+1)/3)
                temp1[k][2] = temp_z[j]
                k=k+1

        temp2 = [[0]*3 for i in range(4)]
        k=0
        for i in range(0,2): #mouse
            for j in range(0,2):
                if(i==1):
                    j=1-j

                temp2[k][0] = temp_x[j+4]+ (temp_x[0]- temp_x[j+4])*((i+1)/3) 
                temp2[k][1] = temp_y[j+4]+ (temp_y[0]- temp_y[j+4])*((i+1)/3)
                temp2[k][2] = temp_z[j+4]
                k=k+1
        
        # for i in range(0,4):
        #     bpy.ops.mesh.primitive_cube_add(location=(temp1[i][0], temp1[i][1], temp1[i][2]))
        #     bpy.ops.mesh.primitive_cube_add(location=(temp2[i][0], temp2[i][1], temp2[i][2]))


        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for fa in faces:
            #isInside(f,mouse,12)
            temp3 = []
            temp3.append(fa.co.x)
            temp3.append(fa.co.y)
            temp3.append(fa.co.z)
           
            ans= main_Operator.isInside(temp3,temp1,4)
            ans2= main_Operator.isInside(temp3,temp2,4)
            if(ans or ans2):
                fa.select=True
        
        bpy.ops.object.mode_set(mode = 'EDIT')

    def isInside(aa,bb,cc):
        crosses = 0
        for i in range(0,cc):
            j = (i+1)%cc
            if((bb[i][1] > aa[1]) != (bb[j][1] > aa[1]) ):
                atX = (bb[j][0]- bb[i][0])*(aa[1]-bb[i][1])/(bb[j][1]-bb[i][1])+bb[i][0]
                if(aa[0] < atX):
                    crosses= crosses+1
        return crosses % 2 > 0

    def select_nose_area(objs_data):
        f= open(bpy.context.scene['file_path']['point'],"r")
        my_object =objs_data
        faces = my_object.vertices
        iter =0
        nose_x =[]
        nose_y =[]
        nose_z =[]

        temp_x = []
        temp_y = []
        temp_z = []

        while True:
            line = f.readline()
        
            if not line:
                break
            split = line.split()
            iter= iter+1

            if iter>=12 and iter<=20 :#eyebrow left 5媛�
                nose_x.append(float(split[0]))
                nose_y.append(float(split[1]))
                nose_z.append(float(split[2]))

            if iter==33 or iter == 39:
                temp_x.append(float(split[0]))
                temp_y.append(float(split[1]))
                temp_z.append(float(split[2]))


        f.close()
        nose = [[0]*3 for i in range(6)]
        j=0
        for i in range(0,9): #mouse
            if(i==0 or (i>=4 and i<=8)):
                nose[j][0] =nose_x[i]
                nose[j][1] =nose_y[i]
                nose[j][2] =nose_z[i]
                j=j+1

        nose[1][0] = temp_x[0]
        nose[5][0] = temp_x[1]
        
        for i in range(0,3):
            nose[i+2][1]= (nose[1][1]+nose[5][1])/2


        temp_coord= [[0]*3 for i in range(6)]
        j=0
        for i in range(0,3):
            temp_coord[i][0] = nose[1][0] + (nose[0][0] - nose[1][0])*((i+1)/4)
            temp_coord[i][1] = nose[1][1] + (nose[0][1] - nose[1][1])*((i+1)/4)

        for i in range(3,6):
            temp_coord[i][0] = nose[0][0] + (nose[5][0] - nose[0][0])*((i-2)/4)
            temp_coord[i][1] = nose[0][1] + (nose[5][1] - nose[0][1])*((i-2)/4)   

        nose_re = [[0]*3 for i in range(12)]

        nose_re[0] = nose[1]
        for i in range(0,3):
            nose_re[i+1]= temp_coord[i]
        
        nose_re[4]= nose[0]
        for i in range(3,6):
            nose_re[i+2] = temp_coord[i]
        
        for i in range(0,4):
            nose_re[i+8] = nose[5-i]

        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for fa in faces:
            #isInside(f,mouse,12)
            temp = []
            temp.append(fa.co.x)
            temp.append(fa.co.y)
            temp.append(fa.co.z)
           
            ans= main_Operator.isInside(temp,nose_re,12)
            if(ans):
                fa.select=True
        
        bpy.ops.object.mode_set(mode = 'EDIT')
            
    def execute(self,context):
        
        # get global file path

        model_file_name = "hee_f-output"    
        bpy.context.scene['file_path'] = {}
        bpy.context.scene['my_obj'] = {}
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

        bpy.ops.mesh.mouth()
        bpy.ops.mesh.create_region_group()
        texturing(objs)
        bpy.ops.mesh.add_eyes()
        
           
        return {'FINISHED'}
