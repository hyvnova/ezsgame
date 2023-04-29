from typing import Any, Callable, Dict, Iterable, Optional, Self, Set, Type
import pygame as pg

from ezsgame.styles.units import Measure

from ..styles.style import Styles

from ..components import ComponentGroup, Component
from ..global_data import get_window
from ..styles.styles_resolver import resolve_position, resolve_size
from ..funcs import center_at
from ..reactivity import Reactive

from ..types import Number, Pos, Size
from ..world import World

class Object:
    r"""
    Object is a base class for all objects in the game.
    should not be instantiated.
    """

    __slots__ = ("pos", "size", "window", "components", "behavior", "__on_draw", "parent", "children", "styles")

    def __init__(
        self, 
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        styles: Optional[Styles] = None,
        parent: Optional["Object"] = None,
        components: Iterable[Component] = [],
        **_styles: Dict[str, Any]
    ):
        """
        Base class for most object, handlers object default and required behavior
        """
        self.window = get_window()
        self.children: Set[Object] = set()
        
        if parent:
            self.parent = parent
            
            if parent != self.window:
                self.parent.add_child(self)
            
        else:
            self.parent = self.window
        
        
        self.styles = styles or Styles(**_styles)
        # resolve styles 
        self.styles.resolve(self.parent.size)
        
        self.size = resolve_size(self, size, self.parent.size)
        self.pos = resolve_position(self, pos, self.parent)

        # Adapt position to world
        self.pos += World.pos


        # defualt behavior - needs it own type and rework
        self.behavior = {"pos": "dynamic"}

        self.__on_draw: Dict[str, Callable] = {}

        self.components = ComponentGroup(self, *components)

        # Calls __after_draw() after  draw() to call after-draw methods
        def _draw_manager(draw_func):
            def wrapper():
                if self.styles.visible:
                    draw_func() 
                                       
                self.__after_draw()
                
            return wrapper
        try:
            self.draw = _draw_manager(self.draw)
        except:
            pass

    def add_child(self, child: Type[Self]) -> None:
        self.children.add(child)

    def _update(self, updated_property_name: str) -> None:
        """
        This method is called when a Reactive property (binded to this object) is updated.
        """
        value: Reactive = getattr(self, updated_property_name)
        value = value.get()
        
        if self.parent != self.window:
            self.parent._child_update(self) 
            
            
    def _child_update(self, child: Self) -> None:
        """
        Called when a child is updated.
        """
        pass        

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
        return f"<Object: {self.__class__.__name__}, ID: {id(self)}>"

    def __after_draw(self):
        r'''
        manages Object draw method and calls `on_draw` functions
        '''
        for func in self.__on_draw.values():
            func()
               
    def center_at(self, object: Type[Self] = None) -> Self:
        r'''
        #### Centers the object at another object
        #### Parameters
        - `object`: object to center at
        '''
        object = object or self.parent
        center_at(self, object)
        return self
            
    
    @property
    def center(self) -> Pos:
        r'''
        #### Returns the center of the object
        '''
        return self.pos + self.size / 2
    
    @center.setter
    def center(self, value: Pos) -> None:
        r'''
        #### Sets the center of the object
        #### Parameters
        - `value`: center position
        '''
        self.pos = value - self.size / 2

    @property
    def width(self) -> Number:
        return self.x

    @width.setter
    def width(self, value):
        self.x = value

    @property
    def height(self) -> Number:
        return self.y

    @height.setter
    def height(self, value):
        self.y = value

    @property
    def x(self) -> Number:
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @property
    def y(self) -> Number:
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos[1] = value    