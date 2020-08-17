import bpy


keymap = None


def register(keyconfig):
    global keymap
    keymap = keyconfig.keymaps.new(name='Object Mode', space_type='EMPTY')

    item = keymap.keymap_items.new('example.example_operator', 'E', 'PRESS')
    item.properties.axis = 'Y'
