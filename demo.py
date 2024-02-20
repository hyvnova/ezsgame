from ezsgame import *
from components import *
from pygame import draw




window = Window()


rect = Rect(
    Pos(x="left", y="center"),
    Size(width=50, height=50),
    color="red"
) 

@on_key("down", "right")
def on_right_down():
    rect.x += 10

while True:
    window.check_events()

    window.fill("black")
    rect.draw()

    # Display the window
    window.update()