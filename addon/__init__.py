from . import props
from . import icons
from . import ops
from . import ui


modules = (
    props,
    icons,
    ops,
    ui,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
