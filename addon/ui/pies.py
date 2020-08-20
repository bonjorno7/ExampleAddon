import bpy


class ExamplePie(bpy.types.Menu):
    bl_idname = 'EXAMPLE_MT_ExamplePie'
    bl_label = 'Example Pie'

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        op = pie.operator('example.example_operator', text='Useful Button')
        op.axis = 'X'
