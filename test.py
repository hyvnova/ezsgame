from ezsgame.main import *

s = Screen(size=(400, 300), title="Test", fps=60, show_fps=True)

boxes = [
    Rect(size=[20,20], pos=[0,"center"], color="white") for i in range(3)
]

def auto_x(screen, objs):
    # auto change pos of objs to aling in x axis resposive to screen
    div = 
    for obj in objs:
        obj.pos 

auto_x(s, boxes)

while True:
    s.check()
    s.fill("black")
    for box in boxes:
        box.draw(s)
    s.update()