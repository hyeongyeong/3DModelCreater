from .createRegionGroup import select_nose_area, duplicate_obj, delete_object
import subprocess
import bpy
import os
import numpy as np
from numpy import genfromtxt
import math
from mathutils import Vector, Matrix



def reset_transform(objs):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    matrix = objs.matrix_world
    M = Matrix(matrix)
    objs.matrix_world = ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))
    objs_data = objs.data
    objs_data.transform(M)
    objs_data.update()


def icp():
    model = os.getcwd() + "/external/intermediate/nose.obj"
    data = os.getcwd() + "/external/intermediate/man_nose.obj"
    save_path = os.getcwd() + "/external/intermediate/result.csv"
    icp = os.getcwd() + "/external/icp/icp_methods"
    subprocess.call(icp +' '+model+' '+data+' '+save_path, shell=True)
    matrix_world = genfromtxt(save_path, delimiter=',')
    # matrix = ((math.floor(matrix_world[0][0]*1000)/1000, matrix_world[1][0],matrix_world[2][0],matrix_world[3][0]),
    # (matrix_world[0][1],math.floor(matrix_world[1][1]*1000)/1000,matrix_world[2][1],matrix_world[3][1]),
    # (matrix_world[0][2],matrix_world[1][2],math.floor(matrix_world[2][2]*1000)/1000,matrix_world[3][2]),
    # (matrix_world[0][3],-matrix_world[2][3],matrix_world[1][3],matrix_world[3][3]))

    # matrix = ((math.floor(matrix_world[0][0]*1000)/1000, 0,0,matrix_world[3][0]),
    # (0,math.floor(matrix_world[1][1]*1000)/1000,0,matrix_world[3][1]),
    # (0,0,math.floor(matrix_world[2][2]*1000)/1000,matrix_world[3][2]),
    # (matrix_world[0][3],-matrix_world[2][3],matrix_world[1][3],matrix_world[3][3]))

    matrix = ((matrix_world[0][0]*1000/1000, 0,0,matrix_world[3][0]),
    (0,matrix_world[1][1]*1000/1000,0,matrix_world[3][1]),
    (0,0,matrix_world[2][2]*1000/1000,matrix_world[3][2]),
    (matrix_world[0][3],-matrix_world[2][3],matrix_world[1][3],matrix_world[3][3]))

    return matrix

def align(objs, matrix):


    # model = os.getcwd() + "/external/intermediate/nose.obj"
    # data = os.getcwd() + "/external/intermediate/man_nose.obj"
    # save_path = os.getcwd() + "/external/intermediate/result.csv"
    # # model = "D:\\research\\Realistic_3D_modeling\\Merge_Project\\icp\\build\\src\\examples\\models\\seok_nose.obj"
    # # data = "D:\\research\\Realistic_3D_modeling\\Merge_Project\\icp\\build\\src\\examples\\models\\man_nose.obj"

    # icp = os.getcwd() + "/external/icp/icp_methods"
    # subprocess.call(icp +' '+model+' '+data+' '+save_path, shell=True)
    # # subprocess.call('D:\\research\\Realistic_3D_modeling\\Merge_Project\\icp\\build\\src\\examples\\Release\\icp_methods' +' '+model+' '+data+' '+save_path, shell=True)
    # # subprocess.call('dir' , shell=True)

    # matrix_world = genfromtxt(save_path, delimiter=',')

    
    bpy.ops.object.select_all(action='DESELECT')
    objs.select_set(True)
    bpy.context.view_layer.objects.active = objs
    
    # matrix = ((math.floor(matrix_world[0][0]*1000)/1000, matrix_world[1][0],matrix_world[2][0],matrix_world[3][0]),
    # (matrix_world[0][1],math.floor(matrix_world[1][1]*1000)/1000,matrix_world[2][1],matrix_world[3][1]),
    # (matrix_world[0][2],matrix_world[1][2],math.floor(matrix_world[2][2]*1000)/1000,matrix_world[3][2]),
    # (matrix_world[0][3],-matrix_world[2][3],matrix_world[1][3],matrix_world[3][3]))
    objs.matrix_world = matrix

def extract_nose(objs):
    temp_objs = duplicate_obj(objs)
    temp_data = temp_objs.data
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    bpy.ops.object.select_all(action='DESELECT')
    
    temp_objs.select_set(True)
    bpy.context.view_layer.objects.active = temp_objs
    select_nose_area(temp_data)

    scn = bpy.context.scene
    names = [obj.name for obj in scn.objects]

    bpy.ops.mesh.separate(type='SELECTED')

    nose_objs = [obj for obj in scn.objects if not obj.name in names][0]


    bpy.ops.object.mode_set(mode = 'OBJECT')    
    bpy.ops.object.select_all(action='DESELECT')
    nose_objs.select_set(True)
    bpy.context.view_layer.objects.active = nose_objs

    bpy.ops.export_scene.obj(use_selection=True, filepath = os.getcwd() + "/external/intermediate/nose.obj")

    delete_object(temp_objs)
    delete_object(nose_objs)






