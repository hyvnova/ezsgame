from typing import Callable, List
import time
import pygame as pg

class Interval:
    __slots__ = "time", "callback", "name", "last_call"
    
    def __init__(self, time: float, callback: Callable, last_call: float, name: str = "Default"):
        self.time = time
        self.callback = callback
        self.name = name
        self.last_call = last_call

class TimeHandler:
    r'''
    - Handles the time events
    '''

    intervals: List[Interval] = []
    to_remove: List[str] = []
    to_add: List[Interval] = []

    def add(call_time: int, callback, name: str = "Default"):
        r'''
        #### Adds a `interval` that will be called every `time` milliseconds
        - `name` : name of the event 
        - `time` : amount of time in milliseconds that the event will be called after
        - `callback` : function to be called when the event is triggered 
        '''

        name = f"{len(TimeHandler.intervals)}.{call_time}" if name == "Default" else name

        TimeHandler.to_add.append(Interval(call_time, callback, 0, name)) 

    def remove(name: str):
        r'''
        #### Removes an `interval` from the event list so it won't be called anymore
        - `name` : name of the event to be removed 
        '''
        TimeHandler.to_remove.append(name)

    def check():
        r'''
        #### Manages the time events
        '''
        # removing intervals
        for name in TimeHandler.to_remove:

            if name in TimeHandler.intervals:
                del TimeHandler.intervals[name]

        TimeHandler.to_remove.clear()

        # adding intervals
        TimeHandler.intervals.extend(TimeHandler.to_add)
       
        TimeHandler.to_add.clear()

        # Checking  Intervals
        
        current_time = pg.time.get_ticks()
        for interval in TimeHandler.intervals:
            
            if current_time - interval.last_call >= interval.time:
                interval.callback()
                interval.last_call = pg.time.get_ticks()

# time decorators  ------------------------------------------------------------
def add_interval(call_time: int, name: str = "Default") -> Callable:
    r'''    
    - Adds an `interval` to the time handler, calls the function every `time` milliseconds
    - `time` : time in milliseconds
    - `name` : name of the interval (Optional)
    '''
    def wrapper(func):
        TimeHandler.add(call_time, func, name)
        return func

    return wrapper

def remove_interval(name: str) -> None:
    r'''
    #### Removes an `interval` from the time handler
    - `name` : name of the interval
    '''
    TimeHandler.remove(name)


