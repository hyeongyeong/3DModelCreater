bl_info = {
    "name": "Region Segmentation",
    "author": "hyeon",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Create Region Vertex group and insert eyes",
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

def make_eye_material(path):
    
    loc = Vector((500,0))
    difference = Vector((300,0))
    
    mat_name = "eye_material"
    
    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True    
    nodes = mat.node_tree.nodes
    
    # handle default 
    nodes.remove(nodes.get('Principled BSDF'))
    material_output = nodes.get('Material Output')
    
    # make new nodes
    diffuse = nodes.new('ShaderNodeBsdfDiffuse')
    hue = nodes.new('ShaderNodeHueSaturation')
    texImage = nodes.new('ShaderNodeTexImage')
    texcoord = nodes.new('ShaderNodeTexCoord')
    
    node_pool = [diffuse, hue, texImage, texcoord]
    
    # edit location of nodes
    material_output.location = loc
    for p in node_pool:
        loc = loc - difference
        p.location = loc
    
    # load text file to texImage
    try :
        image = bpy.data.images.load(path)
        texImage.image = image
    except :
        raise NameError("Cannot load image %s" % path)
        
    # link nodes
    link = mat.node_tree.links
    link.new(texcoord.outputs[0], texImage.inputs[0])
    link.new(texImage.outputs[0],hue.inputs[4])
    link.new(hue.outputs[0],diffuse.inputs[0])
    link.new(material_output.inputs[0], diffuse.outputs[0])
    
    return mat

def apply_eye_texture(eye_meshes, tex):
    
    mat = make_eye_material(tex)
    
    # link material to eye sphere
    for ball in eye_meshes:
        ball.select_set(True)
        ball.active_material = mat
        
def optimize_eye_loc(coord):
    coord_right = coord[0:6] # 2
    coord_left = coord[6:12] # 1

    scale = Vector((19,19,19))
    rot = Vector((radians(15), radians(5), 0))

    right = (coord_right[0].x  + scale.x , coord_right[2].y, (coord_right[2].z + coord_right[4].z)/2 - scale.z )
    left = (coord_left[3].x - scale.x, coord_left[1].y, (coord_left[5].z + coord_left[1].z ) / 2 - scale.z)

    eyes = np.array([right, left, scale, rot])
    
    return eyes

def add_eyeball(self, context, coord, tex):
    
    eyes = []
    
    op = optimize_eye_loc(coord)
    
    right_loc = op[0]
    left_loc = op[1]

    scale_v = op[2]
    rotation_v = op[3]
    rot_dir = Vector((1,-1,1))
 
    loc = [right_loc, left_loc]
     
    for idx, eye in enumerate(loc) :
        bpy.ops.mesh.primitive_uv_sphere_add(location=eye)
        ball = bpy.context.selected_objects[0]
        ball.scale = scale_v
        eyes.append(ball)

        if idx :   
            ball.rotation_euler = rotation_v 
        else :
            ball.rotation_euler = rotation_v * rot_dir

    
    apply_eye_texture(eyes, tex)
    
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

def make_curved_eye_plane(self,context, coord):
    planes = []
    
    points = [coord[0:6], coord[6:12]]
    
    selected_edges = []
    
    subdivided_edges = []
    subdivided_faces = []
    
    ebd = []
    
    right = [
                {'idx': 29, 'edge': None, 'offset': 3.3, 'segments': 5},
                {'idx': 26, 'edge': None, 'offset': 3.3, 'segments': 5},
                {'idx': 23, 'edge': None, 'offset': 3.3, 'segments': 5},
                {'idx': 20, 'edge': None, 'offset': 3.3, 'segments': 5},
            ]
    
    left = [
                {'idx': 26, 'edge': None, 'offset': 3.3, 'segments': 5},
                {'idx': 29, 'edge': None, 'offset': 3.3, 'segments': 5},
                {'idx': 32, 'edge': None, 'offset': 3.3, 'segments': 5},
                {'idx': 18, 'edge': None, 'offset': 3.3, 'segments': 5},
            ]
    
            
    eye_bevel = [right, left]
    
    
    for point_idx, p in enumerate(points):
        point_len = len(p)
        planes.append(add_plane(self,context, p))

        obj = bpy.context.object
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        #error handle
        if obj.mode == 'EDIT' :
            
    #        subdivide edge
            bm=bmesh.from_edit_mesh(obj.data)
            
            selected_edges = [edge for edge in bm.edges if edge.select]
            bmesh.ops.subdivide_edges(bm, edges=selected_edges, cuts=1)
            bmesh.update_edit_mesh(obj.data)
            
            bm.verts.ensure_lookup_table()
            
            for i, vert in enumerate(bm.verts):
                vert.select_set(False)
                if i==12 or i==14 or i==17 or i==20 or i==23 or i==26:
                    vert.select_set(True)
            
            bpy.ops.mesh.delete(type='VERT')
            
            bm.verts.ensure_lookup_table()
            
            # subdivide face
            v=bm.verts
            for i in range(0,point_len):
                if i == point_len - 1:
                    subdivided_faces.append(bm.faces.new([v[i], v[2*i+2*point_len], v[2*i+2*point_len+1], v[i+point_len]]))
                    subdivided_faces.append(bm.faces.new([v[2*i+2*point_len], v[i-point_len+1], v[i+1], v[2*i+2*point_len+1]]))
                else:
                    subdivided_faces.append(bm.faces.new([v[i], v[2*i+2*point_len], v[2*i+2*point_len+1], v[i+point_len]]))
                    subdivided_faces.append(bm.faces.new([v[2*i+point_len*2], v[i+1], v[i+point_len+1], v[2*i+2*point_len+1]]))
           
            bmesh.update_edit_mesh(obj.data)
            
            bm.edges.ensure_lookup_table()
            
            ebd = eye_bevel[point_idx]
            
            # get the edges
            for i in range(len(ebd)):
                ebd[i]['edge'] = bm.edges[ebd[i]['idx']]
            # bevel each edge
            for i in range(len(ebd)):
                e = ebd[i]['edge']
                bev_geom = [e.verts[0], e.verts[1], e]
                o = ebd[i]['offset']
                s = ebd[i]['segments']
                bmesh.ops.bevel(bm, geom=bev_geom, offset=o, segments=s,profile= 0.5,
                vertex_only   = False,
                clamp_overlap = False,
                loop_slide    = True,
                material      = -1,offset_type   = 'OFFSET',)

            
            bmesh.update_edit_mesh(obj.data)
            bpy.ops.object.mode_set(mode = 'OBJECT')

        else:
            print("Object is not in edit mode.")
            
    
    return planes

class MESH_OT_add_eyes(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_eyes"
    bl_label = "Make Eye ball"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
       
        try :
            # TODO : Error output when multiple targets
            bpy.context.scene.cursor.location = (0,0,0)
            planes = []
            landmark_point_file_path = bpy.context.scene['file_path']['point']
            eye_texture_path = bpy.context.scene['file_path']['eye_tex']

            target = bpy.context.scene['my_obj']['ply']
            
            coord = file_read(landmark_point_file_path)
            
            eye_point = coord[20:32]

            planes = make_curved_eye_plane(self, context, eye_point)

            for p in planes :
                # target , plane, operation, delete
                apply_boolean(target, p , "DIFFERENCE", True)

            add_eyeball(self, context, eye_point , eye_texture_path)
            
        except IndexError:
            print("Please select target face mesh!")

        return {'FINISHED'}

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
    