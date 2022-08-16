from turtle import Screen
from uuid import uuid4


def get_id() -> str:
    id = int(uuid4())
    return str(id)
    
class DATA:
    on_update = {}

    Screen = None
    EventHandler = None
    TimeHandler = None

#shortcuts to DATA
get_screen = lambda: DATA.screen

def on_update(key=None,val=None):
    r"""
    #### Sets a function into `DATA.on_update` or returns all funcions if no key is passed
    """
    
    if key:
        DATA.on_update[key] = val
    else:
        return DATA.on_update.values()