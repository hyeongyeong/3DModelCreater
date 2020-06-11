

import bpy
import bmesh
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import statistics
import numpy 
from copy import deepcopy



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


            if iter>=15 and iter<=20 :#eyebrow left 5媛 
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
           
            ans= isInside(temp3,temp1,4)
            ans2= isInside(temp3,temp2,4)
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




def get_selected_vertice():
    selected_index = [v.index for v in bpy.context.active_object.data.vertices if v.select]
    coord_array = []
    for i in selected_index :
        coord_array.append(bpy.context.active_object.data.vertices[i].co[1])
    coord_array.sort()
    
    print(coord_array[0:4])
    hole_vertices = [v.index for v in bpy.context.active_object.data.vertices if (v.co[1] == coord_array[0])]
    #or (v.co[1] == coord_array[1])] #or (v.co[1] == coord_array[2]) or (v.co[1] == coord_array[3])]
    #print(hole_vertices)
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for i in hole_vertices:
        bpy.context.active_object.data.vertices[i].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 

def get_feature_point():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    selected_index = [v.index for v in bpy.context.active_object.data.vertices if v.select]
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_more(use_face_step = False)
    coord_fst = []
    coord_scd = []
    for i in selected_index:
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.active_object.data.vertices[i].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_more(use_face_step = False)
        bpy.ops.object.mode_set(mode = 'OBJECT')
        connected_index = [v.index for v in bpy.context.active_object.data.vertices if v.select]
        #coord = [] #코 좌표 2
        if len(connected_index) == 13:
            coord_fst.append(i)
            arry = []
            if bpy.context.active_object.data.vertices[connected_index[10]].co[0]<0:
                for j in connected_index:
                    arry.append(bpy.context.active_object.data.vertices[j].co[0])
                for k in connected_index:
                    if bpy.context.active_object.data.vertices[k].co[0] == max(arry):
                        coord_scd.append(k)
            else : 
                for j in connected_index:
                    arry.append(bpy.context.active_object.data.vertices[j].co[0])
                for k in connected_index:
                    if bpy.context.active_object.data.vertices[k].co[0] == min(arry):
                        coord_scd.append(k)
        bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_all(action = 'DESELECT')
    if coord_fst : 
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.active_object.data.vertices[coord_fst[0]].select = True
        bpy.context.active_object.data.vertices[coord_fst[1]].select = True
        bpy.context.active_object.data.vertices[coord_scd[0]].select = True
        bpy.context.active_object.data.vertices[coord_scd[1]].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
    
    #return coord_fst[0],coord_fst[1],coord_scd[0],coord_scd[1]

        





class nostril(Operator, AddObjectHelper):
    bl_idname = "mesh.nostrill"
    bl_label = "nostril"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        objs = bpy.context.scene['my_obj']['ply']
        objs_data = objs.data

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = objs
        objs.select_set(True)

        delete_nose_hole(objs_data)
        

        get_feature_point()
        transform = (0, 4, 0)
        bpy.ops.transform.translate(value=transform, 
                            constraint_axis=(False, False, False),
                            #constraint_orientation='GLOBAL',
                            mirror=False, 
                            use_proportional_edit = True,
                            use_proportional_connected=True,
                            proportional_edit_falloff='SMOOTH',
                            proportional_size=7)
        
        
        return {'FINISHED'}
