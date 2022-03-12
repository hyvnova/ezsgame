from ezsgame.main import *
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

s = IScreen(size=(400, 300), title="Test", fps=60, show_fps=True)
s.grid = s.grid_div(10,10)

boxes = [Rect(pos=i[:2], size=i[2:], color="white") for i in s.grid]

def grid_split(matrix, grid_size):
    return [matrix[i:i+grid_size] for i in range(0, len(matrix), grid_size)]
    
matrix = grid_split(boxes, s.grid_size[1])
colors_matrix  = [i.color for i in boxes]
    
def highlight_current():
    for i in range(len(boxes)):
        boxes[i].color = colors_matrix[i]
    mouse_pos = s.mouse_pos()
    pos = int(mouse_pos[0] // s.grid_box_size[0]), int(mouse_pos[1] // s.grid_box_size[1])
    matrix[pos[0]][pos[1]].color = (255,0,0)
    
def get_path():
    int_matrix = [[1 for x in j] for j in matrix]
    
    grid = Grid(matrix=int_matrix)
    start = grid.node(0, 0)
    end = grid.node(len(matrix)-1, len(matrix[0])-1)

    # Create a finder using the A* algorithm
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

    # Run the path finding algorithm
    path, runs = finder.find_path(start=start, end=end, grid=grid)
    
    return path
    
path = get_path()
    
def highlight_path(path):
    for i in range(len(boxes)):
        boxes[i].color = colors_matrix[i]
    
    for i in range(len(path)):
        matrix[path[i][0]][path[i][1]].color = "red"
        
    # highleight the start and end points
    matrix[0][0].color = "green"
    matrix[-1][-1].color = "green"

while True:
    s.check_events()
    s.fill("black")

    highlight_path(path)

    for box in boxes:
        box.draw(s)
    s.update()