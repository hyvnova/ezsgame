from ezsgame import *
from .right import to_place

window: Window = get_window()

"""
Declaracion del "widget" vista izquierda
todo en esta clase solo se dibujara en el View izquiero al ser selecionado
"""

# Clases y funciones 
UI_elements = Group(
    flash_background = Rect(["center", "top"], [0,0], color="black", border_radius=[10,4]),
    flash_text = Text("", ["center","top"], 20, color="white", font=Fonts.RobotoMono.light)
)

def flash_message(message, time):
    global UI_elements

    text = UI_elements.flash_text
    text.visible = True
    text.update(text=message)

    background = UI_elements.flash_background
    background.visible = True
    background.size = text.size + 20
    
    center(background, window, y=False)
    center(text, background, y=True)
    
    @add_interval(time, "flash_message")
    def remove_message():
        global UI_elements
        UI_elements.flash_text.visible = False
        UI_elements.flash_background.visible = False

        remove_interval("flash_message")
        
# Inicializacion de objetos -------------------------------------------------------------------------
selected = None
selected_text= Text("Selected: None", ["center","bottom"], 24, color="black", font=Fonts.RobotoMono.light)

items = Group(
    rock = Sprite([50, 50], [100,100], "assets/img/rock.png"),
    knife = Sprite([200, 150], [100,150], "assets/img/knife.png"),
    basketball = Sprite([500, 300], [100,100], "assets/img/basketball.png")
)

    
def add_click_event(name):  
    item = items[name]
    
    @add_event("click", item)
    def select_item():
        global selected
        selected = (name, item)

for name in items.keys():
    add_click_event(name)

# option menu   
draw_option_menu = False

option_menu = Group(
    parent = "background",
    background = Rect([0,0], [130,50], color="#888", border_radius=[5])
)
option_menu.add(
    delete_option = Text("To inventory", [0, 0], 20, color="white", font=Fonts.OpenSans.light),
)


option = option_menu.delete_option
# hover
@add_event("hover", option)
def hover_option():
    option.update(font = Fonts.OpenSans.medium)
    
# unhover
@add_event("unhover", option)
def unhover_option():
    option.update(font = Fonts.OpenSans.light)
    
@add_event("click", option)
def move_to_inventory():
    global draw_option_menu, items, selected
    
    draw_option_menu = False
    
    if selected:
        to_place.add(selected[1])
        items.remove(selected[0])
        selected = None

# activate option menu on right click
@on_event("right_click")
def open_option_menu():
    global draw_option_menu, selected
    
    if not selected:
        return

    draw_option_menu = not draw_option_menu

    if not draw_option_menu:
        return 

    mouse_pos = get_mouse_pos()
    background = option_menu.background

    # align option menu to mouse position
    if mouse_pos[0] + background.size[0] > window.size[0]:
        background.pos[0] = mouse_pos[0] - background.size[0]
    else:
        background.pos[0] = mouse_pos[0]
        
        
    if mouse_pos[1] + background.size[1] > window.size[1]:
        background.pos[1] = mouse_pos[1] - background.size[1]
    else:
        background.pos[1] = mouse_pos[1]    
    

# Logica de dibujado -----------------------------------------------------------------------------------
flash_message("select an object and right-click", 3000)

def draw():
    
    items.draw()
    UI_elements.draw()

    if selected:
        outline(selected[1], color="red", border_radius=[5], size=1.15)
        
        selected_text.text = "Selected: " + selected[0]
        center(selected_text, window, y=False)
        selected_text.draw()
        
    if draw_option_menu:
        option_menu.draw()
    
# Inicializacion de la clase  (si no es necesario, dejar la funcion vacia)
def init():
    pass