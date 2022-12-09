import bpy
import pandas as pd
import matplotlib.pyplot as plt
import math

def load_data():
    
    raw_data = pd.read_csv('~/Downloads/STLFSI.csv')

    data = raw_data.copy()
    data.columns = ['date', 'vals']
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
#    data = data.head(100)
    data = data.resample('M').last()
    
    return data

def python_render_chart(data):
    
    # plot data in python
    data.plot()
    plt.draw()
    plt.show()

    py_chart = plt.gca()
    
    return py_chart

def map_py_chart_coords_to_blender_coords(py_chart, bl_width=8, bl_height=4, bl_x_offset=0, bl_z_offset=0):

    # get axes values in python coordinates
    py_x_lim = py_chart.get_xlim()
    py_y_lim = py_chart.get_ylim()
    py_x_ticks = py_chart.get_xticks()
    py_y_ticks = py_chart.get_yticks()
    
    # get x-tick labels
    x_text_objs = py_chart.get_xticklabels()
    x_labels_raw = [this_obj.get_text() for this_obj in x_text_objs]
    
    # fix "-" for negative values
    x_labels = [this_label.replace('−', '−-') for this_label in x_labels_raw]
    
    # add y-tick labels
    z_text_objs = py_chart.get_yticklabels()
    z_labels_raw = [this_obj.get_text() for this_obj in z_text_objs]
    
    z_labels = [this_label.replace('−', '−-') for this_label in z_labels_raw]

    # get chart line values; TODO: only first line is used so far
    py_x_vals = list(range(int(py_x_lim[0]), int(py_x_lim[1])+1))
    py_y_vals = py_chart.lines[0].get_ydata()

    assert len(py_x_vals) == len(py_y_vals) # Not sure whether this will hold for all charts

    # define mapping functions
    x_map_func = lambda x: (x - py_x_lim[0])/(py_x_lim[1] - py_x_lim[0])*bl_width + bl_x_offset
    z_map_func = lambda y: (y - py_y_lim[0])/(py_y_lim[1] - py_y_lim[0])*bl_height + bl_z_offset

    # chart coordinates
    bl_x_vals = x_map_func(py_x_vals)
    bl_z_vals = z_map_func(py_y_vals)

    # tick coordinates
    bl_x_ticks = x_map_func(py_x_ticks)
    bl_z_ticks = z_map_func(py_y_ticks)

    # axis limits
    bl_x_lim = x_map_func(py_x_lim)
    bl_z_lim = z_map_func(py_y_lim)

    return bl_x_lim, bl_z_lim, bl_x_ticks, bl_z_ticks, bl_x_vals, bl_z_vals, x_labels, z_labels

def x_z_coords_to_curve(bl_x_vals, bl_z_vals, obj_name):

    ## visualize in blender
    crv = bpy.data.curves.new(obj_name, type='CURVE')
    crv.dimensions = '3D'

    # map coords to spline
    polyline = crv.splines.new('POLY')
    polyline.points.add(len(bl_x_vals)-1)
    for ii in range(0, len(bl_x_vals)):
        x_val = bl_x_vals[ii]
        z_val = bl_z_vals[ii]
        polyline.points[ii].co = (x_val, 0, z_val, 1)
        
#    bpy.ops.curve.select_all(action='SELECT')
#    bpy.ops.curve.handle_type_set(type='VECTOR')

    # create Object
    crv_obj = bpy.data.objects.new(obj_name, crv)
    
    return crv_obj

def add_axis_labels(axis, x_labels, bl_x_ticks, obj_name, obj_collection):
        
    #for ii in range(0, len(bl_x_ticks)):
    for ii in range(0, len(bl_x_ticks)):
        
        this_bl_x_tick = bl_x_ticks[ii]
        this_text = x_labels[ii]

        if axis=='x':
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(this_bl_x_tick, 0, 0), scale=(1, 1, 1))
        elif axis=='z':
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(0, 0, this_bl_x_tick), scale=(1, 1, 1))
        else:
            raise ValueError('Unknown axis reference; Only "x" or "z" are allowed')
        
        obj = bpy.context.active_object
        bpy.data.collections[obj_collection].objects.link(obj)
        
        obj.name = obj_name
        obj.data.body = this_text
        obj.rotation_euler[0] = math.radians(90)
        if axis=='x':
            obj.data.align_x = 'CENTER'
            bpy.context.object.data.align_y = 'TOP'
        else:
            obj.data.align_x = 'RIGHT'
            bpy.context.object.data.align_y = 'CENTER'
            
        scal_val = 0.2
        obj.scale = (scal_val, scal_val, scal_val)
        
