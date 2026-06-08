"""Recommend data models -- RecommendConfig.

Path configuration for the sc-recommend lookup-cache feature. Unlike the
tasklist/roadmap configs, the recommend module is not a claude-subprocess
pipeline (its LLM work is Agent-spawned from skill prose), so this config does
NOT extend ``PipelineConfig`` -- it carries only the cache/telemetry/eval-run
filesystem paths. All fields default so the config constructs without arguments
in tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# Canonical .claude/cache/ artifact locations (tracked YAML + gitignored JSONL).
_CACHE_DIR = Path(".claude/cache")


@dataclass
class RecommendConfig:
    """Filesystem configuration for the sc-recommend lookup-cache.

    Fields:
        lookup_path: tracked lookup-cache YAML (schema_version 2 rows).
        plugin_path: tracked plugin-table YAML (4-phase adoption lifecycle).
        telemetry_path: gitignored high-churn per-invocation events JSONL.
        eval_runs_dir: tracked per-iteration eval-run results directory.
    """

    lookup_path: Path = field(
        default_factory=lambda: _CACHE_DIR / "sc-recommend-lookup.yaml"
    )
    plugin_path: Path = field(
        default_factory=lambda: _CACHE_DIR / "sc-recommend-plugin.yaml"
    )
    telemetry_path: Path = field(
        default_factory=lambda: _CACHE_DIR / "sc-recommend-events.jsonl"
    )
    eval_runs_dir: Path = field(default_factory=lambda: _CACHE_DIR / "eval-runs")
