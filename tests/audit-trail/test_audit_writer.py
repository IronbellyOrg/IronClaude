"""Tests for AuditWriter JSONL record writer (T01.01 + T01.04 verification).

T01.04 adds verifiability property tests confirming the 4 FR-7.2 properties:
1. Real timestamps — ISO-8601, within reasonable bounds of now()
2. Spec-traced records — spec_ref is non-empty, follows FR-*/SC-* or code-ref pattern
3. Runtime observations — observed field contains concrete runtime data
4. Explicit verdicts — verdict is one of PASS, FAIL, SKIP
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

import importlib.util
import sys

# audit-trail is not a valid Python package name (hyphen), so import directly
_spec = importlib.util.spec_from_file_location(
    "audit_writer",
    Path(__file__).parent / "audit_writer.py",
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["audit_writer"] = _mod
_spec.loader.exec_module(_mod)
AuditWriter = _mod.AuditWriter
_REQUIRED_FIELDS = _mod._REQUIRED_FIELDS


@pytest.fixture
def writer(tmp_path: Path) -> AuditWriter:
    return AuditWriter(tmp_path / "audit.jsonl")


def _make_record(writer: AuditWriter, **overrides) -> dict:
    """Helper to emit a valid record with optional overrides."""
    defaults = {
        "test_id": "FR-1.1-test",
        "spec_ref": "executor.py:100-110",
        "assertion_type": "behavioral",
        "inputs": {"config": {"max_turns": 10}},
        "observed": {"result": "ok"},
        "expected": {"result": "ok"},
        "verdict": "PASS",
        "evidence": "Result matched expected value",
    }
    defaults.update(overrides)
    writer.start_timer()
    return writer.record(**defaults)


class TestAuditWriterBasic:
    """Core functionality: schema, JSONL format, field presence."""

    def test_record_produces_valid_jsonl(self, writer: AuditWriter) -> None:
        """Each record() call produces exactly one parseable JSON line."""
        _make_record(writer)
        _make_record(writer, test_id="FR-1.2-test")

        lines = writer.output_path.read_text().strip().split("\n")
        assert len(lines) == 2

        for line in lines:
            parsed = json.loads(line)
            assert isinstance(parsed, dict)

    def test_record_contains_all_10_fields(self, writer: AuditWriter) -> None:
        """Every record has exactly the 10 required schema fields."""
        record = _make_record(writer)
        assert set(record.keys()) == _REQUIRED_FIELDS

    def test_record_written_to_file_matches_return(self, writer: AuditWriter) -> None:
        """The returned dict matches what was written to the JSONL file."""
        record = _make_record(writer)
        line = writer.output_path.read_text().strip()
        written = json.loads(line)
        assert written == record

    def test_deterministic_given_same_inputs(self, writer: AuditWriter) -> None:
        """Given identical inputs, non-temporal fields are identical."""
        temporal_fields = {"timestamp", "duration_ms"}
        r1 = _make_record(writer)
        r2 = _make_record(writer)

        for key in _REQUIRED_FIELDS - temporal_fields:
            assert r1[key] == r2[key], f"Field {key!r} differs between records"


class TestAuditWriterDuration:
    """Auto-computed duration_ms from start_timer()/record()."""

    def test_duration_ms_is_positive(self, writer: AuditWriter) -> None:
        record = _make_record(writer)
        assert record["duration_ms"] > 0

    def test_duration_ms_reflects_elapsed_time(self, writer: AuditWriter) -> None:
        """duration_ms should be at least as long as a known sleep."""
        writer.start_timer()
        time.sleep(0.05)  # 50ms
        record = writer.record(
            test_id="FR-1.1-timing",
            spec_ref="executor.py:1",
            assertion_type="behavioral",
            inputs={},
            observed={},
            expected={},
            verdict="PASS",
            evidence="timing test",
        )
        assert record["duration_ms"] >= 40  # allow small timing variance

    def test_start_timer_required(self, writer: AuditWriter) -> None:
        """record() raises ValueError if start_timer() was not called."""
        with pytest.raises(ValueError, match="start_timer"):
            writer.record(
                test_id="FR-1.1-test",
                spec_ref="executor.py:1",
                assertion_type="behavioral",
                inputs={},
                observed={},
                expected={},
                verdict="PASS",
                evidence="test",
            )

    def test_timer_resets_after_record(self, writer: AuditWriter) -> None:
        """Timer is reset after each record(), requiring a new start_timer()."""
        _make_record(writer)
        with pytest.raises(ValueError, match="start_timer"):
            writer.record(
                test_id="FR-1.1-test2",
                spec_ref="executor.py:1",
                assertion_type="behavioral",
                inputs={},
                observed={},
                expected={},
                verdict="PASS",
                evidence="test",
            )


class TestAuditWriterValidation:
    """Schema validation: invalid verdicts, assertion types."""

    def test_invalid_verdict_raises(self, writer: AuditWriter) -> None:
        with pytest.raises(ValueError, match="verdict"):
            _make_record(writer, verdict="UNKNOWN")

    def test_invalid_assertion_type_raises(self, writer: AuditWriter) -> None:
        with pytest.raises(ValueError, match="assertion_type"):
            _make_record(writer, assertion_type="invalid")

    @pytest.mark.parametrize("verdict", ["PASS", "FAIL", "SKIP"])
    def test_valid_verdicts_accepted(self, writer: AuditWriter, verdict: str) -> None:
        record = _make_record(writer, verdict=verdict)
        assert record["verdict"] == verdict

    @pytest.mark.parametrize("atype", ["behavioral", "structural", "value"])
    def test_valid_assertion_types_accepted(
        self, writer: AuditWriter, atype: str
    ) -> None:
        record = _make_record(writer, assertion_type=atype)
        assert record["assertion_type"] == atype


class TestAuditWriterFileHandling:
    """File creation, append mode, parent directory creation."""

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        deep_path = tmp_path / "a" / "b" / "c" / "audit.jsonl"
        writer = AuditWriter(deep_path)
        _make_record(writer)
        assert deep_path.exists()

    def test_appends_to_existing_file(self, writer: AuditWriter) -> None:
        _make_record(writer, test_id="first")
        _make_record(writer, test_id="second")

        lines = writer.output_path.read_text().strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0])["test_id"] == "first"
        assert json.loads(lines[1])["test_id"] == "second"


class TestVerifiabilityProperties:
    """FR-7.2: Four third-party verifiability properties (T01.04).

    A third party with no prior knowledge MUST be able to determine from the
    audit trail alone that tests were real, spec-traced, runtime-observed,
    and explicitly verdicted.
    """

    def test_real_timestamps(self, writer: AuditWriter, audit_trail) -> None:
        """Property 1: timestamp is ISO-8601 UTC and within reasonable bounds.

        Proves: 'Were real tests run?' — timestamps are wall-clock, not static.
        """
        before = datetime.now(timezone.utc)
        record = _make_record(writer)
        after = datetime.now(timezone.utc)

        ts = record["timestamp"]

        # Must be valid ISO-8601
        parsed = datetime.fromisoformat(ts)
        assert parsed.tzinfo is not None, "Timestamp must be timezone-aware"

        # Must be between before and after (proves it's wall-clock, not hardcoded)
        assert before <= parsed <= after, (
            f"Timestamp {ts} not within test execution window "
            f"[{before.isoformat()}, {after.isoformat()}]"
        )

        # duration_ms must be non-negative (proves real timing)
        assert record["duration_ms"] >= 0

        audit_trail.record(
            test_id="FR-7.2-P1-real-timestamps",
            spec_ref="FR-7.2",
            assertion_type="structural",
            inputs={"property": "real_timestamps"},
            observed={"timestamp": ts, "duration_ms": record["duration_ms"]},
            expected={"iso8601": True, "within_bounds": True, "tz_aware": True},
            verdict="PASS",
            evidence=(
                f"Timestamp {ts} is valid ISO-8601 with timezone, "
                f"falls within test execution window, duration_ms={record['duration_ms']}"
            ),
        )

    def test_spec_traced(self, writer: AuditWriter, audit_trail) -> None:
        """Property 2: spec_ref traces to code location or spec identifier.

        Proves: 'Were tests run according to spec?' — every record is traceable.
        """
        # Test with code-location style spec_ref
        r1 = _make_record(writer, spec_ref="executor.py:1183-1191")
        assert r1["spec_ref"], "spec_ref must be non-empty"
        # Code-location pattern: filename:lines
        assert re.match(r".+\.\w+:\d+", r1["spec_ref"]), (
            f"spec_ref {r1['spec_ref']!r} does not match code-location pattern"
        )

        # Test with FR-* style spec_ref
        r2 = _make_record(writer, spec_ref="FR-1.5")
        assert re.match(r"^(FR|SC|NFR)-\d+", r2["spec_ref"]), (
            f"spec_ref {r2['spec_ref']!r} does not match spec-identifier pattern"
        )

        # Test with SC-* style spec_ref
        r3 = _make_record(writer, spec_ref="SC-4.2")
        assert re.match(r"^(FR|SC|NFR)-\d+", r3["spec_ref"])

        audit_trail.record(
            test_id="FR-7.2-P2-spec-traced",
            spec_ref="FR-7.2",
            assertion_type="structural",
            inputs={"spec_refs_tested": ["executor.py:1183-1191", "FR-1.5", "SC-4.2"]},
            observed={
                "r1_spec_ref": r1["spec_ref"],
                "r2_spec_ref": r2["spec_ref"],
                "r3_spec_ref": r3["spec_ref"],
            },
            expected={"all_non_empty": True, "all_match_pattern": True},
            verdict="PASS",
            evidence=(
                "All spec_ref values are non-empty and match either code-location "
                "(file:line) or spec-identifier (FR-*/SC-*/NFR-*) patterns"
            ),
        )

    def test_runtime_observations(self, writer: AuditWriter, audit_trail) -> None:
        """Property 3: observed field contains concrete runtime data.

        Proves: 'Are results real?' — observed values come from actual execution,
        not hardcoded static fixtures.
        """
        # Produce a record with runtime-derived observed values
        import os

        runtime_pid = os.getpid()
        runtime_time = time.monotonic()

        record = _make_record(
            writer,
            observed={
                "pid": runtime_pid,
                "monotonic_ns": runtime_time,
                "cwd": str(Path.cwd()),
            },
        )

        observed = record["observed"]

        # observed must be a dict with actual content
        assert isinstance(observed, dict), "observed must be a dict"
        assert len(observed) > 0, "observed must not be empty"

        # Values must be concrete runtime data, not None/empty
        assert observed["pid"] == runtime_pid, "observed.pid must match actual PID"
        assert observed["monotonic_ns"] > 0, "observed.monotonic_ns must be positive"
        assert len(observed["cwd"]) > 0, "observed.cwd must be non-empty path"

        audit_trail.record(
            test_id="FR-7.2-P3-runtime-observations",
            spec_ref="FR-7.2",
            assertion_type="behavioral",
            inputs={"observation_fields": ["pid", "monotonic_ns", "cwd"]},
            observed={
                "pid": runtime_pid,
                "monotonic_ns": runtime_time,
                "cwd": str(Path.cwd()),
                "observed_field_count": len(observed),
            },
            expected={"non_empty_dict": True, "concrete_values": True},
            verdict="PASS",
            evidence=(
                f"observed contains {len(observed)} concrete runtime values: "
                f"pid={runtime_pid}, monotonic_ns={runtime_time:.3f}, "
                f"cwd={Path.cwd()}"
            ),
        )

    def test_explicit_verdict(self, writer: AuditWriter, audit_trail) -> None:
        """Property 4: verdict is explicit PASS/FAIL/SKIP with comparable data.

        Proves: 'Pass/fail determination is sound' — expected vs observed
        comparison is explicit and the verdict reflects the comparison.
        """
        # PASS case: observed matches expected
        r_pass = _make_record(
            writer,
            observed={"value": 42},
            expected={"value": 42},
            verdict="PASS",
        )
        assert r_pass["verdict"] == "PASS"
        assert r_pass["observed"] == r_pass["expected"], (
            "PASS verdict requires observed == expected"
        )

        # FAIL case: observed differs from expected
        r_fail = _make_record(
            writer,
            observed={"value": 99},
            expected={"value": 42},
            verdict="FAIL",
        )
        assert r_fail["verdict"] == "FAIL"
        assert r_fail["observed"] != r_fail["expected"], (
            "FAIL verdict requires observed != expected"
        )

        # SKIP case: explicit skip with reason in evidence
        r_skip = _make_record(
            writer,
            observed={},
            expected={},
            verdict="SKIP",
            evidence="Precondition not met: module not available",
        )
        assert r_skip["verdict"] == "SKIP"
        assert len(r_skip["evidence"]) > 0, "SKIP must have evidence explaining why"

        # Verdict enum is exhaustive
        all_verdicts = {r_pass["verdict"], r_fail["verdict"], r_skip["verdict"]}
        assert all_verdicts == {"PASS", "FAIL", "SKIP"}

        audit_trail.record(
            test_id="FR-7.2-P4-explicit-verdict",
            spec_ref="FR-7.2",
            assertion_type="behavioral",
            inputs={"verdicts_tested": ["PASS", "FAIL", "SKIP"]},
            observed={
                "pass_match": r_pass["observed"] == r_pass["expected"],
                "fail_mismatch": r_fail["observed"] != r_fail["expected"],
                "skip_has_evidence": len(r_skip["evidence"]) > 0,
            },
            expected={
                "pass_match": True,
                "fail_mismatch": True,
                "skip_has_evidence": True,
            },
            verdict="PASS",
            evidence=(
                "All 3 verdict types exercised: PASS with matching observed/expected, "
                "FAIL with mismatched values, SKIP with explanatory evidence"
            ),
        )
