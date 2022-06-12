from ezsgame.all import *

screen = Screen(title="Sample Demo", fps=144, show_fps=True)

@screen.on_key("down", ["escape"])
def quit_app():
	screen.quit()

player = Rect(["center", "center"], [50,50], color="white",
		components = [
			Controllable
		],
		behavior = {
		"pos":"dynamic"
		}
)

# player will turn blue while it's clicked
@screen.custom_event(object=player)
def on_click_player(**ev):
	if ev["type"] == pg.MOUSEBUTTONDOWN and ev["button"] == 1 and ev["is_hovering"]:
		player.color = "blue"
	else:
		player.color = "white"

		
while True:   
	screen.check_events()
	screen.fill() 
	
	player.draw()
 
	screen.update()