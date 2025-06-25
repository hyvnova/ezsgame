from ezsgame import *
from concurrent.futures import ThreadPoolExecutor

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

    def enable(self):
        self.object.on_draw.add(self._signal_name, self.draw)

    def disable(self):
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

    def enable(self) -> None:
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

    def disable(self) -> None:
        remove_event(self._hover_signal_name)
        remove_event(self._click_signal_name)


class DetectNear(Component):
    """
    When an object enter near the collision of this object, it will call the callback
    """

    def __init__(self, callback: Callable[[Object], None]) -> None:
        self.callback = callback
        self._event_name = f"detect_near_{id(self)}"

    def mount(self, object: Object):
        self.object = object

    def enable(self):
        # Set up
        @on_event("update", self._event_name)
        def check_for_collision():
            for obj in World.objects:
                if obj != self.object and is_colliding(self.object, obj):
                    self.callback(obj)

    def disable(self):
        remove_event(self._event_name)

    def remove(self):
        self.disable()


class DialogueBox(Component):
    """
    A dialogue box component that displays text in a box
    """

    def __init__(self, text: str | None = None, font_size: int = 20, color: str = "white", pace: int = 1) -> None: 
        self.enabled = True 

        self.lines = text.split("\n") if text else []
        self.current_line = 0

        self.font_size = font_size
        self.color = color
        # Lines per second
        self.pace = pace

        self._signal_name = f"dialogue_box_draw_{id(self)}"
        self._interval_event_name = f"dialogue_box_update_{id(self)}"

        self._time_since_last_line = 0

        # dummy object to hold the text
        self.text_obj = Text("", Pos(0, 0), 0)

    def __repr__(self):
        return f"DialogueBox(lines={self.lines}, current_line={self.current_line}, font_size={self.font_size}, color={self.color}, pace={self.pace})"

    def __str__(self):
        return self.__repr__()

    def push(self, lines: list[str]):
        """
        Set the text of the dialogue box and reset the state
        """
        self.lines = lines
        self.current_line = 0
        self._time_since_last_line = 0

        if not self.enabled:
            print("Enabling DialogueBox")
            self.enable()


    def reset(self):
        """
        Reset the dialogue box to its initial state
        """
        self.lines = []
        self.current_line = 0

        if self.enabled:
            self.disable()

    def update_text(self):
        print(
            "Current line:",
            self.lines[self.current_line] if self.lines else "No lines",
        )

        # Update existing text object if it exists instead of creating a new one
        if self.text_obj in World.objects:
            self.text_obj.text = (
                self.lines[self.current_line] if self.lines else ""
            )
            self.text_obj.pos = (
                self.object.pos + Pos(0, self.object.size.y + 20)
            )
        else:
            self.text_obj = Text(
                self.lines[self.current_line] if self.lines else "",
                # Below the object
                self.object.pos + Pos(0, self.object.size.y + 20),
                self.font_size,
                color=self.color,
                parent=self.object,
                z_index=2,
            )
            World.add(self.text_obj)

    def mount(self, object: Object):
        self.object = object

    def enable(self):
        # If there are no lines, do not enable the dialogue box
        if not self.lines:
            self.disable()
            return
    
        self.enabled = True

        self.update_text()
        World.add(self.text_obj)

        self.current_line -= 1 # So first line also get's time
        @add_interval(self.pace, self._interval_event_name)
        def every_pace():
            self.current_line += 1
            if self.current_line >= len(self.lines):
                self.reset()
                self.disable()
                return

            self.update_text()

    def disable(self):
        self.enabled = False
        World.remove(self.text_obj)

    def remove(self):
        self.disable()
