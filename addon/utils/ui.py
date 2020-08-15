import bpy
from .. import ui


def update_panel_category(self, context):
    category = self.panel_category
    region_type = 'UI' if category else 'HEADER'

    for cls in ui.classes:
        if hasattr(cls, 'bl_category'):
            cls.bl_category = category
            cls.bl_region_type = region_type

            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)


def draw_prop(layout, text, data, prop):
    row = layout.row()
    row.label(text=text)
    row.prop(data, prop, text='')


def draw_bool(layout, text, data, prop):
    row = layout.row()
    row.label(text=text)

    col = row.column()
    col.alignment = 'RIGHT'
    col.prop(data, prop, text='')


def draw_op(layout, text, operator, options={}):
    op = layout.operator(operator, text=text)

    for key, value in options.items():
        op[key] = value
