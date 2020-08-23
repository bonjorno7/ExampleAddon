import bpy
import blf


def draw_text(text, font, size, x, y, horizontal, vertical):
    blf.size(font, size, bpy.context.preferences.system.dpi)
    widths_l = [blf.dimensions(font, line[0])[0] for line in text]
    widths_r = [blf.dimensions(font, line[1])[0] for line in text]

    height = blf.dimensions(font, 'A')[1] * 1.5
    space = height * 0.75
    y += height * 0.25

    if horizontal == 'LEFT':
        x += max(widths_l) + space
    elif horizontal == 'RIGHT':
        x -= max(widths_r) + space

    if vertical == 'BOTTOM':
        y += height * len(text)
    elif vertical == 'CENTER':
        y += height * len(text) * 0.5

    for index, line in enumerate(text):
        offset = (index + 2) * height

        left, right = line
        width = widths_l[index]

        blf.position(font, x - width - space, y - offset, 0)
        blf.draw(font, left)

        blf.position(font, x + space, y - offset, 0)
        blf.draw(font, right)
