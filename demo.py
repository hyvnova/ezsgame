from ezsgame.basics import *

screen = Screen(title="Sample Demo", fps=144, show_fps=True)

@screen.on_key("down", ["escape"])
def quit_app():
	screen.quit()


player = Rect(["center", "center"], [50,50], color="white")

while True:    
    
	screen.check_events()
	screen.fill() 
    
	player.draw()
    
 
	screen.update()