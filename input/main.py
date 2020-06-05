import bpy
import bmesh
from bpy.types import (Operator, Header, Menu, Panel,)
from bpy.props import (FloatVectorProperty, IntProperty, FloatProperty)
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import numpy as np

class main_Operator(bpy.types.Operator):
    bl_idname =  "view3d.cursor_center"
    bl_label = "Simple operator"
    bl_description = "Center 3d cursor"

    def delete_nose_hole(objs_data):
        f= open(bpy.context.scene['file_path']['point'],"r")
        my_object =objs_data
        faces = my_object.vertices
        iter =0
        

        temp_x = []
        temp_y = []
        temp_z = []

        temp_x2 = []
        temp_y2 = []
        temp_z2 = []

        while True:
            line = f.readline()
        
            if not line:
                break
            split = line.split()
            iter= iter+1

            if iter ==23 or iter ==28:
                temp_x2.append(float(split[0]))
                temp_y2.append(float(split[1]))
                temp_z2.append(float(split[2]))


            if iter>=15 and iter<=20 :#eyebrow left 5媛�
                temp_x.append(float(split[0]))
                temp_y.append(float(split[1]))
                temp_z.append(float(split[2]))

        f.close()

        temp_x[1]= temp_x2[0]
        temp_x[5]= temp_x2[1]


        temp1 = [[0]*3 for i in range(4)]
        k=0
        for i in range(0,2): #mouse
            for j in range(0,2):
                if(i==1):
                    j= 1-j

                temp1[k][0] = temp_x[j+1]+ (temp_x[0]- temp_x[j+1])*((i+1)/3) 
                temp1[k][1] = temp_y[j+1]+ (temp_y[0]- temp_y[j+1])*((i+1)/3)
                temp1[k][2] = temp_z[j]
                k=k+1

        temp2 = [[0]*3 for i in range(4)]
        k=0
        for i in range(0,2): #mouse
            for j in range(0,2):
                if(i==1):
                    j=1-j

                temp2[k][0] = temp_x[j+4]+ (temp_x[0]- temp_x[j+4])*((i+1)/3) 
                temp2[k][1] = temp_y[j+4]+ (temp_y[0]- temp_y[j+4])*((i+1)/3)
                temp2[k][2] = temp_z[j+4]
                k=k+1
        
        # for i in range(0,4):
        #     bpy.ops.mesh.primitive_cube_add(location=(temp1[i][0], temp1[i][1], temp1[i][2]))
        #     bpy.ops.mesh.primitive_cube_add(location=(temp2[i][0], temp2[i][1], temp2[i][2]))


        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for fa in faces:
            #isInside(f,mouse,12)
            temp3 = []
            temp3.append(fa.co.x)
            temp3.append(fa.co.y)
            temp3.append(fa.co.z)
           
            ans= main_Operator.isInside(temp3,temp1,4)
            ans2= main_Operator.isInside(temp3,temp2,4)
            if(ans or ans2):
                fa.select=True
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
    def select_eyebrow_point(objs_data):
        f= open(bpy.context.scene['file_path']['point'],"r")
        my_object =objs_data
        faces = my_object.vertices

        iter=0
        eyebrow_left_x = []
        eyebrow_left_y = []
        eyebrow_left_z = []

        eyebrow_right_x = []
        eyebrow_right_y = []
        eyebrow_right_z = []

        while True:
            line = f.readline()
        
            if not line:
                break
            split = line.split()
            iter= iter+1
     
            if iter>=2 and iter<=6 :#eyebrow left 5媛�
                eyebrow_left_x.append(float(split[0]))
                eyebrow_left_y.append(float(split[1]))
                eyebrow_left_z.append(float(split[2]))
            
            if iter>=7 and iter<=11 :#eyebrow right 5媛�
                eyebrow_right_x.append(float(split[0]))
                eyebrow_right_y.append(float(split[1]))
                eyebrow_right_z.append(float(split[2]))
                     
        f.close()
    
        eyebrowleft = [[0]*3 for i in range(8)]
        j=0

    
        for i in range(0,5): #mouse
            eyebrowleft[i][0] =eyebrow_left_x[j]
            eyebrowleft[i][1] =eyebrow_left_y[j]
            eyebrowleft[i][2] =eyebrow_left_z[j]

            j=j+1

        for i in range(7,10):
            eyebrowleft[i-2][0] =eyebrowleft[10-i][0]+3
            eyebrowleft[i-2][1] =eyebrowleft[10-i][1]-4
            eyebrowleft[i-2][2] =eyebrowleft[10-i][2]

        # for i in range(0,8):
        #     bpy.ops.mesh.primitive_cube_add(location=(eyebrowleft[i][0], eyebrowleft[i][1], 10))

        eyebrowright = [[0]*3 for i in range(8)]
        j=0

    
        for i in range(0,5): #mouse
            eyebrowright[i][0] =eyebrow_right_x[j]
            eyebrowright[i][1] =eyebrow_right_y[j]
            eyebrowright[i][2] =eyebrow_right_z[j]

            j=j+1

        for i in range(7,10):
            eyebrowright[i-2][0] =eyebrowright[10-i][0]-3
            eyebrowright[i-2][1] =eyebrowright[10-i][1]-4
            eyebrowright[i-2][2] =eyebrowright[10-i][2]

        # for i in range(0,8):
        #     bpy.ops.mesh.primitive_cube_add(location=(eyebrowright[i][0], eyebrowright[i][1], 10))


        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for fa in faces:
            #isInside(f,mouse,12)
            temp3 = []
            temp3.append(fa.co.x)
            temp3.append(fa.co.y)
            temp3.append(fa.co.z)
           
            ans= main_Operator.isInside(temp3,eyebrowleft,8)
            ans2= main_Operator.isInside(temp3,eyebrowright,8)
            if(ans or ans2):
                fa.select=True
        
        
        bpy.ops.object.mode_set(mode = 'EDIT')

    def isInside(aa,bb,cc):
        crosses = 0
        for i in range(0,cc):
            j = (i+1)%cc
            if((bb[i][1] > aa[1]) != (bb[j][1] > aa[1]) ):
                atX = (bb[j][0]- bb[i][0])*(aa[1]-bb[i][1])/(bb[j][1]-bb[i][1])+bb[i][0]
                if(aa[0] < atX):
                    crosses= crosses+1
        return crosses % 2 > 0

    def select_nose_area(objs_data):
        f= open(bpy.context.scene['file_path']['point'],"r")
        #my_object = objs.data
        #my_object = bpy.data.objects['seok_f-output'].data
        my_object =objs_data
        faces = my_object.vertices
        iter =0
        nose_x =[]
        nose_y =[]
        nose_z =[]

        temp_x = []
        temp_y = []
        temp_z = []

        while True:
            line = f.readline()
        
            if not line:
                break
            split = line.split()
            iter= iter+1

            if iter>=12 and iter<=20 :#eyebrow left 5媛�
                nose_x.append(float(split[0]))
                nose_y.append(float(split[1]))
                nose_z.append(float(split[2]))

            if iter==33 or iter == 39:
                temp_x.append(float(split[0]))
                temp_y.append(float(split[1]))
                temp_z.append(float(split[2]))


        f.close()
        nose = [[0]*3 for i in range(6)]
        j=0
        for i in range(0,9): #mouse
            if(i==0 or (i>=4 and i<=8)):
                nose[j][0] =nose_x[i]
                nose[j][1] =nose_y[i]
                nose[j][2] =nose_z[i]
                j=j+1

        nose[1][0] = temp_x[0]
        nose[5][0] = temp_x[1]
        
        for i in range(0,3):
            nose[i+2][1]= (nose[1][1]+nose[5][1])/2


        temp_coord= [[0]*3 for i in range(6)]
        j=0
        for i in range(0,3):
            temp_coord[i][0] = nose[1][0] + (nose[0][0] - nose[1][0])*((i+1)/4)
            temp_coord[i][1] = nose[1][1] + (nose[0][1] - nose[1][1])*((i+1)/4)

        for i in range(3,6):
            temp_coord[i][0] = nose[0][0] + (nose[5][0] - nose[0][0])*((i-2)/4)
            temp_coord[i][1] = nose[0][1] + (nose[5][1] - nose[0][1])*((i-2)/4)   

        nose_re = [[0]*3 for i in range(12)]

        nose_re[0] = nose[1]
        for i in range(0,3):
            nose_re[i+1]= temp_coord[i]
        
        nose_re[4]= nose[0]
        for i in range(3,6):
            nose_re[i+2] = temp_coord[i]
        
        for i in range(0,4):
            nose_re[i+8] = nose[5-i]

        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for fa in faces:
            #isInside(f,mouse,12)
            temp = []
            temp.append(fa.co.x)
            temp.append(fa.co.y)
            temp.append(fa.co.z)
           
            ans= main_Operator.isInside(temp,nose_re,12)
            if(ans):
                fa.select=True
        
        bpy.ops.object.mode_set(mode = 'EDIT')

    def texturing(objs):
        
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

        BSDF = material.node_tree.nodes.get('Principled BSDF')
        BSDF.inputs[1].default_value=0.15
        
        dark_rate = 0.2 #Skin stain level
        pore_rate = 0.1 #fiacial pore level
        
        Voronoi_sub = material.node_tree.nodes.new('ShaderNodeTexNoise')
        Voronoi_sub.inputs[2].default_value = 1000
        Voronoi_sub.inputs[3].default_value = 200
        Voronoi_sub.location = (-800,600)

        ColorRamp_sub = material.node_tree.nodes.new('ShaderNodeValToRGB')
        ColorRamp_sub.color_ramp.elements[0].color = (0.053, 0, 0, 1)
        ColorRamp_sub.color_ramp.elements[0].position = 0
        ColorRamp_sub.color_ramp.elements[1].color = (0.75, 0.068, 0.073, 1)
        ColorRamp_sub.color_ramp.elements[1].position = 1
        ColorRamp_sub.location = (-600,600)

   
        material.node_tree.links.new(ColorRamp_sub.inputs[0],Voronoi_sub.outputs[0])
        material.node_tree.links.new(BSDF.inputs[3],ColorRamp_sub.outputs[0])

        Voronoi_base = material.node_tree.nodes.new('ShaderNodeTexNoise')
        Voronoi_base.inputs[2].default_value = 1000
        Voronoi_base.inputs[3].default_value = 200
        Voronoi_base.location = (-800,300)

        ColorRamp_base = material.node_tree.nodes.new('ShaderNodeValToRGB')
        #ColorRamp_base.color_ramp.elements[0].color = (face_R[10]*dark_rate, face_G[10]*dark_rate, face_B[10]*dark_rate, 1)
        ColorRamp_base.color_ramp.elements[0].color =(0.177888, 0.109462, 0.0561285, 1)
        ColorRamp_base.color_ramp.elements[0].position = 0.0
        #ColorRamp_base.color_ramp.elements[1].color = (face_R[10], face_G[10], face_B[10], 1)
        ColorRamp_base.color_ramp.elements[1].color = (0.262251, 0.158961, 0.0843762, 1)
        ColorRamp_base.color_ramp.elements[1].position = 1
        ColorRamp_base.location = (-600,300)
        
        MixRGB = material.node_tree.nodes.new('ShaderNodeMixRGB')
        MixRGB.location = (-300,300)
        
        material.node_tree.links.new(ColorRamp_base.inputs[0],Voronoi_base.outputs[0])
        material.node_tree.links.new(MixRGB.inputs[1],ColorRamp_base.outputs[0])
        material.node_tree.links.new(BSDF.inputs[0],MixRGB.outputs[0])
        
        Voronoi = material.node_tree.nodes.new('ShaderNodeTexVoronoi')
        Voronoi.feature = 'SMOOTH_F1'
        Voronoi.inputs[2].default_value = 500
        Voronoi.distance = 'CHEBYCHEV'
        Voronoi.location = (-800,0)

        ColorRamp = material.node_tree.nodes.new('ShaderNodeValToRGB')
        ColorRamp.color_ramp.elements[0].color =  (0.214416, 0.139573, 0.0766113, 1)
        ColorRamp.color_ramp.elements[0].position = 0
        ColorRamp.color_ramp.elements[1].position = 1
        ColorRamp.color_ramp.elements[1].color =   (0.35806, 0.231665, 0.114963, 1)
        ColorRamp.location = (-600,0)

        ColorRamp_roughness = material.node_tree.nodes.new('ShaderNodeValToRGB')
        ColorRamp_roughness.color_ramp.elements[0].color = (1, 1, 1, 1)
        ColorRamp_roughness.color_ramp.elements[0].position = 0.3
        ColorRamp_roughness.color_ramp.elements[1].color = (0, 0, 0, 1)
        ColorRamp_roughness.color_ramp.elements[1].position = 1
        ColorRamp_roughness.location = (-300,00)
        
        Bump = material.node_tree.nodes.new('ShaderNodeBump')
        Bump.inputs[0].default_value = 4
        Bump.inputs[1].default_value = 0.1   
        Bump.location = (-300,-300)

        material.node_tree.links.new(ColorRamp.inputs[0], Voronoi.outputs[0])
        material.node_tree.links.new(MixRGB.inputs[2],ColorRamp.outputs[0])
        material.node_tree.links.new(ColorRamp_roughness.inputs[0],ColorRamp.outputs[0])
        material.node_tree.links.new(Bump.inputs[2],ColorRamp.outputs[0])
        material.node_tree.links.new(BSDF.inputs[7],ColorRamp_roughness.outputs[0])
        material.node_tree.links.new(BSDF.inputs[19], Bump.outputs[0])
        
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
        material.node_tree.links.new(Mix_shader.inputs[1],BSDF.outputs[0])
        material.node_tree.links.new(Mix_shader.inputs[2],Glossy_BSDF.outputs[0])
        
        material.node_tree.links.new(Mix_shader_out.inputs[1],Mix_shader.outputs[0])
        material.node_tree.links.new(Mix_shader_out.inputs[2],Translucent_BSDF.outputs[0])
        material.node_tree.links.new(Output.inputs[0], Mix_shader_out.outputs[0])

        bpy.context.object.active_material = material

        #select mouth area
        bpy.ops.object.mode_set(mode = 'EDIT')    
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group=str("lips"))
        #bpy.context.object.active_index = 0 #lips
        bpy.ops.object.vertex_group_select()

        ######## mouth color #########
        bpy.ops.object.material_slot_add()

        material_mouth  = bpy.data.materials.new("Mouth")
        material_mouth.use_nodes = True

        BSDF_mouth = material_mouth.node_tree.nodes.get('Principled BSDF')
        BSDF_mouth.inputs[1].default_value=0.15

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
        
        Voronoi_sub_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexNoise')
        Voronoi_sub_mouth.inputs[2].default_value = 20
        Voronoi_sub_mouth.location = (-800,600)
   
        ColorRamp_sub_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
        ColorRamp_sub_mouth.color_ramp.elements[0].color = (0.319, 0, 0, 1)
        ColorRamp_sub_mouth.color_ramp.elements[0].position = 0.1
        ColorRamp_sub_mouth.color_ramp.elements[1].color = (0.7, 0.1, 0.1, 1)
        ColorRamp_sub_mouth.color_ramp.elements[1].position = 0.9
        ColorRamp_sub_mouth.location = (-600,600)
        
        material_mouth.node_tree.links.new(ColorRamp_sub_mouth.inputs[0],Voronoi_sub_mouth.outputs[0])
        material_mouth.node_tree.links.new(BSDF_mouth.inputs[3],ColorRamp_sub_mouth.outputs[0])

        Voronoi_base_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexNoise')
        Voronoi_base_mouth.inputs[2].default_value = 20
        Voronoi_base_mouth.location = (-800,300)

        ColorRamp_base_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
        #ColorRamp_base_mouth.color_ramp.elements[0].color = (mouth_R[40]*dark_rate_mouth, mouth_G[40]*dark_rate_mouth, mouth_B[40]*dark_rate_mouth, 1)
        ColorRamp_base_mouth.color_ramp.elements[0].color = (0.23074, 0.0908417, 0.0802198, 1)
        ColorRamp_base_mouth.color_ramp.elements[0].position = 0.0
        #ColorRamp_base_mouth.color_ramp.elements[1].color = (mouth_R[40], mouth_G[40], mouth_B[40], 1)
        ColorRamp_base_mouth.color_ramp.elements[1].color = (0.238398, 0.0908417, 0.0822827, 1)
        ColorRamp_base_mouth.color_ramp.elements[1].position = 1
        ColorRamp_base_mouth.location = (-600,300)
        
        MixRGB_mouth = material_mouth.node_tree.nodes.new('ShaderNodeMixRGB')
        MixRGB_mouth.location = (-300,300)
        
        material_mouth.node_tree.links.new(ColorRamp_base_mouth.inputs[0],Voronoi_base_mouth.outputs[0])
        material_mouth.node_tree.links.new(MixRGB_mouth.inputs[1],ColorRamp_base_mouth.outputs[0])
        material_mouth.node_tree.links.new(BSDF_mouth.inputs[0],MixRGB_mouth.outputs[0])
        
        Voronoi_mouth = material_mouth.node_tree.nodes.new('ShaderNodeTexNoise')
        Voronoi_mouth.inputs[2].default_value = 200
        Voronoi_mouth.location = (-800,0)

        ColorRamp_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
        ColorRamp_mouth.color_ramp.elements[0].color = (0.246201, 0.093059, 0.0897487, 1)
        ColorRamp_mouth.color_ramp.elements[0].position = 0
        ColorRamp_mouth.color_ramp.elements[1].color =   (0.0722718, 0.0273209, 0.0185002, 1)
        ColorRamp_mouth.color_ramp.elements[1].position = 1
        ColorRamp_mouth.location = (-600,0)

        ColorRamp_roughness_mouth = material_mouth.node_tree.nodes.new('ShaderNodeValToRGB')
        ColorRamp_roughness_mouth.color_ramp.elements[0].color = (1, 1, 1, 1)
        ColorRamp_roughness_mouth.color_ramp.elements[0].position = 0
        ColorRamp_roughness_mouth.color_ramp.elements[1].color = (0, 0, 0, 1)
        ColorRamp_roughness_mouth.color_ramp.elements[1].position = 0.18
        ColorRamp_roughness_mouth.location = (-300,00)
        
        Bump_mouth = material_mouth.node_tree.nodes.new('ShaderNodeBump')
        Bump_mouth.inputs[0].default_value = 2
        Bump_mouth.inputs[1].default_value = 0.1
        Bump_mouth.location = (-300,-300)

        material_mouth.node_tree.links.new(ColorRamp_mouth.inputs[0], Voronoi_mouth.outputs[0])
        material_mouth.node_tree.links.new(MixRGB_mouth.inputs[2],ColorRamp_mouth.outputs[0])
        material_mouth.node_tree.links.new(ColorRamp_roughness_mouth.inputs[0],ColorRamp_mouth.outputs[0])
        material_mouth.node_tree.links.new(Bump_mouth.inputs[2],ColorRamp_mouth.outputs[0])
        material_mouth.node_tree.links.new(BSDF_mouth.inputs[7],ColorRamp_roughness_mouth.outputs[0])
        material_mouth.node_tree.links.new(BSDF_mouth.inputs[19], Bump_mouth.outputs[0])

        bpy.context.object.active_material = material_mouth
        bpy.ops.object.material_slot_assign()
        
        #select eyebrow area
        bpy.ops.object.mode_set(mode = 'EDIT')    
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group=str("eye_brow_l"))
        bpy.ops.object.vertex_group_select()

        bpy.ops.object.material_slot_add()

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
        
        bpy.ops.object.material_slot_assign()
        
        bpy.ops.object.mode_set(mode = 'EDIT')    
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_set_active(group=str("eye_brow_r"))
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.material_slot_assign()

        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
    
    def execute(self,context):
        
        # get global file path
        bpy.context.scene['file_path'] = {}
        bpy.context.scene['my_obj'] = {}
        bpy.context.scene['file_path']['point'] = "C:/Users/kwanghee_chang/Downloads/3d_Model/Porject_making_color_map/model_point.txt"
        bpy.context.scene['file_path']['eye'] = "C:/Users/kwanghee_chang/Downloads/3d_Model/Porject_making_color_map/eye22.jpg"
        bpy.context.scene['file_path']['eye_brow_tex'] = "C:/Users/kwanghee_chang/Downloads/3d_Model/Porject_making_color_map/RGB_data/eyebrow_left.txt"
        bpy.context.scene['file_path']['mouth_tex'] = "C:/Users/kwanghee_chang/Downloads/3d_Model/Porject_making_color_map/RGB_data/mouse.txt"
        bpy.context.scene['file_path']['skin_tex'] = "C:/Users/kwanghee_chang/Downloads/3d_Model/Porject_making_color_map/RGB_data/skin.txt"
        bpy.context.scene['file_path']['face'] = "C:/Users/kwanghee_chang/Downloads/3d_Model/Porject_making_color_map/seok_f-output.ply"

        objs = bpy.data.objects
