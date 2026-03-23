"""Audit-trail test fixtures, providing audit_trail for verifiability tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_writer import AuditWriter


class AuditTrailHelper:
    """Wraps AuditWriter with auto-timer management for test convenience."""

    def __init__(self, writer: AuditWriter, results_dir: Path) -> None:
        self.writer = writer
        self.results_dir = results_dir
        self.records: list[dict[str, Any]] = []

    def start_timer(self) -> None:
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


@pytest.fixture(scope="session")
def audit_trail(tmp_path_factory: pytest.TempPathFactory) -> AuditTrailHelper:
    """Session-scoped audit trail for audit-trail verifiability tests."""
    results_dir = tmp_path_factory.mktemp("audit-trail-results")
    output_path = results_dir / "audit.jsonl"
    writer = AuditWriter(output_path)
    helper = AuditTrailHelper(writer, results_dir)

    yield helper

    # Write summary on teardown
    summary = {
        "total": len(helper.records),
        "passed": sum(1 for r in helper.records if r["verdict"] == "PASS"),
        "failed": sum(1 for r in helper.records if r["verdict"] == "FAIL"),
    }
    summary_line = json.dumps({"assertion_type": "session_summary", **summary}, separators=(",", ":"))
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(summary_line + "\n")
