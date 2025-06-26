from collections import defaultdict
from dataclasses import dataclass, field
from operator import call
import random
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    Callable,
    Optional,
    Set,
    Tuple,
    Union,
    override,
)
from flask import app
import pygame as pg
from .world import World, get_window
from .objects import Object
from .funcs import is_hovering
from pygame.event import Event as PygameEvent


# Event that can "attach" to objects
# Will be called upon certain condition being met regarding the object
OBJECT_EVENTS = (
    "click",
    "unclick",
    "hover",
    "unhover",
)

EVENT_TYPE_MAP = {
    # Key events
    "keydown": pg.KEYDOWN,
    "keyup": pg.KEYUP,
    "quit": pg.QUIT,

    "mousemotion": pg.MOUSEMOTION,
    "unhover": pg.MOUSEMOTION,
    "hover": pg.MOUSEMOTION,

    # Mouse down
    "click": pg.MOUSEBUTTONDOWN,
    "leftclick": pg.MOUSEBUTTONDOWN,
    "mousedown": pg.MOUSEBUTTONDOWN,
    "rightclick": pg.MOUSEBUTTONDOWN * 3,

    # Mouse up
    "mouseup": pg.MOUSEBUTTONUP,
    "unclick": pg.MOUSEBUTTONUP,

    # Mouse wheel 
    "mousewheelmotion": pg.MOUSEWHEEL,
    "mousewheel": pg.MOUSEWHEEL,
    "mousewheelup": pg.MOUSEBUTTONDOWN * 4, 
    "mousewheeldown": pg.MOUSEBUTTONDOWN * 5,
}


def to_pgkey(key: str) -> int:
    """
    #### Converts a key to a pygame key
    Example : `a` -> `pg.K_a`
    """
    if key.lower() == "enter":
        key = "RETURN"

    if key.lower() == "esc" or key.lower().startswith("esc"):
        key = "ESCAPE"

    elif len(key) > 1:
        key = key.upper()

    return eval("pg.K_" + key)


def __add_hover_condition(object, neg: bool = False) -> Callable:
    """
    [Decorator]
    Adds a condition to the event callback that checks if the object is hovered
    - `object` : object to check if is hovered
    - `neg` : if True, the condition will be inverted (if not hovering)

    Used to modify the callback of events such that,
    event listener will only be called if the object is hovered or not hovered
    This also applies to click and unclick events, since event_type it's stored in the Event,
    and will abide by the same logic.
    """

    # gets function wrapper
    def wrapper(func):
        # actual function wrapper - applies the condition
        def inner(*args, **kwargs):
            if is_hovering(object) != neg:
                return func(*args, **kwargs)
            return None

        return inner

    return wrapper


def __get_event_type(event: str) -> str:
    if event in EventHandler.__ezsgame_events:
        return event

    event = event.lower().replace(" ", "").replace("_", "")

    if event not in EVENT_TYPE_MAP:
        raise Exception("Event type not found", event)

    return str(EVENT_TYPE_MAP[event])


# ─────────────────────── Event ─────────────────────── #

type EventRegisIdentity = Dict[str, Tuple[Dict[str, Any], Callable]]


