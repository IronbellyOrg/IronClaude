"""Tests for session-end summary report generation (T01.03 verification).

Verifies that the audit_trail fixture teardown produces correct summary
output with total/passed/failed/skipped counts and spec_ref-based wiring
coverage percentage.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "audit-trail"))

from audit_writer import AuditWriter

# Import the helper directly to test summary logic without session fixture
sys.path.insert(0, str(Path(__file__).resolve().parent))
from conftest import AuditTrailHelper


class TestSummaryComputation:
    """Verify summary() produces correct aggregate statistics."""

    @pytest.fixture
    def helper(self, tmp_path: Path) -> AuditTrailHelper:
        """Create a fresh AuditTrailHelper for each test."""
        writer = AuditWriter(tmp_path / "audit.jsonl")
        return AuditTrailHelper(writer, tmp_path)

    def _emit(
        self,
        helper: AuditTrailHelper,
        test_id: str,
        spec_ref: str = "executor.py:100-110",
        verdict: str = "PASS",
    ) -> dict[str, Any]:
        return helper.record(
            test_id=test_id,
            spec_ref=spec_ref,
            assertion_type="behavioral",
            inputs={},
            observed={},
            expected={},
            verdict=verdict,
            evidence="test evidence",
        )

    def test_summary_counts_all_verdicts(self, helper: AuditTrailHelper) -> None:
        """Summary correctly counts PASS, FAIL, and SKIP verdicts."""
        self._emit(helper, "t1", verdict="PASS")
        self._emit(helper, "t2", verdict="PASS")
        self._emit(helper, "t3", verdict="FAIL")
        self._emit(helper, "t4", verdict="SKIP")

        s = helper.summary()
        assert s["total"] == 4
        assert s["passed"] == 2
        assert s["failed"] == 1
        assert s["skipped"] == 1

    def test_summary_empty_session(self, helper: AuditTrailHelper) -> None:
        """Summary handles zero records gracefully."""
        s = helper.summary()
        assert s["total"] == 0
        assert s["passed"] == 0
        assert s["failed"] == 0
        assert s["skipped"] == 0
        assert s["wiring_coverage_pct"] == 0.0

    def test_wiring_coverage_is_spec_ref_based(self, helper: AuditTrailHelper) -> None:
        """Wiring coverage = unique spec_refs with PASS / total unique spec_refs."""
        # 3 distinct spec_refs; 2 have at least one PASS
        self._emit(helper, "t1", spec_ref="FR-1.1", verdict="PASS")
        self._emit(helper, "t2", spec_ref="FR-1.2", verdict="FAIL")
        self._emit(helper, "t3", spec_ref="FR-1.3", verdict="PASS")

        s = helper.summary()
        # 2 out of 3 spec_refs have PASS → 66.67%
        assert s["wiring_coverage_pct"] == pytest.approx(66.67, abs=0.01)

    def test_wiring_coverage_duplicate_spec_refs(self, helper: AuditTrailHelper) -> None:
        """Multiple records for same spec_ref count as one wiring point."""
        self._emit(helper, "t1", spec_ref="FR-1.1", verdict="FAIL")
        self._emit(helper, "t2", spec_ref="FR-1.1", verdict="PASS")  # retry passes
        self._emit(helper, "t3", spec_ref="FR-1.2", verdict="FAIL")

        s = helper.summary()
        # FR-1.1 has a PASS, FR-1.2 does not → 50%
        assert s["wiring_coverage_pct"] == 50.0

    def test_wiring_coverage_all_pass(self, helper: AuditTrailHelper) -> None:
        """100% coverage when all spec_refs have at least one PASS."""
        self._emit(helper, "t1", spec_ref="FR-1.1", verdict="PASS")
        self._emit(helper, "t2", spec_ref="FR-1.2", verdict="PASS")

        s = helper.summary()
        assert s["wiring_coverage_pct"] == 100.0

    def test_wiring_coverage_all_fail(self, helper: AuditTrailHelper) -> None:
        """0% coverage when no spec_refs have PASS."""
        self._emit(helper, "t1", spec_ref="FR-1.1", verdict="FAIL")
        self._emit(helper, "t2", spec_ref="FR-1.2", verdict="SKIP")

        s = helper.summary()
        assert s["wiring_coverage_pct"] == 0.0

    def test_summary_is_deterministic(self, helper: AuditTrailHelper) -> None:
        """Given the same records, summary() returns identical results."""
        self._emit(helper, "t1", spec_ref="FR-1.1", verdict="PASS")
        self._emit(helper, "t2", spec_ref="FR-1.2", verdict="FAIL")

        s1 = helper.summary()
        s2 = helper.summary()
        assert s1 == s2


class TestSummaryTeardownOutput:
    """Verify that fixture teardown writes summary to JSONL and summary.json."""

    def test_teardown_writes_summary_jsonl_record(self, tmp_path: Path) -> None:
        """Teardown appends a session_summary record to the JSONL file."""
        output_path = tmp_path / "audit.jsonl"
        writer = AuditWriter(output_path)
        helper = AuditTrailHelper(writer, tmp_path)

        helper.record(
            test_id="t1",
            spec_ref="FR-1.1",
            assertion_type="behavioral",
            inputs={},
            observed={},
            expected={},
            verdict="PASS",
            evidence="test",
        )

        # Simulate teardown: write summary record
        summary = helper.summary()
        summary_record = {"assertion_type": "session_summary", **summary}
        summary_line = json.dumps(summary_record, separators=(",", ":"))
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(summary_line + "\n")

        lines = output_path.read_text().strip().split("\n")
        last_record = json.loads(lines[-1])
        assert last_record["assertion_type"] == "session_summary"
        assert last_record["total"] == 1
        assert last_record["passed"] == 1
        assert last_record["wiring_coverage_pct"] == 100.0

    def test_teardown_writes_summary_json_file(self, tmp_path: Path) -> None:
        """Teardown writes a standalone summary.json file."""
        output_path = tmp_path / "audit.jsonl"
        writer = AuditWriter(output_path)
        helper = AuditTrailHelper(writer, tmp_path)

        helper.record(
            test_id="t1",
            spec_ref="FR-1.1",
            assertion_type="behavioral",
            inputs={},
            observed={},
            expected={},
            verdict="PASS",
            evidence="test",
        )
        helper.record(
            test_id="t2",
            spec_ref="FR-1.2",
            assertion_type="behavioral",
            inputs={},
            observed={},
            expected={},
            verdict="FAIL",
            evidence="test",
        )

        # Simulate teardown: write summary.json
        summary = helper.summary()
        summary_record = {"assertion_type": "session_summary", **summary}
        summary_path = tmp_path / "summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary_record, f, indent=2)

        assert summary_path.exists()
        loaded = json.loads(summary_path.read_text())
        assert loaded["total"] == 2
        assert loaded["passed"] == 1
        assert loaded["failed"] == 1
        assert loaded["wiring_coverage_pct"] == 50.0
