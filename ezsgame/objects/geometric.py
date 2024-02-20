from typing import Any, Dict, Iterable

from ..world import get_window
from ..objects.object import Object
import pygame as pg
from ..styles.colors import resolve_color, Color
from ..styles.style import Styles
from ..styles.units import Measure
from ..types import Pos, Size
from ..components import Component

class Rect(Object):
    r"""
    #### Rect
    #### Parameters
    - `pos`: position of the rect `[x, y]`
    - `size`: size of the rect `[width, height]`

    #### Styles
    - `color`: color of the rect `"white" or (R, G, B)`
    - `stroke`: stroke of the rect `int`
    - `margins`: margins of the rect `[top, right, bottom, left]`
    - `border_radius`: border radius of the rect `[top-left, top-right, bottom-right, bottom-left]`
    - `components` : components to add in the rect `[Component, ..]`
    """

    def draw(self):
        pg.draw.rect(
            self.window.surface,
            self.styles.color,
            (*self.pos, *self.size),
            self.styles.stroke,
            *self.styles.border_radius
        )


class Circle(Object):
    r"""
    #### Circle
    #### Parameters
    - `pos`: position of the circle `[x, y]`
    - `radius`: radius of the circle `number`

    #### Styles
    - `color`: color of the circle `"white" or (R, G, B)`
    - `stroke`: stroke of the circle `int`
    - `margins`: margins of the circle `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    """

    def __init__(
        self,
        pos: Pos | Iterable[Measure],
        radius: int,
        styles: Styles = Styles(),
        parent: "Object" = None,
        components: Iterable[Component] = [],
        **_styles: Dict[str, Any]
    ):
        if not parent:
            parent = get_window()

        self.radius = radius

        super().__init__(
            pos=pos,
            size=Size(radius * 2, radius * 2),
            styles=styles,
            parent=parent,
            components=components,
            **_styles
        )

    def draw(self):
        pg.draw.circle(
            self.window.surface,
            self.styles.color,
            self.pos,
            self.radius,
            self.styles.stroke,
        )

    def _get_collision_box(self):
        center_x, center_y = self.pos
        radius = self.size[0] / 2
        return (
            (center_x - radius, center_y - radius),  # top-left
            (center_x + radius, center_y - radius),  # top-right
            (center_x - radius, center_y + radius),  # bottom-left
            (center_x + radius, center_y + radius),  # bottom-right
        )


class Ellipse(Object):
    r"""
    #### Ellipse
    #### Parameters
    - `pos`: position of the Ellipse `[x, y]`
    - `size`: size of the Ellipse `[width, height]`
    - `components` : components to add in the object `[Component, ..]`

    #### Styles
    - `color`: color of the Ellipse `"white" or (R, G, B)`
    - `stroke`: stroke of the Ellipse `int`
    - `margins`: margins of the Ellipse `[top, right, bottom, left]`
    """

    def draw(self):
        pg.draw.ellipse(
            self.window.surface,
            self.styles.color,
            (*self.pos, *self.size),
            self.styles.stroke,
        )


class Line:
    r"""
    #### Line

    #### Parameters
    - `start`: start of the line `[x, y]`
    - `end`: end of the line `[x, y]`
    - width : width of the line `int`
    - `color`: color of the line `"white" or (R, G, B)`
    - `stroke`: stroke of the line `int`

    """
    __slots__ = ("start", "end", "width", "color", "window")

    def __init__(self, start: Pos, end: Pos, width: int = 5, color: Color = "white"):
        self.start = start
        self.end = end
        self.width = width
        self.color = resolve_color(color)
        self.window = get_window()

    def draw(self):
        pg.draw.line(self.window.surface, self.color, self.start, self.end, self.width)

    def _get_collision_box(self):
        # collision is checked at line end
        return (
            self.end,
            self.end + (self.width, 0),
            self.end + (0, self.width),
            self.end + (self.width, self.width),
        )
