from ezsgame.main import *

s = Screen(size=(400, 300), title="Test", fps=60, show_fps=True)

grid = Grid(pos=[0,0], size=[s.size[0], s.size[1]], grid_size=[15,15], screen=s)

paint = False

def highlight():
    global paint
    item = grid.get_current()
    if item:
        if paint:
            item.color = random_color()
        else:
            item.color = "white"
            
    
s.time.add(time=50, callback=lambda: highlight())

@s.on("click")
def toggle():
    global paint
    paint = not paint

while True:
    s.check_events()
    s.fill("black")
    
    grid.draw(s)

    s.update()