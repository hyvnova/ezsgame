from ezsgame import *

class Label(Component):
    """
    A label components is a text centered in the object
    """

    def __init__(self, text: str, font_size: int = 20, color: str = "white") -> None:
        self.text = text
        self.font_size = font_size
        self.color = color
        self._signal_name = f"label_draw_{id(self)}"

    def draw(self):
        self.text_obj.draw()

    def mount(self, object: Object):
        self.object = object
        self.text_obj = Text(
            self.text,
            Pos("center", "center"),
            self.font_size,
            color=self.color,
            parent=self.object,
        )

    def activate(self):
        self.object.on_draw.add(self._signal_name, self.draw)

    def deactivate(self):
        self.object.on_draw.remove(self._signal_name)

    def remove(self):
        pass


class Selectable(Component):
    """
    A selectable component is an object that can be selected
    When hovered -> chances color and plays a sound
    When clicked -> gets selected
    """

    def __init__(
        self,
        hover_color: str = "green",
        hover_sound: str = "assets\hover.mp3",
        select_sound: str = "assets\click.mp3",
        on_select: Callable = lambda: None,
    ) -> None:

        self.on_select = on_select

        self.hover_color = hover_color

        self.hover_sound = Sound(hover_sound)
        self.select_sound = Sound(select_sound)

        self.is_hovered = False

        # signals
        self._hover_signal_name = f"selectable_hover_{id(self)}"
        self._click_signal_name = f"selectable_select_{id(self)}"

    def mount(self, object: Object):
        self.object = object
        self.original_color = object.styles.color

    def activate(self) -> None:
        @add_event("hover", self.object, name=self._hover_signal_name)
        def hover():
            if self.is_hovered:
                return

            self.object.styles.color = "green"
            self.object.styles.resolve(self.object.parent.size)
            self.hover_sound.play()

            self.is_hovered = True

        @add_event("unhover", self.object, name=self._hover_signal_name)
        def unhover():
            if not self.is_hovered:
                return

            self.is_hovered = False
            self.object.styles.color = self.original_color
            self.object.styles.resolve(self.object.parent.size)


        @add_event("click", self.object, name=self._click_signal_name)
        def select():
            self.select_sound.play()
            self.on_select()

    def deactivate(self) -> None:
        remove_event(self._hover_signal_name)
        remove_event(self._click_signal_name)
