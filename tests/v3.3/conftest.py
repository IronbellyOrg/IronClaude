"""Session-scoped audit_trail fixture for v3.3 TurnLedger validation (FR-7.3).

Provides a session-scoped ``audit_trail`` fixture that wraps ``AuditWriter``
and is available to all tests under ``tests/v3.3/``.

Fixture scope
-------------
Session-scoped: a single ``AuditWriter`` instance is shared across the entire
test session, writing all audit records to one JSONL file.

Output path
-----------
``{tmp_path_factory basetemp}/v3.3-results/audit.jsonl``

``record()`` method signature
-----------------------------
Same keyword-only arguments as ``AuditWriter.record()``:
    test_id, spec_ref, assertion_type, inputs, observed, expected, verdict, evidence

The fixture automatically calls ``start_timer()`` before yielding and
provides an ``AuditTrailHelper`` with a ``record()`` method that auto-flushes
(the underlying writer flushes on every ``record()`` call since it opens/closes
the file each time).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "audit-trail"))

from audit_writer import AuditWriter


class AuditTrailHelper:
    """Wraps AuditWriter with auto-timer management for test convenience.

    Each call to ``record()`` automatically starts the timer if not already
    started, ensuring ``duration_ms`` is always computable.

    Attributes
    ----------
    writer : AuditWriter
        The underlying JSONL writer.
    results_dir : Path
        Directory containing the audit JSONL output.
    records : list[dict]
        In-memory list of all records emitted during the session.
    """

    def __init__(self, writer: AuditWriter, results_dir: Path) -> None:
        self.writer = writer
        self.results_dir = results_dir
        self.records: list[dict[str, Any]] = []

    def start_timer(self) -> None:
        """Explicitly start the timer for precise duration measurement."""
        self.writer.start_timer()

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
        """Write one audit record, auto-starting timer if needed.

        Parameters match ``AuditWriter.record()`` exactly. The timer is
        auto-started if ``start_timer()`` was not called explicitly,
        giving a near-zero ``duration_ms`` (measuring only record overhead).

        Returns the complete 10-field record dict.
        """
        if self.writer._timer_start is None:
            self.writer.start_timer()

        entry = self.writer.record(
            test_id=test_id,
            spec_ref=spec_ref,
            assertion_type=assertion_type,
            inputs=inputs,
            observed=observed,
            expected=expected,
            verdict=verdict,
            evidence=evidence,
        )
        self.records.append(entry)
        return entry

    def summary(self) -> dict[str, Any]:
        """Compute session summary from all recorded entries.

        Wiring coverage is computed as the percentage of distinct ``spec_ref``
        values that have at least one PASS verdict, relative to the total
        number of distinct ``spec_ref`` values seen across all records.

        Returns
        -------
        dict
            Keys: total, passed, failed, skipped, wiring_coverage_pct
        """
        total = len(self.records)
        passed = sum(1 for r in self.records if r["verdict"] == "PASS")
        failed = sum(1 for r in self.records if r["verdict"] == "FAIL")
        skipped = sum(1 for r in self.records if r["verdict"] == "SKIP")

        # Wiring coverage: fraction of unique spec_refs with at least one PASS
        all_refs = {r["spec_ref"] for r in self.records}
        passed_refs = {r["spec_ref"] for r in self.records if r["verdict"] == "PASS"}
        wiring_coverage = (len(passed_refs) / len(all_refs) * 100.0) if all_refs else 0.0

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "wiring_coverage_pct": round(wiring_coverage, 2),
        }


@pytest.fixture(scope="session")
def results_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Session-scoped results directory for v3.3 test artifacts."""
    d = tmp_path_factory.mktemp("v3.3-results")
    return d


@pytest.fixture(scope="session")
def audit_trail(results_dir: Path) -> AuditTrailHelper:
    """Session-scoped audit trail fixture for JSONL audit record emission.

    Instantiates an ``AuditWriter`` writing to ``results_dir / "audit.jsonl"``
    and wraps it in an ``AuditTrailHelper`` that provides a ``record()`` method
    with auto-timer management and an in-memory record list.

    On teardown, generates a session-end summary report containing:
    - ``total``: number of audit records emitted
    - ``passed``: records with verdict PASS
    - ``failed``: records with verdict FAIL
    - ``skipped``: records with verdict SKIP
    - ``wiring_coverage_pct``: percentage of distinct ``spec_ref`` values
      that have at least one PASS verdict

    The summary is written three ways:
    1. As the final JSONL record in ``audit.jsonl`` (``assertion_type: "session_summary"``)
    2. As a standalone ``summary.json`` file in ``results_dir``
    3. Printed to stdout for visibility in test output

    Yields
    ------
    AuditTrailHelper
        Helper with ``record()`` method matching ``AuditWriter.record()``
        signature, plus ``summary()`` for aggregate statistics.
    """
    output_path = results_dir / "audit.jsonl"
    writer = AuditWriter(output_path)
    helper = AuditTrailHelper(writer, results_dir)

    yield helper

    # Session teardown: generate summary report
    summary = helper.summary()

    # 1. Append summary as final JSONL record
    summary_record = {"assertion_type": "session_summary", **summary}
    summary_line = json.dumps(summary_record, separators=(",", ":"))
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(summary_line + "\n")

    # 2. Write standalone summary JSON file for easy consumption
    summary_path = results_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_record, f, indent=2)

    # 3. Print summary to stdout for visibility in test output
    print(
        f"\n{'='*60}\n"
        f"  v3.3 Audit Trail Session Summary\n"
        f"{'='*60}\n"
        f"  Total:              {summary['total']}\n"
        f"  Passed:             {summary['passed']}\n"
        f"  Failed:             {summary['failed']}\n"
        f"  Skipped:            {summary['skipped']}\n"
        f"  Wiring Coverage:    {summary['wiring_coverage_pct']}%\n"
        f"{'='*60}\n"
        f"  JSONL:    {output_path}\n"
        f"  Summary:  {summary_path}\n"
        f"{'='*60}"
    )
