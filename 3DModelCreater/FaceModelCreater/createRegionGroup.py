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
from .mouthCapacity import SelectObjectsInBound


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

def vertex_group_mustache_beard(objs_data,group_name, group_name2):
    f= open(bpy.context.scene['file_path']['point'],"r")
    my_object =objs_data
    faces = my_object.vertices
    iter =0
    
    top_x = []
    top_y = []
    top_z = []

    bot_x = []
    bot_y = []
    bot_z = []

    nose_top_x =[]
    nose_top_y =[]
    nose_top_z =[]

    while True:
        line = f.readline()

        if not line:
            break
        split = line.split()
        
        if iter ==14:
            nose_top_x.append(float(split[0]))
            nose_top_y.append(float(split[1]))
            nose_top_z.append(float(split[2]))

        if iter >=32 and iter <=38:
            bot_x.append(float(split[0]))
            bot_y.append(float(split[1]))
            bot_z.append(float(split[2]))


        if iter>=15 and iter<=19 :
            top_x.append(float(split[0]))
            top_y.append(float(split[1]))
            top_z.append(float(split[2]))

        iter= iter+1

    f.close()

    top = [[0]*3 for i in range(5)]
    bot = [[0]*3 for i in range(7)]
    target_point = [[0]*3 for i in range(12)]

    for i in range(0,5):
        top[i][0] = top_x[i]
        top[i][1] = (top_y[0]*(2/3) + nose_top_y[0]*(1/3))
        top[i][2] = top_z[i]

    for i in range(0,7):
        bot[i][0] = bot_x[i]
        bot[i][1] = bot_y[0]
        bot[i][2] = bot_z[i]

    for i in range(0,5):
        target_point[i][0] =top[i][0]
        target_point[i][1] =top[i][1]
        target_point[i][2] =top[i][2]

    for i in range(0,7):
        target_point[i+5][0] =bot[6-i][0]
        target_point[i+5][1] =bot[6-i][1]
        target_point[i+5][2] =bot[6-i][2]


    bpy.ops.object.mode_set(mode = 'OBJECT') 
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')


    for fa in faces:
        
        temp3 = []
        temp3.append(fa.co.x)
        temp3.append(fa.co.y)
        temp3.append(fa.co.z)
        
        ans= isInside(temp3,target_point,12)
        
        if(ans):
            fa.select=True
     

    bpy.ops.object.mode_set(mode = 'EDIT')
    vg=bpy.context.object.vertex_groups.new(name=group_name)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    for fa in faces:
        temp3 = []
        temp3.append(fa.co.x)
        temp3.append(fa.co.y)
        temp3.append(fa.co.z)

        if(temp3[1] < top[0][1]):
            fa.select = True

    bpy.ops.object.mode_set(mode = 'EDIT')
    vg=bpy.context.object.vertex_groups.new(name=group_name2)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

def mouthReion(): 
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.region_to_loop()
    #입 주변 바운더리 선택
    #SelectObjectsInBound(Vector((-30.0893, 14.8183, -43.0942)), Vector((30.0893, 30.8558, -28.2911))) #이전의 박스.,
    SelectObjectsInBound(Vector((-30.6703, -42.4804, -34.6092)), Vector((30.7703, -32.9558, -10.1496)))
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    vg=bpy.context.object.vertex_groups.new(name="mouth_boundary")
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    # TODO : vertex group 입 찢어진 부분 생성하기

