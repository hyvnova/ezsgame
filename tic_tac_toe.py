from ezsgame.main import *
import random
from itertools import combinations

screen  = Screen(size=[360, 360], title="Tic Tac Toe")

player1, player2 = "blue", "red"
player1_moves,player2_moves, plays = [],[],[]
winner = None

current_player = random.choice([player1, player2])

board = flat([[IRect(pos=[x,y], size=[100,100], screen=screen, stroke=2) for x in range(30, 330, 100)] for y in range(30, 330, 100)])

def add_play(box, current_player):
    global plays

    plays.append(Circle(pos=[box.pos[0] + box.size[0]/2, box.pos[1] + box.size[1]/2], radius=20, screen=screen, color=current_player))

def add_reaction(box):
    @box.click()
    def on_click():
        global current_player, board, player1_moves, player2_moves, player1, player2
        
        if board.index(box) in (player1_moves or player2_moves):
            return
        
        if current_player == "red":
            add_play(box, current_player)
            player2_moves.append(board.index(box))
            current_player = "blue"

        elif current_player == "blue":
            add_play(box, current_player)
            player1_moves.append(board.index(box))
            current_player = "red"

        check_game()
   
def is_win(moves):
    if len(moves) < 3: 
        return False        
    
    m = [[0,1,2], [0,4,8], [0,3,6], [6,4,2], [3,4,5], [1,4,7], [2,5,8], [6,7,8]]
    m_comb = []
    for i in range(len(m)):
        m_comb.append(list(*combinations(m[i], 3)))        
    m_comb += [i[::-1] for i in m_comb]
        
    if len(moves) == 3:
        if moves in (m + m_comb):
            return True
        
        else:
            if moves[-3:] in (m + m_comb):
                return True
            else:
                return False
   
def check_game():
    global winner, player1_moves, player2_moves

    if is_win(player1_moves):
        winner = "blue"
    elif is_win(player2_moves):
        winner = "red"

    else:
        if len(plays) == 9:
            winner = "tie"
                
for box in board:
    add_reaction(box)
    
def reset():
    global player1_moves, player2_moves, plays, winner, reset_btn
    player1_moves, player2_moves, plays, winner = [],[],[],None
    reset_btn.onclick(lambda: None)

reset_btn = Button(pos=["right-center", "bottom-center"], radius=28, screen=screen, text="Reset", color="white", textcolor="black", fontsize=20)
    
while True:
    screen.check_events()

    screen.fill()

    if winner == None:
        for b in board:
            b.draw()
        
        for p in plays:
            p.draw()
    else:
        if winner == "tie":
            Text(pos=["center", "center"], text="Empate", fontsize=36, screen=screen).draw()
        
        else:
            Text(pos=["center", "center"], text=f"Ganador: {winner}", fontsize=36, screen=screen, color=winner).draw()
    
        reset_btn.draw()
        reset_btn.onclick(lambda: reset())
    
    screen.update()