from ezsgame import *
from components import *

window = Window()


box = Rect(
    Pos("center"),
    Size(50),
    components=[Controllable(), HealthBar(Health(), True, True)],
    color="red",
)


def on_hit(other: Object):
    # knockback effect
    box.pos += (box.pos - other.pos).normalize() * sum(other.size) * 0.5


# listen to the hit signal
health_comp: Health = box.components[Health]
health_comp.on_hit.add("box_hit", on_hit)

box2 = Rect(Pos(100, 100), Size(50), color="blue") # just a dummy object


@window.run
def draw():
    window.fill("black")