#        if bpy.data.objects["Cube"]:
#            objs.remove(objs["Cube"], do_unlink=True)
            
        bpy.ops.import_mesh.ply(filepath=bpy.context.scene['file_path']['face'])
        bpy.ops.object.shade_smooth()


        bpy.context.scene['my_obj']['ply'] = bpy.data.objects["seok_f-output"]

        objs = bpy.data.objects["seok_f-output"]
        objs_data = objs.data

       
        bpy.ops.mesh.create_region_group()
        main_Operator.texturing(objs)
        bpy.ops.mesh.add_eyes()
           
        return {'FINISHED'}

def curved_plane (self, context, coord):
    
    p = coord
    plane = add_plane(self, context, coord)
    point_len = len(coord)
    
    obj = bpy.context.object
    bpy.ops.object.mode_set(mode = 'EDIT')
        
    #error handle
    if obj.mode == 'EDIT' :
        bm=bmesh.from_edit_mesh(obj.data)
        bm.edges.ensure_lookup_table()
    
    
        
        for idx, e in enumerate(bm.edges):
            if idx % 3 == 2 and idx < 33:
                bev_geom = [e.verts[0], e.verts[1], e]
                o = 6
                s = 5
                bmesh.ops.bevel(bm, geom=bev_geom, offset=o, segments=s,profile= 0.5,
                vertex_only   = False,
                clamp_overlap = False,
                loop_slide    = True,
                 material      = -1,offset_type   = 'OFFSET',)
        
        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return plane

