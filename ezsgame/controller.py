from ezsgame.premade import get_id

class Controller:
    def __init__(self, screen, keys=["a","d","w","s"], speed=[-5,5,5,-5]):
        if len(keys) != len(speed):
            raise Exception(f"Number of keys and speed must be the same. ({len(keys)}) keys != ({len(speed)}) speeds")  
        
        self._id = get_id()
        self.screen = screen
        self.keys = keys
        self._speeds = speed
        self.speed = [0 for x in range(len(speed))]

        for i in range(len(keys)):
            self._add_events(i)
        
    def _add_events(self, index):
        @self.screen.on_key(type="down", keys=[self.keys[index]])
        def keydown():
            self.speed[index] = self._speeds[index]

        @self.screen.on_key(type="up", keys=[self.keys[index]])
        def keyup():
            self.speed[index] = 0
        
    def get_speed(self, type="all"):
        r'''
        Returns the speed of the controller.
        @param type: "all", "simple", "average"
        @type all: returns a list of all speeds -> [n...]
        @type simple: returns sum of all speeds from 0-half as x and sum of all speeds from half to end as y -> [x,y]
        @type average: return average of all speeds -> float
        @type any: return first speed that is not 0, if all are 0, return 0 -> int
        '''
        
        if type == "average":
            return sum(self.speed)/len(self.speed)

        if type == "simple":
            if len(self.speed) == 4:
                return [sum([self.speed[i] for i in range(len(self.speed)//2)]),
                        sum([self.speed[i] for i in range(len(self.speed)//2, len(self.speed))])
                       ]
            
            
        if type == "all":
            return self.speed
        
        if type == "any":
            for i in range(len(self.speed)):
                if self.speed[i] != 0:
                    return self.speed[i]
            
            return 0
        
    def stop(self):
        r'''
        Sets all speeds to 0.
        '''
        self.speed = [0 for x in range(len(self.speed))]

    def invert(self):
        r'''
        Inverts all speeds.
        '''
        self.speed = [-x for x in self.speed]