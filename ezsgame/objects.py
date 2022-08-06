from typing import List, Tuple
import pygame as pg
import random
from colour import Color
from .extra.components import ComponentGroup
from .global_data import get_id, get_screen, get_drawn_objects
from .styles_resolver import resolve_color, resolve_margin, resolve_size, resolve_pos
from .funcs import div

# Gradient and colors ------------------------------------------------------------
def random_color(n=1):
    """
    Return a random color if n = 1 -> (135, 6, 233)
    If n is bigger returns a list with random colors -> [(234, 55, 233), ...]
    """
    return [random_color() for i in range(n)] if n > 1 else (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def adapt_rgb(rgb): return tuple(map(lambda i: i*255, rgb))
def pure_rgb(color): return tuple(map(lambda i: i/255, color))

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

        self.screen = get_screen()

        size = resolve_size(size) if size else self.screen.size
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
            pg.draw.rect(self.screen.surface, obj[2], pg.Rect(obj[0], obj[1]))

    def __str__(self):
        return f"<Gradient {self.colors}>"

    def __repr__(self):
        return f"Gradient(*{self.colors})"

# Utility classes ---------------------------------------------------------------
class Vector2:
    r"""
    #### 2 Values Vector, parent of `Pos` and `Size`
    """

    def __init__(self, a=0, b=0):
        self.__call__(a, b)

    def __add__(a, b):
        x, y = b
        return Vector2(a._a + x, a._b + y)

    def __sub__(a, b):
        x, y = b
        return Vector2(a._a - x, a._b - y)

    def __mul__(a, b):
        x, y = b
        return Vector2(a._a * x, a._b * y)

    def __call__(self, a=0, b=0):
        if isinstance(a, list) or isinstance(a, tuple) or isinstance(a, Vector2):
            self._a = a[0]
            self._b = a[1]

        else:
            self._a = a
            self._b = b

    def __str__(self):
        return f"<Vector2 : {self._a}, {self._b}>"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        self.__current_index = 0
        return iter([self._a, self._b])

    def __next__(self):
        if self.__current_index == 0:
            self.__current_index += 1
            return self._a
        elif self.__current_index == 1:
            self.__current_index += 1
            return self._b
        else:
            raise StopIteration

    def __getitem__(self, index):
        if index == 0:
            return self._a
        elif index == 1:
            return self._b
        else:
            raise IndexError

    def __setitem__(self, index, value):
        if index == 0:
            self._a = value
        elif index == 1:
            self._b = value
        else:
            raise IndexError

    def __len__(self):
        return 2

    def copy(self):
        return Vector2(self._a, self._b)

    def ref(self):
        return self

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self._a == other._a and self._b == other._b
        else:
            return False

    def __ne__(self, other):
        return not self == other

class Size (Vector2):
    r"""
    #### Size
    #### Parameters
    - `width`: width  `int` or `[width, height]`
    - `height`: height `int` or `[width, height]`
    """

    def __init__(self, width=0, height=0):
        super().__init__(width, height)

    @property
    def width(self):
        return self._a

    @width.setter
    def width(self, value):
        self._a = value

    @property
    def height(self):
        return self._b

    @height.setter
    def height(self, value):
        self._b = value

class Pos (Vector2):
    r"""
    #### Position
    #### Parameters
    - `x`: x position `number` or `[x, y]`
    - `y`: y position `number`
    """

    def __init__(self, x=0, y=0):
        super().__init__(x, y)

    @property
    def x(self):
        return self._a

    @x.setter
    def x(self, value):
        self._a = value

    @property
    def y(self):
        return self._b

    @y.setter
    def y(self, value):
        self._b = value

# Objects -----------------------------------------------------------------------
class Object:
    r"""
    Object is a base class for all objects in the game.
    Cannot be instantiated.
    """

    def __init__(self, pos: Pos, size: Size, **styles):
        self.id = get_id()
        self.screen = get_screen()

        self.color = styles.get("color", "white")
        # top, right, bottom, left
        self.margin = styles.get("margin", [0, 0, 0, 0])
        self.stroke = styles.get("stroke", 0)
        self.z_index = styles.get("z_index", 1)

        # if only 1 measure is given, use it for both measures
        if len(pos) == 1:
            pos = [pos[0], pos[0]]
        self.pos = Pos(*pos)

        # if only 1 axis is given, use it for both axis
        if len(size) == 1:
            size = [size[0], size[0]]
        self.size = Size(*size)

        if "styles" in styles:
            for k, v in styles["styles"].items():
                setattr(self, k, v)

        self.behavior = styles.get("behavior",
                                   # defualt behavior
                                   {"pos": "dynamic"}
                                   )

        self.__on_draw = {}

        self.components = ComponentGroup(self,  *styles.get("components", []))

        self.resolve_styles()
        # Calls _draw() before draw()

        def _draw_before(draw_func):
            def wrapper():
                draw_func()
                self._draw()

            return wrapper
        try:
            self.draw = _draw_before(self.draw)
        except:
            pass

    def update_styles(self, styles=None, **kwargs):
        r"""
        #### Updates the object's styles

        #### Parameters
        - `styles`: `dict` of styles to update (default: None)
        - `**kwargs`: keyword arguments of styles to update
        """

        if styles:
            for k, v in styles.items():
                setattr(self, k, v)

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.resolve_styles()

    def extends(self, *classes):
        r"""
        #### Extends the properties and methods of the given classes to the current object.
        Note : this can only be done with classes with `extend()` method.
        #### Parameters
        - `classes`: classes to extend (*args)
        """
        for cls in classes:
            if hasattr(cls, "extend"):
                self = cls.extend(self)
            else:
                raise TypeError("Cannot extend class {}".format(cls))
        return self

    def on_draw(self, func, name: str = "Default", pass_object=False):
        r"""
        #### Adds a function to be called after the object is drawn
        #### Parameters
        - `func`: function to be called
        - `name`: name of the function (default: `function name`)
        - `pass_object`: if True, the function will be called with the object as the first parameter

        """
        name = name if name else func.__name__
        self.__on_draw[name] = lambda: func(self) if pass_object else func

    def remove_on_draw(self, name: str):
        r"""
        #### Removes a function from being called after the object is drawn
        #### Parameters
        - `name`: name of the function
        """
        if name in self.__on_draw:
            del self.__on_draw[name]

    def _get_collision_box(self):
        self.resolve_styles()
        return [self.pos, [self.pos[0] + self.size[0], self.pos[1]],
                [self.pos[0], self.pos[1] + self.size[1]],
                [self.pos[0] + self.size[0], self.pos[1] + self.size[1]]]  # esquina superior izq, superior derecha, infeior izq, inferior derecha

    def resolve_styles(self):
        r"""
        #### Resolves the styles of the object (Ex. size, margin, stroke)
        """

        if not isinstance(self.size, Size):
            self.size = Size(*self.size)
        if not isinstance(self.pos, Pos):
            self.pos = Pos(*self.pos)

        # Resolve properties
        self.color = resolve_color(self.color)

        self.margin = resolve_margin(self.margin)

        self.size = resolve_size(self.size)

        self.pos = resolve_pos(self.pos, self.size, self.margin)

    def get_pos(self, ref=False):
        """
        #### Returns postion of the object after revolsing styles

        #### Parameters
        - `ref`: if True, returns a "reference" to the position `bool`(default: False)
        """
        self.resolve_styles()
        self.pos = Pos(*self.pos)
        return self.pos.ref() if ref else Pos(self.pos.copy())

    def get_size(self, ref=False):
        """
        #### Returns size of the object after revolsing styles

        #### Parameters
        - `ref`: if True, returns a "reference" to the size `bool`(default: False)
        """
        self.size = Size(*self.size)
        return self.size.ref() if ref else Size(self.size.copy())

    def __str__(self):
        return f"<Object: {self.__class__.__name__}, ID: {self.id}>"

    def _draw(self):
        r'''
        manages Object draw method and calls `on_draw` functions
        '''
        for func in self.__on_draw.values():
            func()

        get_drawn_objects().append(self.id)


class Rect(Object):
    r'''
    #### Rect
    #### Parameters
    - `pos`: position of the rect `[x, y]`
    - `size`: size of the rect `[width, height]`

    #### Optional Arguments (Keyword Arguments)
    - `color`: color of the rect `"white" or (R, G, B)`
    - `stroke`: stroke of the rect `int`
    - `margin`: margin of the rect `[top, right, bottom, left]`
    - `border_radius`: border radius of the rect `[top-left, top-right, bottom-right, bottom-left]`
    - `components` : components to add in the rect `[Component, ..]`
    '''

    def __init__(self, pos: Pos, size: Size, **styles):
        super().__init__(pos, size, **styles)

        # top-left, top-right, bottom-right, bottom-left
        self.border_radius = styles.get("border_radius", [0, 0, 0, 0])
        if len(self.border_radius) == 1:
            self.border_radius = [self.border_radius[0]] * 4
        elif len(self.border_radius) == 2:
            self.border_radius = [self.border_radius[0]
                                  * 2] * 2 + [self.border_radius[1] * 2] * 2

    def draw(self):
        pg.draw.rect(self.screen.surface, self.color, [
                     *self.get_pos(), *self.size], int(self.stroke), *self.border_radius)


class Text(Object):
    r'''
    #### Text
    #### Parameters
    - `text`: text to be displayed
    - `pos`: position of the text `[x, y]`
    - `font_size`: font size of the text

    #### Optional Arguments (Keyword Arguments)
    - `font` : font of the text `"Arial or "path/to/font.ttf"`
    - `color`: color of the text `"white" or (R, G, B)`
    - `margin`: margin of the text `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    '''

    def __init__(self, text, pos, font_size, **styles):
        self.font = styles.get("font", "Arial")
        self.font_size = font_size
        self.color = styles.get("color", "white")
        self.text = text
        self.text_obj = self.load_font(text, self.font, font_size, self.color)

        if "pos" in styles:
            del styles["pos"]
        if "size" in styles:
            del styles["size"]

        super().__init__(pos=pos, size=[
            self.text_obj.get_width(), self.text_obj.get_height()], **styles)

    def load_font(self, text, name, size, color="white"):
        # load local font
        pg.font.init()
        name = name.lower()
        # if font in system fonts
        if name in pg.font.get_fonts():
            font = pg.font.SysFont(name, size)

        # if font is a path
        elif name.endswith(".ttf"):
            font = pg.font.Font(name, size)

        else:
            raise Exception("Font not found", name)

        return font.render(text, True, color)

    def update(self, **atributes):
        if "text" in atributes:
            self.text = atributes["text"]
            self.text_obj = self.load_font(
                self.text, self.font, self.font_size, self.color)
            self.size = [self.text_obj.get_width(), self.text_obj.get_height()]

        super().__dict__.update(**atributes)

    def draw(self):
        self.text_obj = self.load_font(
            self.text, self.font, self.font_size, self.color)
        self.screen.surface.blit(self.text_obj, self.get_pos())


class Image(Rect):
    r'''
    #### Image
    #### Parameters
    - `pos`: position of the image `[x, y]`
    - `size` : size of the image `[width, height]`
    - `image` : path to image file `str`

    #### Optional Arguments (Keyword Arguments)
    - `scale` : scale the image to the size `bool`
    - `margin`: margin of the image `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    '''

    def __init__(self, pos, size, image, scale=True, **styles):
        super().__init__(pos, size, **styles)
        try:
            self.image = pg.image.load(image)
        except:
            raise ValueError("Image not found in current directory: ", image)

        if scale:
            self.image = pg.transform.scale(self.image, self.size)

    def draw(self):
        self.screen.surface.blit(self.image, self.get_pos())

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.image, angle)
        self.size = [self.image.get_width(), self.image.get_height()]

    def flip(self, x_axis: bool = True, y_axis: bool = False):
        self.image = pg.transform.flip(self.image, x_axis, y_axis)
        self.size = [self.image.get_width(), self.image.get_height()]

    def scale(self, new_size: Size):
        self.image = pg.transform.scale(self.image, new_size)
        self.size = [self.image.get_width(), self.image.get_height()]


