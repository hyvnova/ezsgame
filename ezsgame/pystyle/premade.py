import pygame as pg, random, time as t
from colour import Color
pg.init()
       
def random_color_list(n):
    r'''
    Return a list of n random colors.
    '''
    return [[random.randint(0,255), random.randint(0,255), random.randint(0,255)] for i in range(n)]

def adapt_rgb(rgb_color):
    return tuple([i*255 for i in rgb_color])

def text_to_color(color):
        r'''
        Convert a text color to rgb; "white" -> (255, 255, 255)
        - color need to exist in Color class
        @param color: color name. Example: "red"
        '''
        if isinstance(color, str):
            color = Color(color)
            return adapt_rgb(color.rgb)
        else:
            return color

def gradient(screen, start="green", end="blue", complexity=100):
    r'''
    Draw a gradient from start to end.
    - screen: screen to draw on
    - start: start color
    - end: end color
    - complexity: how many times to draw the gradient
    '''
    grid = screen.grid_div(complexity, complexity)
    color = Color(start)
    colors = list(color.range_to(Color(end),len(grid)))
    objs = []
    for i in range(len(grid)):
        objs.append(Unit(pos=grid[i][:2], size=grid[i][2:], color=adapt_rgb(colors[i].rgb)))
            
    return objs
                    
# PyStyle
class Unit:
    def __init__(self, size, pos, color, screen=None):
        self.size = size
        self.pos = pos
        self.color = color
        self.screen = screen
    
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        pg.draw.rect(screen.surface, self.color, [*self.pos, *self.size], 0)

class Object:
    def __init__(self, size, pos, **styles):
        # define general style properties
        c = styles.get("color", "white")
        if isinstance(c, str):
            c = text_to_color(c)
        self.color = c
        self.margin = styles.get("margin", [0, 0, 0, 0]) # top, right, bottom, left
        self.rounded = styles.get("rounded", 0)
        self.opacity = styles.get("opacity", 255)
        self.pos = pos
        self.size = size
        if styles.get("screen"):
            self.screen = styles["screen"]
            self.resolve_styles(self.screen)   
        if styles.get("name"):
            self.name = styles["name"]    
    
    def center(self):
        r'''
        return center position of obtect
        ''' 
        return [self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2]

    def is_colliding(self, obj, screen=None):
        screen = self.screen if screen == None else screen
        
        self.resolve_styles(screen)
        obj.resolve_styles(screen)

        collide_box = [self.pos[0] + self.margin[3], self.pos[1] + self.margin[0], self.size[0] - self.margin[1] - self.margin[3], self.size[1] - self.margin[0] - self.margin[2]]
        obj_collide_box = [obj.pos[0] + obj.margin[3], obj.pos[1] + obj.margin[0], obj.size[0] - obj.margin[1] - obj.margin[3], obj.size[1] - obj.margin[0] - obj.margin[2]]
        
        if collide_box[0] > obj_collide_box[0] + obj_collide_box[2] or collide_box[0] + collide_box[2] < obj_collide_box[0] or collide_box[1] > obj_collide_box[1] + obj_collide_box[3] or collide_box[1] + collide_box[3] < obj_collide_box[1]:
            return False
        return True
    
    def move(self, x=0, y=0, screen=None):
        screen = self.screen if screen == None else screen
        self.resolve_styles(screen) 
        self.pos[0] += x
        self.pos[1] += y * -1
     
    def is_out(self, screen=None):
        f'''
        Return True if objects is out of bounds and direction of where is objetc (top, bottom, right, left)
        '''
        screen = self.screen if screen == None else screen
        self.resolve_styles(screen)
        # should use object size
        if self.pos[0] < 0 or self.pos[0] + self.size[0] > screen.size[0]:
            return True, "right" if self.pos[0] < 0 else "left"
        elif self.pos[1] < 0 or self.pos[1] + self.size[1] > screen.size[1]:
            return True, "top" if self.pos[1] < 0 else "bottom"     
        else:
            return False, None
        
        
    def resolve_styles(self, screen=None):
        if isinstance(self.color, str):
            self.color = adapt_rgb(Color(self.color).get_rgb())
    
        screen = self.screen if screen == None else screen
            
        if isinstance(self.size, tuple):
            self.size = [self.size[0], self.size[1]]
        if isinstance(self.pos, tuple):
            self.pos = [self.pos[0], self.pos[1]]
        
        if isinstance(self.pos[0], str):
            self.pos[0] = self.pos[0].lower()
            if self.pos[0] not in ["left", "center", "right", "left-center", "right-center"]:
                raise ValueError("Invalid position value", self.pos[0])
            
        if isinstance(self.pos[1], str):
            self.pos[1] = self.pos[1].lower()
            if self.pos[1] not in ["top", "center", "bottom", "top-center", "bottom-center"]:
                raise ValueError("Invalid position value", self.pos[1])
        
        self.size = [self.size[0] - self.margin[0] - self.margin[0], self.size[1] - self.margin[1] - self.margin[1]]
        margin_x = self.margin[3] + self.margin[1]
        margin_y = self.margin[0] + self.margin[2]
        
        # align position x
        if self.pos[0] == "center":
            self.pos[0] =   screen.size[0]/2 - self.size[0]/2
        elif self.pos[0] == "right":
            self.pos[0] = screen.size[0] - self.size[0] - margin_x
        elif self.pos[0] == "right-center":
            self.pos[0] = screen.size[0] - self.size[0] / 2 - screen.center()[0]/2 - margin_x
        elif self.pos[0] == "left":
            self.pos[0] = margin_x
        elif self.pos[0] == "left-center":
            self.pos[0] = screen.center()[0] /2 - self.size[0] / 2 + margin_x
        
        # align position y
        if self.pos[1] == "center":
            self.pos[1] = screen.size[1]/2 - self.size[1]/2
        elif self.pos[1] == "top":
            self.pos[1] = margin_y
        elif self.pos[1] == "top-center":
            self.pos[1] = screen.center()[1] / 2 - self.size[1]/2  + margin_y 
        elif self.pos[1] == "bottom":
            self.pos[1] = screen.size[1] - self.size[1] - margin_y
        elif self.pos[1] == "bottom-center":
            self.pos[1] = screen.size[1] - self.size[1]/2 - screen.center()[1]/2 - margin_y
        
    def get_pos(self, screen=None):
        screen = self.screen if screen == None else screen
        self.resolve_styles(screen)
        return self.pos
                
