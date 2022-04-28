from ezsgame.all import *

screen = Screen(show_fps=True)

rect = Rect(pos=["center", "center"], size=[50,50], components=[Drageable], screen=screen)
   
while True:
    screen.check_events()
    screen.fill("black")
   
    rect.draw(screen)
    
    screen.update()
 