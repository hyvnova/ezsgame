from ezsgame.main import *

s = Screen()

player = Rect(pos=['center', "center"], size=[50,50], screen=s, color="green")

objects = [Rect(pos=[random.randint(70, s.size[0]-70), random.randint(70, s.size[1]-70)], size=[random.randint(5, 80),random.randint(5, 80)], screen=s) for i in range(10)]

control = Controller(s)

objects.append(Rect(pos=[50,0], size=[20,80], screen=s))

while True:
    s.check_events()
    s.fill()
    
    player.move(*control.get_speed("simple"))    

    
    for obj in objects:
        if player.is_colliding(obj, s, True):
            player.color = "red"
            obj.color = "red"

        else:
            player.color = "green"
            obj.color = "white"

        obj.draw()

        
    player.draw()
        
    s.update()