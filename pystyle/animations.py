class Animation:
    def __init__(self, screen, object, start,end, loop, done_callback=None, args=()):
        self.screen = screen
        self.object = object
        self.done = False
        self.done_callback = done_callback
        self.args = args
        self.start = start
        self.surface = self.screen.screen
        self.loop = loop
        self.end = end
        
    def resolve(self):
        object = self.object
        
        obj_pos = self.object.getPos(self.screen)
        self.object.pos = self.start
        self.start = self.object.resolveStyle(self.screen)
        
        self.object.pos = self.end
        self.end = self.object.resolveStyle(self.screen)
    
        self.object.pos = obj_pos

        
class Slide(Animation):
    f'''
    - slide object from start to end
    @param start: start position
    @param end: end position
    @param time: time in Miliseconds
    @param step: step size
    [If objet is not at start position, it will be moved to start position]
    '''
    def __init__(self, screen, object, start="current", end="right", time=1, step=1, loop=False, done_callback=None, args=()):
        super().__init__(screen, object, start, end, loop, done_callback, args)
        self.time = time
        self.step = step
        self.screen = screen
        self.corrected = False
        self.resolve()
        self.screen.time.addInterval(name=f"slide_{start}_{end}", time=self.time, callback=self.update)
        

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
                self.screen.time.remove(f"slide_{self.start}_{self.end}")
                if self.done_callback != None:
                    if isinstance(self.args, list) or isinstance(self.args, tuple):
                        self.done_callback(*self.args)
                    else:
                        self.done_callback(self.args)


        

        
    