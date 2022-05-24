from ezsgame.all import *

screen = Screen(title="Sample Demo")

rect = Rect(pos=["center", "center"], size=[50,50]).extends(IObject)

    
while True:    
    screen.check_events()
    screen.fill() 

    rect.draw()

    
    screen.update()