import bpy


class ExampleOperator(bpy.types.Operator):
    bl_idname = 'example.example_operator'
    bl_label = 'Example Operator'

    def execute(self, context):
        self.report({'INFO'}, 'Placeholder')
        return {'FINISHED'}
