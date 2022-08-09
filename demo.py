from ezsgame.all import *

screen = Screen(show_fps=True)

rect = Rect(["center", "center"], [100, 100], color = "red")

while True:
    screen.check_events()
    screen.fill()

    rect.draw()

    screen.update()