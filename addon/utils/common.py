import bpy
from .. import props


def module():
    return props.addon.name


def prefs():
    return bpy.context.preferences.addons[module()].preferences


def description(*args):
    return '.\n'.join(args)


def sanitize(text: str):
    return ''.join('_' if c in ':*?"<>|' else c for c in text)