def make_eye_material(path):
    
    file_path = path
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
        image = bpy.data.images.load(file_path)
        texImage.image = image
    except :
        raise NameError("Cannot load image %s" % file_path)
        
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
    coord_right = coord[0:6]
    coord_left = coord[6:12]
    
    right_x = []
    right_y = []
    left_x = []
    left_y = []

    for c in coord_right:
        right_x.append(c.x)
        right_y.append(c.y)
        
    for c in coord_left:    
        left_x.append(c.x)
        left_y.append(c.y)
    
    right_x = (max(right_x) + min(right_x)) / 2
    right_y = (max(right_y) + min(right_y)) / 2
    

    left_x = (max(left_x) + min(left_x)) / 2
    left_y = (max(left_y) + min(left_y)) / 2

    
    right = (right_x, right_y, -44.5)
    left = (left_x, left_y, -44.5)

    eyes = np.array([right, left])
    
    return eyes

def add_eyeball(self, context, coord, tex):
    
    eyes = []
    
    scale_info = np.array((1,1,1))* self.size
    scale_default = np.array((18,18,16))
    
    prop_x = np.array((1*self.eyeball_X,0,0))
    prop_y = np.array((0,1*self.eyeball_Y,0))
    prop_depth = np.array((0,0,1*self.depth))
    
    op = optimize_eye_loc(coord)
    
    right_loc = op[0] - prop_x + prop_y + prop_depth
    left_loc = op[1] + prop_x + prop_y + prop_depth
 
    loc = [right_loc, left_loc]
     
    for eye in loc :
        bpy.ops.mesh.primitive_uv_sphere_add(location=eye)
        ball = bpy.context.selected_objects[0]
        ball.scale = scale_default + scale_info
        eyes.append(ball)
    
    apply_eye_texture(eyes, tex)
    
