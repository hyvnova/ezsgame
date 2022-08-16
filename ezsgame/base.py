from typing import Callable, List
import pygame as pg, random, time, os
from .objects import Size, Pos, Gradient, Object, resolve_color, Image
from .global_data import DATA, on_update

class Screen:
    __slots__ = "size", "pos", "title", "icon", "depth", "vsync", "fullscreen", "resizable", "color", "surface", "clock", "show_fps", "delta_time", "fps", "events", "time"
    
    # check if an istance of Screen is created
    is_created: bool = False

    def __new__(cls, *args, **kwargs) -> 'Screen':
        r'''
        #### Creates a new Screen instance if it doesn't exist
        '''
        if not cls.is_created:
            Screen.is_created = True
            return object.__new__(Screen)

        else:
            return DATA.screen

    def __init__(self, size: list = [720, 420], title: str = "", icon: str = "", fps: int = 60,
                 show_fps: bool = False, vsync: bool = False, depth: int = 32, color="black", fullscreen: bool = False,
                 resizable: bool = False):

        self.size = Size(*size)
        self.pos = Pos(0, 0)
        self.title = title
        self.icon = icon
        self.vsync = vsync
        self.fullscreen = fullscreen
        self.resizable = resizable
        self.color = color
        self.fps = fps
        self.depth = depth
        self.show_fps = show_fps
        self.delta_time = 0
        
        self.load_icon(icon)

        # init screen
        self.__init()


    def __str__(self):
        return "<Screen>"

    # -----------------------------------------------------------------------------

    def load_icon(self, icon: str):
        r'''
        #### Loads an icon for the screen
        - `icon` :  path to the icon
        '''
        self.icon = icon
        if icon == "":
            try:
                path = os.path.join(os.path.dirname(
                    __file__), "assets", "img", "icon.jpg")
                self.icon = path
                pg.display.set_icon(pg.image.load(self.icon))

            except FileNotFoundError:
                pass

        return self

    def shake(self, force=5):
        r'''
        #### Shakes the screen
        - `force` : force of the shake
        '''
        if force <= 0:
            return

        force = int(force)
        x, y = self.surface.get_rect().center
        x = random.randint(-force, force)
        y = random.randint(-force, force)
        self.surface.blit(self.surface, (x, y))
        return self

    def get_fps(self):
        r'''
        #### Returns the current screen FPS
        '''
        return self.clock.get_fps()

    def check_events(self):
        r'''
        #### Checks and Manage the events, should be called in the main loop
        '''
        TimeHandler.check()
        EventHandler.check()

    @staticmethod
    def mouse_pos():
        r'''
        #### Returns the mouse position
        '''
        return pg.mouse.get_pos()

    def wait(self, time: int):
        r'''
        #### Waits for a certain amount of time
        - `time` : time to wait for, in milliseconds
        '''
        pg.time.wait(time)

    def __resolve_size(self, size: list):
        if self.fullscreen:
            self.__size = Size(size)
            self.size = pg.display.list_modes()[0]
            return

        else:
            # returns to size before fullscreen
            try:
                self.size = self.__size
                return
            except:
                pass

        if size == []:
            raise Exception("You must specify a size for the screen")

        elif len(size) == 1:
            if size[0] in ("max", "full", "100%"):
                self.size = pg.display.list_modes()[0]
            else:
                raise Exception(
                    "Screen size should \"max\" || \"full\" or list [width, height] ")

        elif len(size) == 2:
            if size[0] in ("max", "full", "100%"):
                self.size[0] = pg.display.list_modes()[0][0]
            elif size[1] in ("max", "full", "100%"):
                self.size[1] = pg.display.list_modes()[0][1]
            else:
                self.size = Size(size[0], size[1])

    def __init(self):
        r'''
        #### Initializes the screen, is called automatically
        '''

        pg.init()
        self.__resolve_size(self.size)

        if self.resizable and self.fullscreen:
            raise ValueError(
                "You can't resize and fullscreen at the same time")

        display_type = 0
        if self.fullscreen:
            display_type = pg.FULLSCREEN

        elif self.resizable:
            display_type = pg.RESIZABLE

        self.surface = pg.display.set_mode(
            self.size, display_type, self.depth, 0, self.vsync)

        pg.display.set_caption(self.title)
        if self.icon != "":
            pg.display.set_icon(pg.image.load(self.icon))
        self.clock = pg.time.Clock()

        self.size = Size(self.size)
        
        # globalize time and event handlers
        DATA.TimeHandler = TimeHandler
        DATA.EventHandler = EventHandler
        
        # set screen globaly
        DATA.screen = self
        
    def update(self):
        r'''
        #### Updates the screen
        '''

        if self.show_fps:
            pg.display.set_caption(
                f"{self.title}  FPS : " + f"{int(self.clock.get_fps())}")

        pg.display.update()
        self.delta_time = self.clock.tick(self.fps) / 1000

        # call on update events
        for func in on_update():
            func()

    def quit(self):
        r'''
        #### Quits the game/App  (Closes/Ends the window)
        '''
        pg.quit()
        quit()

    def fill(self, color=None, pos: list = [0, 0], size: list = [0, 0]):
        r'''
        #### Fill the screen with a `color` or `gradient`
        - `color` : color to fill the screen with, or  `Gradient` or `Image`  (Optional)
        - `pos` : position of the fill start (Optional)
        - `size` : size of the fill (Optional)
        '''
    
        color = self.color if color == None else color
        
        if size == [0, 0]:
            size = self.size

        if isinstance(color, Gradient) or isinstance(color, Image):
            color.draw()

        else:
            color = resolve_color(color)
            pg.draw.rect(self.surface, color, pg.Rect(pos, size))
        
    
    def toggle_fullscreen(self):
        r'''
        #### Toggles the fullscreen mode
        '''
        self.fullscreen = not self.fullscreen
        self.__init()

