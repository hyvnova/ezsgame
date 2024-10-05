from typing import List

from ezsgame.types import Pos
from .world import get_window
import pygame as pg

def outline(obj, color="red", stroke:int=1, size:int=1.5, border_radius:list = [0,0,0,0]):
    r'''
    #### Draws an outline of the object
    - `color` : the color of the outline `White`or `(R,G,B)`
    - `stroke` : the width of the outline `int`
    - `size` : the size  multiplier of the outline (object size * outline size) `int`
    - `border_radius` : the radius of the corners of the outline `[top_left, top_right, bottom_left, bottom_right]`

    #### Note: Automaticly draws the outline when declared
    '''
    
    obj_size = obj.size
    obj_pos = obj.pos

    size = (obj_size[0] * size, obj_size[1] * size)
    pos = (obj_pos[0] - (size[0] - obj_size[0]) / 2, obj_pos[1] - (size[1] - obj_size[1]) / 2)

    pg.draw.rect(get_window().surface, color, [*pos, *size], stroke, *border_radius)
    
def is_out(obj):
    r'''
    Return True if objects is out of bounds and direction of that bound (top, bottom, right, left)
    -> [bool, "direction"]
    '''
    screen = get_window()
    
    if obj.pos[0] + obj.size[0] < 0 or obj.pos[0] - obj.size[0]/4 > screen.size[0]:
        return True, "left" if obj.pos[0] + obj.size[0]/2 <= 0 else "right"
    elif obj.pos[1] + obj.size[1] < 0 or obj.pos[1] - obj.size[1]/4 > screen.size[1]:
        return True, "top" if obj.pos[1] + obj.size[1] <= 0 else "bottom"     
    else:
        return False, None
        
def is_colliding(obj1, obj2, draw_collision_box=False, scale=1):
    r'''
    #### returns True if obj1 is colliding with obj2, False otherwise
    - obj1 : object -> first object with attributes 'pos' (position) and 'size' (width, height)
    - obj2 : object -> second object with attributes 'pos' (position) and 'size' (width, height)
    - draw_collision_box : bool -> if True, draw collision boxes for both objects
    - scale : float -> scale factor to adjust the size of obj2 for collision detection
    '''
    
    obj2_size = obj2.size.copy()  # Store the original size of obj2
    obj2.size *= scale  # Apply scaling to obj2's size

    # Draw collision boxes if requested
    if draw_collision_box:
        outline(obj1, size=1.1, stroke=2)
        outline(obj2, size=1.1, stroke=2)

    # Get positions and sizes for both objects
    x1, y1 = obj1.pos
    w1, h1 = obj1.size
    x2, y2 = obj2.pos
    w2, h2 = obj2.size

    # Check for collision by comparing the bounding boxes of obj1 and obj2
    if (x1 < x2 + w2 and x1 + w1 > x2 and  # Check horizontal overlap
        y1 < y2 + h2 and y1 + h1 > y2):    # Check vertical overlap
        obj2.size = obj2_size  # Restore original size before returning
        return True

    obj2.size = obj2_size  # Restore original size if no collision
    return False

        
        
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
def center_of(obj) -> Pos:
    r'''
    #### Returns the center postion of the object
    - obj : object
    '''
    return Pos(obj.pos[0] + obj.size[0]/2, obj.pos[1] + obj.size[1]/2)


def center_at(obj, parent, x: bool = True, y: bool = True):
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

