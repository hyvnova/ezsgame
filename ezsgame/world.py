from typing import Set
from .types import Pos, Size, Signal


class World:
    """
    #### Defines the "world"
    The `pos` and `size` defined the "view" of the world, objects outside of the view won't be drawn.
    """

    pos = Pos(0, 0)
    size = Size(0, 0)  # will be set on window post init
    window = object

    objects: Set = set()
    objects_to_add: Set = set()

    on_update: Signal = Signal()

    EventHandler = object
    TimeHandler = object

    @classmethod
    def is_inside(cls, obj) -> bool:
        """
        #### Returns `True` if `obj` is inside the world
        """
        return (
            cls.pos[0] <= obj.pos[0] <= cls.pos[0] + cls.size[0]
            and cls.pos[1] <= obj.pos[1] <= cls.pos[1] + cls.size[1]
        )


def get_window():
    """
    #### Returns the window object
    """
    return World.window
