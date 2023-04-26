"""

"""

from ezsgame.types import Pos, Size

class World:
    """
    #### Defines the "world"
    The `pos` and `size` defined the "view" of the world, objects outside of the view won't be drawn.
    """

    pos = Pos(0, 0)
    size = Size(0, 0) # will be set on window post init

    @classmethod
    def is_inside(cls, obj) -> bool:
        """
        #### Returns `True` if `obj` is inside the world
        """
        return cls.pos[0] <= obj.pos[0] <= cls.pos[0] + cls.size[0] and cls.pos[1] <= obj.pos[1] <= cls.pos[1] + cls.size[1]
        