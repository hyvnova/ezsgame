from ezsgame.all import *

screen = Screen(show_fps=True)

rect = Rect(["center", "center"], [100,100])

click_count_text = Text("0", ["center", "top-center"], fontsize=24, color="white")
count = 0

@screen.add_event("click", rect)
def on_click():
    global count
    rect.color = "red"
    count += 1
    
@screen.add_event("unclick", rect)
def on_unclick():
    rect.color = "white"

while True:
    screen.check_events()
    screen.fill()

    rect.draw()
    click_count_text.text = str(count)
    click_count_text.draw()

    screen.update()