class EventRegist:
    """
    Represents a registered event in the event handler.
    Used to handle the creating, storing and calling of events.
    Notice that this is not a Pygame event, but rather a custom event object
    that can used to register callbacks for specific events.
    - `event_type`: type of the event, must be one of the keys in `EVENT_TYPE_MAP`
    - `callback`: function to be called when the event is triggered
    - `object`: optional object to check if is hovering, if you need you need to know whether the event click, hover, etc.
    - `eid`: event id. used to identify the event and remove it later. If no `eid` it will be under `_` name
    """

    def __init__(
        self,
        event_type: str,
        callback: Callable,
        object: Optional[Any] = None,
        eid: str = "_",
        priority: bool = False,
        data: dict = field(default_factory=dict),
    ):
        """
        Event constructor
        - `event_type`: type of the event, must be one of the keys in `EVENT_TYPE_MAP`
        """
        self.type = event_type
        self.data = data
        self.callback = callback
        self.eid = eid
        self.priority = priority

        """
        In case of object, that means the event is a listener for that object.
        And therfore, the callback will need to satisfy some conditions before being called.
        """
        if object is not None:
            if not event_type in OBJECT_EVENTS:
                raise ValueError(
                    "Event type must be one of 'click', 'unclick', 'hover', 'unhover' when object is provided"
                )

            if event_type in ("click", "hover"):
                self.callback = __add_hover_condition(object)(self.callback)
            elif event_type in ("unclick", "unhover"):
                self.callback = __add_hover_condition(object, neg=True)(self.callback)
            else:
                raise ValueError(
                    f"Event type {event_type} is not supported for object events. Must be one of {OBJECT_EVENTS}"
                )

    def __hash__(self) -> int:
        return hash(__get_event_type(self.type))

    # tolerate arg-count mismatches
    def callback(self, **kwargs):
        try:
            self.callback(**kwargs)
        except TypeError:
            self.callback()

    def __eq__(self, other: Object) -> bool:
        return isinstance(other, EventRegist) and self.eid == other.eid

    def identity(self) -> EventRegisIdentity:
        """
        Identity it's the actual data being logged into the EventList
        """
        return {self.eid: (self.data, self.callback)}


# ──────────────────── EventList ────────────────────── #
class EventList:
    """
    Public contract = Python list.
    Internals = list + hash tables for O(1) look-ups.
    """

    def __init__(self, *events: EventRegist):
        """
        Events it's a map of type: EventRegisIdentity
        where each key is a pygame event type as a string, and the value is a dictionary
        In said dictionary, the keys are event names (eid) and the values are tuples
        containing the data and the callback function.
        {
            pygame_event_type_str: {
                "event_name": (data, callback),
                ...
            }
        }
        """
        self.events: Dict[str, EventRegisIdentity] = {}
        self.name_to_type: Dict[str, str] = {}  # name -> event type

        # name -> stashed siblings owned by a priority event
        self.priority_stash: Dict[str, EventRegisIdentity] = {}

    # ── public API ───────────── #
    def remove(self, *names):
        """
        Removes events by their names.
        - `names`: event names to remove
        """
        to_remove = set()
        to_add = set()
        for name, pg_type in self.name_to_type.items():
            if name in names:
                # remove from the events map
                if pg_type in self.events:
                    del self.events[pg_type][name]

                # remove from the name to type map
                to_remove.add(name)

                # If name in priority stash, restore the stashed events and remove the name
                if name in self.priority_stash:
                    for name, details in self.priority_stash[name].items():
                        self.events[pg_type][name] = details
                        to_add.add(name)
                
                    # remove from the priority stash
                    del self.priority_stash[name]

        for name in to_remove:
            del self.name_to_type[name]

        for name in to_add:
            self.name_to_type[name] = pg_type

    def add(self, event: EventRegist):
        """
        Adds an event to the event list.
        - `event`: EventRegist object to add
        """
        pg_type = __get_event_type(event.type)

        # If the event is a priority event, stash its siblings
        if event.priority:
            if event.eid not in self.priority_stash:
                self.priority_stash[event.eid] = {}

            self.priority_stash[event.eid].update(self[pg_type])

            # Clear the current events of this type
            self.events[pg_type] = {}
            # Clear the name to type map for this type
            for name in self.name_to_type.keys():
                if self.name_to_type[name] == pg_type:
                    del self.name_to_type[name]

        # Add the event to the events map
        if pg_type not in self.events:
            self.events[pg_type] = {}

        self.events[pg_type].update(event.identity())
        self.name_to_type[event.eid] = pg_type

    def __getitem__(self, pg_type: str) -> EventRegisIdentity:
        """
        Returns the events under the given type
        - `item`: pygame event type as a string.
        """
        if isinstance(pg_type, str):
            return self.events.get(pg_type, {})
        else:
            raise TypeError(f"Expected str, got {type(pg_type)}")


