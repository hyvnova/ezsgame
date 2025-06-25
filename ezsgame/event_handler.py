from collections import defaultdict
from dataclasses import dataclass, field
import random
from typing import Any, Dict, Generator, Iterable, List, Callable, Optional, Set, Union, override
import pygame as pg
from .world import World
from .objects import Object
from .funcs import is_hovering
from pygame.event import Event as PygameEvent


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


# ─────────────────────── Event ─────────────────────── #
@dataclass(slots=True)
class Event:
    type: str
    event_name: str
    callback: Callable
    object: Optional[Any] = None
    eid: str = "Default"
    priority: bool = False
    data: dict = field(default_factory=dict)

    # tolerate arg-count mismatches
    def __call__(self, **kwargs):
        try:
            self.callback(**kwargs)
        except TypeError:
            self.callback()

    def __eq__(self, other: Object) -> bool:
        return isinstance(other, Event) and self.eid == other.eid


# ──────────────────── EventList ────────────────────── #
class EventList(list):
    """
    Public contract = Python list.
    Internals = list + hash tables for O(1) look-ups.
    """

    def __init__(self, *events: Event):
        super().__init__(events)

        # Fast reverse indexes
        self._by_name: Dict[str, Event] = {}
        self._by_type: Dict[str, List[Event]] = defaultdict(list)
        for ev in self:
            self._register(ev)

        # name -> stashed siblings owned by a priority event
        self.priority_stash: Dict[str, List[Event]] = {}

    # ── internal plumbing ───────────────────────────── #
    def _register(self, ev: Event) -> None:
        self._by_name[ev.eid] = ev
        self._by_type[ev.type].append(ev)

    def _unregister(self, ev: Event) -> None:
        self._by_name.pop(ev.eid, None)
        try:
            self._by_type[ev.type].remove(ev)
            if not self._by_type[ev.type]:
                del self._by_type[ev.type]
        except (KeyError, ValueError):
            pass

    def _append_internal(self, ev: Event) -> None:
        super().append(ev)
        self._register(ev)

    def _remove_internal(self, ev: Event) -> None:
        try:
            super().remove(ev)
        except ValueError:
            pass
        self._unregister(ev)

    # ── public API (unchanged signatures) ───────────── #
    def get_by_type(self, event_type) -> List[Event]:
        # generator → concrete list for easier external reuse
        return list(self._by_type.get(event_type, []))

    def get_by_name(self, event_name) -> Optional[Event]:
        return self._by_name.get(event_name)

    def replace(self, name: str, new_event: Event) -> None:
        old = self._by_name.get(name)
        if not old:
            self.add(new_event)
            return

        idx = self.index(old)  # keep insertion order
        self[idx] = new_event
        self._unregister(old)
        self._register(new_event)

    def remove(self, *names) -> None:
        for name in names:
            ev = self._by_name.get(name)
            if not ev:
                continue

            # restore siblings if this was a priority holder
            if name in self.priority_stash:
                siblings = self.priority_stash.pop(name)
                for sib in siblings:
                    self._append_internal(sib)

            self._remove_internal(ev)

    def add(self, event: Event) -> None:
        # replace duplicates
        if event.eid in self._by_name:
            self.replace(event.eid, event)
            return

        # priority events suspend siblings of same type
        if event.priority:
            siblings = self.get_by_type(event.type)
            if siblings:
                self.priority_stash[event.eid] = siblings
                for sib in siblings:
                    self._remove_internal(sib)

        self._append_internal(event)

    def __contains__(self, item) -> bool:
        if isinstance(item, Event):
            return item.eid in self._by_name
        return item in self._by_name  # allow `'jump' in events`


