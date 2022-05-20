from ezsgame.objects import *
from ezsgame.extra.iobjects import IObject
from ezsgame.extra._sintax_tokens import *
from ezsgame.global_data import get_id, get_screen

def add_before(func, object, **attrs):
    def wrapper():
        for k,v in attrs.items():
            if "k" == "callback":continue
            setattr(object, k, v)        
        func()
            
    return wrapper
        
class StructuredRect(IObject):
    def __init__(self, **styles : dict):
        self.border_radius = styles.get("border_radius", [0,0,0,0]) # top-left, top-right, bottom-right, bottom-left
 
        if "image" in styles:
            if isinstance(styles["image"], str):
                self.image = Image(pos=self.pos, size=self.size, image=styles["image"])
                
                del styles["image"]
                
            else:
                raise ValueError("parameter image must be a string -> path to image")
 
        super().__init__(**{k:v for k,v in styles.items() if (not k.startswith(FUNCTION_TOKEN) )}) 
       
        if "text" in styles:
            self.text = styles['text']
            self.fontsize = styles.get("fontsize", 28)
            self.textcolor = styles.get('textcolor', "white")
            self.font = styles.get("font", "Arial")
    
            self._gen_text_obj
       
        #  FUNCTIONS
        _click_func_name = FUNCTION_TOKEN + "click"
        if _click_func_name in styles:
            func_data = styles[_click_func_name]
            self.__styles_click = dict(zip( 
                                     (keys:= [k for k in func_data.keys() if k != "callback" and k in self.__dict__.keys()]),
                                    [self.__getattribute__(k) for k in keys]))
                
            self.unclick(lambda: self.__remove_styles(self.__styles_click))
            self.click(add_before(func_data.get("callback", lambda:None), self, **func_data))
        
        _hover_func_name = FUNCTION_TOKEN + "hover"
        if _hover_func_name in styles:
            func_data = styles[_hover_func_name]
            
            self.__styles_hover = dict(zip(
                                        (keys:= [k for k in func_data.keys() if k != "callback" and k in self.__dict__.keys()]),
                                        [self.__getattribute__(k) for k in keys]))
                
            self.unhover(lambda: self.__remove_styles(self.__styles_hover))
            self.hover(add_before(func_data.get("callback", lambda:None), self, **func_data))
            
            
        # ITEMS || CHILDREN
        self.spacing = styles.get("spacing", 15)
        self._items_styles = styles.get(STYLES_CLASS_TOKEN + "items", {})
        self.align_direction = styles.get("align_direction", "horizontal")
                    
        self.items = []
        _current_y = self.pos[1] + self.size[1] + self.spacing # vertical align
        _current_x = self.pos[0] + self.spacing/2 # horizontal align
        
        width_div = self.size[0] // len(styles.get("items", [None]))  - self.spacing
        
        for item in styles.get("items", []):
            for k,v in self.__dict__["_items_styles"].items():
                if k not in item:
                    item[k] = v
            
            if self.align_direction == "vertical":
                if "size" not in item:
                    item["size"] = [(90 * self.size[0])/100, (10 * self.size[1])/100]
                    
                if "pos" not in item:
                    item["pos"] = [self.pos[0] + self.size[0]/2 - item["size"][0]/2, _current_y + self.spacing]

                item["pos"] = [item["pos"][0], _current_y]
            
                _current_y += item["size"][1] + self.spacing

            else:
                if "size" not in item:
                    item["size"] = [width_div, (90 * self.size[1])/100]
                    
                if "pos" not in item:
                    item["pos"] = [_current_x, _current_y - self.spacing/2]
                    
                item["pos"] = [_current_x, item["pos"][1]]
                
                _current_x += item["size"][0] + self.spacing
                
            self.items.append(StructuredRect(**item))

        if self.items:
            self.total_size = [self.items[-1].pos[0] + self.items[-1].size[0], self.items[-1].pos[1] + self.items[-1].size[1]]
        else:
            self.total_size = [_current_x - self.spacing/2, _current_y - self.spacing/2]
    

    def _gen_text_obj(self):
        self.text_obj = Text(text=self.text, pos=[self.pos[0], self.pos[1]], fontsize=self.fontsize, color=self.textcolor, fontname=self.font)
        # center the tex    
        self.text_obj.pos = [self.pos[0] + self.size[0]/2 - self.text_obj.size[0]/2, self.pos[1] + self.size[1]/2 - self.text_obj.size[1]/2]
           
    def __remove_styles(self, styles):
        for k,v in styles.items():
            if self.__dict__.get(k, None) != v:
                self.__setattr__(k, v)
                
        self.resolve_styles()
    
    def draw(self): 
        screen =  self.screen
                   
        # background
        pg.draw.rect(screen.surface, self.color, [*self.pos, *self.size], int(self.stroke), *self.border_radius)
        
        if hasattr(self, "image"):
            self.image.draw()
            
        if hasattr(self, "text"):
            self._gen_text_obj()
            self.text_obj.draw()
            
        for item in self.items:
            item.draw()

