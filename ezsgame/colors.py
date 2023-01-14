from colour import Color
import random
from .styles_resolver import *
import pygame as pg
from typing import List, Tuple
from .global_data import get_window
from .funcs import div

def random_color(n=1):
    """
    Return a random color if n = 1 -> (135, 6, 233)
    If n is bigger returns a list with random colors -> [(234, 55, 233), ...]
    """
    return [random_color() for i in range(n)] if n > 1 else (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def _check_color(color):
    if isinstance(color, str):
        return Color(color)

    elif not (isinstance(color, tuple) or isinstance(color, list)):
        raise ValueError(
            "Color must be a tuple or a list, or color name: ", color)

    else:
        return Color(rgb=pure_rgb(color))

def gen_gradient(size, div, start, end, direction="v", pos_prefix: float = 0) -> List[Tuple[List, List, Tuple]]:
    r'''
    Generates a gradient between two colors
    - start: start color
    - end: end color
    - complexity: how many times to draw the gradient
    '''
    if (direction := direction[0].lower()) not in ("v", "h"):
        raise ValueError("Direction must be either 'vertical' or 'horizontal'")

    start = _check_color(start)
    end = _check_color(end)

    size = resolve_size(size)

    colors = tuple(start.range_to(end, len(div)))
    objs = []

    for i in range(len(div)):
        if direction == "h":
            pos = [div[i][0] + pos_prefix, 0]
            obj_size = [div[i][1], size[1]]
        else:
            pos = [0, div[i][0] + pos_prefix]
            obj_size = [size[0], div[i][1]]

        objs.append((pos, obj_size, adapt_rgb(colors[i].rgb)))

        # if current x + width is bigger than screen width, end the loop
        if direction == "h" and div[i][0] + div[i][1] > size[0]:
            break

        # if current y + height is bigger than screen height, end the loop
        if direction == "v" and div[i][0] + div[i][1] > size[1]:
            break

    return objs

class Gradient:
    r'''
    #### Gradient
    #### Parameters
    - `start`: start color `white` or `(R, G, B)`
    - `end`: end color `black` or `(R, G, B)`

    #### Optional Arguments (Keyword Arguments)
    - `direction`: direction of the gradient `"horizontal"` or `"vertical"`
    - `complexity`: space between each color stripe (higher -> load time) `int`
    - `size`: size of the gradient `[width, height]` (default: screen size)
    '''

    def __init__(self, *colors, direction="horizontal", complexity=120, size=None):
        if complexity < 3:
            complexity = 3

        if complexity > 1000:
            complexity = 1000

        if not colors or len(colors) < 2:
            raise ValueError(
                "You must specify at least two colors to create a gradient")

        self.colors = colors

        self.window = get_window()

        size = resolve_size(size) if size else self.window.size
        self.gradient_objs = []
        last_color = None

        for index, division in enumerate(div("x", len(colors), size), start=1):
            if index > len(colors) - 1:
                break

            last_color = colors[index-1]

            self.gradient_objs.extend(gen_gradient(size,
                                                   div("x", complexity, [
                                                       division[1], size[1]]),
                                                   last_color,
                                                   colors[index],
                                                   direction,
                                                   division[0]
            )
            )

    def draw(self):
        for obj in self.gradient_objs:
            pg.draw.rect(self.window.surface, obj[2], pg.Rect(obj[0], obj[1]))

    def __str__(self):
        return f"<Gradient {self.colors}>"

    def __repr__(self):
        return f"Gradient(*{self.colors})"
