"""Tests for ExecutionLog with complete event coverage (NFR-007, T09.04).

Acceptance criteria:
- execution-log.jsonl contains gate_eval event after each gate check
- execution-log.jsonl contains convergence_transition event on each state change
- execution-log.md human-readable format mirrors jsonl content
- All event types have timestamp (ISO-8601), event_type, and step_id fields

Validation commands:
  uv run pytest tests/cli_portify/test_logging.py -k "log_events" -v
  uv run pytest tests/cli_portify/test_logging.py -k "logging_complete" -v
"""

from __future__ import annotations

import json

from superclaude.cli.cli_portify.logging_ import (
    ALL_EVENT_TYPES,
    EV_BUDGET_WARNING,
    EV_CONVERGENCE_TRANSITION,
    EV_GATE_EVAL,
    EV_GATE_FAIL,
    EV_PIPELINE_OUTCOME,
    EV_SIGNAL_RECEIVED,
    EV_STEP_END,
    EV_STEP_START,
    ExecutionLog,
)

# ---------------------------------------------------------------------------
# T09.04 acceptance criteria: log_events
# ---------------------------------------------------------------------------


class TestLogEvents:
    """ExecutionLog emits correct event types with correct schema.

    Validation command: uv run pytest tests/ -k "log_events"
    """

    def test_log_events_step_start_has_schema(self, tmp_path):
        """step_start event has timestamp, event_type, step_id fields."""
        log = ExecutionLog(tmp_path)
        log.step_start("validate-config")
        entries = log.get_all_entries()
        assert len(entries) == 1
        e = entries[0]
        assert e["event_type"] == EV_STEP_START
        assert e["step_id"] == "validate-config"
        assert "timestamp" in e

    def test_log_events_step_end_has_schema(self, tmp_path):
        """step_end event has required fields."""
        log = ExecutionLog(tmp_path)
        log.step_end("validate-config", status="pass", duration_s=1.5)
        entries = log.get_all_entries()
        e = entries[0]
        assert e["event_type"] == EV_STEP_END
        assert e["step_id"] == "validate-config"
        assert e["status"] == "pass"
        assert e["duration_s"] == 1.5

    def test_log_events_gate_eval_after_gate_check(self, tmp_path):
        """gate_eval event is recorded after each gate check."""
        log = ExecutionLog(tmp_path)
        log.gate_eval("analyze-workflow", gate_id="G-003", tier="STRICT")
        entries = log.get_all_entries()
        assert len(entries) == 1
        e = entries[0]
        assert e["event_type"] == EV_GATE_EVAL
        assert e["step_id"] == "analyze-workflow"
        assert e["gate_id"] == "G-003"
        assert e["tier"] == "STRICT"
        assert "timestamp" in e

    def test_log_events_gate_fail_recorded(self, tmp_path):
        """gate_fail event is recorded when a gate fails."""
        log = ExecutionLog(tmp_path)
        log.gate_fail("analyze-workflow", gate_id="G-003", reason="Missing sections")
        entries = log.get_all_entries()
        e = entries[0]
        assert e["event_type"] == EV_GATE_FAIL
        assert e["gate_id"] == "G-003"
        assert "Missing sections" in e["reason"]

    def test_log_events_convergence_transition_on_state_change(self, tmp_path):
        """convergence_transition event is recorded on each state change."""
        log = ExecutionLog(tmp_path)
        log.convergence_transition(
            "panel-review", from_state="RUNNING", to_state="CONVERGED", iteration=2
        )
        entries = log.get_all_entries()
        e = entries[0]
        assert e["event_type"] == EV_CONVERGENCE_TRANSITION
        assert e["step_id"] == "panel-review"
        assert e["from_state"] == "RUNNING"
        assert e["to_state"] == "CONVERGED"
        assert e["iteration"] == 2
        assert "timestamp" in e

    def test_log_events_signal_received(self, tmp_path):
        """signal_received event is recorded on OS signals."""
        log = ExecutionLog(tmp_path)
        log.signal_received("SIGINT", step_id="synthesize-spec")
        entries = log.get_all_entries()
        e = entries[0]
        assert e["event_type"] == EV_SIGNAL_RECEIVED
        assert e["signal_name"] == "SIGINT"

    def test_log_events_budget_warning(self, tmp_path):
        """budget_warning event is recorded when budget < 10%."""
        log = ExecutionLog(tmp_path)
        log.budget_warning(remaining=1, total=20, step_id="panel-review")
        entries = log.get_all_entries()
        e = entries[0]
        assert e["event_type"] == EV_BUDGET_WARNING
        assert e["remaining_turns"] == 1
        assert e["total_turns"] == 20
        assert e["pct_remaining"] == 5.0

    def test_log_events_pipeline_outcome(self, tmp_path):
        """pipeline_outcome event is recorded at pipeline end."""
        log = ExecutionLog(tmp_path)
        log.pipeline_outcome("SUCCESS")
        entries = log.get_all_entries()
        e = entries[0]
        assert e["event_type"] == EV_PIPELINE_OUTCOME
        assert e["outcome"] == "SUCCESS"

    def test_log_events_all_event_types_have_required_schema(self, tmp_path):
        """All 8 event types have timestamp (ISO-8601), event_type, and step_id."""
        log = ExecutionLog(tmp_path)
        log.step_start("s1")
        log.step_end("s1", status="pass")
        log.gate_eval("s1", gate_id="G-000")
        log.gate_fail("s1", gate_id="G-000", reason="test")
        log.convergence_transition("s1", from_state="A", to_state="B")
        log.signal_received("SIGTERM", step_id="s1")
        log.budget_warning(remaining=1, total=10, step_id="s1")
        log.pipeline_outcome("FAILURE")
        entries = log.get_all_entries()
        assert len(entries) == 8
        for e in entries:
            assert "timestamp" in e, f"Missing timestamp in {e['event_type']}"
            assert "event_type" in e
            assert "step_id" in e
            # Verify ISO-8601 format contains T separator
            assert "T" in e["timestamp"], f"Non-ISO timestamp in {e['event_type']}"


