"""Reflect-wrapper data models -- domain types for ``superclaude reflect run``.

Standalone dataclasses + the 4-state ``Verdict`` enum consumed by the thin
fail-closed wrapper around the POST ``/sc:reflect`` gate. These types are the
shared vocabulary between ``config.py`` (input resolution), ``contract.py``
(verdict derivation), and ``runner.py`` (orchestration).

Isolation guardrails (NFR-1 thinness, Risk Section 10):
- No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``.
- Zero ``async def`` / ``await`` anywhere in the package.
- This module imports nothing from ``commands.py`` / ``runner.py`` /
  ``config.py`` / ``contract.py`` -- it is types only.

The exit-code mapping is the load-bearing fail-closed contract (spec Section 6):
``pass`` -> 0 (the ONLY exit-0 path), ``halted`` -> 10, ``degraded`` -> 11,
``blocked`` -> 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Verdict(str, Enum):
    """The 4-state fail-closed verdict derived from ``return-contract.yaml``.

    Ordering is decided by ``contract.derive_verdict`` (first-match-wins:
    blocked -> degraded -> halted -> pass). Only ``PASS`` exits zero.
    """

    PASS = "pass"
    HALTED = "halted"
    DEGRADED = "degraded"
    BLOCKED = "blocked"

    @property
    def exit_code(self) -> int:
        """Process exit code for this verdict (spec Section 6 table).

        pass -> 0, halted -> 10, degraded -> 11, blocked -> 2.
        """
        return {
            Verdict.PASS: 0,
            Verdict.HALTED: 10,
            Verdict.DEGRADED: 11,
            Verdict.BLOCKED: 2,
        }[self]

    @property
    def is_promotable(self) -> bool:
        """True only for a clean, full, non-degraded Tier-2 pass."""
        return self is Verdict.PASS


@dataclass
class ReflectConfig:
    """Resolved launch inputs for one ``superclaude reflect run`` invocation.

    Produced by ``config.resolve_config`` from CLI args + tasklist frontmatter
    + git state. Consumed by ``runner.ReflectRunner`` to build the
    ``/sc:reflect`` prompt and construct ``ClaudeProcess``.
    """

    tasklist_path: Path
    base: str
    head: str
    spec_path: Path | None
    depth: str
    executor_model: str | None
    output_dir: Path
    model: str
    timeout_seconds: int
    max_turns: int
    promote: bool
    allow_single_vendor: bool
    tmux: bool
    dry_run: bool
    print_command: bool
    resume: bool

    @property
    def contract_path(self) -> Path:
        """Pinned location of the contract the wrapper parses (FR-4/FR-5)."""
        return self.output_dir / "return-contract.yaml"


@dataclass
class ReflectResult:
    """Derived verdict + write-back outcome for one wrapper run.

    Built by ``contract.derive_verdict`` (verdict + reason + contract reads)
    and finalized by ``runner`` (``write_status`` after the frontmatter
    write-back). The command keys its process exit off ``verdict.exit_code``.
    """

    verdict: Verdict
    status: str | None
    tier_reached: int | None
    reason: str
    report_path: str | None
    contract_path: str | None
    deviations: dict[str, int] = field(default_factory=dict)
    child_exit_code: int | None = None
    write_status: str = ""

    @property
    def outcome(self) -> str:
        """``"success"`` only for a passing verdict; else ``"failed"``."""
        return "success" if self.verdict is Verdict.PASS else "failed"
