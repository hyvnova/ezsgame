from ezsgame.global_data import get_id, get_screen
from ezsgame.primitive_objects import PRect

def copy(obj, different=False):
    new_obj = copy.copy(obj)
    if different:
        new_obj._id = get_id()
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
    
    screen = get_screen()
    obj_pos = obj2.get_pos()

    for i in obj1._get_collision_box():
        if draw_collision_box:
            PRect(pos=[obj_pos[0]-2, obj_pos[1]-2], size=[obj2.size[0]+4, obj2.size[1]+4], color="red", stroke=2).draw(screen)
            PRect(pos=[obj1.pos[0]-2, obj1.pos[1]-2], size=[obj1.size[0]+4, obj1.size[1]+4], color="red", stroke=2).draw(screen)
            
        if (i[0] >= obj2.pos[0] and i[0] <= obj2.pos[0]+obj2.size[0]) and (i[1] >= obj2.pos[1] and i[1] <= obj2.pos[1] + obj2.size[1]):
            return True
        
    return False
