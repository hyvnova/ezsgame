import pygame as pg, random
from colour import Color
from ezsgame.extra.components import ComponentGroup
from ezsgame.global_data import get_id, get_screen, get_drawn_objects
from ezsgame.primitive_objects import PRect
from ezsgame.styles_resolver import resolve_color, resolve_margin, resolve_size, resolve_pos


def random_color(n=1):
    """
    Return a random color if n = 1 -> (135, 6, 233)
    If n is bigger returns a list with random colors -> [(234, 55, 233), ...] 
    """
    return [random_color() for i in range(n)] if n > 1 else (random.randint(0,255), random.randint(0,255), random.randint(0,255))
       
adapt_rgb = lambda rgb: tuple(map(lambda i: i*255, rgb))
pure_rgb = lambda color: tuple(map(lambda i: i/255, color))

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
    - start: start color
    - end: end color
    - complexity: how many times to draw the gradient
    '''
    if direction not in ("v", "h"):
        raise ValueError("Direction must be either 'vertical' or 'horizontal'")
    
    start = _check_color(start)
    end = _check_color(end)
            
    _size = Size(size)
            
    colors = tuple(start.range_to(end,len(grid)))
    objs = []
    
    for i in range(len(grid)):
        if direction == "h":
            pos = [grid[i][0], 0]
            size = [grid[i][1], size[1]]
        else:
            pos = [0, grid[i][0]]
            size = [size[0], grid[i][1]]

        objs.append(PRect(pos=pos, size=size, color=adapt_rgb(colors[i].rgb), stroke=0))
        
        # if current x + width is bigger than screen width, end the loop
        if grid[i][0] + grid[i][1] > _size[0] and direction == "h":
            break
            
        # if current y + height is bigger than screen height, end the loop
        if grid[i][0] + grid[i][1] > _size[1] and direction == "v":
            break
   
    return objs, colors
        
class Gradient:
    def __init__(self, start, end, direction="horizontal", complexity=120, size=None):
        if complexity < 3:
            complexity = 3
        if complexity > 1000:
            complexity = 1000
            
        self.screen = (screen:= get_screen())
        
        _size = size if size else screen.size   
        _size = Object(pos=[0,0], size=_size).get_size()
                
        div_dir = "x" if direction == "h" else "y"    
        self.objs, self.colors = gen_gradient(_size, screen.div(div_dir, complexity, _size), start, end, direction[0].lower())
        
    def draw(self):
        for obj in self.objs:
            obj.draw()
        
    def __str__(self):
        return "<Gradient>"
    def __repr__(self):
        return "<Gradient>"

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
    def __init__(self, pos : Pos, size : Size, **styles):
        self._id = get_id()

        self.color = styles.get("color", "white")

        self.margin = styles.get("margin", [0, 0, 0, 0]) # top, right, bottom, left
        self.stroke = styles.get("stroke", 0)

        self.pos = Pos(*pos)
        self.size = Size(*size)

        self.screen = get_screen()  

        if styles.get("name"):
            self.name = styles["name"]    

        self.resolve_styles()
        
        if "components" in styles:
            self.components = ComponentGroup(self, styles["components"])         
        
        # Calls _draw() before draw()
        def _draw_before(draw_func):
            def wrapper():
                self._draw()
                draw_func()
            return wrapper
        try:
            self.draw = _draw_before(self.draw)
        except:
            pass
    
    def _get_collision_box(self):
        self.resolve_styles()
        return [self.pos, [self.pos[0] + self.size[0], self.pos[1]], 
                [self.pos[0], self.pos[1] + self.size[1]], 
                [self.pos[0] + self.size[0], self.pos[1] + self.size[1]] ] # esquina superior izq, superior derecha, infeior izq, inferior derecha       
            
    def resolve_styles(self):        
        if not isinstance(self.size, Size):
            self.size = Size(*self.size)
        if not isinstance(self.pos, Pos):
            self.pos = Pos(*self.pos)
            
        # Resolve properties
        self.color = resolve_color(self.color)
        
        self.margin = resolve_margin(self.margin)
        
        self.size = resolve_size(self.size)
        
        self.pos = resolve_pos(self.pos, self.size, self.margin)

    def get_pos(self, ref=False):
        """
        Returns postion of the object after revolsing styles
        """
        self.resolve_styles()
        self.pos = Pos(*self.pos)
        return self.pos.ref() if ref else Pos(self.pos.copy())

    def get_size(self, ref=False):
        """
        Returns size of the object after revolsing styles
        """
        self.size = Size(*self.size)
        return self.size.ref() if ref else Size(self.size.copy())
             
    def __str__(self):
        return f"<Object: {self.__class__.__name__}, ID: {self._id}>"
                 
    def _draw(self):
        r'''
        manages Object draw method
        '''
        get_drawn_objects().append(self._id)
              
class Rect(Object):
    r'''
    @param pos: position of the text ``list(x, y) or list("left", "top")``
    @param size: size of the figure ``list(width, height)``
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
        * stroke= ``int``
    '''
    def __init__(self, pos : Pos, size : Size, **styles):
        super().__init__(pos, size, **styles)
        self.border_radius = styles.get("border_radius", [0,0,0,0]) # top-left, top-right, bottom-right, bottom-left
        if len(self.border_radius) == 1:
            self.border_radius = [self.border_radius[0]] * 4
        elif len(self.border_radius) == 2:
            self.border_radius = [self.border_radius[0] * 2] * 2 + [self.border_radius[1] * 2] * 2
            
                
    def draw(self):
        pg.draw.rect(self.screen.surface, self.color, [*self.get_pos(), *self.size], int(self.stroke), *self.border_radius)
        
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
    '''
    def __init__(self, text, pos, fontsize, **styles):  
        self.path = styles.get("path", "")
        self.font = styles.get("font", "Arial")
        self.fontsize = fontsize
        self.color = styles.get("color","white")
        self.text = text    
        self.text_obj = self.load_font(text, self.font, fontsize, self.color)
        
        if "pos" in styles:
            del styles["pos"]
        if "size" in styles:
            del styles["size"]
        
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
            
    def draw(self):
        self.text_obj = self.load_font(self.text, self.font, self.fontsize, self.color)
        self.screen.surface.blit(self.text_obj, self.get_pos())

