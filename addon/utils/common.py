import bpy
import pathlib
import platform
import ctypes.wintypes
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


def documents():
    '''Get the documents folder on Windows, or the home folder on other platforms.'''
    if platform.system() == 'Windows':
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)

        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 1, buf)
        return pathlib.Path(buf.value)

    else:
        return pathlib.Path.home()


def appdata():
    '''Get the path to the appdata folder for this version of Blender.'''
    user = bpy.utils.resource_path('USER')
    return pathlib.Path(user).resolve()
