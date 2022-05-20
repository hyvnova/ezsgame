from ezsgame.all import *

screen = Screen(title="Sample Demo")

player = Rect(pos=["center", "center"], size=[50,50])
player_controller = Controller()

gradient = Gradient("black", "white", complexity=70)

while True:
    screen.check_events()
    screen.fill(gradient) 
    
    speed = player_controller.get_speed("simple") # gets the speed of the player
    move(player, speed) # moves the player
    player.draw() # draws the player
    
    screen.update()