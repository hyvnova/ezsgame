from ezsgame.all import *

screen = Screen(title="Sample Demo", fps=144, show_fps=True)

#::reload
scroll = Scroll()
#::endreload

reloader = Reload("demo.py", globals(), locals())

@screen.on_key("down", ["r"])
def reload():reloader()

player = Rect(["center", "center"], [50,50], color="white")


while True:   
	screen.check_events()
	screen.fill() 
	
	player.draw()
	scroll.draw()
	

	screen.update()