# EVENT HANDLING ----------------------------------------------------------------------------------------------------


class Event:
    __slot__ = "event_type", "event_name", "callback", "object", "name"
    
    def __init__(self, event_type, event_name, callback: Callable, object: Object = None, name: str = "Default", **kwargs):
        self.type = event_type
        self.event_name = event_name
        self.callback = callback
        self.object = object
        self.name = name

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __contains__(self, item):
        return item in self.__dict__.keys()

    def __call__(self, **kwargs):
        try:
            self.callback(**kwargs)
        except Exception as e:
            self.callback()


class EventList(list):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_by_type(self, event_type) -> List[Event]:
        return [event for event in self if event.type == event_type]

    def get_by_name(self, event_name) -> Event:
        lst = [event for event in self if event.event_name == event_name]
        return lst[0] if lst else None

    def replace(self, name: str, new_event: Event) -> None:
        for i, event in enumerate(self):
            if event.name == name:
                self[i] = new_event

    def remove(self, *names) -> None:
        for name in names:
            for i, event in enumerate(self):
                if event.name == name:
                    del self[i]

    def add(self, event: Event):
        # if event already exists, replace it
        if self.get_by_name(event.name):
            self.replace(event.name, event)

        # otherwise, add it
        else:
            self.append(event)


class EventHandler:
    r'''
    - Manages events on the program 
    '''
    
    events = EventList()
    to_remove: List[str] = []
    to_add: List[Event] = []

    __ezsgame_events = ("update",)

    def check():
        # gets widnow events
        events = pg.event.get()

        # removes events
        for name in EventHandler.to_remove:

            for event in EventHandler.events:
                if event.name == name:
                    EventHandler.events.remove(event)
                    break

            # if is ezsgame event
            else:
                # removes event from DATA so it won't be called anymore
                if name in DATA.on_update:
                    del DATA.on_update[name]

        EventHandler.to_remove.clear()

        # adds events
        for event in EventHandler.to_add:

            # if is ezsgame event
            if event.type == "ezsgame":

                # MANAGE EZSGAME EVENTS

                # on update event
                if event.event_name == "update":
                    on_update(event.name, event.callback)

            # if is a event
            else:
                EventHandler.events.add(event)

        EventHandler.to_add.clear()

        # EVENT MANAGEMENT -------------------------------------------------------------------------------------------
        for ev in events:
            # ev : event to process

            # quit event (cannot be event listener)
            if ev.type == pg.QUIT:
                for event in EventHandler.events.get_by_type(pg.QUIT):
                    event.callback()

                Screen().quit()

            # Manages custom events
            for event in EventHandler.events.get_by_type("custom"):
                event_args = {
                    "key": ev.key if ev.__dict__.get("key") else None,
                    "unicode": ev.unicode if ev.__dict__.get("unicode") else None,
                    "type": ev.type,
                    "button": ev.button if ev.__dict__.get("button") else None,
                    "is_hovering": EventHandler.is_hovering(event["object"]) if "object" in event else False
                }

                event(**event_args)

            #  EVENT LOOP (managing events)
            for event in EventHandler.events.get_by_type(ev.type):

                # if is event listener (uses a object)
                is_event_listener = event.object is not None
                is_hovering = False

                if is_event_listener:
                    is_hovering = EventHandler.is_hovering(event.object)

                    # if is not hovering and event is not unhover then skip
                    if not is_hovering and not event.event_name == "unhover":
                        continue

                # function to reduce code, function decides whaterver callback should called or not
                def callback():
                    if is_event_listener:
                        # events that require be hovering
                        if is_hovering and event.object.visible:
                            event.callback()

                    # if is not event listener is base event, just call callback
                    else:
                        event.callback()

                # mouse events
                if ev.type == pg.MOUSEBUTTONDOWN:
                    # mouse wheel up
                    if event.event_name == "mousewheelup" and ev.button == 4:
                        callback()
                        continue

                        # mouse wheel down
                    elif event.event_name == "mousewheeldown" and ev.button == 5:
                        callback()
                        continue
                
                    # right mouse button
                    elif event.event_name == "rightclick" and ev.button == 3:
                        callback()
                        continue
                            
                    # click, mousedown or leftclick
                    elif event.event_name in ("click", "mousedown", "leftclick") and ev.button == 1:
                        callback()
                        continue
                    

                # hover events
                elif ev.type == pg.MOUSEMOTION:
                    if event.event_name == "unhover":
                        if not is_hovering:
                            event.callback()
                            continue

                    else:
                        callback()
                        continue

                # mouse up events
                elif ev.type == pg.MOUSEBUTTONUP:
                    if event.event_name == "mouseup" or event.type == pg.MOUSEBUTTONUP:
                        event.callback()

                    else:
                        callback()

                elif "key" in event:
                    if event.key == ev.key:
                        event(key=ev.key, unicode=ev.unicode)
                        continue

                # base on key event keydown or keyapp
                elif event.type in (pg.KEYDOWN, pg.KEYUP):
                    event(key=ev.key, unicode=ev.unicode)

                # any event that matchess current window event
                else:
                    callback()

    def add_event(event: str, object: Object, callback, name: str = "Default"):
        r'''
        #### Adds a event listener to a object
        - `event` : event to be added 
                - Events : `click`, `hover`, `unhover`, `unclick`.
        - `name` : name of the event 
        - `object` : object to be added to the event 
        - `callback` : function to be called when the event is triggered
        '''
        
        event, event_type = EventHandler._convert_to_pgevent(event)
        
        if name == "Default":
            name = f"{event}.{object.id}.{len(EventHandler.events)}"

        EventHandler.to_add.append(
            Event(event_type, event, callback, object, name))

    def remove_event(name: str):
        f'''
        #### Removes an event from the event list so it won't be called anymore
        -  `name` : name of the event to be removed 
        '''
        EventHandler.to_remove.append(name)

    def is_hovering(object: Object) -> bool:
        r'''
        #### Checks if the mouse is hovering over the object
        - `object` : object to check if the mouse is hovering over it
        '''
        mouse_pos = pg.mouse.get_pos()
        box = object._get_collision_box()

        if mouse_pos[0] > box[0][0] and mouse_pos[0] < box[1][0]:
            if mouse_pos[1] > box[0][1] and mouse_pos[1] < box[2][1]:
                return True

        return False

    def on_event(event: str, callback, name: str = "Default"):
        r'''
        #### Adds a `Base Event` to the event list, Calls function when event is triggered. 
        - `event`: event to be added 
                - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`, `update`
        -  `callback`: function to be called when the event is triggered ``function``
        - `name`: name of event (optional)
        '''
        
        name = f"base_event.{event}.{len(EventHandler.events)}" if name == "Default" else name

        # if is ezsgame event
        if event in EventHandler.__ezsgame_events:
            EventHandler.to_add.append(
                Event("ezsgame", event, callback, None, name))
            return

        event, event_type = EventHandler._convert_to_pgevent(event)

        EventHandler.to_add.append(
            Event(event_type, event, callback, None, name))

    def on_key(type: str, keys: list, callback, name: str = "Default"):
        r'''
        #### Calls function when key event is triggered.
        -  `type`: type of `Event` to be added
                        - Events : `down` (when key is down), `up` (when key released)
        - `keys`: keys to be added to the event 
        -  `callback`:  function to be called when the event is triggered 
        - `name`: name of event (optional)
        '''
        types = {
            "down": pg.KEYDOWN,
            "up": pg.KEYUP
        }

        event_type = types.get(type, None)

        if not event_type:
            raise ValueError("Invalid type: ", type)

        for key in keys:
            if key.lower() == "enter":
                key = "RETURN"

            elif len(key) > 1:
                key = key.upper()

            k = eval("pg.K_" + key)

            name = f"{key}_{type}_{len(EventHandler.events)}" if name == "Default" else name

            EventHandler.to_add.append(
                Event(event_type, k, callback, None, name, key=k))

    def custom_event(callback, object=None, name: str = "Default"):
        r'''
        #### Creates a custom event. *[Decorator]*
        - `callback` : function to be called with event parameters
        - `object` : object to check if is hovering, if you need `is_hovering` (Optional)
        - `name`: name of event (optional)
        '''

        name = f"custom_event.{name}.{len(EventHandler.events)}" if name == "Default" else name

        EventHandler.to_add.append(
            Event("custom", "custom", callback, object, name))

    def _convert_to_pgevent(event):
        if event in EventHandler.__ezsgame_events:
            return event

        event = event.lower().replace(" ", "").replace("_", "")

        evs = {
            "hover": pg.MOUSEMOTION,
            "click": pg.MOUSEBUTTONDOWN,
            "rightclick": pg.MOUSEBUTTONDOWN,
            "leftclick": pg.MOUSEBUTTONDOWN,
            "mousedown": pg.MOUSEBUTTONDOWN,
            "mouseup": pg.MOUSEBUTTONUP,
            "unhover": pg.MOUSEMOTION,
            "unclick": pg.MOUSEBUTTONUP,
            "keydown": pg.KEYDOWN,
            "keyup": pg.KEYUP,
            "mousewheelmotion": pg.MOUSEWHEEL,
            "mousemotion": pg.MOUSEMOTION,
            "quit": pg.QUIT,
            "mousebuttondown": pg.MOUSEBUTTONDOWN,
            "mousebuttonup": pg.MOUSEBUTTONDOWN,
            "mousewheelup": pg.MOUSEBUTTONDOWN,
            "mousewheeldown": pg.MOUSEBUTTONDOWN
        }

        if event not in evs:
            raise Exception("Event type not found", event)
        
        return (event, evs[event])

