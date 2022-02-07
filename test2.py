from ezsgame.main import *
import random, json

s = Screen(show_fps=True)

box = Rect(pos=["center","center"], size=[50,50])

inbox = InputBox(pos=["center", "top"], size=[200,100], screen=s)
    
styles = [{}]
def reload():
    try:
        with open("stylepack.json", "r") as f:
            styles[0] = json.load(f)
            load()
    except:
        return
        
def load():
    try:
        if inbox.value in styles[0]:    
            box.load_style_pack(styles[0][inbox.value])
    except:
        return

s.events.on("mousedown", lambda: load())
s.time.add(250, lambda: reload(), "reloader")

while True:
    s.check()
    s.fill((0,0,0))
    
    inbox.draw(s)
    try:
        box.draw(s)
    except:
        continue
    s.update()