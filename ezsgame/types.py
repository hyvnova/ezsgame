from dataclasses import dataclass
from typing import Self, Type, TypeAlias
import math
from numpy import sort


Number: TypeAlias = float | int


class Vector2:
    """
    #### 2 Values Vector, can handle arithmetic operations
    """
    __slots__ = ("x", "y")
    
    def __init__(self, a, b = None):
        self.__call__(a, b)

    def normalize(self) -> "Vector2":
        """
        #### Normalize the vector
        """
        mag = math.sqrt(self.x**2 + self.y**2)
        if mag > 0:
            self.x /= mag
            self.y /= mag

        return self

    def dot(self, other: Type[Self]) -> Number:
        """
        #### Dot product between two vectors
        """
        return self.x * other.x + self.y * other.y
    
    def magnitude(self) -> Number:
        """
        #### Return the magnitude of the vector
        """
        return math.sqrt(self.x**2 + self.y**2)

    def to_tuple(self) -> tuple[Number, Number]:
        """
        #### Return the vector as a tuple
        """
        return (self.x, self.y)

    def __add__(a, b):
        T = a.__class__
        
        if isinstance(b, Vector2):
            return T(a.x + b.x, a.y + b.y)    

        elif isinstance(b, (int, float)):
            return T(a.x + b, a.y + b)
        
        x, y = b
        return T(a.x + x, a.y + y)

    def __iadd__(self, b):
        if isinstance(b, Vector2):
            self.x += b.x
            self.y += b.y

        elif isinstance(b, (int, float)):
            self.x += b
            self.y += b

        else:
            x, y = b
            self.x += x
            self.y += y

        return self
        
    def __sub__(a, b):
        T = a.__class__
        
        if isinstance(b, Vector2):
            return T(a.x - b.x, a.y - b.y) 

        elif isinstance(b, (int, float)):
            return T(a.x - b, a.y - b)
        
        x, y = b
        return T(a.x - x, a.y - y)
        

    def __isub__(self, b):
        if isinstance(b, Vector2):
            self.x -= b.x
            self.y -= b.y

        elif isinstance(b, (int, float)):
            self.x -= b
            self.y -= b

        else:
            x, y = b
            self.x -= x
            self.y -= y

        return self

    def __mul__(a, b):
        T = a.__class__
        
        if isinstance(b, Vector2):
            return T(a.x * b.x, a.y * b.y)  

        elif isinstance(b, (int, float)):
            return T(a.x * b, a.y * b)
        
        x, y = b
        return T(a.x * x, a.y * y)

    def __imul__(self, b):
        if isinstance(b, Vector2):
            self.x *= b.x
            self.y *= b.y

        elif isinstance(b, (int, float)):
            self.x *= b
            self.y *= b

        else:
            x, y = b
            self.x *= x
            self.y *= y

        return self

    
    def __truediv__(a, b) -> "Vector2":
        T = a.__class__
        
        if isinstance(b, Vector2):
            return T(a.x / b.x, a.y / b.y)  

        elif isinstance(b, (int, float)):
            return T(a.x / b, a.y / b)

    def __itruediv__(self, b):
        if isinstance(b, Vector2):
            self.x /= b.x
            self.y /= b.y

        elif isinstance(b, (int, float)):
            self.x /= b
            self.y /= b

        else:
            x, y = b
            self.x /= x
            self.y /= y

        return self
    
    def __floordiv__(a, b):
        T = a.__class__
        
        if isinstance(b, Vector2):
            return T(a.x // b.x, a.y // b.y)  

        elif isinstance(b, (int, float)):
            return T(a.x // b, a.y // b)
        
    def __ifloordiv__(self, b):
        if isinstance(b, Vector2):
            self.x //= b.x
            self.y //= b.y

        elif isinstance(b, (int, float)):
            self.x //= b
            self.y //= b

        else:
            x, y = b
            self.x //= x
            self.y //= y

        return self
    
    def __mod__(a, b):
        T = a.__class__
        
        if isinstance(b, Vector2):
            return T(a.x % b.x, a.y % b.y)  

        elif isinstance(b, (int, float)):
            return T(a.x % b, a.y % b)

    def __imod__(self, b):
        if isinstance(b, Vector2):
            self.x %= b.x
            self.y %= b.y

        elif isinstance(b, (int, float)):
            self.x %= b
            self.y %= b

        else:
            x, y = b
            self.x %= x
            self.y %= y

        return self
    

    def __pow__(a, b):
        T = a.__class__
        
        if isinstance(b, Vector2):
            return T(a.x ** b.x, a.y ** b.y)  

        elif isinstance(b, (int, float)):
            return T(a.x ** b, a.y ** b)
        
    def __ipow__(self, b):
        if isinstance(b, Vector2):
            self.x **= b.x
            self.y **= b.y

        elif isinstance(b, (int, float)):
            self.x **= b
            self.y **= b

        else:
            x, y = b
            self.x **= x
            self.y **= y

        return self

    def __neg__(self):
        return self.__class__(-self.x, -self.y)
    
    def __pos__(self):
        return self.__class__(+self.x, +self.y)
    
    def __abs__(self):
        return self.__class__(abs(self.x), abs(self.y))
    
    def __call__(self, a, b):
        # if a is iterable 
        if hasattr(a, "__iter__") and not isinstance(a, str):
            a, b = a

        if a != None and (b == None):
            self.x = a
            self.y = a

        else:
            self.x = a
            self.y = b

    def __str__(self):
        return f"<Vector2 : {self.x}, {self.y}>"

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __iter__(self):
        return (self.x, self.y).__iter__() 

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError

    def __len__(self):
        return 2

    def copy(self) -> Type[Self]:
        return self.__class__(self.x, self.y)

    def ref(self):
        return self

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other):
        return not self == other
    
    def set(self, a, b):
        self.x = a
        self.y = b
    
class Size (Vector2):
    r"""
    #### Size
    #### Parameters
    - `width`: width  `int` or `[width, height]`
    - `height`: height `int` or `[width, height]`
    """

    def __init__(self, width: Number, height: Number = None):
        super().__init__(width, height)

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

    def __str__(self):
        return f"(width: {self.width}, height: {self.height})"
    
    def __repr__(self):
        return f"Size({self.width}, {self.height})"

class Pos (Vector2):
    r"""
    #### Position
    #### Parameters
    - `x`: x position `number` or `[x, y]`
    - `y`: y position `number`
    """

    def __init__(self, x: Number, y: Number = None):
        super().__init__(x, y)

    def __str__(self):
        return f"(x: {self.x}, y: {self.y})"

    def __repr__(self):
        return f"Pos({self.x}, {self.y})"

# Profiling options
import cProfile
from pstats import SortKey

@dataclass
class ProfilingOptions:
    profile: cProfile.Profile = cProfile.Profile()
    sort : SortKey = SortKey.CUMULATIVE
    limit : int = 10
    file : str = "profile.prof"