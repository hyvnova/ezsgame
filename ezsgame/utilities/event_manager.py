"""
This module defines an Event Manager.

An Event Manager is a class that is responsible for handling events, meaning,
    It keeps tracks of event allowing for easy toggling of events and deletion.
"""

from ast import Dict
from ..event_handler import Event, EventHandler, remove_event


class EventManager:
    """
    Event Manager class
    Handles events, allowing for easy toggling and deletion of events.
    When indexed with an alias, it returns the event name.
    When deleted, it removes all events.
    """

    def __init__(self, **events):
        # Dict of event_alias: event_name
        # Alias are meant to refer to event easily with local context
        # Name are the actual event names, which need to be unique
        self.events: Dict[str, str] = events
        self.disabled: Dict[str, Event] = {}

    def add(self, alias: str, name: str):
        self.events[alias] = name

    def remove(self, alias: str):
        """
        Removes the event with the given alias, from both EventManager and EventHandler. 
        """
        remove_event(self.events[alias])
        del self.events[alias]


    def disable(self, alias: str):
        """
        Disables the event with the given alias.
        This removes the event from EventHandler and stores it in the disabled dict.
        """
        self.disabled[alias] = EventHandler.events.get_by_name(self.events[alias])
        remove_event(self.events[alias])

    def enable(self, alias: str):
        """
        Enables the event with the given alias.
        This adds the event back to EventHandler and removes it from the disabled dict.
        """
        if alias not in self.disabled: return
        EventHandler.to_add.append(self.disabled[alias])
        del self.disabled[alias]


    def toggle(self, alias: str):
        """
        Toggles the event with the given alias.
        """
        if alias in self.disabled:
            self.enable(alias)
        else:
            self.disable(alias)

    def __getitem__(self, alias: str):
        return self.events[alias]

    def __del__(self):
        for event in self.events.values():
            remove_event(event)