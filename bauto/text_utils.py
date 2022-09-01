import bpy
import math

TEXT_STYLE = {'text_alignment_x': 'CENTER',
                 'text_fonts_path': "/usr/share/fonts/fonts-go/Go-Mono.ttf"
                 }
TEXT_3D = {'extrude': 0.122,
           'bevel': 0.01}

def make_text_2d_to_3d(obj, extrude=0.122, bevel=0.01):

    # modify text: 2D -> 3D, center, different fonts

    obj.data.extrude = extrude # extrude to make 3D
    obj.data.bevel_depth = bevel # bevel to get smoother edges

def make_default_text_style(obj):
    
    obj.rotation_euler[0] = math.radians(90)

    obj.data.align_x = TEXT_STYLE['text_alignment_x']

    fonts_path = TEXT_STYLE['text_fonts_path']
    fnt = bpy.data.fonts.load(fonts_path)
    obj.data.font = fnt

def make_default_text(obj):
    """2D to 3D; text style (alignment, rotation, fonts)"""

    make_default_text_style(obj)
    make_text_2d_to_3d(obj, TEXT_3D['extrude'], TEXT_3D['bevel'])

def split_text_to_characters(text_obj):
    """
    - Convert text to mesh
    - Remove doubles: in order to join multiple parts of a single character together 
      (e.g. inner and outer circle of "O")
    - Separate again into individual characters
    """
    
    text_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    
    char_obj_arr = bpy.context.selected_objects

    return char_obj_arr


