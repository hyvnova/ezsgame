from main import *
import random, asyncio

# INIT --------------------------------------------------------------------------------------------------------------
s = Screen(title="Jueguito", fps=60, show_fps=True, size=[480, 400])

# START -------------------------------------------------------------------------------------------------------------
bar = Rect(size=[s.size[0]- 20, 50], pos=[0, 50], color=color['white'], rounded=2)
# object to fill the bar
filled_bar = Rect(size=[10, bar.size[1]], pos=[0, 50], color=color['red'])

filling = True
def fill_bar(percent=100, step=1): 
    # check if the bar is already filled to the desired percent
    if filled_bar.size[0] < bar.size[0] * percent / 100:
        # fill the bar
        filled_bar.size[0] += step
    else:
        global filling
        filling = False
        
def unfill_bar(percent=0, step=1):
    percent = 1 if percent == 0 else percent
    if filled_bar.size[0] > bar.size[0] * percent / 100:
        filled_bar.size[0] -= step  
    else:
        global filling
        filling = True

circle = Circle(pos=["center", 0], radius=20, color=color['blue'])

time = [0,0,0]

time_text = Text(pos=["center", "center"], text=f"{time[0]}:{time[1]}:{time[2]}", size=30, color=color['green'])

def update_time():
    global time
    time[2] += 1
    if time[2] == 60:
        time[2] = 0
        time[1] += 1
        if time[1] == 60:
            time[1] = 0
            time[0] += 1
            
    time_text.update(text=f"{time[0]}:{time[1]}:{time[2]}")

# TIME ---------------------------------------------------------------------------------------------------------------
s.time.addInterval(name="test", callback=update_time, time=1)
# EVENTS -------------------------------------------------------------------------------------------------------------

while True:
    # IN-LOOP EVENTS ---------------------------------------------------------------------------------------------------------
    s.check(s)

    # BASE ------------------------------------------------------------------------------
    s.fill(color['black'])

    # LOGIC ----------------------------------------------------------------------------
    if filling:
        fill_bar()
    else:
        unfill_bar()
    
    if circle.isOut(s):
        circle.pos[1] = 0
    circle.pos[1] += 1
    
    # DRAW ------------------------------------------------------------------------------
    filled_bar.draw(s)
    bar.draw(s)
    circle.draw(s)
    time_text.draw(s)
    
    # UPDATE ----------------------------------------------------------------------------
    s.update()

                