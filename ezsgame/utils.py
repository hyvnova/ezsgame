"""
This module contains general purpose functions and classes.
"""

import math
from typing import Callable, Dict, Tuple, overload
from .types import Vector2

class Signal:
    """
    Creates the necesary implementation to add, remove and trigger signals.
    Signals are basicly a function that calls other functions when it is triggered.

    #### Example:
    ```python
    class Health(Component):

        def init(self):
            self.health = 100

            # Signal that will be triggered when the object is hit
            self.on_hit: TriggerSignal = TriggerSignal()

        def activate(self):
            \"\"\"
            Use `HitBox` object `on_collision` signal to add a trigger to the hitbox.
            `health_hitbox_collision` is the name of the trigger, used to remove the trigger if necessary.
            `self.hit` is the function that will be called when the `on_collision` signal is triggered.
            \"\"\"
            self.object.components[HitBox].on_collision.add("health_hitbox_collision", self.hit) 

        def deactivate(self):
            # remove the trigger from the hitbox
            self.object.components[HitBox].on_collision.remove("health_hitbox_collision")

        def hit(self, other):
            self.health -= 10
            self.on_hit.trigger(other) # calls all the functions that are listening to this signal

    ```
    """

    def __init__(self):
        self.listeners: Dict[str, Callable] = {}

    def trigger(self, *args, **kwargs):
        """
        #### Calls all the functions that are listening to this signal with the given arguments
        """
        for func in self.listeners.values():
            func(*args, **kwargs)

    def add(self, name: str, func: Callable):
        """
        #### Adds a function to the signal listeners
        """

        # check if the name is already in use
        if name in self.listeners:
            raise ValueError(f"Name \"{name}\" is already in use in this signal")
        
        self.listeners[name] = func

    def remove(self, name: str):
        """
        #### Removes a function from the signal listeners
        """
        self.listeners.pop(name)



def clamp(value, minimum, maximum):
    """
    Clamps a value between a minimum and maximum range
    """
    return max(minimum, min(maximum, value))

def lerp(start: float, end: float, time: float, duration: float) -> float:
    """
    Linearly interpolate between two values over a given amount of time
    
    ### Params
    - `start`: start value
    - `end`: end value
    - `time`: current time
    - `duration`: duration of the interpolation
    
    ### Return
    interpolated value
    """
    return start + (end - start) * (time / duration)


@overload
def lerp(start:float, stop:float, amount:float)->float:
    return start + (stop-start)*amount


def map_range(value: float, start1: float, stop1: float, start2: float, stop2: float) -> float:
    """
    Maps a value from one range to another
    
    ### Params
    - `value`: value to be mapped
    - `start1`: start of the first range
    - `stop1`: end of the first range
    - `start2`: start of the second range
    - `stop2`: end of the second range
    
    ### Return
    mapped value
    """
    return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2


def normalize(vector: Tuple[float, float] | Vector2) -> Vector2:
    """
    Normalize a 2D vector
    
    ### Params
    - `vector`: vector to be normalized
    
    ### Return
    Normalized vector
    """
    x, y = vector
    length = math.sqrt(x**2 + y**2)
    return x/length, y/length

def distance(p1: Tuple[float, float] | Vector2, p2: Tuple[float, float] | Vector2) -> float:
    """
    Calculates distance between two points
    
    ### Params
    - `p1`: first point
    - `p2`: second point
    
    ### Return
    distance
    """
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
