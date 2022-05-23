import pygame as pg
from ezsgame.global_data import get_id, get_screen

class PObject:
    r'''
    Primitive Objects do not check anything before. BECAREFUL the funcions you use without defining variables
    '''
    def __init__(self, **attributes):
        self._id = get_id()
        self.screen = get_screen()
         
        for k,v in attributes.items():
            self.__setattr__(k,v)

    def __str__(self):
        return f"<Primitive Object: {self.__class__.__name__}, ID: {self._id}>"

    def __repr__(self):
        return self.__str__()
           
class PRect(PObject):
    def __init__(self, **attributes):
        super().__init__(**attributes)
                
    def draw(self):
        vars = self.__dict__
        try:
            pg.draw.rect(self.screen.surface, vars.get("color", "white"), [*vars.get("pos", [0,0]), *vars.get("size", [0,0])], int(vars.get("stroke", 0)), *vars.get("border_radius", [0,0,0,0]))
        except:
            pass
        



    