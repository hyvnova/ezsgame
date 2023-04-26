from ezsgame import *
from vistas import right, left

window: Window = get_window()
EventHandler = DATA.EventHandler

    
def get_arrow(direction:str, view_direction:str) -> Image:
    """
    #### Retornate el objeto de la flecha apuntado hacia x direction para moverte entre vistas
    
    #### Params
    - direction : left, right, up or down
    - to_return : invierte la flecha si es True
    """
    
    # calculate pos
    arrow: Image = Image(pos=[0,0], size=[35,35], image="assets/img/arrow.png")
    
    if direction == "left":
        arrow.pos[0] = 20
        arrow.rotate(90)
    
    elif direction == "right":
        arrow.pos[0] = window.size[0] - arrow.get_size()[0] - 20
        arrow.rotate(-90)
        
    center(arrow, window, x=False)
        
    arrow.extends(IObject)
        
    arrow.__setattr__("direction", view_direction)
    
    return arrow 
      
class Interfaz:
    """
    Clase que maneja la inferfaz
    En esta clase solo deben hacer cosas que sean necesarias para la interfaz principal
    """
    
    # Inicializacion de objetos -------------------------------------------------------------------------
    current_view: str = "left"    

    back_right_arrow, back_left_arrow = get_arrow("right", "left"), get_arrow("left", "right")    
    
    main_text = Text("Click arrows to change view", pos=["center","center"], font_size=40, color="black")
    
    # DRAWING GROUPS -----------------------------------------------------------------------------------
    views = {
        "left" : left,
        "right" : right
    }
    
    
    # dibuja los objetos
    def draw() -> None:    
        
        # dibuja la vista actual
        Interfaz.views[Interfaz.current_view].draw()        

        # dibuja las flechas
        if Interfaz.current_view == "left":
            Interfaz.back_right_arrow.draw()
            
        elif Interfaz.current_view == "right":
            Interfaz.back_left_arrow.draw()
    
    # inicializa la interfaz y las vistas
    def init() -> None:
        Interfaz.change_view(Interfaz.current_view)
        
        for view_obj in Interfaz.views.values():
            view_obj.init()
    

    def change_view(new_view:str):
        # remove events from arrows
        if new_view in ("left", "right"):
            EventHandler.remove_event("to_left_arrow_event")
            EventHandler.remove_event("to_right_arrow_event")

        # add events to arrows
        if new_view == "left":
            Interfaz.back_right_arrow.click(lambda: Interfaz.change_view("right"), "back_right_arrow_event")

        elif new_view == "right":
            Interfaz.back_left_arrow.click(lambda: Interfaz.change_view("left"), "back_left_arrow_event")
        
        Interfaz.current_view = new_view
        Interfaz.draw()