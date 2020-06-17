bl_info = {
    "name": "Create Eyes",
    "author": "hyeon",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Create eye holes and insert eyes",
    "warning": "",
    "wiki_url": "",
    "category": "Eyes",
}

import bpy
import bmesh
from bpy.types import (Operator, Header, Menu, Panel)
from bpy.props import (FloatVectorProperty, IntProperty, FloatProperty)
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import numpy as np
from math import radians

def delete_object(target) :
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True) # Blender 2.8x
    bpy.ops.object.delete() 

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
        bpy.ops.object.shade_smooth()
        ball = bpy.context.selected_objects[0]
        ball.scale = scale_v
        eyes.append(ball)

        if idx :   
            ball.rotation_euler = rotation_v 
        else :
            ball.rotation_euler = rotation_v * rot_dir

    
    apply_eye_texture(eyes, tex)

def apply_boolean(target , plane, operation, delete) :
    
    # select face model
    bpy.ops.object.mode_set(mode = 'OBJECT')
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

def add_plane(self, context, coord): 
    verts = []
    thickness = 10
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

def toggle_edit_mode(target):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action = 'DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active = target

    bpy.ops.object.mode_set(mode = 'EDIT')
    bm=bmesh.from_edit_mesh(target.data)
    bm.verts.ensure_lookup_table()

    return bm

def create_eye_hole(target, planes):
    for i, p in enumerate(planes) :
        if i == 0 :
            vg_name = "eye_right_boundary"
        else :
            vg_name = "eye_left_boundary"
     
        new_obj = duplicate_obj(target)
        new_p = duplicate_obj(p)
   
        # create eye hole
        apply_boolean(target, p , "DIFFERENCE", True)
        intersect = apply_boolean(new_obj, new_p , "INTERSECT", True)
        
        face_bm = toggle_edit_mode(target).verts

        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.region_to_loop()
        selected_verts = [v for v in face_bm if v.select]
        bpy.ops.mesh.select_all(action = 'DESELECT')
        
        for s in selected_verts:
            for c in intersect.data.vertices:
                if np.array_equal(s.co, c.co):
                    s.select = True
                    break

        vg=bpy.context.object.vertex_groups.new(name=vg_name)
        bpy.ops.object.vertex_group_assign()
        delete_object(new_obj)
               
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
            
            # create_eye_hole(target, planes)
            create_eye_hole(target, planes)

            add_eyeball(self, context, eye_point , eye_texture_path)
            
        except IndexError:
            print("Please select target face mesh!")

        return {'FINISHED'}