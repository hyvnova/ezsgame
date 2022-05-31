from ezsgame.all import *

screen = Screen(title="Sample Demo", fps=120, show_fps=True)

player = Rect(["left", "center"], [50,50], color="red", components=[
    Controllable(speed=[-10,10])
    ])

@screen.on_key("down", ["escape"])
def quit_app():
    screen.quit()

while True:    
    screen.check_events()
    screen.fill() 

    player.draw()
    
    screen.update()