"""Core app that imports used_handler but not orphan_handler."""

from handlers.used_handler import handle_request


def main():
    return handle_request()
