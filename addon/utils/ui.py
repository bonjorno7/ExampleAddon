import bpy
from .. import ui


def update_panel_category(self, context):
    '''
    Change the category for addon panels.

    Args:
        self: Prefs which store panel_category.
        context: Current blender context.
    '''

    category = self.panel_category
    region_type = 'UI' if category else 'HEADER'

    for cls in ui.classes:
        if hasattr(cls, 'bl_category'):
            cls.bl_category = category
            cls.bl_region_type = region_type

            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)


def description(*args):
    '''Join arguments with `.\n` between each.'''
    return '.\n'.join(args)


def header(*args):
    '''Join arguments with ` | ` between each.'''
    return ' | '.join(args)


def statistics(header, context):
    '''
    Add scene statistics to the end of the status bar.

    Args:
        header: The status bar to draw on.
        context: Current blender context.
    '''

    if bpy.app.version < (2, 90, 0):
        layout = header.layout
        layout.separator_spacer()

        text = context.scene.statistics(context.view_layer)
        layout.label(text=text, translate=False)
