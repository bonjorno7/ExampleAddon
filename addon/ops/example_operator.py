import bpy
from .. import utils


class ExampleOperator(bpy.types.Operator):
    bl_idname = 'example.example_operator'
    bl_label = 'Example Operator'
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}


    axis: bpy.props.EnumProperty(
        name='Axis',
        description='Which axis to move the object on',
        items=[
            ('X', 'X', ''),
            ('Y', 'Y', ''),
            ('Z', 'Z', ''),
        ],
        default='X',
    )


    offset: bpy.props.FloatProperty(
        name='Offset',
        description='How much to move the object',
        default=0,
    )


    @classmethod
    def description(cls, context, properties):
        return utils.ops.description(
            'Example modal operator that moves the active object',
            'Use bl_description if your tooltip is static',
        )


    @staticmethod
    def status(header, context):
        layout = header.layout
        layout.label(text='Move Object', icon='MOUSE_MOVE')
        layout.label(text='Cycle Axes', icon='EVENT_X')


    @property
    def header(self):
        return utils.ops.header(
            f'Axis: {self.axis}',
            f'Offset: {self.offset:.3}',
        )


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.object


    def invoke(self, context, event):
        self.location = context.object.location.copy()

        utils.ops.write_status_and_header(self)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    def modal(self, context, event):
        if event.type == 'MIDDLEMOUSE':
            return {'PASS_THROUGH'}

        elif event.type in {'LEFTMOUSE', 'SPACE'}:
            return self.finish(context)

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return self.cancel(context)

        elif event.type == 'MOUSEMOVE':
            utils.ops.cursor_warp(event)

            delta = event.mouse_x - event.mouse_prev_x
            delta *= 0.001 if event.shift else 0.01
            self.offset += delta

            self.restore(context)
            self.execute(context)

        elif event.type == 'X' and event.value == 'PRESS':
            index = 'XYZ'.index(self.axis)
            self.axis = 'YZX'[index]

            self.restore(context)
            self.execute(context)

        utils.ops.write_status_and_header(self)
        return {'RUNNING_MODAL'}


    def restore(self, context):
        context.object.location = self.location


    def execute(self, context):
        index = 'XYZ'.index(self.axis)
        context.object.location[index] += self.offset
        return {'FINISHED'}


    def finish(self, context):
        utils.ops.clear_status_and_header(self)
        self.report({'INFO'}, 'Finished')
        return {'FINISHED'}


    def cancel(self, context):
        self.restore(context)
        utils.ops.clear_status_and_header(self)
        self.report({'INFO'}, 'Cancelled')
        return {'CANCELLED'}
