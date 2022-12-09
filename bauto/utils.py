import bpy

def get_object_by_name(obj_name):
    
    return bpy.context.scene.objects[obj_name]

def get_active_object():
    
    return bpy.context.active_object

def clear_all_objects(exclude_types=['LIGHT', 'CAMERA']):
    
    all_objects = bpy.data.objects
    for this_obj in all_objects:
        
        if exclude_types:
            
            if not(this_obj.type in exclude_types):
                
                this_obj.select_set(True)
                bpy.ops.object.delete()
