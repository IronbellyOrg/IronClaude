"""Fixture: class with an Optional[Callable] parameter that is never wired."""

from typing import Callable, Optional


class Processor:
    """Has an injectable hook that nothing provides."""

    def __init__(self, name: str, on_complete: Optional[Callable] = None):
        self.name = name
        self.on_complete = on_complete

    def run(self):
        if self.on_complete:
            self.on_complete()


class WiredProcessor:
    """Has an injectable hook that IS wired by consumer.py."""

    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
