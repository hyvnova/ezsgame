import pygame as pg, random, time as t
from ezsgame.objects import Size, text_to_color, Gradient, random_color, Object, PRect
from functools import wraps
import concurrent.futures as futures


class Screen:
    def __init__(self, size : list = [720, 420], title : str = "", icon : str = "", fps : int = 60, 
                 show_fps : bool = False, vsync = False, depth=32, color="black", fullscreen=False, resizable=False):
        self.size = Size(*size)
        self.title = title
        self.icon = icon
        self.surface = None
        self.vsync = vsync
        self.fullscreen = fullscreen
        self.resizable = resizable
        self.clock = None
        self.color = color
        self.fps = fps
        self.depth = depth
        self.show_fps = show_fps
        self.resolve_size(size)        
        self.events = EventHandler(self)
        self.time = TimeHandler()
        self.load_icon(icon)

        # init screen
        self.init()
  
        
    def __str__(self):
        return "<Screen>"
    
    # time decorators  ------------------------------------------------------------
    def add_interval(self, *args, **kwargs):
        r'''    
        Add an interval to the time handler, call the function every <time> seconds
        @params : time (int) : time in milliseconds
        @params : name (str) : name of the interval
        '''
        
        time = kwargs.get("time", None)
        if time == None:
            time = args[0]
        if time == None:
            raise Exception("Time must be specified")
        

        name = kwargs.get("name", "Default")
        if name == "Default":
            name = args[1] if len(args) > 1 else "Default"
        name = f"{len(self.time.intervals)}.{time}" if name == "Default" else name
        
        def wrapper(func):
            self.time.add(time, func, name)
        return wrapper  
    
    def remove_interval(self, name : str):
        r'''
        Remove an interval from the time handler
        @params : name (str) : name of the interval
        '''
        self.time.remove(name)
    
    # -----------------------------------------------------------------------------
    
    # event decorators ------------------------------------------------------------
    def on_key(self, **kwargs):
        r'''
        Calls the function when the key event is triggered
        @params : type (str) : type of the event (up, down)
        @params : keys (list) : key/keys to listen to ["w", "a", "s", "d"]
        '''
        type = kwargs.get("type", None)
        keys = kwargs.get("keys", None)
            
        if type == None:
            raise Exception("Event Type must be specified")
        
        if keys == None:
            raise Exception("Keys must be specified")
        
        if not isinstance(keys, list):
            keys = [keys]
        
        def decorate(fn):
            self.events.on_key(type, keys, fn)
            @wraps(fn)
            def wrapper(*args, **kwargs):
                print(fn.__name__)
                return fn(*args, **kwargs)
            return wrapper
        return decorate
       
       
    def on(self, *args, **kwargs):
        r'''
        Call funcion when the event is triggered
        @params : event (str) : event to listen to
        '''
        
        event = kwargs.get("event", None)

        if event == None:
            event = args[0]
            
        if event == None:
            raise Exception("Event type must be specified")
            
        name = kwargs.get("name", "Default")
        name = f"base_event.{event}.{len(self.events.base_events)}" if name == "Default" else name
        
        def wrapper(func):
            self.events.on(event, func, name)
            return func
        return wrapper

    # -----------------------------------------------------------------------------
        
    def delta_time(self):
        r'''
        Returns the delta time since the last frame
        '''
        return self.clock.get_time()
         
    def load_icon(self, icon : str):
        r'''
        Loads an icon for the screen
        @params : icon (str) : path to the icon
        '''
        self.icon = icon
        if icon == "":
            self.icon = "ezsgame/assets/img/icon.jpg"
        pg.display.set_icon(pg.image.load(self.icon))
        return self

    def shake(self, force=5):
        r'''
        Shake the screen
        @params : force (int) : force of the shake
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
        Returns the current FPS
        '''
        return self.clock.get_fps()

    def check_events(self):
        r'''
        Check and Manage the events, should be called in the main loop
        '''
        self.events.check(self.events.get(), self)
        self.time.check()

    @staticmethod
    def mouse_pos():
        r'''
        Returns the mouse position
        '''
        return pg.mouse.get_pos()

    def wait(self, time : int):
        r'''
        Wait for a certain amount of time
        @params : time (milliseconds)
        '''
        pg.time.wait(time)
            
    def div(self, axis, q):
        r'''
        Return list of division points of the screen -> [[x1, x2], [x1, x2], ...]
        '''
        divs = []
        if axis == "x":
            # should append [start, end] for each division
            for i in range(q):
                divs.append([round(i * self.size[0] / q, 1), round((i + 1) * self.size[0] / q, 1)])
        elif axis == "y":
            # should append [start, end] for each division
            for i in range(q):
                divs.append([round(i * self.size[1] / q, 1), round((i + 1) * self.size[1] / q, 1)])
            
        return divs
    
    def resolve_size(self, size : list):
        if self.fullscreen:
            self.size = [pg.display.get_surface().get_width(), pg.display.get_surface().get_height()]
            return self
        
        if size == []:
            raise Exception("You must specify a size for the screen")
        elif len(size) == 1:
            if size[0] == "max" or size[0] == "full":
                self.size = pg.display.get_surface().get_size()
            else:
                raise Exception("Screen size should \"max\" || \"full\" or list [width, height] ")
            
        elif len(size) == 2:
            if size[0] == "max" or size[0] == "full":
                self.size[0] = pg.display.get_surface().get_width()
            elif size[1] == "max" or size[1] == "full":
                self.size[1] = pg.display.get_surface().get_height()        
            else:
                self.size = size
        
    def init(self):
        r'''
        Initialize the screen, is called automatically
        '''
        
        pg.init()
                        
        if self.resizable:
            self.surface = pg.display.set_mode(self.size, 0, self.depth, 0, self.vsync, pg.RESIZABLE)
        else:
            self.surface = pg.display.set_mode(self.size, 0, self.depth, 0, self.vsync)
                                           
        pg.display.set_caption(self.title)
        if self.icon != "":
            pg.display.set_icon(pg.image.load(self.icon))
        self.clock = pg.time.Clock()
        
    def update(self):
        r'''
        Update the screen
        '''
        
        if self.show_fps:
            pg.display.set_caption(f"{self.title}  FPS : " + f"{int(self.clock.get_fps())}")
        
        pg.display.update()
        self.clock.tick(self.fps)
        
    def quit(self):
        r'''
        Quit the game/App  (Close/Ends the window)
        '''
        
        pg.quit()
        quit()

    def fill(self, color=None, pos=[0, 0], size=[0, 0]):
        r'''
        Fill the screen with a color or gradient
        '''
        color = self.color if color == None else color
        if isinstance(color, str):
            color = text_to_color(color)

            if size == [0, 0]:
                size = self.size
            pg.draw.rect(self.surface, color, pg.Rect(pos, size))
      

        elif isinstance(color, Gradient):
            for obj in color.objs:
                obj.draw(self)      
                
    def grid_div(self, cols=3, rows=3, transpose=False):
        r'''
        Returns the division of the screen into a grid -> [[x, y, w, h], [x, y, w, h], ...]
        '''
        grid = []
        divs_x = self.div("x", cols)
        box_width = divs_x[-1][0] - divs_x[-2][0]
        divs_y = self.div("y", rows)
        box_height = divs_y[-1][0] - divs_y[-2][0]
        self.grid_size = [rows, cols]
        
        for i in range(cols):
            for j in range(rows):
                if transpose:
                    grid.append([divs_x[j][0], divs_y[i][0], box_width, box_height])
                else:
                    grid.append([divs_x[i][0], divs_y[j][0], box_width, box_height])
        self.grid_space = len(grid)
        self.grid_box_size = [box_width, box_height]
        return grid
    
