import pygame as pg, random, time as t, json, re, copy
from colour import Color, color_scale
from ezsgame.components import ComponentGroup
from ezsgame.global_data import get_id


def random_color(n=1):
    """
    Return a random color if n = 1 -> (135, 6, 233)
    If n is bigger returns a list with random colors -> [(234, 55, 233), ...] 
    """
    return [random_color() for i in range(n)] if n > 1 else (random.randint(0,255), random.randint(0,255), random.randint(0,255))
       
adapt_rgb = lambda rgb: tuple(map(lambda i: i*255, rgb))
pure_rgb = lambda color: tuple(map(lambda i: i/255, color))

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

def _check_color(color):
    if isinstance(color, str):
            return Color(color)
   
    elif not (isinstance(color, tuple) or isinstance(color, list)):
        raise ValueError("Color must be a tuple or a list, or color name: ", color)

    else:
        return Color(rgb=pure_rgb(color))
       
def gen_gradient(size, grid, start="green", end="blue", direction="v"):
    r'''
    Draw a gradient from start to end.
    - screen: screen to draw on
    - start: start color
    - end: end color
    - complexity: how many times to draw the gradient
    '''
    if direction not in ("v", "h"):
        raise ValueError("Direction must be either 'vertical' or 'horizontal'")
    
    start = _check_color(start)
    end = _check_color(end)
            
    colors = tuple(start.range_to(end,len(grid)))
    objs = []
    for i in range(len(grid)):
        if direction == "h":
            pos = [grid[i][0], 0]
            size = [grid[i][1], size[1]]
        else:
            pos = [0, grid[i][0]]
            size = [size[0], grid[i][1]]

        objs.append(Unit(pos=pos, size=size, color=adapt_rgb(colors[i].rgb)))
            
    return objs, colors
        
class Gradient:
    def __init__(self, screen, start, end, direction="horizontal", complexity=120):
        if complexity < 3:
            complexity = 3
        if complexity > 1000:
            complexity = 1000
            
        div_dir = "x" if direction == "h" else "y"    
        self.objs, self.colors = gen_gradient(screen.size, screen.div(div_dir, complexity), start, end, direction[0].lower())
        
    def __str__(self):
        return "<Gradient>"
    def __repr__(self):
        return "<Gradient>"


percent = lambda n, total: (n * total)/100
_to_percent = lambda n, total: percent(float(n.replace("%", "")), total) if isinstance(n, str) and re.match(r"[0-9]+%$", n) else n
 
class Vector2:
    def __init__(self, a=0, b=0):
        if isinstance(a, list):
            self.__a = a[0]
            self.__b = a[1]
            
        else:
            self.__a = a
            self.__b = b
   
    def __str__(self):
        return [self.__a, self.__b]

    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        self.__current_index = 0
        return iter([self.__a, self.__b])

    def __next__(self):
        if self.__current_index == 0:
            self.__current_index += 1
            return self.__a
        elif self.__current_index == 1:
            self.__current_index += 1
            return self.__b
        else:
            raise StopIteration
        
    def __getitem__(self, index):
        if index == 0:
            return self.__a
        elif index == 1:
            return self.__b
        else:
            raise IndexError
        
    def __setitem__(self, index, value):
        if index == 0:
            self.__a = value
        elif index == 1:
            self.__b = value
        else:
            raise IndexError

    def __len__(self):
        return 2

class Size (Vector2):
    def __init__(self, width=0, height=0):
        super().__init__(width, height)

        self.width, self.height  = width, height

    @property
    def width(self):
        self.width = self.__a
        return self.__a

    @width.setter
    def width(self, value):
        self.__a = value

    @property
    def height(self):
        self.height = self.__b
        return self.__b

    @height.setter
    def height(self, value):
        self.__b = value

class Pos (Vector2):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)

        self.x, self.y  = x,y

    @property
    def x(self):
        self.x = self.__a
        return self.__a

    @x.setter
    def x(self, value):
        self.__a = value

    @property
    def y(self):
        self.y = self.__b
        return self.__b

    @y.setter
    def y(self, value):
        self.__b = value
              
