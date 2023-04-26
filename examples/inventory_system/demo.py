from ezsgame import *
window: Window = Window(title="Inventory System", show_fps=True, color="white")


from LibTests.UI import Interfaz

Interfaz.init()


# Mainloop
while True:
    
    window.check_events()
    window.fill()
    
    Interfaz.draw()
    
    window.update()