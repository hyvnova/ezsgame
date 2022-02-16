from ezsgame.main import *
import json, os

s = Screen()

buttons = [
    Button(pos=[40, s.size[1]-40], radius=27, screen=s, text="Add", textcolor=(88, 230, 23), color="white", fontsize=20),
    Button(pos=[100, s.size[1]-40], radius=27, screen=s, text="Remove", textcolor=(230, 23, 109), color="white", fontsize=14),  
    Button(pos=[160, s.size[1]-40], radius=27, screen=s, text="Move", textcolor="blue", color="white", fontsize=20),
    Button(pos=[220, s.size[1]-40], radius=27, screen=s, text="+", textcolor="black", color="white", fontsize=24),
    Button(pos=[280, s.size[1]-40], radius=27, screen=s, text="-", textcolor="black", color="white", fontsize=24),
    
    Button(pos=[680, 40], radius=22, screen=s, text="Save", textcolor="black", color="white", fontsize=16),
    Button(pos=[680, 100], radius=22, screen=s, text="Load", textcolor="black", color="white", fontsize=16),
]

objects = []
current = [None]
ui_objects = {}
mode = [None]  


# add
@buttons[0].click()
def add():
    rect = IRect(pos=["center", "center"], size=[50, 50], color="white", screen=s)
    @rect.hover()
    def hover():
        if f"click_{rect._id}" in ui_objects:
            if current[0] == rect:
                click_red = Rect(pos=[rect.pos[0] - 5, rect.pos[1] - 5], size=[rect.size[0] + 10, rect.size[1] + 10], color=(255, 15, 115), rounded=2,  screen=s)
                ui_objects[f"click_{rect._id}"] = click_red

            if f"hover_{rect._id}" in ui_objects:
                del ui_objects[f"hover_{rect._id}"]
        else:
            hover_rect = Rect(pos=[rect.pos[0] - 5, rect.pos[1] - 5], size=[rect.size[0] + 10, rect.size[1] + 10], color=(255, 82, 154), rounded=1,  screen=s)
            ui_objects[f"hover_{rect._id}"] = hover_rect

    @rect.unhover()
    def unhover():
        if f"hover_{rect._id}" in ui_objects:
            del ui_objects[f"hover_{rect._id}"]

    @rect.click()
    def click():
        if f"click_{rect._id}" in ui_objects:
            del ui_objects[f"click_{rect._id}"]
            current[0] = None
            if mode[0] == "move":
                mode[0] = None
        else:
            click_red = Rect(pos=[rect.pos[0] - 5, rect.pos[1] - 5], size=[rect.size[0] + 10, rect.size[1] + 10], color=(255, 15, 115), rounded=2,  screen=s)
            ui_objects[f"click_{rect._id}"] = click_red
            current[0] = rect
        
            
    objects.append(rect)

# remove
@buttons[1].click()
def remove():
    if current[0] != None:
        del ui_objects[f"click_{current[0]._id}"]
        objects.remove(current[0])
        current[0] = None
            
# move
@buttons[2].click() 
def move():
    mode[0] = "move"
    
# + size
@buttons[3].click() 
def add_size():
    if current[0] != None:
        current[0].size[0] += 10
        current[0].size[1] += 10
        
# - size
@buttons[4].click() 
def sub_size():
    if current[0] != None:
        current[0].size[0] -= 10
        current[0].size[1] -= 10
        
# save
@buttons[5].click()
def save():
    global objects
    file = "save.json"
    objs = objects
    
    with open(file, 'w') as f:
        f.write("{\n\n}")

    with open(file, 'r') as f:
        data = json.load(f)

    if not isinstance(objs, list):
        objs = [objs]
        
    for obj in objects:
        obj_class = str(obj.__class__).split(".")[-1].split("'")[0]
        obj_build_var = f"{obj_class}("
        for key,val in obj.__dict__.items():
            if key[0] != "_":
                if key == ("pos" or "size"):
                    if isinstance(val, tuple):
                        val = list(val)
                
                if key == 'screen':
                    val = None
                
                obj_build_var += f"{key}={val}, "
            
        obj_build_var = obj_build_var[:-2] + ")"
        
        data[obj._id] = obj_build_var
            
    with open(file, 'w') as f:
        json.dump(data, f)
        
    saved_text = Text(pos=["center", "center"], text="Saved", fontsize=30, screen=s, color="white")
    ui_objects[f"saved_{saved_text._id}"] = saved_text
    @s.add_interval(1000, f"saved_{saved_text._id}")   
    def remove_text():
        del ui_objects[f"saved_{saved_text._id}"]
        s.time.remove(f"saved_{saved_text._id}")
        
# load
@buttons[6].click() 
def load():
    if not "inputbox" in ui_objects:
        inputbox = InputBox(pos=["center", "top"], size=[200, 50], screen=s, color="white", fontsize=20)
        ui_objects["inputbox"] = inputbox

def _load(file):
    with open(file, 'r') as f:
        data = json.load(f)

    objs = []
    for key, val in data.items():
        val = val.replace("screen=None", "screen=s")        
        objs.append(eval(val))
        
    return objs   

while True:
    s.check_events()
    s.fill()
    for obj in ui_objects.values():
        obj.draw()
    
    for btn in buttons:
        btn.draw(s)
        
    for obj in objects:
        obj.draw(s)
    
    if mode[0] == "move":    
        if current[0] is not None:
            mouse_pos = s.mouse_pos()
            current[0].pos = [mouse_pos[0] - current[0].size[0] / 2, mouse_pos[1] - current[0].size[1] / 2]
            
            
    if "inputbox" in ui_objects:
        inputbox = ui_objects["inputbox"]
        # if inputbox.value matches a file name in the current directory
        if os.path.isfile(inputbox.value):
            objects += _load(inputbox.value)
            del ui_objects["inputbox"]

    s.update()