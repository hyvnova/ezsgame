from ezsgame.all import *
from ezsgame.styles import Styles

screen = Screen(title="Sample Demo")

styles = Styles("styles.json")
rect = Rect(pos=[0,0], size=[50,50], styles=styles.rect)

while True:    
    screen.check_events()
    screen.fill() 

    rect.draw()
    
    screen.update()