# Time Handler ---------------------------------------------------------------------------------------------------------
class Interval:
    __slots__ = "time", "callback", "name", "last_call"
    
    def __init__(self, time: float, callback: Callable, last_call: float, name: str = "Default"):
        self.time = time
        self.callback = callback
        self.name = name
        self.last_call = last_call

class TimeHandler:
    r'''
    - Handles the time events
    '''

    intervals: List[Interval] = []
    to_remove: List[str] = []
    to_add: List[Interval] = []

<<<<<<< HEAD
    def add(call_time: int, callback, name: str = "Default"):
        r'''
        #### Adds a `interval` that will be called every `time` milliseconds
        - `name` : name of the event 
        - `time` : amount of time in milliseconds that the event will be called after
        - `callback` : function to be called when the event is triggered 
        '''

        name = f"{len(TimeHandler.intervals)}.{call_time}" if name == "Default" else name

        TimeHandler.to_add.append(Interval(call_time, callback, 0, name)) 

    def remove(name: str):
        r'''
        #### Removes an `interval` from the event list so it won't be called anymore
        - `name` : name of the event to be removed 
        '''
        TimeHandler.to_remove.append(name)

    def check():
        r'''
        #### Manages the time events
        '''
        # removing intervals
        for name in TimeHandler.to_remove:

            if name in TimeHandler.intervals:
                del TimeHandler.intervals[name]

        TimeHandler.to_remove.clear()

        # adding intervals
        TimeHandler.intervals.extend(TimeHandler.to_add)
       
        TimeHandler.to_add.clear()

        # Checking  Intervals
        
        current_time = pg.time.get_ticks()
        for interval in TimeHandler.intervals:
            
            if current_time - interval.last_call >= interval.time:
                interval.callback()
                interval.last_call = time.time()

