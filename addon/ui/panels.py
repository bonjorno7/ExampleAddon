import bpy
from .. import utils


class BasePanel:
    bl_space_type = 'VIEW_3D'
    bl_category = 'Example'
    bl_region_type = 'UI'


class ExamplePanel(BasePanel, bpy.types.Panel):
    bl_idname = 'EXAMPLE_PT_ExamplePanel'
    bl_label = 'Example Panel'

    def draw(self, context):
        column = self.layout.column()

        box = column.box()
        utils.ui.draw_op(box, 'Useless Button', 'example.example_operator')
