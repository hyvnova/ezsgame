import pygame as pg, random
from ezsgame.premade import *

class Screen:
    def __init__(self, size : list = [720, 420], title : str = "", icon : str = "", fps : int = 60, 
                 show_fps : bool = False, vsync = False, depth=32, fullscreen=False, color="black"):
        self.size = size
        self.title = title
        self.icon = icon
        self.surface = None
        self.vsync = vsync
        self.clock = None
        self.color = color
        self.fps = fps
        self.depth = depth
        self.show_fps = show_fps
        self.size = [0, 0]
        self.resolve_size(size)        
        self.events = EventHandler(self)
        self.time = TimeHandler()
        self.load_icon(icon)
        self.init()
        
    def __str__(self):
        return "<Screen>"
    def __repr__(self):
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
    def on_key(self, *args, **kwargs):
        r'''
        Calls the function when the key event is triggered
        @params : type (str) : type of the event (keyup, keydown)
        @params : keys (list) : key/keys to listen to ["w", "a", "s", "d"]
        '''
        
        type = kwargs.get("type", None)
        keys = kwargs.get("keys", None)
        
        if type == None:
            type = args[0]
            
        if type == None:
            raise Exception("Event Type must be specified")
        
        if keys == None:
            keys = args[1]
            
        if keys == None:
            raise Exception( "A list of Keys must be specified")
        
        if not isinstance(keys, list):
            keys = [keys]

        def wrapper(func):
            self.events.on_key(type, keys, func)
            return func
        return wrapper
    
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

    def center(self):
        r'''
        return the center of the screen
        '''
        return self.surface.get_rect().center

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
        Fill the screen with a color
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
        colors = random_color_list(len(self.grid))
        c = 0
        for i in self.grid:
            color = colors[c]
            Rect(pos=i[:2], size=i[2:], color=color).draw(self)
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
                    
            elif isinstance(objects, Object) or isinstance(objects, Unit):
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
    
    