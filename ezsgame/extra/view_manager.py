from ..objects import *

screen = get_screen()

class ViewManager:
    
    # Inicializacion de objetos -------------------------------------------------------------------------
    current_view: str = None  

    no_view_text = Text("There's no views setted", pos=["center","center"], font_size=40, color="black")
    
    # DRAWING GROUPS -----------------------------------------------------------------------------------
    views = {}
    
    
    # dibuja los objetos
    def draw() -> None:    
        
        # dibuja la vista principal
        if ViewManager.current_view == None:
            screen.color = "white"
            ViewManager.no_view_text.draw()
            
        else:
            # dibuja la vista actual
            ViewManager.views[ViewManager.current_view].draw()


    # inicializa la ViewManager y las vistas
    def init() -> None:
        ViewManager.change_view(ViewManager.current_view)
        
        for view_obj in ViewManager.views.values():
            view_obj.init()
    

    def change_view(new_view:str):
        ViewManager.current_view = new_view
        ViewManager.draw()
    
    def load_view_folder(folder_path:str):
        """
        Loads all views from a folder
        
        - file name will be used as view name
        """
        for file in os.listdir(folder_path):
            if file.endswith(".py"):
                ViewManager.views[file.split(".")[0]] = __import__(folder_path + "." + file.split(".")[0])
                
    def load_view_from_module(view_name:str, module):
        """
        Loads a view from a module
        """
        ViewManager.views[module.name] = module
        
    def load_view_from_group(view_name:str, group:Group):
        """
        Loads a view from a group
        """
        ViewManager.views[view_name] = group
        
