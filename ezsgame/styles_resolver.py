from typing import List
from colour import Color
from .funcs import center_of
import re

# Utility classes ---------------------------------------------------------------
class Vector2:
    r"""
    #### 2 Values Vector, parent of `Pos` and `Size`
    """
    __slots__ = "_a", "_b", "__current_index"
    
    def __init__(self, a=0, b=0):
        self.__call__(a, b)

    def __add__(a, b):
        if isinstance(b, Vector2):
            return Vector2(a._a + b._a, a._b + b._b)    

        elif isinstance(b, (int, float)):
            return Vector2(a._a + b, a._b + b)
        
        x, y = b
        return Vector2(a._a + x, a._b + y)

    def __sub__(a, b):
        if isinstance(b, Vector2):
            return Vector2(a._a - b._a, a._b - b._b) 

        elif isinstance(b, (int, float)):
            return Vector2(a._a - b, a._b - b)
        
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
    
    def set(self, a, b):
        self._a = a
        self._b = b
        

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


def resolve_measure(measure:str, parent_size:float) -> float:
    if isinstance(measure, (int, float)):
        return measure
    
    if not isinstance(measure, str):
        raise ValueError("Invalid measure value type: " + measure)
    
    # if measure is a percentage    
    elif measure.endswith("%"):
            return float(measure[:-1]) * parent_size / 100
    
    # if measure is aspect ratio of parent
    elif re.match("[0-9]+/[0-9]+", measure):
            ratio = measure.split("/")
            try:
                measure = parent_size * int(ratio[0]) / int(ratio[1])
                
            except ZeroDivisionError as e:
                raise ValueError("Invalid aspect ratio: ", measure + " (divided by zero)")
        
    return measure

def resolve_position(child, parent, absolute: bool) -> Pos:
    """
    #### Resolves child position
    
    #### Parameters
    - `child`: child object
    - `parent`: parent object
    - `absolute`: if True, child position is absolute, otherwise child position is relative to parent position
    
    #### Returns
    - `Pos`: child position
    """
    
    pos = child.pos
    size = child.size
    
    parent_size = parent.size
    parent_center = center_of(parent)

    margin_x = child.margins[3] + child.margins[1]
    margin_y = child.margins[0] + child.margins[2]
    
    
    if len(pos) == 1:
        pos = Pos(pos[0], pos[0])
        
    # align position x
    if isinstance(pos[0], int) or isinstance(pos[0], float):
        pos[0] += margin_x

    elif isinstance(pos[0], str):
        if pos[0].endswith("%"):
            pos[0] = float(pos[0][:-1]) * parent_size.width / 100

        else:
            pos[0] = pos[0].lower()
            
            if pos[0] not in ["left", "center", "right", "left-center", "right-center"]:
                    raise ValueError("Invalid x-axis position value", pos[0])
                
            if pos[0] == "center":
                pos[0] = parent_size[0]/2 - size[0]/2
                
            elif pos[0] == "right":
                pos[0] = parent_size[0] - size[0] - margin_x
                
            elif pos[0] == "right-center":
                pos[0] = parent_size[0] - size[0] / 2 - parent_center[0]/2 - margin_x
                
            elif pos[0] == "left":
                pos[0] = margin_x
                
            elif pos[0] == "left-center":
                pos[0] = parent_center[0]/2 - size[0] / 2 + margin_x
        
     # align position y
    if isinstance(pos[1], int) or isinstance(pos[1], float):
        pos[1] += margin_y
    
    elif isinstance(pos[1], str):
        if pos[1].endswith("%"):
            pos[1] = float(pos[1][:-1]) * parent_size.height / 100
        
        else:
            pos[1] = pos[1].lower()        
            
            if pos[1] not in ["top", "center", "bottom", "top-center", "bottom-center"]:
                raise ValueError("Invalid y-axis position value", pos[1])
            
            if pos[1] == "center":
                pos[1] = parent_size[1]/2 - size[1]/2
                
            elif pos[1] == "top":
                pos[1] = margin_y
                
            elif pos[1] == "top-center":
                pos[1] = parent_center[1]/ 2 - size[1]/2  + margin_y 
                
            elif pos[1] == "bottom":
                pos[1] = parent_size[1] - size[1] - margin_y
                
            elif pos[1] == "bottom-center":
                pos[1] = parent_size[1] - size[1]/2 - parent_center[1]/2 - margin_y


    if not absolute:
        return Pos(pos[0] + parent.pos[0], pos[1] + parent.pos[1])
    
    return Pos(pos[0], pos[1])

def resolve_size(child, parent) -> Size:
    """
    #### Resolves child size
    
    #### Parameters
    - `child`: child object
    - `parent`: parent object
    
    #### Returns
    - `Size`: child size
    """
    
    size = child.size
    parent_size = parent.size
    
    margin_x = child.margins[3] + child.margins[1]
    margin_y = child.margins[0] + child.margins[2]
    
    if len(size) == 1:
        size = Size(size[0], size[0])
    
    # align size x
    if isinstance(size[0], int) or isinstance(size[0], float):
        size[0] += margin_x
    
    elif isinstance(size[0], str):
        size[0] = resolve_measure(size[0], parent_size.width)
        
    # align size y
    if isinstance(size[1], int) or isinstance(size[1], float):
        size[1] += margin_y
    
    elif isinstance(size[1], str):
        size[1] = resolve_measure(size[1], parent_size.height)
       
    return Size(size[0], size[1])
       
def resolve_margins(margins, parent_size:Size) -> List[float]:
    if len(margins) == 1:
        margins = [margins[0], margins[0], margins[0], margins[0]]
        
    if len(margins) == 2:
        margins = [margins[0], margins[0], margins[1], margins[1]]
    
    for i,m in enumerate(margins):
        screen_i = 0 if i%2 == 0 else 1        
        margins[i] = resolve_measure(m, parent_size[screen_i])

    return margins


# COLOR --------------------------------------------------------------------------------------------------------------

adapt_rgb = lambda rgb: tuple(map(lambda i: i*255, rgb))
pure_rgb = lambda color: tuple(map(lambda i: i/255, color))

def resolve_color(color) -> Color:  
    if isinstance(color, str):
        if color.startswith("#"):
            return adapt_rgb(Color(color).rgb)
        
        return adapt_rgb(Color(color).get_rgb())
    
    return color
