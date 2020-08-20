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
