from ezsgame import *
from random import choice

window = Window(title="Bouncing Ball - (Code Sample)", show_fps=True)


ball = Circle(
    pos=Pos("center", "center"),
    radius=30,
    
    # Style
    color="white"
) 

# ball speed
speed: List[int] = [choice((-5, 5)), choice((-5, 5))] # start with random speed


# mainloop
while True:
    
    window.check_events()
    
    window.fill("black")
    
    # ---------- Game Logic -------------
    
    # If ball hits top or bottom
    if (ball.pos.y - ball.radius) <= 0 or (ball.pos.y + ball.radius) >= window.size.height:
        
        # invert y speed
        speed[1] *= -1
        
    # if ball hits left or right
    if (ball.pos.x - ball.radius) <= 0 or (ball.pos.x + ball.radius) >= window.size.width:
        
        # invert x speed
        speed[0] *= -1
        
        
    # Add speeds into ball position
    ball.pos += speed 
    
    # --------- Drawing -----------
    ball.draw()
    
    
    window.update()