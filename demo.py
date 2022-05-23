from ezsgame.basics import *
from ezsgame.extra.components import Controllable, Draggable

screen = Screen(title="Sample Demo")

player = Rect(pos=[0,0], size=[50,50], 
            components=[
                Controllable
            ]) 

box = Rect(pos=["center", "center"], size=[50,50],
            components=[
                Draggable
            ])

while True:    
    screen.check_events()
    screen.fill() 
    
    if is_colliding(player, box, draw_collision_box=True):
        player.color = "red"
        box.color = "green"
        
    else:
        player.color = "white"
        box.color = "white"
        
    player.draw() # draws the player
    box.draw() # draws the box
    
    screen.update()