from ezsgame.all import *

screen = Screen(show_fps=True)

# #::reload
# rect = Rect(["center", "center"], [100, 100])
# #::endreload

# reloader = Reload("demo.py", globals(), locals())

mi_text = Text("Mi texto", ["center", "center"], 40, color="white",
               
               font=Fonts.OpenSans)

while True:
    screen.check_events()
    screen.fill()

    # rect.draw()
    mi_text.draw()

    screen.update()