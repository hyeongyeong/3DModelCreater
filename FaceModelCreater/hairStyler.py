import bpy
import sys
import numpy
import math
import mathutils

from . hairUtils import *
from mathutils import Vector
from mathutils.geometry import tessellate_polygon


bl_info = {
    "name": "Hair_styler",
    "blender": (2, 80, 0),
    "category": "Object",
}


class Hair_styler(bpy.types.Operator):
    """Hair styler"""      
    bl_idname = "mesh.hair_styler"
    bl_label = "add hair"
    bl_options = {'REGISTER', 'UNDO'} 
        
    STYLER_MODE = [
        #"eye_brow_r",
        #"eye_brow_l",
        #"mustache",
        #"beard",
        #"eye_left_boundary",
        #"eye_right_boundary",
        "hair"
    ]
    NAME_HEAD = "Man"

    def execute(self, context):

        for mode in self.STYLER_MODE:
            print("[[INFO]] Styling Hair system : MODE [%s] .... " % mode)
            self.do_styling(mode)

        return {"FINISHED"}


    def do_styling(self, STYLER_MODE):

        head = utils_select_obj(target=self.NAME_HEAD)
        if head == None:
            head = bpy.context.view_layer.objects.active
        option = get_styling_option(STYLER_MODE, head)
        utils_add_particle_system(option)

        if option["style_path"] != "":
            preset = load_preset(option)
        else:
            preset = generate_style(option, scalp_tris=self.get_scalp_tris(option, head)) # TODO
        
        self.init_styling(option)
        if option["styling_process"] == True:
            style = self.generate_custom_style(option, preset)
            self.comb(option, style)
        else:
            self.comb(option, preset)
        self.finalize_styling(option)


    ######################## Custom #####################################
    def generate_custom_style(self, option, full_hair):
        head = option["head"]
        scale, coord_scalp, coord_hair = self.get_transform(option, full_hair, head)
        print(scale, coord_scalp, coord_hair)
        guide_hair = []
        for selected in full_hair:
            if len(guide_hair) == option["num_particle"]:
                break
            
            for i in range(len(selected)):
                selected[i] = transform(selected[i], coord_hair, coord_scalp, scale)

            num_sample = len(selected)
            if num_sample > option["hair_step"]:
                num_sample = option["hair_step"]
            step_idx = sorted( random.sample( range(1,len(selected)), num_sample-1 )    )
            #step_idx = sorted(numpy.random.random_integers(1, len(selected)-1, num_sample-1))
            guide_strand = [selected[0]]
            for step in step_idx:
                guide_strand.append(selected[step])
            guide_strand.append(selected[len(selected)-1])
            guide_hair.append(guide_strand)
        self.fitting_proj(option, guide_hair, head, coord_scalp)
        if option["mode"] == "hair":
            self.fitting_physics(option, guide_hair, head, coord_scalp)
        guide_hair.sort(key=lambda strand:(strand[0][0], strand[0][1], strand[0],[2]))
        
        return guide_hair

    def get_transform(self, option, hair, head):
        root_hair = [Vector(strand[0]) for strand in hair]
        scalp = []
        for v in head.data.vertices :
            for g in v.groups :
                if g.group == head.vertex_groups[option["scalp_name"]].index :
                    if (option["mode"] == "eye_brow_r" or option["mode"] == "eye_brow_l") and v.normal[2] <= 0.2:
                        continue
                    scalp.append(v.co)
        

        coord_hair, scale_hair = self.get_coord(root_hair)
        coord_scalp, scale_scalp = self.get_coord(scalp)
        scale = [scale_scalp[i]/scale_hair[i] for i in range(3)]

        return scale, coord_scalp, coord_hair

    def fitting_proj(self, option, guide_hair, head, coord_scalp):
        root_hair = [Vector(strand[0]) for strand in guide_hair]
        scalp_tris = self.get_scalp_tris(option, head)
        
        for idx, root in enumerate(root_hair):
            intersected = False
            ray = root - coord_scalp
            tri = None
            for tri in scalp_tris:
                if mathutils.geometry.intersect_ray_tri(tri[0], tri[1], tri[2], ray, coord_scalp) != None:
                    intersected = True
                    break
    
            if intersected == False:
                nearest_idx = find_nearest_point(root, scalp_tris)
                tri = scalp_tris[nearest_idx]


            center = get_center(tri=tri, gitter=True)
            for v in range(len(guide_hair[idx])):            
                guide_hair[idx][v] = Vector([ guide_hair[idx][v][i] - root[i] + center[i] for i in range(3) ])

        return 


    def fitting_physics(self, option, guided_hair, model, coord_scalp):
        for hair_idx, strand in enumerate(guided_hair):
            print(hair_idx, len(guided_hair))
            for m in range(1, len(strand)):
                iter = 0
                length = (strand[m]-strand[m-1]).length
                while iter<4000:
                    result, n = is_inside(strand[m], coord_scalp, model)
                    if result == True:
                        new = strand[m] + (strand[m]-coord_scalp)*0.05 - strand[m-1]
                        new.normalize()
                        strand[m] = strand[m-1]+length*new
                        iter += 1
                    else:
                        break
            strand[0] = strand[0] + (strand[0]-coord_scalp)*0.05


    def get_scalp_tris(self, option, head):
        scalp_tris = []
        scalp_idx = head.vertex_groups[option["scalp_name"]].index

        for poly in head.data.polygons:
            all_include = True
            for v_idx in poly.vertices:
                v = head.data.vertices[v_idx]
                is_include = False
                for g in v.groups:
                    if g.group == scalp_idx:
                        is_include = True
                        break
                
                if is_include == False:
                    all_include = False
                    break
            if all_include == True:
                polygon = [head.data.vertices[vi].co for vi in poly.vertices]
                normal = [head.data.vertices[vi].normal for vi in poly.vertices]
                if (option["mode"] == "eye_brow_r" or option["mode"] == "eye_brow_l") and test_normal_dir(normal) == False:
                    continue
                tess = tessellate_polygon((polygon,))
                for tri in tess:
                    scalp_tris.append([polygon[tri[0]], polygon[tri[1]], polygon[tri[2]]])

        return scalp_tris

    def get_coord(self, obj):
        # Guided hair scaling
        coord = Vector((0.0, 0.0, 0.0))
        for data in obj:
            coord += Vector(data)
        coord = coord / len(obj)

        scale = Vector((0.0, 0.0, 0.0))
        for data in obj:
            scale += Vector((math.sqrt((data[i]-coord[i])**2) for i in range(3)))
        scale = scale/len(obj)

        return coord, scale

    #################### Styling method ##################################

    def init_styling(self, option):
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
    
        

    def comb(self, option, style):     
        head = option["head"]
        psys_name = option["psys_name"]
        deps_graph = bpy.context.evaluated_depsgraph_get()
        deps_obj = head.evaluated_get(deps_graph)
        psys = deps_obj.particle_systems[psys_name]
        for i in range(len(psys.particles)):
            style_idx = i
            if i >= len(style):
                style_idx = len(style)-1
            part = psys.particles[i]
            strand = style[style_idx]
            part.location = strand[0]

            for m in range(len(part.hair_keys)):
                strand_m = m
                if m >= len(strand):
                    strand_m = len(strand)-1
                key = part.hair_keys[m]
                key.co = strand[strand_m]

    def finalize_styling(self, option):
        bpy.ops.particle.particle_edit_toggle()
        bpy.ops.particle.particle_edit_toggle()
        bpy.ops.object.mode_set(mode="OBJECT")

        deps_graph = bpy.context.evaluated_depsgraph_get()
        deps_graph.update()

        set_child(option)
        set_physics(option)  


def register():
    bpy.utils.register_class(Hair_styler)


def unregister():
    bpy.utils.unregister_class(Hair_styler)
    
if __name__ == "__main__":
    register()
