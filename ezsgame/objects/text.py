from typing import Any, Dict, Iterable, Set
import pygame as pg
from ..components import Component
from ..global_data import get_window
from ..objects.object import Object
from ..reactivity import Reactive
from ..styles.style import Styles
from ..styles.units import Measure
from ..types import Pos, Size
from ..fonts import Fonts, FontFamily


pg.font.init()


class Text(Object):
    r"""
    #### Text
    #### Parameters
    - `text`: text to be displayed
    - `pos`: position of the text `[x, y]`
    - `font_size`: font size of the text
    - `font` : font of the text `"Arial or "path/to/font.ttf"` or `ezsgame font` (default: `OpenSans`)
    - `bold` : if True, the text will be bold `bool`
    - `italic` : if True, the text will be italic `bool`

    #### Styles
    - `color`: color of the text `"white" or (R, G, B)`
    - `margins`: margins of the text `[top, right, bottom, left]`
    - `components` : components to add in the object `[Component, ..]`
    """

    __slots__ = (
        "font",
        "font_size",
        "text",
        "bold",
        "italic",
        "text_obj",
        "styles",
        "children",
    )

    def __init__(
        self,
        text: str,
        pos: Pos | Iterable[Measure],
        font_size: int,
        styles: Styles = Styles(),
        font: FontFamily | str = Fonts.OpenSans,
        parent: Object = None,
        components: Iterable[Component] = [],
        italic: bool = False,
        bold: bool = False,
        **_styles: Dict[str, Any],
    ):
        if not parent:
            parent = get_window()

        self.children: Set[Object] = set()

        self.font = font
        self.font_size = Reactive(font_size)._mount(self, "font_size")
        self.text = Reactive(text)._mount(self, "text")

        self.bold = bold
        self.italic = italic

        # need before supert init because load_font uses it
        self.styles = styles
        self.styles.resolve(parent.size)

        self.text_obj = self.load_font()

        super().__init__(
            pos=pos,
            size=Size(self.text_obj.get_width(), self.text_obj.get_height()),
            components=components,
            parent=parent,
            styles=styles,
            **_styles,
        )

    def load_font(self):
        # is font is a ezsgame font
        if isinstance(self.font, FontFamily):
            font = self.font.get_font(self.font_size.get())

        # if font is a path | str
        elif isinstance(self.font, str):
            # if font in system fonts
            if font in pg.font.get_fonts():
                font = pg.font.SysFont(
                    font, self.font_size.get(), self.bold, self.italic
                )

            # if font is a path
            elif font.endswith(".ttf"):
                try:
                    font = pg.font.Font(font, self.font_size.get())
                except Exception as e:
                    raise ValueError(f"Error loading font: {e}")

            else:
                raise ValueError("Invalid font name or path: " + self.font)

        else:
            raise ValueError("Invalid font: " + self.font)

        return font.render(self.text.get(), True, self.styles.color)

    def _update(self, updated_property_name: str):
        if updated_property_name == "text":
            self.text_obj = self.load_font()
            self.size = Size(self.text_obj.get_width(), self.text_obj.get_height())

        super()._update(updated_property_name)

    def draw(self):
        self.window.surface.blit(self.text_obj, self.pos)
