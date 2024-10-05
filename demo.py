from ezsgame import *
from components import *

window = Window(title="2v2")


# Barreras
barrier_pos = [
    Pos(70, "center"),       # Pos inicial P1
    Pos(90, "top-center")    # Pos inicial P2 
]

# Projectiles
proj_pos = [
    Pos("right", "center"),  # P1
    Pos("right-center", "top") # P2
]

# ! No renombren las funciones :)

def p1_barrier(y: float, h: int, acceleration: int) -> int:
    if y < 0 + h*2: return DOWN
    if y + h >= window.size.y - h*2: return UP
    return DOWN

def p2_barrier(y: float, h: int, acceleration: int) -> int:
    if y < 0 + h*2: return DOWN
    if y + h >= window.size.y - h*2: return UP
    return UP

    
def p1_proj(x: float, w: int, acceleration: int) -> int:
    return UP # Rapido
    
def p2_proj(x: float, w: int, acceleration: int) -> int:
    return DOWN if acceleration < 0 else UP # Lento



# No tocar de aqui en adelante.  ---------------------------------------------------------------------------------------------------
BAR_TOP_SPEED = 8
PROJECTILE_TOP_SPEED = 12

UP = 1
DOWN = 2
KEEP = 3

nexo = Rect(Pos(10, "center"), Size(50))

barriers = [Rect(pos, Size(20, 60), color="blue") for pos in barrier_pos] 
barrier_accelerations = [1 for _ in barriers]
barrier_movement = [p1_barrier, p2_barrier]

projectiles = [Rect(pos, Size(25), color="red") for pos in proj_pos] 
proj_accelerations = [1 for _ in projectiles]
proj_movement = [p1_proj, p2_proj]

def move_barrier(barrier: Rect, movement: Callable[[float, int, int], int], acc: int) -> int:
    acc_val = movement(barrier.pos.y, barrier.size.y, acc)

    if not (1 <= acc_val <= 3):
        return 3

    if acc_val == UP:
        acc -= 1
        
    if acc_val == DOWN:
        acc += 1
        
    if acc > BAR_TOP_SPEED:
        acc = BAR_TOP_SPEED
    if acc < -BAR_TOP_SPEED:
        acc = 1
        
    barrier.pos.y += acc
    return acc

def move_proj(proj: Rect, movement: Callable[[float, int, int], int], acc: int) -> int:
    acc_val = movement(proj.pos.x, proj.size.x, acc)

    if not (1 <= acc_val <= 3):
        return 3

    if acc_val == UP:
        acc -= 1
        
    if acc_val == DOWN:
        acc += 1
        
    if acc > PROJECTILE_TOP_SPEED:
        acc = PROJECTILE_TOP_SPEED
    if acc < -PROJECTILE_TOP_SPEED:
        acc = 1
        
    proj.pos.x += acc
    return acc

stop = True
@on_key("down", "space", "pause")
def pause():
    global stop
    stop = not stop

while True:
    window.check_events()
    window.fill("black")

    # logic
    if not stop:
        for i, barrier in enumerate(barriers):
            barrier_accelerations[i] = move_barrier(barrier, barrier_movement[i], barrier_accelerations[i])
        
        for i, proj in enumerate(projectiles):
            proj_accelerations[i] = move_proj(proj, proj_movement[i], proj_accelerations[i])
            proj.y += -2 if proj.y  > nexo.y else 2

    # collision detection
    for proj in projectiles:
        if is_colliding(nexo, proj):
            stop = True
            nexo.styles.color = "red"
        
        for barrier in barriers:
            if is_colliding(barrier, proj): 
                barrier.y = -9999
                proj.x = -9999
    
    # drawing
    nexo.draw()
    for barrier in barriers:
        barrier.draw()
    for proj in projectiles:
        proj.draw()

    window.update()
