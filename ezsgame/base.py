import pygame as pg, random, time as t
from ezsgame.objects import Size, Gradient, random_color, Object, PRect, resolve_color
from ezsgame.global_data import DATA

class Screen:
    def __init__(self, size : list = [720, 420], title : str = "", icon : str = "", fps : int = 60, 
                 show_fps : bool = False, vsync:bool = False, depth:int=32, color="black", fullscreen:bool=False,
                 resizable:bool=False):
        
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
        
        self.load_icon(icon)
             
        self.events = EventHandler()
        self.time = TimeHandler()

        # init screen
        self.init()
        
        # Set screen globally
        DATA(screen=self)
        
    def __str__(self):
        return "<Screen>"
    
    
    # time decorators  ------------------------------------------------------------
    def add_interval(self, time:int, name:str = "Default"):
        r'''    
        - Adds an `interval` to the time handler, calls the function every `time` milliseconds
        - `time` : time in milliseconds
        - `name` : name of the interval (Optional)
        '''                
        def wrapper(func):
            self.time.add(time, func, name)
            return func
            
        return wrapper  
    
    def remove_interval(self, name : str):
        r'''
        #### Removes an `interval` from the time handler
        - `name` : name of the interval
        '''
        self.time.remove(name)
    
    # -----------------------------------------------------------------------------
    
    # event decorators ------------------------------------------------------------
    def on_key(self, type:str, keys : list, name:str = "Default"):
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
            self.events.on_key(type, keys, func, name)
            return func
        
        return wrapper
           
    def on_event(self, event:str, name:str = "Default"):
        r'''
        #### Calls funcion when the event is triggered, (Base Event)
        - `event` : event to listen to
            - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`
        - `name` : name of the event (Optional)
        '''
            
        if name == "Default":
            name = f"base_event.{event}.{len(self.events.base_events)}" if name == "Default" else name
        
        def wrapper(func):
            self.events.on_event(event, func, name)
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
        #### Loads an icon for the screen
        - `icon` :  path to the icon
        '''
        self.icon = icon
        if icon == "":
            self.icon = "ezsgame/assets/img/icon.jpg"
        pg.display.set_icon(pg.image.load(self.icon))
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
        self.time.check()
        self.events.check()
        DATA.drawn_objects = []

    @staticmethod
    def mouse_pos():
        r'''
        #### Returns the mouse position
        '''
        return pg.mouse.get_pos()

    def wait(self, time : int):
        r'''
        #### Waits for a certain amount of time
        - `time` : time to wait for, in milliseconds
        '''
        pg.time.wait(time)
            
    def div(self, axis : str, q : int, size : list = None):
        r'''
        #### Returns a list of division points of the screen in the given axis
        
        - `axis` : axis to divide the screen in (`x` or `y`)
        - `q` : number of divisions
        - `size` : Size of where to divide the screen, works as a delimiter (Optional)
        '''
        
        _size = size if size != None else self.size
        
        _size = Object(pos=[0,0], size=_size).get_size()
        
        divs = []
        if axis == "x":
            step = _size[0] / q
            
            for i in range(q):
                divs.append([round(i * step, 1), round((i + 1) * step, 1)])
                
                # if overflows 
                if divs[-1][1] > _size[0]:
                    break
                
        elif axis == "y":
            step = _size[1] / q

            for i in range(q):
                divs.append([round(i * step, 1), round((i + 1) * step, 1)])
        
                # if overflows
                if divs[-1][1] > _size[1]:
                    break
                
        return divs
    
    def resolve_size(self, size : list):
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
                raise Exception("Screen size should \"max\" || \"full\" or list [width, height] ")
            
        elif len(size) == 2:
            if size[0] in ("max", "full", "100%"):
                self.size[0] = pg.display.list_modes()[0][0]    
            elif size[1] in ("max", "full", "100%"):
                self.size[1] = pg.display.list_modes()[0][1] 
            else:
                self.size = Size(size[0], size[1])
        
    def init(self):
        r'''
        #### Initializes the screen, is called automatically
        '''
        
        pg.init()
        self.resolve_size(self.size)
                        
        if self.resizable and self.fullscreen:
            raise ValueError("You can't resize and fullscreen at the same time")
        
        display_type = 0
        if self.fullscreen:
            display_type = pg.FULLSCREEN
            
        elif self.resizable:
            display_type = pg.RESIZABLE    
    
        self.surface = pg.display.set_mode(self.size, display_type, self.depth, 0, self.vsync)                     
                       
        pg.display.set_caption(self.title)
        if self.icon != "":
            pg.display.set_icon(pg.image.load(self.icon))
        self.clock = pg.time.Clock()
        
        self.size = Size(self.size)
        
    def update(self):
        r'''
        #### Updates the screen
        '''
        
        if self.show_fps:
            pg.display.set_caption(f"{self.title}  FPS : " + f"{int(self.clock.get_fps())}")
        
        pg.display.update()
        self.clock.tick(self.fps)
        
    def quit(self):
        r'''
        #### Quits the game/App  (Closse/Ends the window)
        '''
        
        pg.quit()
        quit()

    def fill(self, color = None, pos : list=[0, 0], size:list=[0, 0]):
        r'''
        #### Fill the screen with a `color` or `gradient`
        - `color` : color to fill the screen with, or a `Gradient`  (Optional)
        - `pos` : position of the fill start (Optional)
        - `size` : size of the fill (Optional)
        '''
        color = self.color if color == None else color
        if size == [0, 0]:
            size = self.size
        
        if isinstance(color, Gradient):
            for obj in color.objs:
                obj.draw()      
        else:
            color = resolve_color(color)
            pg.draw.rect(self.surface, color, pg.Rect(pos, size))
        
    def grid_div(self, cols:int=3, rows:int=3, transpose:bool=False):
        r'''
        #### Returns the division of the screen into a grid -> `[[x, y, w, h], [x, y, w, h], ...]`
        - `cols` : number of columns
        - `rows` : number of rows
        - `transpose` : if True, the grid will be transposed
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
    
    def toggle_fullscreen(self):
        r'''
        #### Toggles the fullscreen mode
        '''
        self.fullscreen = not self.fullscreen
        self.init()
        

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
            fill_color = resolve_color(fill_color)
                        
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


