import traceback
import functools


def respond(self, context, event=None):
    '''
    Try to call self.cancel and self.report the traceback.

    Args:
        self: Operator instance.
        context: Current blender context.
        event: Unused.

    Returns:
        result: {'CANCELLED'}.
    '''

    try:
        self.cancel(context)
    except:
        self.report({'ERROR'}, traceback.format_exc())
    else:
        self.report({'ERROR'}, traceback.format_exc())

    return {'CANCELLED'}


def decorator(method):
    '''
    Wrap this method in a try block.

    Args:
        method: Operator method invoke, modal, or execute.

    Returns:
        wrapper: Wrapped operator method.
    '''

    wraps = functools.wraps(method)

    def wrapper(*args):
        try:
            return method(*args)
        except:
            return respond(*args)

    if method.__name__ in {'invoke', 'modal'}:
        return wraps(lambda self, context, event: wrapper(self, context, event))

    elif method.__name__ == 'execute':
        return wraps(lambda self, context: wrapper(self, context))

    raise Exception('This decorator is only for invoke, modal, and execute')
