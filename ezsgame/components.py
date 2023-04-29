from abc import ABC, abstractmethod
from enum import Enum
from .global_data import DATA

EventHandler = DATA.EventHandler

class ComponentGroup:
    """
	Handlers componets as a group, mainly the Mount/Unmount of each components
    """
    
    def __init__(self, object, *components):
        self.object = object
        self.components = {}

        if components:
            self.add(*components)

    def __del__(self):
        self.clear()
        del self

    def __str__(self):
        t = ", ".join([*map(str, self.components.values())])
        return f"<Component Group : [{t}] >"

    def __repr__(self):
        return self.__str__()

    def clear(self):
        self.remove(*self.components.keys())

    def remove(self, *components):
        for component in components:
            comp = self.components.get(component, None)

            if comp:
                comp.__remove()
                del self.components[component]

    def add(self, *components):
        for comp in components:
            comp_name = eval(f"{type(comp).__name__}")

            if comp and comp_name not in self.components:
                self.components[comp_name] = comp(self.object)

    def __contains__(self, thing):
        return eval(f"{type(thing).__name__}") in self.components.keys()

    def toggle(self, component):
        if eval(f"{type(component).__name__}") in self.components:
            self.remove(component)
            return False
        else:
            self.add(component)
            return True

    def __getitem__(self, other):
        if isinstance(other, int):
            return self.components[other]
        elif isinstance(other, slice):
            return self.__getslice__(other)

        else:
            if other in self.components:
                return self.components[other]
            else:
                raise KeyError(
                    f"Cannot get Component <{other}>  because not found in {self}")

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
                    f"Cannot delete Component <{other}>  because not found in {self}")

    def __getslice__(self, other):
        return [*self.components.values()][other.start:other.stop:other.step]

    def __get_components_keys(self, other):
        return [*self.components.keys()][other.start:other.stop:other.step]

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

class Component(ABC):
    def __init__(self):
        self.name = self.__class__.__name__

    def __str__(self):
        return f"<Component : {self.name}>"

    def __repr__(self):
        return self.__str__()

    def __remove(self):
        del self

    @abstractmethod
    def init(self, obj):
        pass

    @abstractmethod
    def call(self, obj):
        pass

    @abstractmethod
    def activate(self, obj):
        pass

    @abstractmethod
    def deactivate(self, obj):
        pass

    @abstractmethod
    def remove(self, obj):
        pass

    
