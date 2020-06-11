
import sys
import random
import pickle
import os
import bpy
from mathutils import Vector
from mathutils.geometry import area_tri, normal


#############################################################################
###################### Style ################################################
#############################################################################


def get_styling_option(STYLER_MODE, head):

    option = {}
    option["eye_brow_l"] = {
            "mode":STYLER_MODE,
            "head":head,
            "scalp_name":STYLER_MODE,
            "style_path":"",
            "material":utils_select_material(head, "material_" + STYLER_MODE),
            "psys_name":"auto_" + STYLER_MODE,
            "num_particle": 150,
            "hair_step":14,
            "physics":False,
            "static_scalp":True,
            "proj_dir":True,
            
            # Child
            "child":False,
            "child_radius":3
    }

    option["eye_brow_r"] = {
            "mode":STYLER_MODE,
            "head":head,
            "scalp_name":STYLER_MODE,
            "style_path":"",#os.getcwd()+"/FaceModelCreater/backup/custom_" + STYLER_MODE + ".pk",
            "material":utils_select_material(head, "material_" + STYLER_MODE),
            "psys_name":"auto_" + STYLER_MODE,
            "num_particle": 150,
            "hair_step":14,
            "physics":False,
            "static_scalp":True,
            "proj_dir":True,
            
            # Child
            "child":False,
            "child_radius":3
                
    }

    option["mustache"] = {
            "mode":STYLER_MODE,
            "head":head,
            "scalp_name":STYLER_MODE,
            "style_path":"",
            "material":utils_select_material(head, "material_" + STYLER_MODE),
            "psys_name":"auto_" + STYLER_MODE,
            "num_particle": 200,
            "hair_step":10,
            "physics":False,
            "static_scalp":True,
            "proj_dir":True,
            
            # Child
            "child":False,
            "child_radius":3            
    }

    option["beard"] = {
            "mode":STYLER_MODE,
            "head":head,
            "scalp_name":STYLER_MODE,
            "style_path":"",
            "material":utils_select_material(head, "material_" + STYLER_MODE),
            "psys_name":"auto_" + STYLER_MODE,
            "num_particle": 500,
            "hair_step":10,
            "physics":False,
            "static_scalp":True,
            "proj_dir":True,
            
            # Child
            "child":False,
            "child_radius":3
                    
    }

    option["hair"] = {
            "mode":STYLER_MODE,
            "head":head,
            "scalp_name":STYLER_MODE,
            "style_path":"",
            "material":utils_select_material(head, "material_" + STYLER_MODE),
            "psys_name":"auto_" + STYLER_MODE,
            "num_particle": 500,
            "hair_step":10,
            "physics":False,
            "static_scalp":True,
            "proj_dir":True,
            
            # Child
            "child":False,
            "child_radius":3
                    
    }

    if STYLER_MODE not in option:    
        print("[[ERR]] MODE error")
        sys.exit(1)
    else:
        return option[STYLER_MODE]


def load_preset(option):
    
    with open(option["style_path"], "rb") as fp:
        full_hair = pickle.load(fp)
    random.shuffle(full_hair)
    print(len(full_hair))
    return full_hair
    

#############################################################################
###################### Graphics Tools #######################################
#############################################################################


def test_normal_dir(normals, threshold=0.2, direction=[0,0,1]):

    dir = 0
    for i, d in enumerate(direction):
        if d == 1:
            dir = i

    for n in normals:
        if n[dir] < threshold:
            return False
    return True

    
def is_inside(p1, p2, model):
    
    origin = p1
    dir = p2 - p1
    dist = (p2 - p1).length
    result = model.ray_cast(origin, dir, distance=dist)
    n = Vector((0, result[2][1], result[2][2]))
    return result[0], n


def find_nearest_point(root, scalp_tris):
    min_idx = 0
    min_v = 10000000000
    for i, tri in enumerate(scalp_tris):
        center = Vector([ (tri[0][i]+tri[1][i]+tri[2][i])/3 for i in range(3) ])    
        dis = (root-center).length
        if dis < min_v:
            min_v = dis
            min_idx = i
        
    return min_idx    

    
def transform(point, hair_move, scalp_move, v_scale):
    point = Vector([ 
                (point[0] - hair_move[0])*v_scale[0] + scalp_move[0],
                (point[1] - hair_move[1])*v_scale[1] + scalp_move[1],
                (point[2] - hair_move[2])*v_scale[2] + scalp_move[2]
            ])
    return point

