import bpy


def description(*args):
    return '.\n'.join(args)


def header(*args):
    return ' | '.join(args)


def statistics(header, context):
    if bpy.app.version < (2, 90, 0):
        layout = header.layout
        layout.separator_spacer()

        text = context.scene.statistics(context.view_layer)
        layout.label(text=text, translate=False)


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
