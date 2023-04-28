from pathlib import Path
from ..components import Component
from ..global_data import get_window
from ..objects.object import Object
from typing import Any, Dict, Iterable
from ..styles.style import Styles
import pygame as pg
from ..styles.units import Measure
from ..types import Pos, Size


class Image(Object):
    r"""
    #### Image
    #### Parameters
    - `pos`: position of the image `[x, y]`
    - `size` : size of the image `[width, height]`
    - `image` : path to image file `str`

    #### Optional Arguments
    - `scale` : scale the image to the size `bool`
    - `components` : components to add in the object `[Component, ..]`
    - `styles` : Styles
    """

    def __init__(
        self,
        image: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        scale: bool = True,
        styles: Styles = Styles(),
        parent: "Object" = None,
        components: Iterable[Component] = [],
        **_styles: Dict[str, Any]
    ):
        if not parent:
            parent = get_window()

        self.image = image
        self.scale = scale

        super().__init__(
            pos=pos,
            size=size,
            styles=styles,
            parent=parent,
            components=components,
            **_styles
        )
        try:
            self.image = pg.image.load(image)
        except:
            raise ValueError("Image not found:", image)

        if scale:
            self.image = pg.transform.scale(self.image, self.size)

    def draw(self):
        self.window.surface.blit(self.image, self.pos)

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.image, angle)
        self.size = [self.image.get_width(), self.image.get_height()]

    def flip(self, x_axis: bool = True, y_axis: bool = False):
        self.image = pg.transform.flip(self.image, x_axis, y_axis)
        self.size = [self.image.get_width(), self.image.get_height()]

    def scale(self, new_size: Size):
        self.image = pg.transform.scale(self.image, new_size)
        self.size = [self.image.get_width(), self.image.get_height()]
