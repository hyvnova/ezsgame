from main import *

s = IScreen(title="Test", fps=60, show_fps=True, size=[480, 400])
s.grid = s.gridDiv(cols=3, rows=3)

s.add([Rect(pos=[0, 0], size=[10, 10], color=randomColor(["black"])) for i in range(s.grid_space)])

while True:
    s.check(s)
    s.fill(color['black'])
    s.draw(auto_place=True)
    s.update()

                