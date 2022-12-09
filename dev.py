# bpy.data.actions["move_rot"].name = "move_rot"

# bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

# # rotate 360 degrees
# bpy.ops.transform.rotate(value=6.28319, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

# bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

# bpy.ops.object.anim_transforms_to_deltas()

# bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 6.65729, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})


def letter_animation(obj, n_frames_animation, n_frames_offset):
    """
    Intention: take a single character (mesh object) and move it to final location:
        - from outside of camera
        - with rotation
    """

    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

    n_frames_beg = n_frames_offset
    n_frames_end = n_frames_offset + n_frames_animation

    # capture final values
    bpy.context.scene.frame_set(n_frames_end)
    obj.keyframe_insert(data_path="location")
    obj.keyframe_insert(data_path="rotation_euler")

    # capture starting values
    bpy.context.scene.frame_set(n_frames_beg)

    # compute object state at begin of anmiation
    obj.location.y -= 4
    obj.rotation_euler[2] = 6.28319
    
    obj.keyframe_insert(data_path="location")
    obj.keyframe_insert(data_path="rotation_euler")


def add_text_object(text_str, obj_name):

    # create text object with label
    bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    obj = get_active_object()
    obj.name = obj_name
    obj.data.body = text_str
    
    return obj

