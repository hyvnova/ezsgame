from main import *

screen = Screen(title="PyStyle", fps=60, show_fps=True,
                size=[200, 200])

def fun(n):
    print("Leaving", n)

screen.events.onQuit(fun, 3)

while True:
    screen.events.check(screen.events.getEvent(), screen)

    screen.fill(color['black'])
    screen.update()