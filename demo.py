from ezsgame.all import *

screen = Screen(show_fps=True, color="white")

grid = Grid(["center", "center"], [400,400], [5,5], 
            box_styles = {
                "border_radius": [10,10,10,10],
                "color" : "black",
                "stroke" : 5
            })

while True:
    screen.check_events()
    screen.fill()

    grid.draw()
    grid.highlight_current({"color": "red"})

    screen.update()