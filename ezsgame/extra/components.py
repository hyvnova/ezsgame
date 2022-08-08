from typing import Callable
from ..global_data import get_screen
from ..extra.controller import Controller
from ..funcs import outline, move


class ComponentGroup:
	def __init__(self, object, *components):
		self.object = object
		self.components = {}
		
		if components:
			self.add(*components)
	
	def __del__(self):
		self.clear()
		del self

	def __str__(self):
		t = ", ".join([*map(str,self.components.values())])
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
			comp_name =  eval(f"{type(comp).__name__}")

			if comp and comp_name not in self.components:
				self.components[ comp_name ] = comp(self.object)
				
	def __contains__(self, thing):
		return eval(f"{type(thing).__name__}") in self.components.keys()

	def toggle(self, component):
		if  eval(f"{type(component).__name__}") in self.components:
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

	def __remove(self):
	   del self

class Resizable (Component):
	def __call__(self, object):
		self.__init__(object, self.__dict__.get("freeze_width", False), self.__dict__.get("freeze_height", False), 
					  self.__dict__.get("outline", outline))
		
		return self
		
	def __init__(self, object=None, freeze_width:bool=False, freeze_height:bool=False, outline:Callable=outline):
		self.freeze_width = freeze_width
		self.freeze_height = freeze_height
		self.outline = outline
		
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
		
		self.screen.events.add_event(event="mousedown", object=self.object, callback= self.activate, name=self._eventname_event_listener)
		
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

			# removes active event
			self.screen.events.remove_event(self._eventname_event_listener)

			# add desactivate event 
			self.screen.events.on_event("mousedown", self.desactivate, self._eventname_unfocus)

			# add resize event 
			self.screen.time.add(50, self._resize, self._eventname_resize)

	def desactivate(self):
		if self.focus:
			self.focus = False

			# removes desactiva event
			self.screen.events.remove_event(self._eventname_unfocus)
			
			# removes resize event
			self.screen.time.remove(self._eventname_resize)
			
		# adds active event
		self.screen.events.add_event(event="mousedown", object=self.object, callback= self.activate, name=self._eventname_event_listener)
		
				
	def draw(self, obj):
		if self.focus and self.outline:
			self.outline(obj)
		
	def __remove(self):
		self.object.remove_on_draw(self._eventname_event_listener)
		self.desactivate()
		self.screen.events.remove_event(self._eventname_event_listener)
		del self

class Draggable(Component):
	def __call__(self, object):
		self.__init__(object, self.__dict__.get("freeze_x", False), self.__dict__.get("freeze_y", False),
					  self.__dict__.get("outline", outline))

		return self
	
	def __init__(self, object=None, freeze_x:bool=False, freeze_y:bool=False, outline:Callable=outline):
		self.freeze_x = freeze_x
		self.freeze_y = freeze_y
		self.outline = outline
		
		if not object:
			return 
		
		if "screen" not in object.__dict__:
			setattr(object, "screen", get_screen())

		super().__init__()
						 
		self.screen = object.screen
		self.object = object

		self.focus = False

		# defines evnames of object os thay can be added or removed
		self._eventname_unfocus = f"DrageableComponent.on.mousedown._unfocus.{self.object.id}"
		self._eventname_focus = f"DrageableComponent.on.keydown._focus.{self.object.id}"
		self._eventname_move = f"DrageableComponent.on.keydown._move.{self.object.id}"
		self._eventname_event_listener = f"DrageableComponent.event_listener.{self.object.id}"
		
		# adds activate event 
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
			
			# removes activate event
			self.screen.events.remove_event(self._eventname_event_listener)

			# adds desactivate event 
			self.screen.events.on_event("click", self.desactivate, self._eventname_unfocus)

			# adds move event
			self.screen.time.add(50, self._move, self._eventname_move)

	def desactivate(self):
		if self.focus:
			self.focus = False
			
			# removes desactivate event 
			self.screen.events.remove_event(self._eventname_unfocus) 
			
			# removes move event 
			self.screen.time.remove(self._eventname_move)
			
		# adds activate event
		self.screen.events.add_event(event="click", object=self.object, callback=self.activate, name=self._eventname_event_listener)
				
	def draw(self, obj):
		if self.focus and self.outline:
			self.outline(obj)

	def __remove(self):
		self.object.remove_on_draw(self._eventname_move)
		self.desactivate()
		self.screen.events.remove_event(self._eventname_event_listener)
		self.screen.time.remove(self._eventname_move)
		del self

