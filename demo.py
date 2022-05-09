from ezsgame.all import *

screen = Screen(title="Sample Demo")

obj = Rect(pos=[0,0], size=[50,50], screen=screen, components=[Draggable])

gradient = Gradient(screen, "blue", "pink", complexity=70)

while True:
    screen.check_events()
    screen.fill(gradient)
    
    
    obj.draw()
    

    screen.update()