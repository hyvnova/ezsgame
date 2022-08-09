from typing import List, Tuple
import pygame as pg, random, os
from colour import Color
from .extra.components import ComponentGroup
from .global_data import get_id, get_screen, get_drawn_objects
from .styles_resolver import resolve_color, resolve_margins, resolve_measure, resolve_size, resolve_position
from .funcs import div
from .fonts import Fonts, FontFamily


# Initialize vars ---------------------------------------------------------
pg.font.init()


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
    __slots__ = "_a", "_b"
    
    def __init__(self, a=0, b=0):
        self.__call__(a, b)

    def __add__(a, b):
        x, y = b
        return Vector2(a._a + x, a._b + y)

    def __sub__(a, b):
        x, y = b
        return Vector2(a._a - x, a._b - y)

    def __mul__(a, b):
        if isinstance(b, Vector2):
            return a._a * b._a + a._b * b._b    

        elif isinstance(b, (int, float)):
            return Vector2(a._a * b, a._b * b)
    
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
    should not be instantiated.
    """

    __slots__ = "pos", "size", "screen", "id", "color", "margins", "stroke", "components", "behavior", "__on_draw", "absolute"

    def __init__(self, **props):
        """
        #### Parameters (props)
        - `parent`: parent object (default: Screen)
           
        - `pos`: position of element (default: (0, 0) )
        - `absolute`: if True, element position is absolute, otherwise element position is relative to parent position (default: False)
        - `margins` : margins of element (default: (0, 0, 0, 0) )
        
        - `size`: size of element
        
        - `color`: color of element (default: white )
         
        """
        self.id = get_id()
        self.screen = get_screen()
        
        self.parent = props.get('parent', get_screen())
        
        self.margins: List[float] = resolve_margins(props.get('margins', [0, 0, 0, 0]), self.parent.size)
        
        # if not size, size = 10% of parent size
        self.size: Size = props.get('size', self.parent.size.copy() * 0.1)
        self.pos: Pos = props.get('pos', Pos(0, 0))
        
        self.size = resolve_size(self, self.parent)
        self.pos = resolve_position(self, self.parent, props.get('absolute', False))
        
        self.absolute = props.get('absolute', False) # if True, element position is absolute, otherwise element position is relative to parent position

        self.color: Color = resolve_color(props.get('color', 'white'))
       
        if (styles := props.get("styles")) :
            for name, value in styles.items():
                setattr(self, name, value)


        self.behavior = props.get("behavior",
                                   # defualt behavior
                                   {"pos": "dynamic"}
                                   )

        self.__on_draw = {}
        self.__last_props = {}

        self.components = ComponentGroup(self,  *props.get("components", []))

        self.resolve_styles()
        # Calls __after_draw() before draw() to call on draw methods

        def _draw_manager(draw_func):
            def wrapper():
                
                props = {k:v for k,v in self.__dict__.items() if not k.startswith("_")}
                
                if self.__last_props != props:
                    get_drawn_objects().append(self.id)
                    draw_func()                    
                    self.__last_props = props

                self.__after_draw()
                
            return wrapper
        
        try:
            self.draw = _draw_manager(self.draw)
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
        #### Resolves the styles of the object (Ex. size, margins, stroke)
        """

        if not isinstance(self.size, Size):
            self.size = Size(*self.size)
        if not isinstance(self.pos, Pos):
            self.pos = Pos(*self.pos)

        # Resolve properties
        self.color = resolve_color(self.color)

        self.margins = resolve_margins(self.margins, self.parent.size)

        self.size = resolve_size(self, self.parent)

        self.pos = resolve_position(self, self.parent, self.absolute)

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

    def __after_draw(self):
        r'''
        manages Object draw method and calls `on_draw` functions
        '''
        for func in self.__on_draw.values():
            func()


