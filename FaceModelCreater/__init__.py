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

from . main import main_Operator
from . mainPanel import Model_PT_Panel
from . createRegionGroup import MESH_OT_create_region_group
from . mouthCapacity import mouth_creation
from . createEyes import MESH_OT_add_eyes
from . nostril import nostril
from . faceTexturing import MESH_OT_apply_texturing

classes = (main_Operator, Model_PT_Panel, MESH_OT_add_eyes, MESH_OT_create_region_group, mouth_creation, nostril, MESH_OT_apply_texturing)


register,unregister = bpy.utils.register_classes_factory(classes)