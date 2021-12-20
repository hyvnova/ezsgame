import pygame as pg

screen = pg.display.set_mode((200, 200))
pg.display.set_caption('Pygame')

clock = pg.time.Clock()
fps = 60

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        
    screen.fill((0, 0, 0))
    
    pg.display.set_caption(f"Current FPS : {int(clock.get_fps())}")
    
    pg.display.update()
    clock.tick(fps)