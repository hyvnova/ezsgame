from typing import Tuple
import pygame as pg

from ezsgame.types import Pos
from ezsgame.world import World


def get_mouse_pos() -> Pos:
    r'''
    #### Returns the mouse position
    Note: position is already adapted to the world position
    '''
    return Pos(pg.mouse.get_pos()) + World.pos