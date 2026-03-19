"""Fixture: dispatch registry with broken and valid entries."""


def valid_handler():
    return "ok"


# This registry has one valid and one broken entry
STEP_REGISTRY = {
    "valid": valid_handler,
    "broken": nonexistent_handler,  # noqa: F821 — intentionally unresolvable
}

# This registry is valid
TASK_DISPATCH = {
    "process": valid_handler,
}