# ---------------------------------------------------------------------------
# T09.04 acceptance criteria: logging_complete
# ---------------------------------------------------------------------------


class TestLoggingComplete:
    """ExecutionLog produces correct JSONL and Markdown files.

    Validation command: uv run pytest tests/ -k "logging_complete"
    """

    def test_logging_complete_jsonl_written_on_flush(self, tmp_path):
        """flush() writes execution-log.jsonl."""
        log = ExecutionLog(tmp_path)
        log.step_start("validate-config")
        log.flush(phase="validate-config", status="pass", elapsed=1.0)
        jsonl_path = tmp_path / "execution-log.jsonl"
        assert jsonl_path.exists()
        lines = jsonl_path.read_text().strip().splitlines()
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["event_type"] == EV_STEP_START

    def test_logging_complete_md_written_on_flush(self, tmp_path):
        """flush() writes execution-log.md."""
        log = ExecutionLog(tmp_path)
        log.step_start("validate-config")
        log.flush(phase="validate-config", status="pass", elapsed=0.5)
        md_path = tmp_path / "execution-log.md"
        assert md_path.exists()
        content = md_path.read_text()
        assert "validate-config" in content
        assert "pass" in content

    def test_logging_complete_md_mirrors_jsonl_content(self, tmp_path):
        """execution-log.md human-readable format mirrors jsonl content."""
        log = ExecutionLog(tmp_path)
        log.gate_eval("analyze-workflow", gate_id="G-003")
        log.flush(phase="analyze-workflow", status="pass", elapsed=2.3)
        jsonl_path = tmp_path / "execution-log.jsonl"
        md_path = tmp_path / "execution-log.md"
        # jsonl has the gate_eval event
        lines = jsonl_path.read_text().strip().splitlines()
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["event_type"] == EV_GATE_EVAL
        # md has the phase reference
        content = md_path.read_text()
        assert "analyze-workflow" in content

    def test_logging_complete_all_eight_event_types(self, tmp_path):
        """All 8 event types are present in ALL_EVENT_TYPES constant."""
        expected = {
            "step_start",
            "step_end",
            "gate_eval",
            "gate_fail",
            "convergence_transition",
            "signal_received",
            "budget_warning",
            "pipeline_outcome",
        }
        assert set(ALL_EVENT_TYPES) == expected

    def test_logging_complete_entries_cleared_after_flush(self, tmp_path):
        """Entries are cleared after flush."""
        log = ExecutionLog(tmp_path)
        log.step_start("validate-config")
        assert len(log.get_all_entries()) == 1
        log.flush()
        assert len(log.get_all_entries()) == 0

    def test_logging_complete_multiple_flushes_append(self, tmp_path):
        """Multiple flush() calls append to execution-log.jsonl."""
        log = ExecutionLog(tmp_path)
        log.step_start("validate-config")
        log.flush(phase="phase1", status="pass", elapsed=0.5)
        log.step_end("validate-config", status="pass")
        log.flush(phase="phase1", status="pass", elapsed=0.2)
        jsonl_path = tmp_path / "execution-log.jsonl"
        lines = jsonl_path.read_text().strip().splitlines()
        assert len(lines) == 2

    def test_logging_complete_gate_eval_in_jsonl(self, tmp_path):
        """gate_eval event appears in execution-log.jsonl after gate check."""
        log = ExecutionLog(tmp_path)
        log.gate_eval("synthesize-spec", gate_id="G-007", tier="STRICT")
        log.flush()
        jsonl_path = tmp_path / "execution-log.jsonl"
        lines = jsonl_path.read_text().strip().splitlines()
        assert len(lines) == 1
        e = json.loads(lines[0])
        assert e["event_type"] == EV_GATE_EVAL

    def test_logging_complete_convergence_transition_in_jsonl(self, tmp_path):
        """convergence_transition event appears in execution-log.jsonl."""
        log = ExecutionLog(tmp_path)
        log.convergence_transition(
            "panel-review", from_state="RUNNING", to_state="ESCALATED", iteration=3
        )
        log.flush()
        jsonl_path = tmp_path / "execution-log.jsonl"
        e = json.loads(jsonl_path.read_text().strip())
        assert e["event_type"] == EV_CONVERGENCE_TRANSITION
        assert e["to_state"] == "ESCALATED"