class Rect(Object):
    r'''
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param size: size of the figure ``list(width, height)``
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * rounded= ``int``
        * screen = ``Screen``
    '''
    def __init__(self,size, pos, **styles):
        super().__init__(size, pos, **styles)
                
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        pg.draw.rect(screen.surface, self.color, [*self.get_pos(screen), *self.size], self.rounded)
        
class Text(Object):
    r'''
    @param text: text to be rendered ``str``
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param size: size of the text ``int``
    @param fontname: font name ``str``
    @param path: Path to Local Fonts are stored
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * path = path to font folder ``str``
        * screen = ``Screen``
    '''
    def __init__(self, text, pos, size, **styles):  
        self.path = styles.get("path", "")
        self.fontname = styles.get("fontname", "Arial")
        self.fontsize = size
        self.color = styles.get("color","white")
        self.innertext = text
        self.text = self.font(text, self.fontname, size, self.color)
        super().__init__(size=[self.text.get_width(), self.text.get_height()], pos=pos, **styles)
        
    def font(self, text, name, size, color="white"):
        # load local font 
        pg.font.init()
        name = name.lower()
        # if font in system fonts
        if name in pg.font.get_fonts():
            font = pg.font.SysFont(name, size)
        else:
            raise Exception("Font not found", name)
                
        return font.render(text, True, color)
            
    def update(self, **atributes):
        self.text = self.font(atributes.get("text", self.innertext), self.fontname, self.fontsize, atributes.get("color", self.color))
        self.size = [self.text.get_width(), self.text.get_height()]
        self.color = atributes.get("color", self.color)
        self.fontname = atributes.get("fontname", self.fontname)
        self.fontsize = atributes.get("fontsize", self.fontsize)
        self.margin = atributes.get("margin", self.margin)
        self.pos = atributes.get("pos", self.pos)
            
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen    
        screen.surface.blit(self.text, self.get_pos(screen))

class Image(Rect):
    r'''
    @param image: image to be rendered ``str``
    @param pos: position of the image ``list(x, y) or list("left", "top")``
    @param size: size of the image ``int``
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * screen = ``Screen``
    '''
    def __init__(self, image, pos, size, **styles):
        super().__init__(size, pos, **styles)
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, self.size)
        
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        screen.surface.blit(self.image, self.get_pos(screen))
      
