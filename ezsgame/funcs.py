from ezsgame.global_data import get_id, get_screen
from ezsgame.styles_resolver import resolve_color
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
    
    obj_size = obj.get_size()
    obj_pos = obj.get_pos()

    size = [obj_size[0] * size, obj_size[1] * size]
    pos = [obj_pos[0] - (size[0] - obj_size[0]) / 2, obj_pos[1] - (size[1] - obj_size[1]) / 2]

    color = resolve_color(color)

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

