from ast import Tuple
from typing import Callable, Iterable, List, Dict, Tuple
from pathlib import Path
import pygame

from ezsgame.asset_handler import find_asset
from ezsgame.objects.object import Object
from ..styles.styles_resolver import resolve_position, resolve_size
from ..styles.units import Measure
from ezsgame.types import Pos, Size
from ..world import get_window
from PIL import Image, ImageSequence


pgSpriteClass = pygame.sprite.Sprite


class Sprite(pgSpriteClass, Object):
    """Static image that can be positioned and drawn like any other Object."""
    _scale_cache: Dict[Tuple[str, Tuple[int, int]], pygame.Surface] = {}
    def __new__(
        cls,
        sprite: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        scale: bool = True,
        static: bool = False,
    ):
        """Instantiate Sprite unless given a GIF path."""

        # if is animated
        if Path(sprite).suffix == ".gif":
            raise TypeError("Use the AnimatedSprite class for animated sprites instead.")

        return object.__new__(Sprite)

    def __init__(
        self,
        sprite: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        scale: bool = True,
        static: bool = False,
    ):
        """Load an image and prepare rects for drawing."""
        pgSpriteClass.__init__(self)
        Object.__init__(self, pos, size)

        self.sprite = find_asset(sprite)
        self._orig_image = pygame.image.load(self.sprite)
        self.scale = scale

        if scale:
            key = (self.sprite, self.size.as_tuple())
            self.image = Sprite._scale_cache.get(key)
            if self.image is None:
                self.image = pygame.transform.scale(self._orig_image, self.size)
                Sprite._scale_cache[key] = self.image
        else:
            self.image = self._orig_image

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos.as_tuple()
        self.rect.size = self.size.as_tuple()
        self.start_pos = self.pos
        self.start_size = self.size
        self._last_size = self.size

        if static:
            self.draw = lambda: self.window.surface.blit(self.image, self.rect)

    def _update(self):
        """Resize image when needed and update rect coordinates."""

        if self.scale and self.size != self._last_size:
            key = (self.sprite, self.size.as_tuple())
            self.image = Sprite._scale_cache.get(key)
            if self.image is None:
                self.image = pygame.transform.scale(self._orig_image, self.size)
                Sprite._scale_cache[key] = self.image
            self._last_size = self.size

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos.as_tuple()
        self.rect.size = self.size.as_tuple()

    def draw(self):
        self._update()
        self.window.surface.blit(self.image, self.rect)


class AnimatedSprite(pgSpriteClass):
    """GIF-based sprite that updates frames automatically."""
    _cached_frames: Dict[str, List[pygame.Surface]] = {} # {path: [frames]} used to cache frames/resources for animated sprites
    _cached_sprites: Dict[str, Tuple] = {} # {path: (size, frame_rate, scale, draw_method)} used to cache sprites that do the same but are in different locations
    
    def __new__(
        cls,
        sprite: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        frame_rate: int = 5,
        scale: bool = True,
    ):
        """Return cached clone when possible to save memory."""

        if AnimatedSprite._cached_sprites.get(sprite, [None])[:-1] == (size, frame_rate, scale):
            # Return a AnimatedSpriteRef object that references the cached sprite
            return AnimatedSpriteRef.__new__(AnimatedSpriteRef, AnimatedSprite._cached_sprites[sprite][-1])
            
        return object.__new__(AnimatedSprite)

    def __init__(
        self,
        sprite: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        frame_rate: int = -1, # -1 = auto
        scale: bool = True,
    ):
        """Load frames from a GIF and set up initial state."""

        pgSpriteClass.__init__(self)

        self.window = get_window()

        # resolve pos and size
        self.size = resolve_size(self, size, self.window.size, True)
        self.pos = resolve_position(self, pos, self.window, True)

        self.current_frame = 0
        self.last_update_time = 0

        if sprite in self._cached_frames:
            self.frames = self._cached_frames[sprite]

        # load frames (sprite is a gif)
        else:
            self.frames = [
                pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                for frame in ImageSequence.Iterator(Image.open(sprite))
            ]
            self.frames = self.frames[1:]

            self._cached_frames[sprite] = self.frames

        # set frame rate
        if frame_rate == -1:
            self.frame_rate = len(self.frames)

        # set sprite image and rect
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

        # set scale
        if scale:
            self.image = pygame.transform.scale(self.image, self.size)
            self.rect.size = self.size

        # cache sprite
        self._cached_sprites[sprite] = (size, frame_rate, scale, self.draw)

    def _update(self):
        """Advance the animation if enough time has elapsed."""

        current_time = pygame.time.get_ticks()

        # calculate time since last update
        time_since_last_update = current_time - self.last_update_time

        # update current frame if enough time has passed
        if time_since_last_update > 1000 / self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update_time = current_time

    def draw(self):
        self._update()
        self.window.surface.blit(self.image, self.rect)

class AnimatedSpriteRef:
    """Lightweight proxy that reuses a cached draw method."""

    def __new__(
        cls,
        draw_method: Callable,
    ):
        """Create a reference object without copying surfaces."""

        return object.__new__(cls)

    def __init__(self, draw_method: Callable):
        """Store the cached draw callable."""

        self.draw = draw_method

    def draw(self):
        """Placeholder so AnimatedSpriteRef matches Sprite interface."""

        pass
