from ezsgame.all import *

screen = Screen(title="Sample Demo", fps=144, show_fps=True)

player = Rect([ 200, 300], [ 50,50 ], 
            components=[
                Controllable(keys=["a","d", "w", "a"], speed=[-25, 25, 0, 0])
            ])

camera = Camera(player)
camera.setmethod(Follow(camera))

background = Image([ 0, 0 ], [ 720,480 ], "img/blue_sky.png")
floor = Image([ 0,350 ], [ 720, 120 ], "img/grass.png")
rock = Image([ 550, 250 ], [ 100, 100 ], "img/rock.png")

while True:
    screen.check_events()
    screen.fill()
    
    #logic
    camera.scroll()
    
    # scene drawing
    background.draw()
    floor.draw()
    rock.draw()
    
    rock.pos.x = 550 - camera.offset.x

    player.draw()
    
    screen.update()