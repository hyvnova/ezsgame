from functools import lru_cache
from turtle import st
from typing import Set
from .types import Pos, Size, Signal


class World:
    """
    #### Defines the "world"
    The `pos` and `size` defined the "view" of the world, objects outside of the view won't be drawn.
    """


    # will be set on window post init
    window = object
    pos = Pos(0, 0)
    size = Size(0, 0)  
    
    EventHandler = object
    TimeHandler = object

    objects: Set = set()
    objects_to_add: Set = set() # avoids iteration errors (adding objects during iteration)
    objects_to_remove: Set = set() # avoids iteration errors (removing objects during iteration)

    on_update: Signal = Signal()
    
    @classmethod
    def is_inside(cls, obj) -> bool:
        """
        #### Returns `True` if `obj` is inside the world
        """
        return (
            cls.pos[0] <= obj.pos[0] <= cls.pos[0] + cls.size[0]
            and cls.pos[1] <= obj.pos[1] <= cls.pos[1] + cls.size[1]
        )

    @classmethod
    def add(cls, obj):
        """
        #### Adds an object to the world
        - If the obj has `on_world_add` method, it will be called instead of adding it to the world
        - If the obj has children and they're not added, they will be added too
        """
        if hasattr(obj, "on_world_add"):
            obj.on_world_add()
        else:
            cls.objects_to_add.add(obj)
            
            if hasattr(obj, "children"):
                for child in obj.children:
                    cls.objects_to_add.add(child)

    @classmethod
    def remove(cls, obj):
        """
        #### Removes an object from the world
        - If the obj has `on_world_remove` method, it will be called instead of removing it from the world
        - If the obj has childrem and they're not added, they will be added too
        """
        if hasattr(obj, "on_world_remove"):
            obj.on_world_remove()
        else:
            cls.objects_to_remove.add(obj)
            
            if hasattr(obj, "children"):
                for child in obj.children:
                    cls.objects_to_remove.add(child)
        

    @classmethod
    def update(cls):
        """
        Adds and removes pending objects

        This method is called automatically by the window update method
        """

        if len(cls.objects_to_add) > 0:
            cls.objects.update(cls.objects_to_add)
            cls.objects_to_add.clear()

        if len(cls.objects_to_remove) > 0:
            cls.objects.difference_update(cls.objects_to_remove)
            cls.objects_to_remove.clear()

        # sort objects by z-index
        cls.objects = set(sorted(cls.objects, key=lambda obj: obj.styles.z_index if hasattr(obj, "styles") else 0))

    @staticmethod
    def search(**attrval) -> Set:
        """
        Searches for objects in the world that match the given attributes and values.
        Ex. search(tag={"name": "player"}) -> {player} if player has tag "name" with value "player" of course
        """
        results = set()
        for obj in cls.objects:
            if all(getattr(obj, key, None) == value for key, value in attrval.items()):
                results.add(obj)
        return results
    
    @staticmethod
    def search_single(**attrval):
        """
        Searches for a single object in the world that matches the given attributes and values.
        If none exists an error will be raised.
        Use this method when you expect only one object to match the criteria.
        Ex. search_single(tag={"name": "player"}) -> player if player has tag "name" with value "player"
        """
        for obj in World.objects:
            if all(getattr(obj, key, None) == value for key, value in attrval.items()):
                return obj

        raise ValueError("No object found for criteria: " + str(attrval))

# Utility for getting the window object easily
@lru_cache()
def get_window():
    """
    #### Returns the window object
    """
    return World.window
