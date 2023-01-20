from typing import Iterable
import pygame as pg, random, os

from .styles.units import Measure
from .objects import Image
from .global_data import DATA, on_update

from .types import Size, Pos
from .styles.colors import Gradient
from .styles.styles_resolver import resolve_color
  
# handlers
from .event_handler import EventHandler
from .time_handler import TimeHandler

class Window:
    __slots__ = ("size", "pos", "title", "icon", "depth", "vsync", "fullscreen", "resizable", "color", "surface", "clock", "show_fps", "delta_time", "fps")
    
    # check if an istance of Window is created
    is_created: bool = False

    def __new__(cls, *args, **kwargs) -> 'Window':
        r'''
        #### Creates a new Window instance if it doesn't exist
        '''
        if not cls.is_created:
            cls.is_created = True
            
            window = object.__new__(cls)
            
            DATA.window = window
            
            # globalize time and event handlers
            DATA.TimeHandler = TimeHandler
            DATA.EventHandler = EventHandler
            return window

        else:
            return DATA.window

    def __init__(self, size: Size | Iterable[Measure] = Size(720, 420), title: str = "", icon: str = "", fps: int = 60,
                 show_fps: bool = False, vsync: bool = False, depth: int = 32, color="black", fullscreen: bool = False,
                 resizable: bool = False):

        self.size = size if isinstance(size, Size) else Size(*size)
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
        
        self.delta_time = lambda: self.clock.tick(self.fps) / 1000
        
        self.load_icon(icon)

        # init window
        self.__init()


    def __str__(self):
        return "<Window>"

    # -----------------------------------------------------------------------------

    def load_icon(self, icon: str):
        r'''
        #### Loads an icon for the window
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
        #### Shakes the window
        - `force` : force of the shake
        '''
        if force <= 0:
            return

        force = int(force)
        x = random.randint(-force, force)
        y = random.randint(-force, force)
        self.surface.blit(self.surface, (x, y))
        return self

    def get_fps(self):
        r'''
        #### Returns the current window FPS
        '''
        return self.clock.get_fps()

    def check_events(self):
        r'''
        #### Checks and Manage the events, should be called in the main loop
        '''
        TimeHandler.check()
        EventHandler.check()

    def wait(self, time: int):
        r'''
        #### Waits for a certain amount of time
        - `time` : time to wait for, in milliseconds
        '''
        pg.time.wait(time)

    def __init(self):
        r'''
        #### Initializes the window, is called automatically
        '''

        pg.init()

        if self.resizable and self.fullscreen:
            raise ValueError("You can't have resize and fullscreen at the same time")

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
    
        
    def update(self):
        r'''
        #### Updates the Window
        '''

        if self.show_fps:
            pg.display.set_caption(
                f"{self.title}  FPS : " + f"{int(self.clock.get_fps())}")

        pg.display.update()
        
        self.clock.tick(self.fps)

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
        #### Fill the Window with a `color` or `gradient`
        - `color` : color to fill the Window with, or  `Gradient` or `Image`  (Optional)
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
        