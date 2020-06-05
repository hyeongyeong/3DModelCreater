import bpy

class Test_PT_Panel(bpy.types.Panel):
    bl_label = "Create Face Panel"
    bl_category = "Face"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self,context):
        layout = self.layout

        row = layout.row()
        row.operator('mesh.create_face_main',text= "create Face")
