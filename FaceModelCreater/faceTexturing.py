import bpy

class MESH_OT_apply_texturing(bpy.types.Operator):
    bl_idname = "mesh.apply_texturing"
    bl_label = "apply_texturing"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
        control_face_roughness = 0.7 # 0.5 ~ 1 
        control_face_skin_condition = 0.1
        texturing(control_face_roughness, control_face_skin_condition)
        fun_control_face_roughness(0.8)
        
        return {'FINISHED'}

def fun_control_face_roughness(control_face_roughness):
    bpy.data.materials["Face"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[1].position = control_face_roughness 

def fun_control_face_skin_condition(control_face_skin_condition):
    bpy.data.materials["Face"].node_tree.nodes["Bump"].inputs[0].default_value = control_face_skin_condition 

def fun_control_face_flushing_forehead(control_face_flushing_forehead):
    bpy.data.materials["Face"].node_tree.nodes["Mix.001"].inputs[0].default_value = control_face_flushing_forehead 

def fun_control_face_flushing_cheek(control_face_flushing_cheek):
    bpy.data.materials["Face"].node_tree.nodes["Mix.003"].inputs[0].default_value = control_face_flushing_cheek 

def fun_control_face_flushing_nose(control_face_flushing_nose):
    bpy.data.materials["Face"].node_tree.nodes["Mix.005"].inputs[0].default_value = control_face_flushing_nose

def texturing(control_face_roughness, control_face_skin_condition):
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
    
    material_face = bpy.data.materials.new("Face")
    material_face.use_nodes = True

    Face_Skin_Group = material_face.node_tree

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
    ColorRamp_wrinkle.location = (1200,-400)
    Math_wrinkle = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_wrinkle.blend_type='MULTIPLY'
    Math_wrinkle.inputs[0].default_value = 0
    Math_wrinkle.location = (1500,0)
    Bump = Face_Skin_Group.nodes.new('ShaderNodeBump')
    Bump.inputs[0].default_value = control_face_skin_condition
    Bump.inputs[1].default_value = 0.1
    Bump.location = (1800,-600)
    ColorRamp_roughness = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_roughness.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_roughness.color_ramp.elements[0].position = 0
    ColorRamp_roughness.color_ramp.elements[1].color = (0, 0, 0, 1)
    ColorRamp_roughness.color_ramp.elements[1].position = control_face_roughness
    ColorRamp_roughness.location = (1800,-300)
    UVMap_face = Face_Skin_Group.nodes.new('ShaderNodeUVMap')
    UVMap_face.uv_map = "UVMap"
    UVMap_face.location = (900,200)
    Teximage_face = Face_Skin_Group.nodes.new('ShaderNodeTexImage')
    Teximage_face.image = bpy.data.images.load(bpy.context.scene['file_path']['face_texture'])
    Teximage_face.location = (1200,200)
    Face_Skin_Group.links.new(Mapping_wrinkle.inputs[0], TexCoord_wrinkle.outputs[3])
    Face_Skin_Group.links.new(Teximage_wrinkle.inputs[0], Mapping_wrinkle.outputs[0])
    Face_Skin_Group.links.new(BrightContrast_wrinkle.inputs[0],Teximage_wrinkle.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_wrinkle.inputs[0],BrightContrast_wrinkle.outputs[0])
    Face_Skin_Group.links.new(Teximage_face.inputs[0],UVMap_face.outputs[0])
    Face_Skin_Group.links.new(Math_wrinkle.inputs[1],Teximage_face.outputs[0])
    Face_Skin_Group.links.new(Math_wrinkle.inputs[2],ColorRamp_wrinkle.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_roughness.inputs[0],Math_wrinkle.outputs[0])
    Face_Skin_Group.links.new(Bump.inputs[2],Math_wrinkle.outputs[0])
    
    #flushing - forehead cheek nose
    TexCoord_flushing = Face_Skin_Group.nodes.new('ShaderNodeTexCoord')
    TexCoord_flushing.location = (0,1000)
    TexCoord_flushing.object =   bpy.context.scene['my_obj']['ply']
    Mapping_flushing_base = Face_Skin_Group.nodes.new('ShaderNodeMapping')
    Mapping_flushing_base.location = (200,1600)
    TexGradient_flushing_base = Face_Skin_Group.nodes.new('ShaderNodeTexGradient')
    TexGradient_flushing_base.gradient_type = 'SPHERICAL'
    TexGradient_flushing_base.location = (400,1600)
    ColorRamp_flushing_base = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_flushing_base.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_flushing_base.color_ramp.elements[1].color = (1, 1, 1, 1)
    ColorRamp_flushing_base.location = (600,1600)
    Mapping_flushing_forehead = Face_Skin_Group.nodes.new('ShaderNodeMapping')
    Mapping_flushing_forehead.inputs[1].default_value = (0,-2.2,0)
    Mapping_flushing_forehead.inputs[3].default_value = (0.02,0.03,0)
    Mapping_flushing_forehead.location = (200,1400)
    TexGradient_flushing_forehead = Face_Skin_Group.nodes.new('ShaderNodeTexGradient')
    TexGradient_flushing_forehead.gradient_type = 'SPHERICAL'
    TexGradient_flushing_forehead.location = (400,1400)
    ColorRamp_flushing_forehead = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_flushing_forehead.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_flushing_forehead.color_ramp.elements[1].color = (0, 0, 0, 0.5)
    ColorRamp_flushing_forehead.color_ramp.elements[1].position = 0.8
    ColorRamp_flushing_forehead.location = (600,1400)
    Mapping_flushing_cheek_R = Face_Skin_Group.nodes.new('ShaderNodeMapping')
    Mapping_flushing_cheek_R.inputs[1].default_value = (1.2,0.1,0)
    Mapping_flushing_cheek_R.inputs[3].default_value = (0.03,0.02,0)
    Mapping_flushing_cheek_R.location = (200,1200)
    TexGradient_flushing_cheek_R = Face_Skin_Group.nodes.new('ShaderNodeTexGradient')
    TexGradient_flushing_cheek_R.gradient_type = 'SPHERICAL'
    TexGradient_flushing_cheek_R.location = (400,1200)
    ColorRamp_flushing_cheek_R = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_flushing_cheek_R.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_flushing_cheek_R.color_ramp.elements[1].position = 0.2
    ColorRamp_flushing_cheek_R.color_ramp.elements[1].color = (0, 0, 0, 0.5)
    ColorRamp_flushing_cheek_R.color_ramp.elements[1].position = 0.8
    ColorRamp_flushing_cheek_R.location = (600,1200)
    Mapping_flushing_cheek_L = Face_Skin_Group.nodes.new('ShaderNodeMapping')
    Mapping_flushing_cheek_L.inputs[1].default_value = (-1.2,0.1,0)
    Mapping_flushing_cheek_L.inputs[3].default_value = (0.03,0.02,0)
    Mapping_flushing_cheek_L.location = (200,1000)
    TexGradient_flushing_cheek_L = Face_Skin_Group.nodes.new('ShaderNodeTexGradient')
    TexGradient_flushing_cheek_L.gradient_type = 'SPHERICAL'
    TexGradient_flushing_cheek_L.location = (400,1000)
    ColorRamp_flushing_cheek_L = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_flushing_cheek_L.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_flushing_cheek_L.color_ramp.elements[1].position = 0.2
    ColorRamp_flushing_cheek_L.color_ramp.elements[1].color = (0, 0, 0, 0.5)
    ColorRamp_flushing_cheek_L.color_ramp.elements[1].position = 0.8
    ColorRamp_flushing_cheek_L.location = (600,1000)
    Mapping_flushing_nose_u = Face_Skin_Group.nodes.new('ShaderNodeMapping')
    Mapping_flushing_nose_u.inputs[1].default_value = (0,-0.4,0)
    Mapping_flushing_nose_u.inputs[3].default_value = (0.07,0.03,0)
    Mapping_flushing_nose_u.location = (200,800)
    TexGradient_flushing_nose_u = Face_Skin_Group.nodes.new('ShaderNodeTexGradient')
    TexGradient_flushing_nose_u.gradient_type = 'SPHERICAL'
    TexGradient_flushing_nose_u.location = (400,800)
    ColorRamp_flushing_nose_u = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_flushing_nose_u.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_flushing_nose_u.color_ramp.elements[1].position = 0.2
    ColorRamp_flushing_nose_u.color_ramp.elements[1].color = (0, 0, 0, 0.5)
    ColorRamp_flushing_nose_u.color_ramp.elements[1].position = 1
    ColorRamp_flushing_nose_u.location = (600,800)
    Mapping_flushing_nose_d = Face_Skin_Group.nodes.new('ShaderNodeMapping')
    Mapping_flushing_nose_d.inputs[1].default_value = (0,-0.4,0)
    Mapping_flushing_nose_d.inputs[3].default_value = (0.07,0.03,0)
    Mapping_flushing_nose_d.location = (200,600)
    TexGradient_flushing_nose_d = Face_Skin_Group.nodes.new('ShaderNodeTexGradient')
    TexGradient_flushing_nose_d.gradient_type = 'SPHERICAL'
    TexGradient_flushing_nose_d.location = (400,600)
    ColorRamp_flushing_nose_d = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_flushing_nose_d.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_flushing_nose_d.color_ramp.elements[1].position = 0.2
    ColorRamp_flushing_nose_d.color_ramp.elements[1].color = (0, 0, 0, 0.5)
    ColorRamp_flushing_nose_d.color_ramp.elements[1].position = 1
    ColorRamp_flushing_nose_d.location = (600,600)
    
    Face_Skin_Group.links.new(Mapping_flushing_base.inputs[0],TexCoord_flushing.outputs[3])
    Face_Skin_Group.links.new(Mapping_flushing_forehead.inputs[0],TexCoord_flushing.outputs[3])
    Face_Skin_Group.links.new(Mapping_flushing_cheek_R.inputs[0],TexCoord_flushing.outputs[3])
    Face_Skin_Group.links.new(Mapping_flushing_cheek_L.inputs[0],TexCoord_flushing.outputs[3])
    Face_Skin_Group.links.new(Mapping_flushing_nose_u.inputs[0],TexCoord_flushing.outputs[3])
    Face_Skin_Group.links.new(Mapping_flushing_nose_d.inputs[0],TexCoord_flushing.outputs[3])
    Face_Skin_Group.links.new(TexGradient_flushing_base.inputs[0],Mapping_flushing_base.outputs[0])
    Face_Skin_Group.links.new(TexGradient_flushing_forehead.inputs[0],Mapping_flushing_forehead.outputs[0])
    Face_Skin_Group.links.new(TexGradient_flushing_cheek_R.inputs[0],Mapping_flushing_cheek_R.outputs[0])
    Face_Skin_Group.links.new(TexGradient_flushing_cheek_L.inputs[0],Mapping_flushing_cheek_L.outputs[0])
    Face_Skin_Group.links.new(TexGradient_flushing_nose_u.inputs[0],Mapping_flushing_nose_u.outputs[0])
    Face_Skin_Group.links.new(TexGradient_flushing_nose_d.inputs[0],Mapping_flushing_nose_d.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_flushing_base.inputs[0],TexGradient_flushing_base.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_flushing_forehead.inputs[0],TexGradient_flushing_forehead.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_flushing_cheek_R.inputs[0],TexGradient_flushing_cheek_R.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_flushing_cheek_L.inputs[0],TexGradient_flushing_cheek_L.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_flushing_nose_u.inputs[0],TexGradient_flushing_nose_u.outputs[0])
    Face_Skin_Group.links.new(ColorRamp_flushing_nose_d.inputs[0],TexGradient_flushing_nose_d.outputs[0])

    control_face_flushing_forehead = 1
    control_face_flushing_cheek = 1
    control_face_flushing_nose = 1
    
    Math_flushing_control_forehead = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing_control_forehead.blend_type='MULTIPLY'
    Math_flushing_control_forehead.inputs[0].default_value = control_face_flushing_forehead
    Math_flushing_control_forehead.location = (1000,1600)
    Math_flushing_combine_cheek_RL = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing_combine_cheek_RL.blend_type='MULTIPLY'
    Math_flushing_combine_cheek_RL.inputs[0].default_value = 1
    Math_flushing_combine_cheek_RL.location = (1000,1200)
    Math_flushing_control_cheek = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing_control_cheek.blend_type='MULTIPLY'
    Math_flushing_control_cheek.inputs[0].default_value = control_face_flushing_cheek
    Math_flushing_control_cheek.location = (1200,1200)
    Math_flushing_combine_nose_ud= Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing_combine_nose_ud.blend_type='MULTIPLY'
    Math_flushing_combine_nose_ud.inputs[0].default_value = 1
    Math_flushing_combine_nose_ud.location = (1000,800)
    Math_flushing_control_nose = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing_control_nose.blend_type='MULTIPLY'
    Math_flushing_control_nose.inputs[0].default_value = control_face_flushing_nose
    Math_flushing_control_nose.location = (1200,800)
    Math_flushing_combine_nose_cheek = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing_combine_nose_cheek.blend_type='MULTIPLY'
    Math_flushing_combine_nose_cheek.inputs[0].default_value = 1
    Math_flushing_combine_nose_cheek.location = (1400,1200)
    Math_flushing_combine_nose_cheek_forehead = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing_combine_nose_cheek_forehead.blend_type='MULTIPLY'
    Math_flushing_combine_nose_cheek_forehead.inputs[0].default_value = 1
    Math_flushing_combine_nose_cheek_forehead.location = (1600,1200)
    TexNoise_flushing = Face_Skin_Group.nodes.new('ShaderNodeTexNoise')
    TexNoise_flushing.inputs[2].default_value = 0.7
    TexNoise_flushing.location = (200,400)
    ColorRamp_flushing_color = Face_Skin_Group.nodes.new('ShaderNodeValToRGB')
    ColorRamp_flushing_color.color_ramp.elements[0].color = (0.936894, 0.0939393, 0.102388, 1)
    ColorRamp_flushing_color.color_ramp.elements[1].position = 0
    ColorRamp_flushing_color.color_ramp.elements[1].color = (0.10649, 0.0151563, 0.0205034, 1)
    ColorRamp_flushing_color.color_ramp.elements[1].position = 1
    ColorRamp_flushing_color.location = (400,400)
    Math_flushing = Face_Skin_Group.nodes.new('ShaderNodeMixRGB')
    Math_flushing.blend_type='MIX'
    Math_flushing.location = (1800,400)

    Face_Skin_Group.links.new(Math_flushing_control_forehead.inputs[1],ColorRamp_flushing_base.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_control_forehead.inputs[2],ColorRamp_flushing_forehead.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_combine_cheek_RL.inputs[1],ColorRamp_flushing_cheek_R.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_combine_cheek_RL.inputs[2],ColorRamp_flushing_cheek_L.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_control_cheek.inputs[1],ColorRamp_flushing_base.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_control_cheek.inputs[2],Math_flushing_combine_cheek_RL.outputs[0])
    Face_Skin_Group.links.new(Math_flushing_combine_nose_cheek.inputs[1],Math_flushing_control_cheek.outputs[0])
    Face_Skin_Group.links.new(Math_flushing_combine_nose_cheek.inputs[2],Math_flushing_control_nose.outputs[0])
    Face_Skin_Group.links.new(Math_flushing_combine_nose_ud.inputs[1],ColorRamp_flushing_nose_u.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_combine_nose_ud.inputs[2],ColorRamp_flushing_nose_d.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_control_nose.inputs[1],ColorRamp_flushing_base.outputs[1])
    Face_Skin_Group.links.new(Math_flushing_control_nose.inputs[2],Math_flushing_combine_nose_ud.outputs[0])
    Face_Skin_Group.links.new(Math_flushing_combine_nose_cheek_forehead.inputs[1],Math_flushing_control_forehead.outputs[0])
    Face_Skin_Group.links.new(Math_flushing_combine_nose_cheek_forehead.inputs[2],Math_flushing_combine_nose_cheek.outputs[0])

    Face_Skin_Group.links.new(TexNoise_flushing.inputs[0],TexCoord_flushing.outputs[3])
    Face_Skin_Group.links.new(ColorRamp_flushing_color.inputs[0],TexNoise_flushing.outputs[0])

    Face_Skin_Group.links.new(Math_flushing.inputs[0],Math_flushing_combine_nose_cheek_forehead.outputs[0])
    Face_Skin_Group.links.new(Math_flushing.inputs[1],ColorRamp_flushing_color.outputs[0])
    Face_Skin_Group.links.new(Math_flushing.inputs[2],Teximage_face.outputs[0])
    

    material_output = material_face.node_tree.nodes.get('Material Output')
    material_output.location = (2400,0)
    BSDF = material_face.node_tree.nodes.get('Principled BSDF')
    BSDF.inputs[1].default_value=0
    BSDF.location = (2100,0)
    #Face_Skin_Group.links.new(BSDF.inputs[0],Teximage_face.outputs[0])
    Face_Skin_Group.links.new(BSDF.inputs[0],Math_flushing.outputs[0])
    Face_Skin_Group.links.new(BSDF.inputs[7],ColorRamp_roughness.outputs[0])
    Face_Skin_Group.links.new(BSDF.inputs[19],Bump.outputs[0])

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