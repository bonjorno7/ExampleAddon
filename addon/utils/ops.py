import bpy


def cursor_warp(event):
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


def hide_hud():
    '''
    Hide the sidebar and redo panel.

    Returns:
        hud_info: Two booleans, to be used with show_hud.
    '''

    space_data = bpy.context.space_data
    sidebar = space_data.show_region_ui
    redo = space_data.show_region_hud

    if sidebar:
        space_data.show_region_ui = False

    if redo:
        space_data.show_region_hud = False

    return sidebar, redo


def show_hud(hud_info):
    '''
    Show the sidebar and redo panel.

    Args:
        hud_info: Two booleans, returned by hide_hud.
    '''

    sidebar, redo = hud_info
    space_data = bpy.context.space_data

    if sidebar:
        space_data.show_region_ui = True

    if redo:
        space_data.show_region_hud = True