def create_chart_collections():

    # add collections
    #chart_coll = bpy.data.collections.new("chart_line")
    #bpy.context.scene.collection.children.link(chart_coll)

    axes_coll = bpy.data.collections.new("chart_axes")
    bpy.context.scene.collection.children.link(axes_coll)

    x_labels_coll = bpy.data.collections.new("x_labels")
    axes_coll.children.link(x_labels_coll)

    z_labels_coll = bpy.data.collections.new("z_labels")
    axes_coll.children.link(z_labels_coll)
    
data = load_data()
py_chart = python_render_chart(data)
bl_x_lim, bl_z_lim, bl_x_ticks, bl_z_ticks, bl_x_vals, bl_z_vals, x_labels, z_labels = map_py_chart_coords_to_blender_coords(py_chart, bl_width=8, bl_height=4, bl_x_offset=0, bl_z_offset=0)


create_chart_collections()

x_axis_obj = x_z_coords_to_curve(bl_x_lim, [0,0], 'x_axis')
z_axis_obj = x_z_coords_to_curve([0,0], bl_z_lim, 'z_axis')

bpy.data.scenes[0].collection.objects.link(x_axis_obj)
bpy.data.scenes[0].collection.objects.link(z_axis_obj)

add_axis_labels('x', x_labels, bl_x_ticks, 'x_tick_label', 'x_labels')
add_axis_labels('z', z_labels, bl_z_ticks, 'z_tick_label', 'z_labels')

#crv_obj = x_z_coords_to_curve(bl_x_vals, bl_z_vals, 'FSI')
#bpy.data.scenes[0].collection.objects.link(crv_obj)

obj_name = 'FSI'
crv = bpy.data.curves.new(obj_name, type='CURVE')
crv.dimensions = '3D'

# map coords to spline
line_curve = crv.splines.new('BEZIER')

for ii in range(0, len(bl_x_vals)):
    
    line_curve.bezier_points.add(1)
    bez_point = line_curve.bezier_points[-1]

    x_val = bl_x_vals[ii]
    z_val = bl_z_vals[ii]
    bez_point.co = (x_val, 0, z_val)
    bez_point.handle_right_type = 'ALIGNED'
    bez_point.handle_left_type = 'ALIGNED'
    
    scal_factor = 0.006
    
    #Reset left handle to correct length
    b_loc = bez_point.co
    l_loc_new = bez_point.handle_left
    l_vec = l_loc_new - b_loc
    bez_point.handle_left = b_loc - scal_factor * l_vec.normalized()

    #Reset right handle to correct length
    r_loc_new = bez_point.handle_right
    r_vec = r_loc_new - b_loc
    bez_point.handle_right = b_loc - scal_factor * r_vec.normalized()

crv_obj = bpy.data.objects.new(obj_name, crv)
bpy.data.scenes[0].collection.objects.link(crv_obj)
bpy.context.view_layer.objects.active = crv_obj

#crv_obj.select_set(True)
#bpy.ops.object.editmode_toggle()
#bpy.ops.curve.select_all(action='SELECT')
#bpy.ops.curve.handle_type_set(type='VECTOR')




import bpy
import pandas as pd
import matplotlib.pyplot as plt
import math

def load_data():
    
    raw_data = pd.read_csv('~/Downloads/STLFSI.csv')

    data = raw_data.copy()
    data.columns = ['date', 'vals']
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
#    data = data.head(100)
    data = data.resample('M').last()
    
    return data

def python_render_chart(data):
    
    # plot data in python
    data.plot()
    plt.draw()
    plt.show()

    py_chart = plt.gca()
    
    return py_chart

