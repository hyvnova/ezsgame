import pygame as pg, json, re, copy, random
from colour import Color
from ezsgame.components import ComponentGroup
from ezsgame.global_data import get_id
from ezsgame.primitive_objects import PRect


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

        objs.append(PRect(pos=pos, size=size, color=adapt_rgb(colors[i].rgb)))
                    
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
        self.__call__(a,b)
   
    def __call__(self, a=0, b=0):
        if isinstance(a, list) or isinstance(a, tuple) or isinstance(a, Vector2):
            self._a = a[0]
            self._b = a[1]
            
        else:
            self._a = a
            self._b = b
            

    def __str__(self):
        return f"<Vector2 : {self._a}, {self._b}>"

    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        self.__current_index = 0
        return iter([self._a, self._b])

    def __next__(self):
        if self.__current_index == 0:
            self.__current_index += 1
            return self._a
        elif self.__current_index == 1:
            self.__current_index += 1
            return self._b
        else:
            raise StopIteration
        
    def __getitem__(self, index):
        if index == 0:
            return self._a
        elif index == 1:
            return self._b
        else:
            raise IndexError
        
    def __setitem__(self, index, value):
        if index == 0:
            self._a = value
        elif index == 1:
            self._b = value
        else:
            raise IndexError

    def __len__(self):
        return 2
    
    def copy(self):
        return Vector2(self._a, self._b)

    def ref(self):
        return self

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self._a == other._a and self._b == other._b
        else:
            return False
             
        
    def __ne__(self, other):
        return not self == other

class Size (Vector2):
    def __init__(self, width=0, height=0):
        super().__init__(width, height)

    @property
    def width(self):
        return self._a

    @width.setter
    def width(self, value):
        self._a = value

    @property
    def height(self):
        return self._b

    @height.setter
    def height(self, value):
        self._b = value

class Pos (Vector2):
    def __init__(self, x=0, y=0):
        super().__init__(x,y)
        
    @property
    def x(self):
        return self._a

    @x.setter
    def x(self, value):
        self._a = value

    @property
    def y(self):
        return self._b

    @y.setter
    def y(self, value):
        self._b = value

            
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
        if self.__dict__.get(property, None) != value and value:
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
        if isinstance(x, list) or isinstance(x, Vector2):
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

        # measures
        
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
            
        
    def get_pos(self, screen=None, ref=False):
        """
        Returns postion of the object after revolsing styles
        """

        screen = self.screen if screen == None else screen
        self.resolve_styles(screen)
        self.pos = Pos(*self.pos)
        return self.pos.ref() if ref else Pos(self.pos.copy())

    def get_size(self, screen=None, ref=False):
        """
        Returns size of the object after revolsing styles
        """
        screen = self.screen if screen == None else screen
        self.resolve_styles(screen)
        self.size = Size(*self.size)
        return self.size.ref() if ref else Size(self.size.copy())
             
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
         
