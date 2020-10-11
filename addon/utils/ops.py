import bpy
import typing


def cursor_warp(event: bpy.types.Event):
    '''
    Warp the cursor to keep it inside the active area.
    
    Args:
        event: Modal operator event.
    '''

    area = bpy.context.area
    prefs = bpy.context.preferences
    offset = prefs.view.ui_scale * 100

    left = area.x + offset
    right = area.x + area.width - offset
    x = event.mouse_x

    down = area.y + offset
    up = area.y + area.height - offset
    y = event.mouse_y

    if x < left:
        x = right + x - left
    elif x > right:
        x = left + x - right

    if y < down:
        y = up + y - down
    elif y > up:
        y = down + y - up

    if x != event.mouse_x or y != event.mouse_y:
        bpy.context.window.cursor_warp(x, y)


def hide_hud() -> typing.Tuple[bool, bool, bool]:
    '''
    Hide the toolbar, sidebar, and redo panel.

    Returns:
        hud_info: Three booleans, to be used with show_hud.
    '''

    space_data = bpy.context.space_data
    toolbar = space_data.show_region_toolbar
    sidebar = space_data.show_region_ui
    redo = space_data.show_region_hud

    if toolbar:
        space_data.show_region_toolbar = False

    if sidebar:
        space_data.show_region_ui = False

    if redo:
        space_data.show_region_hud = False

    return toolbar, sidebar, redo


def show_hud(hud_info: typing.Tuple[bool, bool, bool]):
    '''
    Show the toolbar, sidebar, and redo panel.

    Args:
        hud_info: Three booleans, returned by hide_hud.
    '''

    toolbar, sidebar, redo = hud_info
    space_data = bpy.context.space_data

    if toolbar:
        space_data.show_region_toolbar = True

    if sidebar:
        space_data.show_region_ui = True

    if redo:
        space_data.show_region_hud = True
