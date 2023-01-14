# inicializacion de la pantalla (Max. Priority)
from ezsgame import *
window: Window = Window(title="Inventory System", show_fps=True, color="white")


# IMPORTS -----------------------------------------------------------------------------------------------
from UI import Interfaz


# Incializacion de variables -------------------------------------------------------------------------
Interfaz.init()


# Mainloop
while True:
    
    window.check_events()
    window.fill()
    
    Interfaz.draw()
    
    window.update()