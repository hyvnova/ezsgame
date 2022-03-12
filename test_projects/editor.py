from ezsgame.main import *
import json, os

s = Screen(show_fps=False
           , fps=120)

buttons = [
    Button(pos=[40, s.size[1]-40], radius=26, screen=s, text="Add", textcolor=(88, 230, 23), color="white", fontsize=20),
    Button(pos=[100, s.size[1]-40], radius=26, screen=s, text="Remove", textcolor=(230, 23, 109), color="white", fontsize=14),  
    Button(pos=[160, s.size[1]-40], radius=26, screen=s, text="Move", textcolor="blue", color="white", fontsize=20),
    Button(pos=[680, 40], radius=22, screen=s, text="Save", textcolor="black", color="white", fontsize=16),
    Button(pos=[680, 100], radius=22, screen=s, text="Load", textcolor="black", color="white", fontsize=16),
    Button(pos=[220, s.size[1]-40], radius=25, screen=s, text="Copy", textcolor="black", color="white", fontsize=18),
    Button(pos=[280, s.size[1]-40], radius=25, screen=s, text="Paste", textcolor="black", color="white", fontsize=16),
]

objects = []
current = [None]
ui_objects = {}
mode = [None]  

def add_interaction(obj): 
    @obj.hover()
    def hover():
        if "click" in ui_objects:
            if current[0] == obj:
                click_red = Rect(pos=[obj.pos[0] - 5, obj.pos[1] - 5], size=[obj.size[0] + 10, obj.size[1] + 10], color=(255, 15, 115), rounded=2,  screen=s)
                ui_objects["click"] = click_red

            if f"hover_{obj._id}" in ui_objects:
                del ui_objects[f"hover_{obj._id}"]
        else:
            hover_rect = Rect(pos=[obj.pos[0] - 5, obj.pos[1] - 5], size=[obj.size[0] + 10, obj.size[1] + 10], color=(255, 82, 154), rounded=1,  screen=s)
            ui_objects[f"hover_{obj._id}"] = hover_rect

    @obj.unhover()
    def unhover():
        if f"hover_{obj._id}" in ui_objects:
            del ui_objects[f"hover_{obj._id}"]

    @obj.click()
    def click():
        if "click" in ui_objects:
            
            
            del ui_objects["click"]
            current[0] = None
            if mode[0] == "move":
                mode[0] = None
        else:
            click_red = Rect(pos=[obj.pos[0] - 5, obj.pos[1] - 5], size=[obj.size[0] + 10, obj.size[1] + 10], color=(255, 15, 115), rounded=2,  screen=s)
            ui_objects["click"] = click_red
            current[0] = obj

# add
@buttons[0].click()
@s.on_key(type="down", keys=["1"])
def add():
    rect = IRect(pos=["center", "center"], size=[50, 50], color="white", screen=s)
    add_interaction(rect)
        
    objects.append(rect)

# remove
@buttons[1].click()
@s.on_key(type="down", keys=["2"])

def remove():
    if current[0] != None:
        del ui_objects[f"click"]
        try:
            objects.remove(current[0])
            del ui_objects[f"hover_{current[0]._id}"]
            del ui_objects[f"click"]
        except:
            pass
        finally:
            current[0] = None
            
# move
@buttons[2].click() 
@s.on_key(type="down", keys=["3"])
def move():
    mode[0] = "move"

# save
@buttons[3].click()
@s.on_key(type="down", keys=["9"])
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
                    
                if key == "objects":
                    continue
                
                obj_build_var += f"{key}={val}, "
            
        obj_build_var = obj_build_var[:-2] + ")"
        
        data[obj._id] = obj_build_var
            
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)
        
    saved_text = Text(pos=["center", "center"], text="Saved", fontsize=30, screen=s, color="white")
    ui_objects[f"saved_{saved_text._id}"] = saved_text
    @s.add_interval(1000, f"saved_{saved_text._id}")   
    def remove_text():
        del ui_objects[f"saved_{saved_text._id}"]
        s.time.remove(f"saved_{saved_text._id}")
        
# load
@buttons[4].click() 
@s.on_key(type="down", keys=["0"])
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
        obj = eval(val)    
        add_interaction(obj)
        objs.append(obj)
        
    return objs   

# copy
@buttons[5].click()
@s.on_key(type="down", keys=["4"])
def copy():
    if current[0] != None:
        copy_obj = current[0].copy()
        copy_obj._id = get_id()
        add_interaction(copy_obj)
        ui_objects["copy"] = copy_obj

# paste
@buttons[6].click()
@s.on_key(type="down", keys=["5"])
def paste():
    if "copy" in ui_objects:
        obj = ui_objects["copy"]
        mouse_pos = s.mouse_pos()
        obj.pos = [mouse_pos[0] - obj.size[0] / 2, mouse_pos[1] - obj.size[1] / 2]
        objects.append(obj)
        
        ui_objects["copy"] = obj.copy()
        ui_objects["copy"]._id = get_id()
        add_interaction(ui_objects["copy"])

# + size x
@s.on_key(type="down", keys=["right"])
def add_width():
    if current[0] != None:
        current[0].size[0] += 10
        
# - size x
@s.on_key(type="down", keys=["left"])
def sub_width():
    if current[0] != None:
        current[0].size[0] -= 10
        
# + size y
@s.on_key(type="down", keys=["up"])
def add_width():
    if current[0] != None:
        current[0].size[1] += 10
        
# - size y
@s.on_key(type="down", keys=["down"])
def sub_width():
    if current[0] != None:
        current[0].size[1] -= 10

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