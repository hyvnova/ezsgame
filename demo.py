from ezsgame import *


window = Window()

from components import * # loaded after window to avoid window not being initialized


box = Rect(
    Pos("center"),
    Size(50),
    components=[
        Controllable(), 
        HealthBar(Health(), True, True)
    ],
    color="red",
)

def on_hit(other: Object):
    # knockback effect
    box.pos += (box.pos - other.pos).normalize() * sum(other.size) * 0.5

# listen to the hit signal
health_comp: Health = box.components[Health]
health_comp.on_hit.add("box_hit", on_hit)

box2 = Rect(Pos(100, 100), Size(50), color="blue")


@window.run
def draw():
    window.fill("black")
