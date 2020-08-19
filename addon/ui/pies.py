import bpy
from .. import utils


class ExamplePie(bpy.types.Menu):
    bl_idname = 'EXAMPLE_MT_ExamplePie'
    bl_label = 'Example Pie'

    def draw(self, context):
        pie = self.layout.menu_pie()

        utils.ui.draw_op(pie, 'Useful Button', 'example.example_operator', axis='X')
