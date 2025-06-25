from collections import defaultdict
from dataclasses import dataclass, field
import random
from typing import Any, Dict, Generator, Iterable, List, Callable, Optional, Set, Union, override
from numpy.char import lower
import pygame as pg
from .world import World
from .objects import Object


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
    name: str = "Default"
    priority: bool = False
    data: dict = field(default_factory=dict)

    # tolerate arg-count mismatches
    def __call__(self, **kwargs):
        try:
            self.callback(**kwargs)
        except TypeError:
            self.callback()

    def __eq__(self, other: Object) -> bool:
        return isinstance(other, Event) and self.name == other.name


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
        self._by_name[ev.name] = ev
        self._by_type[ev.type].append(ev)

    def _unregister(self, ev: Event) -> None:
        self._by_name.pop(ev.name, None)
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
        if event.name in self._by_name:
            self.replace(event.name, event)
            return

        # priority events suspend siblings of same type
        if event.priority:
            siblings = self.get_by_type(event.type)
            if siblings:
                self.priority_stash[event.name] = siblings
                for sib in siblings:
                    self._remove_internal(sib)

        self._append_internal(event)

    def __contains__(self, item) -> bool:
        if isinstance(item, Event):
            return item.name in self._by_name
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

    def check():
        # gets widnow events
        events = pg.event.get()

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
        for event in EventHandler.to_add:

            # if is ezsgame event
            if event.type == "ezsgame":

                # MANAGE EZSGAME EVENTS

                # on update event
                if event.event_name == "update":
                    World.on_update.add(event.name, event.callback)

            # if is a event
            else:
                EventHandler.events.add(event)

        EventHandler.to_add.clear()

        # EVENT MANAGEMENT -------------------------------------------------------------------------------------------
        for ev in events:
            # ev : event to process

            # quit event (cannot be event listener)
            if ev.type == pg.QUIT:
                for event in EventHandler.events.get_by_type(pg.QUIT):
                    event.callback()

                World.window.quit()

            # Manages custom events
            for event in EventHandler.events.get_by_type("custom"):
                event_args = {
                    "keys": event.data.get("keys"),
                    "unicode": ev.data.get("unicode"),
                    "type": ev.type,
                    "button": event.data.get("button"),
                    "is_hovering": (
                        EventHandler.is_hovering(event["object"])
                        if "object" in event
                        else False
                    ),
                }

                event(**event_args)

            #  EVENT LOOP (managing events)
            for event in EventHandler.events.get_by_type(ev.type):

                # if is event listener (uses a object)
                is_event_listener = event.object is not None
                is_hovering = False

                if is_event_listener:
                    is_hovering = EventHandler.is_hovering(event.object)

                    # if is not hovering and event is not unhover then skip
                    if not is_hovering and not event.event_name == "unhover":
                        continue

                # function to reduce code, function decides whaterver callback should called or not
                def callback():
                    if is_event_listener:
                        # events that require be hovering
                        if is_hovering and event.object.styles.visible:
                            event.callback()

                    # if is not event listener is base event, just call callback
                    else:
                        event.callback()

                # mouse events
                if ev.type == pg.MOUSEBUTTONDOWN:
                    # mouse wheel up
                    if event.event_name == "mousewheelup" and ev.button == 4:
                        callback()
                        continue

                        # mouse wheel down
                    elif event.event_name == "mousewheeldown" and ev.button == 5:
                        callback()
                        continue

                    # right mouse button
                    elif event.event_name == "rightclick" and ev.button == 3:
                        callback()
                        continue

                    # click, mousedown or leftclick
                    elif (
                        event.event_name in ("click", "mousedown", "leftclick")
                        and ev.button == 1
                    ):
                        callback()
                        continue

                # hover events
                elif ev.type == pg.MOUSEMOTION:
                    if event.event_name == "unhover":
                        if not is_hovering:
                            event.callback()
                            continue

                    else:
                        callback()
                        continue

                # mouse up events
                elif ev.type == pg.MOUSEBUTTONUP:
                    if event.event_name == "mouseup" or event.type == pg.MOUSEBUTTONUP:
                        event.callback()
                        continue

                    else:
                        callback()
                        continue

                # Key pressed events
                elif (ev_keys := event.data.get("keys")):
                    if ev.key in ev_keys:
                        event(key=ev.key, unicode=ev.unicode)
                        continue

                # base on key event keydown or keyup
                # keydown or keyup events
                elif event.type in (pg.KEYDOWN, pg.KEYUP):
                    event(key=ev.key, unicode=ev.unicode)
                    continue

                # any event that matchess current window event
                else:
                    callback()
                    continue

    def add_event(event: str, object: Object, callback, name: str = "Default"):
        """
        #### Adds a event listener to a object
        - `event` : event to be added
                - Events : `click`, `hover`, `unhover`, `unclick`.
        - `name` : name of the event
        - `object` : object to be added to the event
        - `callback` : function to be called when the event is triggered
        """

        event, event_type = EventHandler._convert_to_pgevent(event)

        if name == "Default":
            name = f"{event}.{id(object)}.{len(EventHandler.events)}.{len(EventHandler.to_add)}"

        EventHandler.to_add.append(Event(event_type, event, callback, object, name))

    def remove_event(name: str):
        f"""
        #### Removes an event from the event list so it won't be called anymore
        -  `name` : name of the event to be removed 
        """
        EventHandler.to_remove.add(name)

    def is_hovering(object: Object) -> bool:
        """
        #### Checks if the mouse is hovering over the object
        - `object` : object to check if the mouse is hovering over it
        """
        mouse_pos = pg.mouse.get_pos()
        box = object._get_collision_box()

        if mouse_pos[0] > box[0][0] and mouse_pos[0] < box[1][0]:
            if mouse_pos[1] > box[0][1] and mouse_pos[1] < box[2][1]:
                return True

        return False

    def on_event(event: str, callback, name: str = "Default", priority: bool = False):
        """
        #### Adds a `Base Event` to the event list, Calls function when event is triggered.
        - `event`: event to be added
                - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`, `update`
        -  `callback`: function to be called when the event is triggered ``function``
        - `name`: name of event (optional)
        """

        name = (
            f"base_event.{event}.{len(EventHandler.events)}"
            if name == "Default"
            else name
        )

        # if is ezsgame event
        if event in EventHandler.__ezsgame_events:
            EventHandler.to_add.append(Event("ezsgame", event, callback, None, name, priority=priority))
            return

        event, event_type = EventHandler._convert_to_pgevent(event)

        EventHandler.to_add.append(Event(event_type, event, callback, None, name, priority=priority))

    def on_key(type: str, keys: list, callback, name: str = "Default", priority: bool = False):
        """
        #### Calls function when key event is triggered.
        -  `type`: type of `Event` to be added
                - Events : `down` (when key is down), `up` (when key released)
        - `keys`: keys to be added to the event
        -  `callback`:  function to be called when the event is triggered
        - `name`: name of event (optional)
        """
        types = {"down": pg.KEYDOWN, "up": pg.KEYUP}

        event_type = types.get(type, None)

        if not event_type:
            raise ValueError('Invalid type: \nValid types are: "up", "down"', type)

        name = f"{keys}_{type}_{len(EventHandler.events)}" if name == "Default" else name

        keys = list(map(to_pgkey, keys))

        EventHandler.to_add.append(
            Event(event_type, keys, callback, None, name, data={ "keys": keys}, priority=priority)
        )

    def custom_event(callback, object=None, name: str = "Default", data: dict = {}, priority: bool = False):
        """
        #### Creates a custom event. *[Decorator]*
        - `callback` : function to be called with event parameters
        - `object` : object to check if is hovering, if you need `is_hovering` (Optional)
        - `name`: name of event (optional)
        """

        name = (
            f"custom_event.{name}.{len(EventHandler.events)}"
            if name == "Default"
            else name
        )

        EventHandler.to_add.append(Event("custom", "custom", callback, object, name, data=data, priority=priority))

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
def on_key(type: str, keys: Iterable | str, name: str = "Default") -> Callable:
    """
    #### Calls the function when the key event is triggered
    - `type` : type of the event. `up` or `down`
            - Event types : `up` (when the key is released), `down` (when the key is pressed)
    - `keys` : key/keys to listen to
    - `name` : name of the event (Optional)
    """
    if not hasattr(keys, "__iter__") or isinstance(keys, str):
        keys = [keys]

    def wrapper(func):
        EventHandler.on_key(type, keys, func, name)
        return func

    return wrapper