class EventHandler:
    """
    - Manages events on the program
    """

    events = EventList()
    to_remove: Set[str] = set()
    to_add: List[EventRegist] = []
    pressed_keys: pg.key.ScancodeWrapper = None # type: ignore

    __ezsgame_events = ("update",)


    @staticmethod
    def __process_event(app_event: PygameEvent, data: dict, callback: Callable):
        """
        Processes an event from the app, and calls the callback with the data.
        - `app_event`: event to process
        - `data`: data to pass to the callback
        - `callback`: function to call with the data
        """

        # If key event, we need to check if the key is pressed
        if app_event.type in (pg.KEYDOWN, pg.KEYUP):
            keys = data.get("keys", [])

            if app_event.key not in keys and not keys:
                # if key is not in the keys, we don't process the event
                return
            
            callback(key=app_event.key, unicode=app_event.unicode)
            return
        
        else:
            # should be good to go
            callback()


    @staticmethod
    def check():
        # gets widnow events
        app_incoming_events: List[PygameEvent] = pg.event.get()

        # log pressed keys
        EventHandler.pressed_keys = pg.key.get_pressed()

        # -------------------- removes events --------------------
        # 1️⃣  Snapshot → set for O(1) look-ups
        doomed = EventHandler.to_remove

        # 2️⃣  Nuke matching events in one pass, no in-place mutation hazards
        EventHandler.events.remove(*doomed)

        # 3️⃣  Unregister from the on_update signal
        for name in doomed:
            if name in World.on_update.listeners:  # keys, not values
                World.on_update.remove(name)

        # 4️⃣  Reset the queue
        EventHandler.to_remove.clear()

        # -------------------- adds events --------------------
        for user_event in EventHandler.to_add:
            if user_event.type == "update":
                World.on_update.add(user_event.eid, user_event.callback)

            else:
                EventHandler.events.add(user_event)

        EventHandler.to_add.clear()

        # EVENT MANAGEMENT -------------------------------------------------------------------------------------------
        for app_event in app_incoming_events:
            # app_event = event to process
            app_event_type = str(app_event.type)

            # Event that must be processed, since they match the event type
            user_events = EventHandler.events[app_event_type]

            print(f"{len(user_events)} events of type {app_event_type}: {user_events.keys()}")

            # quit event (cannot be event listener)
            if app_event.type == pg.QUIT:
                map(lambda item: item[1](), user_events.values())
                get_window().quit()

            #  EVENT LOOP (managing events)
            for data, callback in user_events.values():
                EventHandler.__process_event(
                    app_event, data, callback
                )

    @staticmethod
    def add_event(
        event_type: str,
        object: Object,
        callback,
        eid: str = "_",
        priority: bool = False,
    ):
        """
        #### Adds a event listener to a object
        - `event` : event to be added
                - Events : `click`, `hover`, `unhover`, `unclick`.
        - `eid` : event id. used to identify the event and remove it later
        - `object` : object to be added to the event
        - `callback` : function to be called when the event is triggered
        """

        if event_type not in OBJECT_EVENTS:
            raise ValueError(
                f"Event must be one of type: {OBJECT_EVENTS}, got {event_type}"
            )

        EventHandler.to_add.append(
            EventRegist(event_type, callback, object, eid, priority=priority)
        )

    @staticmethod
    def remove_event(name: str):
        f"""
        #### Removes an event from the event list so it won't be called anymore
        -  `name` : name of the event to be removed 
        """
        EventHandler.to_remove.add(name)

    @staticmethod
    def on_event(event_type: str, callback, eid: str = "_", priority: bool = False):
        """
        #### Adds a `Base Event` to the event list, Calls function when event is triggered.
        - `event`: event to be added
                - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`, `update`
        -  `callback`: function to be called when the event is triggered ``function``
        - `eid`: event id. used to identify the event and remove it later
        """

        EventHandler.to_add.append(
            EventRegist(event_type, callback, None, eid, priority=priority)
        )

    @staticmethod
    def on_key(
        event_type: str,
        keys: Iterable[str],
        callback,
        eid: str = "_",
        priority: bool = False,
    ):
        """
        #### Calls function when key event is triggered.
        -  `type`: type of `Event` to be added
                - Events : `down` (when key is down), `up` (when key released)
        - `keys`: keys to be added to the event
        -  `callback`:  function to be called when the event is triggered
        - `eid`: event id. used to identify the event and remove it later
        """

        if not event_type:
            raise ValueError('Invalid type: \nValid types are: "up", "down"', type)

        pg_keys = list(map(to_pgkey, keys))

        EventHandler.to_add.append(
            EventRegist(
                event_type,
                callback,
                None,
                eid,
                data={"keys": pg_keys},
                priority=priority,
            )
        )

    @staticmethod
    def custom_event(
        callback,
        object=None,
        eid: str = "_",
        data: dict = {},
        priority: bool = False,
    ):
        """
        #### Creates a custom event. *[Decorator]*
        - `callback` : function to be called with event parameters
        - `object` : object to check if is hovering, if you need `is_hovering` (Optional)
        - `eid`: event id. used to identify the event and remove it later
        """

        EventHandler.to_add.append(
            EventRegist("custom", callback, object, eid, data=data, priority=priority)
        )


