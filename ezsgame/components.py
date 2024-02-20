from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar


class Component(ABC):
    """
    Base class for components, ensures that components will act as supposed.

    ###  Methods:
    - `__init__` : Called when the component is created (Used for initialization and getting arguments) Note: `__init__` is called before `mount` so it doen't have access to a `self.object` yet
    - `mount(object)` : Called after the component is mounted to an object
    - `activate` : Called when the component is activated
    - `deactivate` : Called when the component is deactivated
    - `remove` : Called when the component is removed
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__name__ = cls.__name__
        return instance

    def __str__(self):
        return f"<Component : {self.__name__}>"

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def mount(self, object) -> None:
        """
        Called after the component is mounted to an object
        """
        raise NotImplementedError(
            f"Component <{self.__name__}> must implement `init` (Component initialization)"
        )

    @abstractmethod
    def activate(self) -> None:
        raise NotImplementedError(
            f"Component <{self.__name__}> must implement `activate` (Component activation)"
        )

    @abstractmethod
    def deactivate(self) -> None:
        raise NotImplementedError(
            f"Component <{self.__name__}> must implement `deactivate` (Component deactivation)"
        )

    def remove(self) -> None:
        """
        You should not call this method, it is called by the component group when removing the component.
        Makes sure the component is deleted and removed properly
        """
        self.deactivate()
        del self

ComponentType = TypeVar('ComponentType', bound=Component)

class ComponentGroup:
    """
    Handlers components for an object, can be used to add, remove, toggle, get, set, delete, iterate, slice, clear, check if contains, etc.
    """

    def __init__(self, object):
        self.object = object
        self.components: Dict[Type[Component], Component] = {}

    def __del__(self):
        self.clear()
        del self

    def __str__(self):
        t = ", ".join([*map(str, self.components.values())])
        return f"<Component Group : [{t}] >"

    def __repr__(self):
        return self.__str__()

    def get(self, component: Type[Component], default: Any = None) -> Component:
        """
        Get a component from the component group

        ### Example:
        ```py
        component_group.get(HitBox)
        """
        return self.components.get(component.__name__, default)

    def clear(self):
        self.remove(*self.components.keys())

    def remove(self, *components: Component):
        for component in components:
            comp = self.components.get(component, None)

            if comp:
                comp.remove()
                del self.components[component]

    def add(self, *components: Component, force: bool = False):
        for comp in components:
            comp_name = comp.__name__

            if comp and (comp_name not in self.components or force):
                self.components[comp_name] = comp
                comp.mount(self.object)
                comp.activate()

    def __contains__(self, component: Type[Component]):
        return component.__name__ in self.components.keys()

    def toggle(self, component: Type[Component]):
        if component.__name__ in self.components:
            self.remove(component)
            return False
        else:
            self.add(component)
            return True

    def __getitem__(self, other: Type[ComponentType]) -> ComponentType:
        other = other.__name__

        if other in self.components:
            return self.components[other]
        else:
            raise KeyError(f"Cannot get Component {other}  because not found in {self}")

    def __delitem__(self, other):
        if isinstance(other, int):
            del self.components[list(self.components.keys())[other]]

        elif isinstance(other, slice):
            self.__delslice__(other)

        else:
            if other in self.components:
                self.remove(other)
            else:
                raise KeyError(
                    f"Cannot delete Component <{other}>  because not found in {self}"
                )

    def __getslice__(self, other):
        return [*self.components.values()][other.start : other.stop : other.step]

    def __get_components_keys(self, other):
        return [*self.components.keys()][other.start : other.stop : other.step]

    def __delslice__(self, other):
        for comp in self.__get_components_keys(other):
            self.remove(comp)

    def __get_key_by_index(self, index):
        return list(self.components.keys())[index]

    def __setitem__(self, other, item):
        if item not in self.components:
            try:
                comp = self.__get_key_by_index(other)
                self.remove(comp)
                self.add(item)
            except:
                raise TypeError("ComponentGroup can only contain Components")

        else:
            del self.components[other]

    def __len__(self):
        return len(self.components)

    def __iter__(self):
        self.__current_index = 0
        return iter(self.components.values())

    def __next__(self):
        if self.__current_index >= len(self.components):
            raise StopIteration
        else:
            self.__current_index += 1
            return self.components.values()[self.__current_index - 1]
