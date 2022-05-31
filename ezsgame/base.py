import pygame as pg, random, time as t
from ezsgame.objects import Size, Pos, Gradient, Object, resolve_color
from ezsgame.global_data import DATA, get_screen

class Screen:
    def __init__(self, size : list = [720, 420], title : str = "", icon : str = "", fps : int = 60, 
                 show_fps : bool = False, vsync:bool = False, depth:int=32, color="black", fullscreen:bool=False,
                 resizable:bool=False):
        
        self.size = Size(*size)
        self.pos = Pos(0,0)
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
        self.delta_time = 0 
        
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

    def remove_event(self, name : str):
        r'''
        #### Removes an event from the event handler
        - `name` : name of the event
        '''
        self.events.remove_event(name)
        
    def remove_base_event(self, name:str = "Default"):
        r'''
        #### Removes an base event from the event handler
        - `name` : name of the event
        '''
        self.events.remove_base_events(name)
        

    # -----------------------------------------------------------------------------
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
        self.delta_time = self.clock.tick(self.fps) / 1000
        
        
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
        
class Interface:
    def __init__(self, display, grid=None):
        self.display = display
        self.objects = []
        self.current_z_index = 1
        self.screen = get_screen()

        self.__gen_grid(grid if grid else [5,5])
        
    def __gen_grid(self, size):
        if not size or size==[]: 
            size = []           
            length = len(self.objects)
            
            
            d = dict(zip(range(10, 90, 20), range(2, 6)))
            for k,v in d.items():
                if length < k:
                    n = v
                    break
            
            for i in range(2, length //n):
                for x in range(2, length//n):
                    if i*x == length:
                        size = [i, x]
                        break   
        
        self.grid_size = size
        self.grid_space = size[0] * size[1]
        self.grid_box_size = [self.display.size[0]/size[0], self.display.size[1]/size[1]]
        
        self.grid = []
        
        x_values = self.screen.div("x", self.grid_size[0])
        y_values = self.screen.div("y", self.grid_size[1])

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid.append([x_values[i][0], y_values[j][0]])
   
    def add(self, *objects):
        r'''
        #### Adds passed objects to the interface
        '''
        if isinstance(objects[0], list):
            objects = objects[0]
        
        for obj in objects:
            obj.z_index = self.current_z_index
            self.current_z_index += 1
            
            self.objects.append(obj)
            
        return self
            
    def remove(self, *objects):
        r'''
        #### Removes passed objects from the interface
        '''
        for obj in objects:
            self.objects.remove(obj)
                    
    def align(self, direction="row", spacing="auto"):
        r'''
        #### Aligns objects in the interface
        - `direction` : align direction "row" or "column"
        ''' 
        if (direction:= direction.lower()) not in ("row", "column"):
            raise ValueError("Direction must be either 'row' or 'column'")
        
        if isinstance(spacing, str):
            if spacing.lower() == "auto":
                spacing = self.display.size[0] // (self.grid_size[0]//2 * len(self.objects))
                
            else:
                raise ValueError("Spacing must be either 'auto' or a number")
        
        x,y = spacing//2, spacing//2
        
        step = [self.objects[-1].size[0] + spacing,
                self.objects[-1].size[1] + spacing]
        
        for obj in self.objects:
            obj.pos = [x, y]
            if direction == "row":
                if obj.pos[0] + obj.size.width > self.display.pos[0] + self.display.size[0]:
                    x = spacing//2
                    y += step[1]
                    obj.pos = [x, y]  
                    
                    x += step[0]  
                
                else:
                    x += step[0]
                    
            elif direction == "column":
                if obj.pos[1] + obj.size.height > self.display.size.height:
                    x += step[0] + spacing//2
                    y = spacing//2
                    obj.pos = [x, y]    
                    
                    y += step[1]
                    
                else:
                    y += step[1]
            
    def grid_align(self, size=[]):
        r'''
        #### Aligns objects in the interface grid
        - `size` : grid dimensions (Optional)
        ''' 
        self.__gen_grid(size)
                
        # add a grid pos and size to each object
        for i in range(len(self.grid)):
            if len(self.objects) > i:
                self.objects[i].pos = Pos(self.grid[i])
                self.objects[i].size = Size(self.grid_box_size)
                        
    def draw(self):
        r'''
        #### Draws all objects in the interface
        '''
        for obj in self.objects:
            obj.draw()
        
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
                              
            for ev_type in self.base_events.keys():
                if ev.type == ev_type:
                    for i in self.base_events[ev_type]:
                        
                        if ev.type == pg.MOUSEBUTTONDOWN:
                            if i["evname"] == "mousewheelup" and ev.button == 4:
                                i["callback"]()
                            
                            elif i["evname"] == "mousewheeldown" and ev.button == 5:
                                i["callback"]()   
                            
                    
                        elif i["type"] == (pg.KEYDOWN or pg.KEYUP):
                            add_args(value["callback"], key=ev.key, unicode=ev.unicode)()
                    
                        else:
                            i["callback"]()
                           
            # STORED EVENTS --------------------------------------------------------------------------------
            for value in self.events.values():
                if value["type"] == ev.type:
                    
                    # ON key events
                    if "key" in value:
                        if value["key"] == ev.key:
                            add_args(value["callback"], key=ev.key, unicode=ev.unicode)()
                    
                    else:                
                        is_hovering = self.is_hovering(value["object"]) and value["object"].id in DATA.drawn_objects
                        
                        if value.get("evname", "") == "unhover":
                            if not is_hovering:
                                value["callback"]()
                            else:
                                return
                        
                        else:
                            if is_hovering:
                                if ev.type == pg.MOUSEBUTTONDOWN:
                                    if value.get("evname", None) == "mousewheelup" and ev.button == 4:
                                        value["callback"]()
                                
                                    elif value.get("evname", None) == "mousewheeldown" and ev.button == 5:
                                        value["callback"]()                                        
                        
                                else:
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
            name = f"{event}.{object.id}.{len(self.events)}"
            
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
        
        self.to_add["base_events"].append([event_, {"type": event_, "callback": callback, "name":name, "evname":event}])
        
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
            "mousewheelmotion" : pg.MOUSEWHEEL,
            "mousemotion" : pg.MOUSEMOTION,
            "quit" : pg.QUIT,
            "mousebuttondown" : pg.MOUSEBUTTONDOWN,
            "mousebuttonup" : pg.MOUSEBUTTONDOWN,
            "mousewheelup" : pg.MOUSEBUTTONDOWN,
            "mousewheeldown" : pg.MOUSEBUTTONDOWN
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