def map_py_chart_coords_to_blender_coords(py_chart, bl_width=8, bl_height=4, bl_x_offset=0, bl_z_offset=0):

    # get axes values in python coordinates
    py_x_lim = py_chart.get_xlim()
    py_y_lim = py_chart.get_ylim()
    py_x_ticks = py_chart.get_xticks()
    py_y_ticks = py_chart.get_yticks()
    
    # get x-tick labels
    x_text_objs = py_chart.get_xticklabels()
    x_labels_raw = [this_obj.get_text() for this_obj in x_text_objs]
    
    # fix "-" for negative values
    x_labels = [this_label.replace('−', '−-') for this_label in x_labels_raw]
    
    # add y-tick labels
    z_text_objs = py_chart.get_yticklabels()
    z_labels_raw = [this_obj.get_text() for this_obj in z_text_objs]
    
    z_labels = [this_label.replace('−', '−-') for this_label in z_labels_raw]

    # get chart line values; TODO: only first line is used so far
    py_x_vals = list(range(int(py_x_lim[0]), int(py_x_lim[1])+1))
    py_y_vals = py_chart.lines[0].get_ydata()

    assert len(py_x_vals) == len(py_y_vals) # Not sure whether this will hold for all charts

    # define mapping functions
    x_map_func = lambda x: (x - py_x_lim[0])/(py_x_lim[1] - py_x_lim[0])*bl_width + bl_x_offset
    z_map_func = lambda y: (y - py_y_lim[0])/(py_y_lim[1] - py_y_lim[0])*bl_height + bl_z_offset

    # chart coordinates
    bl_x_vals = x_map_func(py_x_vals)
    bl_z_vals = z_map_func(py_y_vals)

    # tick coordinates
    bl_x_ticks = x_map_func(py_x_ticks)
    bl_z_ticks = z_map_func(py_y_ticks)

    # axis limits
    bl_x_lim = x_map_func(py_x_lim)
    bl_z_lim = z_map_func(py_y_lim)

    return bl_x_lim, bl_z_lim, bl_x_ticks, bl_z_ticks, bl_x_vals, bl_z_vals, x_labels, z_labels

def x_z_coords_to_curve(bl_x_vals, bl_z_vals, obj_name):

    ## visualize in blender
    crv = bpy.data.curves.new(obj_name, type='CURVE')
    crv.dimensions = '3D'

    # map coords to spline
    polyline = crv.splines.new('POLY')
    polyline.points.add(len(bl_x_vals)-1)
    for ii in range(0, len(bl_x_vals)):
        x_val = bl_x_vals[ii]
        z_val = bl_z_vals[ii]
        polyline.points[ii].co = (x_val, 0, z_val, 1)
        
#    bpy.ops.curve.select_all(action='SELECT')
#    bpy.ops.curve.handle_type_set(type='VECTOR')

    # create Object
    crv_obj = bpy.data.objects.new(obj_name, crv)
    
    return crv_obj

def add_axis_labels(axis, x_labels, bl_x_ticks, obj_name, obj_collection):
        
    #for ii in range(0, len(bl_x_ticks)):
    for ii in range(0, len(bl_x_ticks)):
        
        this_bl_x_tick = bl_x_ticks[ii]
        this_text = x_labels[ii]

        if axis=='x':
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(this_bl_x_tick, 0, 0), scale=(1, 1, 1))
        elif axis=='z':
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(0, 0, this_bl_x_tick), scale=(1, 1, 1))
        else:
            raise ValueError('Unknown axis reference; Only "x" or "z" are allowed')
        
        obj = bpy.context.active_object
        bpy.data.collections[obj_collection].objects.link(obj)
        
        obj.name = obj_name
        obj.data.body = this_text
        obj.rotation_euler[0] = math.radians(90)
        if axis=='x':
            obj.data.align_x = 'CENTER'
            bpy.context.object.data.align_y = 'TOP'
        else:
            obj.data.align_x = 'RIGHT'
            bpy.context.object.data.align_y = 'CENTER'
            
        scal_val = 0.2
        obj.scale = (scal_val, scal_val, scal_val)
        
