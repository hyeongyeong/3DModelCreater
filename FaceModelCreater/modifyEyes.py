
import bpy

def get_color_setting() :

    color = {}

    color["light_black"] =  {'Hue' : 1.0, 'Saturation' : 2.0, 'Value' : 2.0, 'Fac': 0.346}
    color["dark_black"] = {'Hue' : 0, 'Saturation' : 0, 'Value' : 0, 'Fac': 0.8}
    color["gray"] =  {'Hue' : 0, 'Saturation' : 0, 'Value' : 1.5, 'Fac': 0.631}
    color["red"] = {'Hue' : 0.4, 'Saturation' : 2, 'Value' : 2, 'Fac': 1}
    color["brown"] = {'Hue' : 0, 'Saturation' : 0, 'Value' : 0, 'Fac': 0}
    color["blue"] = {'Hue' : 1, 'Saturation' : 2, 'Value' : 2, 'Fac': 1}
    color["dark_blue"] = {'Hue' : 0.1, 'Saturation' : 2, 'Value' : 2, 'Fac': 1}
    color["green"] =  {'Hue' : 0.8, 'Saturation' : 2, 'Value' : 2, 'Fac': 1}
    color["purple"] = {'Hue' : 0.2, 'Saturation' : 2, 'Value' : 2, 'Fac': 1}

    return color

def set_eye_color(color_name):

    left_eye_material = "Iris"
    right_eye_material = "Iris.001"

    set_eye_material(left_eye_material, color_name)
    set_eye_material(right_eye_material, color_name)


def set_eye_material(material_name ,color_name):

    color_set = get_color_setting()
    
    material_eye = bpy.data.materials.get(material_name)
    hue = material_eye.node_tree.nodes.get('Hue Saturation Value')

    hue.inputs[0].default_value = color_set[color_name]['Hue']
    hue.inputs[1].default_value = color_set[color_name]['Saturation']
    hue.inputs[2].default_value = color_set[color_name]['Value']
    hue.inputs[3].default_value = color_set[color_name]['Fac']

