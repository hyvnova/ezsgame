from ezsgame.all import *
from npc_logic import think

screen = Screen()

# PLAYER #####################################################################################
p = Rect(["center","bottom-center"], [50,50], color="green", components=[
    Controllable(speed=[-25,25,0,0])
])

# cooldown bar
cd_bar = Bar(pos=["center", "bottom"], size=[200, 30], min=0, max=100, value=100)

# shoot
bullets = Group()
@screen.on_key("down", ["w"])
def shoot():
    if cd_bar.value == 100:
        bullets.add(Rect(pos=center_of(p), size=[10,10]))
        
        cd_bar.value = 0
        
        # cooldown
        @screen.add_interval(150, "cooldown")
        def charge_cd():
            cd_bar.value += 3

            if cd_bar.value >= 100:
                cd_bar.value = 100
                screen.remove_interval("cooldown")


# move bullets
def move_bullets():
    bullets.map(lambda bullet: move(bullet, 0,2))        

# remove bullet excess
def remove_bullets():
    bullets.filter(lambda bullet: bullet.pos[1]>0)
    
    
#####################################################################################

# ENEMY ###################################################################
enemy = Rect(pos=["center", "top-center"], size=[50,50], color="white")

def hit():
    enemy.color = "red"
    screen.shake(10)
    screen.shake(15)
    screen.shake(20)
    
    @screen.add_interval(750, "restore color")
    def restore_color():
        enemy.color = "white"
        screen.remove_interval("restore color")
        
###########################################################################

# UI #########################################################################

points = 0
points_text = Text(f"Points: {points}", pos=["center", "top"], fontsize=22)

while True:
    screen.check_events()
    
    screen.fill()
    
    # DRAWING ############
    p.draw()
    
    cd_bar.draw()
    
    #bullets
    move_bullets()
    bullets.draw()
    
    # remove bullet excess
    remove_bullets()
    
    
    # ENEMY DRAW AND LOGIC
    think(enemy, p, bullets, screen.size.width, 5)

    for bullet in bullets:
        if is_colliding(enemy, bullet):
            points += 1
            points_text.text = f"Points: {points}"
            hit()

    enemy.draw()
    
    #UI
    points_text.draw()
    
    screen.update()