class Controllable(Component):
	def __call__(self, object):
		self.__init__(object, 
					  self.__dict__.get("keys", ["a", "d", "w", "s"]), 
					  self.__dict__.get("speed", [-25,25,25,-25]), 
					  self.__dict__.get("use_delta_time", True)
					  )
		return self
		
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
		speed = self.controller.get_speed()
  
		if len(speed) == 4:
			speed = [speed[0] + speed[1], speed[2] + speed[3]]
 
		move(obj, speed)

	def __remove(self):
		self.object.remove_on_draw(f"ControllableComponent.on.draw.{self.object.id}")
		del self.controller
		del self    
	
 
# custom components creation ---------------------------------------------------
class ComponentTemplate:
    
	activation_methods = type("activation_methods", (), {
		"on_click" : "on_click",
		"on_keydown" : "on_keydown",

	})
 
	@staticmethod
	def __get_activation_function(method:str):
     
		# on click 
		if method == ComponentTemplate.activation_methods.on_click:
      
			# this funcions creates all needed vars for activation/desactivation at __init__
			def load_activation(self):
				self.__activation_event_name = f"{self.__class__.__name__} on click activation {self.object.id}"
				self.__desactivation_event_name = f"{self.__class__.__name__} on click desactivation {self.object.id}"
				self.__activated = False
    
				# adds activation event
				self.screen.events.add_event(event="click", object=self.object, callback=self.__activate, name=self.__activation_event_name)		
   
			def activate(self):
				if self.__activated == False:
					self.__activated = True        
					
					# removes activate event
					self.screen.events.remove_event(self.__activation_event_name)

					# adds desactivate event 
					self.screen.events.on_event("mousedown", self.__desactivate, self.__desactivation_event_name)
					
					# calls "real" activation 
					self.activate()
     
			def desactivate(self):
				if self.__activated:
					self.__activated = False
					
					# removes desactivate event 
					self.screen.events.remove_event(self.__desactivation_event_name) 
					
					# calls "real" desactivation
					self.desactivate()
     
					# adds activate event
					self.screen.events.add_event(event="click", object=self.object, callback=self.__activate, name=self.__activation_event_name)
				
			def remove(self):
				self.__desactivate()
				self.screen.events.remove_event(self.__activation_event_name)
				self.remove()
				del self

		else:
			load_activation = activate = desactivate = lambda self: None
			
			def remove(self):
				self.remove()
				del self

		return load_activation, activate, desactivate, remove

 
	def create(template_class, set_kwargs_as_attr=False) -> Component:
		
		# if no actiovation method is defined raise error
		if not template_class.__dict__.get("activation_method"):
			raise Exception(f"No activation method defined at {template_class.__name__}")

		load_activation_func, activation_func, desactivation_func, remove_func = ComponentTemplate.__get_activation_function(
      						template_class.activation_method
                 			)
  
		# if no init method is defined raise error
		if not template_class.__dict__.get("init"):
			raise Exception(f"No init method defined at {template_class.__name__}")
  
		# __init__ function of component
		def default_init_func(self, object=None, **kwargs):
			self.__kwargs = kwargs
     
			if not object:
				return	
	
			self.object = object
			self.screen = object.screen
   
			if set_kwargs_as_attr:
				for key, value in kwargs.items():
					setattr(self, key, value)
     
			# calls load activation function

			self.__activate = lambda: activation_func(self)
			self.__desactivate = lambda: desactivation_func(self)
			self.__remove = lambda: remove_func(self)

			load_activation_func(self)

			Component.__init__(self)
			self.init(**kwargs)
	
		# __call__ function of component
		def default_call_func(self, object):
			self.__init__(object, **self.__kwargs)
	
		if not template_class.__dict__.get("remove"):
			template_class.remove = lambda: None
	
		# set functions
		template_class.__init__ = default_init_func
		template_class.__call__ = default_call_func
  
		# add default functions for activation/desactivation in case they are not defined
		if not template_class.__dict__.get("activate"):
			template_class.activate = lambda self: None

		if not template_class.__dict__.get("desactivate"):
			template_class.desactivate = lambda self: None
   
	
		return template_class
    
			