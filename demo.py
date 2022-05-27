from ezsgame.all import *
import random

screen = Screen(title="Sample Demo")

def gen_objects(n, size=[50,50]):
    return [Rect([0,0], 
                [ random.randint(size[0]/2, size[0]*1.5), 
                random.randint(size[1]/2, size[1]*1.5)],
                color=random_color()) for i in range(n)] 

plane = Interface(screen)
plane.add(gen_objects(9, [100,100])).align("row")

while True:    
    screen.check_events()
    screen.fill() 

    plane.draw()
    
    screen.update()