from ezsgame.main import *

s = IScreen(size=[480, 400], title="Test", fps=120, show_fps=True)

player = Rect(pos=["left", "top"], size=[40, 40], color="red")

s.add(player)
    
s.events.on("mousedown", callback=lambda: Slide(s, object=player, end=["right", "bottom"], time=10, step=2)) 

while True:
    s.check()
    s.fill("black")
    s.draw()