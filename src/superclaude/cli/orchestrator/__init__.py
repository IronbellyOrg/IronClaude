"""Orchestrator module -- ``superclaude orchestrator``, the verbs of /sc:orchestrator."""


def __getattr__(name: str):
    if name == "orchestrator_group":
        from .group import orchestrator_group

        return orchestrator_group
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["orchestrator_group"]
