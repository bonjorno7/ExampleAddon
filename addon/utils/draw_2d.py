import bpy
import blf


def draw_text(text, font, size, x, y, horizontal, vertical, shadow):
    '''
    Draw two aligned columns of text.

    Args:
        text: List of tuples of two strings.
        font: ID returned by blf.load or 0.
        size: How large the font should be.
        x, y: Pixel on the active area.
        horizontal: 'LEFT', 'CENTER', or 'RIGHT'.
        vertical: 'BOTTOM', 'CENTER', or 'TOP'.
        shadow: Whether to add a dropshadow.
    '''

    blf.size(font, size, bpy.context.preferences.system.dpi)
    widths_l = [blf.dimensions(font, line[0])[0] for line in text]
    widths_r = [blf.dimensions(font, line[1])[0] for line in text]

    height = blf.dimensions(font, 'A')[1] * 2
    space = height * 0.5
    y += height * 0.25

    if horizontal == 'LEFT':
        x += max(widths_l) + space
    elif horizontal == 'RIGHT':
        x -= max(widths_r) + space

    if vertical == 'BOTTOM':
        y += height * len(text)
    elif vertical == 'CENTER':
        y += height * len(text) * 0.5

    if shadow:
        blf.enable(font, blf.SHADOW)
        blf.shadow(font, 5, 0, 0, 0, 1)
        blf.shadow_offset(font, 1, -1)

    for index, line in enumerate(text):
        offset = (index + 2) * height

        left, right = line
        width = widths_l[index]

        blf.position(font, x - width - space, y - offset, 0)
        blf.draw(font, left)

        blf.position(font, x + space, y - offset, 0)
        blf.draw(font, right)

    if shadow:
        blf.disable(font, blf.SHADOW)
