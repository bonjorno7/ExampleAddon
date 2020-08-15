import bpy
from .. import utils


class ExamplePanel(bpy.types.Panel):
    bl_idname = 'EXAMPLE_PT_ExamplePanel'
    bl_category = 'Example'
    bl_label = 'Example Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        column = self.layout.column()

        box = column.box()
        utils.ui.draw_op(box, 'Useless Button', 'example.example_operator')