class Circle(Object):
    r'''
    #### Circle
    #### Parameters
    - `pos`: position of the circle `[x, y]`
    - `radius`: radius of the circle `number`

    #### Optional Arguments (Keyword Arguments)
    - `color`: color of the circle `"white" or (R, G, B)`
    - `stroke`: stroke of the circle `int`
    - `margin`: margin of the circle `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    '''

    def __init__(self, pos, radius, **styles):
        if isinstance(radius, str):
            if radius.endswith("%"):
                radius = int(float(radius[:-1]) / 100 * get_screen().size[0])

        super().__init__(pos=pos, size=[radius*2, radius*2],  **styles)
        self.radius = radius

    def draw(self):
        pos = self.get_pos()
        pg.draw.circle(self.screen.surface, self.color,
                       pos, self.radius, int(self.stroke))

    def _get_collision_box(self):
        pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1] / 2]
        return [pos, [pos[0] + self.size[0], pos[1]],
                [pos[0], pos[1] + self.size[1]], [pos[0] +
                                                  self.size[0], pos[1] + self.size[1]]
                ]  # esquina superior izq, superior derecha, infeior izq, inferior derecha


class Ellipse(Object):
    r'''
        #### Ellipse
        #### Parameters
        - `pos`: position of the Ellipse `[x, y]`
        - `size`: size of the Ellipse `[width, height]`

        #### Optional Arguments (Keyword Arguments)
        - `color`: color of the Ellipse `"white" or (R, G, B)`
        - `stroke`: stroke of the Ellipse `int`
        - `margin`: margin of the Ellipse `[top, right, bottom, left]`
        - `components` : components to add in the object `[Component, ..]`
        '''

    def __init__(self, pos: Pos, size: Size, **styles):
        super().__init__(pos=pos, size=size, **styles)

    def draw(self):
        pg.draw.ellipse(self.screen.surface, self.color, [
                    *self.get_pos(), *self.size], int(self.stroke))