# ------------------------ Event Handler Decorators ------------------------ #
def on_key(type: str, keys: Iterable[str] | str, eid: str = "_") -> Callable: # type: ignore
    """
    #### Calls the function when the key event is triggered
    - `type` : type of the event. `up` or `down`
            - Event types : `up` (when the key is released), `down` (when the key is pressed)
    - `keys` : key/keys to listen to
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """
    if not hasattr(keys, "__iter__") or isinstance(keys, str):
        keys: list[str] = [keys]  # type: ignore

    def wrapper(func):
        EventHandler.on_key(type, keys, func, eid)
        return func

    return wrapper


def on_key_updown(
    keys: Iterable | str,
    on_down: Callable,
    on_up: Callable,
    eid: str = "_",
    priority: bool = False,
) -> None:
    """
    #### Calls the function when the key event is triggered
    - `keys` : key/keys to listen to
    - `on_down` : function to be called when the key is pressed
    - `on_up` : function to be called when the key is released
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """
    if not hasattr(keys, "__iter__") or isinstance(keys, str):
        keys = [keys]

    EventHandler.on_key("up", keys, on_up, eid, priority)
    EventHandler.on_key("down", keys, on_down, eid, priority)


def add_event(
    event: str, object: Object, eid: str = "_", priority: bool = False
) -> Callable:
    """
    #### Adds an event listener to an object
    - `event` : event to listen to, MUST be one of the `OBJECT_EVENTS`
    - `object` : object that will be "listening"
    - `eid` : event id. used to identify the event and remove it later (Optional)
    - `priority` : if True, the event will be called before other events of the same type
    """

    def wrapper(func):
        EventHandler.add_event(event, object, func, eid, priority)
        return func

    return wrapper


def on_event(event: str, eid: str = "_", priority: bool = False) -> Callable:
    """
    #### Calls funcion when the event is triggered, (Base Event)
    - `event` : event to listen to
            - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """

    def wrapper(func):
        EventHandler.on_event(event, func, eid, priority)
        return func

    return wrapper


def remove_event(eid: str):
    """
    #### Removes an event from the event handler
    - `eid` : event id. used to identify the event
    """
    EventHandler.remove_event(eid)


def is_down(key: str) -> bool:
    """
    #### Returns if the key being is pressed
    - `key` : key to check
    """
    return pg.key.get_pressed()[to_pgkey(key)]


def went_down(key: str) -> bool:
    """
    #### Returns `True` if the key was pressed during this frame
    """
    return EventHandler.pressed_keys[to_pgkey(key)]
