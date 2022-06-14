import pygame
from .objects import Object

pgSpriteClass = pygame.sprite.Sprite

class Sprite(pgSpriteClass, Object):
    
    def __init__(self, pos, size, sprite, scale=True, **styles):
        pgSpriteClass.__init__(self)
        Object.__init__(self, pos, size, **styles)
        
        self.sprite = sprite

        self.image = pygame.image.load(sprite)
        
        if scale:
            self.image = pygame.transform.scale(self.image, size)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.size = size
        self.start_pos = pos
        
       
    def draw(self):
        self.rect.topleft = self.pos
        self.rect.size = self.size
        
        self.screen.surface.blit(self.image, self.rect)