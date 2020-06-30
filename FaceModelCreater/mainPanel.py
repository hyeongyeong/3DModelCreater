import bpy

class Model_PT_Panel(bpy.types.Panel):
    bl_label = "Create Face Panel"
    bl_category = "Face"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self,context):
        layout = self.layout


        row = layout.row()
        row.operator('step.one', text = "Step 1")
        row = layout.row()
        row.operator('step.two', text = "Step 2")
        row = layout.row()
        row.operator('step.three', text = "Step 3")
        row = layout.row()
        row.operator('step.four', text = "Step 4")

        # row = layout.row()
        # row.operator('my.button', text = "create Model")
        # row = layout.row()
        # row.operator('mesh.create_model_main',text= "create Face")

        # row = layout.row()
        # row.operator('mesh.hair_styler', text="add hair system")
