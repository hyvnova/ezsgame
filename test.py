from main import *
import random, asyncio

# INIT --------------------------------------------------------------------------------------------------------------
s = Screen(title="Jueguito", fps=60, show_fps=True, size=[480, 400])

# START -------------------------------------------------------------------------------------------------------------
player = Rect(size=[40,40], pos=["left", "center"], color=color['green'])

bullets = []

bullets_left = 10   
bullets_left_text = Text(text=f"Bullets left: {bullets_left}", pos=["center", "bottom"], color=color['white'], size=20, surface=s)

reloading_text = Text(text="Reloading...", pos=["center", "center"], color=color['white'], size=18, surface=s)

def shoot(mouse_pos):
    global can_shoot
    if can_shoot == False:  
        return
    
    global bullets_left
    
    if bullets_left <= 0:
        bullets_left_text.update(text=f"Bullets left: {bullets_left}", color=color['red'])
        return
    
    divs = s.div("y", 3)
    for i in range(len(divs)):
        r = [x for x in range(int(divs[i][0]), int(divs[i][1]))]
        if i == 0:
            if mouse_pos[1] in r:
                direction = "top"
        elif i == 1:
            if mouse_pos[1] in r:
                direction = "center"
        elif i == 2:
            if mouse_pos[1] in r:
                direction = "bottom"
                
    pos = [player.pos[0] + player.size[0]/2, player.pos[1] + player.size[1]/2]
    bullets.append([Circle(pos=pos, radius=5, color=color['white'], surface=s), direction])
    bullets_left -= 1

enemys = []
def spawn_enemy(q=3):
    for i in range(q):
        enemys.append(Rect(size=[40,40], pos=[random.randint(s.half()[0] - 40, s.size[0] - 40), 0], color=color['red'], surface=s))

points = 0
points_text = Text(text=f"Points: {points}", pos=["center", "top"], size=28, color=color['white'], fontname="Arial")

spawn_enemy(5)

# ANIMATION
reloading = False
can_shoot = True
def reload_bullets():
    if len(bullets) > 0:
        return

    global bullets_left
    if bullets_left < 10:
        bullets_left += 1
        if bullets_left <= 3:
            c = color['red']
        elif bullets_left <= 7:
            c = color['yellow']
        else:
            c = color['white']
        
        bullets_left_text.update(text=f"Bullets left: {bullets_left}", color=c)
        s.sleep(100)


win_text = Text(text="Que te parecio? HDP", pos=["center", "center"], size=40, color=color['green'], fontname="Arial")
# EVENTS -------------------------------------------------------------------------------------------------------------


while True:
    # IN-LOOP EVENTS ---------------------------------------------------------------------------------------------------------
    s.events.check(s.events.get(), s)
    s.events.on("mousedown", shoot, [s.mousePos()])

    # BASE ------------------------------------------------------------------------------
    s.fill(color['black'])

    # LOGIC ----------------------------------------------------------------------------
    
        
    if reloading:
        reload_bullets()
          
    if bullets_left <= 0:
        reloading = True
        can_shoot = False
    if bullets_left == 10:
        reloading = False
        can_shoot = True
                
    if points >= 10:
        can_shoot = False
        reloading = False
        reloading_text
        win_text.draw(s)
        enemys = []
        bullets = []
        reloading_text.update(pos=[-100, -100])
        player.pos = [-100, -100]
    else:
        if len(enemys) == 0:
            spawn_enemy(random.randint(1, 5))
        
    # DRAW ------------------------------------------------------------------------------
    player.draw(s)
    points_text.draw(s)
    bullets_left_text.draw(s)

    if can_shoot == False:
        reloading_text.draw(s)
    
    for enemy in enemys:
        enemy.move(x=0, y=-random.randint(2, 4), surface=s)    
        enemy.draw(s)
        if enemy.isOut(s):
            enemy.pos = [random.randint(s.half()[0] - 40, s.size[0] - 40), 0]
              
    for item in bullets:
        item[0].draw(s)
        if item[1] == "top":
            item[0].move(x=5, y=2, surface=s)
        elif item[1] == "center":
            item[0].move(x=5, y=0, surface=s)
        elif item[1] == "bottom":
            item[0].move(x=5, y=-2, surface=s)
        
        if item[0].isOut(s):
            bullets.remove(item)    
        
        for enemy in enemys:
            if item[0].collision(obj=enemy, surface=s):
                enemys.remove(enemy)
                bullets.remove(item)
                points += 1
                break
            
    
    # UPDATE ----------------------------------------------------------------------------
    s.update()
    points_text.update(text=f"Points: {points}")
    bullets_left_text.update(text=f"Bullets left: {bullets_left}")
                