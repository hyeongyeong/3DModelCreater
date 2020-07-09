import bpy

class MESH_OT_apply_texturing(bpy.types.Operator):
    bl_idname = "mesh.apply_texturing"
    bl_label = "apply_texturing"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
       texturing(self,context)
       return {'FINISHED'}

def create_face_group(context,operator,group_name):
         ###############################
        bpy.context.scene.use_nodes = True
        
        Face_Skin_Group = bpy.data.node_groups.new(group_name,'ShaderNodeTree')

        TexCoord_wrinkle = Face_Skin_Group.nodes.new('ShaderNodeTexCoord')
        TexCoord_wrinkle.location = (0,0)
        TexCoord_wrinkle.object =   bpy.context.scene['my_obj']['ply']
        Mapping_wrinkle = Face_Skin_Group.nodes.new('ShaderNodeMapping')
        Mapping_wrinkle.inputs[1].default_value[0] = 0.5
        Mapping_wrinkle.inputs[1].default_value[1] = 0.25
        Mapping_wrinkle.inputs[3].default_value[0] = 0.009
        Mapping_wrinkle.inputs[3].default_value[1] = 0.008
        Mapping_wrinkle.inputs[3].default_value[2] = 0
        Mapping_wrinkle.location = (300,0)
        Teximage_wrinkle = Face_Skin_Group.nodes.new('ShaderNodeTexImage')
        Teximage_wrinkle.image = bpy.data.images.load(bpy.context.scene['file_path']['wrinkle_texture'])
        Teximage_wrinkle.location = (600,0)
        BrightContrast_wrinkle = Face_Skin_Group.nodes.new('ShaderNodeBrightContrast')
        BrightContrast_wrinkle.inputs[1].default_value = 0.15
        BrightContrast_wrinkle.inputs[2].default_value = 1
        BrightContrast_wrinkle.location = (900,0)
        ColorRamp_wrinkle = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
        ColorRamp_wrinkle.color_ramp.elements[0].color = (0, 0, 0, 1)
        ColorRamp_wrinkle.color_ramp.elements[0].position = 0
        ColorRamp_wrinkle.color_ramp.elements[1].color = (1, 1, 1, 0)
        ColorRamp_wrinkle.color_ramp.elements[1].position = 0.5
        ColorRamp_wrinkle.location = (1200,0)
        Math_wrinkle = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
        Math_wrinkle.blend_type='MULTIPLY'
        Math_wrinkle.inputs[0].default_value = 0
        Math_wrinkle.location = (1500,0)
        Bump = Face_Skin_Group.nodes.new('ShaderNodeBump')
        Bump.inputs[0].default_value = 0.1
        Bump.inputs[1].default_value = 0.1
        Bump.location = (1800,150)
        ColorRamp_roughness = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
        ColorRamp_roughness.color_ramp.elements[0].color = (1, 1, 1, 1)
        ColorRamp_roughness.color_ramp.elements[0].position = 0
        ColorRamp_roughness.color_ramp.elements[1].color = (0, 0, 0, 1)
        ColorRamp_roughness.color_ramp.elements[1].position = 0.7
        ColorRamp_roughness.location = (1800,450)
        UVMap_face = Face_Skin_Group.nodes.new('ShaderNodeUVMap')
        UVMap_face.uv_map = "UVMap"
        UVMap_face.location = (900,750)
        Teximage_face = Face_Skin_Group.nodes.new('ShaderNodeTexImage')
        Teximage_face.image = bpy.data.images.load(bpy.context.scene['file_path']['face_texture'])
        Teximage_face.location = (1200,750)
        Group_input = Face_Skin_Group.nodes.new('NodeGroupInput')
        Group_input.location = (0,450)
        Group_output = Face_Skin_Group.nodes.new('NodeGroupOutput')
        Group_output.location = (2100,450)
        Face_Skin_Group.links.new(Mapping_wrinkle.inputs[0], TexCoord_wrinkle.outputs[3])
        Face_Skin_Group.links.new(Teximage_wrinkle.inputs[0], Mapping_wrinkle.outputs[0])
        Face_Skin_Group.links.new(BrightContrast_wrinkle.inputs[0],Teximage_wrinkle.outputs[0])
        Face_Skin_Group.links.new(ColorRamp_wrinkle.inputs[0],BrightContrast_wrinkle.outputs[0])
        Face_Skin_Group.links.new(Teximage_face.inputs[0],UVMap_face.outputs[0])
        Face_Skin_Group.links.new(Group_output.inputs[0],Teximage_face.outputs[0])
        #Face_Skin_Group.links.new(Math_wrinkle.inputs[0],Group_input.outputs[0])
        Face_Skin_Group.links.new(BrightContrast_wrinkle.inputs[2],Group_input.outputs[0])
        Face_Skin_Group.links.new(Math_wrinkle.inputs[1],Teximage_face.outputs[0])
        Face_Skin_Group.links.new(Math_wrinkle.inputs[2],ColorRamp_wrinkle.outputs[0])
        Face_Skin_Group.links.new(ColorRamp_roughness.inputs[0],Math_wrinkle.outputs[0])
        Face_Skin_Group.links.new(Bump.inputs[0],Group_input.outputs[1])
        Face_Skin_Group.links.new(Bump.inputs[1],Group_input.outputs[2])
        Face_Skin_Group.links.new(Bump.inputs[2],Math_wrinkle.outputs[0])
        Face_Skin_Group.links.new(Group_output.inputs[1],ColorRamp_roughness.outputs[0])
        Face_Skin_Group.links.new(Group_output.inputs[2],Bump.outputs[0])
        Face_Skin_Group.links.new(Mapping_wrinkle.inputs[1],Group_input.outputs[3])
        Face_Skin_Group.links.new(Mapping_wrinkle.inputs[3],Group_input.outputs[4])

        return Face_Skin_Group

