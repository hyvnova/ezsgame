from main import *

s = Screen(size=[720, 420], title="Test", icon="", fps=60, show_fps=True)

c = Circle(pos=["center", "center"], radius=20, screen=s)

speeds = [0,0,0,0]

def move(obj, index, speed):
    speeds[index] = speed

s.events.onKey(type="down", keys=["w"], callback=lambda: move(c, 0, 5))
s.events.onKey(type="down", keys=["s"], callback=lambda: move(c, 1, -5))
s.events.onKey(type="down", keys=["a"], callback=lambda: move(c, 2, -5))
s.events.onKey(type="down", keys=["d"], callback=lambda: move(c, 3, 5))

s.events.onKey("up", keys=["w"], callback=lambda: move(c, 0, 0))
s.events.onKey("up", keys=["s"], callback=lambda: move(c, 1, 0))
s.events.onKey("up", keys=["a"], callback=lambda: move(c, 2, 0))    
s.events.onKey("up", keys=["d"], callback=lambda: move(c, 3, 0))

while True:
    s.events.check(s.events.get(), s)
    s.fill((0, 0, 0))
    c.move(x=speeds[2] + speeds[3], y=speeds[0] + speeds[1], screen=s)
    c.draw(s)
    s.update()
    