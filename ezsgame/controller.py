

class Controller:
    def __init__(self, screen, keys=["a","d","w","s"], speed=[-5,5,5,-5]):
        if len(keys) != len(speed):
            raise Exception(f"Number of keys and speed must be the same. ({len(keys)}) keys != ({len(speed)}) speeds")

        self.screen = screen
        self.keys = keys
        self._speeds = speed
        self.speed = [0 for x in range(len(speed))]

        for i in range(len(keys)):
            self.screen.events.on_key("down", [keys[i]], lambda: self.move(i, self._speeds[i]))
            self.screen.events.on_key("up", [keys[i]], lambda: self.move(i, 0))

    def move(self, index, val):
        self.speed[index] = val