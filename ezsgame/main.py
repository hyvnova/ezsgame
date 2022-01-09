import pygame as pg, random
from ezsgame.pystyle.premade import *
from ezsgame.pystyle.animations import *

class Screen:
    def __init__(self, size : list = [720, 420], title : str = "PyStyle", icon : str = "", fps : int = 60, 
                 show_fps : bool = False):
        self.size = size
        self.title = title
        self.icon = icon
        self.surface = None
        self.clock = None
        self.fps = fps
        self.show_fps = show_fps
        self.size = [0, 0]
        self.resolveSize(size)        
        self.events = EventHandler(self)
        self.time = TimeHandler()
        self.loadIcon(icon)
        self.init()
        
    def deltaTime(self):
        r'''
        Returns the delta time since the last frame
        '''
        return self.clock.get_time()
         
    def loadIcon(self, icon : str):
        r'''
        Loads an icon for the screen
        '''
        self.icon = icon
        if icon == "":
            self.icon = "ezsgame/pystyle/assets/img/icon.jpg"
        pg.display.set_icon(pg.image.load(self.icon))

    def shake(self, force=5):
        r'''
        Shake the screen
        '''
        x, y = self.surface.get_rect().center
        x = random.randint(-force, force)
        y = random.randint(-force, force)
        self.surface.blit(self.surface, (x, y))
        
    def getFPS(self):
        r'''
        Returns the current FPS
        '''
        return self.clock.get_fps()

    def check(self):
        r'''
        Check and Manage the events, should be called in the main loop
        '''
        self.events.check(self.events.get(), self)
        self.time.check()

    @staticmethod
    def mousePos():
        r'''
        Returns the mouse position
        '''
        return pg.mouse.get_pos()

    def wait(self, time : int):
        r'''
        Wait for a certain amount of time
        '''
        pg.time.wait(time)
            
    def div(self, axis, q):
        r'''
        Return list of division points of the screen -> [[x, y], [x, y], ...]
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
    
    def center(self):
        r'''
        Returns the center of the screen
        '''
        return self.size[0] / 2, self.size[1] / 2

    def resolveSize(self, size : list):
        if size == []:
            raise Exception("You must specify a size for the screen")
        elif len(size) == 1:
            if size[0] == "max" or size[0] == "full":
                self.size = pg.display.get_surface().get_size()
            else:
                self.size = [size[0], size[0]]
            
        elif len(size) == 2:
            if size[0] == "max" or size[0] == "full":
                self.size[0] = pg.display.get_surface().get_width()
            elif size[1] == "max" or size[1] == "full":
                self.size[1] = pg.display.get_surface().get_height()        
            else:
                self.size = size
        
    def init(self):
        pg.init()
        self.surface = pg.display.set_mode(self.size, 0, 32)
        pg.display.set_caption(self.title)
        if self.icon != "":
            pg.display.set_icon(pg.image.load(self.icon))
        self.clock = pg.time.Clock()
        
    def update(self):
        if self.show_fps:
            pg.display.set_caption(f"{self.title}  FPS : " + f"{int(self.clock.get_fps())}")
        
        pg.display.update()
        self.clock.tick(self.fps)
        
    def quit(self):
        pg.quit()
        quit()

    def fill(self, color, pos=[0, 0], size=[0, 0]):
        r'''
        Fill the screen with a color
        '''
        if isinstance(color, str):
            if color in Color:
                color = Color[color]
        
        if size == [0, 0]:
            size = self.size
        if pos == [0, 0]:
            pos = [0, 0]
        pg.draw.rect(self.surface, color, pg.Rect(pos, size))
      
    def gridDiv(self, cols=3, rows=3):
        r'''
        Returns the division of the screen into a grid
        ahould return a list with potistion of earch box in the grid
        '''
        grid = []
        divs_x = self.div("x", cols)
        box_width = divs_x[-1][0] - divs_x[-2][0]
        divs_y = self.div("y", rows)
        box_height = divs_y[-1][0] - divs_y[-2][0]
        
        self.grid_size = [rows, cols]
        
        for i in range(cols):
            for j in range(rows):
                grid.append([divs_x[i][0], divs_y[j][0], box_width, box_height])
                
        self.grid_space = len(grid)
                
        return grid
    
    def run(self, fill_color=(0,0,0)):
        r'''
        Run the screen
        '''
        while True:
            self.check()
            self.fill(fill_color)
            self.draw()
            self.update()

class IScreen(Screen):
    def __init__(self, size : list = [720, 420], title : str = "PyStyle", icon : str = "", fps : int = 60, 
                 show_fps : bool = False, objects = []):
        super().__init__(size, title, icon, fps, show_fps)
        self.objects = objects
        self.grid = self.gridDiv(cols=3, rows=3)
        self.formatObjects()
    
    def formatObjects(self):
        r'''
        Format the objects in the screen
        '''
        objs = []
        i = 0
        for obj in self.objects:
            if isinstance(obj, Object):
                objs.append({"object": obj, "z-index": i})
                i += 1
            
        self.objects = objs
    
    def showGrid(self):
        r'''
        Draws  grid on the screen
        '''
        colors = list(color.values())
        c = 0
        for i in self.grid:
            Rect(pos=i[:2], size=i[2:], color=colors[c]).draw(self)
            c += 1
   
    def place(self, object, row=0, col=0):     
        r'''
        Place an object in the grid
        '''
        pos = self.grid[row * 3 + col]
        # center object in the box
        object.pos = [pos[0] + pos[2] / 2 - object.size[0] / 2, pos[1] + pos[3] / 2 - object.size[1] / 2]
   
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
                    
            elif isinstance(objects, Object):
                self.objects.append({"object": objects, "z-index":1})

            else:
                raise Exception("Object must be a list of objects or an object")
            
        if auto_place:
            if len(objects) > self.grid_space:
                raise Exception(f"Not enough space in the grid ({self.grid_space}) for {len(objects)} objects")
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
                    if objects[i]["object"].collides(objects[j]["object"]):
                        colliding.append([{"object": objects[j]["object"], "z-index": objects[j]["z-index"], "index": i},
                                          {"object": objects[j]["object"], "z-index": objects[j]["z-index"], "index": j}])
                        to_remove.append(objects[i])
                        to_remove.append(objects[j])
                        
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
        

 

        