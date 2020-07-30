import bpy
from bpy.props import (StringProperty,BoolProperty,IntProperty,FloatProperty,FloatVectorProperty,EnumProperty,PointerProperty)
from bpy.types import (Panel,Menu,Operator,PropertyGroup)
from . faceTexturing import fun_control_face_roughness, fun_control_face_skin_condition, fun_control_face_flushing_forehead, fun_control_face_flushing_cheek, fun_control_face_flushing_nose
#from . scatter_dot import scatter_random
#import faceTexturing


#Customizing Properties

class Custom_Properties(PropertyGroup):
    my_bool: BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int: IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )

    Specular_value: FloatProperty(
        name = "Skin Specular",
        description = "A float property",
        default = 0.3,
        min = 0.01,
        max = 1
        )

    Skin_score: FloatProperty(
        name = "Skin Condition",
        description = "A float property",
        default = 0.1,
        min = 0,
        max = 1
        )

    Face_flush_forehead: FloatProperty(
        name = "Forehead Flush",
        description = "A float property",
        default = 0.1,
        min = 0,
        max = 1
        )

    Face_flush_nose: FloatProperty(
        name = "Nose Flush",
        description = "A float property",
        default = 0.1,
        min = 0,
        max = 1
        )

    Face_flush_cheek: FloatProperty(
        name = "Cheek Flush",
        description = "A float property",
        default = 0.1,
        min = 0,
        max = 1
        )

    my_float_vector: FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= 0.0, # float
        max = 0.1
    ) 

    my_string: StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )

    my_path: StringProperty(
        name = "Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
        )

    my_enum: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )

#import default model

class back_to_default(Operator):
    bl_label = "GO BACK TO DEFAULT MODEL"
    bl_idname = "customize.back_to_default"
   
    def execute(self, context):
        self.test()
        #import default model

        return {'FINISHED'}
   
    def test(self):
        print("say hello")
        return {'FINISHED'}

"""
class OBJECT_MT_CustomMenu(bpy.types.Menu):
    bl_label = "Select"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        # Built-in operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")
"""
# ------------------------------------------------------------------------
#    Panels
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "Customizing"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Customizing"
    bl_context = "objectmode"   
    #bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        layout.operator("customize.back_to_default")
    

#Specular Panel

class OBJECT_PT_CustomPanel_Specular(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_custom_panel"
    bl_label = "Custom Face Specular"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    
    def draw(self, context):
        #layout = self.layout  
        #layout.prop(self, "icon", expand=True)    
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        layout.prop(mytool, "Specular_value")
        layout.operator('customize.specular', text = "apply specular")
        #layout.operator(self.test(), text = "specular")
        #self.test()
    
    def test(self,context):
        value_specular = context.scene.my_tool.Specular_value
        fun_control_face_roughness(value_specular)
        return {'FINISHED'} 

class Run_Customize_specular(bpy.types.Operator):
    bl_idname = "customize.specular"
    bl_label = "Operator to specular customize"
    bl_description = "Operator to specular customize"
    
    def execute(self, context):
        value_specular = context.scene.my_tool.Specular_value
        fun_control_face_roughness(value_specular)
        
        #scatter_random ("face_image_texture.tif", "dot", "mapping.bmp","dot_map.bmp","random_dot.bmp", 0.1,0.3,0.6, 0.9,20)
        return {'FINISHED'}


# Skin Condition Panel

class OBJECT_PT_CustomPanel_Skin_Condition(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_custom_panel"
    bl_label = "Custom Skin Condition"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    
    def draw(self, context): 
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        layout.prop(mytool, "Skin_score")
        layout.operator('customize.skin_condition', text = "apply skin condition")

class Run_Customize_Skin_Condition(bpy.types.Operator):
    bl_idname = "customize.skin_condition"
    bl_label = "Operator to skin_condition customize"
    bl_description = "Operator to skin_condition customize"
    
    def execute(self, context):
        skin_condition = context.scene.my_tool.Skin_score
        fun_control_face_skin_condition(skin_condition)
        
        #scatter_random ("face_image_texture.tif", "dot", "mapping.bmp","dot_map.bmp","random_dot.bmp", 0.1,0.3,0.6, 0.9,20)
        return {'FINISHED'}

# Face Flush Panel

class OBJECT_PT_CustomPanel_Face_Flush(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_custom_panel"
    bl_label = "Custom Face Flush"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    
    def draw(self, context): 
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        layout.prop(mytool, "Face_flush_forehead")
        layout.prop(mytool, "Face_flush_nose")
        layout.prop(mytool, "Face_flush_cheek")
        layout.operator('customize.face_flush', text = "apply face flush")

class Run_Customize_Face_Flush(bpy.types.Operator):
    bl_idname = "customize.face_flush"
    bl_label = "Operator to face_flush customize"
    bl_description = "Operator to face_flush customize"
    
    def execute(self, context):
        Face_flush_forehead = context.scene.my_tool.Face_flush_forehead
        Face_flush_nose = context.scene.my_tool.Face_flush_nose
        Face_flush_cheek = context.scene.my_tool.Face_flush_cheek

        fun_control_face_flushing_forehead(Face_flush_forehead)
        fun_control_face_flushing_nose(Face_flush_nose)
        fun_control_face_flushing_cheek(Face_flush_cheek)

        
        #scatter_random ("face_image_texture.tif", "dot", "mapping.bmp","dot_map.bmp","random_dot.bmp", 0.1,0.3,0.6, 0.9,20)
        return {'FINISHED'}

"""
count = 0
class Record_history(bpy.types.Operator):
    bl_idname = "customoize.history"
    bl_label = "history"
    bl_description = "add history"
    
    
    
    def execute(self, context):
        bpy.ops.ed.undo_push()
        global count
        count += 1
        print(count)
        return {'FINISHED'}
"""
#class History(object):
#    def __init__(self):
#        self.count = 0

        


"""a
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        #box = layout.box()
        #row = box.row()
       #row.label("asdf")
       # row = box.row()
        #row.prop(mytool, "my_string")
        row = layout.row()
        row.prop(mytool, "my_string")
        box = layout.box()
        row = box.row()
        box = layout.box()
        box.prop(mytool, "my_bool")
        box.prop(mytool, "my_enum", text="") 
        box.prop(mytool, "my_int")

        box = layout.box()
        box.prop(mytool, "my_float")
        box.prop(mytool, "my_float_vector", text="")
        box.prop(mytool, "my_string")

        box = layout.box()
        box.prop(mytool, "my_path")
        box.operator("back_to_default")
        box.menu(OBJECT_MT_CustomMenu.bl_idname, text="Presets", icon="SCENE")
        box.separator()

        # layout.prop(mytool, "my_bool")
        # layout.prop(mytool, "my_enum", text="") 
        # layout.prop(mytool, "my_int")
        # layout.prop(mytool, "my_float")
        # layout.prop(mytool, "my_float_vector", text="")
        # layout.prop(mytool, "my_string")
        # layout.prop(mytool, "my_path")
        # layout.operator("back_to_default")
        # layout.menu(OBJECT_MT_CustomMenu.bl_idname, text="Presets", icon="SCENE")
        # layout.separator()
        """