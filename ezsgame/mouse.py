from typing import Tuple
import pygame as pg

from ezsgame.types import Pos


def get_mouse_pos() -> Pos:
    r'''
    #### Returns the mouse position
    '''
    return Pos(pg.mouse.get_pos())