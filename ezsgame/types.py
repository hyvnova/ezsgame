class Vector2:
    """
    #### 2 Values Vector, handles basic arithmetic operations
    """
    __slots__ = ("_a", "_b")
    
    def __init__(self, a, b):
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
    
    def __call__(self, a, b):
        
        if isinstance(a, list) or isinstance(a, tuple) or isinstance(a, Vector2):
            self._a = a[0]
            self._b = a[1]

        else:
            self._a = a
            self._b = b

    def __str__(self):
        return f"<Vector2 : {self._a}, {self._b}>"

    def __repr__(self):
        return f"Vector2({self._a}, {self._b})"

    def __iter__(self):
        return (self._a, self._b).__iter__() 

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

    def copy(self) -> 'Vector2':
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

    def __init__(self, width, height):
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

    def __init__(self, x, y):
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

