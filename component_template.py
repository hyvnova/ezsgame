from typing import Any
from enum import Enum

class ActivationMethod(Enum):
    ON_CLICK = "on_click"
    ON_KEYDOWN = "on_keydown"

class ComponentTemplate:
    def __init__(self):
        pass

    @staticmethod
    def _get_activation_functions(method: ActivationMethod):
        if method == ActivationMethod.ON_CLICK:
            def load_activation(self):
                self.__activation_event_name = f"{self.__class__.__name__} on click activation {id(self.object)}"
                self.__deactivation_event_name = f"{self.__class__.__name__} on click deactivation {id(self.object)}"
                self.__activated = False

                self.window.events.add_event(
                    event="click",
                    object=self.object,
                    callback=self.__activate,
                    name=self.__activation_event_name
                )

            def activate(self):
                if not self.__activated:
                    self.__activated = True
                    self.window.events.remove_event(self.__activation_event_name)
                    self.window.events.on_event(
                        "mousedown",
                        self.__deactivate,
                        self.__deactivation_event_name
                    )
                    self._activate()

            def deactivate(self):
                if self.__activated:
                    self.__activated = False
                    self.window.events.remove_event(self.__deactivation_event_name)
                    self._deactivate()
                    self.window.events.add_event(
                        event="click",
                        object=self.object,
                        callback=self.__activate,
                        name=self.__activation_event_name
                    )

            def remove(self):
                self.deactivate()
                self.window.events.remove_event(self.__activation_event_name)
                self._remove()
                del self

        else:
            load_activation = activate = deactivate = lambda self: None

            def remove(self):
                self._remove()
                del self

        return load_activation, activate, deactivate, remove

    @staticmethod
    def create(template_class, set_kwargs_as_attr=False) -> Any:
        if not hasattr(template_class, "activation_method"):
            raise Exception(f"No activation method defined at {template_class.__name__}")

        load_activation_func, activation_func, deactivation_func, remove_func = ComponentTemplate._get_activation_functions(
            template_class.activation_method
        )

        if not hasattr(template_class, "init"):
            raise Exception(f"No init method defined at {template_class.__name__}")

        def default_init_func(self, object=None, **kwargs):
            self.__kwargs = kwargs

            if not object:
                return

            self.object = object
            self.window = object.window

            if set_kwargs_as_attr:
                for key, value in kwargs.items():
                    setattr(self, key, value)

            self.__activate = lambda: activation_func(self)
            self.__deactivate = lambda: deactivation_func(self)
            self.__remove = lambda: remove_func(self)

            load_activation_func(self)

            self.init(**kwargs)

        def default_call_func(self, object):
            self.__init__(object, **self.__kwargs)

        if not hasattr(template_class, "remove"):
            template_class.remove = lambda self: None

        template_class.__init__ = default_init_func
        template_class.__call__ = default_call_func

        if not hasattr(template_class, "activate"):
            template_class.activate = lambda self: None

        if not hasattr(template_class, "deactivate"):
            template_class.deactivate = lambda self: None

        return template_class

# Example usage
class MyComponent:
    activation_method = ActivationMethod.ON_CLICK
    
    def init(self, text=None):
        self.text = text or "Hello, World!"
        print(f"MyComponent initialized with text '{self.text}'")
    
    def _activate(self):
        print(f"MyComponent")
