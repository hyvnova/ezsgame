from ezsgame import *

window: Window = Window()

while True:
    window.check_events()
    window.fill()

    window.update()