def get_center(tri, gitter=False):

    if gitter == False:
        return Vector([ (tri[0][i]+tri[1][i]+tri[2][i])/3 for i in range(3) ]) # add jitter
    else:
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        c = random.randint(1, 5)   
        return Vector([ (tri[0][i]*a+tri[1][i]*b+tri[2][i]*c)/(a+b+c) for i in range(3) ]) # add jitter


#############################################################################
###################### Bledner Tools #######################################
#############################################################################


def utils_select_obj(target):
    obj = None
    for obj in bpy.data.objects:
        if obj.name.find(target) != -1:
            break
        else :
            obj = None
    bpy.context.view_layer.objects.active = obj
    return obj
    

def utils_add_particle_system(option):
    head = option["head"]
    psys_name = option["psys_name"]
    bpy.ops.object.mode_set(mode="OBJECT")
        
    if psys_name in head.particle_systems:
        head.modifiers.remove(head.modifiers.get(psys_name))
    head.modifiers.new(psys_name, "PARTICLE_SYSTEM")
    head.particle_systems[-1].name = psys_name
    psys = head.particle_systems[psys_name]

    # Setting - generate
    psys.settings.type = "HAIR"
    psys.settings.render_step = 5
    psys.settings.display_step = 3
    psys.settings.hair_length = 4.0
    psys.settings.count = option["num_particle"]
    psys.settings.hair_step = option["hair_step"]
    psys.settings.emit_from = "FACE"
    psys.settings.use_strand_primitive = True
    
    # Setting - color
    mat_hair = option["material"]
    psys.settings.material_slot = mat_hair.name
    
    return psys


def set_child(option):
    if option["child"] == True:
        head = option["head"]
        psys_name = option["psys_name"]
        psys = head.particle_systems[psys_name]
        psys.settings.child_type = "SIMPLE"
        psys.settings.child_nbr = 4
        psys.settings.rendered_child_count = 4
        psys.settings.child_length = 1.0
        psys.settings.child_length_threshold = 0.0
        psys.settings.child_radius = option["child_radius"]
        psys.settings.child_roundness = 1.0    
            
def set_physics(option):        
    head = option["head"]
    psys_name = option["psys_name"]
    psys = head.particle_systems[psys_name]
    if option["physics"] == True:
        psys.use_hair_dynamics = option["physics"]
        psys.cloth.settings.pin_stiffness = 0.5        
    else:
        psys.use_hair_dynamics = False




def utils_select_material(head, mat_name):
    mat_hair = None
    for mat in head.data.materials:
        if mat.name.find(mat_name) != -1:
            mat_hair = mat
            break
    if mat_hair == None:
        mat_hair = bpy.data.materials.new(name = mat_name)
        mat_hair.diffuse_color = (0.01, 0.01, 0.01, 0)
        head.data.materials.append(mat_hair)
    return mat_hair


#############################################################################
###################### Debugging tools ######################################
#############################################################################



def add_cube(xyz, idx=1):
    temp = bpy.context.active_object
    size = 0.5
    if idx == 0:
        size = 0.2
    bpy.ops.mesh.primitive_cube_add(location=(xyz[0], xyz[1], xyz[2]), size=size)
    obj = bpy.context.active_object
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = temp

