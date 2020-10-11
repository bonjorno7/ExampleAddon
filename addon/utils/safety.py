import traceback
import functools


def decorator(method: function) -> function:
    '''
    Wrap this method in a try block.

    Args:
        method: Operator invoke or modal.

    Returns:
        wrapper: Wrapped operator method.
    '''

    @functools.wraps(method)
    def wrapper(self, context, event):
        try:
            return method(self, context, event)

        except:
            try:
                self.cancel(context)
            except:
                message = traceback.format_exc()
            else:
                message = traceback.format_exc()

            print(message)
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

    return wrapper
