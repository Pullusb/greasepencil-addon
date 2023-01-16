import bpy
import blf, gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector, Matrix
from time import time
from pathlib import Path

from bpy.props import (BoolProperty,
                       StringProperty,
                       IntProperty,
                       FloatVectorProperty,
                       IntProperty,
                       PointerProperty,
                       EnumProperty)

from .prefs import get_addon_prefs

lock_on = [
    Vector((18, 10)), Vector((2, 10)),
    Vector((2, 10)), Vector((2, 2)),
    Vector((2, 2)), Vector((18, 2)),
    Vector((18, 2)), Vector((18, 10)),
    Vector((6, 16)), Vector((4, 14)),
    Vector((14, 16)), Vector((16, 14)),
    Vector((6, 16)), Vector((14, 16)),
    Vector((4, 14)), Vector((4, 10)),
    Vector((16, 14)), Vector((16, 10)),
]

lock_off = [
    Vector((18, 10)), Vector((2, 10)),
    Vector((2, 10)), Vector((2, 2)),
    Vector((2, 2)), Vector((18, 2)),
    Vector((18, 2)), Vector((18, 10)),
    Vector((2, 16)), Vector((4, 14)),
    Vector((-6, 16)), Vector((-8, 14)),
    Vector((2, 16)), Vector((-6, 16)),
    Vector((4, 14)), Vector((4, 10)),
    Vector((-8, 14)), Vector((-8, 10)),
]

hide_off = [
    Vector((4, 4)), Vector((10, 2)),
    Vector((4, 12)), Vector((0, 8)),
    Vector((16, 12)), Vector((20, 8)),
    Vector((16, 4)), Vector((20, 8)),
    Vector((10, 4)), Vector((7, 5)),
    Vector((13, 5)), Vector((10, 4)),
    Vector((10, 12)), Vector((13, 11)),
    Vector((10, 14)), Vector((4, 12)),
    Vector((0, 8)), Vector((4, 4)),
    Vector((10, 14)), Vector((16, 12)),
    Vector((10, 2)), Vector((16, 4)),
    Vector((7, 11)), Vector((10, 12)),
    Vector((6, 8)), Vector((7, 11)),
    Vector((7, 5)), Vector((6, 8)),
    Vector((14, 8)), Vector((13, 5)),
    Vector((13, 11)), Vector((14, 8)),
]

hide_on = [
    Vector((4, 4)), Vector((10, 2)),
    Vector((16, 4)), Vector((20, 8)),
    Vector((0, 8)), Vector((4, 4)),
    Vector((10, 2)), Vector((16, 4)),
]


def rectangle_tris_from_coords(quad_list):
    '''Get a list of Vector corner for a triangle
    return a list of TRI for gpu drawing'''
    return [           
            # tri 1
            quad_list[0],
            quad_list[1],
            quad_list[2],
            # tri 2
            quad_list[0],
            quad_list[3],
            quad_list[2]
        ]

def move_layer_to_index(l, idx):
    a = [i for i, lay in enumerate(l.id_data.layers) if lay == l][0]
    move = idx - a
    if move == 0:
        return
    direction = 'UP' if move > 0 else 'DOWN'
    for _i in range(abs(move)):
        l.id_data.layers.move(l, direction)

def get_reduced_area_coord(context):
    w, h = context.region.width, context.region.height

    ## minus tool leftbar + sidebar right
    regs = context.area.regions
    toolbar = regs[2]
    sidebar = regs[3]
    header = regs[0]
    tool_header = regs[1]
    up_margin = down_margin = 0
    if tool_header.alignment == 'TOP':
        up_margin += tool_header.height
    else:
        down_margin += tool_header.height

    ## set corner values
    left_down = (toolbar.width, down_margin+2)
    right_down = (w - sidebar.width, down_margin+2)
    left_up = (toolbar.width, h - up_margin-1)
    right_up = (w - sidebar.width, h - up_margin-1)
    return left_down, right_down, left_up, right_up

