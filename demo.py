from ezsgame.all import *

screen = Screen(title="Sample Demo")

def gen_objects(n, size=[50,50]):
    return [Rect([0,0], size, color=random_color()) for _ in range(n)]

plane = Interface(screen)
plane.add(gen_objects(2, [100,50])).align("row")

while True:    
    screen.check_events()
    screen.fill() 

    plane.draw()
    
    screen.update()