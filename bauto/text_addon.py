bl_info = {
    "name": "CG 3D text animation tools",
    "blender": (3, 2, 0),
    "category": "Object",
}

import bpy
import math
import bauto.bauto.text_utils as batext

class Text2dTo3d(bpy.types.Operator):
    """Transform 2D text into standardized 3D text"""
    
    bl_idname = "object.text_2d_to_3d"
    bl_label = "Text 2D to 3D"
    bl_options = {'REGISTER', 'UNDO'} # allow dynamic interaction

    extrude: bpy.props.FloatProperty(name="Extrusion", default=0.122, min=0, max=100)
    bevel: bpy.props.FloatProperty(name="Bevel depth", default=0.01, min=0, max=10)
    default_text_style: bpy.props.BoolProperty(name="Adapt text style", default=True)
    
    @classmethod
    def poll(cls, context):
        is_object_mode = (context.mode == 'OBJECT')
        active_object_exists = (context.active_object is not None)
        return is_object_mode & active_object_exists
    
    def execute(self, context):
        obj = context.active_object # TODO: allow multiple objects, selection instead of active object

        if self.default_text_style:
            batext.make_default_text_style(obj)

        batext.make_text_2d_to_3d(obj, self.extrude, self.bevel)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}


class SplitTextToChars(bpy.types.Operator):
    """Transform text object into mesh and split into characters"""
    
    bl_idname = "object.split_text_to_chars"
    bl_label = "Split text into characters"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        is_object_mode = (context.mode == 'OBJECT')
        active_object_exists = (context.active_object is not None)
        return is_object_mode & active_object_exists
    
    def execute(self, context):
        obj = context.active_object
        
        # convert to mesh
        # remove doubles to e.g. combine inner and outer circle of letter "O"
        # separate into individual characters
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'} 

def register_operators():
    bpy.utils.register_class(Text2dTo3d)
    bpy.utils.register_class(SplitTextToChars)


def menu_func_1(self, context):
    self.layout.operator(Text2dTo3d.bl_idname)

def menu_func_2(self, context):
    self.layout.operator(SplitTextToChars.bl_idname)

def register_operators_to_object_menu():
    bpy.types.VIEW3D_MT_object.append(menu_func_1)
    bpy.types.VIEW3D_MT_object.append(menu_func_2)

#def register_operators_to_object_region_panel():
#    # TODO: add to panel for easy access to operator properties
    

def register():
    register_operators()
    register_operators_to_object_menu()
    

def unregister():
    bpy.utils.unregister_class(Text2dTo3d)
    bpy.utils.unregister_class(SplitTextToChars)

# class TextRoutinesPanel(bpy.types.Panel):
#     bl_idname = "OBJECT_PT_text_routines"
#     bl_label = "Text Routines"
#     bl_space_type = 'PROPERTIES' # properties editor
#     bl_region_type = 'WINDOW'
#     bl_context = "data" # object data tab

#     def draw(self, context):
#         #self.layout.operator("object.text_2d_to_3d")
        
#         layout = self.layout
#         col = layout.column()
        
#         col.prop(kmi.properties, "extrude")
#         col.prop(kmi.properties, "bevel")
#         op = col.operator("object.text_2d_to_3d")
#         op.extrude = kmi.properties.extrude
#         op.bevel = kmi.properties.bevel
        
#         op = context.active_operator
#         if op and op.bl_idname == "Text2dTo3d":
#             layout = self.layout
#             col = layout.column()
#             for prop in op.properties.keys():
#                 col.prop(op.properties, prop)
    

# bpy.utils.register_class(TextRoutinesPanel)
# kmi = bpy.context.window_manager.keyconfigs.addon.keymaps['File Browser Main'].keymap_items.new("object.text_2d_to_3d", "NONE", "ANY")


# TODO:
# - add a panel to properties editor, object data properties tab ("text tab")
# - panel name: Text Routines
# - add operators / animations:
#   - 2D to 3D (w or w/o text rotation)
#   - text splitting to characters
#   - text animations

if __name__ == "__main__":
    register()