class EventHandler:
    """
    - Manages events on the program
    """

    events = EventList()
    to_remove: Set[str] = set()
    to_add: List[Event] = []
    pressed_keys: pg.key.ScancodeWrapper = None

    __ezsgame_events = ("update",)

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
        EventHandler.events[:] = [
            ev for ev in EventHandler.events if ev.name not in doomed
        ]

        # 3️⃣  Unregister from the on_update signal
        for name in doomed:
            if name in World.on_update.listeners:   # keys, not values
                World.on_update.remove(name)

        # 4️⃣  Reset the queue
        EventHandler.to_remove.clear()

        # -------------------- adds events --------------------
        for user_event in EventHandler.to_add:

            # if is ezsgame event
            if user_event.type == "ezsgame":

                # MANAGE EZSGAME EVENTS

                # on update event
                if user_event.event_name == "update":
                    World.on_update.add(user_event.eid, user_event.callback)

            # if is a event
            else:
                EventHandler.events.add(user_event)

        EventHandler.to_add.clear()

        # EVENT MANAGEMENT -------------------------------------------------------------------------------------------
        for app_event in app_incoming_events:
            # app_event : event to process 

            # event_list[app_eventhash] -> [Callbacks]
            

            # quit event (cannot be event listener)
            if app_event.type == pg.QUIT:
                for user_event in EventHandler.events.get_by_type(pg.QUIT):
                    user_event.callback()

                World.window.quit()

            # Manages custom events
            for user_event in EventHandler.events.get_by_type("custom"):
                event_args = {
                    "keys": user_event.data.get("keys"),
                    "unicode": app_event.data.get("unicode"),
                    "type": app_event.type,
                    "button": user_event.data.get("button"),
                    "is_hovering": (
                        is_hovering(user_event["object"])
                        if "object" in user_event
                        else False
                    ),
                }

                user_event(**event_args)

            #  EVENT LOOP (managing events)
            for user_event in EventHandler.events.get_by_type(app_event.type):

                # if is event listener (uses a object)
                is_event_listener = user_event.object is not None
                is_hovering = False

                if is_event_listener:
                    is_hovering = EventHandler.is_hovering(user_event.object)

                    # if is not hovering and event is not unhover then skip
                    if not is_hovering and not user_event.event_name == "unhover":
                        continue

                # function to reduce code, function decides whaterver callback should called or not
                def callback():
                    if is_event_listener:
                        # events that require be hovering
                        if is_hovering and user_event.object.styles.visible:
                            user_event.callback()

                    # if is not event listener is base event, just call callback
                    else:
                        user_event.callback()

                # mouse events
                if app_event.type == pg.MOUSEBUTTONDOWN:
                    # mouse wheel up
                    if user_event.event_name == "mousewheelup" and app_event.button == 4:
                        callback()
                        continue

                        # mouse wheel down
                    elif user_event.event_name == "mousewheeldown" and app_event.button == 5:
                        callback()
                        continue

                    # right mouse button
                    elif user_event.event_name == "rightclick" and app_event.button == 3:
                        callback()
                        continue

                    # click, mousedown or leftclick
                    elif (
                        user_event.event_name in ("click", "mousedown", "leftclick")
                        and app_event.button == 1
                    ):
                        callback()
                        continue

                # hover events
                elif app_event.type == pg.MOUSEMOTION:
                    if user_event.event_name == "unhover":
                        if not is_hovering:
                            user_event.callback()
                            continue

                    else:
                        callback()
                        continue

                # mouse up events
                elif app_event.type == pg.MOUSEBUTTONUP:
                    if user_event.event_name == "mouseup" or user_event.type == pg.MOUSEBUTTONUP:
                        user_event.callback()
                        continue

                    else:
                        callback()
                        continue

                # Key pressed events
                elif (ev_keys := user_event.data.get("keys")):
                    if app_event.key in ev_keys:
                        user_event(key=app_event.key, unicode=app_event.unicode)
                        continue

                # base on key event keydown or keyup
                # keydown or keyup events
                elif user_event.type in (pg.KEYDOWN, pg.KEYUP):
                    user_event(key=app_event.key, unicode=app_event.unicode)
                    continue

                # any event that matchess current window event
                else:
                    callback()
                    continue

    @staticmethod
    def add_event(event: str, object: Object, callback, eid: str = "Default", priority: bool = False):
        """
        #### Adds a event listener to a object
        - `event` : event to be added
                - Events : `click`, `hover`, `unhover`, `unclick`.
        - `eid` : event id. used to identify the event and remove it later
        - `object` : object to be added to the event
        - `callback` : function to be called when the event is triggered
        """

        event, event_type = EventHandler._convert_to_pgevent(event)

        if eid == "Default":
            eid = f"{event}.{id(object)}.{len(EventHandler.events)}.{len(EventHandler.to_add)}"

        EventHandler.to_add.append(Event(event_type, event, callback, object, eid, priority=priority))

    @staticmethod
    def remove_event(name: str):
        f"""
        #### Removes an event from the event list so it won't be called anymore
        -  `name` : name of the event to be removed 
        """
        EventHandler.to_remove.add(name)


    @staticmethod
    def on_event(event: str, callback, eid: str = "Default", priority: bool = False):
        """
        #### Adds a `Base Event` to the event list, Calls function when event is triggered.
        - `event`: event to be added
                - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`, `update`
        -  `callback`: function to be called when the event is triggered ``function``
        - `eid`: event id. used to identify the event and remove it later
        """

        eid = (
            f"base_event.{event}.{len(EventHandler.events)}"
            if eid == "Default"
            else eid
        )

        # if is ezsgame event
        if event in EventHandler.__ezsgame_events:
            EventHandler.to_add.append(Event("ezsgame", event, callback, None, eid, priority=priority))
            return

        event, event_type = EventHandler._convert_to_pgevent(event)

        EventHandler.to_add.append(Event(event_type, event, callback, None, eid, priority=priority))

    @staticmethod
    def on_key(type: str, keys: list, callback, eid: str = "Default", priority: bool = False):
        """
        #### Calls function when key event is triggered.
        -  `type`: type of `Event` to be added
                - Events : `down` (when key is down), `up` (when key released)
        - `keys`: keys to be added to the event
        -  `callback`:  function to be called when the event is triggered
        - `eid`: event id. used to identify the event and remove it later
        """
        types = {"down": pg.KEYDOWN, "up": pg.KEYUP}

        event_type = types.get(type, None)

        if not event_type:
            raise ValueError('Invalid type: \nValid types are: "up", "down"', type)

        eid = f"{keys}_{type}_{len(EventHandler.events)}" if eid == "Default" else eid

        keys = list(map(to_pgkey, keys))

        EventHandler.to_add.append(
            Event(event_type, keys, callback, None, eid, data={ "keys": keys}, priority=priority)
        )

    @staticmethod
    def custom_event(callback, object=None, eid: str = "Default", data: dict = {}, priority: bool = False):
        """
        #### Creates a custom event. *[Decorator]*
        - `callback` : function to be called with event parameters
        - `object` : object to check if is hovering, if you need `is_hovering` (Optional)
        - `eid`: event id. used to identify the event and remove it later
        """

        eid = (
            f"custom_event.{eid}.{len(EventHandler.events)}"
            if eid == "Default"
            else eid
        )

        EventHandler.to_add.append(Event("custom", "custom", callback, object, eid, data=data, priority=priority))


    @staticmethod
    def _convert_to_pgevent(event):
        if event in EventHandler.__ezsgame_events:
            return event

        event = event.lower().replace(" ", "").replace("_", "")

        evs = {
            "hover": pg.MOUSEMOTION,
            "click": pg.MOUSEBUTTONDOWN,
            "rightclick": pg.MOUSEBUTTONDOWN,
            "leftclick": pg.MOUSEBUTTONDOWN,
            "mousedown": pg.MOUSEBUTTONDOWN,
            "mouseup": pg.MOUSEBUTTONUP,
            "unhover": pg.MOUSEMOTION,
            "unclick": pg.MOUSEBUTTONUP,
            "keydown": pg.KEYDOWN,
            "keyup": pg.KEYUP,
            "mousewheelmotion": pg.MOUSEWHEEL,
            "mousemotion": pg.MOUSEMOTION,
            "quit": pg.QUIT,
            "mousebuttondown": pg.MOUSEBUTTONDOWN,
            "mousebuttonup": pg.MOUSEBUTTONDOWN,
            "mousewheelup": pg.MOUSEBUTTONDOWN,
            "mousewheeldown": pg.MOUSEBUTTONDOWN,
        }

        if event not in evs:
            raise Exception("Event type not found", event)

        return (event, evs[event])


