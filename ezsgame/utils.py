
import math
from typing import Tuple, overload
from .types import Vector2


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