# time decorators  ------------------------------------------------------------
def add_interval(call_time: int, name: str = "Default") -> Callable:
    r'''    
    - Adds an `interval` to the time handler, calls the function every `time` milliseconds
    - `time` : time in milliseconds
    - `name` : name of the interval (Optional)
    '''
    def wrapper(func):
        TimeHandler.add(call_time, func, name)
        return func

    return wrapper

def remove_interval(name: str) -> None:
    r'''
    #### Removes an `interval` from the time handler
    - `name` : name of the interval
    '''
    TimeHandler.remove(name)


# event decorators ------------------------------------------------------------
def on_key(type: str, keys: list, name: str = "Default") -> Callable:
    r'''
    #### Calls the function when the key event is triggered
    - `type` : type of the event. `up` or `down`
            - Event types : `up` (when the key is released), `down` (when the key is pressed)
    - `keys` : key/keys to listen to
    - `name` : name of the event (Optional) 
    '''
    if not isinstance(keys, list):
        keys = [keys]

    def wrapper(func):
        EventHandler.on_key(type, keys, func, name)
        return func

    return wrapper

def add_event(event: str, object: Object, name: str = "Default") -> Callable:
    r'''
    #### Adds an event listener to an object
    - `event` : event to listen to
    - `object` : object that will be "listening"
    - `name` : name of the event (Optional)
    '''

    def wrapper(func):
        EventHandler.add_event(event, object, func, name)
        return func

    return wrapper

