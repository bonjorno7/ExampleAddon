import bpy, bgl, blf, gpu, gpu_extras
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
            f'Axis: {properties.axis}',
        )


    def set_status(self, context):
        def status(header, context):
            layout = header.layout
            layout.label(text=f'Offset: {self.offset:.3}', icon='MOUSE_MOVE')
            layout.label(text=f'Axis: {self.axis}', icon='EVENT_X')
            utils.ops.statistics(header, context)

        context.workspace.status_text_set(status)

    @property
    def header(self):
        return utils.ops.header(
            f'Axis: {self.axis}',
            f'Offset: {self.offset:.3}',
        )


    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.object


    @utils.safety.invoke
    def invoke(self, context, event):
        self.location = context.object.location.copy()
        self.offset = 0

        self.draw_handler_2d = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_2d, (context, ), 'WINDOW', 'POST_PIXEL')
        self.draw_handler_3d = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_3d, (context, ), 'WINDOW', 'POST_VIEW')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    @utils.safety.modal
    def modal(self, context, event):
        if event.type == 'MIDDLEMOUSE':
            return {'PASS_THROUGH'}

        elif event.type in {'LEFTMOUSE', 'SPACE'}:
            self.report({'INFO'}, 'Finished')
            return self.finish(context)

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.report({'INFO'}, 'Cancelled')
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

        elif event.type == 'Z' and event.value == 'PRESS':
            raise Exception('Example Exception')

        utils.ops.write_status_and_header(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}


    @utils.safety.execute
    def execute(self, context):
        index = 'XYZ'.index(self.axis)
        context.object.location[index] += self.offset
        return {'FINISHED'}


    def finish(self, context):
        self.cleanup(context)
        return {'FINISHED'}


    def cancel(self, context):
        self.restore(context)
        self.cleanup(context)
        return {'CANCELLED'}


    def restore(self, context):
        context.object.location = self.location


    def cleanup(self, context):
        if getattr(self, 'draw_handler_2d', None):
            self.draw_handler_2d = bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler_2d, 'WINDOW')

        if getattr(self, 'draw_handler_3d', None):
            self.draw_handler_3d = bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler_3d, 'WINDOW')

        utils.ops.clear_status_and_header()


    def draw_callback_2d(self, context):
        font_id = 0
        blf.position(font_id, 15, 30, 0)
        blf.size(font_id, 20, 72)
        blf.draw(font_id, context.object.name)


    def draw_callback_3d(self, context):
        font_id = 0
        blf.position(font_id, 2, 2, 0)
        blf.size(font_id, 20, 72)
        blf.draw(font_id, context.object.name)
