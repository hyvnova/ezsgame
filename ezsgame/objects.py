from pathlib import Path
from typing import Any, Dict, Iterable
import pygame as pg

from ezsgame.styles.units import Measure

from .styles.style import Styles

from .futures.components import ComponentGroup, Component
from .global_data import get_id, get_window
from .styles.styles_resolver import resolve_measure, resolve_color, Color
from .funcs import center
from .fonts import Fonts, FontFamily

from .types import Pos, Size

# Initialize vars ---------------------------------------------------------
pg.font.init()


# Objects -----------------------------------------------------------------------
class Object:
    r"""
    Object is a base class for all objects in the game.
    should not be instantiated.
    """

    __slots__ = ("pos", "size", "window", "id", "components", "behavior", "__on_draw", "parent")

    def __init__(
        self, 
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        styles: Styles = Styles(),
        parent: "Object" = get_window(),
        components: Iterable[Component] = [],
        **_styles: Dict[str, Any]
    ):
        """
        Base class for most object, handlers object default and required behavior
        """
        self.id = get_id()
        self.parent = parent

        self.pos = pos if isinstance(pos, Pos) else Pos(*pos)
        self.size = size if isinstance(size, Size) else Size(*size)

        # defualt behavior - needs it own type and rework
        self.behavior = {"pos": "dynamic"}

        self.styles = styles or Styles(**_styles)
        
        styles.resolve(self.parent.size)

        self.__on_draw = {}

        self.components = ComponentGroup(self, *components)


        # Calls __after_draw() before draw() to call on draw methods
        def _draw_manager(draw_func):
            def wrapper():
                if self.visible:
                    draw_func() 
                                       
                self.__after_draw()
                
            return wrapper
        try:
            self.draw = _draw_manager(self.draw)
        except:
            pass

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
        x, y = self.pos
        w, h = self.size
        return [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]

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

    #### Styles
    - `color`: color of the rect `"white" or (R, G, B)`
    - `stroke`: stroke of the rect `int`
    - `margins`: margins of the rect `[top, right, bottom, left]`
    - `border_radius`: border radius of the rect `[top-left, top-right, bottom-right, bottom-left]`
    - `components` : components to add in the rect `[Component, ..]`
    '''         

    def draw(self):
        pg.draw.rect(
            self.window.surface, 
            self.styles.color, 
            (*self.pos, *self.size), 
            self.styles.stroke, 
            *self.styles.border_radius
        )

class Text(Object):
    r'''
    #### Text
    #### Parameters
    - `text`: text to be displayed
    - `pos`: position of the text `[x, y]`
    - `font_size`: font size of the text
    - `font` : font of the text `"Arial or "path/to/font.ttf"` or `ezsgame font` (default: `OpenSans`)
    - `bold` : if True, the text will be bold `bool`    
    - `italic` : if True, the text will be italic `bool`

    #### Styles
    - `color`: color of the text `"white" or (R, G, B)`
    - `margins`: margins of the text `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    '''

    __slots__ = "font", "font_size", "text", "bold", "italic", "text_obj", "styles"

    def __init__(
        self, 
        text: str, 
        pos: Pos | Iterable[Measure], 
        font_size: int, 
        styles: Styles = Styles(),
        font: FontFamily | str = Fonts.OpenSans,
        parent: Object = get_window(),
        components: Iterable[Component] = [],
        italic: bool = False,
        bold: bool = False,
        **_styles: Dict[str, Any]
    ):
        
        self.font = font
        self.font_size = font_size
        self.text = text
        self.bold = bold
        self.italic = italic
        
        # need before supert init because load_font uses it
        self.styles = styles 
        self.styles.resolve(parent.size)
        
        self.text_obj = self.load_font()

        super().__init__(
            pos=pos, 
            size=Size(self.text_obj.get_width(), self.text_obj.get_height()), 
            components=components, 
            parent=parent, 
            styles=styles,
            **_styles
        )
        
    def load_font(self):
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
        
        return font.render(self.text, True, self.styles.color)

    def update(self, **atributes):
        for k,v in atributes.items():
            if k in self.__slots__:
                setattr(self, k, v)
            else:
                raise ValueError(f"Invalid atribute: {k}")
        
        self.text_obj = self.load_font()
            
        self.size = Size(self.text_obj.get_width(), self.text_obj.get_height())


    def draw(self):
        self.window.surface.blit(self.text_obj, self.pos)

class Image(Object):
    r'''
    #### Image
    #### Parameters
    - `pos`: position of the image `[x, y]`
    - `size` : size of the image `[width, height]`
    - `image` : path to image file `str`

    #### Optional Arguments
    - `scale` : scale the image to the size `bool`
    - `components` : components to add in the object `[Component, ..]`
    - `styles` : Styles
    '''

    def __init__(
        self, 
        image: Path | str,
        pos: Pos | Iterable[Measure],  
        size: Size | Iterable[Measure],
        scale: bool = True,
        styles: Styles = Styles(),
        parent: "Object" = get_window(),
        components: Iterable[Component] = [],
        **_styles: Dict[str, Any]
    ):
        self.image = image
        self.scale = scale
        
        super().__init__(pos=pos, size=size, styles=styles, parent=parent, components=components, **_styles)
        try:
            self.image = pg.image.load(image)
        except:
            raise ValueError("Image not found:", image)

        if scale:
            self.image = pg.transform.scale(self.image, self.size)

    def draw(self):
        self.window.surface.blit(self.image, self.pos)

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

    #### Styles
    - `color`: color of the circle `"white" or (R, G, B)`
    - `stroke`: stroke of the circle `int`
    - `margins`: margins of the circle `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    '''
    __slots__ = ("radius", )

    def __init__(
        self, 
        pos: Pos | Iterable[Measure],
        radius: Measure,
        styles: Styles = Styles(),
        parent: "Object" = get_window(),
        components: Iterable[Component] = [],
        **_styles: Dict[str, Any]
        
    ):
        self.radius = resolve_measure(radius)

        super().__init__(pos=pos, size=Size(radius*2), styles=styles, parent=parent, components=components, **_styles)

    def draw(self):
        pg.draw.circle(
            self.window.surface,
            self.styles.color,
            self.pos, 
            self.radius, 
            self.styles.stroke
        )

    def _get_collision_box(self):
        center_x, center_y = self.pos
        radius = self.size[0]/2
        return (
            (center_x - radius, center_y - radius), # top-left
            (center_x + radius, center_y - radius), # top-right
            (center_x - radius, center_y + radius), # bottom-left
            (center_x + radius, center_y + radius)  # bottom-right
        )

class Ellipse(Object):
    r'''
        #### Ellipse
        #### Parameters
        - `pos`: position of the Ellipse `[x, y]`
        - `size`: size of the Ellipse `[width, height]`
        - `components` : components to add in the object `[Component, ..]`

        #### Styles
        - `color`: color of the Ellipse `"white" or (R, G, B)`
        - `stroke`: stroke of the Ellipse `int`
        - `margins`: margins of the Ellipse `[top, right, bottom, left]`
        '''

    def draw(self):
        pg.draw.ellipse(
            self.window.surface,
            self.styles.color, 
            (*self.pos, *self.size), 
            self.styles.stroke
        )

class Group:
    r"""
    #### Group
    
	#### Parameters
    - `parent` : parent of the group, objects position in the group will be relative to this object `Object`
        - if parent is a string, it will be searched in the group items
        
    - [*args] `objects` : objects to add in the group `Object, ..`
    - [**kwargs] `named_objects` : named objects to add in the group `name = Object, ..`

    #### Notes
    - named objects can be accessed by: `group["name"]`
    - no named objects can be accessed by: `group[object.id]`

    """
    
    def __init__(self, *objects, **named_objects):
        self.__objects = {}
        
        parent = named_objects.get("parent", None)
        if parent:
            del named_objects["parent"]
        
        self.add(*objects, **named_objects)
        
        if parent:
            if isinstance(parent, str):
                parent = self.__objects[parent]
                
        else:
            parent = None

        self.__parent = parent
        self.__last_parent_pos = Pos(0,0)
        
    def add(self, *objects, **named_objects):
        for obj in objects:
            self.__objects[obj.id] = obj
        
        self.__objects.update(named_objects)
    
    def remove(self, name: str):
        self.__objects.pop(name)

    def align_objects(self, auto_size = True):
        # aligns objects in the group
        if self.__parent.pos != self.__last_parent_pos:
                
            margin = self.__parent.size[1]*0.1
                
            current_y = self.__parent.pos[1] + margin
            
            for obj in self.__objects.values():
                if obj != self.__parent:
                
                    center(obj, self.__parent)
                    obj.pos[1] = current_y
                
                    current_y += obj.size[1] + margin
                    
                    if auto_size:
                        # if overflow, resize parent
                        
                        # x axis
                        if obj.pos[0] + obj.size[0] > self.__parent.pos[0] + self.__parent.size[0]:
                            self.__parent.size[0] = obj.pos[0] + obj.size[0] + margin * 1.5
                            center(obj, self.__parent)
                            
                        # y axis
                        if obj.pos[1] + obj.size[1] > self.__parent.pos[1] + self.__parent.size[1]:
                            self.__parent.size[1] = obj.pos[1] + obj.size[1] + margin * 1.5

            self.__last_parent_pos = self.__parent.pos

    def draw(self):
        # align objects to paren    
        if self.__parent:
            self.align_objects()
        
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
        d = {k: v for k, v in self.items() if func(v)}
        return d

    # getters        
    def __getitem__(self, key):
        return self.__objects[key]

    def __getattr__(self, name):
        return self.__objects[name]
    
    def values(self, no_parent=False):
        if no_parent and self.__parent:
            return [v for k, v in self.__objects.items() if v != self.__parent]
        
        return self.__objects.values()
    
    def items(self, no_parent=False):
        if no_parent and self.__parent:
            return {k: v for k, v in self.__objects.items() if v != self.__parent}
        
        return self.__objects.items()

    def keys(self, no_parent=False):
        if no_parent and self.__parent:
            return [k for k, v in self.__objects.items() if v != self.__parent]
    
        return self.__objects.keys()
    
    # delete item
    def __delitem__(self, key):
        self.__objects.pop(key)
        self.__dict__.pop(key)
        
    def __delattr__(self, key):
        self.__objects.pop(key)
        self.__dict__.pop(key)
    
    # contains
    def __contains__(self, key):
        return key in self.__objects
    
    # iterables
    def __iter__(self):
        return iter(self.values())
    
    def __next__(self):
        return next(self.values())

    def __len__(self):
        return len(self.__objects)
 
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
        pg.draw.line(self.window.surface, self.color,
                     self.start, self.end, self.width)

    def _get_collision_box(self):
        # collision is checked at line end
        return (self.end, self.end + (self.width, 0), self.end + (0, self.width), self.end + (self.width, self.width))
