from ezsgame.all import *

screen = Screen(title="Sample Demo")

player = Rect(["center", "center"], [50,50], color="red", border_radius=[5,5,5,5], components=[
    Controllable
])

while True:    
    screen.check_events()
    screen.fill() 

    player.draw()
    
    screen.update()