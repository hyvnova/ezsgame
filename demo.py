from ezsgame.all import *

screen = Screen(title="Sample Demo", fps=120, show_fps=True)


#::reload
player = Rect(["left", "center"], [50,50], color="red", components=[
    Controllable
    ])

#::endreload

@screen.on_key("down", ["escape"])
def quit_app():
    screen.quit()
    
reloader = Reload("demo.py", globals(), locals())
    
@screen.on_key("down", ["r"])
def reload_script():
    reloader()
             
while True:    
    screen.check_events()
    screen.fill() 

    player.draw()
    
    screen.update()