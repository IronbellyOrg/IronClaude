"""JSONL audit record writer for TurnLedger validation (FR-7.1).

Writes one JSON line per audit record to a JSONL file. Each record contains
exactly 10 fields conforming to the FR-7.1 schema:

Schema Fields
-------------
test_id : str
    Unique test identifier, e.g. "FR-1.5-phase-delegation-task-inventory".
spec_ref : str
    Traceability reference to source code or spec, e.g. "executor.py:1183-1191".
timestamp : str
    ISO-8601 UTC timestamp of when the record was emitted.
assertion_type : str
    Classification of the assertion: "behavioral", "structural", or "value".
inputs : dict
    Test inputs/configuration used for the assertion.
observed : dict
    Concrete runtime values observed during the test.
expected : dict
    Expected values the test asserts against.
verdict : str
    One of "PASS", "FAIL", or "SKIP".
evidence : str
    Human-readable description of what was checked and why the verdict holds.
duration_ms : float
    Wall-clock duration in milliseconds, auto-computed from start_timer()/record().

Usage
-----
    writer = AuditWriter(Path("results/audit-trail.jsonl"))
    writer.start_timer()
    # ... run test logic ...
    writer.record(
        test_id="FR-1.5-test",
        spec_ref="executor.py:100-110",
        assertion_type="behavioral",
        inputs={"config": {"max_turns": 10}},
        observed={"result": "ok"},
        expected={"result": "ok"},
        verdict="PASS",
        evidence="Result matched expected value",
    )
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REQUIRED_FIELDS = frozenset({
    "test_id",
    "spec_ref",
    "timestamp",
    "assertion_type",
    "inputs",
    "observed",
    "expected",
    "verdict",
    "evidence",
    "duration_ms",
})

_VALID_VERDICTS = frozenset({"PASS", "FAIL", "SKIP"})

_VALID_ASSERTION_TYPES = frozenset({"behavioral", "structural", "value"})


class AuditWriter:
    """Appends JSONL audit records to a file.

    Each call to ``record()`` validates the 10-field schema, computes
    ``timestamp`` and ``duration_ms`` automatically, and writes exactly
    one JSON line to the output file.

    Parameters
    ----------
    output_path : Path | str
        File path for JSONL output. Parent directories are created if needed.
    """

    def __init__(self, output_path: Path | str) -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._timer_start: float | None = None

    def start_timer(self) -> None:
        """Mark the start of a timed test region.

        Call this before the test logic runs. ``record()`` will compute
        ``duration_ms`` as the elapsed time since this call.
        """
        self._timer_start = time.monotonic()

    def record(
        self,
        *,
        test_id: str,
        spec_ref: str,
        assertion_type: str,
        inputs: dict[str, Any],
        observed: dict[str, Any],
        expected: dict[str, Any],
        verdict: str,
        evidence: str,
    ) -> dict[str, Any]:
        """Write one JSONL audit record.

        ``timestamp`` and ``duration_ms`` are auto-computed and must NOT
        be passed as arguments.

        Parameters
        ----------
        test_id : str
            Unique test identifier.
        spec_ref : str
            Code/spec traceability reference.
        assertion_type : str
            One of "behavioral", "structural", "value".
        inputs : dict
            Test configuration/inputs.
        observed : dict
            Runtime observations.
        expected : dict
            Expected values.
        verdict : str
            One of "PASS", "FAIL", "SKIP".
        evidence : str
            Human-readable justification.

        Returns
        -------
        dict
            The complete 10-field record that was written.

        Raises
        ------
        ValueError
            If ``verdict`` or ``assertion_type`` is invalid, or if
            ``start_timer()`` was not called.
        """
        if verdict not in _VALID_VERDICTS:
            raise ValueError(
                f"verdict must be one of {sorted(_VALID_VERDICTS)}, got {verdict!r}"
            )

        if assertion_type not in _VALID_ASSERTION_TYPES:
            raise ValueError(
                f"assertion_type must be one of {sorted(_VALID_ASSERTION_TYPES)}, "
                f"got {assertion_type!r}"
            )

        if self._timer_start is None:
            raise ValueError(
                "start_timer() must be called before record() to compute duration_ms"
            )

        duration_ms = (time.monotonic() - self._timer_start) * 1000.0
        timestamp = datetime.now(timezone.utc).isoformat()

        entry: dict[str, Any] = {
            "test_id": test_id,
            "spec_ref": spec_ref,
            "timestamp": timestamp,
            "assertion_type": assertion_type,
            "inputs": inputs,
            "observed": observed,
            "expected": expected,
            "verdict": verdict,
            "evidence": evidence,
            "duration_ms": round(duration_ms, 3),
        }

        # Validate all 10 required fields are present
        missing = _REQUIRED_FIELDS - entry.keys()
        if missing:
            raise ValueError(f"Missing required audit fields: {sorted(missing)}")

        line = json.dumps(entry, separators=(",", ":"), sort_keys=False)
        with open(self.output_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        # Reset timer for next record
        self._timer_start = None

        return entry
