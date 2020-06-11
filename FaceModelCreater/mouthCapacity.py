bl_info = {
    "name" : "BlenderDemoAddon",
    "author" : "songdae",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


import bpy
import bmesh
from bpy.types import Operator
from bpy.types import Menu
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import statistics
import numpy 
from copy import deepcopy


def get_position(self, context):
    obj = bpy.context.active_object
    if obj.mode == 'EDIT':
        # this works only in edit mode,
        bm = bmesh.from_edit_mesh(obj.data)
        verts = [vert.co for vert in bm.verts]
    else:
        # this works only in object mode,
        verts = [vert.co for vert in obj.data.vertices]
    # coordinates as tuples
    plain_verts = [vert.to_tuple() for vert in verts]
    print(plain_verts[0])

    
def print_vert_details(selected_verts):
    num_verts = len(selected_verts)
    print("number of verts: {}".format(num_verts))
    print("vert indices: {}".format([id.index for id in selected_verts]))
    

def get_vertex_data(object_reference):
    bm = bmesh.from_edit_mesh(object_reference.data)
    selected_verts = [vert for vert in bm.verts if vert.select]
    print_vert_details(selected_verts)

#오브젝트 정점 중 해당 인덱스의 정점을 선택(edit mode)
def select_by_index(index1,index2):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj.data.vertices[index1].select = True
    obj.data.vertices[index2].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 

#특정 영역 내 vertex 존재 유무 판단
def IsInBoundingVectors(vector_check, vector1, vector2):
    for i in range(0, 3):
        if ((vector_check[i] < vector1[i] and vector_check[i] < vector2[i])
            or (vector_check[i] > vector1[i] and vector_check[i] > vector2[i])):
            return False  
        
    return True


#특정 영역 내 vertices unselect
def SelectObjectsInBound(vector1, vector2):
    #mode = bpy.context.active_object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    selected_verts_indices = [v.index for v in bpy.context.active_object.data.vertices if v.select]
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for i in selected_verts_indices:
        if(IsInBoundingVectors(obj.matrix_world @ bpy.context.active_object.data.vertices[i].co, vector1, vector2)):
            obj.data.vertices[i].select = True
        else:
            obj.data.vertices[i].select = False
    bpy.ops.object.mode_set(mode = 'EDIT') 

    bpy.ops.object.mode_set(mode='OBJECT')


# 선택된 vertices의 양 끝점 추출
def sort_endpoints(object_reference):
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(object_reference.data)
    verts = [obj.matrix_world @ vert.co for vert in bm.verts if vert.select]
    verts_loc = [vert.to_tuple() for vert in verts]  
    return verts_loc, verts

#교차되어 있는 입술 이동
def move_lip(arry_even,arry_odd,object_reference):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.scene['my_obj']['ply'].data
    for i in range(0,len(arry_even)-1):
        if(obj.vertices[arry_even[i]].co[1]>obj.vertices[arry_odd[i]].co[1]):
            obj.vertices[arry_odd[i]].co[1] = obj.vertices[arry_even[i]].co[1]+0.2
        elif(obj.vertices[arry_odd[i]].co[1]>obj.vertices[arry_even[i]].co[1]):
            obj.vertices[arry_even[i]].co[1] = obj.vertices[arry_odd[i]].co[1]+0.2
        else:
            obj.vertices[arry_odd[i]].co[1] = obj.vertices[arry_even[i]].co[1]+0.2

    
    
    


#입술 verts 정렬
def sort_upperLips(sortedvertices,object_reference,context):
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(object_reference.data)
    verts = [vert for vert in bm.verts if vert.select]
    arry_even = []
    arry_odd = []
    for i in sortedvertices:
        if((sortedvertices.index(i) != 0) and (sortedvertices.index(i) != len(sortedvertices)-1)):
            if(sortedvertices.index(i) % 2):
                for vert in verts:
                    if(i == obj.matrix_world @ vert.co):
                        arry_even.append(vert.index)
            else:
                for vert in verts:
                    if(i == obj.matrix_world @ vert.co):
                        arry_odd.append(vert.index)


    

    # 입 벌려있는지 판단
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.active_object.data.vertices[arry_even[(len(arry_even)-10)]].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_more(use_face_step = False) 
    bpy.ops.object.mode_set(mode = 'OBJECT')
    selected_verts_indices_even = [v.index for v in bpy.context.active_object.data.vertices if v.select]
    bpy.ops.object.mode_set(mode = 'EDIT')

    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.active_object.data.vertices[arry_odd[(len(arry_odd)-10)]].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_more(use_face_step = False) 
    bpy.ops.object.mode_set(mode = 'OBJECT')
    selected_verts_indices_odd = [v.index for v in bpy.context.active_object.data.vertices if v.select]
    bpy.ops.object.mode_set(mode = 'EDIT')

    ycord_even = []
    ycord_odd = []
    
    for i in selected_verts_indices_even :
        ycord_even.append(bpy.context.active_object.data.vertices[i].co[1])
    for i in selected_verts_indices_odd :
        ycord_odd.append(bpy.context.active_object.data.vertices[i].co[1])
    

    if (max(ycord_even)>max(ycord_odd)) & (min(ycord_even)>max(ycord_odd)):
        print('do not move lip boundary')
    elif (max(ycord_odd)>max(ycord_even)) & (min(ycord_odd)>max(ycord_even)):
        print('do not move lip boundary')
    else:
        move_lip(arry_even,arry_odd,object_reference)  

                        
    


class mouth_creation(Operator,AddObjectHelper ):
#class mouth(bpy.types.Operator):
    bl_idname = "mesh.mouth"
    bl_label = "create mouth"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        file_loc = bpy.context.scene['file_path']['mouth_cavity'] 
        bpy.ops.import_scene.obj(filepath=file_loc)
        #구강 선택 후 바운더리 따기
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.context.object.vertex_groups.new(name="mouth_cavity_boundary")
        bpy.ops.mesh.region_to_loop()
        bpy.ops.object.vertex_group_assign()



        
        obj = bpy.context.active_object
        cloc,cind = sort_endpoints(obj)     #mouth cavity의 좌표와 인덱스들 저장(처음 로드됬을때의 위치정보)
        del(cind)

        #얼굴 선택 후 바운더리 따기
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.context.scene['my_obj']['ply']
        bpy.context.scene['my_obj']['ply'].select_set(True)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.object.vertex_group_set_active(group=str("mouth_boundary"))
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        selected_verts_indices = [v.index for v in bpy.context.active_object.data.vertices if v.select]
        for i in selected_verts_indices:
            bpy.context.scene['my_obj']['ply'].data.vertices[i].co[2] -= 1.17
           


        bpy.ops.object.mode_set(mode = 'EDIT')
        
        obj_mask = bpy.context.active_object
        mloc,mind = sort_endpoints(obj_mask)    #mask의 좌표와 인덱스들
        
        
        sortedvertices = sorted(mind, key=lambda x: x[0])       #x좌표 기준을 정렬된 정점들
        object_reference = bpy.context.active_object
        sort_upperLips(sortedvertices,object_reference,context)
        
        
        # 마스크의 x좌표 길이/mouth cavity의 x좌표 길이 가 scale이 된다
        mouth_cavity = bpy.data.objects["models.001"]
        scl = (max(mloc)[0]-min(mloc)[0]) / (max(cloc)[0]-min(cloc)[0])
        mouth_cavity.scale = (scl,scl,scl)
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].scale = (scl,scl,scl)
        bpy.data.objects["tongue_lowres_Mesh.001"].scale = (scl,scl,scl)   
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].scale = (scl,scl,scl)

        # mouth cavity의 좌표값이 변화하였으니 갱신해준다 (scale변화로 인해 갱신)
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group=str("mouth_cavity_boundary"))
        bpy.ops.object.vertex_group_select()
        obj = bpy.context.active_object
        cloc_revised,cind_revised = sort_endpoints(obj)
        del(cind_revised)

        # 마스크 입 좌표중 x좌표가 가장 작은 점이 base point가 된다
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)
        obj = bpy.context.active_object
        obj.location.x += min(mloc)[0]-min(cloc_revised)[0]     #base point의 x좌표 차이만큼 이동시킨다, yz도
        obj.location.y += min(mloc)[1]-min(cloc_revised)[1]
        obj.location.z += min(mloc)[2]-min(cloc_revised)[2]

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['Lower_jaw_teeth_Lower_jaw_teeth.001'] # 하악의 위치도 이동
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(True)
        obj = bpy.context.active_object
        obj.location.x += min(mloc)[0]-min(cloc_revised)[0]
        obj.location.y += min(mloc)[1]-min(cloc_revised)[1]
        obj.location.z += min(mloc)[2]-min(cloc_revised)[2]

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['tongue_lowres_Mesh.001']   #혀 이동
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(True)
        obj = bpy.context.active_object
        obj.location.x += min(mloc)[0]-min(cloc_revised)[0]
        obj.location.y += min(mloc)[1]-min(cloc_revised)[1]
        obj.location.z += min(mloc)[2]-min(cloc_revised)[2]

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['Upper_jaw_teeth_Upper_jaw_teeth.001'] #상악 이동
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(True)
        obj = bpy.context.active_object
        obj.location.x += min(mloc)[0]-min(cloc_revised)[0]
        obj.location.y += min(mloc)[1]-min(cloc_revised)[1]
        obj.location.z += min(mloc)[2]-min(cloc_revised)[2]

        # mouth cavity의 좌표값이 변화하였으니 갱신해준다
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group=str("mouth_cavity_boundary"))
        bpy.ops.object.vertex_group_select()
        obj = bpy.context.active_object
        cloc_revised_2,cind_revised_2 = sort_endpoints(obj)
        del(cloc_revised_2)

        # rot하기 위한 pivot 변경 
        bpy.ops.object.mode_set(mode = 'OBJECT')
        save_loc = bpy.context.scene.cursor.location    #현재 커서 위치 저장
        vec = mind[mloc.index(min(mloc))] + mind[mloc.index(max(mloc))]
        bpy.context.scene.cursor.location = vec/2
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["models.001"].select_set(False)
        
        
        
        bpy.context.view_layer.objects.active = bpy.data.objects['Lower_jaw_teeth_Lower_jaw_teeth.001'] # 하악의 위치도 이동
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(True)
        save_loc_lower = bpy.context.scene.cursor.location
        bpy.context.scene.cursor.location = vec/2
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(False)

        bpy.context.view_layer.objects.active = bpy.data.objects['tongue_lowres_Mesh.001']   #혀 이동
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(True)
        save_loc_tongue = bpy.context.scene.cursor.location
        bpy.context.scene.cursor.location = vec/2
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(False)

        bpy.context.view_layer.objects.active = bpy.data.objects['Upper_jaw_teeth_Upper_jaw_teeth.001'] #상악 이동
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(True)
        save_loc_upper = bpy.context.scene.cursor.location
        bpy.context.scene.cursor.location = vec/2
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(False)
        
        
        #rot 값 생성
        v_c = statistics.median(cind_revised_2)
        v_m = statistics.median(mind)
        v_o = vec/2
        v_o[0] = v_m[0]
        
        v1 = v_c - v_o
        v2 = v_m - v_o
        a1 = v2.angle(v1)   #radian 값

        if(a1> 0.785398):
            a1 =  3.141592/2 - a1 


    
        #rotation
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)
        default_ang = bpy.context.object.rotation_euler
        angle = default_ang[0]-a1
        bpy.context.object.rotation_euler[0] = angle
        bpy.context.view_layer.objects.active = bpy.data.objects['Lower_jaw_teeth_Lower_jaw_teeth.001']
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(True)
        bpy.context.object.rotation_euler[0] = angle
        
        bpy.context.view_layer.objects.active = bpy.data.objects['tongue_lowres_Mesh.001']
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(True)
        #bpy.context.object.rotation_euler[0] = default_ang[0]-a1
        bpy.context.object.rotation_euler[0] = angle
        
        bpy.context.view_layer.objects.active = bpy.data.objects['Upper_jaw_teeth_Upper_jaw_teeth.001']
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(True)
        #bpy.context.object.rotation_euler[0] = default_ang[0]-a1
        bpy.context.object.rotation_euler[0] = angle


        #구강 메시가 튀어나오는 부분이 생겨서 뒤로 민다, 임의값 1만큼
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)
        obj = bpy.context.active_object
        obj.location.z -= 0.2
        
        #해제
        bpy.data.objects["models.001"].select_set(False)
        bpy.context.scene['my_obj']['ply'].select_set(False)
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(False)
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(False)
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(False)

        
        
        #오리진을 원래 상태로 복구
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)
        bpy.context.scene.cursor.location = save_loc
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["models.001"].select_set(False)

        bpy.context.view_layer.objects.active = bpy.data.objects['Lower_jaw_teeth_Lower_jaw_teeth.001']
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(True)
        bpy.context.scene.cursor.location = save_loc_lower
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(False)
        
        bpy.context.view_layer.objects.active = bpy.data.objects['tongue_lowres_Mesh.001']
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(True)
        bpy.context.scene.cursor.location = save_loc_tongue
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(False)
        
        bpy.context.view_layer.objects.active = bpy.data.objects['Upper_jaw_teeth_Upper_jaw_teeth.001']
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(True)
        bpy.context.scene.cursor.location = save_loc_upper
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(False)
        #해제
        bpy.data.objects["models.001"].select_set(False)
        bpy.context.scene['my_obj']['ply'].select_set(False)
        bpy.data.objects["Lower_jaw_teeth_Lower_jaw_teeth.001"].select_set(False)
        bpy.data.objects["tongue_lowres_Mesh.001"].select_set(False)
        bpy.data.objects["Upper_jaw_teeth_Upper_jaw_teeth.001"].select_set(False)
        
        
        #join
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.view_layer.objects.active = bpy.data.objects['models.001']
        bpy.data.objects["models.001"].select_set(True)

        bpy.context.view_layer.objects.active = bpy.context.scene['my_obj']['ply']
        bpy.context.scene['my_obj']['ply'].select_set(True)

        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.context.object.vertex_groups.new(name="mouth_cavity_boundary")


        #boundary loop 선택
        bpy.ops.object.mode_set(mode = 'EDIT')    
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group=str("mouth_boundary"))
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.loop_multi_select(ring = False)
        bpy.ops.object.vertex_group_set_active(group=str("mouth_cavity_boundary"))
        bpy.ops.object.vertex_group_select()
       
        bpy.ops.mesh.bridge_edge_loops()
        
        
        return {'FINISHED'}






class OBJECT_OT_check_vertex(Operator, AddObjectHelper):
    bl_idname = "mesh.check_index"
    bl_label = "Check vertex index Object test"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        object_reference = bpy.context.active_object
        get_vertex_data(object_reference)
        get_position(self, context)
        return {'FINISHED'}