class Image(Rect):
    r'''
    @param image: image to be rendered ``str``
    @param pos: position of the image ``list(x, y) or list("left", "top")``
    @param size: size of the image ``int``
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
    '''
    def __init__(self, pos, size, image, scale=True, **styles):
        super().__init__(pos, size, **styles)
        try:
            self.image = pg.image.load(image)
        except:
            raise ValueError("Image not found in current directory: ", image)
    
        if scale:
            self.image = pg.transform.scale(self.image, self.size)
        
    def draw(self):
        self.screen.surface.blit(self.image, self.get_pos())
      
class Circle(Object):
    r'''
    @param pos: position of the circle ``list(x, y) or list("left", "top")``
    @param radius: radius of the circle ``int``
    @Keyword Arguments:
        * color= (R, G, B) ``"white" or tuple(R, G, B)``
        * margin= [top, right, bottom, left] ``list(top, right, bottom, left)``
    '''
    def __init__(self, pos, radius, **styles):
        if isinstance(radius, str):
            if radius.endswith("%"):
                radius = int(float(radius[:-1]) / 100 * get_screen().size[0])
        
        super().__init__(pos=pos, size=[radius*2, radius*2],  **styles)
        self.radius = radius
        
    def draw(self):
        pos = self.get_pos()
        pg.draw.circle(self.screen.surface, self.color, pos, self.radius)
    
    def _get_collision_box(self):
        pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1] /2]
        return [pos, [pos[0] + self.size[0], pos[1]],
                            [pos[0], pos[1] + self.size[1]], [pos[0] + self.size[0], pos[1] + self.size[1]]
                           ] # esquina superior izq, superior derecha, infeior izq, inferior derecha       
         