# event decorators ------------------------------------------------------------
def on_key(type: str, keys: Iterable | str, eid: str = "Default") -> Callable:
    """
    #### Calls the function when the key event is triggered
    - `type` : type of the event. `up` or `down`
            - Event types : `up` (when the key is released), `down` (when the key is pressed)
    - `keys` : key/keys to listen to
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """
    if not hasattr(keys, "__iter__") or isinstance(keys, str):
        keys = [keys]

    def wrapper(func):
        EventHandler.on_key(type, keys, func, eid)
        return func

    return wrapper


def on_key_updown(keys: Iterable | str, on_down: Callable, on_up: Callable, eid: str = "Default", priority: bool = False) -> None:
    """
    #### Calls the function when the key event is triggered
    - `keys` : key/keys to listen to
    - `on_down` : function to be called when the key is pressed
    - `on_up` : function to be called when the key is released
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """
    if not hasattr(keys, "__iter__") or isinstance(keys, str):
        keys = [keys]

    if eid == "Default":
        eid = f"key_updown.{len(EventHandler.events)}_{random.uniform(1, 10)}"

    EventHandler.on_key("up", keys, on_up, eid, priority)
    EventHandler.on_key("down", keys, on_down, eid, priority)


def add_event(event: str, object: Object, eid: str = "Default", priority: bool = False) -> Callable:
    """
    #### Adds an event listener to an object
    - `event` : event to listen to
    - `object` : object that will be "listening"
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """

    def wrapper(func):
        EventHandler.add_event(event, object, func, eid, priority)
        return func

    return wrapper


def on_event(event: str, eid: str = "Default", priority: bool = False) -> Callable:
    """
    #### Calls funcion when the event is triggered, (Base Event)
    - `event` : event to listen to
            - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """

    if eid == "Default":
        eid = (
            f"base_event.{event}.{len(EventHandler.events)}.{random.uniform(1, 10)}"
            if eid == "Default"
            else eid
        )

    def wrapper(func):
        EventHandler.on_event(event, func, eid, priority)
        return func

    return wrapper


def custom_event(object=None, eid: str = "Default", priority: bool = False) -> Callable:
    """
    #### Adds a function as custom event
    - `object` : object to check if is hovering, if you need `is_hovering` (Optional)
    - `eid` : event id. used to identify the event and remove it later (Optional)
    """

    def wrapper(func):
        EventHandler.custom_event(func, object, eid, priority)
        return func

    return wrapper


def remove_event(eid: str):
    """
    #### Removes an event from the event handler
    - `eid` : event id. used to identify the event
    """
    EventHandler.remove_event(name)


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
