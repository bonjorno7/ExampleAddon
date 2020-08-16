import bpy


def description(*args):
    return '.\n'.join(args)


def header(*args):
    return ' | '.join(args)


def write_status_and_header(self):
    bpy.context.workspace.status_text_set(self.status)
    bpy.context.area.header_text_set(self.header)


def clear_status_and_header(self):
    bpy.context.workspace.status_text_set(None)
    bpy.context.area.header_text_set(None)


def cursor_warp(event):
    area = bpy.context.area
    prefs = bpy.context.preferences
    offset = prefs.view.ui_scale * 200

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