def texturing(self,context):
    objs = bpy.context.scene['my_obj']['ply'].data 
    f_face= open(bpy.context.scene['file_path']['skin_tex'],"r")
    face_R = []
    face_G = []
    face_B = []
    while True:
        line_face = f_face.readline()
    
        if not line_face:
            break
        split_face = line_face.split()
        face_R.append(float(split_face[0])/255) # always 1
        face_G.append(float(split_face[1])/255)
        face_B.append(float(split_face[2])/255)
    f_face.close()    

    ########### body ###############
    material_body = bpy.data.materials.new("Body")
    material_body.use_nodes = True

    TexCoord = material_body.node_tree.nodes.new('ShaderNodeTexCoord')
    TexCoord.location = (0,0)
    TexCoord.object =   bpy.context.scene['my_obj']['ply']
    Mapping_color = material_body.node_tree.nodes.new('ShaderNodeMapping')
    Mapping_color.inputs[1].default_value[0] = -0.5
    Mapping_color.inputs[1].default_value[1] = -0.1
    Mapping_color.inputs[3].default_value[0] = 0.0008
    Mapping_color.inputs[3].default_value[1] = 0.0008
    Mapping_color.inputs[3].default_value[2] = 0
    Mapping_color.location = (300,300)
    Mapping_skin = material_body.node_tree.nodes.new('ShaderNodeMapping')
    Mapping_skin.inputs[3].default_value[0] = 80
    Mapping_skin.inputs[3].default_value[1] = 80
    Mapping_skin.inputs[3].default_value[2] = 0
    Mapping_skin.location = (300,-100)
    Teximage_color = material_body.node_tree.nodes.new('ShaderNodeTexImage')
    Teximage_color.image = bpy.data.images.load(bpy.context.scene['file_path']['face_texture'])
    Teximage_color.location = (600,300)
    Teximage_skin = material_body.node_tree.nodes.new('ShaderNodeTexImage')
    Teximage_skin.image = bpy.data.images.load(bpy.context.scene['file_path']['body_texture'])
    Teximage_skin.location = (600,0)
    Bump = material_body.node_tree.nodes.new('ShaderNodeBump')
    Bump.inputs[0].default_value = 0.2
    Bump.inputs[1].default_value = 0.2
    Bump.location = (900,-100)
    ColorRamp_roughness = material_body.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_roughness.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_roughness.color_ramp.elements[0].position = 0
    ColorRamp_roughness.color_ramp.elements[1].color = (0, 0, 0, 1)
    ColorRamp_roughness.color_ramp.elements[1].position = 0.5
    ColorRamp_roughness.location = (900,200)
    BSDF = material_body.node_tree.nodes.get('Principled BSDF')
    BSDF.inputs[1].default_value=0
    BSDF.location = (1200,300)
    Output_body = material_body.node_tree.nodes.get('Material Output')
    Output_body.location = (1500,0)
    material_body.node_tree.links.new(Mapping_color.inputs[0], TexCoord.outputs[3])
    material_body.node_tree.links.new(Mapping_skin.inputs[0], TexCoord.outputs[0])
    material_body.node_tree.links.new(Teximage_color.inputs[0], Mapping_color.outputs[0])
    material_body.node_tree.links.new(Teximage_skin.inputs[0], Mapping_skin.outputs[0])
    material_body.node_tree.links.new(BSDF.inputs[0], Teximage_color.outputs[0])
    material_body.node_tree.links.new(ColorRamp_roughness.inputs[0], Teximage_skin.outputs[0])
    material_body.node_tree.links.new(Bump.inputs[2], Teximage_skin.outputs[0])
    material_body.node_tree.links.new(BSDF.inputs[7], ColorRamp_roughness.outputs[0])
    material_body.node_tree.links.new(BSDF.inputs[19], Bump.outputs[0])
    
    bpy.context.object.active_material_index = 0
    bpy.context.object.active_material = material_body

    ##############face ####################
    group_face_texture=create_face_group(self,context,'face_texture')
    material_face = bpy.data.materials.new("Face")
    material_face.use_nodes = True
    face_texture_group =  material_face.node_tree.nodes.new('ShaderNodeGroup')
    face_texture_group.node_tree = bpy.data.node_groups[group_face_texture.name]
    face_texture_group.location = (-300,0)
    face_texture_group.inputs[0].default_value = 1
    BSDF = material_face.node_tree.nodes.get('Principled BSDF')
    BSDF.inputs[1].default_value=0
    material_face.node_tree.links.new(BSDF.inputs[0], face_texture_group.outputs[0])
    material_face.node_tree.links.new(BSDF.inputs[7], face_texture_group.outputs[1])
    material_face.node_tree.links.new(BSDF.inputs[19], face_texture_group.outputs[2])
    bpy.context.object.active_material_index = 1
    bpy.context.object.active_material = material_face
    bpy.ops.object.mode_set(mode = 'OBJECT')


    #select eyebrow area
    bpy.ops.object.mode_set(mode = 'EDIT')    
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("face_edge"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)

    bpy.ops.object.material_slot_add()

    material_face_edge = bpy.data.materials.new("Face_edge")
    material_face_edge.use_nodes = True
    bpy.context.object.active_material_index = 2
    bpy.context.object.active_material = material_body
    bpy.ops.object.material_slot_assign()

    bpy.ops.object.mode_set(mode = 'OBJECT')