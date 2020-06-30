'''
Face Rigging Automation
Author: Jaehan Park
Last update: 2020-05-22

- need landmark points as 3D
- need matched mesh with forementioned landmark points
'''
import bpy
import numpy as np
from mathutils import Vector, Matrix
from math import radians


def dot_vec_mat4d(vec, mat):
    vec4d = Vector((vec[0], vec[1], vec[2], 1))
    dot = vec4d @ mat
    return Vector((dot[0], dot[1], dot[2]))


def generate_rig(parts_locations, outer_align_mat):
    #bpy.ops.object.mode_set(mode='OBJECT')
    MESH_ID = 'seok'

    # Activate Mesh
    objects = bpy.context.view_layer.objects
    obj = bpy.data.objects['Man']
    #obj = objects[f'{MESH_ID}_f-output']
    objects.active = obj
    #print('active 1', objects.active)


    # Read points list & Preprocessing 
    with open(f"C:/blender/test/input/model_point_{MESH_ID}.txt", "r") as f:
        lines = f.readlines()
        l_points = []
        for line in lines:
            l_points.append(Vector([float(val) for val in line.strip().split()]))

    align_mat = Matrix(np.loadtxt('C:/blender/GS_git_dev/input/align_matrix.txt', delimiter=','))

    aligned = []
    for _vec in l_points:
        aligned.append(_vec @ align_mat)



    # Labeling points
    labels_lndmrk = {'mouth_jaw':[0],
                    'brow.r':[1, 2, 3, 4, 5],
                    'brow.l':[6, 7, 8, 9, 10],
                    'brow_center':[11],
                    'nose_top':[12, 13, 14],
                    'nose_bottom':[15, 16, 17, 18, 19],
                    'eye_tail.r':[20, 23],
                    'eye_top.r':[21, 22],
                    'eye_bottom.r':[24, 25],
                    'eye_tail.l':[26, 29],
                    'eye_top.l':[27, 28],
                    'eye_bottom.l':[30, 31],
                    'mouth_tail.r':[32],
                    'mouth_tail.l':[38],
                    'mouth_top':[33, 34, 35, 36, 37],
                    'mouth_bottom':[39, 40, 41, 42, 43],
                    'lip_hole':[44, 45, 46, 47, 48, 49],
                    'face_edge.r':[50, 51, 52, 53, 54, 55, 56, 57],
                    'face_edge.l':[58, 59, 60, 61, 62, 63, 64, 65]}


    lndmrk_labels = {}
    for key, lndmrks in labels_lndmrk.items():
        for n in lndmrks:
            lndmrk_labels[n] = key

    print(lndmrk_labels)

    # Remove useless point
    rm_indices = labels_lndmrk['lip_hole'] + labels_lndmrk['face_edge.r'] + labels_lndmrk['face_edge.l']
    selected_landmarks = [vec for i, vec in enumerate(aligned) if i not in rm_indices]

    # Assign points to Vector
    # p -> bone-head
    # n -> bone-tail
    points = []
    normals = []
    for v in selected_landmarks:
        p = Vector((v[0], v[1]+0.012, v[2]))
        n = Vector((p[0], p[1], p[2]+0.1))
        points.append(p)
        normals.append(n)


    # Define new armature & rig
    #amt = bpy.data.armatures.new(obj.name + "_vBones")
    #rig = bpy.data.objects.new(obj.name + '_vRig', amt)

    # Link rig to collection
    #bpy.context.collection.objects.link(rig)

    # Activate rig
    #bpy.context.view_layer.objects.active = rig
    #print('active 2', objects.active)

    amt = bpy.data.armatures['Armature']
    rig = bpy.data.objects['Armature']
    bpy.context.view_layer.objects.active = rig
    #print(bpy.ops.object.mode_set.poll())
    # Mode set
    bpy.ops.object.mode_set(mode='EDIT')

    # Generate bones at selected landmark points
    for i, l in enumerate(zip(points, normals)):
        bone = amt.edit_bones.new(str(i))
        if i in labels_lndmrk['mouth_jaw']:
            # Jaw
            h = l[0]
            t = l[1]
            new_head_jaw = Vector((h[0], h[1]+0.25, h[2]-0.35))
            new_tail_jaw = Vector((t[0], t[1]+0.05, t[2]))
            bone.head = new_head_jaw
            bone.tail = new_tail_jaw
            bone.name = lndmrk_labels[i]
        elif i in labels_lndmrk['mouth_bottom']:
            # mouth_bottom-jaw parenting 
            bone.head = l[0]
            bone.tail = l[1]
            bone.name = lndmrk_labels[i]
            bone.parent = amt.edit_bones['mouth_jaw']
        elif i in labels_lndmrk['eye_tail.r']+labels_lndmrk['eye_bottom.r']+labels_lndmrk['eye_tail.l']+labels_lndmrk['eye_bottom.l']:
            # add eye_bottom
            bone.head = l[0]
            bone.tail = l[1]
            bone.name = lndmrk_labels[i]
            # eye restricting
            anc_bone = amt.edit_bones.new('anchor_'+str(i))
            h = l[0]
            t = l[1]
            anc_head = Vector((h[0], h[1]-0.1, h[2]))
            anc_tail = Vector((t[0], t[1]-0.1, t[2]))
            anc_bone.head = anc_head
            anc_bone.tail = anc_tail
        elif i in labels_lndmrk['brow.r']+labels_lndmrk['brow.l']+labels_lndmrk['brow_center']:
            # add brows
            bone.head = l[0]
            bone.tail = l[1]
            bone.name = lndmrk_labels[i]
            # eye restricting
            anc_bone = amt.edit_bones.new('anchor_'+str(i))
            h = l[0]
            t = l[1]
            anc_head = Vector((h[0], h[1]+0.1, h[2]))
            anc_tail = Vector((t[0], t[1]+0.1, t[2]))
            anc_bone.head = anc_head
            anc_bone.tail = anc_tail
        else:
            bone.head = l[0]
            bone.tail = l[1]
            bone.name = lndmrk_labels[i]

    head_bone = amt.edit_bones["mixamorig:Head.001"]
    #head_bone.select = True
    #rig_obj.data.bones.active = head_bone

    face_bones = []
    for _bone in amt.edit_bones:
        if 'mixamorig' not in _bone.name:
            face_bones.append(_bone.name)
            if _bone.parent == None:
                _bone.parent = head_bone

    bpy.ops.object.mode_set(mode='OBJECT')

    # Get mesh and rig
    mesh_obj = obj #bpy.data.objects[obj.name]
    #rig_obj = rig #bpy.data.objects[obj.name + '_vRig']

    # Select mesh first, then select rig
    mesh_obj.select_set(True)
    rig.select_set(True)


    # Automatic weighting
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')


