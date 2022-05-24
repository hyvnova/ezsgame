from ezsgame.all import *

screen = Screen(title="Sample Demo")

irect = IObject.extend(
    Rect(pos=["center", "center"], size=[50,50])
)
    

while True:    
    screen.check_events()
    screen.fill() 

    irect.draw()

    
    screen.update()