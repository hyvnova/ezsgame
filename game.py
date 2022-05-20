from ezsgame.all import *
from game_data import GAME_DATA

player_data = GAME_DATA.player
player = Rect(player_data["pos"], player_data["size"], color=player_data["color"])

player_controller = Controller() 
player_controller.disable()


#::main          
   
player_controller.enable()
        
move(player, player_controller.get_speed("simple"))
GAME_DATA.player["pos"] = player.pos

    
player.draw()
