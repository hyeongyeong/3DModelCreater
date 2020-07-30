# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "FaceCreater",
    "author" : "h",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . main import main_Operator, step_one, step_two
from . mainPanel import Model_PT_Panel
from . createRegionGroup import MESH_OT_create_region_group
from . mouthCapacity import mouth_creation
from . createEyes import MESH_OT_add_eyes
from . nostril import nostril
from . faceTexturing import MESH_OT_apply_texturing
from . hairStyler import Hair_styler
from . button import MY_BUTTON_OT_Button, step_four, step_three
from . createPhiltrum import MESH_OT_create_philtrum
from . uvmap import apply_UVMap
from . customize import Custom_Properties, back_to_default, OBJECT_PT_CustomPanel, OBJECT_PT_CustomPanel_Specular,Run_Customize_specular, OBJECT_PT_CustomPanel_Skin_Condition, Run_Customize_Skin_Condition, OBJECT_PT_CustomPanel_Face_Flush, Run_Customize_Face_Flush
from bpy.props import PointerProperty

classes = (main_Operator, step_one, step_two, step_three, step_four, Model_PT_Panel,MY_BUTTON_OT_Button, MESH_OT_add_eyes, MESH_OT_create_region_group, mouth_creation, nostril, MESH_OT_apply_texturing, Hair_styler,MESH_OT_create_philtrum, apply_UVMap, Custom_Properties, back_to_default, OBJECT_PT_CustomPanel, OBJECT_PT_CustomPanel_Specular,Run_Customize_specular, OBJECT_PT_CustomPanel_Skin_Condition, Run_Customize_Skin_Condition, OBJECT_PT_CustomPanel_Face_Flush, Run_Customize_Face_Flush)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=Custom_Properties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


#register,unregister = bpy.utils.register_classes_factory(classes)