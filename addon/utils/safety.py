import traceback
import functools


def respond(self, context):
    self.report({'ERROR'}, traceback.format_exc())

    if hasattr(self, 'cancel'):
        try:
            self.cancel(context)
        except:
            self.report({'ERROR'}, traceback.format_exc())

    return {'CANCELLED'}


def execute(method):
    @functools.wraps(method)
    def wrapper(self, context):
        try:
            return method(self, context)
        except:
            return respond(self, context)

    return wrapper


def invoke(method):
    @functools.wraps(method)
    def wrapper(self, context, event):
        try:
            return method(self, context, event)
        except:
            return respond(self, context)

    return wrapper


def modal(method):
    @functools.wraps(method)
    def wrapper(self, context, event):
        try:
            return method(self, context, event)
        except:
            return respond(self, context)

    return wrapper
