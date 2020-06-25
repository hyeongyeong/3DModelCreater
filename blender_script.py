from FaceModelCreater import *

override = bpy.context.copy()
for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if (area.type == "VIEW_3D"):
            
            override ={'window': window,'screen':screen,'area': area}
            # bpy.ops.dconfig.viewport_defaults(override)
            # print("found it")
            # bpy.ops.particle.brush_edit(stroke=[{'name': '', 'location': (0, 0, 0), 'mouse': (0, 0), 'pressure': 0, 'size': 0, 'pen_flip': False, 'time': 0, 'is_start': False}])

        else:
            print("not 3D view")
bpy.ops.mesh.create_model_main(override)
bpy.ops.mesh.hair_styler(override)

# bpy.ops.mesh.hair_styler()

# cnt = 1
# for window in bpy.context.window_manager.windows:
#     screen = window.screen
    
#     for area in screen.areas:
#         print(cnt)
#         if (area.type == "VIEW_3D"):
#             print("found it")
#         else:
#             print("not 3D view")
#         cnt = cnt + 1
