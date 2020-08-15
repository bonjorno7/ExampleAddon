import bpy
from .. import utils


name = __name__.partition('.')[0]


class AddonProps(bpy.types.PropertyGroup):
    addon: bpy.props.StringProperty(
        name='Addon',
        description='The module for this addon',
        default=name,
    )

    @property
    def prefs(self):
        return utils.common.prefs()
