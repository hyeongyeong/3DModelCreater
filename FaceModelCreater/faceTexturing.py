import bpy

class MESH_OT_apply_texturing(bpy.types.Operator):
    bl_idname = "mesh.apply_texturing"
    bl_label = "apply_texturing"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
       texturing()
       return {'FINISHED'}


def texturing():
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
    
    material = bpy.data.materials.new("Face")
    material.use_nodes = True
    BSDF_face = material.node_tree.nodes.get('Principled BSDF')
    BSDF_face.inputs[1].default_value=0
    
    dark_rate = 0.2 #Skin stain level
    pore_rate = 0.1 #fiacial pore level

    
    #make subsurface color
    TexNoise_sub_face = material.node_tree.nodes.new('ShaderNodeTexNoise')
    TexNoise_sub_face.noise_dimensions = '2D'
    TexNoise_sub_face.inputs[2].default_value = 1
    TexNoise_sub_face.inputs[3].default_value = 2
    TexNoise_sub_face.location = (-1200,0)
    ColorRamp_sub_face = material.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_sub_face.color_ramp.elements[0].color = (0.0783149, 0, 0, 1)
    ColorRamp_sub_face.color_ramp.elements[0].position = 0
    ColorRamp_sub_face.color_ramp.elements[1].color = (0.75, 0.068, 0.073, 1)
    ColorRamp_sub_face.color_ramp.elements[1].position = 1
    ColorRamp_sub_face.location = (-900,0)
    material.node_tree.links.new(ColorRamp_sub_face.inputs[0],TexNoise_sub_face.outputs[0])
    #material.node_tree.links.new(BSDF_face.inputs[3],ColorRamp_sub_face.outputs[0])

    #make base color   
    TexNoise_base_face = material.node_tree.nodes.new('ShaderNodeTexNoise')
    TexNoise_base_face.inputs[2].default_value = 1000
    TexNoise_base_face.inputs[3].default_value = 200
    TexNoise_base_face.location = (-1200,300)
    ColorRamp_base_face = material.node_tree.nodes.new('ShaderNodeValToRGB')
    #ColorRamp_base_face.color_ramp.elements[0].color = (face_R[10]*dark_rate, face_G[10]*dark_rate, face_B[10]*dark_rate, 1)
    ColorRamp_base_face.color_ramp.elements[0].color =(0.433448, 0.173237, 0.139672, 1)
    ColorRamp_base_face.color_ramp.elements[0].position = 0
    #ColorRamp_base_face.color_ramp.elements[1].color = (face_R[10], face_G[10], face_B[10], 1)
    ColorRamp_base_face.color_ramp.elements[1].color = (0.570909, 0.183189, 0.145607, 1)
    ColorRamp_base_face.color_ramp.elements[1].position = 1
    ColorRamp_base_face.location = (-900,300)
    MixRGB_base_face = material.node_tree.nodes.new('ShaderNodeMixRGB')
    MixRGB_base_face.location = (-600,300)
    MixRGB_face = material.node_tree.nodes.new('ShaderNodeMixRGB')
    MixRGB_face.inputs[0].default_value = 0.858333
    MixRGB_face.location = (-300,300)  
    MixRGB_small_face = material.node_tree.nodes.new('ShaderNodeMixRGB')
    MixRGB_small_face.inputs[0].default_value = 0.15
    MixRGB_small_face.location = (-300,600)  
    material.node_tree.links.new(ColorRamp_base_face.inputs[0],TexNoise_base_face.outputs[0])
    material.node_tree.links.new(MixRGB_base_face.inputs[1],ColorRamp_base_face.outputs[0])
    material.node_tree.links.new(MixRGB_face.inputs[2],MixRGB_base_face.outputs[0])
    #material.node_tree.links.new(BSDF_face.inputs[0],MixRGB_face.outputs[0])
    material.node_tree.links.new(MixRGB_small_face.inputs[2],ColorRamp_sub_face.outputs[0])
    material.node_tree.links.new(MixRGB_small_face.inputs[1],MixRGB_face.outputs[0])
    material.node_tree.links.new(BSDF_face.inputs[0],MixRGB_small_face.outputs[0])
                                       
    #make flushing face
    TexCoord_base_right_face = material.node_tree.nodes.new('ShaderNodeTexCoord')
    TexCoord_base_right_face.location = (-1800,900)
    TexCoord_base_right_face.object = bpy.context.scene['my_obj']['ply']
    Mapping_base_right_face = material.node_tree.nodes.new('ShaderNodeMapping')
    Mapping_base_right_face.inputs[1].default_value[0] = -2.1
    Mapping_base_right_face.inputs[1].default_value[1] = -2.6
    Mapping_base_right_face.inputs[3].default_value[0] = 3
    Mapping_base_right_face.inputs[3].default_value[1] = 5.5
    Mapping_base_right_face.inputs[3].default_value[2] = 1
    Mapping_base_right_face.location = (-1500,1100)
    TexGradient_base_right_face = material.node_tree.nodes.new('ShaderNodeTexGradient')
    TexGradient_base_right_face.gradient_type = 'SPHERICAL'   
    TexGradient_base_right_face.location = (-1200,900)
    ColorRamp_base_right_face = material.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_base_right_face.color_ramp.elements[0].color = (0.462077, 0.198069, 0.119538, 1)
    ColorRamp_base_right_face.color_ramp.elements[0].position = 0.0
    ColorRamp_base_right_face.color_ramp.elements[1].color = (1, 0, 0.0109254, 1)
    ColorRamp_base_right_face.color_ramp.elements[1].position = 0.35
    ColorRamp_base_right_face.color_ramp.interpolation = 'EASE'
    ColorRamp_base_right_face.location = (-900,900)
    TexCoord_base_left_face = material.node_tree.nodes.new('ShaderNodeTexCoord')
    TexCoord_base_left_face.location = (-1800,600)
    TexCoord_base_left_face.object =   bpy.context.scene['my_obj']['ply']
    Mapping_base_left_face = material.node_tree.nodes.new('ShaderNodeMapping')
    Mapping_base_left_face.inputs[1].default_value[0] = -0.9
    Mapping_base_left_face.inputs[1].default_value[1] = -2.6
    Mapping_base_left_face.inputs[3].default_value[0] = 3
    Mapping_base_left_face.inputs[3].default_value[1] = 5.5
    Mapping_base_left_face.inputs[3].default_value[2] = 1
    Mapping_base_left_face.location = (-1500,600)
    TexGradient_base_left_face = material.node_tree.nodes.new('ShaderNodeTexGradient')
    TexGradient_base_left_face.gradient_type = 'SPHERICAL'   
    TexGradient_base_left_face.location = (-1200,600)
    ColorRamp_base_left_face = material.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_base_left_face.color_ramp.elements[0].color = (0.462077, 0.198069, 0.119538, 1)
    ColorRamp_base_left_face.color_ramp.elements[0].position = 0.0
    ColorRamp_base_left_face.color_ramp.elements[1].color = (1, 0, 0.0109254, 1)
    ColorRamp_base_left_face.color_ramp.elements[1].position = 0.35
    ColorRamp_base_left_face.color_ramp.interpolation = 'EASE'
    ColorRamp_base_left_face.location = (-900,600)
    MixRGB_base_left_right_face = material.node_tree.nodes.new('ShaderNodeMixRGB')
    MixRGB_base_left_right_face.location = (-600,600)
    material.node_tree.links.new(Mapping_base_right_face.inputs[0],TexCoord_base_right_face.outputs[0])
    material.node_tree.links.new(TexGradient_base_right_face.inputs[0],Mapping_base_right_face.outputs[0])
    material.node_tree.links.new(ColorRamp_base_right_face.inputs[0],TexGradient_base_right_face.outputs[1])
    material.node_tree.links.new(MixRGB_base_left_right_face.inputs[1],ColorRamp_base_right_face.outputs[0])
    material.node_tree.links.new(Mapping_base_left_face.inputs[0],TexCoord_base_left_face.outputs[0])
    material.node_tree.links.new(TexGradient_base_left_face.inputs[0],Mapping_base_left_face.outputs[0])
    material.node_tree.links.new(ColorRamp_base_left_face.inputs[0],TexGradient_base_left_face.outputs[1])
    material.node_tree.links.new(MixRGB_base_left_right_face.inputs[2],ColorRamp_base_left_face.outputs[0])
    material.node_tree.links.new(MixRGB_face.inputs[1],MixRGB_base_left_right_face.outputs[0])        
    
    #make facial pores of face
    TexCoord_pores_face = material.node_tree.nodes.new('ShaderNodeTexCoord')
    TexCoord_pores_face.location = (-1500,-300)
    TexCoord_pores_face.object =   bpy.context.scene['my_obj']['ply']
    TexVoronoi_pores_face = material.node_tree.nodes.new('ShaderNodeTexVoronoi')
    TexVoronoi_pores_face.feature = 'SMOOTH_F1'
    TexVoronoi_pores_face.inputs[2].default_value = 500
    TexVoronoi_pores_face.distance = 'CHEBYCHEV'
    TexVoronoi_pores_face.location = (-1200,-300)
    ColorRamp_pores_face = material.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_pores_face.color_ramp.elements[0].color =  (0.517641, 0.294275, 0.210766, 1)
    ColorRamp_pores_face.color_ramp.elements[0].position = 0
    ColorRamp_pores_face.color_ramp.elements[1].color =   (0.617207, 0.346704, 0.246201, 1)
    ColorRamp_pores_face.color_ramp.elements[1].position = 1        
    ColorRamp_pores_face.location = (-900,-300)
    ColorRamp_roughness_face = material.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_roughness_face.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_roughness_face.color_ramp.elements[0].position = 0.1
    ColorRamp_roughness_face.color_ramp.elements[1].color = (0, 0, 0, 1)
    ColorRamp_roughness_face.color_ramp.elements[1].position = 0.7
    ColorRamp_roughness_face.location = (-500,-150)
    Bump_face = material.node_tree.nodes.new('ShaderNodeBump')
    #Bump_face.inputs[0].default_value = 4
    Bump_face.inputs[0].default_value = 0.4
    Bump_face.inputs[1].default_value = 0.1   
    Bump_face.location = (-500,-450)
    material.node_tree.links.new(TexVoronoi_pores_face.inputs[0], TexCoord_pores_face.outputs[3])
    material.node_tree.links.new(TexNoise_sub_face.inputs[0], TexCoord_pores_face.outputs[3])
    material.node_tree.links.new(TexNoise_base_face.inputs[0], TexCoord_pores_face.outputs[3])
    material.node_tree.links.new(ColorRamp_pores_face.inputs[0], TexVoronoi_pores_face.outputs[0])
    material.node_tree.links.new(MixRGB_base_face.inputs[2],ColorRamp_pores_face.outputs[0])
    material.node_tree.links.new(ColorRamp_roughness_face.inputs[0],ColorRamp_pores_face.outputs[0])
    material.node_tree.links.new(Bump_face.inputs[2],ColorRamp_pores_face.outputs[0])
    material.node_tree.links.new(BSDF_face.inputs[7],ColorRamp_roughness_face.outputs[0])
    material.node_tree.links.new(BSDF_face.inputs[19], Bump_face.outputs[0])
    
    #Improving shading effect performance
    Glossy_BSDF = material.node_tree.nodes.new('ShaderNodeBsdfGlossy')
    Glossy_BSDF.location=(0,-300)
    Mix_shader = material.node_tree.nodes.new('ShaderNodeMixShader')
    Mix_shader.location=(300,300)
    Fresnel = material.node_tree.nodes.new('ShaderNodeFresnel')
    Fresnel.location=(0,500)
    Fresnel.inputs[0].default_value=1
    Mix_shader_out = material.node_tree.nodes.new('ShaderNodeMixShader')
    Mix_shader_out.location=(600,0)
    Mix_shader_out.inputs[0].default_value=0.1
    Translucent_BSDF =  material.node_tree.nodes.new('ShaderNodeBsdfTranslucent')
    Translucent_BSDF.location=(300,0)
    Output = material.node_tree.nodes.get('Material Output')
    Output.location = (900,0)
    material.node_tree.links.new(Mix_shader.inputs[0], Fresnel.outputs[0])
    material.node_tree.links.new(Mix_shader.inputs[1],BSDF_face.outputs[0])
    material.node_tree.links.new(Mix_shader.inputs[2],Glossy_BSDF.outputs[0])
    material.node_tree.links.new(Mix_shader_out.inputs[1],Mix_shader.outputs[0])
    material.node_tree.links.new(Mix_shader_out.inputs[2],Translucent_BSDF.outputs[0])
    material.node_tree.links.new(Output.inputs[0], Mix_shader_out.outputs[0])

    bpy.context.object.active_material = material

    #select mouth area
    bpy.ops.object.mode_set(mode = 'EDIT')    
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("lips"))
    bpy.ops.object.vertex_group_select()

    ######## mouth color #########
    bpy.ops.object.material_slot_add()

    material_mouth  = bpy.data.materials.new("Mouth")
    material_mouth.use_nodes = True

    BSDF_mouth = material_mouth.node_tree.nodes.get('Principled BSDF')
    BSDF_mouth.inputs[1].default_value=0

    f_mouth= open(bpy.context.scene['file_path']['mouth_tex'],"r")
    mouth_R = []
    mouth_G = []
    mouth_B = []
    while True:
        line_mouth = f_mouth.readline()
        
    
        if not line_mouth:
            break
        split_mouth = line_mouth.split()
        mouth_R.append(float(split_mouth[0])/255) # always 1
        mouth_G.append(float(split_mouth[1])/255)
        mouth_B.append(float(split_mouth[2])/255)
    f_mouth.close()    
    
    dark_rate_mouth = 0.2 #Skin stain level
    
    
    #make Subsurface Color
    NoiseTex_sub_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexNoise')
    NoiseTex_sub_mouth.inputs[2].default_value = 20
    NoiseTex_sub_mouth.location = (-600,300)
    ColorRamp_sub_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_sub_mouth.color_ramp.elements[0].color = (0.319, 0, 0, 1)
    ColorRamp_sub_mouth.color_ramp.elements[0].position = 0.1
    ColorRamp_sub_mouth.color_ramp.elements[1].color = (0.7, 0.1, 0.1, 1)
    ColorRamp_sub_mouth.color_ramp.elements[1].position = 0.9
    ColorRamp_sub_mouth.location = (-300,300)
    material_mouth.node_tree.links.new(ColorRamp_sub_mouth.inputs[0],NoiseTex_sub_mouth.outputs[0])
    #material_mouth.node_tree.links.new(BSDF_mouth.inputs[3],ColorRamp_sub_mouth.outputs[0])

    #make Base Color 
    TexCoord_base_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexCoord')
    TexCoord_base_mouth.location = (-1200,600)
    Mapping_base_mouth = material_mouth.node_tree.nodes.new('ShaderNodeMapping')
    Mapping_base_mouth.inputs[1].default_value[0] = -1.5
    Mapping_base_mouth.inputs[1].default_value[1] = -1.1
    Mapping_base_mouth.inputs[3].default_value[0] = 3
    Mapping_base_mouth.inputs[3].default_value[1] = 4.9
    Mapping_base_mouth.inputs[3].default_value[2] = 1.1
    Mapping_base_mouth.location = (-900,600)
    TexGradient_base_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexGradient')
    TexGradient_base_mouth.gradient_type = 'SPHERICAL'   
    TexGradient_base_mouth.location = (-600,600)
    ColorRamp_base_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
    #ColorRamp_base_mouth.color_ramp.elements[0].color = (mouth_R[40]*dark_rate_mouth, mouth_G[40]*dark_rate_mouth, mouth_B[40]*dark_rate_mouth, 1)
    ColorRamp_base_mouth.color_ramp.elements[0].color = (0.412543, 0.250158, 0.198069, 1)
    ColorRamp_base_mouth.color_ramp.elements[0].position = 0.0
    #ColorRamp_base_mouth.color_ramp.elements[1].color = (mouth_R[40], mouth_G[40], mouth_B[40], 1)
    ColorRamp_base_mouth.color_ramp.elements[1].color = (0.322782, 0.0801937, 0.0701032, 1)
    ColorRamp_base_mouth.color_ramp.elements[1].position = 0.05
    ColorRamp_base_mouth.location = (-300,600)
    MixRGB_base_mouth = material_mouth.node_tree.nodes.new('ShaderNodeMixRGB')
    MixRGB_base_mouth.inputs[0].default_value = 0.15
    MixRGB_base_mouth.location=(0,600)
    material_mouth.node_tree.links.new(Mapping_base_mouth.inputs[0],TexCoord_base_mouth.outputs[0])
    material_mouth.node_tree.links.new(TexGradient_base_mouth.inputs[0],Mapping_base_mouth.outputs[0])
    material_mouth.node_tree.links.new(ColorRamp_base_mouth.inputs[0],TexGradient_base_mouth.outputs[1])
    #material_mouth.node_tree.links.new(BSDF_mouth.inputs[0],ColorRamp_base_mouth.outputs[0])
    material_mouth.node_tree.links.new(MixRGB_base_mouth.inputs[1],ColorRamp_base_mouth.outputs[0])
    material_mouth.node_tree.links.new(MixRGB_base_mouth.inputs[2],ColorRamp_sub_mouth.outputs[0])
    material_mouth.node_tree.links.new(BSDF_mouth.inputs[0],MixRGB_base_mouth.outputs[0])
    #make Roughness and Normal
    TexCoord_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexCoord')
    TexCoord_normal_mouth.location = (-1800,0)
    TexCoord_normal_mouth.object =  bpy.context.scene['my_obj']['ply']
    Mapping_vertical_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeMapping')
    Mapping_vertical_normal_mouth.inputs[3].default_value[0] = 5
    Mapping_vertical_normal_mouth.inputs[3].default_value[1] = 1
    Mapping_vertical_normal_mouth.inputs[3].default_value[2] = 1
    Mapping_vertical_normal_mouth.location = (-1500,150)
    TexNoise_vertical_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexNoise')
    TexNoise_vertical_normal_mouth.inputs[2].default_value = 80
    TexNoise_vertical_normal_mouth.inputs[3].default_value = 1
    TexNoise_vertical_normal_mouth.location = (-1200,0)
    ColorRamp_vertical_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_vertical_normal_mouth.color_ramp.elements[0].color = (0.167827, 0.0684274, 0.0594318, 1)
    ColorRamp_vertical_normal_mouth.color_ramp.elements[0].position = 0.5
    ColorRamp_vertical_normal_mouth.color_ramp.elements.new(1)
    ColorRamp_vertical_normal_mouth.color_ramp.elements.new(0.95)
    ColorRamp_vertical_normal_mouth.color_ramp.elements[1].color =   (0.0839136, 0.0342137, 0.0297159, 1)
    ColorRamp_vertical_normal_mouth.color_ramp.elements[2].color =   (0, 0, 0, 1)
    ColorRamp_vertical_normal_mouth.location = (-900,0)
    Mapping_horizontal_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeMapping')
    Mapping_horizontal_normal_mouth.inputs[3].default_value[0] = 1
    Mapping_horizontal_normal_mouth.inputs[3].default_value[1] = 8
    Mapping_horizontal_normal_mouth.inputs[3].default_value[2] = 1
    Mapping_horizontal_normal_mouth.location = (-1500,-300)
    TexNoise_horizontal_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexNoise')
    TexNoise_horizontal_normal_mouth.inputs[2].default_value = 200
    TexNoise_horizontal_normal_mouth.inputs[3].default_value = 2
    TexNoise_horizontal_normal_mouth.location = (-1200,-300)
    ColorRamp_horizontal_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_horizontal_normal_mouth.color_ramp.elements[0].color = (0.0648033, 0.0262412, 0.0231534, 1)
    ColorRamp_horizontal_normal_mouth.color_ramp.elements[0].position = 0
    ColorRamp_horizontal_normal_mouth.color_ramp.elements[1].color =   (0.242281, 0.0975874, 0.0843762, 1)
    ColorRamp_horizontal_normal_mouth.color_ramp.elements[1].position = 1
    ColorRamp_horizontal_normal_mouth.location = (-900,-300)
    material_mouth.node_tree.links.new(Mapping_vertical_normal_mouth.inputs[0], TexCoord_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(TexNoise_vertical_normal_mouth.inputs[0],Mapping_vertical_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(ColorRamp_vertical_normal_mouth.inputs[0],TexNoise_vertical_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(Mapping_horizontal_normal_mouth.inputs[0], TexCoord_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(TexNoise_horizontal_normal_mouth.inputs[0],Mapping_horizontal_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(ColorRamp_horizontal_normal_mouth.inputs[0],TexNoise_horizontal_normal_mouth.outputs[0])
    
    MixRGB_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeMixRGB')
    MixRGB_normal_mouth.inputs[0].default_value = 0.316667
    MixRGB_normal_mouth.location=(-600,0)
    ColorRamp_normal_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_normal_mouth.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_normal_mouth.color_ramp.elements[0].position = 0.04
    ColorRamp_normal_mouth.color_ramp.elements[1].color = (0, 0, 0, 1)
    ColorRamp_normal_mouth.color_ramp.elements[1].position = 0.11
    ColorRamp_normal_mouth.location = (-300,0)
    Bump_mouth = material_mouth.node_tree.nodes.new('ShaderNodeBump')
    #Bump_mouth.inputs[0].default_value = 30
    Bump_mouth.inputs[0].default_value = 0.3
    Bump_mouth.inputs[1].default_value = 0.1
    Bump_mouth.location = (-300,-300)
    material_mouth.node_tree.links.new(MixRGB_normal_mouth.inputs[1], ColorRamp_vertical_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(MixRGB_normal_mouth.inputs[2],ColorRamp_horizontal_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(ColorRamp_normal_mouth.inputs[0],MixRGB_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(Bump_mouth.inputs[2],MixRGB_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(BSDF_mouth.inputs[7],ColorRamp_normal_mouth.outputs[0])
    material_mouth.node_tree.links.new(BSDF_mouth.inputs[19], Bump_mouth.outputs[0])

    bpy.context.object.active_material = material_mouth
    bpy.ops.object.material_slot_assign()
    
    #select eyebrow area
    bpy.ops.object.mode_set(mode = 'EDIT')    
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("eye_brow_l"))
    bpy.ops.object.vertex_group_select()

    bpy.ops.object.material_slot_add()

    """
    material_eyebrow  = bpy.data.materials.new("Eyebrow")
    material_eyebrow.use_nodes = True

    BSDF_eyebrow = material_eyebrow.node_tree.nodes.get('Principled BSDF')
    BSDF_eyebrow.inputs[1].default_value=0.15

    f_eyebrow= open(bpy.context.scene['file_path']['eye_brow_tex'],"r")
    eyebrow_R = []
    eyebrow_G = []
    eyebrow_B = []
    while True:
        line_eyebrow = f_eyebrow.readline()
    
        if not line_eyebrow:
            break
        split_eyebrow = line_eyebrow.split()
        eyebrow_R.append(float(split_eyebrow[0])/255) # always 1
        eyebrow_G.append(float(split_eyebrow[1])/255)
        eyebrow_B.append(float(split_eyebrow[2])/255)
    f_eyebrow.close()    
    
    dark_rate_eyebrow = 0.2 #Skin stain level
    
    Voronoi_sub_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeTexNoise')
    Voronoi_sub_eyebrow.inputs[2].default_value = 20
    Voronoi_sub_eyebrow.location = (-800,600)
    
    ColorRamp_sub_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_sub_eyebrow.color_ramp.elements[0].color = (0, 0, 0, 1)
    ColorRamp_sub_eyebrow.color_ramp.elements[0].position = 0.1
    ColorRamp_sub_eyebrow.color_ramp.elements[1].color = (0, 0, 0, 1)
    ColorRamp_sub_eyebrow.color_ramp.elements[1].position = 0.9
    ColorRamp_sub_eyebrow.location = (-600,600)
    
    material_eyebrow.node_tree.links.new(ColorRamp_sub_eyebrow.inputs[0],Voronoi_sub_eyebrow.outputs[0])
    material_eyebrow.node_tree.links.new(BSDF_eyebrow.inputs[3],ColorRamp_sub_eyebrow.outputs[0])

    Voronoi_base_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeTexNoise')
    Voronoi_base_eyebrow.inputs[2].default_value = 15
    Voronoi_base_eyebrow.location = (-800,300)

    ColorRamp_base_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeValToRGB')
    #ColorRamp_base_eyebrow.color_ramp.elements[0].color = (eyebrow_R[40]*dark_rate_eyebrow, eyebrow_G[40]*dark_rate_eyebrow, eyebrow_B[40]*dark_rate_eyebrow, 1)
    ColorRamp_base_eyebrow.color_ramp.elements[0].color = (0.177888, 0.109462, 0.0561285, 1)
    ColorRamp_base_eyebrow.color_ramp.elements[0].position = 0.0
    #ColorRamp_base_eyebrow.color_ramp.elements[1].color = (eyebrow_R[40], eyebrow_G[40], eyebrow_B[40], 1)
    ColorRamp_base_eyebrow.color_ramp.elements[1].color = (0.262251, 0.158961, 0.0843762, 1)
    ColorRamp_base_eyebrow.color_ramp.elements[1].position = 1
    ColorRamp_base_eyebrow.location = (-600,300)
    
    material_eyebrow.node_tree.links.new(ColorRamp_base_eyebrow.inputs[0],Voronoi_base_eyebrow.outputs[0])
    material_eyebrow.node_tree.links.new(BSDF_eyebrow.inputs[0],ColorRamp_base_eyebrow.outputs[0])
    
    Voronoi_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeTexVoronoi')
    Voronoi_eyebrow.feature = 'SMOOTH_F1'
    Voronoi_eyebrow.inputs[2].default_value = 1024
    Voronoi_eyebrow.distance = 'MANHATTAN'
    Voronoi_eyebrow.location = (-800,0)

    ColorRamp_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeValToRGB')
    #ColorRamp_eyebrow.color_ramp.elements[0].color = (eyebrow_R[20]*dark_rate_eyebrow, eyebrow_G[20]*dark_rate_eyebrow, eyebrow_B[20]*dark_rate_eyebrow, 1)
    ColorRamp_eyebrow.color_ramp.elements[0].color = (0.35806, 0.231665, 0.114963, 1)
    ColorRamp_eyebrow.color_ramp.elements[0].position = 0
    #ColorRamp_eyebrow.color_ramp.elements[1].color =  (eyebrow_R[20], eyebrow_G[20], eyebrow_B[20], 1)
    ColorRamp_eyebrow.color_ramp.elements[1].color =  (0.163335, 0.107151, 0.0599214, 1)
    ColorRamp_eyebrow.color_ramp.elements[1].position = 0.4
    ColorRamp_eyebrow.location = (-600,0)

    ColorRamp_roughness_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeValToRGB')
    ColorRamp_roughness_eyebrow.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRamp_roughness_eyebrow.color_ramp.elements[0].position = 0.3
    ColorRamp_roughness_eyebrow.color_ramp.elements[1].color = (0, 0, 0, 1)
    ColorRamp_roughness_eyebrow.color_ramp.elements[1].position = 1
    ColorRamp_roughness_eyebrow.location = (-300,00)
    
    Bump_eyebrow = material_eyebrow.node_tree.nodes.new('ShaderNodeBump')
    Bump_eyebrow.inputs[0].default_value = 4
    Bump_eyebrow.inputs[1].default_value = 0.1
    Bump_eyebrow.location = (-300,-300)

    material_eyebrow.node_tree.links.new(ColorRamp_eyebrow.inputs[0], Voronoi_eyebrow.outputs[0])
    material_eyebrow.node_tree.links.new(ColorRamp_roughness_eyebrow.inputs[0],ColorRamp_eyebrow.outputs[0])
    material_eyebrow.node_tree.links.new(Bump_eyebrow.inputs[2],ColorRamp_eyebrow.outputs[0])
    material_eyebrow.node_tree.links.new(BSDF_eyebrow.inputs[7],ColorRamp_roughness_eyebrow.outputs[0])
    material_eyebrow.node_tree.links.new(BSDF_eyebrow.inputs[19], Bump_eyebrow.outputs[0])

    bpy.context.object.active_material = material_eyebrow
    """
    bpy.context.object.active_material = material # Input the same skin as the face
    bpy.ops.object.material_slot_assign()
    
    bpy.ops.object.mode_set(mode = 'EDIT')    
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=str("eye_brow_r"))
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.material_slot_assign()

    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')