class Group:
    r"""
    #### Group
    
	#### Parameters
	- [*args] objects : objects to add in the group
    """
    
    def __init__(self, *args):
        self.screen = get_screen()
        self.objects = [*args]

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        self.__current_index = 0
        return iter(self.objects)

    def __next__(self):
        if self.__current_index >= len(self.objects):
            raise StopIteration
        else:
            self.__current_index += 1
            return self.objects[self.__current_index - 1]

    def __getitem__(self, other):
        if isinstance(other, int):
            return self.objects[other]

        elif isinstance(other, slice):
            return self.__getslice__(other)

        elif isinstance(other, Object):
            return self.objects[self.objects.index(other)]

        else:
            raise TypeError("Index must be an integer, slice or Object")

    def __contains__(self, thing):
        return thing in self.objects

    def __getslice__(self, other):
        return self.objects[other.start:other.stop:other.step]

    def __delitem__(self, other):
        if isinstance(other, int):
            del self.objects[other]

        elif isinstance(other, slice):
            self.__delslice__(other)

        else:
            raise KeyError("Index must be an integer or slice")

    def __delslice__(self, other):
        del self.objects[other.start:other.stop:other.step]

    def __setitem__(self, other, item):
        self.objects[other] = item

    def add(self, *objects):
        self.objects.append(*objects)

    def remove(self, obj):
        self.objects.remove(obj)

    def draw(self):
        for obj in self.objects:
            obj.draw()

    def __del__(self):
        for obj in self.objects:
            del obj

        del self

    def map(self, func):
        for obj in self.objects:
            func(obj)

    def __str__(self):
        t = ", ".join([str(i) for i in self.objects])
        return f"<Group : {t} >"

    def __repr__(self):
        return self.__str__()

    def filter(self, func):
        self.objects = [obj for obj in self.objects if func(obj)]
        return self.objects

    def copy(self):
        return Group(*self.objects)

    def __add__(a, b):
        return Group(*a, *b)


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
    
    def __init__(self, start: Pos, end: Pos, width: int = 5, **styles):
        self.start = start
        self.end = end
        self.width = width
        self.color = styles.get("color", "white")
        self.screen = get_screen()

    def draw(self):
        pg.draw.line(self.screen.surface, self.color,
                     self.start, self.end, self.width)

    def _get_collision_box(self):
        # collision is checked at line end
        return [self.end, self.end + [self.width, 0], self.end + [0, self.width], self.end + [self.width, self.width]]

    def get_size(self):
        return Size(self.width, self.width)

    def get_pos(self):
        return self.end