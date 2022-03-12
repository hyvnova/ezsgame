from ezsgame.main import *
s = Screen(size=(400,360))
boxes = [Rect(pos=(100,100), size=(100,100), color="white", rounded=1),Rect(pos=(200,100), size=(100,100), color="white", rounded=1),Rect(pos=(200,200), size=(100,100), color="white", rounded=1),Rect(pos=(100,200), size=(100,100), color="white", rounded=1)]
texts = [Text(pos=(150,150), text="", fontsize=20, color="white"),Text(pos=(250,150), text="", fontsize=20, color="white"),Text(pos=(250,250), text="", fontsize=20, color="white"),Text(pos=(150,250), text="", fontsize=20, color="white")]
intput_boxes = [InputBox(pos=[120, 40], size=[50,50], screen=s), InputBox(pos=[220, 40], size=[50,50], screen=s),InputBox(pos=[40, 130], size=[50,50], screen=s), InputBox(pos=[40, 210], size=[50,50], screen=s) ]
while True:
    s.check_events()
    s.fill("black")
    texts[0].update(text=f"{intput_boxes[2].value}{intput_boxes[0].value}")
    texts[1].update(text=f"{intput_boxes[2].value}{intput_boxes[1].value}")
    texts[2].update(text=f"{intput_boxes[3].value}{intput_boxes[0].value}")
    texts[3].update(text=f"{intput_boxes[3].value}{intput_boxes[1].value}")
    for box in boxes:
        box.draw(s)
    for text in texts:
        text.draw(s)
    for box in intput_boxes:
        box.draw(s)    
    s.update()