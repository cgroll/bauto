bl_info = {
    "name": "CG reload modules utility",
    "blender": (3, 2, 0),
    "category": "Object",
}

import bpy
import importlib
import bauto.bauto.text_addon

class ReloadTextAddon(bpy.types.Operator):
    """Re-import the bauto text_addon.
    """
    
    bl_idname = "object.reload_cg_text_addon"
    bl_label = "Reload bauto text_addon"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        
        importlib.reload(bauto.bauto.text_addon)
        bauto.bauto.text_addon.register()

        return {'FINISHED'}

def register_operators():
    bpy.utils.register_class(ReloadTextAddon)

def register():
    register_operators()

def unregister():
    bpy.utils.unregister_class(ReloadTextAddon)


if __name__ == "__main__":
    register()

