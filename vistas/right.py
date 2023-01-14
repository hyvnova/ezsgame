from ezsgame import *

window: Window = get_window()

"""
Declaracion del "widget" vista izquierda
todo en esta clase solo se dibujara en el View izquiero al ser selecionado
"""
    
# Inicializacion de objetos -------------------------------------------------------------------------

inventory_open: bool = False



to_place = Group()
index = 0

# Textos
open_inventory_text = Text("Press \"e\" to open Inventory" , pos=["center","center"], color="black", font_size=30)

#Inventario
inventory: Group = Group( title = Text("Inventory", pos=["center", 20], color="black", font_size=30),
            
            slots = Grid(pos=[35, 160], size=["90%", "60%"], shape=[6, 3],
                box_styles={
                    "color": "black",
                    "stroke" : 1,
                    "border_radius": [10,10,10,10]
                }
            )
)

# Logica de dibujado
def draw():
    global inventory_open, index
    
    # si el inventario esta abierto, se dibuja
    if inventory_open:
        for item in to_place:
            inventory.slots.place(index, item)
        
            index += 1
        
        index = 0
        
        inventory.draw()
        
    # si no, se dibuja el texto que indica como abrir el inventario
    else:
        open_inventory_text.draw()
        
            
# Inicializacion de la clase  (si no es necesario, dejar la funcion vacia)
def init():
    # Abrir y cerrar el inventario
    # Al presionar la "e" se abre el inventario y se cierra cuando se presiona otra vez
    @on_key("down", ["e"])
    def open_inventory():
        global inventory_open
        
        if inventory_open:
            inventory_open = False
        else:
            inventory_open = True