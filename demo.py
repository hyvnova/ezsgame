from ezsgame.all import *

screen = Screen(title="Sample Demo")

player = Rect(pos=["center", "center"], size=[50,50], components=[Draggable]) # Create a object
player_controller = Controller()

while True:
    screen.check_events()
    screen.fill() 
    
    speed = player_controller.get_speed("simple") # gets the speed of the player
    move(player, speed) # moves the player
    player.draw() # draws the player

    screen.update()