# Manager Objects
        
def add_args(func, **kwargs):
    def inner(*_, **__):
        try:
            return func(**kwargs)
        except Exception as e:
            return func()
    return inner
    
class EventHandler:
    r'''
    - Manages events on the app 
    '''
    def __init__(self):
        self.events  = {}
        self.base_events = {}
        self.to_remove = {"events": [], "base_events": []}
        self.to_add = {"events": [], "base_events": []}
                                            
    def check(self):
        event = self._get_events()
        
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
            
        names = []
        for item in self.to_add["base_events"]:
            
            if item[1]["name"] not in names:
                self.base_events[item[0]].append(item[1])
                names.append(item[1]["name"])
        
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
                        if base_event == (pg.KEYDOWN or pg.KEYUP):
                            add_args(item["callback"], key=ev.key, unicode=ev.unicode)()
                        
                        else:
                            item["callback"]()
                           
            # STORED EVENTS --------------------------------------------------------------------------------
            for key, value in self.events.items():
                if value["type"] == ev.type:
                    if "key" in value:
                        if value["key"] == ev.key:
                            add_args(value["callback"], key=ev.key, unicode=ev.unicode)()
                    
                    else:
                        if value.get("evname",None) == "unhover":
                            if not self.is_hovering(value["object"]) and value["object"]._id in DATA.drawn_objects:
                                self.events[key]["callback"]()
                        else:               
                            if self.is_hovering(value["object"]) and value["object"]._id in DATA.drawn_objects:
                                value["callback"]()
                                            
    def add_event(self, event:str, object:Object, callback, name:str="Default"):
        r'''
        #### Adds a event listener to a object
        - `event` : event to be added 
            - Events : `click`, `hover`, `unhover`, `unclick`.
        - `name` : name of the event 
        - `object` : object to be added to the event 
        - `callback` : function to be called when the event is triggered
        '''
     
        event = event.lower()
        event_ = self._convert_to_pgevent(event)
        
        if name == "Default":
            name = f"{event}.{object._id}.{len(self.events)}"
            
        self.to_add["events"].append([name, {"type": event_, "object": object, "callback": callback, "evname" : event}])

    def remove_event(self, name:str):
        f'''
        #### Removes an event from the event list so it won't be called anymore
        -  `name` : name of the event to be removed 
        '''
        self.to_remove["events"].append(name)

    def is_hovering(self, object:Object) -> bool:
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
            
    def _get_events(self):
        f"""
        #### Returns Current Events, Is called automatically
        """
        # return current event
        return pg.event.get()
    
    def on_event(self, event : str, callback , name:str = "Default"):
        r'''
        #### Adds a `Base Event` to the event list, Calls function when event is triggered. 
        - `event`: event to be added 
            - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`
        -  `callback`: function to be called when the event is triggered ``function``
        - `name`: name of event (optional)
        '''
        event = event.lower()
    
        event_ = self._convert_to_pgevent(event)
        
        if event not in self.base_events:
            self.base_events[event_] = []
        name = f"base_event.{event}.{len(self.base_events)}" if name == "Default" else name
        
        self.to_add["base_events"].append([event_, {"type": event_, "callback": callback, "name":name}])
        
    def remove_base_event(self, name : str):
        r'''
        #### Removes a `Base Event` from the event list, so it won't be called anymore
        - `name` : name of the event to be removed
        '''
        
        self.to_remove["base_events"].append(name)
                   
    def on_key(self, type : str, keys : list, callback, name:str = "Default"):
        r'''
        #### Calls function when key event is triggered.
        -  `type`: type of `Event` to be added
                - Events : `down` (when key is down), `up` (when key released)
        - `keys`: keys to be added to the event 
        -  `callback`:  function to be called when the event is triggered 
        - `name`: name of event (optional)
        '''
        types = {
            "down" : pg.KEYDOWN,
            "up" : pg.KEYUP
        }        
        t = types.get(type, None)
        if not t:
            raise ValueError("Invalid type: ", type)
         
        for key in keys:    
            if key.lower() == "enter":
                key = "RETURN"
                
            elif len(key) > 1:
                key = key.upper()

            
            k = eval("pg.K_" + key)
            
            name = f"{key}_{type}_{len(self.events)}" if name == "Default" else name
        
            self.events[name] = {"type": t, "key": k, "callback": callback}
            
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

    def add(self, time : int, callback, name:str ="Default"):
        r'''
        #### Adds a `interval` that will be called every `time` milliseconds
        - `name` : name of the event 
        - `time` : amount of time in milliseconds that the event will be called after
        - `callback` : function to be called when the event is triggered 
        '''
        name = f"{len(self.intervals)}.{time}" if name == "Default" else name
        self.to_add.append([name, {"callback": callback, "time": time//1000, "last_call": t.time()}])

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