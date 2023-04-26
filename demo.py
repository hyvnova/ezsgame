from ezsgame import *

tile_size = 32
scale = 1

window: Window = Window(
    Size((tile_size * 16) * scale, (tile_size * 16) * scale), show_fps=True
)

pos_text = Text("", Pos(0, 0), 14)
view_controller = Controller(speed=[-1, 1, -1, 1], use_delta_time=False)

while True:
    window.check_events()
    window.fill()

    # Draw grid lines 
    for x in range(0, window.size[0], tile_size):
        draw.line(window.surface, (115, 115, 115), (x, 0), (x, window.size[1]))
    
    for y in range(0, window.size[1], tile_size):
        draw.line(window.surface, (115, 115, 115), (0, y), (window.size[0], y))


    # Move the view
    World.pos += view_controller.get_speed("simple")

    # Highligh the square under the mouse
    mouse_pos = get_mouse_pos()
    tile_pos = mouse_pos // tile_size * tile_size
    draw.rect(window.surface, (255, 0, 0), (tile_pos, (tile_size, tile_size)), 1)
    
    # Draw current mouse position
    pos_text.text.set(f"{tile_pos}  {mouse_pos}")
    pos_text.pos = mouse_pos + 10

    pos_text.draw()


    window.update()
