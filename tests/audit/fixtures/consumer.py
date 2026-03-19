"""Fixture: consumer that wires WiredProcessor's callback."""

from .unwired_callable import WiredProcessor


def main():
    p = WiredProcessor(callback=lambda: print("wired"))
    return p
