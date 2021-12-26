import pygame as pg, random, time, asyncio
from pystyle.premade import *

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
        self.time = TimeHandler()

    def getFPS(self):
        return self.clock.get_fps()

    def check(self, surface=None):
        surface = self if surface == None else surface
        self.events.check(self.events.get(), surface)
        self.time.check()

    @staticmethod
    def mousePos():
        return pg.mouse.get_pos()

    def sleep(self, time : int):
        pg.time.wait(time)
            
    def div(self, axis, q):
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

    def half(self):
        r'''
        Returns the half of the screen size -> [width, height]
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
        self.screen = pg.display.set_mode(self.size, 0, 32)
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

    def fill(self, color : list):
        self.screen.fill(color)
        
    
    
 

        