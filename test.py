from ezsgame.main import *

s = Screen(size=[480, 400], title="Test", fps=60)

rect = Rect(pos=[100, 100], size=[100, 100], color="red")

while True:
    s.check()
    s.fill((0,0,0))
    
    rect.draw(s)
    
    s.update()