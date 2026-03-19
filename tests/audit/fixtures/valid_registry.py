"""Fixture: dispatch registry where all entries are valid."""


def handler_a():
    return "a"


def handler_b():
    return "b"


STEP_REGISTRY = {
    "a": handler_a,
    "b": handler_b,
    "null": None,  # Explicit null handler — allowed
}
