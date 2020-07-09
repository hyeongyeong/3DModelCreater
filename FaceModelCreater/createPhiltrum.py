import bpy

class MESH_OT_create_philtrum(bpy.types.Operator):
    bl_idname = "mesh.create_philtrum"
    bl_label = "apply_creating"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
       creating_philtrum()
       return {'FINISHED'}


def creating_philtrum():
    bpy.ops.object.mode_set(mode = 'EDIT')    
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("philtrum"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.translate(value=(0,2,-2), constraint_axis=(False, False, False),mirror=False, use_proportional_edit = True,use_proportional_connected=True,proportional_edit_falloff='SMOOTH',proportional_size=7)

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("lips_top"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.translate(value=(0,0,0.5), constraint_axis=(False, False, False),mirror=False, use_proportional_edit = True,use_proportional_connected=True,proportional_edit_falloff='SMOOTH',proportional_size=5)
    bpy.ops.transform.translate(value=(0,-2,0), constraint_axis=(False, False, False),mirror=False, use_proportional_edit = True,use_proportional_connected=True,proportional_edit_falloff='SMOOTH',proportional_size=5)
    
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("eye_top"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.translate(value=(0,0,-1), constraint_axis=(False, False, False),mirror=False, use_proportional_edit = True,use_proportional_connected=True,proportional_edit_falloff='SMOOTH',proportional_size=16)
    bpy.ops.transform.translate(value=(0,0,-1), constraint_axis=(False, False, False),mirror=False, use_proportional_edit = True,use_proportional_connected=True,proportional_edit_falloff='SMOOTH',proportional_size=13)
    bpy.ops.transform.translate(value=(0,-0.3,2), constraint_axis=(False, False, False),mirror=False, use_proportional_edit = True,use_proportional_connected=True,proportional_edit_falloff='SMOOTH',proportional_size=10)
    
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("eye_bot"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.translate(value=(0,0,0.5), constraint_axis=(False, False, False),mirror=False, use_proportional_edit = True,use_proportional_connected=True,proportional_edit_falloff='SMOOTH',proportional_size=5)
    
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')