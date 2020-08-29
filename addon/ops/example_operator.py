import bpy, bmesh
import bgl, blf
import gpu, gpu_extras
from .. import utils


# This operator is meant to show some options; you don't have to use all of them.
# For example I wouldn't put actual values in the status bar if they're also in the header.
# And I wouldn't bother with status and header at all if I was using a 2D draw handler.
# I rarely use 3D draw handlers because they're usually not worth the effort.
# I would use bl_description instead of the classmethod if the tooltip was static.
# And I wouldn't use the safety decorator if there was nothing to clean up.


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


    checkbox: bpy.props.BoolProperty(
        name='Checkbox',
        description='True or False',
        default=True,
    )


    @classmethod
    def description(cls, context, properties):
        return utils.ui.description(
            'Example modal operator that moves the active object',
            f'Axis: {properties.axis}',
        )


    def set_status(self, context):
        def status(header, context):
            layout = header.layout
            layout.label(text=f'Offset: {self.offset:.2f}', icon='MOUSE_MOVE')
            layout.label(text=f'Axis: {self.axis}', icon='EVENT_X')
            layout.label(text='Error', icon='EVENT_Z')
            utils.ui.statistics(header, context)

        context.workspace.status_text_set(status)


    def set_header(self, context):
        header = utils.ui.header(
            f'Axis: {self.axis}',
            f'Offset: {self.offset:.2f}',
        )

        context.area.header_text_set(header)


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, 'axis')
        layout.prop(self, 'offset')
        layout.prop(self, 'checkbox')


    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.object


    @utils.safety.decorator
    def invoke(self, context, event):
        self.location = context.object.location.copy()
        self.buffer = 0
        self.offset = 0

        color = context.preferences.themes[0].view_3d.object_active
        self.color = (color.r, color.g, color.b, 1.0)
        self.points = utils.draw_3d.wireframe(context.object, True)

        self.set_status(context)
        self.hud_info = utils.ops.hide_hud()
        self.draw_handler_2d = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_2d, (context, ), 'WINDOW', 'POST_PIXEL')
        self.draw_handler_3d = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_3d, (context, ), 'WINDOW', 'POST_VIEW')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    @utils.safety.decorator
    def modal(self, context, event):
        if event.type == 'MIDDLEMOUSE':
            return {'PASS_THROUGH'}

        elif event.alt and not event.ascii:
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
            self.buffer += delta

            digits = 2 if not event.ctrl else 1 if event.shift else 0
            self.offset = round(self.buffer, digits)

            self.restore(context)
            self.execute(context)

        elif event.type == 'X' and event.value == 'PRESS':
            index = 'XYZ'.index(self.axis)
            self.axis = 'YZX'[index]

            self.restore(context)
            self.execute(context)

        elif event.type == 'Z' and event.value == 'PRESS':
            raise Exception('Example Exception')

        self.set_header(context)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}


    def execute(self, context):
        index = 'XYZ'.index(self.axis)
        context.object.location[index] += self.offset
        return {'FINISHED'}


    def finish(self, context):
        self.cleanup(context)
        return {'FINISHED'}


    def cancel(self, context):
        self.cleanup(context)
        self.restore(context)
        return {'CANCELLED'}


    def restore(self, context):
        context.object.location = self.location


    def cleanup(self, context):
        context.workspace.status_text_set(None)
        context.area.header_text_set(None)

        if getattr(self, 'draw_handler_2d', None):
            self.draw_handler_2d = bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler_2d, 'WINDOW')

        if getattr(self, 'draw_handler_3d', None):
            self.draw_handler_3d = bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler_3d, 'WINDOW')

        utils.ops.show_hud(self.hud_info)
        context.area.tag_redraw()


    def draw_callback_2d(self, context):
        scale = context.preferences.view.ui_scale

        offset = round(100 * scale)
        size = round(14 * scale)

        font = 0
        shadow = True

        text = [
            ('Move Mouse', 'Adjust Offset'),
            ('X', 'Change Axis'),
            ('Z', 'Cause Error'),
        ]

        x, y = offset, offset
        utils.draw_2d.draw_text(text, font, size, x, y, 'LEFT', 'BOTTOM', shadow)

        text = [
            ('Offset', f'{self.offset:.2f}'),
            ('Axis', f'{self.axis}'),
            ('Checkbox', f'{self.checkbox}'),
        ]

        x, y = context.area.width - offset, offset
        utils.draw_2d.draw_text(text, font, size, x, y, 'RIGHT', 'BOTTOM', shadow)


    def draw_callback_3d(self, context):
        scale = context.preferences.view.ui_scale

        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glLineWidth(2 * scale)

        shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        shader.bind()
        shader.uniform_float('color', self.color)

        batch = gpu_extras.batch.batch_for_shader(shader, 'LINES', {'pos': self.points})
        batch.draw(shader)

        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
        bgl.glDisable(bgl.GL_BLEND)
