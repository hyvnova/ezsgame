from ezsgame.all import *

screen = Screen(title="Sample Demo", fps=144, show_fps=True)

player = Rect([ 200, 300], [ 50,50 ], 
            components=[
                Controllable(keys=["a","d", "w", "a"], speed=[-25, 25, 0, 0])
            ])

camera = Camera(player)
camera.setmethod(Follow(camera))

static_group = Group(Sprite([ 0, 0 ], [ 720,480 ], "img/blue_sky.png"), Sprite([ 0,350 ], [ 720, 120 ], "img/grass.png"))
dynamic_group = Group(Sprite([ 550, 250 ], [ 100, 100 ], "img/rock.png"), Sprite([ -50, 250 ], [ 100, 100 ], "img/rock.png"))

def offset_sprite(sprite):
    # add camera offset to sprite position
    sprite.pos[0] = sprite.start_pos[0] - camera.offset.x

while True:
    screen.check_events()
    screen.fill()
    
    #logic
    camera.scroll()
    
    # scene drawing
    static_group.draw()
    dynamic_group.draw()
    
    dynamic_group.map(lambda sprite: offset_sprite(sprite))
    
    player.draw()
    
    screen.update()