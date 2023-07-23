from ezsgame import *

window = Window(Size(800, 600), title="Just a square")

square = Rect(
    Pos("center"),
    Size(100, 100),
)

timer = Text("0", Pos("center", "center"), font_size=26, color="white")

controller = Controller()


# update timer
@add_interval(1000, repeat=3)
def update_timer():
    timer.text.set(str(int(timer.text.get()) + 1))


# quit after 10 seconds (used for profiling)
@add_interval(10 * 1000)
def quit_window():
    window.quit()


while True:
    window.check_events()
    window.fill()

    square.pos += controller.get_speed("simple")

    # square.draw()
    timer.draw()

    window.update()
