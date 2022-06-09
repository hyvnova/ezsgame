from ..global_data import get_screen
from ..extra.controller import Controller
from ..funcs import outline, move


class ComponentGroup:
    def __init__(self, object, components=None):
        self.object = object
        self.components = {}
        
        if components:
            self.add(*components)
    
    def __str__(self):
        t = ", ".join([*map(str,self.components.values())])
        return f"<Component Group : [{t}] >"
        
    def __repr__(self):
        return self.__str__()

    def clear(self):
        for comp in self.components:
            self.remove(comp)
           
    def remove(self, *components):
        for component in components:
            comp = self.components.get(component, None)
            if comp:
                del self.components[component]
                comp.remove()
                
    def add(self, *components):
        for comp in components:
            if comp not in self.components:
                self.components[comp] = comp(self.object)
                
    def __contains__(self, thing):
        return thing in self.components

    def toggle(self, component):
        if component in self.components:
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
                raise KeyError(f"Cannot get Component <{other}>  because not found in {self}")

    def __delitem__(self, other):
        if isinstance(other, int):
            del self.components[list(self.components.keys())[other]]

        elif isinstance(other, slice):
            self.__delslice__(other)
            
        else:
            if other in self.components:
                self.remove(other)
            else:
                raise KeyError(f"Cannot delete Component <{other}>  because not found in {self}")
        
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

    def remove(self):
       del self

class Resizable (Component):
    def __call__(self, object):
        self.__init__(object, self.__dict__.get("freeze_width", False), self.__dict__.get("freeze_height", False))
        
    def __init__(self, object=None, freeze_width:bool=False, freeze_height:bool=False):
        self.freeze_width = freeze_width
        self.freeze_height = freeze_height
        
        if not object:
            return
        
        if "screen" not in object.__dict__:
            setattr(object, "screen", get_screen())

        super().__init__()
                         
        self.screen = object.screen
        self.object = object

        self.focus = False

        self._eventname_unfocus = f"ResizableComponent.on.mousedown._unfocus.{self.object.id}"
        self._eventname_focus = f"ResizableComponent.on.keydown._focus.{self.object.id}"
        self._eventname_resize = f"ResizableComponent.on.keydown._resize.{self.object.id}"
        self._eventname_event_listener = f"ResizableComponent.event_listener.{self.object.id}"
        
        self.screen.events.add_event(event="mousedown", object=self.object, callback= self.activate,name=self._eventname_event_listener)
        self.screen.events.on_event("mousedown", self.desactivate, self._eventname_unfocus)
        
        self.object.on_draw(self.draw, self._eventname_event_listener, True)
        
    def _resize(self):
        start = self.object.pos.copy()
        current = self.screen.mouse_pos()   
        
        x,y = current[0] - start[0], current[1] - start[1]
    
        if not self.freeze_width:
            if x < 0:
                self.object.pos[0] = current[0] 
                self.object.size[0] = abs(x) + self.object.size[0]
            else:
                self.object.size[0] = x
            
        if not self.freeze_height:
            if y < 0:   
                self.object.pos[1] = current[1]
                self.object.size[1] = abs(y)
            else:
                self.object.size[1] = y
            

    def activate(self):
        if self.focus == False:
            self.focus = True        
            self.screen.events.on_event("mousedown", self.desactivate, self._eventname_unfocus)
            self.screen.time.add(10, self._resize, self._eventname_resize)

    def desactivate(self):
        if self.focus:
            self.focus = False
        if "keydown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_focus)
        if "mousedown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_unfocus)  
            
        self.screen.time.remove(self._eventname_resize)
                
    def draw(self, obj):
        if self.focus:
            outline(obj)

    def remove(self):
        self.object.remove_on_draw(self._eventname_event_listener)
        self.desactivate()
        self.screen.events.remove(self._eventname_event_listener)
        del self

class Draggable(Component):
    def __call__(self, object):
        self.__init__(object, self.__dict__.get("freeze_x", False), self.__dict__.get("freeze_y", False))
    
    def __init__(self, object=None, freeze_x:bool=False, freeze_y:bool=False):
        self.freeze_x = freeze_x
        self.freeze_y = freeze_y
        
        if not object:
            return
        
        if "screen" not in object.__dict__:
            setattr(object, "screen", get_screen())

        super().__init__()
                         
        self.screen = object.screen
        self.object = object

        self.focus = False

        self._eventname_unfocus = f"DrageableComponent.on.mousedown._unfocus.{self.object.id}"
        self._eventname_focus = f"DrageableComponent.on.keydown._focus.{self.object.id}"
        self._eventname_move = f"DrageableComponent.on.keydown._move.{self.object.id}"
        self._eventname_event_listener = f"DrageableComponent.event_listener.{self.object.id}"
        
        self.screen.events.add_event(event="mousedown", object=self.object, callback= self.activate, name=self._eventname_event_listener)
        self.object.on_draw(self.draw, self._eventname_move, True)
              
    def _move(self):
        pos = self.screen.mouse_pos()
        if not self.freeze_x:
            self.object.pos[0] = pos[0] - self.object.size[0] // 2 
            
        if not self.freeze_y:
            self.object.pos[1] = pos[1] - self.object.size[1] // 2 

    def activate(self):
        if self.focus == False:
            self.focus = True        
            self.screen.events.on_event("mousedown", self.desactivate, self._eventname_unfocus)
            self.screen.time.add(10, self._move, self._eventname_move)
            
            self.screen.events.remove_event(self._eventname_event_listener)

    def desactivate(self):
        if self.focus:
            self.focus = False
            self.screen.time.remove(self._eventname_move)
            self.screen.events.add_event(event="mousedown", object=self.object, callback=self.activate, name=self._eventname_event_listener)

        if "keydown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_focus)
        if "mousedown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_unfocus)  
                
    def draw(self, obj):
        if self.focus:
            outline(obj)

    def remove(self):
        self.object.remove_on_draw(self._eventname_move)
        self.desactivate()
        self.screen.events.remove_event(self._eventname_event_listener)
        self.screen.time.remove(self._eventname_move)
        del self

class Controllable(Component):
    def __call__(self, object):
        self.__init__(object, self.__dict__.get("keys", ["a", "d", "w", "s"]), 
                        self.__dict__.get("speed", [-25,25,25,-25]), 
                        self.__dict__.get("use_delta_time", True))
        
    def __init__(self, object=None, keys:list=["a", "d", "w", "s"], speed:list =[-25,25,25,-25], use_delta_time=True):
        self.keys = keys
        self.speed = speed
        self.user_delta_time = use_delta_time
        
        if not object:
            return
    
        super().__init__()
                         
        self.screen = object.screen
        self.object = object

        self.controller = Controller(keys=keys, speed=speed, use_delta_time=use_delta_time)
        self.object.on_draw(self._move, f"ControllableComponent.on.draw.{self.object.id}", True)
        
    def activate(self):
        self.controller.enable()
        
    def deactivate(self):
        self.controller.disable()
    
    def _move(self, obj):
        speed = self.controller.get_speed("simple")
        move(obj, speed)

    def remove(self):
        self.object.remove_on_draw(f"ControllableComponent.on.draw.{self.object.id}")
        del self.controller
        del self    
    