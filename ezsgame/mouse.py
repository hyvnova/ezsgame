from typing import Tuple
import pygame as pg

def get_mouse_pos() -> Tuple[int, int]:
    r'''
    #### Returns the mouse position
    '''
    return pg.mouse.get_pos()