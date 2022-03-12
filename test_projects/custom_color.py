from ezsgame.main import *
s = Screen()

boxes = [InputBox(pos=["left-center","top-center"], size=[60,60], screen=s),
    InputBox(pos=["center","top-center"], size=[60,60], screen=s),
    InputBox(pos=["right-center","top-center"], size=[60,60], screen=s)]

player = Rect(pos=["center", "center"], size=[70,70], color="white", screen=s)

@s.add_interval(350)    
def update_color():
    global player, boxes
    if not all(box.value.isdigit() for box in boxes):
        return
    
    color = [int(boxes[0].value), int(boxes[1].value), int(boxes[2].value)]
    
    for i, c in enumerate(color):
        if c > 255:
            color[i] = 255
        elif c < 0:
            color[i] = 0
            
    player.color = color        

while True:
    s.check_events()
    s.fill()
    
    for box in boxes:
        box.draw(s)
    
    player.draw(s)

    s.update()