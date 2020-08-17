import bpy
from . import panels
from . import pies


classes = (
    panels.ExamplePanel,
    pies.ExamplePie,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
