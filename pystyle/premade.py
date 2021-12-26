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
    def __init__(self, size, pos, **styles):
        # define general style properties
        self.color = styles.get("color", color["white"])
        self.margin = styles.get("margin", [0, 0, 0, 0]) # top, right, bottom, left
        self.padding = styles.get("padding", [0, 0, 0, 0]) # top, right, bottom, left
        self.rounded = styles.get("rounded", 0)
        self.opacity = styles.get("opacity", 255)
        self.pos = pos
        self.size = size
        self.surface = styles.get("surface", None)

    def collision(self, obj, surface=None):
        surface = self.surface if surface == None else surface.screen
        
        self.resolveStyle(surface)
        obj.resolveStyle(surface)
        
        if self.pos[0] + self.size[0] > obj.pos[0] and self.pos[0] < obj.pos[0] + obj.size[0] and self.pos[1] + self.size[1] > obj.pos[1] and self.pos[1] < obj.pos[1] + obj.size[1]:
            return True
        return False
            
    def move(self, x=0, y=0, surface=None):
        surface = self.surface if surface == None else surface.screen
        self.resolveStyle(surface) 
        self.pos[0] += x
        self.pos[1] += y * -1
     
    # return true if object is out of screen
    def isOut(self, surface=None):
        surface = self.surface if surface == None else surface.screen
        self.resolveStyle(surface)
        if self.pos[0] < 0 or self.pos[0] + self.size[0] > surface.get_width() or self.pos[1] < 0 or self.pos[1] + self.size[1] > surface.get_height():
            return True
        return False
            
    def resolveStyle(self, surface=None):
        if not isinstance(surface, pg.Surface):
            surface = self.surface if surface == None else surface.screen
        
        if isinstance(self.size, tuple):
            self.size = [self.size[0], self.size[1]]
        if isinstance(self.pos, tuple):
            self.pos = [self.pos[0], self.pos[1]]
        
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
        
    def getPos(self, surface=None):
        surface = self.surface if surface == None else surface.screen

        self.resolveStyle(surface)
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
    def __init__(self,size, pos, **styles):
        super().__init__(size, pos, **styles)
                
    def draw(self, surface=None):
        surface = self.surface if surface == None else surface.screen
        self.resolveStyle(surface)
        pg.draw.rect(surface, self.color, [self.pos[0], self.pos[1], self.size[0], self.size[1]], self.rounded)
    