# ---------------------------------------------------------------------------
# Migrated from test_monitor.py TestEventLogger/TestDiagnosticReport
# (C01 rows A-02, A-03, A-04, A-20) onto the live ExecutionLog owner.
# ---------------------------------------------------------------------------


class TestLiveLoggingMigrated:
    """Live ExecutionLog obligations previously asserted via monitor helpers."""

    def _record_sequence(self, log):
        log.step_start("s1")
        log.gate_eval("s1", gate_id="G-001", tier="STRICT")
        log.gate_fail("s1", gate_id="G-001", reason="missing section")
        log.step_end("s1", status="fail", duration_s=0.25)
        log.pipeline_outcome("FAILURE")
        return [
            EV_STEP_START,
            EV_GATE_EVAL,
            EV_GATE_FAIL,
            EV_STEP_END,
            EV_PIPELINE_OUTCOME,
        ]

    def test_logging_complete_n_events_one_flush_n_jsonl_lines(self, tmp_path):
        """A-02: N records in one flush -> N parseable JSONL lines with schema."""
        log = ExecutionLog(tmp_path)
        expected = self._record_sequence(log)
        log.flush(phase="p", status="fail", elapsed=0.0)
        lines = (tmp_path / "execution-log.jsonl").read_text().splitlines()
        assert len(lines) == len(expected) == 5
        for line in lines:
            e = json.loads(line)
            assert {"timestamp", "event_type", "step_id"} <= e.keys()
            assert "T" in e["timestamp"]

    def test_logging_complete_record_order_preserved(self, tmp_path):
        """A-03: in-memory entries and flushed JSONL keep record order."""
        log = ExecutionLog(tmp_path)
        expected = self._record_sequence(log)
        assert [e["event_type"] for e in log.get_all_entries()] == expected
        log.flush()
        lines = (tmp_path / "execution-log.jsonl").read_text().splitlines()
        assert [json.loads(line)["event_type"] for line in lines] == expected

    def test_logging_complete_extra_kwargs_in_jsonl(self, tmp_path):
        """A-04: arbitrary record() kwargs are serialized as top-level fields."""
        log = ExecutionLog(tmp_path)
        log.record(EV_STEP_START, step_id="s1", attempt=2, detail={"k": "v"})
        log.step_end("s1", status="pass", custom_flag=True)
        log.flush()
        lines = (tmp_path / "execution-log.jsonl").read_text().splitlines()
        first, second = (json.loads(line) for line in lines)
        assert first["attempt"] == 2
        assert first["detail"] == {"k": "v"}
        assert first["step_id"] == "s1"
        assert second["custom_flag"] is True
        assert second["status"] == "pass"

    def test_logging_complete_md_row_reports_event_count(self, tmp_path):
        """A-20: execution-log.md row reports the number of flushed events."""
        log = ExecutionLog(tmp_path)
        self._record_sequence(log)
        log.flush(phase="analyze", status="fail", elapsed=1.5)
        log.step_start("s2")
        log.flush(phase="synth", status="pass", elapsed=0.25)
        md_lines = (tmp_path / "execution-log.md").read_text().splitlines()
        assert md_lines[2] == "| Phase | Status | Elapsed | Events |"
        assert md_lines[4] == "| analyze | fail | 1.500s | 5 |"
        assert md_lines[5] == "| synth | pass | 0.250s | 1 |"
        jsonl = (tmp_path / "execution-log.jsonl").read_text().splitlines()
        assert len(jsonl) == 6  # md counts sum to JSONL line total
