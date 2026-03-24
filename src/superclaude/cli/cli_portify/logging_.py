"""Execution log emission for CLI Portify (NFR-007).

Emits:
- execution-log.jsonl  — machine-readable NDJSON log
- execution-log.md     — human-readable Markdown summary

Event schema: {timestamp (ISO-8601), event_type, step_id, data: dict}

Supported event types (8 total):
  step_start            — step begins execution
  step_end              — step completes (pass or fail)
  gate_eval             — gate evaluation initiated
  gate_fail             — gate evaluation failed
  convergence_transition — convergence state change
  signal_received       — OS signal received (SIGINT, SIGTERM)
  budget_warning        — turn budget drops below 10%
  pipeline_outcome      — final pipeline outcome
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Event type constants
# ---------------------------------------------------------------------------

EV_STEP_START: str = "step_start"
EV_STEP_END: str = "step_end"
EV_GATE_EVAL: str = "gate_eval"
EV_GATE_FAIL: str = "gate_fail"
EV_CONVERGENCE_TRANSITION: str = "convergence_transition"
EV_SIGNAL_RECEIVED: str = "signal_received"
EV_BUDGET_WARNING: str = "budget_warning"
EV_PIPELINE_OUTCOME: str = "pipeline_outcome"

ALL_EVENT_TYPES: tuple[str, ...] = (
    EV_STEP_START,
    EV_STEP_END,
    EV_GATE_EVAL,
    EV_GATE_FAIL,
    EV_CONVERGENCE_TRANSITION,
    EV_SIGNAL_RECEIVED,
    EV_BUDGET_WARNING,
    EV_PIPELINE_OUTCOME,
)


def _iso_now() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="milliseconds"
    )


class ExecutionLog:
    """Writes execution-log.jsonl and execution-log.md to workdir.

    Event schema per NFR-007:
      {"timestamp": "<ISO-8601>", "event_type": "<type>", "step_id": "<id>", ...data}
    """

    def __init__(self, workdir: Path) -> None:
        self.workdir = workdir
        self._entries: list[dict[str, Any]] = []

    def record(self, event_type: str, step_id: str = "", **kwargs) -> None:
        """Record a log entry with ISO-8601 timestamp.

        Args:
            event_type: One of the 8 supported event types.
            step_id: Pipeline step identifier (empty for pipeline-level events).
            **kwargs: Additional event-specific data fields.
        """
        entry: dict[str, Any] = {
            "timestamp": _iso_now(),
            "event_type": event_type,
            "step_id": step_id,
        }
        entry.update(kwargs)
        self._entries.append(entry)

    # ------------------------------------------------------------------
    # Convenience event recorders
    # ------------------------------------------------------------------

    def step_start(self, step_id: str, **kwargs) -> None:
        """Record a step_start event."""
        self.record(EV_STEP_START, step_id=step_id, **kwargs)

    def step_end(
        self, step_id: str, status: str, duration_s: float = 0.0, **kwargs
    ) -> None:
        """Record a step_end event."""
        self.record(
            EV_STEP_END, step_id=step_id, status=status, duration_s=duration_s, **kwargs
        )

    def gate_eval(self, step_id: str, gate_id: str, tier: str = "", **kwargs) -> None:
        """Record a gate_eval event."""
        self.record(EV_GATE_EVAL, step_id=step_id, gate_id=gate_id, tier=tier, **kwargs)

    def gate_fail(self, step_id: str, gate_id: str, reason: str = "", **kwargs) -> None:
        """Record a gate_fail event."""
        self.record(
            EV_GATE_FAIL, step_id=step_id, gate_id=gate_id, reason=reason, **kwargs
        )

    def convergence_transition(
        self, step_id: str, from_state: str, to_state: str, iteration: int = 0, **kwargs
    ) -> None:
        """Record a convergence_transition event."""
        self.record(
            EV_CONVERGENCE_TRANSITION,
            step_id=step_id,
            from_state=from_state,
            to_state=to_state,
            iteration=iteration,
            **kwargs,
        )

    def signal_received(self, signal_name: str, step_id: str = "", **kwargs) -> None:
        """Record a signal_received event."""
        self.record(
            EV_SIGNAL_RECEIVED, step_id=step_id, signal_name=signal_name, **kwargs
        )

    def budget_warning(
        self, remaining: int, total: int, step_id: str = "", **kwargs
    ) -> None:
        """Record a budget_warning event (when remaining < 10% of total)."""
        self.record(
            EV_BUDGET_WARNING,
            step_id=step_id,
            remaining_turns=remaining,
            total_turns=total,
            pct_remaining=round(100.0 * remaining / total, 1) if total > 0 else 0.0,
            **kwargs,
        )

    def failure_handler(
        self, step_id: str, handler_name: str = "", classification: str = "", **kwargs
    ) -> None:
        """Record that a failure handler was dispatched for a step."""
        self.record(
            "failure_handler",
            step_id=step_id,
            handler_name=handler_name,
            classification=classification,
            **kwargs,
        )

    def pipeline_outcome(self, outcome: str, step_id: str = "", **kwargs) -> None:
        """Record the final pipeline_outcome event."""
        self.record(EV_PIPELINE_OUTCOME, step_id=step_id, outcome=outcome, **kwargs)

    # ------------------------------------------------------------------
    # Flush to disk
    # ------------------------------------------------------------------

    def flush(self, phase: str = "", status: str = "", elapsed: float = 0.0) -> None:
        """Write both log files to workdir.

        Args:
            phase: Optional phase label for the Markdown summary row.
            status: Optional status label for the Markdown summary row.
            elapsed: Elapsed time in seconds for the Markdown summary row.
        """
        self.workdir.mkdir(parents=True, exist_ok=True)

        # NDJSON — append all queued entries
        jsonl_path = self.workdir / "execution-log.jsonl"
        with open(jsonl_path, "a", encoding="utf-8") as fh:
            for entry in self._entries:
                fh.write(json.dumps(entry) + "\n")

        # Markdown summary — initialise header on first write, then append rows
        md_path = self.workdir / "execution-log.md"
        if not md_path.exists():
            with open(md_path, "w", encoding="utf-8") as fh:
                fh.write("# CLI Portify Execution Log\n\n")
                fh.write("| Phase | Status | Elapsed | Events |\n")
                fh.write("|-------|--------|---------|--------|\n")

        with open(md_path, "a", encoding="utf-8") as fh:
            fh.write(
                f"| {phase} | {status} | {elapsed:.3f}s | {len(self._entries)} |\n"
            )

        self._entries.clear()

    def get_all_entries(self) -> list[dict[str, Any]]:
        """Return a copy of all queued (unflushed) entries."""
        return list(self._entries)
