# inicializacion de la pantalla (Max. Priority)
from ezsgame import *
screen: Screen = Screen(title="Inventory System", show_fps=True, color="white")


# IMPORTS -----------------------------------------------------------------------------------------------
from UI import Interfaz


# Incializacion de variables -------------------------------------------------------------------------
Interfaz.init()


# Mainloop4
while True:
    
    screen.check_events()
    screen.fill()
    
    Interfaz.draw()
    
    screen.update()