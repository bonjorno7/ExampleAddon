import bpy
from .. import props


def module():
    '''The top level module for this addon.'''
    return props.addon.name


def prefs():
    '''The preferences for this addon.'''
    return bpy.context.preferences.addons[module()].preferences


def sanitize(text):
    '''
    Replace invalid characters with underscores.
    
    Args:
        text: String containing invalid characters.

    Returns:
        sanitized: String that can be used as file path.
    '''

    return ''.join('_' if c in ':*?"<>|' else c for c in text)
