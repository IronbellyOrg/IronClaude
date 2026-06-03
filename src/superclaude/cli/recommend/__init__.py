"""Recommend module -- ``superclaude recommend`` CLI command.

Provides the deterministic-helper surface backing the ``sc-recommend``
lookup-cache feature: the YAML lookup-cache reader/writer (atomic write,
surface_hash reset), the telemetry JSONL appender, the ``best_model`` tier
selection, and the per-row / plugin ``--eval`` pipeline. The hot/cold-path
dispatch orchestration lives in skill prose (see ``sc-recommend/SKILL.md``);
this module owns the file/eval operations the skill shells out to.
"""


def __getattr__(name: str):
    if name == "recommend_group":
        from .commands import recommend_group

        return recommend_group
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["recommend_group"]
