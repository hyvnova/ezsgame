from ezsgame.all import *
from ezsgame.styles import Styles

screen = Screen(title="Sample Demo")

plane = Interface(screen)
plane.add([
    Rect([0,0], [200,100], color="red"),
    Rect([0,0], [100,100], color="green"),
    Rect([0,0], [300,50], color="blue"),
]).flex("row", "center", "center")

while True:    
    screen.check_events()
    screen.fill() 

    plane.draw()
    
    screen.update()