def add_plane(self, context, coord): 
    verts = []
    thickness = 50
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

def apply_boolean(target , plane, operation, delete) :
    
    # select face model
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

def join_obj(target, obj):
    
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    bpy.ops.object.select_all(action='DESELECT')
    
    target.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()

def select_intersect_vertices(target, obj, group_name):
    
    verts = []
    
    bpy.ops.object.mode_set(mode = 'OBJECT')    
    bpy.ops.object.select_all(action='DESELECT')
    
    target.select_set(True)
    bpy.ops.object.mode_set(mode = 'EDIT')    
    
    target_bm=bmesh.from_edit_mesh(target.data)
    target_bm.verts.ensure_lookup_table()
 
    obj_v = obj.data.vertices
    
    i= 0
    for t in target_bm.verts:
        for o in obj_v:
            t.select = False
            if t.co.x == o.co.x and t.co.y == o.co.y and t.co.z == o.co.z :
                t.select = True
                verts.append(t.index)
                i=i+1
                break
            else:
                t.select = False
            
    vg=bpy.context.object.vertex_groups.new(name=group_name)
    bpy.ops.object.vertex_group_assign()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')    

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

def create_region_group(self, context, target, coord, vertex_group_name):
    
    intersect = "INTERSECT"
    difference = "DIFFERENCE"
    union = "UNION"
    
    # create new_obj plane to apply intersect and difference
    new_obj = duplicate_obj(target)
    new_obj_plane_d = curved_plane(self, context, coord)
    new_obj_plane_i = duplicate_obj(new_obj_plane_d)
            
    # apply boolean to get region of new_obj
    apply_boolean(target, new_obj_plane_d, difference, True)
    apply_boolean(new_obj, new_obj_plane_i, intersect, True)
    join = duplicate_obj(new_obj)
    join_obj(target, join)
    # apply_boolean(target, new_obj, union, False)
    
    select_intersect_vertices(target, new_obj, vertex_group_name)
    
    delete_object(new_obj)

