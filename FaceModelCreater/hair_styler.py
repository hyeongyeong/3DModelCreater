
import bpy

bl_info = {
    "name": "Hair_styler",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import sys
import pickle
import random
import numpy
import math
import mathutils
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

class Hair_styler(bpy.types.Operator):
    """Hair styler"""      
    bl_idname = "mesh.hair_styler"
    bl_label = "add hair"
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        MODE = [
                "eye_brow_r",
                #"mustache",
                "eye_brow_l",
                #"beard",
                #"hair"
                ]
                
        for mode in MODE:
            print("Styling " + mode + " ....")
            self.styling(mode)

            
        return {'FINISHED'}      

    def styling(self, MODE):

        head = self._select_obj("hee_f")
        option = self._get_option(MODE, head)

        self._add_psys(option)
        style = self._load_style(option)
        psys = self._init_styling(option)
        
        ### Styling
        
        for i in range(len(psys.particles)):
            part = psys.particles[i]
            strand = style[i]
            part.location = strand[0]
            
            for m in range(len(part.hair_keys)):
                key = part.hair_keys[m]
                key.co = strand[m]
        
        self._finalize_styling(option)
        self._set_child(option)
        self._set_physics(option)   
        

    ################ Styling ######################        

    def _add_psys(self, option):
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
        psys.settings.display_step = 5
        psys.settings.hair_length = 4.0
        psys.settings.count = option["num_particle"]
        psys.settings.hair_step = option["hair_step"]
        psys.settings.emit_from = "FACE"
        psys.settings.use_strand_primitive = True
        
        # Setting - color
        mat_hair = option["material"]
        psys.settings.material_slot = mat_hair.name
        

    def _load_style(self, option):

        guide_hair = []
        head = option["head"]
        psys = head.particle_systems[option["psys_name"]]
        full_hair = self._data_load(option)

            
            
        v_scale, scalp_move, hair_move = self._hair_matching(option, full_hair, head)        
        num_selected = 0
        step_idxs = sorted(numpy.random.random_integers(1, 98, option["hair_step"]-1))
        random.shuffle(full_hair)
        for selected in full_hair:
            if num_selected >= option["num_particle"]:
                break
            
            if len(selected) != 100:
                continue
            
            num_selected += 1
            
            for i in range(100):
                selected[i] = self._move(selected[i], hair_move, scalp_move, v_scale)
                
            guide_strand = [selected[0]]
            for step_idx in step_idxs:
                guide_strand.append(selected[step_idx])
            guide_strand.append(selected[99])
            guide_hair.append(guide_strand)
        
        
        self._fit_proj(option, guide_hair, head, scalp_move)
        #if option["mode"] == "hair":
        #    self._local_fitting(option, guide_hair, head)


        guide_hair.sort(key=lambda strand:(strand[0][0], strand[0][1], strand[0],[2]))
        
        return guide_hair

    def _init_styling(self,option):
        head = option["head"]
        psys_name = option["psys_name"]
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="PARTICLE_EDIT")
        bpy.context.scene.tool_settings.particle_edit.tool = "COMB"
        bpy.context.scene.tool_settings.particle_edit.brush.count = 1
        if bpy.context.area.type == "VIEW_3D":
            bpy.ops.particle.brush_edit(stroke=[{'name': '', 'location': (0, 0, 0), 'mouse': (0, 0), 'pressure': 0, 'size': 0, 'pen_flip': False, 'time': 0, 'is_start': False}])
        bpy.ops.particle.particle_edit_toggle()
        bpy.context.scene.tool_settings.particle_edit.use_emitter_deflect = True
        bpy.context.scene.tool_settings.particle_edit.use_preserve_root = True
        bpy.context.scene.tool_settings.particle_edit.use_preserve_length = True
        bpy.ops.particle.disconnect_hair(all=True)
        bpy.ops.particle.connect_hair(all=True)  
    
        deps_graph = bpy.context.evaluated_depsgraph_get()
        deps_obj = head.evaluated_get(deps_graph)
        psys = deps_obj.particle_systems[psys_name]
        return psys

    def _finalize_styling(self, option):
        bpy.ops.particle.particle_edit_toggle()
        bpy.ops.particle.particle_edit_toggle()
        bpy.ops.object.mode_set(mode="OBJECT")
        deps_graph = bpy.context.evaluated_depsgraph_get()
        deps_graph.update()


    def _set_child(self, option):
        if option["child"] == True:
            head = option["head"]
            psys_name = option["psys_name"]
            psys = head.particle_systems[psys_name]
            psys.settings.child_type = "SIMPLE"
            psys.settings.child_nbr = 4
            psys.settings.rendered_child_count = 4
            psys.settings.child_length = 1.0
            psys.settings.child_length_threshold = 0.0
            psys.settings.child_radius = 2
            psys.settings.child_roundness = 1.0    
             
    def _set_physics(self, option):        
        head = option["head"]
        psys_name = option["psys_name"]
        psys = head.particle_systems[psys_name]
        if option["physics"] == True:
            psys.use_hair_dynamics = option["physics"]
            psys.cloth.settings.pin_stiffness = 0.5        
        else:
            psys.use_hair_dynamics = False


    ############# matching ##############
    def _hair_matching(self, option, hair, head):
       
        # Guided hair scaling
        hair_m = Vector((0.0, 0.0, 0.0))
        for strand in hair:
            root = Vector(strand[0])
            hair_m = hair_m + root
        hair_m = hair_m / len(hair)

        hair_scale = Vector((0.0, 0.0, 0.0))
        for strand in hair:
            root = Vector(strand[0])
            hair_scale = hair_scale + Vector((math.sqrt((root[i]-hair_m[i])**2) for i in range(3)))

        hair_scale = hair_scale / len(hair)
        hair_scale = [hair_scale[i] if hair_scale[i]!=0 else 0.001 for i in range(3)]
              
        # scalp scaling
        group_idx = head.vertex_groups[option["scalp_name"]].index
        scalp = []
        for v in head.data.vertices:
            for g in v.groups:
                if g.group == group_idx:
                    scalp.append(v.co)
        scalp_m = Vector((0.0, 0.0, 0.0))
        for point in scalp:
            scalp_m = scalp_m + point
        scalp_m = scalp_m/len(scalp)

        scalp_scale = Vector((0.0, 0.0, 0.0))
        for point in scalp:
            scalp_scale = scalp_scale + Vector((math.sqrt((point[i]-scalp_m[i])**2) for i in range(3)))
        scalp_scale = scalp_scale/len(scalp)
    
        scale = [scalp_scale[i] / hair_scale[i] for i in range(3)]
        
        print(scalp_m)
        scalp_m = list(scalp_m)
        print(scalp_m)
        if option["proj_dir"] == True:
            max_v = 0
            for point in scalp :
                if max_v < point[2]:
                    max_v = point[2]
            scalp_m.append(max_v)

        print(scalp_m)
        print(option["mode"])
        print(scale)
        print("scalp")
        print(scalp_scale)
        print(scalp_m)
        print("hair")
        print(hair_scale)
        print(hair_m)
        

        return scale, scalp_m, hair_m

     
    def _fit_proj(self, option, guided_hair, head, scalp_center):
        scalp_tris = []
        root = []
        group_idx = head.vertex_groups[option["scalp_name"]].index

        if option["static_scalp"] == True:
            for poly in head.data.polygons:
                all_include = True
                for v_idx in poly.vertices:
                    v = head.data.vertices[v_idx]
                    is_include = False
                    for g in v.groups:
                        if g.group == group_idx:
                            is_include = True
                            break
                    
                    if is_include == False:
                        all_include = False
                        break
                if all_include == True:
                    polygon = [head.data.vertices[vi].co for vi in poly.vertices]
                    tess = tessellate_polygon((polygon,))
                    for tri in tess:
                        scalp_tris.append( [ polygon[tri[0]], polygon[tri[1]], polygon[tri[2]] ] )
            
        else:
            for poly in head.data.polygons:
                scalp_tris.append( [head.data.vertices[v].co for v in poly.vertices] )
        for strand in guided_hair:
            root.append(strand[0])            
        for idx, p in enumerate(root):
            ray = [p[i]-scalp_center[i] for i in range(3)]
            intersected = False
            for tri in scalp_tris:
                if mathutils.geometry.intersect_ray_tri(tri[0], tri[1], tri[2], ray, scalp_center) != None:
                    a = random.randint(1, 5)
                    b = random.randint(1, 5)
                    c = random.randint(1, 5)
                    center = [ (tri[0][i]*a+tri[1][i]*b+tri[2][i]*c)/(a+b+c) for i in range(3) ] # add jitter
                    for v in range(len(guided_hair[idx])):
                        point = guided_hair[idx][v]                    
                        guided_hair[idx][v] = Vector([ point[i] - p[i] + center[i] for i in range(3) ])
                    intersected = True
                    break
            
            if intersected == False:
                neighbor = self._find_neighbor(p, scalp_tris)
                tri = scalp_tris[neighbor]
                a = random.randint(1, 5)
                b = random.randint(1, 5)
                c = random.randint(1, 5)                
                center = [ (tri[0][i]*a+tri[1][i]*b+tri[2][i]*c)/(a+b+c) for i in range(3) ]    
                for v in range(len(guided_hair[idx])):
                    point = guided_hair[idx][v]                    
                    guided_hair[idx][v] = Vector([ point[i] - p[i] + center[i] for i in range(3) ])



    def _local_fitting(self, option, guided_hair, model):
        
        for hair_idx, strand in enumerate(guided_hair):
            stor = strand[0]
            strand[0] = strand[0]*1.1
            for i in range(0, len(strand)-1):
                p1 = strand[i]
                p2 = strand[i+1]
                length = (p2 - p1).length
                delta = length*0.1
                iter = 0
                while iter<1000:
                    iter += 1
                    result, n = self._is_inside(p1, p2, model)
                    if result == True:
                        p2 = (p2+delta*n)
                        p2 = p1 + ((p2-p1).normalized()*length)
                    else :
                        break
            strand[0] = stor
        
        
    def _is_inside(self, p1, p2, model):
        
        origin = p1
        dir = p2 - p1
        dist = (p2 - p1).length
        result = model.ray_cast(origin, dir, distance=dist)
        n = Vector((0, result[2][1], result[2][2]))
        return result[0], n
                
    def _find_neighbor(self, root, scalp_tris):
        min_idx = 0
        min_v = 10000000000
        for i, tri in enumerate(scalp_tris):
            center = Vector([ (tri[0][i]+tri[1][i]+tri[2][i])/3 for i in range(3) ]) # add jitter    
            dis = (root-center).length
            if dis < min_v:
                min_v = dis
                min_idx = i
            
        return min_idx    

      
    def _move(self, point, hair_move, scalp_move, v_scale):

        strand = Vector([ 
                    (point[0] - hair_move[0])*v_scale[0] + scalp_move[0],
                    (point[1] - hair_move[1])*v_scale[1] + scalp_move[1],
                    (point[2] - hair_move[2])*v_scale[2] + scalp_move[3]
                ])
        return strand      

    ############# utils #################
    def _select_obj(self, target):
        obj = None
        for obj in bpy.data.objects:
            if obj.name.find(target) != -1:
                break
            else :
                obj = None
        bpy.context.view_layer.objects.active = obj
        return obj
    
    def _select_material(self, head, mat_name):
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

    def _get_option(self, mode, head):
        
        ''' 
            MODE list: "eye_brow_l", "eye_brow_r", "mustache", "beard", "hair"
        '''
        option = None
        if mode =="eye_brow_l":
            
            option = {
                "mode":mode,
                "head":head,
                "scalp_name":mode,
                "style_path":"",
                "material":self._select_material(head, "material_" + mode),
                "psys_name":"auto_" + mode,
                "num_particle": 500,
                "hair_step":10,
                "child":True,
                "physics":False,
                "static_scalp":True,
                "proj_dir":True,
            }
            
        elif mode == "eye_brow_r":
                
            option = {
                "mode":mode,
                "head":head,
                "scalp_name":mode,
                "style_path":"",
                "material":self._select_material(head, "material_" + mode),
                "psys_name":"auto_" + mode,
                "num_particle": 500,
                "hair_step":10,
                "child":True,
                "physics":False,
                "static_scalp":True,
                "proj_dir":True,
            }

        elif mode == "mustache":
                            
            option = {
                "mode":mode,
                "head":head,
                "scalp_name":mode,
                "style_path":"",
                "material":self._select_material(head, "material_" + mode),
                "psys_name":"auto_" + mode,
                "num_particle": 200,
                "hair_step":10,
                "child":False,
                "physics":False,
                "static_scalp":True,
                "proj_dir":True,
            }
            
        elif mode == "beard":
                            
            option = {
                "mode":mode,
                "head":head,
                "scalp_name":mode,
                "style_path":"",
                "material":self._select_material(head, "material_" + mode),
                "psys_name":"auto_" + mode,
                "num_particle": 500,
                "hair_step":10,
                "child":False,
                "physics":False,
                "static_scalp":True,
                "proj_dir":True,
            }
            
        elif mode == "hair":
                            
            option = {
                "mode":mode,
                "head":head,
                "scalp_name":mode,
                "style_path":"",
                "material":self._select_material(head, "material_" + mode),
                "psys_name":"auto_" + mode,
                "num_particle": 1000,
                "hair_step":10,
                "child":True,
                "physics":False,
                "static_scalp":True,
                "proj_dir":True,
            }
            
            
        else:
            print("[[ERR]] MODE error")
            sys.exit(1)

        return option

    def _data_load(self, option):
        mode = option["mode"]
        full_hair = []
        if mode == "eye_brow_l":
                        
            direct = 1 if option["mode"] == "eye_brow_l" else -1
            for i in range(10000):            
                strand = []
                y_rand = random.randint(-10, 10)
                for m in range(100):
                    strand.append((i/2+11+m*m*direct/40, i%2+11+y_rand + m*y_rand*0.001, ((5000-i)*(direct)+(360-(m-60)**2)/10)))
                full_hair.append(strand)

        elif mode == "eye_brow_r":
            
            direct = 1 if option["mode"] == "eye_brow_l" else -1
            for i in range(10000):            
                strand = []
                y_rand = random.randint(-10, 10)
                for m in range(100):
                    strand.append((i/2+11+m*m*direct/40, i%2+11+y_rand + m*y_rand*0.001, 0.2*((5000-i)*(direct)+(360-(m-60)**2)/10)))
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
            '''
            pk_f = open(option["style_path"], "rb")
            full_hair = pickle.load(pk_f)
            #pk_f.close()
            '''
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
 
              


def register():
    
    bpy.utils.register_class(Hair_styler)


def unregister():
    bpy.utils.unregister_class(Hair_styler)

if __name__ == "__main__":

    register()