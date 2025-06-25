from .funcs import is_hovering
from .event_handler import *
from .objects import *


class InputBox:
    def __init__(
        self,
        callback: Callable,
        prompt: str = "",
        max_length: int = 64,
        focused: bool = True,
    ):

        self.max_length = max_length
        self.callback = callback
        self.prompt = prompt
        self.focused = focused

        self.rect = Rect(
            Pos("center", "bottom"),
            Size("30%", "8%"),
            color="white",
            stroke=4,
        )

        self.text = Text(
            "",
            Pos("center", "center"),
            font_size=25,
            color="white",
            parent=self.rect,
        )

        World.add(self.rect)

        self._event_names = [
            f"key_down_{id(self)}",
        ]

        if self.focused:
            self._catch_keys()

    def _catch_keys(self):
        @on_event("keydown", name=self._event_names[0], priority=True)
        def keydown(key, unicode):
            # stop on enter
            if key == pg.K_RETURN:
                self.end()
                return

            text = self.text
            # stop on backspace
            if key == pg.K_BACKSPACE:
                text.text.set(text.text.get()[:-1] if len(text) > 0 else "")
                return

            if len(text) >= self.max_length:
                return

            text.text += unicode


    def _stop_catch_keys(self):
        """
        Stop catching keys
        """
        for event_name in self._event_names:
            remove_event(event_name)

    def end(self):
        """
        End the input box and call the callback
        """
        self.focused = False
        self._stop_catch_keys()
        text = self.text.text.get().strip()
        del self.rect
        del self.text
        self.callback(text)
        Input.getting_input = False


class Input:
    """
    Use to acquire user input
    """

    _instance = None
    getting_input = False

    def __new__(self):
        if not self._instance:
            self._instance = super(Input, self).__new__(self)
        return self._instance

    def __call__(self):
        return self

    def get_text(
        self, ui_input_box: "InputBox" = InputBox, **kwargs
    ):  # Arguments being passed to InputBox constructor
        """
        Decorator, will call the function when user inputs text
        """

        def wrapper(func):

            if Input.getting_input:
                return

            Input.getting_input = True
            ui_input_box(func, **kwargs)

            return func

        return wrapper
