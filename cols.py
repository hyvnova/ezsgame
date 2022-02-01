from ezsgame.main import *

s = Screen(fps=60)

r1, r2 = Rect(pos=["left-center", "center"], size=["9u","9u"], color='red'), Circle(pos=[100,100], radius=30, color='blue') 
speed = [0,0,0,0,   0,0,0,0]
def ms(i, val):
    speed[i] = val

cs = 3

s.events.on_key(type="down", keys=["w"], callback=lambda: ms(0,cs))
s.events.on_key(type="up", keys=["w"], callback=lambda: ms(0,0))
s.events.on_key(type="down", keys=["s"], callback=lambda: ms(1,-cs))
s.events.on_key(type="up", keys=["s"], callback=lambda: ms(1,0))
s.events.on_key(type="down", keys=["a"], callback=lambda: ms(2,-cs))
s.events.on_key(type="up", keys=["a"], callback=lambda: ms(2,0))
s.events.on_key(type="down", keys=["d"], callback=lambda: ms(3,cs))
s.events.on_key(type="up", keys=["d"], callback=lambda: ms(3,0))

s.events.on_key(type="down", keys=["up"], callback=lambda: ms(4,cs))
s.events.on_key(type="up", keys=["up"], callback=lambda: ms(4,0))
s.events.on_key(type="down", keys=["down"], callback=lambda: ms(5,-cs))
s.events.on_key(type="up", keys=["down"], callback=lambda: ms(5,0))
s.events.on_key(type="down", keys=["left"], callback=lambda: ms(6,-cs))
s.events.on_key(type="up", keys=["left"], callback=lambda: ms(6,0))
s.events.on_key(type="down", keys=["right"], callback=lambda: ms(7,cs))
s.events.on_key(type="up", keys=["right"], callback=lambda: ms(7,0))

point = Rect(pos=[100,100], size=[60,60], color="yellow")

while True:
    s.check()
    s.fill((0,0,0))

    r1.move(speed[2] + speed[3], speed[0] + speed[1], s)
    r2.move(speed[6] + speed[7], speed[4] +  speed[5], s)

    if r1.is_colliding(r2, s):
        r1.color = "white"
        r2.color = "white"
    else:
        r1.color = "blue"
        r2.color = "red"

    if r2.pos == [100,100]:
        r2.color = "yellow"

    r1.draw(s)
    r2.draw(s)
    point.draw(s)


    s.update()