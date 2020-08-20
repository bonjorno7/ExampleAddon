import bpy


class BasePanel:
    bl_space_type = 'VIEW_3D'
    bl_category = 'Example'
    bl_region_type = 'UI'


class ExamplePanel(BasePanel, bpy.types.Panel):
    bl_idname = 'EXAMPLE_PT_ExamplePanel'
    bl_label = 'Example Panel'

    def draw(self, context):
        layout = self.layout

        op = layout.operator('example.example_operator', text='Useful Button')
        op.axis = 'Z'