class Unit:
    def __init__(self, pos, size, color, screen=None):
        self.size = Size(*size)
        self.pos = Pos(*pos)
        self.color = color
        self.screen = screen
        self._id = get_id()
    
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        if isinstance(self.color, str):
            self.color = adapt_rgb(Color(self.color).get_rgb())
        pg.draw.rect(screen.surface, self.color, [*self.pos, *self.size], 0)

class Object:
    def __init__(self, pos, size, **styles):
        self._id = get_id()

        c = styles.get("color", "white")
        if isinstance(c, str):
            c = text_to_color(c)
        self.color = c

        self.margin = styles.get("margin", [0, 0, 0, 0]) # top, right, bottom, left
        self.stroke = styles.get("stroke", 0)

        self.pos = Pos(*pos)
        self.size = Size(*size)

        if styles.get("screen"):
            self.screen = styles["screen"]
            self.resolve_styles(self.screen)   

        if styles.get("name"):
            self.name = styles["name"]    

        self._current = 0
        self._animation_done = False

        if "components" in styles:
            self.components = ComponentGroup(self, styles["components"])
            
    def set(self, property, value):
        r'''
        sets a object property to a valie
        '''
        if self.__dict__[property] != value and value:
            self.__dict__[property] = value
        else:
            return
    
    def load_style_pack(self, pack, ignore_exceptions=True):
            try:
                for k,v in pack.items():
                    if k == "color":
                        if isinstance(v, str):
                            v = adapt_rgb(Color(v).get_rgb())
                    self.set(k,v)
            except Exception as e:
                if ignore_exceptions:
                    return
                else:
                    raise Exception(e)
    
    def load_animation(self, file, time, screen, repeat=False, ignore_exceptions=True):
        screen = self.screen if screen == None else screen
        if screen == None:
            raise Exception(f"load_animation function needs screen (ID : {self._id})")
        
        self._repeat_animation = repeat
        
        self._animation_eventname = f"object.{self._id}.load_animation.{time}"
        screen.time.add(time, lambda:self._load_animation(file, screen, ignore_exceptions), self._animation_eventname)

    def _load_animation(self, file, screen, ignore_exceptions):
        try:
            if self._animation_done:
                if self._repeat_animation:
                    self._current = 0
                    self._animation_done = False
                else:
                    screen.time.remove(self._animation_eventname) 
                    return
                
            with open(file, "r") as f:
                animation  = json.load(f)
            
            try:
                self._current_animation_point = [*animation.keys()][self._current] 
            except:
                self._animation_done = True 
                return
                
            self.load_style_pack(animation[self._current_animation_point])
            self._current += 1
            
        except Exception as e:
                if ignore_exceptions:
                    return
                else:
                    raise Exception(e)
    
    def _get_collision_box(self):
        self.resolve_styles(self.screen)
        return [self.pos, [self.pos[0] + self.size[0], self.pos[1]],
                [self.pos[0], self.pos[1] + self.size[1]], [self.pos[0] + self.size[0], self.pos[1] + self.size[1]]
                ] # esquina superior izq, superior derecha, infeior izq, inferior derecha       
        
    def is_colliding(self, obj, screen=None, draw_collision_box=False):
        r'''
        returns True if the object is colliding with another object, False if not
        '''
        
        screen = self.screen if screen == None else screen    
        obj_pos = obj.get_pos(screen)
    
        for i in self._get_collision_box():
            if draw_collision_box:
                Rect(pos=[obj_pos[0]-2, obj_pos[1]-2], size=[obj.size[0]+4, obj.size[1]+4], color="red", stroke=2).draw(screen)
                Rect(pos=[self.pos[0]-2, self.pos[1]-2], size=[self.size[0]+4, self.size[1]+4], color="red", stroke=2).draw(screen)
                
            if (i[0] >= obj.pos[0] and i[0] <= obj.pos[0]+obj.size[0]) and (i[1] >= obj.pos[1] and i[1] <= obj.pos[1] + obj.size[1]):
                return True
            
        return False
            
    def copy(self, different=False):
        obj = copy.copy(self)
        if different:
            obj._id = get_id()
        return obj

    def move(self, x=0, y=0):
        r'''
        Adds x,y to the current object position. (Also inverts y )
        '''        
        if isinstance(x, list) or isinstance(x, tuple):
            x, y = x

        self.pos[0] += x
        self.pos[1] += y * -1
    
    def is_out(self, screen=None):
        r'''
        Return True if objects is out of bounds and direction of that bound (top, bottom, right, left)
        -> [bool, "direction"]
        '''
        screen = self.screen if screen == None else screen
        self.resolve_styles(screen)
        
        if self.pos[0] + self.size[0] < 0 or self.pos[0] - self.size[0]/4 > screen.size[0]:
            return True, "left" if self.pos[0] + self.size[0]/2 <= 0 else "right"
        elif self.pos[1] + self.size[1] < 0 or self.pos[1] - self.size[1]/4 > screen.size[1]:
            return True, "top" if self.pos[1] + self.size[1] <= 0 else "bottom"     
        else:
            return False, None
       
    def resolve_styles(self, screen=None):
        screen = self.screen if screen == None else screen
        
        #units, percents and other measures
        
        if type(self.size) == tuple:
            self.size = list(self.size)
        
        for i in range(len(self.size)):
            self.size[i] = _to_percent(self.size[i], screen.size[i])
                    
        for i in range(len(self.pos)):
            self.pos[i] = _to_percent(self.pos[i], screen.size[i])
                             
        screen_i = 0
        for i in range(len(self.margin)):
            self.margin[i] = _to_percent(self.margin[i], screen.size[screen_i])
            screen_i += 1
            if screen_i == 2:
                screen_i = 0
         
        # colors
        if isinstance(self.color, str):
            self.color = adapt_rgb(Color(self.color).get_rgb())
    
        if isinstance(self.size, tuple):
            self.size = [self.size[0], self.size[1]]
        if isinstance(self.pos, tuple):
            self.pos = [self.pos[0], self.pos[1]]
            
        
        if isinstance(self.pos[0], str):
            self.pos[0] = self.pos[0].lower()
            if self.pos[0] not in ["left", "center", "right", "left-center", "right-center"]:
                raise ValueError("Invalid x-axis position value", self.pos[0])
            
        if isinstance(self.pos[1], str):
            self.pos[1] = self.pos[1].lower()
            if self.pos[1] not in ["top", "center", "bottom", "top-center", "bottom-center"]:
                raise ValueError("Invalid y-axis position value", self.pos[1])
        
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
            
        # apply alpha
        
    def get_pos(self, screen=None):
        """
        Returns postion of the object after revolsing styles
        """

        screen = self.screen if screen == None else screen
        self.resolve_styles(screen)
        return self.pos
             
    def __str__(self):
        return f"<Object: {self.__class__.__name__}, ID: {self._id}>"
    
    def __repr__(self):
        return f"<Object: {self.__class__.__name__}, ID: {self._id}>"
               
