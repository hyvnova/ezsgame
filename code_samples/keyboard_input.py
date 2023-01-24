from ezsgame import *
from ezsgame.futures.controller import Controller


window = Window(title="Bouncing Ball - (Code Sample)")


player_speed = 25
player_controller = Controller(keys=["a", "d", "w", "s"], speed=[-player_speed,player_speed,-player_speed,player_speed])

player = Rect(
    pos=("center", "bottom"),
    size=(30, 30)
)

while True:
    
    window.check_events()
    
    window.fill("black")
    
    # add speed to player postion
    player.pos += player_controller.get_speed("simple") # the simple method return speeds as [x, y] which is what we need
    
    player.draw()
    
    window.update()
    