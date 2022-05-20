class Data:
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
        
    def set(self, **attrs):
        self.__dict__.update(attrs)
    
    def get(self, key):
        return self.__dict__[key]
    
GAME_DATA = Data()

GAME_DATA(difficulty="easy")
GAME_DATA(player={
    "pos": ["center", "center"],
    "size": [50, 50],
    "color": "red"
})

