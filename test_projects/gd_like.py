from ezsgame.main import *

s = Screen(show_fps=True)

player = Rect(pos=[50,s.size[1]-50], size=[50,50], color="white", screen=s)

player_controller = Controller(s, keys=["w", "space", "up"], speed=[15,15,15])

Gravity(player, s, [0, -7])

obstacles = []

def spawn_obstacle():
    global obstacles
    obstacle = Rect(pos=[s.size[0], random.randint(0, s.size[1])], size=[50,50], color="red", screen=s)
        
    end_pos = [-50, 0] if random.randint(0,1) else [-50, s.size[1]-50]
    end_pos[1] = random.randint(0, s.size[1]-50)
    
    Slide(s, obstacle, end=end_pos, time=5, step=5)
    obstacles.append(obstacle)

points = 0
points_text = Text(f"{points}", pos=["center", "top"], fontsize=28, color="white", screen=s)
shake_force = 1

@s.add_interval(250)
def add_point():
    global points
    points += 1
    
last_color = s.color
current_color = s.color
@s.add_interval(500)
def gradient():
    global last_color, current_color
    last_color = current_color
    current_color = random_color()

while True:
    s.check_events()
    s.fill_gradient(last_color, current_color, complexity=20)

    x = random.randint(0, 100)
    if x >=99 or x <= 2:
        spawn_obstacle()
        
    if player.pos[1] + player.size[1] > s.size[1]:
        player.pos[1] = s.size[1] - player.size[1]
        
    if player.pos[1] + player.size[1] < 0:
        player.pos[1] = 0 + player.size[1]/4
        
    if shake_force < 0:
        shake_force = 0.5
        
    for obstacle in obstacles:
        obstacle.draw(s)
        if player.is_colliding(obstacle, s):
            obstacle.color = random_color()
            
            points -= 0.35
            points_text.color = "red"
            shake_force += 0.5 if shake_force < 50 else 0
            
        else:
            shake_force -= 0.01 if shake_force > 0 else 0
            
            if obstacle.pos[0] + obstacle.size[0] <=  5:
                obstacles.remove(obstacle)
            
    s.shake(int(shake_force)) 
    
    player.move(0, player_controller.get_speed("any"))
    player.draw(s)
    
    points_text.text = f"{int(points)}"
    points_text.draw(s)
    
    points_text.color = "white"
        
    s.update()
    