def vertex_group_philtrum(objs_data,group_name):
    f= open(bpy.context.scene['file_path']['point'],"r")
    my_object =objs_data
    faces = my_object.vertices
    iter =0
    
    top_x = []
    top_y = []
    top_z = []

    bot_x = []
    bot_y = []
    bot_z = []

    nose_top_x =[]
    nose_top_y =[]
    nose_top_z =[]

    while True:
        line = f.readline()

        if not line:
            break
        split = line.split()
        
        if iter ==14:
            nose_top_x.append(float(split[0]))
            nose_top_y.append(float(split[1]))
            nose_top_z.append(float(split[2]))

        if iter >=32 and iter <=38:
            bot_x.append(float(split[0]))
            bot_y.append(float(split[1]))
            bot_z.append(float(split[2]))


        if iter>=15 and iter<=19 :
            top_x.append(float(split[0]))
            top_y.append(float(split[1]))
            top_z.append(float(split[2]))

        iter= iter+1

    f.close()

    top = [[0]*3 for i in range(5)]
    bot = [[0]*3 for i in range(7)]
    

    for i in range(0,5):
        top[i][0] = top_x[i]
        top[i][1] = (top_y[1]*4/5 + nose_top_y[0]*1/5) 
        
        top[i][2] = top_z[i]

    for i in range(0,7):
        bot[i][0] = bot_x[i]
        bot[i][1] = bot_y[0]
        bot[i][2] = bot_z[i]


    bot_point_y = top[2][1] * 1/5 + bot_y[3] *4/5
    for fa in faces:
        if(fa.co.x - top[2][0] < 1 and fa.co.x - top[2][0] > -1):
            #if(fa.co.y< top[2][1] and fa.co.y >bot_y[3] ):
            if(fa.co.y< top[2][1] and fa.co.y >bot_point_y ):
                fa.select = True

    bpy.ops.object.mode_set(mode = 'EDIT')
    vg=bpy.context.object.vertex_groups.new(name=group_name)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

