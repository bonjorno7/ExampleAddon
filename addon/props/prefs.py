import bpy
from .. import utils


class AddonPrefs(bpy.types.AddonPreferences):
    bl_idname = utils.common.module()

    panel_category: bpy.props.StringProperty(
        name='Panel Category',
        description='What category to show addon panels in, leave empty to hide them entirely',
        default='Example',
        update=utils.ui.update_panel_category,
    )

    def draw(self, context):
        utils.ui.draw_prop(self.layout, 'Panel Category', self, 'panel_category')
