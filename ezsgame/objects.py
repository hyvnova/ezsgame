import pygame as pg
from ezsgame.premade import Rect, Object, Unit
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core import grid
from pathfinding.finder.a_star import AStarFinder


pg.init()

class IRect(Rect):
    def __init__(self,  pos, size, screen, **styles):
        super().__init__(pos, size, **styles)
        if screen == None:
            raise Exception(f"InputBox object needs screen (ID : {self._id})")
        self.screen = screen
        
    def click(self, *args, **kwargs):
        def wrapper(func):
            self.screen.events.add_event_listener("click", self, func)
        return wrapper
    
    def hover(self, *args, **kwargs):
        def wrapper(func):
            self.screen.events.add_event_listener("hover", self, func)
        return wrapper

    def unhover(self, *args, **kwargs):
        def wrapper(func):
            self.screen.events.add_event_listener("unhover", self, func)
        return wrapper
    
    def unclick(self, *args, **kwargs):
        def wrapper(func):
            self.screen.events.add_event_listener("unclick", self, func)
        return wrapper

class Grid(Object):
    def __init__(self, pos, size, grid_size, screen, **styles):
        super().__init__(pos, size, **styles)
        self.box_color = styles.get("box_color", "white")
        self.screen = screen
        self.grid_size = grid_size
        self.matrix = self.grid_div(*self.grid_size) 
        self.grid = self.grid_split(self.matrix, self.grid_size[1])
        self.colors_grid = [[obj.color for obj in row] for row in self.grid]
          
    def div(self, axis, q):
        r'''
        Return list of division points of the screen -> [[x1, x2], [x1, x2], ...]
        '''
        divs = []
        if axis == "x":
            # should append [start, end] for each division
            for i in range(q):
                divs.append([round(i * self.size[0] / q, 1), round((i + 1) * self.size[0] / q, 1)])
        elif axis == "y":
            # should append [start, end] for each division
            for i in range(q):
                divs.append([round(i * self.size[1] / q, 1), round((i + 1) * self.size[1] / q, 1)])
            
        return divs
        
    def grid_div(self, cols=3, rows=3, transpose=False):
        r'''
        Returns the division of the screen into a grid -> [[x, y, w, h], [x, y, w, h], ...]
        '''
        grid = []
        divs_x = self.div("x", cols)
        box_width = divs_x[-1][0] - divs_x[-2][0]
        divs_y = self.div("y", rows)
        box_height = divs_y[-1][0] - divs_y[-2][0]
        self.grid_size = [rows, cols]
        
        for i in range(cols):
            for j in range(rows):
                if transpose:
                    grid.append([divs_x[j][0], divs_y[i][0], box_width, box_height])
                else:
                    grid.append([divs_x[i][0], divs_y[j][0], box_width, box_height])
        self.grid_space = len(grid)
        self.grid_box_size = [box_width, box_height]
        return grid
    
    def grid_split(self, matrix, grid_size):
        r'''
        Splits a matrix into a grid : [1,2,3,4,5,6,7,8,9] -> [[Unit,Unit,Unit], [Unit,Unit,Unit], [Unit,Unit,Unit]]
        '''
        if isinstance(grid_size, list) or isinstance(grid_size, tuple):
            grid_size = grid_size[1]
        
        grid = [matrix[i:i+grid_size] for i in range(0, len(matrix), grid_size)]
        return [[Unit(pos=i[:2], size=i[2:], color=self.box_color)  for i in row] for row in grid]
    
    def draw(self, screen=None):
        screen = self.screen if screen == None else screen
        
        pg.draw.rect(screen.surface, self.color, [*self.get_pos(screen), *self.size], int(self.rounded))
        for row in self.grid:
            for obj in row:
                obj.draw(screen)
            
    def highlight_current(self, color="red"):
        for i in range(len(self.colors_grid)):
            for j in range(len(self.colors_grid[i])):
                if self.colors_grid[i][j] != color:
                    self.grid[i][j].color = self.colors_grid[i][j]
        
        mouse_pos = self.screen.mouse_pos()
        pos = int(mouse_pos[0] // self.grid_box_size[0]), int(mouse_pos[1] // self.grid_box_size[1])
        # select the current box
        
        if pos[0] < self.grid_size[0] and pos[1] < self.grid_size[1]:
            self.grid[pos[0]][pos[1]].color = color

    def get_path(self, start,end):
        int_grid = [[1 for x in j] for j in self.grid]
    
        _grid = grid.Grid(matrix=int_grid)
        start = _grid.node(*start)
        end = _grid.node(*end)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        path, runs = finder.find_path(start=start, end=end, grid=_grid)
        
        return path

    def highlight_path(self, start, end, color="red"):
        if  0 > (start[0] or start[1]) or start[1] > self.grid_size[1] or start[0] > self.grid_size[0]:
            raise Exception("Start position is out of bounds")
        if 0 > (end[0] or end[1]) or end[1] > self.grid_size[1] or end[0] > self.grid_size[0]:
            raise Exception("End position is out of bounds")
        if start == end:
            raise Exception("Start and end positions must be different")
        
        path = self.get_path(start, end)
        for i in range(len(path)):
            self.grid[path[i][0]][path[i][1]].color = color
    

    def get_current(self):
        mouse_pos = self.screen.mouse_pos()
        pos = int(mouse_pos[0] // self.grid_box_size[0]), int(mouse_pos[1] // self.grid_box_size[1])
        # select the current box
        if pos[0] < self.grid_size[0] and pos[1] < self.grid_size[1]:
            return self.grid[pos[0]][pos[1]]
        else:
            return None
