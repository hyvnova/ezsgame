from ast import Tuple
from typing import Callable, Iterable, List, Dict
from path import Path
import pygame
from ezsgame.styles.units import Measure
from ezsgame.types import Pos, Size
from ..objects import Object
from ..global_data import get_window

pgSpriteClass = pygame.sprite.Sprite


class Sprite(pgSpriteClass, Object):
    def __new__(
        cls,
        sprite: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        scale: bool = True,
        static: bool = False,
    ):
        # if is animated
        if Path(sprite).ext == ".gif":
            return AnimatedSprite.__new__(
                AnimatedSprite,
                sprite=sprite,
                pos=pos,
                size=size,
                scale=scale,
            )

        return object.__new__(Sprite)

    def __init__(
        self,
        sprite: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        scale: bool = True,
        static: bool = False,
    ):
        pgSpriteClass.__init__(self)
        Object.__init__(self, pos=pos, size=size)

        self.sprite = sprite
        self.image = pygame.image.load(sprite)

        if scale:
            self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.size = size
        self.start_pos = pos
        self.start_size = size

        if static:
            self.draw = lambda: self.window.surface.blit(self.image, self.rect)

    def _update(self):
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.rect.size = self.size

    def draw(self):
        self._update()
        self.window.surface.blit(self.image, self.rect)


from PIL import Image, ImageSequence


class AnimatedSprite(Sprite):
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
        if cls._cached_sprites.get(sprite, [None])[:-1] == (size, frame_rate, scale):
            # Return a AnimatedSpriteRef object that references the cached sprite
            return AnimatedSpriteRef.__new__(AnimatedSpriteRef, cls._cached_sprites[sprite][-1])
            
        return object.__new__(cls)

    def __init__(
        self,
        sprite: Path | str,
        pos: Pos | Iterable[Measure],
        size: Size | Iterable[Measure],
        frame_rate: int = -1, # -1 = auto
        scale: bool = True,
    ):
        super().__init__(sprite, pos, size, scale)

        self.window = get_window()

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
        self.rect.x, self.rect.y = pos

        # set scale
        if scale:
            self.image = pygame.transform.scale(self.image, size)
            self.rect.size = size

        # cache sprite
        self._cached_sprites[sprite] = (size, frame_rate, scale, self.draw)

    def _update(self):
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

    def __new__(
        cls,
        draw_method: Callable,
    ):
        return object.__new__(cls)        

    def __init__(self, draw_method: Callable):
        self.draw = draw_method

    def draw(self):
        pass