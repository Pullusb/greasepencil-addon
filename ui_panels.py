# SPDX-FileCopyrightText: 2020-2023 Blender Foundation
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy

class GP_PT_sidebarPanel(bpy.types.Panel):
    bl_label = "Grease Pencil Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Grease Pencil"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        # Box deform ops
        self.layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('view3d.gp_box_deform', icon ="MOD_MESHDEFORM")

        # Straight line ops
        layout.operator('gpencil.straight_stroke', icon ="CURVE_PATH")


        # Expose native view operators
        row = layout.row(align=True)
        row.operator('view3d.zoom_camera_1_to_1', text = 'Zoom 1:1', icon = 'ZOOM_PREVIOUS')
        row.operator('view3d.view_center_camera', text = 'Zoom Fit', icon = 'FULLSCREEN_ENTER')

        # Rotation save/load
        row = layout.row(align=True)
        row.operator('view3d.rotate_canvas_reset', text = 'Reset Rotation', icon = 'FILE_REFRESH')
        row.operator('view3d.rotate_canvas_set', text = 'Save Rotation', icon = 'DRIVER_ROTATIONAL_DIFFERENCE')

        # View flip
        if context.scene.camera and context.scene.camera.scale.x < 0:
            row = layout.row(align=True)
            row.operator('view3d.camera_flip_x', text = 'Camera Mirror Flip', icon = 'MOD_MIRROR')
            row.label(text='', icon='LOOP_BACK')
        else:
            layout.operator('view3d.camera_flip_x', text = 'Camera Mirror Flip', icon = 'MOD_MIRROR')


def menu_boxdeform_entry(self, context):
    """Transform shortcut to append in existing menu"""
    layout = self.layout
    obj = bpy.context.object
    if obj and obj.type == 'GREASEPENCIL' and context.mode in {'OBJECT', 'EDIT_GREASE_PENCIL', 'PAINT_GREASE_PENCIL'}:
        self.layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('view3d.gp_box_deform', text='Box Deform')

def menu_stroke_entry(self, context):
    layout = self.layout
    if context.mode in {'EDIT_GREASE_PENCIL', 'PAINT_GREASE_PENCIL'}:
        self.layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator('gpencil.straight_stroke', text='Straight Stroke')


def register():
    bpy.utils.register_class(GP_PT_sidebarPanel)
    ## VIEW3D_MT_edit_gpencil.append# Grease pencil menu
    bpy.types.VIEW3D_MT_transform_object.append(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_transform.append(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_edit_greasepencil_stroke.append(menu_stroke_entry)


def unregister():
    bpy.types.VIEW3D_MT_transform_object.remove(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_transform.remove(menu_boxdeform_entry)
    bpy.types.VIEW3D_MT_edit_greasepencil_stroke.remove(menu_stroke_entry)
    bpy.utils.unregister_class(GP_PT_sidebarPanel)