def deSelectVerticesInBound(vector1, vector2, g_matrix):
    #for delesecting edges that are not needed
        mode = bpy.context.active_object.mode
        
        
        bpy.ops.object.mode_set(mode='OBJECT')
        selectedEdges = [e for e in bpy.context.active_object.data.edges if e.select]
        selectedVerts = [v for v in bpy.context.active_object.data.vertices if v.select]
        
        for e in selectedEdges:
            v_1 = bpy.context.active_object.data.vertices[e.vertices[0]]
            v_2 = bpy.context.active_object.data.vertices[e.vertices[1]]
            v_1_global = g_matrix @ v_1.co
            v_2_global = g_matrix @ v_2.co

            
            if (v_1_global[0] > vector1[0]) and (v_1_global[0] < vector2[0]) and (v_1_global[1] > vector1[1]) and (v_1_global[1] < vector2[1]):
                v_1.select = False
                v_2.select = False
                e.select = False
        bpy.ops.object.mode_set(mode=mode)


def store_boundary_loop(objs):
    #select 3D face model
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    bpy.ops.object.select_all(action='DESELECT')
    objs.select_set(True)
    bpy.context.view_layer.objects.active = objs
    global_matrix = objs.matrix_world
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.region_to_loop()
    deSelectVerticesInBound(Vector((-30.6703, -42.4804, -34.6092)), Vector((30.7703, -32.9558, -10.1496)),global_matrix)
    # deSelectVerticesInBound(Vector((0.219, 7.861, 0)), Vector((0.5429, 7.991, 0)), global_matrix)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    vg = objs.vertex_groups.new(name="face_edge")
    vert = []
    for v in objs.data.vertices:
        if v.select:
            vert.append(v.index)
    vg.add(vert, 1.0, 'ADD')

