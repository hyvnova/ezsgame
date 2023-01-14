import pygame
from abc import ABC, abstractmethod
from .global_data import get_window

vec = pygame.math.Vector2

class Camera:
    def __init__(self, object, scrollmethod=None):
        self.object = object
        self.offset = vec(0, 0)
        self.width, self.height = get_window().size
        self.CONST = vec(-self.width / 2 + object.size[0] / 2, -self.object.size[1] + 20)

        if scrollmethod:
            self.setmethod(scrollmethod)

    def setmethod(self, method):
        try:
            self.method = method(self)
        except:
            self.method = method

    def scroll(self):
        self.method.scroll()

class CamScroll(ABC):
    def __call__(self, camera):
        self.camera = camera
        self.object = camera.object
    
    def __init__(self, camera):
        self.__call__(camera)

    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera=None):
        CamScroll.__init__(self, camera)

    def scroll(self):
        self.camera.offset.x += (self.object.pos.x - self.camera.offset.x + self.camera.CONST.x)
        self.camera.offset.y += (self.object.pos.y - self.camera.offset.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset.x), int(self.camera.offset.y)

class Border(CamScroll):
    def __init__(self, camera=None, borders=[]):
        self.borders = borders
        
        if not borders:
            self.borders = [self.object.pos.x, self.object.pos.x + self.object.size.width, self.object.pos.y, self.object.pos.y + self.object.size.height]
        
        CamScroll.__init__(self, camera)
        
    def scroll(self):
        self.camera.offset.x += (self.object.pos.x - self.camera.offset.x + self.camera.CONST.x)
        self.camera.offset.y += (self.object.pos.y - self.camera.offset.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset.x), int(self.camera.offset.y)
        
        #border right 
        self.camera.offset.x = max(self.borders[0], self.camera.offset.x)
        
        #   border left
        self.camera.offset.x = min(self.camera.offset.x, self.borders[1] - self.camera.width)

class Auto(CamScroll):
    def __init__(self,camera=None):
        CamScroll.__init__(self,camera)

    def scroll(self):
        self.camera.offset.x += 1

