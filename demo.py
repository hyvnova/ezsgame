from ezsgame import *

tile_size = 32
scale = 1
view_pos = Pos(0, 0) # The position of the top left corner of the view in the world


window: Window = Window(
    Size((tile_size * 16) * scale, (tile_size * 16) * scale), show_fps=True
)


pos_text = Text("", Pos(0, 0), 14)

while True:
    window.check_events()
    window.fill()


    # Draw grid lines 
    for x in range(0, window.size[0], tile_size):
        draw.line(window.surface, (115, 115, 115), (x, 0), (x, window.size[1]))
    
    for y in range(0, window.size[1], tile_size):
        draw.line(window.surface, (115, 115, 115), (0, y), (window.size[0], y))

    # Highligh the square under the mouse
    mouse_pos = get_mouse_pos()

    # Mouse position in the world
    mouse_pos = Pos(
        mouse_pos[0] + view_pos[0],
        mouse_pos[1] + view_pos[1]
    )

    square_pos = (
        mouse_pos[0] // tile_size * tile_size,
        mouse_pos[1] // tile_size * tile_size,
    )

    draw.rect(window.surface, (255, 0, 0), (square_pos, (tile_size, tile_size)), 1)
    
    # Draw current mouse position
    pos_text.text = f"{square_pos}"
    # Prevent text from going off screen
    if pos_text.x + pos_text.width > window.size[0]:
        pos_text.x -= pos_text.width

    if pos_text.y + pos_text.height > window.size[1]:
        pos_text.y -= pos_text.height

    pos_text.draw()



    window.update()
