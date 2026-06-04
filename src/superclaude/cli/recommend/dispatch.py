"""Option-P hot-path dispatch core (deterministic).

Under the resolved boundary decision (Option P — Python-heavy / thin Haiku), the
`cli/recommend/` module owns the deterministic half of the hot-path control flow:
table scan, key-match, the top-2-confidence-delta ambiguity gate, per-row
source_hash validation (Read + sha256 compare — NEVER a Haiku-computed hash), and
the budget gate. The Claude session (SKILL.md) owns the parts only it can do:
spawning the Haiku classifier Agent (the anthropic SDK is banned, so the CLI
cannot spawn Agents) and, on a miss, spawning the cold-path Agent.

This module is a PURE function: given the classifier output + the cache, it
returns a ``DispatchResult``. It does NOT write telemetry (the caller logs exactly
one event per invocation, since only the caller knows whether the cold path
subsequently ran). It does NOT spawn Agents. It does NOT write the cache.

Control flow (research/04 §2.2, hot path steps 3-9):
  1. native_likely -> short-circuit to native (no table, no cold path).
  2. key unknown/empty -> miss_no_key.
  3. confidence_top2_delta < 0.10 -> miss_low_confidence.
  4. table scan; no row for key -> miss_no_key.
  5. row.native_fallback true -> native (rows flagged native skip the scan).
  6. source_hash validation: Read row.source_path, sha256, compare -> on
     mismatch/absent, miss_validation_stale.
  7. budget gate: cumulative hot-path tokens > limit -> miss_budget_exceeded.
  8. else HIT: emit the row's prompt_envelope_template + best_model hint.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .cache import LookupCache, compute_source_hash, compute_surface_hash

# The four hot-path miss reasons the dispatch can emit. All are members of the
# telemetry closed enum (telemetry.CACHE_RESULTS); the caller logs whichever is
# the final outcome (or "cold_inserted" if the cold path then inserts a row).
LOW_CONFIDENCE_DELTA = 0.10
DEFAULT_BUDGET_LIMIT = 10_000


@dataclass
class DispatchResult:
    """Outcome of the deterministic hot-path dispatch."""

    outcome: str  # "hit" | "native" | "miss"
    # cache_result is a telemetry enum value for hit/miss; None for native
    # (native is not a cache-table event and has no enum member).
    cache_result: str | None = None
    miss_reason: str | None = None  # populated on outcome == "miss"
    recommendation: str | None = None  # filled prompt_envelope_template on hit
    best_model_hint: dict | None = None
    candidate: str | None = None
    needs_cold_path: bool = False  # True for every miss; False for hit/native

    def to_dict(self) -> dict:
        return {
            "outcome": self.outcome,
            "cache_result": self.cache_result,
            "miss_reason": self.miss_reason,
            "recommendation": self.recommendation,
            "best_model_hint": self.best_model_hint,
            "candidate": self.candidate,
            "needs_cold_path": self.needs_cold_path,
        }


def _miss(reason: str) -> DispatchResult:
    return DispatchResult(
        outcome="miss", cache_result=reason, miss_reason=reason, needs_cold_path=True
    )


def dispatch(
    *,
    classification_key: str | None,
    native_likely: bool,
    confidence_top2_delta: float,
    cache_path: Path,
    surface_base: Path = Path("src/superclaude"),
    budget_tokens_used: int = 0,
    budget_limit: int = DEFAULT_BUDGET_LIMIT,
) -> DispatchResult:
    """Run the deterministic hot-path dispatch and return a ``DispatchResult``.

    Pure: no Agent spawn, no telemetry write, no cache write. The caller (the
    skill, via the ``recommend dispatch`` subcommand) interprets the result —
    emitting the recommendation on a hit, recommending native on native, or
    spawning the cold-path Agent on a miss.
    """
    # 1. native short-circuit (classifier judged the task better done natively).
    if native_likely:
        return DispatchResult(outcome="native", cache_result=None)

    # 2. unknown / empty key -> no cacheable row.
    if not classification_key or classification_key in ("unknown", "native"):
        return _miss("miss_no_key")

    # 3. ambiguous classification (top-2 too close) -> treat as a miss.
    if confidence_top2_delta < LOW_CONFIDENCE_DELTA:
        return _miss("miss_low_confidence")

    # 4. table scan.
    surface_hash = compute_surface_hash(surface_base)
    cache = LookupCache.load_or_create(cache_path, surface_hash)
    row = cache.get_row(classification_key)
    if row is None:
        return _miss("miss_no_key")

    # 5. native_fallback rows are skipped (never recommended via the table).
    if row.get("native_fallback"):
        return DispatchResult(
            outcome="native", cache_result=None, candidate=row.get("candidate")
        )

    # 6. source_hash validation (deterministic Read + sha256 compare).
    source_path = row.get("source_path")
    if not source_path:
        return _miss("miss_validation_stale")
    src = Path(source_path)
    if not src.exists():
        return _miss("miss_validation_stale")
    if compute_source_hash(src.read_bytes()) != row.get("source_hash"):
        return _miss("miss_validation_stale")

    # 7. budget gate.
    if budget_tokens_used > budget_limit:
        return _miss("miss_budget_exceeded")

    # 8. HIT — emit the row's hand-off envelope + best_model hint.
    return DispatchResult(
        outcome="hit",
        cache_result="hit",
        recommendation=row.get("prompt_envelope_template"),
        best_model_hint=row.get("best_model"),
        candidate=row.get("candidate"),
    )
