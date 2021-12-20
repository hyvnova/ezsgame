import pygame as pg, random
from pystyle.premade import color, Text, Rect, EventHandler, Image, Circle

class Screen:
    def __init__(self, size : list = [720, 420], title : str = "PyStyle", icon : str = "", fps : int = 60, 
                 show_fps : bool = False):
        self.size = size
        self.title = title
        self.icon = icon
        self.screen = None
        self.clock = None
        self.fps = 60
        self.show_fps = show_fps
        self.size = [0, 0]
        
        self.resolveSize(size)        
        
        self.init()
        self.events = EventHandler(self.screen)

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
        self.screen = pg.display.set_mode(self.size, 0, 32)
        pg.display.set_caption(self.title)
        if self.icon != "":
            pg.display.set_icon(pg.image.load(self.icon))
        self.clock = pg.time.Clock()
        
    def update(self):
        if self.show_fps:
            pg.display.set_caption(f"Current FPS : " + f"{int(self.clock.get_fps())}")
        
        pg.display.update()
        self.clock.tick(self.fps)
        
    def quit(self):
        pg.quit()
        quit()

    def fill(self, color : list):
        self.screen.fill(color)
        
    
    
 

        