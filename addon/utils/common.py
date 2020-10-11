import bpy
import pathlib
import platform
import ctypes.wintypes
from .. import props


def module() -> str:
    '''The top level module for this addon.'''
    return props.addon.name


def prefs() -> bpy.types.AddonPreferences:
    '''The preferences for this addon.'''
    return bpy.context.preferences.addons[module()].preferences


def sanitize(text: str) -> str:
    '''
    Replace invalid characters with underscores.
    
    Args:
        text: String containing invalid characters.

    Returns:
        sanitized: String that can be used as file path.
    '''

    return ''.join('_' if c in ':*?"<>|' else c for c in text)


def documents() -> pathlib.Path:
    '''Get the documents folder on Windows, or the home folder on other platforms.'''
    if platform.system() == 'Windows':
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)

        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 1, buf)
        return pathlib.Path(buf.value)

    else:
        return pathlib.Path.home()


def appdata() -> pathlib.Path:
    '''Get the path to the appdata folder for this version of Blender.'''
    user = bpy.utils.resource_path('USER')
    return pathlib.Path(user).resolve()
