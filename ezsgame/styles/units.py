from ast import pattern
from typing import NewType, Pattern, Union

Percent = NewType('Percent', Pattern[str])
percent: Percent = r'\d+%'

Pixels = NewType('Pixels', Pattern[str])
pixels: Pixels = r'\d+(px)?'

Fraction = NewType('Fraction', Pattern[str])
fraction: Fraction = r'\d+/\d+'

Measure = Union[Percent, Pixels, Fraction]