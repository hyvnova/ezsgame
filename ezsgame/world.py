from functools import lru_cache
from typing import Set
from .types import Pos, Size, Signal


class World:
    """
    #### Defines the "world"
    The `pos` and `size` defined the "view" of the world, objects outside of the view won't be drawn.
    """


    # will be set on window post init
    window = object
    pos = Pos(0, 0)
    size = Size(0, 0)  
    
    EventHandler = object
    TimeHandler = object

    objects: Set = set()
    objects_to_add: Set = set() # avoids iteration errors (adding objects during iteration)

    on_update: Signal = Signal()
    
    @classmethod
    def is_inside(cls, obj) -> bool:
        """
        #### Returns `True` if `obj` is inside the world
        """
        return (
            cls.pos[0] <= obj.pos[0] <= cls.pos[0] + cls.size[0]
            and cls.pos[1] <= obj.pos[1] <= cls.pos[1] + cls.size[1]
        )


# Utility for getting the window object easily
@lru_cache()
def get_window():
    """
    #### Returns the window object
    """
    return World.window