def on_key_updown(keys: Iterable | str, on_down: Callable, on_up: Callable, name: str = "Default", priority: bool = False) -> None:
    """
    #### Calls the function when the key event is triggered
    - `keys` : key/keys to listen to
    - `on_down` : function to be called when the key is pressed
    - `on_up` : function to be called when the key is released
    - `name` : name of the event (Optional) 
    """
    if not hasattr(keys, "__iter__") or isinstance(keys, str):
        keys = [keys]

    if name == "Default":
        name = f"key_updown.{len(EventHandler.events)}_{random.uniform(1, 10)}"

    EventHandler.on_key("up", keys, on_up, name, priority)
    EventHandler.on_key("down", keys, on_down, name, priority)


def add_event(event: str, object: Object, name: str = "Default", priority: bool = False) -> Callable:
    """
    #### Adds an event listener to an object
    - `event` : event to listen to
    - `object` : object that will be "listening"
    - `name` : name of the event (Optional)
    """

    def wrapper(func):
        EventHandler.add_event(event, object, func, name, priority)
        return func

    return wrapper


def on_event(event: str, name: str = "Default", priority: bool = False) -> Callable:
    """
    #### Calls funcion when the event is triggered, (Base Event)
    - `event` : event to listen to
            - Events : `quit`, `mousemotion`, `mousedown`, `mouseup`, `keydown`, `keyup`, `mousewheel`
    - `name` : name of the event (Optional)
    """

    if name == "Default":
        name = (
            f"base_event.{event}.{len(EventHandler.events)}.{random.uniform(1, 10)}"
            if name == "Default"
            else name
        )

    def wrapper(func):
        EventHandler.on_event(event, func, name, priority)
        return func

    return wrapper


def custom_event(object=None, name: str = "Default", priority: bool = False) -> Callable:
    """
    #### Adds a function as custom event
    - `object` : object to check if is hovering, if you need `is_hovering` (Optional)
    - `name` : name of the event (Optional)
    """

    def wrapper(func):
        EventHandler.custom_event(func, object, name, priority)
        return func

    return wrapper


def remove_event(name: str):
    """
    #### Removes an event from the event handler
    - `name` : name of the event
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
