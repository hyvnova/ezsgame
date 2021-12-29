from main import *
import random

s = IScreen(title="Test", fps=60, show_fps=True, size=[480, 400])
s.grid = s.gridDiv(cols=3, rows=3)

s.add([Rect(pos=[0, 0], size=[100, 100], color=randomColor(["black"])) for i in range(s.grid_space)])

while True:
    s.check(s)
    s.fill(color['black'])
    s.draw(auto_place=True)
    s.update()

                