class Rect(Object):
    r'''
    #### Rect
    #### Parameters
    - `pos`: position of the rect `[x, y]`
    - `size`: size of the rect `[width, height]`

    #### Optional Arguments (Keyword Arguments)
    - `color`: color of the rect `"white" or (R, G, B)`
    - `stroke`: stroke of the rect `int`
    - `margins`: margins of the rect `[top, right, bottom, left]`
    - `border_radius`: border radius of the rect `[top-left, top-right, bottom-right, bottom-left]`
    - `components` : components to add in the rect `[Component, ..]`
    '''

    def __init__(self, pos: Pos, size: Size, **props):
        super().__init__(pos=pos, size=size, **props)

        # top-left, top-right, bottom-right, bottom-left
        self.border_radius = props.get("border_radius", [0, 0, 0, 0])
        
        if len(self.border_radius) == 1:
            self.border_radius = [self.border_radius[0]] * 4
            
        elif len(self.border_radius) == 2:
            self.border_radius = [self.border_radius[0]
                                  * 2] * 2 + [self.border_radius[1] * 2] * 2
            
        self.stroke = props.get("stroke", 0)
        self.stroke = resolve_measure(self.stroke, self.parent)    

    def draw(self):
        print("drawing rect")
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
    - `font` : font of the text `"Arial or "path/to/font.ttf"` or `ezsgame font` (default: `OpenSans`)
    - `color`: color of the text `"white" or (R, G, B)`
    - `margins`: margins of the text `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    - `bold` : if True, the text will be bold `bool`    
    - `italic` : if True, the text will be italic `bool`
    '''

    __slots__ = "font", "font_size", "text", "bold", "italic", "text_obj"

    def __init__(self, text, pos, font_size, **props):
        self.font = props.get("font", Fonts.OpenSans)
        self.font_size = font_size
        self.color = props.get("color", "white")
        self.text = text
        self.bold = props.get("bold", False)
        self.italic = props.get("italic", False)
        
        self.text_obj = self.load_font()

        if "pos" in props:
            del props["pos"]
        if "size" in props:
            del props["size"]

        super().__init__(pos=pos, size=[
            self.text_obj.get_width(), self.text_obj.get_height()], **props)

    def load_font(self):
        # load local font
        
        # is font is a ezsgame font
        if isinstance(self.font, FontFamily):
            font = self.font.get_font(self.font_size)
        
        # if font is a path | str
        elif isinstance(self.font, str):
            
            # if font in system fonts
            if font in pg.font.get_fonts():
                font = pg.font.SysFont(font, self.font_size, self.bold, self.italic)

            # if font is a path
            elif font.endswith(".ttf"):
                try:
                    font = pg.font.Font(font, self.font_size)
                except Exception as e:
                    raise ValueError(f"Error loading font: {e}")
                
            else:
                raise ValueError("Invalid font name or path: " + self.font) 
            
        else:
            raise ValueError("Invalid font: " + self.font)
        
        return font.render(self.text, True, self.color)

    def update(self, **atributes):
        if "text" in atributes:
            self.text = atributes["text"]
            self.text_obj = self.load_font()
            
            self.size = [self.text_obj.get_width(), self.text_obj.get_height()]

        super().__dict__.update(**atributes)

    def draw(self):
        self.text_obj = self.load_font()
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
    - `margins`: margins of the image `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    '''

    def __init__(self, pos, size, image, scale=True, **props):
        super().__init__(pos, size, **props)
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
    - `margins`: margins of the circle `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    '''

    def __init__(self, pos : Pos, radius: float, **props):
        if isinstance(radius, str):
            if radius.endswith("%"):
                radius = int(float(radius[:-1]) / 100 * get_screen().size[0])

        super().__init__(pos=pos, size=[radius*2, radius*2],  **props)
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
        - `margins`: margins of the Ellipse `[top, right, bottom, left]`
        - `components` : components to add in the object `[Component, ..]`
        '''

    def __init__(self, pos: Pos, size: Size, **props):
        super().__init__(pos=pos, size=size, **props)

    def draw(self):
        pg.draw.ellipse(self.screen.surface, self.color, [
                    *self.get_pos(), *self.size], int(self.stroke))

class Group(dict):
    r"""
    #### Group
    
	#### Parameters
    - [*args] objects : objects to add in the group `Object, ..`
    - [**kwargs] named_objects : named objects to add in the group `name = Object, ..`

    #### Notes
    - named objects can be accessed by: `group["name"]`
    - no named objects can be accessed by: `group[object.id]`

    """
    
    def __init__(self,*objects, **named_objects):
        objects = {obj.id : obj for obj in objects}
        super().__init__(**objects, **named_objects)
        
        for name, value in self.items():
            self.__setattr__(name, value)
        
    
    def add(self, **objects):
        self.update(**objects)

    def draw(self):
        for obj in self.values():
            obj.draw()

    def map(self, func):
        for obj in self.values():
            func(obj)

    def __str__(self):
        t = ", ".join([str(i) for i in self.objects])
        return f"<Group : {t} >"

    def __repr__(self):
        return self.__str__()

    def filter(self, func) -> 'Group':
        self = {k: v for k, v in self.items() if func(v)}
        return self

    def copy(self) -> 'Group':
        return Group(**self)
    
    # item setters
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__[key] = value
    
    def __setattr__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__[key] = value

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
    
    def __init__(self, start: Pos, end: Pos, width: int = 5, **props):
        self.start = start
        self.end = end
        self.width = width
        self.color = props.get("color", "white")
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