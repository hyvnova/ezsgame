import pygame as pg, json
from ezsgame.premade import get_id

class Animation:
    def __init__(self, screen, object, start, end, time=50, step=1, loop=False, done_callback=None):
        self.screen = screen
        self._id = get_id()
        self.object = object
        self.done = False
        self.done_callback = done_callback
        self.start = start
        self.loop = loop
        self.end = end
        self.time = time
        self.step = step    
        self.corrected = False
        self.name = f"slide_{self.start}_{self.end}_{self._id}"
        self.resolve()

    def resolve(self):
        obj_pos = self.object.get_pos(self.screen)
        if self.start == "current":
            self.start = obj_pos.copy()
        if self.end == "current":
            self.end = obj_pos.copy()      
        if isinstance(self.start, list) or isinstance(self.start, tuple):
            self.object.pos = self.start.copy()
            self.start = self.object.get_pos(self.screen)
            
            self.object.pos = self.end.copy()
            self.end = self.object.get_pos(self.screen)
        
            self.object.pos = obj_pos.copy()
        
class Slide(Animation):
    f'''
    - slide object from start to end
    @param start: start position - [x, y] or "current"
    @param end: end position - [x, y] or "current"
    @param time: time in Miliseconds
    @param step: step size
    [If objet is not at start position, it will be moved to start position]
    '''
    def __init__(self, screen, object, start="current", end=["center", "center"], time=10, step=1, loop=False, done_callback=None):
        super().__init__(screen, object, start, end, time, step, loop, done_callback)
        self.screen.time.add(name=self.name, time=self.time, callback=self.update)        

    def update(self):    
        if self.done:
            return
         
        # start
        if self.corrected == False:
            # go to start position
            if self.object.pos != self.start:
                if self.object.pos[0] > self.start[0]:
                    self.object.pos[0] -= self.step
                elif self.object.pos[0] < self.start[0]:
                    self.object.pos[0] += self.step                
                
                if self.object.pos[1] > self.start[1]:
                    self.object.pos[1] -= self.step
                elif self.object.pos[1] < self.start[1]:
                    self.object.pos[1] += self.step
                            
                return True
            else:
                self.corrected = True
                
        # end
        if self.object.pos != self.end:
            if self.object.pos[0] > self.end[0]:
                self.object.pos[0] -= self.step
            elif self.object.pos[0] < self.end[0]:
                self.object.pos[0] += self.step

            if self.object.pos[1] > self.end[1]:
                self.object.pos[1] -= self.step
            elif self.object.pos[1] < self.end[1]:
                self.object.pos[1] += self.step
                
            return True
         
        else:
            if self.loop == True:
                self.corrected = False
                self.object.pos = self.end.copy()
                return True
            
            else:
                self.done = True
                self.screen.time.remove(self.name)
                if self.done_callback != None:
                    self.done_callback()
                
                return False
   
class AlternateColors:
    def __init__(self, colors, reverse=False, reverse_colors_after=0):
        self.colors = colors
        self.current = 0
        self.count = 0
        self.reverse_colors_after = reverse_colors_after
        self.reverse = reverse
        self.n = 0

    def get(self):
        if self.count == 1:
            self.current == len(self.colors)-1
        
        c = self.colors[self.current]
        try:
            n = 1
            if self.reverse:
                if self.current == len(self.colors)-1:
                    self.count += 1
                    
                if self.count == 2:
                    n = -1
                    
                if self.current == 0:
                    self.count = 0          
                           
            if self.count != 1:
                self.current += n if self.colors[self.current + n] else 0
        except:
            self.current = 0
         
        if self.reverse_colors_after:   
            self.n += 1
            if self.n == self.reverse_colors_after:
                self.colors = self.colors[::-1]
                self.n = 0
        return c
             
def create_animation_file(frames, kwargs): 
    """ 
    "size":[[100,100], [10,10]] goes from [100,100] to [10,10]
    "color' : ["white", "red", "blue"]] 
    "stroke : [0, 10] goes  from 0 to 10
    """
    steps = {}    
    if "color" in kwargs:
        alt_color = AlternateColors(kwargs["color"])
        del kwargs["color"]
        steps["color"] = alt_color.get()
        
    for k,v in kwargs.items():
        if len(v) == 2:
            try:
                if len(v[0]) == 2:
                    steps[k] = [max([v[0][0],v[1][0]])/frames, max([v[0][1], v[1][1]])/frames]
                    steps[k][0] = steps[k][0]*1 if v[0][0] < v[1][0] else steps[k][0]
                    steps[k][1] = steps[k][1]*1 if v[0][1] < v[1][1] else steps[k][1]
            except:
                steps[k] = max(v)/frames
                steps[k] = steps[k]*1 if v[0] < v[1] else steps[k]
        
    if "color" in steps:
        kwargs["color"] = steps["color"]
        
    with open("animation.json", "w") as f:
        f.write("{\n\n}")
    index = {"0" : {}}
    for item in kwargs.keys():
        if len(kwargs[item]) == 2:
            try:
                if len(kwargs[item][0]) == 2:
                    index["0"][item] = kwargs[item][0]  
            except:
                index["0"][item] = kwargs[item][0]
                
    
    with open("animation.json", "r" ) as f:
        animation = json.load(f)
        
    animation["0"] = index["0"]
    with open("animation.json", "w") as f:
        json.dump(animation, f, indent=4)

    for i in range(1,frames):            
        index = {f"{i}" : {}}
        for item in kwargs.keys():
            if item == "color":
                index[str(i)][item] = alt_color.get()
            else:
                if len(kwargs[item]) == 2:
                    try:
                        if len(kwargs[item][0]) == 2:
                            kwargs[item][0][0] += steps[item][0]
                            kwargs[item][0][1] += steps[item][1]
                            
                            index[str(i)][item] = kwargs[item][0]
                            
                    except:
                        kwargs[item][0] += steps[item]
                        index[str(i)][item] = kwargs[item][0]
                        
            
        with open("animation.json", "r") as f:
            animation = json.load(f)
            animation[str(i)] = index[str(i)]
             
        with open("animation.json", "w") as f:
            json.dump(animation, f, indent=4)
