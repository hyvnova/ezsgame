"""
Module for scenes manipulation and creation
"""

from abc import ABC, abstractmethod
from typing import FrozenSet

from .global_data import get_window

class Scene(ABC):
    """
    Abstract class for scenes

    ### Init
    Note: the minimum required for a scene is to have an `init`, `update` and `draw` methods
    - `name`: Name of the scene (defaults to class name without `_scene`) Example: `main_scene` -> `main`
    - `shadow_update`: If True, the scene will be updated even if it's not the current scene
    - `shadow_draw`: If True, the scene will be drawn even if it's not the current scene
    """

    def __init__(
        self, name: str = None, shadow_update: bool = False, shadow_draw: bool = False
    ):
        self.name: str = name or self.__class__.__name__.replace("_scene", "")
        self.shadow_update: bool = shadow_update
        self.shadow_draw: bool = shadow_draw

        self.manager: SceneManager = None


    @abstractmethod
    def init(self) -> None:
        """
        Initialize the scene
        (Happens before main loop)
        """

    @abstractmethod
    def update(self) -> None:
        """
        Update the scene
        (Happens before draw)
        """

    @abstractmethod
    def draw(self) -> None:
        """
        Draw the scene
        """

    def on_switch(self) -> None:
        """
        Called when the scene is switched to
        """
        pass

    def on_switch_out(self) -> None:
        """
        Called when the scene is switched from
        """
        pass

    def switch_to(self, scene_name: str) -> None:
        """
        Switch to a scene
        """
        if self.manager:
            self.manager.switch_to(scene_name)
        else:
            raise Exception("Scene manager not found")


class SceneManager:
    """
    Class for managing scenes

    ### Init
    - `scenes`: Scenes to be managed
    - `main_scene`: Name of the main scene (defaults to `main`)
    - `lazy_load`: If True, scenes will be initialized (init method) only when switched to not when the scene manager is initialized (Main scene will always be initialized)
    """

    def __init__(self, *scenes: Scene, main_scene: str = "main", lazy_load: bool = False):

        self.window = get_window()

        self.lazy_load: bool = lazy_load
        self.scenes: dict = {scene.name: scene for scene in scenes}
        
        try:
            self.current_scene: Scene = self.scenes[main_scene]
            self.current_scene.init()
            self.current_scene.on_switch()
        except KeyError:
            raise Exception(f"Main scene '{main_scene}' not found in scenes <{self.scenes.keys()}>")


        # Reference to scenes that have shadow_update
        self.has_shadow_update: FrozenSet[str] = frozenset(
            [scene.name for scene in scenes if getattr(scene, "shadow_update", False)]
        )

        # Reference to scenes that have shadow_draw
        self.has_shadow_draw: FrozenSet[str] = frozenset(
            [scene.name for scene in scenes if getattr(scene, "shadow_draw", False)]
        )

        for scene in scenes:
            scene.manager = self

        if not lazy_load:
            for scene in scenes:
                scene.init()

    def switch_to(self, scene_name: str) -> None:
        """
        Switch to a scene
        """
        if scene_name in self.scenes.keys():
            if self.current_scene:
                self.current_scene.on_switch_out()
                self.window.fill() # Clear window

            self.current_scene = self.scenes[scene_name]

            if self.lazy_load:
                self.current_scene.init()

            self.current_scene.on_switch()
        else:
            raise Exception(f"Scene '{scene_name}' not found")

    def update(self) -> None:
        """
        Update sthe current scene (and scenes that have shadow_update)
        """
        if self.current_scene:
            self.current_scene.update()

            # Update scenes that have shadow_update
            map(
                lambda name: self.scenes[name].update(),
                self.has_shadow_update - {self.current_scene.name},
            )

    def draw(self) -> None:
        """
        Draws the current scene (and scenes that have shadow_draw)
        """
        if self.current_scene:
            self.current_scene.draw()

            # Draw scenes that have shadow_draw
            map(
                lambda name: self.scenes[name].draw(),
                self.has_shadow_draw - {self.current_scene.name},
            )

    def __del__(self) -> None:
        """
        Exits all scenes
        """
        for scene in self.scenes.values():
            del scene # Calls exit

    # Utility methods ----------------------------------------------
    def __getitem__(self, scene_name: str) -> Scene:
        """
        Returns a scene
        """
        return self.scenes[scene_name]