def create_chart_collections():

    # add collections
    #chart_coll = bpy.data.collections.new("chart_line")
    #bpy.context.scene.collection.children.link(chart_coll)

    axes_coll = bpy.data.collections.new("chart_axes")
    bpy.context.scene.collection.children.link(axes_coll)

    x_labels_coll = bpy.data.collections.new("x_labels")
    axes_coll.children.link(x_labels_coll)

    z_labels_coll = bpy.data.collections.new("z_labels")
    axes_coll.children.link(z_labels_coll)
    
data = load_data()
py_chart = python_render_chart(data)
bl_x_lim, bl_z_lim, bl_x_ticks, bl_z_ticks, bl_x_vals, bl_z_vals, x_labels, z_labels = map_py_chart_coords_to_blender_coords(py_chart, bl_width=8, bl_height=4, bl_x_offset=0, bl_z_offset=0)


create_chart_collections()

x_axis_obj = x_z_coords_to_curve(bl_x_lim, [0,0], 'x_axis')
z_axis_obj = x_z_coords_to_curve([0,0], bl_z_lim, 'z_axis')

bpy.data.scenes[0].collection.objects.link(x_axis_obj)
bpy.data.scenes[0].collection.objects.link(z_axis_obj)

add_axis_labels('x', x_labels, bl_x_ticks, 'x_tick_label', 'x_labels')
add_axis_labels('z', z_labels, bl_z_ticks, 'z_tick_label', 'z_labels')

#crv_obj = x_z_coords_to_curve(bl_x_vals, bl_z_vals, 'FSI')
#bpy.data.scenes[0].collection.objects.link(crv_obj)

obj_name = 'FSI'
crv = bpy.data.curves.new(obj_name, type='CURVE')
crv.dimensions = '3D'

# map coords to spline
line_curve = crv.splines.new('BEZIER')

for ii in range(0, len(bl_x_vals)):
    
    line_curve.bezier_points.add(1)
    bez_point = line_curve.bezier_points[-1]

    x_val = bl_x_vals[ii]
    z_val = bl_z_vals[ii]
    bez_point.co = (x_val, 0, z_val)
    bez_point.handle_right_type = 'ALIGNED'
    bez_point.handle_left_type = 'ALIGNED'
    
    scal_factor = 0.006
    
    #Reset left handle to correct length
    b_loc = bez_point.co
    l_loc_new = bez_point.handle_left
    l_vec = l_loc_new - b_loc
    bez_point.handle_left = b_loc - scal_factor * l_vec.normalized()

    #Reset right handle to correct length
    r_loc_new = bez_point.handle_right
    r_vec = r_loc_new - b_loc
    bez_point.handle_right = b_loc - scal_factor * r_vec.normalized()

crv_obj = bpy.data.objects.new(obj_name, crv)
bpy.data.scenes[0].collection.objects.link(crv_obj)
bpy.context.view_layer.objects.active = crv_obj

#crv_obj.select_set(True)
#bpy.ops.object.editmode_toggle()
#bpy.ops.curve.select_all(action='SELECT')
#bpy.ops.curve.handle_type_set(type='VECTOR')




import bpy
import bauto.utils as bautils
import bauto.text_utils as batext
import importlib
import math

importlib.reload(batext)
importlib.reload(bautils)

bautils.clear_all_objects()

obj_name = 'animation_text'
text_str = 'BRONZE'
text_str = '5-2-1 rule'
obj = batext.add_text_object(text_str, obj_name)

fonts_path = "/usr/share/fonts/fonts-go/Go-Mono.ttf"
batext.make_text_2d_to_3d(obj)
    
char_obj_arr = batext.split_text_to_characters(obj)
bpy.ops.object.select_all(action='DESELECT')

n_frames_animation = 50
animation_offset = 0
individual_character_offset = 8
counter = 0

n_chars = len(char_obj_arr)
for ii in range(n_chars-1, -1, -1):
    this_obj = char_obj_arr[ii]
    this_character_offset = animation_offset + counter*individual_character_offset
    batext.letter_animation(this_obj, n_frames_animation, this_character_offset)
    counter += 1

bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.frame_set(0)