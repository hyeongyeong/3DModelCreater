bl_info = {
    "name": "Region Segmentation",
    "author": "hyeon",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Create Region Vertex group",
    "warning": "",
    "wiki_url": "",
    "category": "Region",
}

import bpy
import bmesh
from bpy.types import (Operator, Header, Menu, Panel)
from bpy.props import (FloatVectorProperty, IntProperty, FloatProperty)
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import numpy as np
from math import radians


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
        
        ans= isInside(temp,nose_re,12)
        if(ans):
            fa.select=True

    bpy.ops.object.mode_set(mode = 'EDIT')

def curved_plane (self, context, coord):
    
    p = coord
    plane = add_plane(self, context, coord)
    point_len = len(coord)
    
    obj = bpy.context.object
    bpy.ops.object.mode_set(mode = 'EDIT')
        
    #error handle
    if obj.mode == 'EDIT' :
        bm=bmesh.from_edit_mesh(obj.data)
        bm.edges.ensure_lookup_table()
    
    
        
        for idx, e in enumerate(bm.edges):
            if idx % 3 == 2 and idx < 33:
                bev_geom = [e.verts[0], e.verts[1], e]
                o = 6
                s = 5
                bmesh.ops.bevel(bm, geom=bev_geom, offset=o, segments=s,profile= 0.5,
                vertex_only   = False,
                clamp_overlap = False,
                loop_slide    = True,
                 material      = -1,offset_type   = 'OFFSET',)
        
        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return plane
    
def add_plane(self, context, coord): 
    verts = []
    thickness = 30
    param_thick = Vector((0,0,1 * thickness))
    
    floor = ceiling = np.array(coord)
    
    ceiling = ceiling + param_thick
    floor = floor - param_thick
    verts = np.vstack([ceiling,floor])

    total = len(coord)

    #    create mesh
    edges = []
    faces = []

    for i in range(0, total):
        if i == total-1 : # the last loop
            faces.append([i,i-total+1,i+1,i+total])
        else :
            faces.append([i,i+1,i+total+1,i+total])

    mesh = bpy.data.meshes.new(name="plane")
    mesh.from_pydata(verts, edges, faces)
    
    return object_data_add(context, mesh, operator=self)

def file_read(path):
     f= open(path,"r")
     coord=[]
     while True:
            line = f.readline()
            if not line:
                break
            split = line.split()
            coord.append(Vector((float(split[0]), float(split[1]), float(split[2]))))
     f.close()
     return coord

def apply_boolean(target , plane, operation, delete) :
    
    # select face model
    bpy.ops.object.select_all(action='DESELECT')
    
    target.select_set(True)    
    bpy.context.view_layer.objects.active = target
    
    
    # add boolean modifier and apply
    bpy.ops.object.modifier_add(type="BOOLEAN")
    bpy.context.object.modifiers["Boolean"].object = plane
    bpy.context.object.modifiers["Boolean"].operation = operation
    bpy.ops.object.modifier_apply(apply_as='DATA',modifier= "Boolean")
    
    # delete modifier    
    for modifier in bpy.context.object.modifiers:
        bpy.ops.object.modifier_remove(modifier=modifier.name)
    
    if delete :
        delete_object(plane)
    
    return target

def join_obj(target, obj):
    
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    bpy.ops.object.select_all(action='DESELECT')
    
    target.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()

def select_intersect_vertices(target, obj, group_name):
    
    verts = []
    
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    bpy.ops.object.select_all(action='DESELECT')
    
    target.select_set(True)
    bpy.ops.object.mode_set(mode = 'EDIT')    
    
    target_bm=bmesh.from_edit_mesh(target.data)
    target_bm.verts.ensure_lookup_table()
 
    obj_v = obj.data.vertices
    
    i= 0
    for t in target_bm.verts:
        for o in obj_v:
            t.select = False
            if t.co.x == o.co.x and t.co.y == o.co.y and t.co.z == o.co.z :
                t.select = True
                verts.append(t.index)
                i=i+1
                break
            else:
                t.select = False
            
    vg=bpy.context.object.vertex_groups.new(name=group_name)
    bpy.ops.object.vertex_group_assign()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')    

def duplicate_obj(target):
    

    target.select_set(True)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.ops.object.select_all(action='DESELECT')
    
    new_obj = target.copy()
    new_obj.data = target.data.copy()
    bpy.context.collection.objects.link(new_obj) 
    
    return new_obj

def delete_object(target) :
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True) # Blender 2.8x
    bpy.ops.object.delete() 

def create_region_group(self, context, target, coord, vertex_group_name):
    
    intersect = "INTERSECT"
    difference = "DIFFERENCE"
    union = "UNION"
    
    # create new_obj plane to apply intersect and difference
    new_obj = duplicate_obj(target)
    new_obj_plane_d = curved_plane(self, context, coord)
    new_obj_plane_i = duplicate_obj(new_obj_plane_d)
            
    # apply boolean to get region of new_obj
    apply_boolean(target, new_obj_plane_d, difference, True)
    apply_boolean(new_obj, new_obj_plane_i, intersect, True)
    join = duplicate_obj(new_obj)
    join_obj(target, join)
    
    select_intersect_vertices(target, new_obj, vertex_group_name)
    
    delete_object(new_obj)

def eye_brow_thickness(coord, direction):
    
    total = len(coord)
    print(total)
    new_coord = []
    for i in range(0,3):
        c = coord[total-i-2]
        v = Vector((c.x + direction*3, c.y - 4, c.z))
        new_coord.append(v)
    
    return coord+ new_coord

class MESH_OT_create_region_group(Operator, AddObjectHelper):
    bl_idname = "mesh.create_region_group"
    bl_label = "Create region group"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
       
        try :
            bpy.context.scene.cursor.location = (0,0,0)
            model_point_path = bpy.context.scene['file_path']['point']

            target = bpy.context.scene['my_obj']['ply']
            coord = file_read(model_point_path)

            lips_coord = coord[32:44]
            eye_brow_right_coord = coord[1:6]
            eye_brow_left_coord = coord[6:11]
            
            # Adding thickness to eye brow
            eye_brow_right_coord = eye_brow_thickness(eye_brow_right_coord, 1) # RIGHT
            eye_brow_left_coord = eye_brow_thickness(eye_brow_left_coord, -1) # LEFT

            # create vertex group of lips
            create_region_group(self, context, target, lips_coord, "lips")
            create_region_group(self, context, target, eye_brow_right_coord, "eye_brow_r")
            create_region_group(self, context, target, eye_brow_left_coord, "eye_brow_l")

            
        except IndexError:
            print("ERROR")

        return {'FINISHED'}
    