class Rect(Object):
    r'''
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param size: size of the figure ``list(width, height)``
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * stroke= ``int``
        * screen = ``Screen``
    '''
    def __init__(self, pos, size, **styles):
        super().__init__(pos, size, **styles)
                
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        pg.draw.rect(screen.surface, self.color, [*self.get_pos(screen), *self.size], int(self.stroke))
        
class Text(Object):
    r'''
    @param text: text to be rendered ``str``
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param fontsize: text size ``int``
    @param fontname: font name ``str``
    @param path: Path to Local Fonts are stored
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * path = path to font folder ``str``
        * screen = ``Screen``
    '''
    def __init__(self, text, pos, fontsize, **styles):  
        self.path = styles.get("path", "")
        self.font = styles.get("font", "Arial")
        self.fontsize = fontsize
        self.color = styles.get("color","white")
        self.text = text    
        self.text_obj = self.load_font(text, self.font, fontsize, self.color)
        super().__init__(pos=pos, size=[self.text_obj.get_width(), self.text_obj.get_height()], **styles)
        
    def load_font(self, text, name, size, color="white"):
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
        self.text = atributes.get("text", self.text)
        self.size = atributes.get("size", [self.text_obj.get_width(), self.text_obj.get_height()])
        self.color = atributes.get("color", self.color)
        self.font = atributes.get("font", self.font)
        self.fontsize = atributes.get("fontsize", self.fontsize)
        self.margin = atributes.get("margin", self.margin)
        self.pos = atributes.get("pos", self.pos)
            
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen   
        self.text_obj = self.load_font(self.text, self.font, self.fontsize, self.color)
        screen.surface.blit(self.text_obj, self.get_pos(screen))

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
    def __init__(self, pos, size, image, **styles):
        super().__init__(pos, size, **styles)
        try:
            self.image = pg.image.load(image)
        except:
            raise Exception("Image not found in current directory: ", image)
    
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
        self.to_remove = {"events": [], "base_events": []}
        self.to_add = {"events": [], "base_events": []}
                                            
    def check(self, event, screen=None):
        screen = self.screen if screen == None else screen
        self.events = {k:v for k,v in self.events.items() if v != None}
        
        # remove events
        for name in self.to_remove["events"]:
            if name in self.events:
                del self.events[name]
            
        for name in self.to_remove["base_events"]:
            for i in self.base_events:
                for item in self.base_events[i]:
                    if item["name"] == name:
                        self.base_events[i].pop(self.base_events[i].index(item))
                        break
        self.to_remove = {"events": [], "base_events": []}
                    
        # add events
        for item in self.to_add["events"]:
            self.events[item[0]] = item[1]
            
        for item in self.to_add["base_events"]:
            self.base_events[item[0]].append(item[1])
        
        self.to_add = {"events": [], "base_events": []}
        
        for ev in event:
            # BASE EVENTS ----------------------------------------------------------------------------------
            if ev.type == pg.QUIT:
                for i in self.base_events.get(pg.QUIT, ""):
                    if i["type"] == pg.QUIT:
                        i["callback"]()
                        break
                    
                pg.quit()
                quit()
                              
            for base_event in self.base_events:
                if ev.type == base_event:
                    for item in self.base_events.get(base_event, None):
                        if base_event == pg.KEYDOWN:
                            self.pressed_key = [ev.unicode, ev.key]
                        item["callback"]()
                                    
            # STORED EVENTS --------------------------------------------------------------------------------
            for key, value in self.events.items():
                if value["type"] == ev.type:
                    if "key" in value:
                        if ev.key == value["key"]:
                            value["callback"]()
                    else:
                        if value["evname"] == "unhover":
                            if self.is_hovering(value["object"]) == False:  
                                    self.events[key]["callback"]()
                        else:               
                            if self.is_hovering(value["object"]):
                                value["callback"]()
            
      
    def get_pressed_key(self):
        r'''
        Return the pressed key -> [key, unicode]
        '''
        return self.pressed_key
                                            
    def add_event_listener(self, event, object, callback, name="Default"):
        r'''
        - Adds a event listener to a object
        @param event: event to be added ``str``
            --events : (mousedown or click), hover, unhover, (mouseup or unclick).
        @param name: name of the event ``str``
        @param object: object to be added to the event ``Object``
        @param callback: callback function to be called when the event is triggered ``function``
        '''
     
        event = event.lower()
        event_ = self._convert_to_pgevent(event)
        
        if name == "Default":
            name = f"{event}.{object._id}.{len(self.events)}"
            
        self.to_add["events"].append([name, {"type": event_, "object": object, "callback": callback, "evname" : event}])

    def remove(self, name):
        f'''
        - Removes an event from the event list so it won't be called anymore
        @param name: name of the event to be removed ``str``
        '''
        self.to_remove["events"].append(name)

    def is_hovering(self, object):
        r'''
        - Checks if the mouse is hovering over the object
        @param object: object to be checked ``Object``
        '''
        mouse_pos = pg.mouse.get_pos()
        box = object._get_collision_box()
        
        if mouse_pos[0] > box[0][0] and mouse_pos[0] < box[1][0]:
            if mouse_pos[1] > box[0][1] and mouse_pos[1] < box[2][1]:
                return True
            
        return False
            
    def get(self):
        f"""
        - Return Current Events, should be in the main loop
        """
        # return current event
        return pg.event.get()
    
    def on(self, event, callback, name="Default"):
        r'''
        - Called when event is triggered
        @param event: event to be added ``str``
            --events : quit, mousemotion, mousedown, mouseup, keydown, keyup, mousewheel
        @param callback: callback function to be called when the event is triggered ``function``
        @param name: name of event object, used to removed the event if needed
        '''
        event = event.lower()
    
        event_ = self._convert_to_pgevent(event)
        
        if event not in self.base_events:
            self.base_events[event_] = []
        name = f"base_event.{event}.{len(self.base_events)}" if name == "Default" else name
        
        self.to_add["base_events"].append([event_, {"type": event_, "callback": callback, "name":name}])
        
    def remove_base_event(self, name):
        self.to_remove["base_events"].append(name)
                   
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
        if type not in types:
            raise Exception(f"{type} is not a valid on_key event type.")
        
        t = types[type]
         
        for key in keys:
            if key.lower() in ["multiply", "minus", "plus", "enter"]:
                key = "KP_" + key.upper()
            elif len(key) > 1:
                key = key.upper()
              
            else:
                key = key.lower()
            
            k = eval("pg.K_" + key)
            self.events[f"{key}_{type}_{len(self.events)}"] = {"type": t, "key": k, "callback": callback}
            
    def _base_event_index(self, type, item):
        for i in range(len(self.base_events[type])):
            if self.base_events[type][i]["name"] == item["name"]:
                return i
                    
    def _convert_to_pgevent(self, event):
        evs  = {
            "hover" : pg.MOUSEMOTION,
            "click" : pg.MOUSEBUTTONDOWN,
            "mousedown" : pg.MOUSEBUTTONDOWN,
            "mouseup" : pg.MOUSEBUTTONUP,
            "unhover" : pg.MOUSEMOTION,
            "unclick" : pg.MOUSEBUTTONUP,
            "keydown" : pg.KEYDOWN,
            "keyup" : pg.KEYUP,
            "mousewheel" : pg.MOUSEWHEEL,
            "mousemotion" : pg.MOUSEMOTION,
            "quit" : pg.QUIT,
            "mousebuttondown" : pg.MOUSEBUTTONDOWN,
            "mousebuttonup" : pg.MOUSEBUTTONDOWN,
            "mousewheelup" : pg.MOUSEBUTTONDOWN
        }
        if event not in evs:
            raise Exception("Event type not found", event)
        return evs[event]
                    
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
        if isinstance(radius, str):
            if re.match(r"[0-9]+%", radius):
                raise Exception(f"Radius cannot be a percent (ID : {self._id})")
        
        super().__init__(pos=pos, size=[radius*2, radius*2],  **styles)
        self.radius = radius
        
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        pos = self.get_pos(screen)
        pg.draw.circle(screen.surface, self.color, pos, self.radius)
    
    def _get_collision_box(self):
        pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1] /2]
        return [pos, [pos[0] + self.size[0], pos[1]],
                            [pos[0], pos[1] + self.size[1]], [pos[0] + self.size[0], pos[1] + self.size[1]]
                           ] # esquina superior izq, superior derecha, infeior izq, inferior derecha       
         
class TimeHandler:
    r'''
    - Handles the time events
    '''
    def __init__(self):
        self.intervals = {}
        self.start_time = t.time()
        self.time = 0
        self.to_remove = []
        self.to_add = []

    def add(self, time, callback, name="Default"):
        r'''
        - Adds event that will be called every time the time is reached
        @param name: name of the event ``str``
        @param time: time to be called ``int`` in miliseconds
        @param callback: callback function to be called when the event is triggered ``function``
        '''
        time = time / 1000
        name = f"{len(self.intervals)}.{time}" if name == "Default" else name
        self.to_add.append([name, {"callback": callback, "time": time, "last_call": t.time()}])

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
        self.to_remove = []
                
        for item in self.to_add:
            self.intervals[item[0]] = item[1]
        self.to_add = []
        
        
        for key, value in self.intervals.items():
            if t.time() - value["last_call"] >= value["time"]:
                self.intervals[key]["last_call"] = t.time()
                self.intervals[key]["callback"]()
    
