from typing import Any, Tuple, Union
from ..funcs import center_at

from ..objects.object import Object
from ..types import Pos

class Group:
    r"""
    #### Group
    
	#### Parameters
    - `parent` : parent of the group, objects position in the group will be relative to this object `Object`
        - if parent is a string, it will be searched in the group items
        
    - [*args] `objects` : objects to add in the group `Object, ..`
    - [**kwargs] `named_objects` : named objects to add in the group `name = Object, ..`

    #### Notes
    - named objects can be accessed by: `group["name"]`
    - no named objects can be accessed by: `group[id(object)]`

    """
    
    def __init__(self, *objects, **named_objects):
        self.__objects = {}
        
        parent = named_objects.get("parent", None)
        if parent:
            del named_objects["parent"]
        
        self.add(*objects, **named_objects)
        
        if parent:
            if isinstance(parent, str):
                parent = self.__objects[parent]
                
        else:
            parent = None

        self.__parent = parent
        self.__last_parent_pos = Pos(0,0)
        
    def add(self, *objects, **named_objects):
        for obj in objects:
            self.__objects[id(obj)] = obj
        
        self.__objects.update(named_objects)

    def add_as(self, key: Union[int, float, bool, str, Tuple], object: Object):
        """
        Adds a object to the group with a custom key.
        Make sure the key is a valid dictionary key.        
        """
        self.__objects[key] = object

    def get(self, name: Union[int, float, bool, str, Tuple], default: Any = None) -> Object | None:
        """
        Gets a object from the group by it's name if it exists, otherwise `default` will be returned.
        """
        return self.__objects.get(name, default)
    
    def remove(self, name: str):
        self.__objects.pop(name)

    def align_objects(self, auto_size = True):
        # aligns objects in the group
        if self.__parent.pos != self.__last_parent_pos:
                
            margin = self.__parent.size[1]*0.1
                
            current_y = self.__parent.pos[1] + margin
            
            for obj in self.__objects.values():
                if obj != self.__parent:
                
                    center_at(obj, self.__parent)
                    obj.pos[1] = current_y
                
                    current_y += obj.size[1] + margin
                    
                    if auto_size:
                        # if overflow, resize parent
                        
                        # x axis
                        if obj.pos[0] + obj.size[0] > self.__parent.pos[0] + self.__parent.size[0]:
                            self.__parent.size[0] = obj.pos[0] + obj.size[0] + margin * 1.5
                            center_at(obj, self.__parent)
                            
                        # y axis
                        if obj.pos[1] + obj.size[1] > self.__parent.pos[1] + self.__parent.size[1]:
                            self.__parent.size[1] = obj.pos[1] + obj.size[1] + margin * 1.5

            self.__last_parent_pos = self.__parent.pos

    def draw(self):
        # align objects to paren    
        if self.__parent:
            self.align_objects()
        
        for obj in self.values():
            obj.draw()

    def map(self, func):
        for obj in self.values():
            func(obj)

    def __str__(self):
        t = ", ".join([str(i) for i in self.objects])
        return f"<Group : {t} >"

    def __repr__(self):
        return self.__str__()

    def filter(self, func) -> 'Group':
        d = {k: v for k, v in self.items() if func(v)}
        return d


    # getters        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__objects[list(self.__objects.keys())[key]]
        return self.__objects[key]

    def __getattr__(self, name):
        return self.__objects.get(name, None) or self.__dict__[name]
    
    def values(self, no_parent=False):
        if no_parent and self.__parent:
            return [v for k, v in self.__objects.items() if v != self.__parent]
        
        return self.__objects.values()
    
    def items(self, no_parent=False):
        if no_parent and self.__parent:
            return {k: v for k, v in self.__objects.items() if v != self.__parent}
        
        return self.__objects.items()

    def keys(self, no_parent=False):
        if no_parent and self.__parent:
            return [k for k, v in self.__objects.items() if v != self.__parent]
    
        return self.__objects.keys()
    

    def __del__(self):
        for obj in self.__objects.values():
            del obj
        

    # delete item
    def __delitem__(self, key):
        self.__objects.pop(key)
        self.__dict__.pop(key)
        
    def __delattr__(self, key):
        self.__objects.pop(key)
        self.__dict__.pop(key)
    
    # contains
    def __contains__(self, key):
        return key in self.__objects
    
    # iterables
    def __iter__(self):
        return iter(self.values())
    
    def __next__(self):
        return next(self.values())

    def __len__(self):
        return len(self.__objects)