def on_event(event: str, name: str = "Default") -> Callable:
    r'''
    #### Calls funcion when the event is triggered, (Base Event)
    - `event` : event to listen to
            - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`
    - `name` : name of the event (Optional)
    '''

    if name == "Default":
        name = f"base_event.{event}.{len(EventHandler.events)}" if name == "Default" else name

    def wrapper(func):
        EventHandler.on_event(event, func, name)
        return func

    return wrapper

def custom_event(object=None, name: str = "Default") -> Callable:
    r'''
    #### Adds a function as custom event
    - `object` : object to check if is hovering, if you need `is_hovering` (Optional)
    - `name` : name of the event (Optional)
    '''
    def wrapper(func):
        EventHandler.custom_event(func, object, name)
        return func

    return wrapper

def remove_event(name: str):
    r'''
    #### Removes an event from the event handler
    - `name` : name of the event
    '''
    EventHandler.remove_event(name)

get_mouse_pos = lambda: Pos(pg.mouse.get_pos())
=======
	def remove(self, name:str):
		r'''
		#### Removes an `interval` from the event list so it won't be called anymore
		- `name` : name of the event to be removed 
		'''
		self.to_remove.append(name)
		
	def check(self):
		r'''
		#### Manages the time events
		'''
		for name in self.to_remove:
			if name in self.intervals:
				del self.intervals[name]
		self.to_remove = []
				
		for item in self.to_add:
			self.intervals[item[0]] = item[1]
		self.to_add = []
		
		for value in self.intervals.values():
			if t.time() - value["last_call"] >= value["time"]:
				value["last_call"] = t.time()
				value["callback"]()
				   
def flat(arr, depth=1):
	r'''
	Flattens a list
	[1,2,[3],4] -> [1,2,3,4]
	'''
	if depth == 0:
		return arr
	else:
		return [item for sublist in arr for item in flat(sublist, depth - 1)]
>>>>>>> 601d0e9277ee615fb37c4788399a74d1a37926ef
