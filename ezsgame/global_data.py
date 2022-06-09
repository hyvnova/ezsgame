from uuid import uuid4

__USED_IDS = set()
def get_id() -> int:
    global __USED_IDS
    id = int(uuid4())
    while id in __USED_IDS:
        id = int(uuid4())
        
    __USED_IDS.add(id)
    return id
    
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
        
    def set(self, key, value):
        self.__dict__[key] = value
    
    def get(self, key):
        return self.__dict__[key]
            
DATA = Data()

#shortcuts to DATA
get_screen = lambda: DATA.screen
get_drawn_objects = lambda: DATA.drawn_objects 