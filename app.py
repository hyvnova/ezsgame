from ezsgame.all import *

from game_data import GAME_DATA

screen = Screen(fullscreen=False, show_fps=True)

game_scene = Scene("game.py")

CURRENT_SCENE = "menu"

def switch_to(scene):
    global CURRENT_SCENE
    CURRENT_SCENE = scene

#::reload

menu = Menu({   
    "spacing" : 30,
    "size" : (size := ["53%", "100%"]),
    "background" : Gradient((227, 66, 245), (241, 183, 247), size=size),
    
    "title": {
        "text": "Main Menu",
        "font": "Arial",
        "fontsize": 40,
        "color": "white"
    },
    
    "::items" : {
        "color" : "white",
        "stroke" : 1,
        "fontsize" : 24,
        "font" : "Arial",
        "border_radius" :[10,10,10,10],
        "on:hover" : {"color" : "blue", "textcolor" : "blue"}
    }, 
    
    "items": [
        {"text": "Play", "on:click": {"callback": lambda: switch_to("game")}},
        {"text": "Options", "on:click": {"callback": lambda: switch_to("options")}},
        {"text": "Quit", "on:click": {"callback": screen.quit}}
    ]
})

options_menu = Menu({
    "spacing" : 20,
    "size" : screen.size.copy(),
    "background" : "gray",
    
    "title": {
        "text": "Options",
        "font": "Arial",
        "fontsize": 52,
        "color": "white"
    },
    
    "::items" : {
        "color" : "white",
        "stroke" : 1,
        "fontsize" : 24,
        "font" : "Arial",
        "border_radius" :[10,10,10,10],
        "on:hover" : {"color" : "blue", "textcolor" : "blue"}
    },
    
    "items": [{   
        "text": "Difficulty",
        "stroke": 0,
        "color" : "black",
        "textcolor" : "white",
        "on:hover" : {
            "textcolor" : "blue"
        },
        
        "::items" : {
            "color" : "white",
            "stroke" : 1,
            "fontsize" : 15,
            "font" : "Arial",
            "border_radius" :[5],
        },
         
        "items": [
            {"text": "Facil", "on:click": {"callback": lambda: GAME_DATA(difficulty="easy") },
                "on:hover" : {"color" : "green", "textcolor" : "green"}},
            
            {"text": "Medio", "on:click": {"callback": lambda: GAME_DATA(difficulty="medium") },
                "on:hover" : {"color" : "yellow", "textcolor" : "yellow"}},
            
            {"text": "Dificil", "on:click": {"callback": lambda: GAME_DATA(difficulty="hard") },
                "on:hover" : {"color" : "red", "textcolor" : "red"}},
        ],  
            
        "on:click": {"callback": lambda: None}
        },
              
        {"text": "Back", "on:click": {"callback": lambda: switch_to("menu")}}    ]
})

@screen.on_key(type="down", keys=["escape"])
def open_menu():
    switch_to("menu")

#::endreload
# reloader = Reload("app.py", globals(), locals())

while True:
    # reloader()
    screen.check_events()
    screen.fill()
    
    # IN MENU
    if CURRENT_SCENE == "menu":
        menu.draw()
    
    # IN GAME
    elif CURRENT_SCENE == "game":
        game_scene.play()

    # IN OPTIONS
    elif CURRENT_SCENE == "options":
        options_menu.draw()  

    screen.update()
    
