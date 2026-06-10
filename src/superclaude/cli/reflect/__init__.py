"""Reflect wrapper -- ``superclaude reflect run`` thin fail-closed POST gate.

Launches ``/sc:reflect --mode post`` as a top-level ``claude --print``
subprocess (escaping the Agent-tool nesting limit so Tier 2 fans out), parses
``return-contract.yaml``, derives a 4-state verdict {pass, halted, degraded,
blocked}, writes a ``reflect_post:`` block back into the tasklist frontmatter
atomically + race-safely, and exits on a fail-closed exit-code contract.

Modules:
- ``models``: dataclasses + the ``Verdict`` enum (types only).
- ``config``: ``resolve_config`` (FR-3 derivation + FR-4 output STOP).
- ``contract``: isolated verdict map (Section 6) + FR-11 routing + version gating.
- ``runner``: thin orchestrator (Phase 3).
- ``commands``: Click ``reflect_group`` surface (Phase 4).
"""

from .commands import reflect_group
from .config import resolve_config
from .contract import derive_verdict, parse_contract
from .models import ReflectConfig, ReflectResult, Verdict

__all__ = [
    "reflect_group",
    "Verdict",
    "ReflectConfig",
    "ReflectResult",
    "resolve_config",
    "derive_verdict",
    "parse_contract",
]
