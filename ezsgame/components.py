from ezsgame.primitive_objects import PRect

class ComponentGroup:
    def __init__(self, object, components=None):
        self.object = object
        self.components = []
        
        if components:
            self.add(*components)
     
    def add(self, *components):
        for comp in components:
            if comp not in self.components:
                self.components.append(comp)
                comp(self.object)


    def __str__(self):
        t = " ,".join([comp.__str__() for comp in self.components])
        return f"<Component Group : [{t}]>"
        
    def __repr__(self):
        return self.__str__()
   
    def remove(self, component):
        comp =  self.components[self.components.index(component)]
        comp.remove()
            

class Component:
    def __init__(self):
        self.name = self.__class__.__name__

    def __str__(self):
        return f"<Component : {self.name}>"
        
    def __repr__(self):
        return self.__str__()


class Resizable (Component):
    def __init__(self, object):
        if "screen" not in object.__dict__:
            raise Exception(f"Resizable components requires object (ID : {object._id}) to have screen attribute")

        super().__init__()
                         
        self.screen = object.screen
        self.object = object

        self.focus = False

        self._eventname_unfocus = "ResizableComponent.on.mousedown._unfocus.{self.object._id}"
        self._eventname_focus = "ResizableComponent.on.keydown._focus.{self.object._id}"
        self._eventname_resize = "ResizableComponent.on.keydown._resize.{self.object._id}"
        self._eventname_event_listener = "ResizableComponent.event_listener.{self.object._id}"
        
        self.screen.events.add_event_listener(event="mousedown", object=self.object, callback=lambda: self._activate(),name=self._eventname_event_listener)
        self.screen.events.on("mousedown", lambda: self._desactivate(), self._eventname_unfocus)

        self.gen_resize_obj()
        
        # saves the function to restore it is component is deleted
        self._object_draw_func = self.object.draw
        
        self.object.draw = self.draw(self.object.draw)
                                

    def gen_resize_obj(self):
        size = [self.object.size[0]*1.5, self.object.size[1]*1.5]
        pos = [self.object.pos[0] - size[0]//2 + self.object.size[0]//2, self.object.pos[1] - size[1]//2 + self.object.size[1]//2]
        self.resize_obj = PRect(size=size, pos=pos, screen=self.screen, color="red", stroke=2)
        
        
    def _resize(self):
        start = self.object.pos.copy()
        current = self.screen.mouse_pos()
        self.object.size[0] = current[0] - start[0]
        self.object.size[1] = current[1] - start[1]
        self.gen_resize_obj()


    def _activate(self):
        if self.focus == False:
            self.focus = True        
            self.screen.events.on("mousedown", lambda: self._desactivate(), self._eventname_unfocus)
            self.screen.time.add(10, self._resize, self._eventname_resize)

    def _desactivate(self):
        if self.focus:
            self.focus = False
        if "keydown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_focus)
        if "mousedown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_unfocus)  
            
        self.screen.time.remove(self._eventname_resize)
                
    
    def draw(self, func):
        def wrapper(*args, **kwargs):
            if self.focus:
                self.resize_obj.draw()
            func(*args, **kwargs)
            return func

        return wrapper

    def remove(self):
        self.object.draw = self._object_draw_func
        self._desactivate()
        self.screen.events.remove(self._eventname_event_listener)


class Drageable(Component):
    def __init__(self, object):
        if "screen" not in object.__dict__:
            raise Exception(f"Resizable components requires object (ID : {object._id}) to have screen attribute")

        super().__init__()
                         
        self.screen = object.screen
        self.object = object

        self.focus = False

        self._eventname_unfocus = "DrageableComponent.on.mousedown._unfocus.{self.object._id}"
        self._eventname_focus = "DrageableComponent.on.keydown._focus.{self.object._id}"
        self._eventname_move = "DrageableComponent.on.keydown._move.{self.object._id}"
        self._eventname_event_listener = "DrageableComponent.event_listener.{self.object._id}"
        
        self.screen.events.on("mousedown", lambda: self._desactivate(), self._eventname_unfocus)
        self.screen.events.add_event_listener(event="mousedown", object=self.object, callback=lambda: self._activate(),name=self._eventname_event_listener)

        self.gen_resize_obj()
        
        # saves the function to restore it is component is deleted
        self._object_draw_func = self.object.draw
        
        self.object.draw = self.draw(self.object.draw)
                                

    def gen_resize_obj(self):
        size = [self.object.size[0]*1.5, self.object.size[1]*1.5]
        pos = [self.object.pos[0] - size[0]//2 + self.object.size[0]//2, self.object.pos[1] - size[1]//2 + self.object.size[1]//2]
        self.resize_obj = PRect(size=size, pos=pos, screen=self.screen, color="red", stroke=1)
        
        
    def _move(self):
        pos = self.screen.mouse_pos()
        self.object.pos[0] = pos[0] - self.object.size[0] // 2 
        self.object.pos[1] = pos[1] - self.object.size[1] // 2 

        self.gen_resize_obj()


    def _activate(self):
        if self.focus == False:
            self.focus = True        
            self.screen.events.on("mousedown", lambda: self._desactivate(), self._eventname_unfocus)
            self.screen.time.add(10, self._move, self._eventname_move)
            
            self.screen.events.remove(self._eventname_event_listener)

    def _desactivate(self):
        if self.focus:
            self.focus = False
            self.screen.time.remove(self._eventname_move)
            self.screen.events.add_event_listener(event="mousedown", object=self.object, callback=lambda: self._activate(),name=self._eventname_event_listener)

        if "keydown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_focus)
        if "mousedown" in self.screen.events.base_events:
            self.screen.events.remove_base_event(self._eventname_unfocus)  
            

    
    def draw(self, func):
        def wrapper(*args, **kwargs):
            if self.focus:
                self.resize_obj.draw()
            func(*args, **kwargs)
            return func

        return wrapper

    def remove(self):
        self.object.draw = self._object_draw_func
        self._desactivate()
        self.screen.events.remove(self._eventname_event_listener)