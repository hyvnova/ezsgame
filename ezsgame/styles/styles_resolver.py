from typing import Iterable, List
from ..funcs import center_of
import re

from ..types import Size, Pos
from .units import Measure

from .colors import resolve_color, Color


def resolve_measure(measure: Measure, parent_length: float) -> float:
    if isinstance(measure, (int, float)):
        return measure
    
    if not isinstance(measure, str):
        raise ValueError("Invalid measure value type: " + measure)
    
    # if measure is a percentage    
    elif measure.endswith("%"):
            return float(measure[:-1]) * parent_length / 100
    
    # if measure is aspect ratio of parent
    elif re.match("[0-9]+/[0-9]+", measure):
            ratio = measure.split("/")
            try:
                measure = parent_length * int(ratio[0]) / int(ratio[1])
                
            except ZeroDivisionError as e:
                raise ValueError("Invalid aspect ratio: ", measure + " (divided by zero)")
        
    return measure

def resolve_position(child, pos: Pos | Iterable[Measure], parent) -> Pos:
    """
    #### Resolves child position
    
    #### Parameters
    - `child`: child object
    - `parent`: parent object, object will be
    
    #### Returns
    - `Pos`: child position
    """
    
    pos = Pos(
        resolve_measure(pos[0], parent.size[0]),
        resolve_measure(pos[1], parent.size[1])
    )
    size = child.size
    
    parent_size = parent.size
    parent_center = center_of(parent)

    margins = child.styles.margins

    margin_x = margins[3] + margins[1]
    margin_y = margins[0] + margins[2]
    
        
    # align position x
    if isinstance(pos[0], int) or isinstance(pos[0], float):
        pos[0] += margin_x

    elif isinstance(pos[0], str):

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


    return Pos(pos[0] + parent.pos[0], pos[1] + parent.pos[1])
    
def resolve_size(child, size: Size | Iterable[Measure], parent_size: Size) -> Size:
    """
    #### Resolves child size
    
    #### Parameters
    - `child`: child object
    - `parent`: parent object
    
    #### Returns
    - `Size`: child size
    """
    
    size = Size(
        resolve_measure(size[0], parent_size[0]),
        resolve_measure(size[1], parent_size[1])
    )
    
    margins = child.styles.margins

    margin_x = margins[3] + margins[1]
    margin_y = margins[0] + margins[2]
    
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
       
def resolve_margins(margins: Iterable[Measure], parent_size:Size) -> List[float]:
    if len(margins) == 1:
        margins = [margins[0], margins[0], margins[0], margins[0]]
        
    if len(margins) == 2:
        margins = [margins[0], margins[0], margins[1], margins[1]]
    
    for i,m in enumerate(margins):
        screen_i = 0 if i%2 == 0 else 1        
        margins[i] = resolve_measure(m, parent_size[screen_i])

    return margins