def merge(objs, body_objs):
    #extract boundary edge loop
    new_objs = duplicate_obj(objs)
    bpy.ops.object.select_all(action = 'DESELECT')
    new_objs.select_set(True)
    bpy.context.view_layer.objects.active = new_objs
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("face_edge"))
    bpy.ops.object.vertex_group_select()

    face_v = [v for v in bpy.context.active_object.data.vertices if v.select] # use this vertices to transfer normal to shrink object & extrude object


    scn = bpy.context.scene
    names = [obj.name for obj in scn.objects]

    bpy.ops.mesh.separate(type='SELECTED')

    extrude_objs = [obj for obj in scn.objects if not obj.name in names][0]

    delete_object(new_objs)

    bpy.ops.object.select_all(action = 'DESELECT')
    extrude_objs.select_set(True)
    bpy.context.view_layer.objects.active = extrude_objs
    
    extrude_normal = []
    for i in range(len(extrude_objs.data.vertices)):
        extrude_objs.data.vertices[i].normal = face_v[i].normal
        extrude_normal.append(extrude_objs.data.vertices[i].normal)
        



    shrink_objs = duplicate_obj(extrude_objs)
    
    bpy.ops.object.select_all(action = 'DESELECT')
    extrude_objs.select_set(True)
    bpy.context.view_layer.objects.active = extrude_objs  
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.506911), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.289664, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    


    #selected boundary edge loop for creating face plane and create face plane
    bpy.ops.object.mode_set(mode = 'OBJECT')
    selectedEdges = [e for e in bpy.context.active_object.data.edges if e.select]
    selectedVerts = [v for v in bpy.context.active_object.data.vertices if v.select]
    for e in extrude_objs.data.edges:
        if e.select:
            extrude_objs.data.vertices[e.vertices[0]].select = False
            extrude_objs.data.vertices[e.vertices[1]].select = False
            e.select = False

        else:
            if (extrude_objs.data.vertices[e.vertices[0]] not in selectedVerts) & (extrude_objs.data.vertices[e.vertices[1]] not in selectedVerts):
                extrude_objs.data.vertices[e.vertices[0]].select = True
                extrude_objs.data.vertices[e.vertices[1]].select = True   
                e.select = True
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.fill()

    # add boolean modifier and apply
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    body_objs.select_set(True)
    bpy.context.view_layer.objects.active = body_objs
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.modifier_add(type="BOOLEAN")
    bpy.context.object.modifiers["Boolean"].object = extrude_objs
    bpy.context.object.modifiers["Boolean"].operation = "DIFFERENCE"
    bpy.ops.object.modifier_apply(apply_as='DATA',modifier= "Boolean")

    delete_object(extrude_objs)

    # add edge loop to vertex group and use shrink modifier to attach to body model
    bpy.ops.object.select_all(action='DESELECT')
    shrink_objs.select_set(True)
    bpy.context.view_layer.objects.active =shrink_objs
    vg = shrink_objs.vertex_groups.new(name="body_edge")
    vert = []
    i = 0

    for i in range(len(face_v)):
        print(face_v[i].normal)

    for i in range(len(shrink_objs.data.vertices)):
        shrink_objs.data.vertices[i].normal = extrude_normal[i]
        vert.append(shrink_objs.data.vertices[i].index)
    # for v in shrink_objs.data.vertices:
    #     # v.normal = face_v[i].normal
    #     print(v.normal)
    #     vert.append(v.index)
    #     i = i + 1
    vg.add(vert, 1.0, 'ADD')
    bpy.ops.object.modifier_add(type='SHRINKWRAP')
    bpy.context.object.modifiers["Shrinkwrap"].target = body_objs
    bpy.context.object.modifiers["Shrinkwrap"].wrap_method = 'TARGET_PROJECT'
    bpy.context.object.modifiers["Shrinkwrap"].wrap_mode = 'INSIDE'
    bpy.ops.object.modifier_apply(apply_as='DATA',modifier= "Shrinkwrap")


    #join two object
    bpy.ops.object.select_all(action='DESELECT')
    body_objs.select_set(True)
    shrink_objs.select_set(True)
    bpy.context.view_layer.objects.active = body_objs
    bpy.ops.object.join()



    # this is for testing. Fix it when commit
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    body_objs.select_set(True)
    bpy.context.view_layer.objects.active =body_objs
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("body_edge"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    will_modified = [v for v in bpy.context.active_object.data.vertices if v.select] # use this vertices to transfer normal to shrink object & extrude object


    for i in range(len(will_modified)):
        will_modified[i].normal = extrude_normal[i]


    model = os.getcwd() + "/external/intermediate/nose.obj"
    data = os.getcwd() + "/external/intermediate/man_nose.obj"
    save_path = os.getcwd() + "/external/intermediate/result.csv"
    icp = os.getcwd() + "/external/icp/icp_methods"
    subprocess.call(icp +' '+model+' '+data+' '+save_path, shell=True)
    matrix_world = genfromtxt(save_path, delimiter=',')

    matrix = ((math.floor(matrix_world[0][0]*1000)/1000, 0,0,matrix_world[3][0]),
    (0,math.floor(matrix_world[1][1]*1000)/1000,0,matrix_world[3][1]),
    (0,0,math.floor(matrix_world[2][2]*1000)/1000,matrix_world[3][2]),
    (matrix_world[0][3],-matrix_world[2][3],matrix_world[1][3],matrix_world[3][3]))
    objs.matrix_world = matrix


    #search nearby vertex
    bpy.ops.object.mode_set(mode='OBJECT')
    search_distance = 0.01
    bpy.ops.object.select_all(action='DESELECT')
    body_objs.select_set(True)
    bpy.context.view_layer.objects.active = body_objs
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'EDIT')

    bpy.ops.object.vertex_group_set_active(group=str("body_edge"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.mode_set(mode='OBJECT')
    selectedEdges = [e for e in bpy.context.active_object.data.edges if e.select]
    selectedVerts = [v for v in bpy.context.active_object.data.vertices if v.select]

    for v in bpy.context.active_object.data.vertices:
        # print(v.co)
        if (not v.select):
            for v_ in selectedVerts:
                dist = math.sqrt((v.co.x - v_.co.x)**2 + (v.co.y - v_.co.y)**2 + (v.co.z - v_.co.z)**2)
                if dist < search_distance:
                    v.select =True

    








    # #join face and body
    # bpy.ops.object.mode_set(mode ='OBJECT')
    # bpy.ops.object.select_all(action='DESELECT')
    # body_objs.select_set(True)
    # objs.select_set(True)
    # bpy.context.view_layer.objects.active = body_objs
    # bpy.ops.object.join()

    # #merge face and body
    # bpy.ops.object.select_all(action='DESELECT')
    # body_objs.select_set(True)
    # bpy.context.view_layer.objects.active =body_objs
    # bpy.ops.object.mode_set(mode = 'EDIT')
    # bpy.ops.mesh.select_all(action='DESELECT')
    # bpy.ops.object.mode_set(mode = 'EDIT')
    # bpy.ops.object.vertex_group_set_active(group=str("face_edge"))
    # bpy.ops.object.vertex_group_select()
    # bpy.ops.object.vertex_group_set_active(group=str("body_edge"))
    # bpy.ops.object.vertex_group_select()
    # bpy.ops.mesh.bridge_edge_loops()   
    # bpy.ops.mesh.bridge_edge_loops(interpolation='SURFACE')
    # bpy.ops.mesh.bridge_edge_loops(number_cuts=10, interpolation='SURFACE')




