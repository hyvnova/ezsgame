from ezsgame.all import *

screen = Screen(title="Sample Demo", fps=120, show_fps=True)

player = Rect(["center", "center"], [50,50], color="white", 
	components=[
		Controllable, Draggable
	])

@screen.on_key("down", ["escape"])
def quit_app():
	screen.quit()
	

while True:    
    
	screen.check_events()
	screen.fill() 
    
	player.draw()
    
 
	screen.update()