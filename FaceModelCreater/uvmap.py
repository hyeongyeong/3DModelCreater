import bpy

class apply_UVMap(bpy.types.Operator):
    bl_idname = "mesh.apply_uvmap"
    bl_label = "apply_uvmap"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'EDIT')    
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        bpy.ops.object.mode_set(mode = 'OBJECT')    
        #UV_Map_Copy(self, context)
        UV_Map_Paste(self, context)
        return {'FINISHED'}

def UV_Map_Copy(self, context):
    f = open(bpy.context.scene['file_path']['uv_map'], 'w')
    for i in range(0,20207):
        data = str(context.active_object.data.uv_layers.active.data[i].uv.x) + "\n" + str(context.active_object.data.uv_layers.active.data[i].uv.y) +"\n"
        f.write(data)
    return {'FINISHED'}

def UV_Map_Paste(self, context):
    f = open(bpy.context.scene['file_path']['uv_map'], 'r')
    for i in range(0,20207):
        line = f.readline()
        context.active_object.data.uv_layers.active.data[i].uv.x = float(line)
        line = f.readline()
        context.active_object.data.uv_layers.active.data[i].uv.y = float(line)
    return {'FINISHED'}