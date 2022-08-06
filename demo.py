from ezsgame.all import *

screen = Screen(show_fps=True)

input_box = InputBox(["center", "center"], [250, 50])

@input_box.onchange("mycallback")
def onchange(value):
    print(value)

while True:
    screen.check_events()
    screen.fill()

    input_box.draw()

    screen.update()