'''
    # Deselect existing selections
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    # Into Pose mode
    #rig_obj = bpy.data.objects['seok_f-output_vRig']
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')

    # Activate mouth_jaw bone
    bone_obj = amt.bones["mouth_jaw"]
    bone_obj.select = True
    rig.data.bones.active = bone_obj

    # tongue parenting
    mesh_obj = bpy.data.objects['tongue_lowres_Mesh.001']
    mesh_obj.select_set(True)
    bpy.ops.object.parent_set(type='BONE')

    # lower teeth parenting
    mesh_obj.select_set(False)
    mesh_obj = bpy.data.objects['Lower_jaw_teeth_Lower_jaw_teeth.001']
    mesh_obj.select_set(True)
    bpy.ops.object.parent_set(type='BONE')

    # Activate head bone for upper teeth
    bone_obj = amt.bones["mixamorig:Head.001"]
    bone_obj.select = True
    rig.data.bones.active = bone_obj

    # Upper teeth parenting
    mesh_obj.select_set(False)
    mesh_obj = bpy.data.objects['Upper_jaw_teeth_Upper_jaw_teeth.001']
    mesh_obj.select_set(True)
    bpy.ops.object.parent_set(type='BONE')

    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')


    #rig = bpy.data.objects['seok_f-output_vRig']
    #amt = bpy.data.armatures['seok_f-output_vBones']

    right_head = dot_vec_mat4d(parts_locations['eye_r'], Matrix(outer_align_mat)) #bpy.data.objects['Sphere'].location
    right_tail = right_head + Vector((0, 0, 0.2))
    left_head = dot_vec_mat4d(parts_locations['eye_l'], Matrix(outer_align_mat)) #bpy.data.objects['Sphere.001'].location
    left_tail = left_head + Vector((0, 0, 0.2))


    # Activate rig
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')

    # Make eye bone
    re_bone = amt.edit_bones.new('right_eyeball')
    re_bone.head = right_head
    re_bone.tail = right_tail

    le_bone = amt.edit_bones.new('left_eyeball')
    le_bone.head = left_head
    le_bone.tail = left_tail

    # Make eye control bone
    control_height = 0.25
    center_controller_bone = amt.edit_bones.new('center_controller')
    center_controller_bone.head = (right_tail + left_tail)/2 + Vector((0, 0, control_height))
    center_controller_bone.tail = (right_tail + left_tail)/2 + Vector((0, 0.1, control_height))

    rec_bone = amt.edit_bones.new('right_eye_control')
    rec_bone.head = right_tail + Vector((0, 0, control_height))
    rec_bone.tail = right_tail + Vector((0, 0, control_height+0.1))
    rec_bone.parent = amt.edit_bones['center_controller']

    lec_bone = amt.edit_bones.new('left_eye_control')
    lec_bone.head = left_tail + Vector((0, 0, control_height))
    lec_bone.tail = left_tail + Vector((0, 0, control_height+0.1))
    lec_bone.parent = amt.edit_bones['center_controller']



    # Get mesh objects
    re_mesh = bpy.data.objects['Sphere']
    le_mesh = bpy.data.objects['Sphere.001']


    # Deselect existing selections
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    # Into Pose mode
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')


    re_posebone = amt.bones["right_eyeball"]
    re_posebone.select = True
    rig.data.bones.active = re_posebone

    re_mesh.select_set(True)
    bpy.ops.object.parent_set(type='BONE')

    re_posebone.select = False
    re_mesh.select_set(False)


    le_posebone = amt.bones["left_eyeball"]
    le_posebone.select = True
    rig.data.bones.active = le_posebone

    le_mesh.select_set(True)
    bpy.ops.object.parent_set(type='BONE')


    re_constraint = rig.pose.bones['right_eyeball'].constraints.new(type='TRACK_TO')
    re_constraint.target = rig
    re_constraint.subtarget = 'right_eye_control'

    le_constraint = rig.pose.bones['left_eyeball'].constraints.new(type='TRACK_TO')
    le_constraint.target = rig
    le_constraint.subtarget = 'left_eye_control'
'''