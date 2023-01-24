from ezsgame import *
from ezsgame.futures.controller import Controller

# Initialize window
window = Window(title="Controllable Player Game", show_fps=True)

# Initialize player
player_speed = 25
player_controller = Controller(keys=["a", "d", "w", "s"], speed=[-player_speed,player_speed,-player_speed,player_speed])
player = Rect(pos=("center", "center"), size=(50, 50), color="blue")

# Main loop
while True:
    window.check_events()

    # Move player based on user input
    player.pos += player_controller.get_speed("simple")

    # Keep player within window bounds
    player.pos.x = clamp(player.pos.x, player.size.width/2, window.size.width - player.size.width/2)
    player.pos.y = clamp(player.pos.y, player.size.height/2, window.size.height - player.size.height/2)

    # Clear screen
    window.fill("black")

    # Draw player
    player.draw()

    # Update window
    window.update()
