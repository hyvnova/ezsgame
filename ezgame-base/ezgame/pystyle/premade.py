import pygame as pg, random, os
pg.init()
# Colors (R, G, B)
color = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 128, 0),
    "purple": (128, 0, 128),
    "pink": (255, 0, 255),
    "light_blue": (0, 255, 255),
    "light_green": (0, 255, 0),
    "light_red": (255, 0, 0),
    "light_yellow": (255, 255, 0),
    "light_orange": (255, 128, 0),
    "light_purple": (128, 0, 128),
    "dark_blue": (0, 0, 128),
    "dark_green": (0, 128, 0),
    "dark_red": (128, 0, 0),
    "dark_yellow": (128, 128, 0),
    "dark_orange": (128, 64, 0),
    "dark_purple": (128, 0, 128), 
}

# PyStyle
class Object:
    def __init__(self, size, pos, **kwargs):
        # define general style properties
        self.color = color["white"]
        self.margin = [0, 0, 0, 0] # top, right, bottom, left
        self.padding = [0, 0, 0, 0] # top, right, bottom, left
        self.rounded = 0
        self.opacity = 255
        self.pos = pos
        self.style(**kwargs)
        self.size = size
        
    def style(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__dict__:
                setattr(self, key, value)
            else:
                print("Style not found: ", key)

    def collision(self, surface, obj):
        self.resolveStyle(obj)
        obj.resolveStyle(surface)
        
        if self.pos[0] + self.size[0] > obj.pos[0] and self.pos[0] < obj.pos[0] + obj.size[0] and self.pos[1] + self.size[1] > obj.pos[1] and self.pos[1] < obj.pos[1] + obj.size[1]:
            return True
        return False
            
    def move(self, surface, x=0, y=0):
        self.resolveStyle(surface) 
        self.pos[0] += x
        self.pos[1] += y
    
    # return true if object is out of screen
    def isOut(self, surface):
        self.resolveStyle(surface)
        if self.pos[0] < 0 or self.pos[0] + self.size[0] > surface.get_width() or self.pos[1] < 0 or self.pos[1] + self.size[1] > surface.get_height():
            return True
        return False
            
    def resolveStyle(self, surface):
        # resolve style properties
        self.size = [self.size[0] - self.margin[0] - self.margin[0], self.size[1] - self.margin[1] - self.margin[1]]
        # align position x
        if self.pos[0] == "center":
            padding = self.padding[0] + self.padding[2] + self.margin[0] + self.margin[2] + self.rounded
            self.pos[0] = (surface.get_width() - self.size[0]) / 2 - padding
        elif self.pos[0] == "right":
            self.pos[0] = surface.get_width() - self.size[0] - self.margin[0] - self.padding[0]
        elif self.pos[0] == "left":
            self.pos[0] = self.margin[0] + self.padding[0] + self.size[0] 
        elif self.pos[0] == "right-center":
            self.pos[0] = surface.get_width() - self.size[0] - self.margin[0] - self.padding[0] / 2 - (self.size[0] * 2) + self.margin[0] / 2
        elif self.pos[0] == "left-center":
            self.pos[0] = self.margin[0] + self.padding[0] / 2 + self.size[0] - self.margin[0] / 2 + (self.size[0] * 2)
        else:
            self.pos[0] += self.padding[0] / 2 
    
        # align position y
        if self.pos[1] == "center":
            self.pos[1] = (surface.get_height() - self.size[1]) / 2 + self.margin[1] / 2 + self.padding[1] / 2 
        elif self.pos[1] == "top":
            self.pos[1] = self.margin[1] + self.padding[1]
        elif self.pos[1] == "bottom":
            self.pos[1] = surface.get_height() - self.size[1] - self.margin[1] - self.padding[1]
        elif self.pos[1] == "top-center":
            self.pos[1] = self.margin[1] + self.padding[1] + (surface.get_height() - self.size[1]) / 2 - (surface.get_height() - self.size[1]) / 2 / 2
        elif self.pos[1] == "bottom-center":
            self.pos[1] = surface.get_height() - self.size[1] - self.margin[1] - self.padding[1] - (surface.get_height() - self.size[1]) / 2 / 2 
        else:
            self.pos[1] = self.pos[1] + self.margin[1] + self.padding[1] / 2
        return self.pos
            
class Rect(Object):
    r'''
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param size: size of the figure ``list(width, height)``
    @Keyword Arguments:
        * color= (R, G, B) ``color["white"] or tuple(R, G, B)``
        * background= (R, G, B) ``color["white"] or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * padding= [top, right, bottom, left] ``list(top, right, bottom, left)``
    '''
    def __init__(self,size, pos, **kwargs):
        super().__init__(size, pos, **kwargs)
        
    def getPos(self, surface):
        self.resolveStyle(surface)
        return self.pos

    def resolveStyle(self, surface):
        super().resolveStyle(surface)
        
    def draw(self, surface):
        self.resolveStyle(surface)
        pg.draw.rect(surface, self.color, [self.pos[0], self.pos[1], self.size[0], self.size[1]], self.rounded)
    
class Text(Object):
    r'''
    @param text: text to be rendered ``str``
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param size: size of the text ``int``
    @param fontname: font name ``str``
    @Keyword Arguments:
        * color= (R, G, B) ``color["white"] or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * padding= [top, right, bottom, left] ``list(top, right, bottom, left)``
    '''
    def __init__(self, text, pos, size, fontname, **kwargs):        
        self.text = self.font(text, fontname, size, self.color)
        super().__init__(size=[self.text.get_width(), self.text.get_height()], pos=pos, **kwargs)
        
    def font(self, text, name, size, color=color["white"]):
        # load local font 
        pg.font.init()
        name = name.lower()
        # if font in system fonts
        if name in pg.font.get_fonts():
            font = pg.font.SysFont(name, size)
        else:
            font = pg.font.Font(f"assets/fonts/{name}.ttf", size)
            
        return font.render(text, True, color)
    
    def resolveStyle(self, surface):
        super().resolveStyle(surface, [self.text.get_width(), self.text.get_height()])

    def getPos(self, surface):
        self.resolveStyle(surface)
        return self.pos
        
    def draw(self, surface):
        self.resolveStyle(surface)        
        surface.blit(self.text, self.pos)

class Image(Rect):
    r'''
    @param image: image to be rendered ``str``
    @param pos: position of the image ``list(x, y) or list("left", "top")``
    @param size: size of the image ``int``
    @Keyword Arguments:
        * color= (R, G, B) ``color["white"] or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * padding= [top, right, bottom, left] ``list(top, right, bottom, left)``
    '''
    def __init__(self, image, pos, size, **kwargs):
        super().__init__(size, pos, **kwargs)
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, self.size)
        
    def getPos(self, surface):
        self.resolveStyle(surface)
        return self.pos
        
    def draw(self, surface):
        self.resolveStyle(surface)
        surface.blit(self.image, self.pos)
      
