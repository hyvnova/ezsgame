from dataclasses import dataclass, field
from typing import  Iterable, Tuple

from ..types import Size

from .styles_resolver import resolve_color, resolve_margins
from .colors import Color
from .units import Measure

@dataclass(slots=True)
class Styles:
    """
    Structure of objects styles
    """
    color: Color | str | Tuple[int, int, int] = "white"
    
    margins: Iterable[Measure] = field(default_factory=lambda: [0])
    border_radius: Iterable[Measure] = field(default_factory=lambda: [0])
    
    stroke: int = 0
    z_index: int = 0

    # bools
    visible: bool = True
    
    
    def resolve(self, parent_size: Size):
        
        # color
        self.color = resolve_color(self.color)
        
        # marings
        self.margins = resolve_margins(self.margins, parent_size)
        
        # border radiues
        self.border_radius = resolve_margins(self.border_radius, parent_size)
        