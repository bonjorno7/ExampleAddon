import bpy
from . import objectmode


modules = (
    objectmode,
)


def register():
    keyconfig = bpy.context.window_manager.keyconfigs.addon

    for module in modules:
        module.register(keyconfig)


def unregister():
    keyconfig = bpy.context.window_manager.keyconfigs.addon

    for module in modules:
        keyconfig.keymaps.remove(module.keymap)
