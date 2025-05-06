from ezsgame.components import Component
from ezsgame.utilities.event_manager import EventManager
from ..event_handler import on_key, remove_event
from ..world import World, get_window
from ezsgame import world


class Controller(Component):
    r"""
    #### Controller
    A controller is a class that can be used to control a component throught keyboard.

    #### Parameters
    - `keys`: A list of keys that can be used to control the component.
    - `speed`: A list of speeds that can be used to control the component.

    ##### length of speed must be equal to length of keys, unless `auto_complete_speed` is `True`
    - `use_delta_time`: If True, the speed will be multiplied by the delta_time.

    - `auto_complete_speed`: If true will "resolve" the speed list in case is not.
        - if speed length is 1 -> `[max]`
            - Example: `[10]` -> `[-10,10,-10,10]` left, right, down, down
        - if speed length is 2 -> `[min, max]`
            - Example: `[-10,10]` -> `[-10,10, -10,-10]` left, right, down, up

    """

    __name__ = "Controller"

    def __init__(
        self,
        keys=["a", "d", "w", "s"],
        speed=[-25, 25, -25, 25],
        use_delta_time=True,
        auto_complete_speed=True,
    ):

        self.window = get_window()
        self.keys = keys
        self.use_delta_time = use_delta_time
        self.event_mananger = EventManager(
            update=f"Controller.update.{id(self)}"
        )

        # auto speed complete
        if auto_complete_speed and len(speed) < len(keys):
            if len(speed) == 1:
                speed = [speed[0] * 1, speed[0]] * len(keys)

            elif len(speed) == 2:
                speed = [speed[0], speed[1]] * len(keys)

        if len(keys) != len(speed):
            raise Exception(
                f"Number of keys and speed must be the same. ({len(keys)}) keys != ({len(speed)}) speeds"
            )

        if use_delta_time:
            self._speeds = list(map(lambda x: x * 10, speed))
        else:
            self._speeds = speed

        self.speed = [0] * len(self._speeds)

        for i in range(len(keys)):
            self._add_events(i)


    def mount(self, object):
        self.object = object
        self.add_update_position_event()


    def _add_events(self, index):
        self.event_mananger.add(f"keydown.{index}", f"Controller.keydown.{id(self)}.{index}")
        self.event_mananger.add(f"keyup.{index}", f"Controller.keyup.{id(self)}.{index}")
            
        @on_key(type="down", keys=[self.keys[index]], name=self.event_mananger[f"keydown.{index}"])
        def keydown():
            if self.use_delta_time:
                self.speed[index] = self._speeds[index] * self.window.get_delta_time()
            else:
                self.speed[index] = self._speeds[index]

        @on_key(type="up", keys=[self.keys[index]], name=self.event_mananger[f"keyup.{index}"])
        def keyup():
            self.speed[index] = 0


    def add_update_position_event(self):
        @World.on_update(self.event_mananger["update"])
        def update_position():
            self.object.pos += self.get_speed("simple")


    def get_speed(self, type="all"):
        r"""
        Returns the speed of the controller.
        `type`: "all", "simple", "average"
        all -> returns a list of all speeds -> [n...]
        simple -> returns sum of all speeds from 0-half as x and sum of all speeds from half to end as y -> [x,y]
        average -> return average of all speeds -> float
        any -> return first speed that is not 0, if all are 0, return 0 -> int
        """

        if type == "average":
            return sum(self.speed) / len(self.speed)

        if type == "simple":
            if len(self.speed) == 4:
                return [
                    sum([self.speed[i] for i in range(len(self.speed) // 2)]),
                    sum(
                        [
                            self.speed[i]
                            for i in range(len(self.speed) // 2, len(self.speed))
                        ]
                    ),
                ]

        if type == "all":
            return self.speed

        if type == "any":
            for i in range(len(self.speed)):
                if self.speed[i] != 0:
                    return self.speed[i]

            return 0

    def stop(self):
        r"""
        Sets all speeds to 0.
        """
        self.speed = [0 for x in range(len(self.speed))]

    def invert(self):
        r"""
        Inverts all speeds.
        """
        self.speed = [-x for x in self.speed]

    def disable(self):
        self.__speeds = self._speeds
        self.stop()
        self._speeds = [0] * len(self._speeds)
        self.event_mananger.disable("update")

    def enable(self):
        try:
            self._speeds = self.__speeds
        except:
            return
        
        self.add_update_position_event()

    def __del__(self):
        del self.event_mananger
        del self
