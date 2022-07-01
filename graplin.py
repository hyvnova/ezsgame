from ezsgame.basics import *
import random

screen = Screen(show_fps=True)

player = Rect(["center", "center"], [50, 50], color="yellow")

grapling = Line(center_of(player), center_of(player) + Vector2(1,1),  color="blue")
going_pos = []

freezed = False    

score = 0
score_text = Text(f"Score: {score}", ["center", "top"], fontsize=28, color="white",)

@screen.on_event("click")
def on_click():
    global going_pos
    
    going_pos = screen.mouse_pos()
    
    @screen.add_interval(80, "grapling move")
    def grapling_move():
        global freezed
        
        if freezed:
            return
        
        step = 5 
        current = grapling.end
        
        # X axis
        if going_pos[0] > current[0]:

            # if adding step causes overpass
            if current[0] + step > going_pos[0]:
                grapling.end[0] = going_pos[0]
            
            else:
                grapling.end[0] += step
                     
        elif going_pos[0] < current[0]:
          
            # if adding step causes overpass
            if current[0] - step < going_pos[0]:
                grapling.end[0] = going_pos[0]
            
            else:
                grapling.end[0] -= step          
                
        # Y axis
        if going_pos[1] > current[1]:
                
                # if adding step causes overpass
                if current[1] + step > going_pos[1]:
                    grapling.end[1] = going_pos[1]
                
                else:
                    grapling.end[1] += step
                    
        elif going_pos[1] < current[1]:
            # if adding step causes overpass
            if current[1] - step < going_pos[1]:
                grapling.end[1] = going_pos[1]
            
            else:
                grapling.end[1] -= step
                
    
        # grabs something 
        if is_colliding(grapling, box, True):
            box.color = "red"
            pull(box)
        else:
            box.color = "white"           
          
def pull(obj):
    global freezed
    freezed = True

    @screen.add_interval(250, "pulling")
    def pulling():
        global grapling, freezed, player, score, score_text
        
        if not freezed:
            return
        
        step = 3

        end = center_of(player)
        obj_center = center_of(obj)
        
        # bring obj and grapling to player
        
        # X axis
        if end[0] > obj_center[0]:
           
            # if adding step causes overpass
            if obj_center[0] + step > end[0]:
                obj_center[0] = end[0]
            
            else:
                obj_center[0] += step
                
        elif end[0] < obj_center[0]:
            # if adding step causes overpass
            if obj_center[0] - step < end[0]:
                obj_center[0] = end[0]
            
            else:
                obj_center[0] -= step
                
        # Y axis
        if end[1] > obj_center[1]:
            # if adding step causes overpass
            if obj_center[1] + step > end[1]:
                obj_center[1] = end[1]
            
            else:
                obj_center[1] += step
                
        elif end[1] < obj_center[1]:
            # if adding step causes overpass
            if obj_center[1] - step < end[1]:
                obj_center[1] = end[1]
            
            else:
                obj_center[1] -= step
                
        grapling.end = obj_center
        obj.pos = obj_center - [obj.size.width / 2, obj.size.height / 2]
        
        # if reached
        if is_colliding(box, player):
            freezed = False
            screen.remove_interval("pulling")     
            
            grapling.end = center_of(player)
            
            # add score
            score += 1
            score_text.text = f"Score: {score}"
            
            # give a random position to box
            box.pos = Pos(random.randint(15, screen.size.width), random.randint(15, screen.size.height))
                          
# randonly moves box far from player       
def move(obj):    
    @screen.add_interval(250, "moving")
    def moving():
        global freezed
        
        if freezed:
            return
        
        step = lambda : random.randint(-10,10)
        obj.pos += Vector2(step(), step())
        
        # if out of screen
        if is_out(obj)[0]:
            obj.pos = Pos(random.randint(15, screen.size.width), random.randint(15, screen.size.height))
          
box = Rect([200, 50], [30, 30], color="white")
move(box)

win_audio = Sound("audio.mp3")
win_img = Image([0,0], screen.size.copy(), "wakeup.png")

while True:
    screen.check_events()
    screen.fill()
    
    if score >= 10:
        win_audio.play()
        win_img.draw()

    else:
        player.draw()
        grapling.draw()            
        box.draw()
        score_text.draw()
            
    screen.update()
