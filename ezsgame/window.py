from typing import Iterable
import pygame as pg, random, os

from ezsgame.scenes import SceneManager
from .objects import Image
from .styles.units import Measure
from .global_data import DATA, on_update
from .types import ProfilingOptions, Size, Pos
from .styles.colors import Gradient
from .styles.styles_resolver import resolve_color
from .world import World

# handlers
from .event_handler import EventHandler
from .time_handler import TimeHandler

from pstats import SortKey, Stats


pg.init()

class Window:
    """
    #### Window
    
    - Profiling: If a `ProfilingOptions` is passed to the `profiling` parameter, the profiling will be enabled.
    """
    __slots__ = (
        "size",
        "pos",
        "title",
        "icon",
        "depth",
        "vsync",
        "fullscreen",
        "resizable",
        "color",
        "surface",
        "clock",
        "show_fps",
        "fps",
        "profiling",
        "pr"
    )

    # check if an istance of Window is created
    is_created: bool = False

    def __new__(cls, *args, **kwargs) -> "Window":
        r"""
        #### Creates a new Window instance if it doesn't exist
        """
        if not cls.is_created:
            cls.is_created = True
            return object.__new__(cls)
        else:
            return DATA.window

    def _post_init(self):
        """
        #### Post init
        Creates global objects that need the window instance to be created beforehand.
        """
        # globalize time and event handlers
        DATA.TimeHandler = TimeHandler
        DATA.EventHandler = EventHandler
        DATA.window = self

        # set world size
        World.size = self.size

    def __init__(
        self,
        size: Size | Iterable[Measure] = Size(720, 420),
        title: str = "",
        icon: str = "",
        fps: int = 60,
        show_fps: bool = False,
        vsync: bool = False,
        depth: int = 32,
        color="black",
        fullscreen: bool = False,
        resizable: bool = False,
        profiling: ProfilingOptions = False,
    ):
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
        self.profiling = profiling

        self.load_icon(icon)

        # Profiling
        if self.profiling:
            self.profiling.profile.enable()

        # init window and surface
        self._init() 

        # Post init
        self._post_init()

    def __str__(self):
        return "<Window>"

    # -----------------------------------------------------------------------------
    def resize(self, size: Size):
        r"""
        #### Resizes the window
        - `size` : new size
        """
        self.size = size
        self._resolve_size(size)
        pg.display.set_mode(self.size, pg.RESIZABLE)
        return self
    
    def get_delta_time(self) -> int:
        return self.clock.get_time() / 1000

    def load_icon(self, icon: str):
        r"""
        #### Loads an icon for the window
        - `icon` :  path to the icon
        """
        self.icon = icon
        if icon == "":
            try:
                path = os.path.join(
                    os.path.dirname(__file__), "assets", "img", "icon.jpg"
                )
                self.icon = path
                pg.display.set_icon(pg.image.load(self.icon))

            except FileNotFoundError:
                pass

        return self

    def shake(self, force=5):
        r"""
        #### Shakes the window
        - `force` : force of the shake
        """
        if force <= 0:
            return

        force = int(force)
        x = random.randint(-force, force)
        y = random.randint(-force, force)
        self.surface.blit(self.surface, (x, y))
        return self

    def get_fps(self):
        r"""
        #### Returns the current window FPS
        """
        return self.clock.get_fps()

    def check_events(self):
        r"""
        #### Checks and Manage the events, should be called in the main loop
        """
        TimeHandler.check()
        EventHandler.check()

    def _resolve_size(self, size: Size):
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
                    'Screen size should "max" || "full" or list [width, height] '
                )

        elif len(size) == 2:
            if size[0] in ("max", "full", "100%"):
                self.size[0] = pg.display.list_modes()[0][0]
            elif size[1] in ("max", "full", "100%"):
                self.size[1] = pg.display.list_modes()[0][1]
            else:
                self.size = Size(size[0], size[1])

    def _init(self):
        r"""
        #### Initializes the window, is called automatically
        """

        self._resolve_size(self.size)

        if self.resizable and self.fullscreen:
            raise ValueError("You can't have resize and fullscreen at the same time")

        display_type = 0
        if self.fullscreen:
            display_type = pg.FULLSCREEN

        elif self.resizable:
            display_type = pg.RESIZABLE

        self.surface = pg.display.set_mode(
            self.size, display_type, self.depth, 0, self.vsync
        )

        pg.display.set_caption(self.title)
        if self.icon != "":
            pg.display.set_icon(pg.image.load(self.icon))

        self.clock = pg.time.Clock()


    # Property shortcuts 
    @property
    def x(self) -> Measure:
        return self.pos.x
    
    @x.setter
    def x(self, value: Measure) -> None:
        self.pos.x = value

    @property
    def y(self) -> Measure:
        return self.pos.y
    
    @y.setter
    def y(self, value: Measure) -> None:
        self.pos.y = value

    @property
    def width(self) -> Measure:
        return self.size.width
    
    @width.setter
    def width(self, value: Measure) -> None:
        self.size.width = value

    @property
    def height(self) -> Measure:
        return self.size.height
    
    @height.setter
    def height(self, value: Measure) -> None:
        self.size.height = value


    def update(self):
        r"""
        #### Updates the Window
        """

        if self.show_fps:
            pg.display.set_caption(
                f"{self.title}  FPS : " + f"{int(self.clock.get_fps())}"
            )

        pg.display.update()

        self.clock.tick(self.fps)

        # call on update events
        for func in on_update():
            func()

    def quit(self):
        r"""
        #### Quits the App  (Ends the window)
        """

        if self.profiling:
            self.profiling.profile.disable()

            # save profiling stats
            self.profiling.profile.dump_stats(self.profiling.file)

            # print profiling stats
            stats = Stats(self.profiling.file)
            stats.sort_stats(SortKey.TIME).print_stats(self.profiling.limit)

        pg.quit()
        quit()

    def fill(self, color=None, pos: list = [0, 0], size: list = [0, 0]):
        r"""
        #### Fill the Window with a `color` or `gradient`
        - `color` : color to fill the Window with, or  `Gradient` or `Image`  (Optional)
        - `pos` : position of the fill start (Optional)
        - `size` : size of the fill (Optional)
        """

        color = self.color if color == None else color

        if size == [0, 0]:
            size = self.size

        if isinstance(color, Gradient) or isinstance(color, Image):
            color.draw()

        else:
            color = resolve_color(color)
            pg.draw.rect(self.surface, color, pg.Rect(pos, size))

    def toggle_fullscreen(self):
        r"""
        #### Toggles the fullscreen mode
        """
        self.fullscreen = not self.fullscreen
        self._init()


    # Scenes
    def run_scenes(self, scene_manager: SceneManager):
        # Main loop
        while True:
            self.check_events()

            scene_manager.update()
            scene_manager.draw()
    
            self.update()