class IScreen(Screen):
    def __init__(self, size : list = [720, 420], title : str = "", icon : str = "", fps : int = 60, 
                 show_fps : bool = False, objects = [], color : str = "black", depth : int = 0, vsync : bool = False):
        super().__init__(size, title, icon, fps, show_fps, color, depth, vsync)
        self.objects = objects
        self.color = color
        self.depth = depth
        self.vsync = vsync
        self.grid = self.grid_div(cols=3, rows=3)
        self.format_objects()
        self.init()
        
    def grid_positions(self, order=[0,1]):
        pos = []
        for k in range(self.grid_size[order[0]]):
            for j in range(self.grid_size[order[1]]):
               pos.append([k, j]) 
        return pos          
    
    def format_objects(self):
        r'''
        Format the objects in the screen
        '''
        objs = []
        i = 0
        for obj in self.objects:
            if isinstance(obj, Object):
                obj.screen = self
                objs.append({"object": obj, "z-index": i})
                i += 1
            
        self.objects = objs
    
    def run(self, fill_color=None, auto_place=True, grid=[3,3]):
        r'''
        Run the screen
        '''
        self.grid = self.grid_div(*grid)
        fill_color = self.color if fill_color == None else fill_color
        if isinstance(fill_color, str):
            fill_color = text_to_color(fill_color)
                
        while True:
            self.check_events()
            self.fill(fill_color)
            self.draw(auto_place)
            self.update()

    def show_grid(self):
        r'''
        Draws  grid on the screen
        '''
        colors = random_color(len(self.grid))
        c = 0
        for i in self.grid:
            color = colors[c]
            PRect(pos=i[:2], size=i[2:], color=color).draw(self)
            c += 1
   
        return self
     
    def place(self, object, row=0, col=0):     
        r'''
        Place an object in the grid
        '''
        pos = self.grid[(row * 3) + col]
        # center object in the box
        object.pos = [pos[0] + pos[2] / 2 - object.size[0] / 4, pos[1] + pos[3] / 2 - object.size[1] / 4]
   
    def add(self, objects):
        r'''
        Add objects to the screen object list
        '''
        if isinstance(objects, list):
            for obj in objects:
                obj.screen = self
                self.objects.append({"object": obj, "z-index":1})
        elif isinstance(objects, Object):
            objects.screen = self
            self.objects.append({"object": objects, "z-index":1})
        else:
            raise Exception("Object must be a list of objects or an object")    
        
    def draw(self, auto_place=False, objects=None):
        if objects == None:
            objects = self.objects
        else:
            if isinstance(objects, list):
                for obj in objects:
                    self.objects.append({"object": obj, "z-index":1})
                    
            elif isinstance(objects, Object) or isinstance(objects, PRect):
                self.objects.append({"object": objects, "z-index":1})

            else:
                raise Exception("Object must be a list of objects or an object")
            
        if auto_place:
            if len(objects) > self.grid_space:
                raise Exception(f"Not enough space in the grid ({self.grid_space} places) for {len(objects)} objects")
            c = 0
            r = 0
            for obj in objects:
                self.place(obj["object"], r,c)
                c += 1
                if c == self.grid_size[1] * 3:
                    c = 0
                    r += 1
            
        colliding = []
        to_remove = []
        for i in range(len(objects)):
            for j in range(len(objects)):
                if i != j:
                    try:
                        if objects[i]["object"].is_colliding(objects[j]["object"]):
                            colliding.append([{"object": objects[j]["object"], "z-index": objects[j]["z-index"], "index": i},
                                            {"object": objects[j]["object"], "z-index": objects[j]["z-index"], "index": j}])
                            to_remove.append(objects[i])
                            to_remove.append(objects[j])
                    except:
                        pass
                            
        # remove duplicates in to_remove
        to_remove = filter(lambda x: x not in to_remove, to_remove)
  
        for obj in colliding:
            if obj[0]["z-index"] > obj[1]["z-index"]:
                obj[1]["object"].draw(self)
                obj[0]["object"].draw(self)
            
            elif obj[0]["z-index"] == obj[1]["z-index"]:
                if obj[0]["index"] > obj[1]["index"]:
                    obj[1]["object"].draw(self)
                    obj[0]["object"].draw(self)
                else:
                    obj[0]["object"].draw(self)
                    obj[1]["object"].draw(self)
                    
            else:
                obj[0]["object"].draw(self)
                obj[1]["object"].draw(self)
                               
        for obj in objects:
            obj["object"].draw(self)
    
        self.update()
        
