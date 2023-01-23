from typing import Any, Callable, List, Self, Set


class Reactive:
    def __init__(self, value: Any) -> None:

        if isinstance(value, Reactive):
            self = value
            
        else:
            self._value = value
            
            self._update_method: Callable[[str], None] = None
            self._property_name: str = None
            
    def _mount(self, object, property_name: str, update_method_name: str = "_update") -> Self:
        
        self._update_method = getattr(object, update_method_name, None)
        self._property_name = property_name
        
        if not self._update_method:
            raise ValueError(f"Error while trying to mount Reactive value -> Cannot find {update_method_name} method at {object}")
        
        return self
        
    def set(self, new_value: Any) -> None:
        self._value = new_value
        self._update_method(self._property_name)

    def get(self) -> Any:
        return self._value
    

    # Arithmetic magic method that change the value
    def __iadd__(self, other):
        self._value += other
        self.set(self._value)
        return self

    def __isub__(self, other):
        self._value -= other
        self.set(self._value)
        return self

    def __imul__(self, other):
        self._value *= other
        self.set(self._value)
        return self

    def __itruediv__(self, other):
        self._value /= other
        self.set(self._value)
        return self


    # Arithmetic magic method
    def __add__(self, other):
        return self._value + other
    
    def __sub__(self, other):
        return self._value - other

    def __mult__(self, other):
        return self._value * other
    
    def __div__(self, other):
        return self._value / other
    
    def __truediv__(self, other):
        return self._value // other
    
    def __pow__(self, other):
        return self._value ** other

    # Comparing magic methods
    
    def __eq__(self, other):
        return self._value == other

    def __ne__(self, other):
        return self._value != other

    def __lt__(self, other):
        return self._value < other
    
    def __le__(self, other):
        return self._value <= other

    def __gt__(self, other):
        return self._value > other

    def __ge__(self, other):
        return self._value >= other

    def __neg__(self):
        return -self._value

    def __pos__(self):
        return +self._value

    def __abs__(self):
        return abs(self._value)

    def __invert__(self):
        return ~self._value

    def __and__(self, other):
        return self._value & other

    def __or__(self, other):
        return self._value | other

    def __xor__(self, other):
        return self._value ^ other

    def __lshift__(self, other):
        return self._value << other

    def __rshift__(self, other):
        return self._value >> other
