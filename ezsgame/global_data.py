from uuid import uuid4

def get_id() -> str:
    id = int(uuid4())
    return str(id)
    
class Data:
    def __init__(self):
        self.drawn_objects = []
        self.on_update = {}

        
        
    def __call__(self, **attrs):
        self.__dict__.update(attrs)
        
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        
    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        
            
DATA = Data()

#shortcuts to DATA
get_screen = lambda: DATA.screen
get_drawn_objects = lambda: DATA.drawn_objects 

def on_update(key=None,val=None):
    r"""
    #### Sets a function into `DATA.on_update` or returns all funcions if no key is passed
    """
    
    if key:
        DATA.on_update[key] = val
    else:
        return DATA.on_update.values()