class Text(Object):
    r'''
    @param text: text to be rendered ``str``
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param size: size of the text ``int``
    @param fontname: font name ``str``
    @param path: Path to Local Fonts are stored
    @Keyword Arguments:
        * color= (R, G, B) ``color["white"] or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * padding= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * path = path to font folder ``str``
    '''
    def __init__(self, text, pos, size, **styles):  
        self.path = styles.get("path", "")
        self.fontname = styles.get("fontname", "Arial")
        self.fontsize = size
        self.color = styles.get("color",color["white"])
        self.innertext = text
        self.text = self.font(text, self.fontname, size, self.color)
        super().__init__(size=[self.text.get_width(), self.text.get_height()], pos=pos, **styles)
        
    def font(self, text, name, size, color=color["white"]):
        # load local font 
        pg.font.init()
        name = name.lower()
        # if font in system fonts
        if name in pg.font.get_fonts():
            font = pg.font.SysFont(name, size)
        else:
            # if font in local fonts
            if os.path.exists(self.path + name + ".ttf"):
                font = pg.font.Font(self.path + name + ".ttf", size)
            else:
                raise Exception("Local Font not found in path: " + self.path + name + ".ttf")
                
        return font.render(text, True, color)
            
    def update(self, **atributes):
        self.text = self.font(atributes.get("text", self.innertext), self.fontname, self.fontsize, atributes.get("color", self.color))
        self.size = [self.text.get_width(), self.text.get_height()]
        self.color = atributes.get("color", self.color)
        self.fontname = atributes.get("fontname", self.fontname)
        self.fontsize = atributes.get("fontsize", self.fontsize)
        self.margin = atributes.get("margin", self.margin)
        self.padding = atributes.get("padding", self.padding)
        self.pos = atributes.get("pos", self.pos)
            
    def draw(self, surface=None):
        surface = self.surface if surface == None else surface.screen
        
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
    def __init__(self, image, pos, size, **styles):
        super().__init__(size, pos, **styles)
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, self.size)
        
    def draw(self, surface=None):
        surface = self.surface if surface == None else surface.screen
        
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
                                            
    def check(self, event, surface=None):
        if surface != None:
            if surface.screen != self.surface:
                self.surface = surface.screen
                
        self.events = {k:v for k,v in self.events.items() if v != None}
        
        for ev in event:
            # BASE EVENTS ----------------------------------------------------------------------------------
            # quit
            if ev.type == pg.QUIT:
                if "quit" in self.base_events:
                    self.base_events["quit"]["callback"](*self.base_events["quit"]["args"])
                pg.quit()
                quit()
                
            if ev.type == pg.MOUSEMOTION:
                if "mousemotion" in self.base_events:
                    self.base_events["mousemotion"]["callback"](*self.base_events["mousemotion"]["args"])
                
            if ev.type == pg.MOUSEBUTTONDOWN:
                if "mousedown" in self.base_events:
                    self.base_events["mousedown"]["callback"](*self.base_events["mousedown"]["args"])
                    
            if ev.type == pg.MOUSEBUTTONUP:
                if "mouseup" in self.base_events:
                    self.base_events["mouseup"]["callback"](*self.base_events["mouseup"]["args"])
                    
            if ev.type == pg.KEYDOWN:
                if "keydown" in self.base_events:
                    self.base_events["keydown"]["callback"](*self.base_events["keydown"]["args"])
                
            if ev.type == pg.KEYUP:
                if "keyup" in self.base_events:
                    self.base_events["keyup"]["callback"](*self.base_events["keyup"]["args"])
                            
            # STORED EVENTS --------------------------------------------------------------------------------
            for key, value in self.events.items():
                # onclick, onhover
                if value["type"] == 1025 or value["type"] == 1026:
                    if self.isHovering(value["object"]):
                        self.call(self.events[key]["callback"], self.events[key]["args"])
                        continue                
                    
                #key up or down
                elif value["type"] == pg.KEYDOWN and ev.type == pg.KEYDOWN:
                    if ev.key == value["key"]:
                        self.call(self.events[key]["callback"], self.events[key]["args"])
                        continue
                    
                elif value["type"] == pg.KEYUP and ev.type == pg.KEYUP:
                    if ev.key == value["key"]:
                        self.call(self.events[key]["callback"], self.events[key]["args"])
                        continue
                                               
    def call(self, fun, args : list = []):
        if args == []:
            fun()
        else:
            if isinstance(args, list):
                fun(*args)
            else:
                fun(args)
                        
    def addEventListener(self, event, name, object, callback, args : list = []):
        r'''
        - Adds a event listener to a object
        @param event: event to be added ``str``
            --events : click, hover
        @param name: name of the event ``str``
        @param object: object to be added to the event ``Object``
        @param callback: callback function to be called when the event is triggered ``function``
        @param args: arguments to be passed to the callback function ``list``
        '''
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
        f'''
        - Removes an event from the event list so it won't be called anymore
        @param name: name of the event to be removed ``str``
        '''
        
        del self.events[name]

    def isHovering(self, object):
        r'''
        - Checks if the mouse is hovering over the object
        @param object: object to be checked ``Object``
        '''
        mouse_pos = pg.mouse.get_pos()
        object_pos = object.getPos(self.surface)
        object_size = object.size

        if mouse_pos[0] > object_pos[0] and mouse_pos[0] < object_pos[0] + object_size[0] and mouse_pos[1] > object_pos[1] and mouse_pos[1] < object_pos[1] + object_size[1]:
            return True
        else:
            return False
            
    def get(self):
        f"""
        - Return Current Events, should be in the main loop
        """
        # return current event
        return pg.event.get()
    
    def on(self, event, callback, args = ()):
        r'''
        - Called when event is triggered
        @param event: event to be added ``str``
            --events : quit, mousemotion, mousedown, mouseup, keydown, keyup, mousewheel
        @param callback: callback function to be called when the event is triggered ``function``
        @param args: arguments to be passed to the callback function ``list``
        '''
        event = event.lower()
        self.base_events[event] = {"type": event, "callback": callback, "args": args}
        
    def onKey(self, type, keys, callback, args = ()):
        r'''
        - Called when key event is triggered
        @param type: type of event to be added ``str``
            --events : down, up
        @param keys: keys to be added to the event ``list``
        @param callback: callback function to be called when the event is triggered ``function``
        @param args: arguments to be passed to the callback function ``list``
        '''
        types = {
            "down" : pg.KEYDOWN,
            "up" : pg.KEYUP
        }
        t = types[type]
         
        for key in keys:
            if len(key) > 1:
                key = key.upper()
            else:
                key = key.lower()
            
            k = eval("pg.K_" + key)
            self.events[f"{key}_{type}"] = {"type": t, "key": k, "callback": callback, "args": args}
    
            
class Circle(Object):
    r'''
    @param pos: position of the circle ``list(x, y) or list("left", "top")``
    @param radius: radius of the circle ``int``
    @Keyword Arguments:
        * color= (R, G, B) ``color["white"] or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * padding= [top, right, bottom, left] ``list(top, right, bottom, left)``
    '''
    def __init__(self, pos, radius, **styles):
        super().__init__(size=[radius*2, radius*2], pos=pos, **styles)
        self.radius = radius
        
    def draw(self, surface=None):
        surface = self.surface if surface == None else surface.screen
        
        self.resolveStyle(surface)
        pg.draw.circle(surface, self.color, self.pos, self.radius)
        
        