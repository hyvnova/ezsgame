"""
Module for scenes manipulation and creation
"""

from abc import ABC, abstractmethod
from typing import FrozenSet


class Scene(ABC):
    """
    Abstract class for scenes
    - Note: A module can be a scene if it has the following method and properties:
        - `name` (Property, str)
        - `draw` (Method)
    """

    def __init__(
        self, name: str, shadow_update: bool = False, shadow_draw: bool = False
    ):
        self.name: str = name
        self.shadow_update: bool = shadow_update
        self.shadow_draw: bool = shadow_draw

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

    @abstractmethod
    def exit(self) -> None:
        """
        Exit the scene
        (Happens after main loop)
        """

    @abstractmethod
    def switch_to(self) -> None:
        """
        Switch to this scene
        """


class SceneManager:
    """
    Class for managing scenes
    """

    def __init__(self, *scenes: Scene):
        self.scenes: dict = {scene.name: scene for scene in scenes}
        self.current_scene: Scene = None

        # Reference to scenes that have shadow_update
        self.has_shadow_update: FrozenSet[str] = frozenset(
            [scene.name for scene in scenes if scene.shadow_update]
        )

        # Reference to scenes that have shadow_draw
        self.has_shadow_draw: FrozenSet[str] = frozenset(
            [scene.name for scene in scenes if scene.shadow_draw]
        )

    def switch_to(self, scene_name: str) -> None:
        """
        Switch to a scene
        """
        if scene_name in self.scenes.keys():
            if self.current_scene:
                self.current_scene.exit()
            self.current_scene = self.scenes[scene_name]
            self.current_scene.switch_to()
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

    # Utility methods ----------------------------------------------

    def __getitem__(self, scene_name: str) -> Scene:
        """
        Returns a scene
        """
        return self.scenes[scene_name]
