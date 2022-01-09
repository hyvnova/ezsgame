import pygame as pg

class Animation:
    def __init__(self, screen, object, start, end, time=50, step=1, loop=False, done_callback=None, args=()):
        self.screen = screen
        self.object = object
        self.done = False
        self.done_callback = done_callback
        self.args = args
        self.start = start
        self.loop = loop
        self.end = end
        self.time = time
        self.step = step    
        self.corrected = False
        self.resolve()

        
    def resolve(self):
        obj_pos = self.object.getPos(self.screen)
        if self.start == "current":
            self.start = obj_pos.copy()
        if self.end == "current":
            self.end = obj_pos.copy()      
        if isinstance(self.start, list) or isinstance(self.start, tuple):
            self.object.pos = self.start.copy()
            self.start = self.object.getPos(self.screen)
            
            self.object.pos = self.end.copy()
            self.end = self.object.getPos(self.screen)
        
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
    def __init__(self, screen, object, start="current", end="right", time=50, step=1, loop=False, done_callback=None, args=()):
        super().__init__(screen, object, start, end, time, step, loop, done_callback, args)
        self.name = f"slide_{self.start}_{self.end}"
        self.screen.time.addInterval(name=self.name, time=self.time, callback=self.update)        

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
                    if isinstance(self.args, list) or isinstance(self.args, tuple):
                        self.done_callback(*self.args)
                    else:
                        self.done_callback(self.args)
                return False
            

        

        
    