from typing import List
from .global_data import get_id, get_screen
import pygame as pg, os, subprocess

def outline(obj, color="red", stroke:int=1, size:int=1.5, border_radius:list = [0,0,0,0]):
    r'''
    #### Draws an outline of the object
    - `color` : the color of the outline `White`or `(R,G,B)`
    - `stroke` : the width of the outline `int`
    - `size` : the size  multiplier of the outline (object size * outline size) `int`
    - `border_radius` : the radius of the corners of the outline `[top_left, top_right, bottom_left, bottom_right]`

    #### Note: Automaticly draws the outline when declared
    '''
    
    obj_size = obj.get_size()
    obj_pos = obj.get_pos()

    size = [obj_size[0] * size, obj_size[1] * size]
    pos = [obj_pos[0] - (size[0] - obj_size[0]) / 2, obj_pos[1] - (size[1] - obj_size[1]) / 2]

    pg.draw.rect(get_screen().surface, color, [*pos, *size], stroke, *border_radius)

def copy(obj, different=False):
    new_obj = copy.copy(obj)
    if different:
        new_obj.id = get_id()
    return obj
    
def is_out(obj):
    r'''
    Return True if objects is out of bounds and direction of that bound (top, bottom, right, left)
    -> [bool, "direction"]
    '''
    screen = get_screen()
    
    if obj.pos[0] + obj.size[0] < 0 or obj.pos[0] - obj.size[0]/4 > screen.size[0]:
        return True, "left" if obj.pos[0] + obj.size[0]/2 <= 0 else "right"
    elif obj.pos[1] + obj.size[1] < 0 or obj.pos[1] - obj.size[1]/4 > screen.size[1]:
        return True, "top" if obj.pos[1] + obj.size[1] <= 0 else "bottom"     
    else:
        return False, None
    
def move(obj, x=0, y=0):
    r'''
    #### Adds x,y to the current object position. (Also inverts y )
    - x : int, float or list -> value to add to x-axis
    - y : int, float -> value to add to y-axis
    '''     
    if obj.behavior.get("pos", "dynamic") == "static":
        return

    try:
        x,y = x[0], x[1]
    except:
        pass

    obj.pos[0] += x
    obj.pos[1] += y * -1
    
def is_colliding(obj1, obj2, draw_collision_box=False):
    r'''
    #### returns True if the object is colliding with another object, False if not
    - obj1 : object -> first object
    - obj2 : object -> second object
    - draw_collision_box : bool -> if True, draw collision box
    '''
    
    if draw_collision_box:
        outline(obj1, size=1.1, stroke=2)
        outline(obj2, size=1.1, stroke=2)

    for i in obj1._get_collision_box():    
        if (i[0] >= obj2.pos[0] and i[0] <= obj2.pos[0]+obj2.size[0]) and (i[1] >= obj2.pos[1] and i[1] <= obj2.pos[1] + obj2.size[1]):
            return True
                
        
    return False


def build(
    file,
    oneFile: bool = True,
    based: bool = True,
    icon: str = None,
    output: str = os.path.join(os.getcwd(), "build")
    ) :

    
    if not os.path.exists(output):
        os.mkdir(output)
        
    args = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        ("--onedir", "--onefile")[oneFile],
        ("--console", "--windowed")[based],
        (*(f"--icon", icon), None)[icon is None],
        
        "--add-data", 
        f"{os.getcwd()}\\ezsgame;ezsgame", # Folder
        
        "--add-data",
        f"{os.getcwd()}\\ezsgame\\assets;icon.jpg", # File
    
        "--add-data",
        f"{os.getcwd()};audio.mp3",

        "--add-data",
        f"{os.getcwd()};wakeup.png",
        
        f"{os.getcwd()}\\{file}", # File
        
    ]
    
    # Clear a None value in args
    args = [x for x in args if x is not None]
    subprocess.run(args, cwd=output)
    

def center(parent, obj, x_axis=True, y_axis=True):
    r'''
    #### Centers an object in the parent object
    - parent : object -> parent object
    - obj : object -> object to center
    - x_axis : bool -> if True, center x-axis
    - y_axis : bool -> if True, center y-axis
    '''
    if x_axis:
        obj.pos[0] = parent.pos[0] + (parent.size[0] - obj.size[0]) / 2
    if y_axis:
        obj.pos[1] = parent.pos[1] + (parent.size[1] - obj.size[1]) / 2
        
        
def div(axis : str, q : int, size : float = None) -> List[List[float]]:
		r'''
		#### Returns a list of division points of the screen in the given axis
		
		- `axis` : axis to divide the screen in (`x` or `y`)
		- `q` : number of divisions
		- `size` : Size of where to divide the screen, works as a delimiter (Optional)
        - `pos_prefix` : Position to add to the division points (Optional)
		'''
		
		divs = []
		if axis == "x":
			step = size[0] / q
			
			for i in range(q):
				divs.append([round(i * step, 1), round((i + 1) * step, 1) ])
				
				# if overflows 
				if divs[-1][1] > size[0]:
					break
				
		elif axis == "y":
			step = size[1] / q

			for i in range(q):
				divs.append([round(i * step, 1), round((i + 1) * step, 1)])
		
				# if overflows
				if divs[-1][1] > size[1]:
					break
				
		return divs

# Positioning functions
def center_of(obj) -> List[float]:
    r'''
    #### Returns the center postion of the object
    - obj : object -> object
    '''
    return [obj.pos[0] + obj.size[0]/2, obj.pos[1] + obj.size[1]/2]


def center(obj, parent, x: bool = True, y: bool = True):
    r'''
    #### Centers an object in the parent object
    - obj : object -> object to center
    - parent : object -> parent object
    - x -> if True, center x-axis
    - y -> if True, center y-axis
    '''
    if x:
        obj.pos[0] = parent.pos[0] + (parent.size[0] - obj.size[0]) / 2
    if y:
        obj.pos[1] = parent.pos[1] + (parent.size[1] - obj.size[1]) / 2



def is_hovering(obj):
    """
    #### Returns True if the mouse is hovering over the object, False if not
    - obj : object -> object
    """

    box = obj._get_collision_box()
    
    mouse_pos = pg.mouse.get_pos()
    
    if mouse_pos[0] >= box[0][0] and mouse_pos[0] <= box[1][0] and mouse_pos[1] >= box[0][1] and mouse_pos[1] <= box[1][1]:
        return True
    else:
        return False
