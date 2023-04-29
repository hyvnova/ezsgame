from ezsgame import *

window = Window(Size(800, 600), title="Just a square", profiling=ProfilingOptions())

square = Rect(
    Pos("center"),
    Size(100, 100),
)

controller = Controller()


# quit after 10 seconds (used for profiling)
@add_interval(Milliseconds.from_unit(TimeUnit.seconds, 10), "quit")
def quit():
    window.quit()


while True:
    window.check_events()
    window.fill()

    square.pos += controller.get_speed("simple")

    square.draw()

    window.update()
