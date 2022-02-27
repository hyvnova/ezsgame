# Sounds Test

from ezsgame.main import *

s = Screen()

sound = Sound("sounds/my-ordinary-life.mp3").play()

colors = s.fill_gradient((0,0,0), (255,255,255))

@s.add_interval(150)
def change_color():
    global colors
    colors = s.fill_gradient(colors[-2], random_color())

while True:
    s.check_events()    
    s.fill_gradient(colors[0], colors[-1])
        
    s.update()