def draw_callback_px(self, context):
    if context.area != self.current_area:
        return
    font_id = 0

    ## timer for debug purposes
    # blf.position(font_id, 15, 30, 0)
    # blf.size(font_id, 20, 72)
    # blf.draw(font_id, "Time " + self.text)

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')  # initiate shader
    gpu.state.blend_set('ALPHA')
    gpu.state.line_width_set(1.0)

    shader.bind()

    ## draw one background at once
    # shader.uniform_float("color", self.bg_color) # (1.0, 1.0, 1.0, 1.0)
    # self.batch_bg.draw(shader)

    ## locked layer (individual rectangle)
    rects = []
    lock_rects = []
    opacitys = []
    opacity_bars = []
    active_case = []
    # icons = [] # lineicons
    ## tex icon store
    icons = {'locked':[],'unlocked':[], 'hide_off':[], 'hide_on':[]}


    for i, l in enumerate(self.gpl):
        ## rect coords from bottom left corner

        corner = Vector((self.left, self.bottom + self.px_h * i))
        if i == self.ui_idx:
            active_case = [v + corner for v in self.case]

        lock_coord = corner + Vector((self.px_w - self.icons_margin_a, self.mid_height - int(self.icon_size / 2)))

        # Old width -70 (16 diff)
        hide_coord = corner + Vector((self.px_w - self.icons_margin_b, self.mid_height - int(self.icon_size / 2) - 2)) # extra -2 to align better with lock

        if l.lock:
            lock_rects += rectangle_tris_from_coords(
                [v + corner for v in self.case]
            )
            # icons += [v + lock_coord for v in lock_on] # lineicons
            icons['locked'].append([v + lock_coord for v in self.icon_tex_coord])
        else:
            rects += rectangle_tris_from_coords(
                [v + corner for v in self.case]
            )
            # icons += [v + lock_coord for v in lock_off] # lineicons
            icons['unlocked'].append([v + lock_coord for v in self.icon_tex_coord])

        # if l.hide: # lineicons
        #     icons += [v + hide_coord for v in hide_on] # lineicons
        # else: # lineicons
        #     icons += [v + hide_coord for v in hide_off] # lineicons

        if l.hide:
            icons['hide_on'].append([v + hide_coord for v in self.icon_tex_coord])
        else:
            icons['hide_off'].append([v + hide_coord for v in self.icon_tex_coord])


        ## opacity sliders background
        # if l.opacity != 1.0:
        opacity_bars += rectangle_tris_from_coords(
            [corner + v for v in self.opacity_slider]
        )
        ## opacity sliders
        if l.opacity:
            opacitys += rectangle_tris_from_coords(
                [corner + v for v in self.opacity_slider[:2]]
                + [corner +  Vector((int(v[0] * l.opacity), v[1])) for v in self.opacity_slider[2:]]
            )

    ## TODO: idea : colorize squares according to stroke type in the layer
    # -> need to be check at invoke, maybe too heavy check
    # -> maybe not evaluate every stroke in layers...

    ### --- Trace squares
    ## individual unlocked squares
    shader.uniform_float("color", self.bg_color)
    batch_squares = batch_for_shader(shader, 'TRIS', {"pos": rects})
    batch_squares.draw(shader)

    ## locked squares
    shader.uniform_float("color", self.lock_color)
    batch_lock = batch_for_shader(shader, 'TRIS', {"pos": lock_rects})
    batch_lock.draw(shader)

    ## bg_full_bar
    shader.uniform_float("color", self.opacity_bar_color)
    batch_lock = batch_for_shader(shader, 'TRIS', {"pos": opacity_bars})
    batch_lock.draw(shader)

    ## opacity sliders
    shader.uniform_float("color", self.opacity_color)
    batch_lock = batch_for_shader(shader, 'TRIS', {"pos": opacitys})
    batch_lock.draw(shader)

    ### --- Trace Lines
    gpu.state.line_width_set(2.0)

    ## line color
    shader.uniform_float("color", self.lines_color) # (1.0, 1.0, 1.0, 1.0)
    self.batch_lines.draw(shader)

    ## Lock/hide State icons
    # batch_icon = batch_for_shader(shader, 'LINES', {"pos": icons}) # lineicons
    # batch_icon.draw(shader) # lineicons

    ## Loop to draw tex icons
    for icon_name, coord_list in icons.items():
        texture = gpu.texture.from_image(self.icon_tex[icon_name])
        for coords in coord_list:
            shader_tex = gpu.shader.from_builtin('2D_IMAGE')
            batch_icons = batch_for_shader(
                shader_tex, 'TRI_FAN',
                {
                    "pos": coords,
                    "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
                },
            )
            shader_tex.bind()
            shader_tex.uniform_sampler("image", texture)
            batch_icons.draw(shader_tex)

    gpu.state.line_width_set(4.0)
    ## Highlight active layer
    if active_case:
        shader.uniform_float("color", self.active_layer_color) # (1.0, 1.0, 1.0, 1.0)
        active_case.append(active_case[0])
        batch_active = batch_for_shader(shader, 'LINE_STRIP', {"pos": active_case})
        batch_active.draw(shader)

    gpu.state.line_width_set(1.0)
    gpu.state.blend_set('NONE')


    ### --- Texts
    for i, l in enumerate(self.gpl):
        ## add color underneath active name
        # if i == self.ui_idx:
        #     ## color = self.active_layer_color # Color active name
        #     blf.position(font_id, self.text_x+1, self.text_pos[i]-1, 0)
        #     blf.size(font_id, self.text_size, 72)
        #     blf.color(font_id, *self.active_layer_color)
        #     blf.draw(font_id, l.info)
        if l.hide:
            color = self.hided_layer_color
        elif not len(l.frames) or (len(l.frames) == 1 and not len(l.frames[0].strokes)):
            # Show darker color if is empty if layer is empty (or has one empty keyframe)
            color = self.empty_layer_color
        else:
            color = self.other_layer_color

        blf.position(font_id, self.text_x, self.text_pos[i], 0)
        blf.size(font_id, self.text_size, 72)
        blf.color(font_id, *color)
        blf.draw(font_id, l.info)

    ## Drag text
    if self.dragging and self.drag_text:
        blf.position(font_id, self.mouse.x + 5, self.mouse.y + 5, 0)
        blf.size(font_id, self.text_size, 72)
        blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
        if self.drag_text == 'opacity_level':
            blf.draw(font_id, f'{self.gpl[self.ui_idx].opacity:.2f}')
        else:
            blf.draw(font_id, self.drag_text)


