from typing import Callable, List
import pygame as pg


class Interval:
    __slots__ = "time", "callback", "name", "last_call", "repeat"

    def __init__(
        self, time: float, callback: Callable, last_call: float, name, repeat: int
    ):
        self.time = time
        self.callback = callback
        self.name = name
        self.last_call = last_call
        self.repeat = repeat


class TimeHandler:
    r"""
    - Handles the time events
    """

    intervals: List[Interval] = []
    to_remove: List[str] = []
    to_add: List[Interval] = []

    def add(call_time: float, callback, name: str = "Default", repeat: int = -1):
        r"""
        #### Adds a `interval` that will be called every `time` seconds
        - `name` : name of the event
        - `time` : amount of time in seconds that the event will be called after
        - `callback` : function to be called when the event is triggered
        - `repeat` : number of times the interval will last (-1 for infinite)
        """
        call_time *= 1000  # sec → ms
        now = pg.time.get_ticks()
        name = f"{len(TimeHandler.intervals)}.{call_time}" if name == "Default" else name
        if repeat <= 0 and repeat != -1:
            raise ValueError("repeat must be -1 or > 0")
        # start counting *now* so first fire is after `call_time`
        TimeHandler.to_add.append(Interval(call_time, callback, now, name, repeat))

    def remove(name: str):
        r"""
        #### Removes an `interval` from the event list so it won't be called anymore
        - `name` : name of the event to be removed
        """
        TimeHandler.to_remove.append(name)

    def check():
        r"""
        #### Manages the time events
        """
        # removing intervals
        for target_name in TimeHandler.to_remove:
            for index, interval in enumerate(TimeHandler.intervals):
                if interval.name == target_name:
                    del TimeHandler.intervals[index]
                    break

        TimeHandler.to_remove.clear()

        # adding intervals
        TimeHandler.intervals.extend(TimeHandler.to_add)
        TimeHandler.to_add.clear()

        # Checking  Intervals
        current_time = pg.time.get_ticks()
        for interval in TimeHandler.intervals:
            # fire as many times as period has elapsed
            while current_time - interval.last_call >= interval.time:
                interval.callback()
                interval.last_call += interval.time  # keep absolute schedule
                if interval.repeat > 0:
                    interval.repeat -= 1
                    if interval.repeat == 0:
                        TimeHandler.to_remove.append(interval.name)
                        break

# time decorators  ------------------------------------------------------------
def add_interval(time: int, name: str = "Default", repeat: int = -1) -> Callable:
    r"""
    - Adds an `interval` to the time handler, calls the function every `time`
    - `time` : amount of time in seconds that the event will be called after
    - `name` : name of the interval (Optional)
    """

    def wrapper(func):
        TimeHandler.add(time, func, name, repeat)
        return func

    return wrapper


def remove_interval(name: str) -> None:
    r"""
    #### Removes an `interval` from the time handler
    - `name` : name of the interval
    """
    TimeHandler.remove(name)