def flat(arr, depth=1):
    r'''
    Flatten a list
    [1,2,[3],4] -> [1,2,3,4]
    '''
    if depth == 0:
        return arr
    else:
        return [item for sublist in arr for item in flat(sublist, depth - 1)]
    
def add_args(func, *args, **kwargs):
    def inner(*_, **__):
        try:
            return func(*args, **kwargs)
        except:
            return func()
    return inner
    
class EventHandler:
    r'''
    - Manages events on the app 
    '''
    def __init__(self, screen):
        self.screen = screen
        self.events  = {}
        self.base_events = {}
        self.to_remove = {"events": [], "base_events": []}
        self.to_add = {"events": [], "base_events": []}

                                            
    def check(self, event, screen=None):
        screen = self.screen if screen == None else screen
        self.events = {k:v for k,v in self.events.items() if v != None}
        
        # remove events
        for name in self.to_remove["events"]:
            if name in self.events:
                del self.events[name]
            
        for name in self.to_remove["base_events"]:
            for i in self.base_events:
                for item in self.base_events[i]:
                    if item["name"] == name:
                        self.base_events[i].pop(self.base_events[i].index(item))
                        break
        self.to_remove = {"events": [], "base_events": []}
                    
        # add events
        for item in self.to_add["events"]:
            self.events[item[0]] = item[1]
            
        for item in self.to_add["base_events"]:
            self.base_events[item[0]].append(item[1])
        
        self.to_add = {"events": [], "base_events": []}
        
        for ev in event:
            # BASE EVENTS ----------------------------------------------------------------------------------
            if ev.type == pg.QUIT:
                for i in self.base_events.get(pg.QUIT, ""):
                    if i["type"] == pg.QUIT:
                        i["callback"]()
                        break
                    
                pg.quit()
                quit()
                              
            for base_event in self.base_events:
                if ev.type == base_event:
                    for item in self.base_events.get(base_event, None):
                        if base_event == pg.KEYDOWN:
                            item["callback"] = add_args(item["callback"], key=ev.key, unicode=ev.unicode)
                        item["callback"]()
                           
   
            # STORED EVENTS --------------------------------------------------------------------------------
            for key, value in self.events.items():
                if value["type"] == ev.type:
                    if "key" in value:
                        if value["key"] == ev.key:
                            add_args(value["callback"], key=ev.key, unicode=ev.unicode)()
                    
                    else:
                        if value.get("evname",None) == "unhover":
                            if self.is_hovering(value["object"]) == False:  
                                    self.events[key]["callback"]()
                        else:               
                            if self.is_hovering(value["object"]):
                                value["callback"]()
                                            
    def add_event_listener(self, event, object, callback, name="Default"):
        r'''
        - Adds a event listener to a object
        @param event: event to be added ``str``
            --events : (mousedown or click), hover, unhover, (mouseup or unclick).
        @param name: name of the event ``str``
        @param object: object to be added to the event ``Object``
        @param callback: callback function to be called when the event is triggered ``function``
        '''
     
        event = event.lower()
        event_ = self._convert_to_pgevent(event)
        
        if name == "Default":
            name = f"{event}.{object._id}.{len(self.events)}"
            
        self.to_add["events"].append([name, {"type": event_, "object": object, "callback": callback, "evname" : event}])

    def remove(self, name):
        f'''
        - Removes an event from the event list so it won't be called anymore
        @param name: name of the event to be removed ``str``
        '''
        self.to_remove["events"].append(name)

    def is_hovering(self, object):
        r'''
        - Checks if the mouse is hovering over the object
        @param object: object to be checked ``Object``
        '''
        mouse_pos = pg.mouse.get_pos()
        box = object._get_collision_box()
        
        if mouse_pos[0] > box[0][0] and mouse_pos[0] < box[1][0]:
            if mouse_pos[1] > box[0][1] and mouse_pos[1] < box[2][1]:
                return True
            
        return False
            
    def get(self):
        f"""
        - Return Current Events, should be in the main loop
        """
        # return current event
        return pg.event.get()
    
    def on(self, event, callback, name="Default"):
        r'''
        - Called when event is triggered
        @param event: event to be added ``str``
            --events : quit, mousemotion, mousedown, mouseup, keydown, keyup, mousewheel
        @param callback: callback function to be called when the event is triggered ``function``
        @param name: name of event object, used to removed the event if needed
        '''
        event = event.lower()
    
        event_ = self._convert_to_pgevent(event)
        
        if event not in self.base_events:
            self.base_events[event_] = []
        name = f"base_event.{event}.{len(self.base_events)}" if name == "Default" else name
        
        self.to_add["base_events"].append([event_, {"type": event_, "callback": callback, "name":name}])
        
    def remove_base_event(self, name):
        self.to_remove["base_events"].append(name)
                   
    def on_key(self, type, keys, callback):
        r'''
        - Called when key event is triggered
        @param type: type of event to be added ``str``
            --events : down, up
        @param keys: keys to be added to the event ``list``
        @param callback: callback function to be called when the event is triggered ``function``
        '''
        types = {
            "down" : pg.KEYDOWN,
            "up" : pg.KEYUP
        }
        if type not in types:
            raise Exception(f"{type} is not a valid on_key event type.")
        
        t = types[type]
         
        for key in keys:
            if key.lower() in ["multiply", "minus", "plus", "enter"]:
                key = "KP_" + key.upper()
            elif len(key) > 1:
                key = key.upper()
              
            else:
                key = key.lower()
            
            k = eval("pg.K_" + key)
            self.events[f"{key}_{type}_{len(self.events)}"] = {"type": t, "key": k, "callback": callback}
            
    def _base_event_index(self, type, item):
        for i in range(len(self.base_events[type])):
            if self.base_events[type][i]["name"] == item["name"]:
                return i
                    
    def _convert_to_pgevent(self, event):
        evs  = {
            "hover" : pg.MOUSEMOTION,
            "click" : pg.MOUSEBUTTONDOWN,
            "mousedown" : pg.MOUSEBUTTONDOWN,
            "mouseup" : pg.MOUSEBUTTONUP,
            "unhover" : pg.MOUSEMOTION,
            "unclick" : pg.MOUSEBUTTONUP,
            "keydown" : pg.KEYDOWN,
            "keyup" : pg.KEYUP,
            "mousewheel" : pg.MOUSEWHEEL,
            "mousemotion" : pg.MOUSEMOTION,
            "quit" : pg.QUIT,
            "mousebuttondown" : pg.MOUSEBUTTONDOWN,
            "mousebuttonup" : pg.MOUSEBUTTONDOWN,
            "mousewheelup" : pg.MOUSEBUTTONDOWN
        }
        if event not in evs:
            raise Exception("Event type not found", event)
        return evs[event]
   
