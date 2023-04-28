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

class Component:
    def __init__(self):
        self.name = self.__class__.__name__

    def __str__(self):
        return f"<Component : {self.name}>"

    def __repr__(self):
        return self.__str__()

    def __remove(self):
        del self

# custom components creation ---------------------------------------------------
from enum import Enum


class ActivationMethods(Enum):
    ON_CLICK = "on_click"
    ON_KEYDOWN = "on_keydown"


from enum import Enum

class ActivationMethod(Enum):
    ON_CLICK = "on_click"
    ON_KEYDOWN = "on_keydown"
    
    
class ComponentTemplate:
    def __init__(self, activation_method: ActivationMethod = None):
        if not activation_method:
            raise ValueError("An activation method must be specified")
        if activation_method not in ActivationMethod:
            raise ValueError("Invalid activation method specified")
        
        self.activation_method = activation_method
        self.init_func = None
        self.call_func = None
        self.activate_func = None
        self.deactivate_func = None
        self.remove_func = None
        
    def init(self, func):
        self.init_func = func
        return func
        
    def call(self, func):
        self.call_func = func
        return func
        
    def activate(self, func):
        self.activate_func = func
        return func
        
    def deactivate(self, func):
        self.deactivate_func = func
        return func
        
    def remove(self, func):
        self.remove_func = func
        return func
        
    def create_component(self, obj, **kwargs):
        if not self.init_func:
            raise ValueError("An init function must be specified")
        
        component = Component()
        component.__kwargs = kwargs
        component.object = obj
        component.window = obj.window
        
        for key, value in kwargs.items():
            setattr(component, key, value)
        
        self.init_func(component)
        
        if self.activation_method == ActivationMethod.ON_CLICK:
            component.__activation_event_name = f"{component.__class__.__name__} on click activation {id(component.object)}"
            component.__desactivation_event_name = f"{component.__class__.__name__} on click desactivation {id(component.object)}"
            component.__activated = False
            
            def activate():
                if component.__activated == False:
                    component.__activated = True
                    
                    # removes activate event
                    component.window.events.remove_event(component.__activation_event_name)
                    
                    # adds desactivate event
                    component.window.events.on_event("mousedown", component.__desactivate, component.__desactivation_event_name)
                    
                    # calls "real" activation
                    self.activate_func(component)
                    
            def desactivate():
                if component.__activated:
                    component.__activated = False
                    
                    # removes desactivate event
                    component.window.events.remove_event(component.__desactivation_event_name)
                    
                    # calls "real" desactivation
                    self.deactivate_func(component)
                    
                    # adds activate event
                    component.window.events.add_event(event="click", object=component.object, callback=component.__activate, name=component.__activation_event_name)
            
            component.__activate = activate
            component.__desactivate = desactivate
            component.__remove = self.remove_func or (lambda: None)
            
            component.window.events.add_event(event="click", object=component.object, callback=component.__activate, name=component.__activation_event_name)
            
        else:
            component.__activate = self.activate_func or (lambda: None)
            component.__desactivate = self.deactivate_func or (lambda: None)
            component.__remove = self.remove_func or (lambda: None)
        
        if self.call_func:
            self.call_func(component, obj)
        else:
            component.__init__(**kwargs)
            
        return component