def vertex_group_eyelashes(objs_data,group_name1,group_name2):

    eye_left_array = bpy.context.scene['eyes'][str(0)]
    eye_right_array = bpy.context.scene['eyes'][str(1)]
    my_object =objs_data
    faces = my_object.vertices       
    
    for i in eye_left_array:
        eye = Vector(i)
        for fa in faces:
            if(eye.x == fa.co.x and eye.y == fa.co.y):
                fa.select = True                      

    bpy.ops.object.mode_set(mode = 'EDIT')
    vg=bpy.context.object.vertex_groups.new(name=group_name1)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    for i in eye_right_array:
        eye = Vector(i)
        for fa in faces:
            if(eye.x == fa.co.x and eye.y == fa.co.y):
                fa.select = True                      

    bpy.ops.object.mode_set(mode = 'EDIT')
    vg=bpy.context.object.vertex_groups.new(name=group_name2)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')





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
    
    for t in target_bm.verts:
        for o in obj_v:
            t.select = False
            if t.co.x == o.co.x and t.co.y == o.co.y and t.co.z == o.co.z :
                t.select = True
                verts.append(t.index)
                break
            else:
                t.select = False
            
    vg=bpy.context.object.vertex_groups.new(name=group_name)

    bpy.ops.object.vertex_group_assign()
    
    bpy.ops.mesh.remove_doubles(threshold=0.001)
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
       
        # try :

            f= open(bpy.context.scene['file_path']['point'],"r")

            iter =0
            nose_top_x=[]
            nose_top_y=[]
            nose_top_z=[]

            while True:
                line = f.readline()


                if not line:
                    break
                split = line.split()
                
                if iter ==14:
                    nose_top_x.append(float(split[0]))
                    nose_top_y.append(float(split[1]))
                    nose_top_z.append(float(split[2]))

        
                iter= iter+1

            f.close()


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

            mouthReion()

            # create vertex group of lips

            vertex_group_philtrum(target.data,"philtrum")
            
            create_region_group(self, context, target, lips_coord, "lips")
            create_region_group(self, context, target, eye_brow_right_coord, "eye_brow_r")
            create_region_group(self, context, target, eye_brow_left_coord, "eye_brow_l")
            vertex_group_mustache_beard(target.data, "temp1","temp2")
            vertex_group_eyelashes(target.data,"left_eyelashes","right_eyelashes")
            

            
            # bpy.ops.object.mode_set(mode = 'EDIT')
            # bpy.ops.object.vertex_group_set_active(group=str("lips"))
            # bpy.ops.object.vertex_group_select()
            
            # lips_x = []
            # lips_y = []
            # lips_z = []
            # idx_lip=0
            # vg_vertex2 = []

            # bm=bmesh.from_edit_mesh(target.data)
            # bm.verts.ensure_lookup_table()
            
            # for v in bm.verts:
            #     if v.select:
            #         lips_x.append(v.co.x)
            #         lips_y.append(v.co.y)
            #         lips_z.append(v.co.z)
            #         idx_lip= idx_lip+1
            #         vg_vertex2.append(v)
           
            # bpy.ops.mesh.select_all(action = 'DESELECT')
            
            # bpy.ops.object.vertex_group_set_active(group=str("temp1"))
            # bpy.ops.object.vertex_group_select()
            
            
            # must_x = []
            # must_y = []
            # must_z = []
            # vg_vertex = []
            # idx_must =0
            
            # for v in bm.verts:
            #     if v.select:
            #         must_x.append(v.co.x)
            #         must_y.append(v.co.y)
            #         must_z.append(v.co.z)
            #         idx_must = idx_must+1
            #         vg_vertex.append(v)
           
           

            # for v in bm.verts:      
            #     if(v.co.y< nose_top_y[0]):
            #         if v.select:    
            #             for t in vg_vertex2:
            #                 if np.array_equal(v.co, t.co) :
            #                     v.select = False
            #                     break
            
            
            
            # bpy.ops.object.mode_set(mode = 'EDIT')
            # vg=bpy.context.object.vertex_groups.new(name="mustache")
            # bpy.ops.object.vertex_group_assign()
            # bpy.ops.mesh.select_all(action = 'DESELECT')
            # bpy.ops.object.mode_set(mode = 'OBJECT')

            # ####
            # bpy.ops.object.mode_set(mode = 'EDIT')
            # bpy.ops.object.vertex_group_set_active(group=str("lips"))
            # bpy.ops.object.vertex_group_select()
            
            # lips_x = []
            # lips_y = []
            # lips_z = []
            # idx_lip=0
            # vg_vertex2 = []

            # bm=bmesh.from_edit_mesh(target.data)
            # bm.verts.ensure_lookup_table()
            
            # for v in bm.verts:
            #     if v.select:
            #         lips_x.append(v.co.x)
            #         lips_y.append(v.co.y)
            #         lips_z.append(v.co.z)
            #         idx_lip= idx_lip+1
            #         vg_vertex2.append(v)
           
            # bpy.ops.mesh.select_all(action = 'DESELECT')


            # ###
            # bpy.ops.object.mode_set(mode = 'EDIT')
            # bpy.ops.object.vertex_group_set_active(group=str("mustache"))
            # bpy.ops.object.vertex_group_select()
            
            # must_x = []
            # must_y = []
            # must_z = []
            # idx_must=0
            
            # bm=bmesh.from_edit_mesh(target.data)
            # bm.verts.ensure_lookup_table()
            
            # for v in bm.verts:
            #     if v.select:
            #         must_x.append(v.co.x)
            #         must_y.append(v.co.y)
            #         must_z.append(v.co.z)
            #         idx_must= idx_must+1
            #         vg_vertex2.append(v)
           
            # bpy.ops.mesh.select_all(action = 'DESELECT')

            # ###
            # bpy.ops.object.vertex_group_set_active(group=str("temp2"))
            # bpy.ops.object.vertex_group_select()
            
            
            # beard_x = []
            # beard_y = []
            # beard_z = []
            # vg_vertex = []
            # idx_beard =0
            
            # for v in bm.verts:
            #     if v.select:
            #         beard_x.append(v.co.x)
            #         beard_y.append(v.co.y)
            #         beard_z.append(v.co.z)
            #         idx_beard = idx_beard+1
            #         vg_vertex.append(v)
           
           
            # for v in bm.verts:
            #     if(v.co.y< nose_top_y[0]):
            #         if v.select:
            #             for t in vg_vertex2:
            #                 if np.array_equal(v.co, t.co) :
            #                     v.select = False
            #                     break
            
          
        
            # bpy.ops.object.mode_set(mode = 'EDIT')
            # vg=bpy.context.object.vertex_groups.new(name="beard")
            # bpy.ops.object.vertex_group_assign()
            # bpy.ops.mesh.select_all(action = 'DESELECT')
            # bpy.ops.object.mode_set(mode = 'OBJECT')
    
            
        # except IndexError:
        #     print("ERROR")

            return {'FINISHED'}
    