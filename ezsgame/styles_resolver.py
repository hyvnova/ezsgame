from colour import Color
from .global_data import get_screen

adapt_rgb = lambda rgb: tuple(map(lambda i: i*255, rgb))

def center_of(obj):
    r'''
    #### Returns the center postion of the object
    - obj : object -> object
    '''
    return [obj.pos[0] + obj.size[0]/2, obj.pos[1] + obj.size[1]/2]

def resolve_measure(measure, size):
    if isinstance(measure, str):
        if measure.endswith("%"):
            return float(measure[:-1]) * size / 100
        
        else:
            raise ValueError("Invalid measure value", measure)
    
    return measure 

def resolve_color(color):   
    if isinstance(color, str):
        if color.startswith("#"):
            return adapt_rgb(Color(color).rgb)
        
        return adapt_rgb(Color(color).get_rgb())
    
    return color

def resolve_margin(margin):
    screen = get_screen()

    for i,m in enumerate(margin):
        screen_i = 0 if i%2 == 0 else 1        

        margin[i] = resolve_measure(m, screen.size[screen_i])

    return margin

def resolve_size(size):
    screen = get_screen()
    
    # if only 1 axis is given, use it for both axis
    if len(size) == 1:
        size = [size[0],size[0]]

    for i,s in enumerate(size):
        screen_i = 0 if i%2 == 0 else 1

        size[i] = resolve_measure(s, screen.size[screen_i])
   
    return size

def resolve_pos(pos,size, margin):
    screen = get_screen()
    
    if len(pos) == 1:
        pos = [pos[0],pos[0]]

    margin_x = margin[3] + margin[1]
    margin_y = margin[0] + margin[2]
    
    screen_center = center_of(screen)
    
    # align position x
    
    if isinstance(pos[0], int) or isinstance(pos[0], float):
        pos[0] += margin_x 

    elif isinstance(pos[0], str):
        if pos[0].endswith("%"):
            pos[0] = float(pos[0][:-1]) * screen.width / 100

        else:
            pos[0] = pos[0].lower()
            
            if pos[0] not in ["left", "center", "right", "left-center", "right-center"]:
                    raise ValueError("Invalid x-axis position value", pos[0])
                
            if pos[0] == "center":
                pos[0] =   screen.size[0]/2 - size[0]/2
            elif pos[0] == "right":
                pos[0] = screen.size[0] - size[0] - margin_x
            elif pos[0] == "right-center":
                pos[0] = screen.size[0] - size[0] / 2 - screen_center[0]/2 - margin_x
            elif pos[0] == "left":
                pos[0] = margin_x
            elif pos[0] == "left-center":
                pos[0] = screen_center[0]/2 - size[0] / 2 + margin_x
        
        
    # align position y
    if isinstance(pos[1], int) or isinstance(pos[1], float):
        pos[1] += margin_y
    
    elif isinstance(pos[1], str):
        if pos[1].endswith("%"):
            pos[1] = float(pos[1][:-1]) * screen.height / 100
        
        else:
            pos[1] = pos[1].lower()        
            
            if pos[1] not in ["top", "center", "bottom", "top-center", "bottom-center"]:
                raise ValueError("Invalid y-axis position value", pos[1])
            
            if pos[1] == "center":
                pos[1] = screen.size[1]/2 - size[1]/2
            elif pos[1] == "top":
                pos[1] = margin_y
            elif pos[1] == "top-center":
                pos[1] = screen_center[1]/ 2 - size[1]/2  + margin_y 
            elif pos[1] == "bottom":
                pos[1] = screen.size[1] - size[1] - margin_y
            elif pos[1] == "bottom-center":
                pos[1] = screen.size[1] - size[1]/2 - screen_center[1]/2 - margin_y
                    
                    
    return pos