def generate_style(option, scalp_tris=None, num_root=700, num_vtx=100):
    mode = option["mode"]
    path_store=os.getcwd()+"/FaceModelCreater/backup/%s.pk" % (mode)
    fp = open(path_store, "wb")
    roots = []
    normals = []
    total_area = 0.0
    min_x, max_x = 1000000000, 0
    for tri in scalp_tris:
        total_area += area_tri(tri[0], tri[1], tri[2]) 
        for p in tri:
            if p[0] < min_x:
                min_x = p[0]
            if p[0] > max_x:
                max_x = p[0]
    root_per_area = num_root/total_area
    
    if mode == "eye_brow_l":
        force = Vector((100, -9.8, -50))
        length = (max_x-min_x)/(num_vtx*10)
    elif mode == "eye_brow_r":
        force = Vector((-100, -9.8, -50))
        length = (max_x-min_x)/(num_vtx*10)
    elif mode == "mustache":
        force = Vector((0, -98, -15))
        length = (max_x-min_x)/(num_vtx*10)
    elif mode == "beard":
        force = Vector((0, -98, -15))
        length = (max_x-min_x)/(num_vtx*10)
    else:
        force = Vector((0,0,0))
    force.normalize()
    print(length)

    for tri in scalp_tris:
        num = int(root_per_area * area_tri(tri[0], tri[1], tri[2]))
        num = 1 if num == 0 else num
        for _ in range(num):
            roots.append( get_center(tri, gitter=True) )
            normals.append( normal(tri) )

    print("num root: %d" % len(roots))
    
    guide_hair = []
    for i, root in enumerate(roots):
        n = normals[i]
        strand = [root]
        for m in range(1, num_vtx):
            prev = strand[-1]
            dir = (n + force*(m))
            dir.normalize()
            dir = random.uniform(0.6,1.0)*length*dir
            strand.append(prev + dir)

        guide_hair.append(strand)
    random.shuffle(guide_hair)


    for i, strand in enumerate(guide_hair):
        for m, v in enumerate(strand):
            guide_hair[i][m] = list(v)
    pickle.dump(guide_hair, fp)
    fp.close()
    return guide_hair

def print_style(model, psys_name="") :
    deps_graph = bpy.context.evaluated_depsgraph_get()
    head = model.evaluated_get(deps_graph)
    psys = head.particle_systems["auto_" + psys_name]
    parts = []
    for i in range(len(psys.particles)):
        part = psys.particles[i]
        hair_keys = []
        for m in range(len(part.hair_keys)):
            key = part.hair_keys[m]
            hair_keys.append(list(key.co_local))
        parts.append( [list(part.location), hair_keys] )        

    with open(os.getcwd()+"/FaceModelCreater/backup/custom_" + psys_name + ".pk", "wb") as fp:
        print(os.getcwd()+"/FaceModelCreater/backup/custom_" + psys_name + ".pk")
        pickle.dump(parts, fp)

    '''
    mode = option["mode"]
    full_hair = []
    if mode == "eye_brow_l":
        direct = 1 if option["mode"] == "eye_brow_l" else -1
        for i in range(10000):            
            strand = []
            y_rand = random.randint(-100, 100)
            for m in range(100):
                x = i/4+11 + m*m*direct/100
                y = (10000-i)*i/(6*6) + i%6 + (1e-4*m+1)*y_rand*m
                z = ((i)**2)*(-1)*1e-1+(1600-(m-40)**2)*1e+2
                strand.append((x,y,z))
            full_hair.append(strand)

    elif mode == "eye_brow_r":
        direct = 1 if option["mode"] == "eye_brow_l" else -1
        for i in range(10000):            
            strand = []
            y_rand = random.randint(-100, 100)
            for m in range(100):
                x = i/4+11 + m*m*direct/100
                y = (10000-i)*i/(6*6) + i%6 + (1e-4*m+1)*y_rand*m 
                z = ((10000-i)**2)*(-1)*1e-1+(1600-(m-40)**2)*1e+2
                strand.append((x,y,z))
            full_hair.append(strand)

    elif mode == "mustache":

        for i in range(10000):            
            strand = []
            y_rand = random.randint(-10, 10)
            length = random.uniform(0.9, 1.0)
            for m in range(100):
                strand.append((i/2+11, i%2+11+y_rand+(m*y_rand*0.001-m*m)*(1e-5), length*(1+(360-(m-60)**2)*(1e-7))  ))
            full_hair.append(strand)
        
    elif mode == "beard":
                        
        for i in range(10000):            
            strand = []
            y_rand = random.randint(-10, 10)
            length = random.uniform(0.9, 1.0)
            for m in range(100):
                strand.append((i/2+11, i%2+11+y_rand+(m*y_rand*0.001-m*m)*(1e-5), length*(1+(360-(m-60)**2)*(1e-7))  ))
            full_hair.append(strand)
        
    elif mode == "hair":
        for i in range(10000):            
            strand = []
            y_rand = random.randint(-10, 10)
            length = random.uniform(0.9, 1.0)
            for m in range(100):
                strand.append((0,0,0))
            full_hair.append(strand)

    else:
        print("[[ERR]] MODE error")
        sys.exit(1)

    return full_hair
    '''