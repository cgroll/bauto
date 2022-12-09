import bpy
import bauto.utils as bautils
import bauto.text_utils as batext
import importlib
import math

importlib.reload(batext)
importlib.reload(bautils)


def clear_action_if_exists(action_name):
    """
    Delete existing action. Not only for an object, but globally.
    """
    
    this_action = bpy.data.actions.get(action_name)

    if this_action:
        bpy.data.actions.remove(this_action)


action_name = 'Move_and_rotate'

# make script idempotent
bautils.clear_all_objects()
clear_action_if_exists(action_name)

# add objects to scene
bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
obj_cube = bpy.context.active_object
obj_cube.select_set(False)

# create second object at different location
bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
obj_monkey = bpy.context.active_object
obj_monkey.location.y += 4
obj_monkey.select_set(False)
#bpy.ops.transform.translate(value=(0, 5.32666, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

# select first object
obj = obj_cube
obj_cube.select_set(True)

# create action
obj.animation_data_create()
obj.animation_data.action = bpy.data.actions.new(name=action_name)

# add_relative_action(action_name)
# add_end_frame(frame_offset=0)
# add_start_frame(shift, rotation, frame_end=50+offset)

frame_beg = 1
bpy.context.scene.frame_set(frame_beg)
obj.keyframe_insert("location", frame=frame_beg)
obj.keyframe_insert("rotation_euler", frame=frame_beg)

frame_end = 50
bpy.context.scene.frame_set(frame_end)

bpy.ops.transform.translate(value=(-10.575, -0, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
obj.rotation_euler[2] = math.radians(360)

obj.keyframe_insert("location", frame=frame_end)
obj.keyframe_insert("rotation_euler", frame=frame_end)

# make action relative 
bpy.ops.object.anim_transforms_to_deltas()

# apply action to second object
obj = obj_monkey
obj_monkey.select_set(True)

obj.animation_data_create()
bpy.context.object.animation_data.action = bpy.data.actions[action_name]




#### working example with modification of existing action

import bpy

def copy_action_with_offset(action_name, offset):
    
    # copy action with new name
    modified_action_copy = bpy.data.actions[action_name].copy()
    new_action_name = modified_action_copy.name

    # modify existing fcurves
    fcurves = modified_action_copy.fcurves
    
    for curve in fcurves:
        keyframePoints = curve.keyframe_points
        for keyframe in keyframePoints:
            keyframe.co[0] += this_offset
            keyframe.handle_left[0] += this_offset
            keyframe.handle_right[0] += this_offset
            
    return new_action_name
    
objs = bpy.context.selected_objects
offset = 2
action_name = 'tree_vanish'

counter = 0

for this_obj in objs:
    
    this_offset = offset * (counter+1)
    new_action_name = copy_action_with_offset(action_name, this_offset)
    this_obj.select_set(True)
    this_obj.animation_data.action = bpy.data.actions[new_action_name]

    counter += 1