class EventHandler:
    r'''
    @param surface: surface to be drawn on ``pygame.Surface``
    '''
    def __init__(self, surface):
        self.surface = surface
        self.events  = {}
        self.base_events = {}
    
    def removeDuplicates(self):
        self.events = {k:v for k,v in self.events.items() if v != None}
                                            
    def check(self, event, surface=None):
        
        if surface != None:
            if surface.screen != self.surface:
                self.surface = surface.screen
        self.removeDuplicates()
        
        for ev in event:
            # BASE EVENTS ----------------------------------------------------------------------------------
            # quit
            if ev.type == pg.QUIT:
                if "quit" in self.base_events:
                    self.base_events["quit"]["callback"](*self.base_events["quit"]["args"])
                pg.quit()
                quit()
                
            # STORED EVENTS --------------------------------------------------------------------------------
            for key, value in self.events.items():
                if value["type"] == event.type:
                    
                    # onclick
                    if value["type"] == 1025:
                        if self.isHovering(value["object"]):
                            self.call(self.events[key]["callback"], *self.events[key]["args"])
                            continue
                        
                    # onmouseover 
                    elif value["type"] == 1024:
                        if self.isHovering(value["object"]):
                            self.call(self.events[key]["callback"], *self.events[key]["args"])
                            continue
                        
    def call(self, fun, args : list = []):
        if args == []:
            fun()
        else:
            fun(*args)
                        
    def addEventListener(self, event, name, object, callback, args : list = []):
        evs  = {
            "click" : 1025,
            "hover" : 1024
        }
        if event in evs:
            event = evs[event]
        else:
            raise Exception("Event type not found", event)
        
        self.events[name] = {"type": event, "object": object, "callback": callback, "args": args}

    def remove(self, name):
        del self.events[name]

    def isHovering(self, object):
        mouse_pos = pg.mouse.get_pos()
        object_pos = object.getPos(self.surface)
        object_size = object.size

        if mouse_pos[0] > object_pos[0] and mouse_pos[0] < object_pos[0] + object_size[0] and mouse_pos[1] > object_pos[1] and mouse_pos[1] < object_pos[1] + object_size[1]:
            return True
        else:
            return False
            
    def getEvent(self):
        # return current event
        return pg.event.get()
    
    def onQuit(self, callback, args : list = []):
        self.base_events["quit"] = {"callback": callback, "args": args if type(args) == list else [args]}
            
class Circle(Object):
    r'''
    @param pos: position of the circle ``list(x, y) or list("left", "top")``
    @param radius: radius of the circle ``int``
    @Keyword Arguments:
        * color= (R, G, B) ``color["white"] or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * padding= [top, right, bottom, left] ``list(top, right, bottom, left)``
    '''
    def __init__(self, pos, radius, **kwargs):
        super().__init__(size=[radius*2, radius*2], pos=pos, **kwargs)
        self.radius = radius

    def resolveStyle(self, surface):
        super().resolveStyle(surface)
            
    def getPos(self, surface):
        self.resolveStyle(surface)
        return self.pos
        
    def draw(self, surface):
        self.resolveStyle(surface)
        pg.draw.circle(surface, self.color, self.pos, self.radius)
        
        