class EventHandler:
    r'''
    - Manages events on the app 
    '''
    def __init__(self, screen):
        self.screen = screen
        self.events  = {}
        self.base_events = {}
                                            
    def check(self, event, screen=None):
        screen = self.screen if screen == None else screen
                
        self.events = {k:v for k,v in self.events.items() if v != None}
        
        for ev in event:
            # BASE EVENTS ----------------------------------------------------------------------------------
            if ev.type == pg.QUIT:
                if "quit" in self.base_events:
                    self.base_events["quit"]["callback"]()
                pg.quit()
                quit()
                
            if ev.type == pg.MOUSEMOTION:
                if "mousemotion" in self.base_events:
                    self.base_events["mousemotion"]["callback"]()
                
            if ev.type == pg.MOUSEBUTTONDOWN:
                if "mousedown" in self.base_events:
                    self.base_events["mousedown"]["callback"]()
                    
            if ev.type == pg.MOUSEBUTTONUP:
                if "mouseup" in self.base_events:
                    self.base_events["mouseup"]["callback"]()
                    
            if ev.type == pg.KEYDOWN:
                if "keydown" in self.base_events:
                    self.base_events["keydown"]["callback"]()
                
            if ev.type == pg.KEYUP:
                if "keyup" in self.base_events:
                    self.base_events["keyup"]["callback"]()
                            
            # STORED EVENTS --------------------------------------------------------------------------------
            for key, value in self.events.items():
                # onclick, onhover
                if value["type"] == 1025 or value["type"] == 1026:
                    if self.is_hovering(value["object"]):
                        self.events[key]["callback"]()
                        continue                
                    
                #key up or down
                elif value["type"] == pg.KEYDOWN and ev.type == pg.KEYDOWN:
                    if ev.key == value["key"]:
                        self.events[key]["callback"]()
                        continue
                    
                elif value["type"] == pg.KEYUP and ev.type == pg.KEYUP:
                    if ev.key == value["key"]:
                        self.events[key]["callback"]()
                        continue
                                            
    def add_event_listener(self,name, event, object, callback):
        r'''
        - Adds a event listener to a object
        @param event: event to be added ``str``
            --events : click, hover
        @param name: name of the event ``str``
        @param object: object to be added to the event ``Object``
        @param callback: callback function to be called when the event is triggered ``function``
        '''
        evs  = {
            "click" : 1025,
            "hover" : 1024
        }
        if event in evs:
            event = evs[event]
        else:
            raise Exception("Event type not found", event)
        
        self.events[name] = {"type": event, "object": object, "callback": callback}

    def remove(self, name):
        f'''
        - Removes an event from the event list so it won't be called anymore
        @param name: name of the event to be removed ``str``
        '''
        del self.events[name]

    def is_hovering(self, object):
        r'''
        - Checks if the mouse is hovering over the object
        @param object: object to be checked ``Object``
        '''
        mouse_pos = pg.mouse.get_pos()
        object_pos = object.get_pos(self.screen)
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
    
    def on(self, event, callback):
        r'''
        - Called when event is triggered
        @param event: event to be added ``str``
            --events : quit, mousemotion, mousedown, mouseup, keydown, keyup, mousewheel
        @param callback: callback function to be called when the event is triggered ``function``
        '''
        event = event.lower()
        self.base_events[event] = {"type": event, "callback": callback}
        
    def on_key(self, type, keys, callback):
        r'''
        - Called when key event is triggered
        @param type: type of event to be added ``str``
            --events : down, up
        @param keys: keys to be added to the event ``list``
        @param callback: callback function to be called when the event is triggered ``function``
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
            self.events[f"{key}_{type}"] = {"type": t, "key": k, "callback": callback}
            
class Circle(Object):
    r'''
    @param pos: position of the circle ``list(x, y) or list("left", "top")``
    @param radius: radius of the circle ``int``
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * screen = ``Screen`` 
    '''
    def __init__(self, pos, radius, **styles):
        super().__init__(size=[radius*2, radius*2], pos=pos, **styles)
        self.radius = radius
        
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        pos = self.get_pos(screen)
        pg.draw.circle(screen.surface, self.color, pos, self.radius)
        
class TimeHandler:
    r'''
    - Handles the time events
    '''
    def __init__(self):
        self.intervals = {}
        self.start_time = t.time()
        self.time = 0
        self.to_remove = []

    def add(self, name, time, callback):
        r'''
        - Adds event that will be called every time the time is reached
        @param name: name of the event ``str``
        @param time: time to be called ``int`` in miliseconds
        @param callback: callback function to be called when the event is triggered ``function``
        '''
        time = time / 1000
        self.intervals[name] = {"callback": callback, "time": time, "last_call": t.time()}
        
    def remove(self, name):
        r'''
        - Removes an event from the event list so it won't be called anymore
        @param name: name of the event to be removed ``str``
        '''
        self.to_remove.append(name)
        
    def check(self):
        r'''
        - Checks if the time is reached and calls the event
        '''
        for name in self.to_remove:
            if name in self.intervals:
                del self.intervals[name]
        
        for key, value in self.intervals.items():
            if t.time() - value["last_call"] >= value["time"]:
                self.intervals[key]["last_call"] = t.time()
                self.intervals[key]["callback"]()
    

        
    