class TimeHandler:
    r'''
    - Handles the time events
    '''
    def __init__(self):
        self.intervals = {}
        self.start_time = t.time()
        self.time = 0
        self.to_remove = []
        self.to_add = []

    def add(self, time, callback, name="Default"):
        r'''
        - Adds event that will be called every time the time is reached
        @param name: name of the event ``str``
        @param time: time to be called ``int`` in miliseconds
        @param callback: callback function to be called when the event is triggered ``function``
        '''
        time = time / 1000
        name = f"{len(self.intervals)}.{time}" if name == "Default" else name
        self.to_add.append([name, {"callback": callback, "time": time, "last_call": t.time()}])

    def remove(self, name):
        r'''
        - Removes an event from the event list so it won't be called anymore
        @param name: name of the event to be removed ``str``
        '''
        self.to_remove.append(name)
        
    def check(self):
        r'''
        - Checks if the time is reached and calls the event
        '''
        for name in self.to_remove:
            if name in self.intervals:
                del self.intervals[name]
        self.to_remove = []
                
        for item in self.to_add:
            self.intervals[item[0]] = item[1]
        self.to_add = []
        
        
        for key, value in self.intervals.items():
            if t.time() - value["last_call"] >= value["time"]:
                self.intervals[key]["last_call"] = t.time()
                self.intervals[key]["callback"]()
    