class GPT_OT_viewport_layer_nav_osd(bpy.types.Operator):
    bl_idname = "gpencil.viewport_layer_nav_osd"
    bl_label = "GP Layer Navigator Pop up"
    bl_description = "Change active GP layer with a viewport interactive OSD"
    bl_options = {'REGISTER', 'INTERNAL'}

    interval = 0.1
    limit = 2.2
    # fade_appear = 0.1
    lapse = 0
    text = ''
    color = ''
    ct = 0
    # px_w = 260
    # px_h = 90
    # text_size = 18
    left_handed = False

    icons_margin_a = 30
    icons_margin_b = 54

    use_fade = False
    ## set as prop so change is remembered upon next launch
    # use_fade : bpy.props.BoolProperty(name='Fade other layer', default=False)
    fade_value = 0.15

    bg_color = (0.1, 0.1, 0.1, 0.96)
    lock_color = (0.02, 0.02, 0.02, 0.98) # overlap opacity darken
    lines_color = (0.5, 0.5, 0.5, 0.6)
    opacity_bar_color = (0.25, 0.25, 0.25, 1.0)
    opacity_color = (0.4, 0.4, 0.4, 1.0) # (0.28, 0.45, 0.7, 1.0)

    other_layer_color = (0.8, 0.8, 0.8, 1.0) # strong grey
    active_layer_color = (0.28, 0.45, 0.7, 1.0) # Blue  (active color)
    empty_layer_color = (0.7, 0.5, 0.4, 1.0) # mid reddish grey # (0.5, 0.5, 0.5, 1.0) # mid grey
    hided_layer_color = (0.4, 0.4, 0.4, 1.0) # faded grey


    add_box = 24

    # value = None
    texts=[]

    def get_icon(self, img_name):
        store_name = '.' + img_name
        img = bpy.data.images.get(store_name)
        if not img:
            icon_folder = Path(__file__).parent / 'icons'
            img = bpy.data.images.load(filepath=str((icon_folder / img_name).with_suffix('.png')), check_existing=False)
            img.name = store_name

        return img


    def invoke(self, context, event):
        # Load texture icons
        ## stored in a dict
        self.icon_size = 20
        self.icon_tex_coord = (
            Vector((0, 0)),
            Vector((self.icon_size, 0)),
            Vector((self.icon_size, self.icon_size)),
            Vector((0, self.icon_size))
            )

        self.icon_tex = {n: self.get_icon(n) for n in ('locked','unlocked', 'hide_off', 'hide_on')}
        # self.locked_icon = self.get_icon('locked')
        # self.unlocked_icon = self.get_icon('unlocked')
        # self.hide_off_icon = self.get_icon('hide_off')
        # self.hide_on_icon = self.get_icon('hide_on')


        prefs = get_addon_prefs().nav
        self.px_h = prefs.box_height
        self.px_w = prefs.box_width
        self.text_size = prefs.text_size
        self.left_handed = prefs.left_handed

        # if not context.area.type == 'VIEW_3D':
        #     self.report({'WARNING'}, "View3D not found, cannot run operator")
        #     return {'CANCELLED'}
        # if not context.object or context.object.type != 'GPENCIL':
        #     self.report({'WARNING'}, "Active object not a Grease pencil object")
        #     return {'CANCELLED'}
        # if not 'GPENCIL' in context.mode:
        #     self.report({'WARNING'}, "Need to be in a grease pencil mode")
        #     return {'CANCELLED'}

        self.key = event.type

        wm = context.window_manager
        args = (self, context)

        self.current_area = context.area
        ## get layers
        self.gpl = context.object.data.layers
        if not len(self.gpl):
            self.report({'WARNING'}, "No layer to show")
            return {'CANCELLED'}
        if len(self.gpl) == 1:
            self.report({'WARNING'}, "Only one layer")
            return {'CANCELLED'}
        self.layer_list = [(l.info, l) for l in self.gpl]
        self.ui_idx = self.org_index = context.object.data.layers.active_index
        self.id_num = len(self.layer_list)
        self.dragging = False
        self.drag_mode = None
        self.drag_text = None
        self.pressed = False
        self.click_time = 0
        self.id_src = self.click_src = None
        self.mouse = self.init_mouse = Vector((event.mouse_region_x, event.mouse_region_y))

        ## Structure:
        # 
        #  ---  <-- top
        # |   |
        #  ---
        # |   |
        #  ---
        # |   | <-- bottom_base
        #  ---  <-- bottom

        max_w = self.px_w + self.add_box
        mid_square = int(self.px_w / 2)
        ## define zones
        bottom_base = self.init_mouse.y - (self.org_index * self.px_h) #  - self.px_h / 2
        self.text_bottom = bottom_base - int(self.text_size / 2) # self.text_size #

        self.mid_height = int(self.px_h / 2)
        self.bottom = bottom_base - self.mid_height
        self.top = self.bottom + (self.px_h * self.id_num)
        if self.left_handed:
            self.left = self.init_mouse.x - int(self.px_w / 10)
        else:
            # right hand
            self.left = self.init_mouse.x - mid_square

        ## Push from viewport borders if needed
        BL, BR, _1, _2 = get_reduced_area_coord(context)

        over_right = (self.left + max_w) - (BR[0] + 10) # from sidebar border
        # over_right = (self.left + max_w) - (context.area.width - 20) # from right border
        if over_right > 0:
            self.left = self.left - over_right

        # Priority on left push
        over_left = BL[0] - self.left # from toolbar border
        # over_left = 1 - self.left # from left border
        if over_left > 0:
            self.left = self.left + over_left

        self.right = self.left + self.px_w

        self.text_x = (self.left + mid_square) - int(self.px_w / 3)

        self.lines = []
        # self.texts = []
        self.text_pos = []
        self.ranges = []
        for i in range(self.id_num):
            y_coord = self.bottom + (i * self.px_h)
            self.lines += [(self.left, y_coord), (self.right, y_coord)]

            # self.texts.append((self.gpl[i].info, self.text_bottom + (i * self.px_h)))
            self.text_pos.append(self.text_bottom + (i * self.px_h))

            ## define index ranges
            self.ranges.append((y_coord, y_coord + self.px_h))


        ## add boxes 
        box = [
            Vector((0, 0)),
            Vector((self.add_box, 0)),
            Vector((self.add_box, self.add_box)),
            Vector((0, self.add_box)),
        ]

        self.add_box_zones = []
        mid = int(self.add_box / 2)
        marg = int(self.add_box / 4)
        plus = [
            Vector((mid, marg)), Vector((mid, self.add_box - marg)),
            Vector((marg, mid)), Vector((self.add_box - marg, mid)),
        ]
        plus_lines = []
        for i in range(len(self.gpl) + 1):
            height = self.bottom - self.add_box + (i * self.px_h)
            self.add_box_zones.append(
                [v + Vector((self.right,  height)) for v in box]
            )
            plus_lines += [v + Vector((self.right,  height)) for v in plus]

        self.add_box_rects = []
        for box in self.add_box_zones:
            self.add_box_rects += rectangle_tris_from_coords(box)

        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        # shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')

        self.case = [
            Vector((0, 0)),
            Vector((0, self.px_h)),
            Vector((self.px_w, self.px_h)),
            Vector((self.px_w, 0)),
        ]

        # self.opacity_slider_length = self.px_w - 80
        # self.opacity_slider_length = int(self.px_w / 2) # half-width
        self.opacity_slider_length = int(self.px_w * 68 / 100) # as width's percentage
        self.slider_height = 10
        self.opacity_slider = [
            Vector((0, self.px_h - self.slider_height)),
            Vector((0, self.px_h)),
            Vector((self.opacity_slider_length, self.px_h)),
            Vector((self.opacity_slider_length, self.px_h - self.slider_height)),
        ]

        # rectangle = rectangle_tris_from_coords([
        #      Vector((self.left, self.bottom)),
        #      Vector((self.left, self.top)),
        #      Vector((self.right, self.top)),
        #      Vector((self.right, self.bottom)),
        #     ])
        # self.batch_bg = batch_for_shader(
        #     # shader, 'TRIS', {"pos": rectangle + self.add_box_rects}) # box around plus sign
        #     shader, 'TRIS', {"pos": rectangle})

        ## Add contour lines
        self.lines += [Vector((self.left, self.top)), Vector((self.right, self.top)),
                    Vector((self.left, self.bottom)), Vector((self.right, self.bottom)),
                    Vector((self.left, self.top)), Vector((self.left, self.bottom)),
                    Vector((self.right, self.top)), Vector((self.right, self.bottom))]


        self.batch_lines = batch_for_shader(
            shader, 'LINES', {"pos": self.lines[2:] + plus_lines})

        self.first = True
        self.store_settings(context)

        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        # self._timer = wm.event_timer_add(0.1, window=context.window)

        wm.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}


    def set_fade(self, context):
        context.space_data.overlay.use_gpencil_fade_layers = True
        context.space_data.overlay.gpencil_fade_layer = self.fade_value
        self.use_fade=True

    def stop_fade(self, context):
        context.space_data.overlay.use_gpencil_fade_layers = self.org_use_gpencil_fade_layers
        context.space_data.overlay.gpencil_fade_layer = self.org_gpencil_fade_layer
        self.use_fade=False


    def store_settings(self, context):
        ## store values anyway
        self.org_use_gpencil_fade_layers = context.space_data.overlay.use_gpencil_fade_layers
        self.org_gpencil_fade_layer = context.space_data.overlay.gpencil_fade_layer
        if self.use_fade:
            self.set_fade(context)

    def id_from_coord(self, v):
        if v.y < self.ranges[0][0]:
            return 0 # return -1 # below deck
        for i, (bottom, top) in enumerate(self.ranges):
            if bottom < v.y < top:
                return i
        return i # return min if below and max if above instead of None

    def id_from_mouse(self):
        return self.id_from_coord(self.mouse)

    def click(self, context):
        ## check "add" zone
        if self.add_box_zones[0][0].x <= self.mouse.x <= self.add_box_zones[0][2].x:
            ## if its on a box zone, add layer at this place
            for i, zone in enumerate(self.add_box_zones):
                # if (zone[0].x <= self.mouse.x <= zone[2].x) and (zone[0].y <= self.mouse.y <= zone[2].y):
                if zone[0].y <= self.mouse.y <= zone[2].y:
                    # add layer
                    nl = context.object.data.layers.new('GP_Layer')
                    nl.frames.new(context.scene.frame_current, active=True)
                    nl.use_lights = False
                    if i == 0:
                        ## bottom layer, need to get down by one
                        # bpy.ops.gpencil.layer_move(type='DOWN')
                        self.gpl.move(nl, type='DOWN')
                    return True # stop the modal

        ## check hide / lock toggles
        hide_col = lock_col = False
        if self.right - self.icons_margin_a <= self.mouse.x <= self.right - self.icons_margin_a + 20:
            lock_col = True
        elif self.right - self.icons_margin_b - 6 <= self.mouse.x <= self.right - self.icons_margin_b + 20:
            hide_col = True

        if hide_col or lock_col:
            dist_from_case_bottom = self.mid_height - int(self.icon_size / 2)
            for i, l in enumerate(self.gpl):
                icon_base = self.bottom + (i * self.px_h) + dist_from_case_bottom
                if icon_base - 4 <= self.mouse.y <= icon_base + 20:
                    if hide_col:
                        self.gpl[i].hide = not self.gpl[i].hide # l.hide = not l.hide
                        self.drag_mode = 'hide' if self.gpl[i].hide else 'unhide'
                    elif lock_col:
                        self.gpl[i].lock = not self.gpl[i].lock # l.lock = not l.lock
                        self.drag_mode = 'lock' if self.gpl[i].lock else 'unlock'
                    return False

        ## Check if clicked on layer zone and remember which id

        # if (self.left <= self.mouse.x <= self.right) and (self.bottom <= self.mouse.y <= self.top):
        ## remove selection limit from left
        if (self.mouse.x <= self.right) and (self.bottom <= self.mouse.y <= self.top):
            ## rename on layer double click
            # /!\ problem ! 'Y' is still continuously pressed result: yyyyyyyyyyyes !
            # new_time = time()
            # print('new_time - self.click_time: ', new_time - self.click_time)
            # if new_time - self.click_time < 0.22:
            #     bpy.ops.wm.call_panel(name="GPTB_PT_layer_name_ui", keep_open=False)
            #     return True

            self.click_time = time()
            self.id_src = self.id_from_mouse() # self.ui_idx
            self.click_src = self.mouse.copy()

            top_case = self.bottom + self.px_h * (self.ui_idx + 1)
            # extra 10 px from top
            # if (top_case - self.slider_height) <= self.mouse.y <= top_case:
            if (top_case - 20) <= self.mouse.y <= top_case:
                ## On opacity slider
                self.drag_text = 'opacity_level'
                self.drag_mode = 'opacity'
                self.org_opacity = self.gpl[self.id_src].opacity
            else:
                ## on layer
                self.drag_text = self.gpl[self.id_src].info
                self.drag_mode = 'layer'
        return False

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse = Vector((event.mouse_region_x, event.mouse_region_y))
        current_idx = context.object.data.layers.active_index

        ## key tester
        # if event.type not in {self.key, 'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'TIMER_REPORT'}:
        #     print('key:', event.type, 'value:', event.value)

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.stop_mod(context)
            context.object.data.layers.active_index = self.org_index
            return {'CANCELLED'}

        if event.type == self.key and event.value == 'RELEASE':
            self.stop_mod(context)
            return {'FINISHED'}

        if event.type == 'X' and event.value == 'PRESS':
            # Toggle Xray
            context.object.show_in_front = not context.object.show_in_front

        ## set fade with a key
        if event.type == 'R' and event.value == 'PRESS':
            if self.use_fade:
                self.stop_fade(context)
            else:
                self.set_fade(context)

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.pressed = True
            stop = self.click(context)
            if stop:
                self.stop_mod(context)
                return {'FINISHED'}

        ## toggle based on distance
        # self.dragging = self.pressed and (self.mouse - self.click_src).length > 4

        ## toggle dragging once passed px amount from source
        if self.pressed and self.click_src:
            if (self.mouse - self.click_src).length > 4:
                self.dragging = True
            if self.dragging and self.drag_mode == 'opacity':
                x_travel = self.mouse[0] - self.click_src[0]
                change = x_travel / self.opacity_slider_length # value 0 to 1.0
                self.gpl[self.id_src].opacity = self.org_opacity + change


        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            ## check if there was an ongoing drag action
            if self.dragging:
                if self.drag_mode == 'layer' and self.id_src is not None:
                    # move layer
                    # print('move idx:', self.id_src, self.id_from_mouse())
                    move_layer_to_index(self.gpl[self.id_src], self.id_from_mouse())
                    self.id_src = None

            self.pressed = self.dragging = False
            self.click_src = self.drag_text = self.drag_mode = None

        ## Set Fade when passing sides of the list
        if self.left < self.mouse.x < self.right + self.add_box:
            if self.use_fade:
                self.stop_fade(context)
        else:
            if not self.use_fade:
                self.set_fade(context)

        ## Swap autolock
        if event.type == 'T' and event.value == 'PRESS':
            context.object.data.use_autolock_layers = not context.object.data.use_autolock_layers
            context.object.data.layers.active = context.object.data.layers.active # (force refresh of the autolocking)

        if event.type == 'H' and event.value == 'PRESS':
            bpy.ops.gpencil.layer_isolate(affect_visibility=True)
        if event.type == 'L' and event.value == 'PRESS':
            bpy.ops.gpencil.layer_isolate(affect_visibility=False)

            # return {'RUNNING_MODAL'}

        for i, (bottom, top) in enumerate(self.ranges):
            if bottom < self.mouse.y < top:
                self.ui_idx = i
                break

        if self.ui_idx == current_idx:
            return {'RUNNING_MODAL'}
        else:
            context.object.data.layers.active_index = self.ui_idx
            if self.drag_mode:
                ## maybe add a self.state value ?
                if self.drag_mode == 'hide' and not self.gpl[self.ui_idx].hide:
                    self.gpl[self.ui_idx].hide = True
                if self.drag_mode == 'unhide' and self.gpl[self.ui_idx].hide:
                    self.gpl[self.ui_idx].hide = False

                if self.drag_mode == 'lock' and not self.gpl[self.ui_idx].lock:
                    self.gpl[self.ui_idx].lock = True
                if self.drag_mode == 'unlock' and self.gpl[self.ui_idx].lock:
                    self.gpl[self.ui_idx].lock = False


        # if event.type == 'TIMER':
        #     #print(self._timer.time_delta, self._timer.time_duration, self._timer.time_step)
        #     self.lapse += self.interval
        #     self.text = '{:.1f}'.format(self.lapse)

        #     for text in self.texts:
        #         text.tick += self.interval
        #         if text.tick > text.up_time:
        #             if text.tick >= text.up_time + text.fade_time:
        #                 self.texts.pop(self.texts.index(text))
        #             else:
        #                 ## just decrement alpha
        #                 alpha = text.color[3] - self.interval / text.fade_time
        #                 alpha = 0 if alpha < 0 else alpha#clamp to 0
        #                 text.color[3] -= self.interval / text.fade_time

        #     if self.lapse >= self.limit:
        #         self.stop_mod(context)
        #         return {'FINISHED'}


        # if trigger:
        #     if self.first:
        #         self.store_settings(context)
        #         self.first=False
        #     self.lapse = 0#reset counter

        #     for text in self.texts:
        #         text.y += 30#move up previous

        return {'RUNNING_MODAL'} # running modal prevent original usage to be triggered (capture keys)

        # return {'PASS_THROUGH'}

    def stop_mod(self, context):
        # restore fade
        if self.use_fade:
            self.stop_fade(context)
        wm = context.window_manager
        # wm.event_timer_remove(self._timer)
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')

        context.area.tag_redraw()


