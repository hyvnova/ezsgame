class DATA:
    on_update = {}
    window = object
    EventHandler = object
    TimeHandler = object

#shortcuts to DATA
def get_window():
    """
    #### Returns the window object
    """
    return DATA.window

def on_update(key=None,val=None):
    r"""
    #### Sets a function into `DATA.on_update` or returns all funcions if no key is passed
    """
    
    if key:
        DATA.on_update[key] = val
    else:
        return DATA.on_update.values()