class Menu: 
    def __init__(self, data : dict):
        self._id = get_id()
        self.screen = get_screen()
        self.spacing = data.get("spacing", 15)
        self.pos = data.get("pos", [0,0])
        self.size = data.get("size", ["50%", "100%"])
        
        self.size = (obj:=Object(size=self.size, pos=self.pos)).get_size() 
        self.pos = obj.get_pos()

        if "background" not in data or  not isinstance(data["background"], Image) and not isinstance(data["background"], Gradient):
            self.background = PRect(screen=self.screen, pos=self.pos, size=self.size, color=data.get("background", "black"),
                                stroke=0)
        elif isinstance(data["background"], Image):
            self.background = data["background"]
            self.background.pos = self.pos
            self.background.size = self.size
            
        elif isinstance(data["background"], Gradient):
            self.background = data["background"]
             
        if "title" in data:
            title = data["title"]
            
            if "size" not in title:
                title["size"] = [(90 * self.size[0])/100, (20 * self.size[1])/100]
            
            if "pos" not in title:                
                title["pos"] = [self.pos[0] + self.size[0]/2 - title["size"][0]/2, self.pos[1] + self.spacing ]

            self.title = Text(**data["title"])
        
        self._items_styles = data.get(STYLES_CLASS_TOKEN + "items", {})
                    
        self.align_direction = data.get("align_direction", "vertical")
                    
        self.items = []
        _current_y = self.title.pos[1] + self.title.size[1] + self.spacing # vertical align
        _current_x = self.title.pos[0] + self.spacing # horizontal align
        
        width_div = self.size[0] // len(data.get("items", [None]))  - self.spacing
        
        for item in data.get("items", []):
            for k,v in self.__dict__["_items_styles"].items():
                if k not in item:
                    item[k] = v
            
            if self.align_direction == "vertical":
                if "size" not in item:
                    item["size"] = [(90 * self.size[0])/100, (10 * self.size[1])/100]
                    
                if "pos" not in item:
                    item["pos"] = [self.pos[0] + self.size[0]/2 - item["size"][0]/2, _current_y + self.spacing]

                item["pos"] = [item["pos"][0], _current_y]
            
                _current_y += item["size"][1] + self.spacing

            else:
                if "size" not in item:
                    item["size"] = [width_div, (90 * self.size[1])/100]
                    
                if "pos" not in item:
                    item["pos"] = [_current_x, self.pos[1] + self.size[1]/2 - item["size"][1]/2]
                    
                item["pos"] = [_current_x, item["pos"][1]]
                
                _current_x += item["size"][0] + self.spacing
                
            self.items.append(StructuredRect(**item))
            total_size = self.items[-1].total_size
            _current_x = total_size[0] + self.spacing
            _current_y = total_size[1] + self.spacing
            
            
    def draw(self):
        self.background.draw()
            
        if hasattr(self, "title"):
            self.title.draw()
    
        for item in self.items:
            item.draw()
