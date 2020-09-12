import bpy
from .. import ui
from .. import utils


class AddonPrefs(bpy.types.AddonPreferences):
    bl_idname = utils.common.module()

    panel_category: bpy.props.StringProperty(
        name='Panel Category',
        description='What category to show addon panels in, leave empty to hide them entirely',
        default=ui.panels.BasePanel.bl_category,
        update=utils.ui.update_panel_category,
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, 'panel_category')
