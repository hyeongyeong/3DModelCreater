import bpy
import sys
import numpy

from . hairUtils import *



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
        "eye_brow_r",
        #"mustache",
        "eye_brow_l",
        #"beard",
        #"hair"
    ]
    NAME_HEAD = "hee_f"

    def execute(self, context):

        for mode in self.STYLER_MODE:
            print("[[INFO]] Styling Hair system : MODE [%s] .... ")
            self.do_styling(mode)

        return {"FINISHED"}


    def do_styling(self, STYLER_MODE):

        head = utils_select_obj(target=self.NAME_HEAD)
        option = get_styling_option(STYLER_MODE, head)
        utils_add_particle_system(option)
        preset = load_preset(option)

        style = self.generate_custom_style(option, preset)
        self.init_styling(option)
        self.comb(option, style)
        self.finalize_styling(option)


    ######################## Custom #####################################
    def generate_custom_style(self, option, full_hair):
        head = option["head"]
        step_idx = sorted(numpy.random.random_integers(1, 98, option["hair_step"]-1))
        scale, coord_scalp, coord_hair = self.get_transform(option, full_hair, head)
        
        guide_hair = []
        for selected in full_hair:
            if len(guide_hair) == option["num_particle"]:
                break

            if len(selected) != 100:
                continue

            for i in range(len(selected)):
                selected[i] = transform(selected, coord_hair, coord_scalp, scale)

            guide_strand = [selected[0]]
            for step in step_idx:
                guide_strand.append(selected[step])
            guide_strand[selected[99]]
            guide_hair.append(guide_strand)

        self.fitting_proj(option, guide_hair, head, coord_scalp)
        guide_hair.sort(key=lambda strand:(strand[0][0], strand[0][1], strand[0],[2]))
        return guide_hair

    def get_transform(self, option, hair, head):
        scalp_idx = head.vertex_groups[option["scalp_name"]].index
        root_hair = [Vector(strand[0]) for strand in hair]
        scalp = []
        for v in head.data.vertices :
            for g in v.groups :
                if g.group == group_idx :
                    scalp.append(v.co)

        coord_hair, scale_hair = self.get_info(root_hair)
        coord_scalp, scale_scalp = self.get_info(scalp)
        scale = [scale_scalp[i]/scale_hair[i] for i in range(3)]
        return scale, coord_scalp, coord_hair

    def fitting_proj(self, option, guide_hair, head, coor_scalp):


    def get_coord(obj):
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
            part = psys.particles[i]
            strand = style[i]
            part.location = strand[0]
            
            for m in range(len(part.hair_keys)):
                key = part.hair_keys[m]
                key.co = strand[m]

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