class GPNAV_layer_navigation_settings(bpy.types.PropertyGroup):

    # sizes
    box_height: IntProperty(
        name="Layer Box Height",
        description="Individual layer box height.\
            \na big size take more screen space but allow better targeting",
        default=30,
        min=10,
        max=200,
        soft_min=26,
        soft_max=120,
        step=1,
        subtype='PIXEL')

    box_width: IntProperty(
        name="Layer Box Width",
        description="Individual layer box width.\
            \na big size take more screen space but allow better targeting",
        default=250,
        min=120,
        max=500,
        soft_min=150,
        soft_max=350,
        step=1,
        subtype='PIXEL')

    text_size: IntProperty(
        name="Label Size",
        description="Layer name label size",
        default=12,
        min=4,
        max=40,
        soft_min=8,
        soft_max=20,
        step=1,
        subtype='PIXEL')

    left_handed: BoolProperty(
        name='Left Handed',
        description="Pop-up appear offseted at the right of the mouse pointer\
            \nto avoif hand occluding layer label",
        default=False)



def draw_nav_pref(prefs, layout):
    # - General settings
    layout.label(text='Layer Navigation:')
    # layout.prop(prefs, 'use')
    # if not prefs.use:
    #     return
    col = layout.column()
    row = col.row()
    row.prop(prefs, 'box_height')
    row.prop(prefs, 'box_width')

    row = col.row()
    row.prop(prefs, 'text_size')
    row.prop(prefs, 'left_handed')

    # -/ Keymap -


addon_keymaps = []

def register_keymaps():
    addon = bpy.context.window_manager.keyconfigs.addon

    for name in [
        "Grease Pencil Stroke Paint Mode",
        "Grease Pencil Stroke Edit Mode",
        "Grease Pencil Stroke Sculpt Mode",
        "Grease Pencil Stroke Vertex Mode",
        "Grease Pencil Stroke Weight Mode",
            ]:
        km = addon.keymaps.new(name = name, space_type = "EMPTY")
        kmi = km.keymap_items.new('gpencil.viewport_layer_nav_osd', type='Y', value='PRESS')
        addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

classes = (
    GPT_OT_viewport_layer_nav_osd,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_keymaps()

def unregister():
    unregister_keymaps()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)