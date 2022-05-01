import pygame as pg
from ezsgame.global_data import get_id

class PObject:
    r'''
    Primitive Objects do not check anything before. BECAREFUL the funcions you use without defining variables
    '''
    def __init__(self, **attributes):
       self._id = get_id()
       for k,v in attributes.items():
           self.__setattr__(k,v)

    def __str__(self):
        return f"<Primitive Object: {self.__class__.__name__}, ID: {self._id}>"

    def __repr__(self):
        return self.__str__()
           
class PRect(PObject):
    def __init__(self, **attributes):
        super().__init__(**attributes)
                
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        pg.draw.rect(screen.surface, self.color, [*self.pos, *self.size], int(self.stroke))
        
        