def eye_brow_thickness(coord, direction):
    
    total = len(coord)
    print(total)
    new_coord = []
    for i in range(0,3):
        c = coord[total-i-2]
        v = Vector((c.x + direction*3, c.y - 4, c.z))
        new_coord.append(v)
    
    return coord+ new_coord

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

class MESH_OT_add_eyes(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_eyes"
    bl_label = "Make Eye ball"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    thickness : IntProperty(
        name="thickness",
        default= 10,
        min = 5,
        max = 100,
        description="The thickness of the eyelid",
    )
    
    eyeball_X : FloatProperty(
     name = "eyeballX",
     default = -2,
     description = "Correcting the left and right position of the eyeball",
    )
    
    eyeball_Y : FloatProperty(
     name = "eyeballY",
     default = 0,
     description = "Correct the position of the top and bottom of the eyeball",
    )
    
    depth : FloatProperty(
    
     name = "depth",
     default = 0,
     description = "Depth of eyeball"
    )
    
    size = FloatProperty(
     name = "size",
     default = 0,
     description = "Size of eyeball"
    )

    
    def execute(self, context):
       
        try :
            # TODO : Error output when multiple targets
            planes = []
            landmark_point_file_path = bpy.context.scene['file_path']['point']
            eye_texture_path = bpy.context.scene['file_path']['eye']

            target = bpy.context.scene['my_obj']['ply']
            
            coord = file_read(landmark_point_file_path)
            
            eye_point = coord[20:32]

            planes = make_curved_eye_plane(self, context, eye_point)

            for p in planes :
                # target , plane, operation, delete
                apply_boolean(target, p , "DIFFERENCE", True)

            add_eyeball(self, context, eye_point , eye_texture_path)
            
        except IndexError:
            print("Please select target face mesh!")

        return {'FINISHED'}

class MESH_OT_create_region_group(Operator, AddObjectHelper):
    bl_idname = "mesh.create_region_group"
    bl_label = "Create region group"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
       
        try :
            model_point_path = bpy.context.scene['file_path']['point']

            target = bpy.context.scene['my_obj']['ply']
            coord = file_read(model_point_path)

            lips_coord = coord[32:44]
            eye_brow_right_coord = coord[1:6]
            eye_brow_left_coord = coord[6:11]
            
            # Adding thickness to eye brow
            eye_brow_right_coord = eye_brow_thickness(eye_brow_right_coord, 1) # RIGHT
            eye_brow_left_coord = eye_brow_thickness(eye_brow_left_coord, -1) # LEFT

            # create vertex group of lips
            create_region_group(self, context, target, lips_coord, "lips")
            create_region_group(self, context, target, eye_brow_right_coord, "eye_brow_r")
            create_region_group(self, context, target, eye_brow_left_coord, "eye_brow_l")

            
        except IndexError:
            print("ERROR")

        return {'FINISHED'}
    
class View3D_PT_eye_hole(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Face"
    bl_label = "Create Face"
    
    def draw(self, context):
        cols = self.layout.column(align = True)
        cols.prop(context.scene, 'action')  
        
        props = cols.operator('view3d.cursor_center', text ='Face')
       


def register():
    bpy.utils.register_class(MESH_OT_add_eyes)
    bpy.utils.register_class(MESH_OT_create_region_group)
    bpy.utils.register_class(main_Operator)
    bpy.utils.register_class(View3D_PT_eye_hole)
    

def unregister():
    bpy.utils.unregister_class(MESH_OT_add_eyes)
    bpy.utils.unregister_class(MESH_OT_create_region_group)
    bpy.utils.unregister_class(main_Operator)
    bpy.utils.unregister_class(View3D_PT_eye_hole)
    
    
if __name__ == "__main__":
    register()
