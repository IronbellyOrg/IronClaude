"""Sweep module -- ``superclaude sweep`` read-only coordinator CLI command."""


def __getattr__(name: str):
    if name == "sweep_group":
        from .commands import sweep_group

        return sweep_group
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["sweep_group"]
