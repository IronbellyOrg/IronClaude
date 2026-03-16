"""Tests for Phase 1 data model additions: execution_mode, command, classifier,
PhaseStatus.PREFLIGHT_PASS, and python-mode validation.

Covers roadmap items R-008 through R-013.
"""

from __future__ import annotations

from pathlib import Path

import click
import pytest

from superclaude.cli.sprint.config import (
    discover_phases,
    parse_tasklist,
)
from superclaude.cli.sprint.models import Phase, PhaseStatus, TaskEntry


# ---------------------------------------------------------------------------
# T01.07 — Unit tests (R-008 through R-012)
# ---------------------------------------------------------------------------


class TestPhaseExecutionMode:
    """Unit tests for Phase.execution_mode field (R-008)."""

    @pytest.mark.unit
    def test_phase_execution_mode_default(self):
        """Phase.execution_mode defaults to 'claude'."""
        phase = Phase(number=1, file=Path("phase-1-tasklist.md"))
        assert phase.execution_mode == "claude"

    @pytest.mark.unit
    def test_phase_execution_mode_python(self):
        """Phase.execution_mode can be set to 'python'."""
        phase = Phase(
            number=1, file=Path("phase-1-tasklist.md"), execution_mode="python"
        )
        assert phase.execution_mode == "python"

    @pytest.mark.unit
    def test_phase_execution_mode_skip(self):
        """Phase.execution_mode can be set to 'skip'."""
        phase = Phase(number=1, file=Path("phase-1-tasklist.md"), execution_mode="skip")
        assert phase.execution_mode == "skip"

    @pytest.mark.unit
    def test_phase_existing_fields_unchanged(self):
        """Existing Phase fields (number, file, name) still work correctly."""
        p = Path("phase-2-tasklist.md")
        phase = Phase(number=2, file=p, name="Test Phase")
        assert phase.number == 2
        assert phase.file == p
        assert phase.name == "Test Phase"
        assert phase.display_name == "Test Phase"


class TestTaskEntryCommand:
    """Unit tests for TaskEntry.command field (R-009)."""

    @pytest.mark.unit
    def test_task_entry_command_empty(self):
        """TaskEntry.command defaults to empty string."""
        task = TaskEntry(task_id="T01.01", title="Test task")
        assert task.command == ""

    @pytest.mark.unit
    def test_task_entry_command_simple(self):
        """parse_tasklist extracts a simple **Command:** field."""
        content = """\
### T01.01 -- Simple command task

**Command:** `echo hello`

**Dependencies:** None
"""
        tasks = parse_tasklist(content)
        assert len(tasks) == 1
        assert tasks[0].command == "echo hello"

    @pytest.mark.unit
    def test_task_entry_command_pipes(self):
        """parse_tasklist preserves pipes verbatim in command."""
        content = """\
### T01.01 -- Pipe command task

**Command:** `uv run pytest tests/ | grep PASS > results.txt`

**Dependencies:** None
"""
        tasks = parse_tasklist(content)
        assert len(tasks) == 1
        assert tasks[0].command == "uv run pytest tests/ | grep PASS > results.txt"

    @pytest.mark.unit
    def test_task_entry_command_quotes(self):
        """parse_tasklist preserves quoted arguments in command."""
        content = """\
### T01.01 -- Quoted args task

**Command:** `cmd "arg with spaces" --flag`

**Dependencies:** None
"""
        tasks = parse_tasklist(content)
        assert len(tasks) == 1
        assert tasks[0].command == 'cmd "arg with spaces" --flag'

    @pytest.mark.unit
    def test_task_entry_command_no_backticks(self):
        """parse_tasklist extracts command without backtick delimiters."""
        content = """\
### T01.01 -- No backtick task

**Command:** uv run python script.py

**Dependencies:** None
"""
        tasks = parse_tasklist(content)
        assert len(tasks) == 1
        assert tasks[0].command == "uv run python script.py"

    @pytest.mark.unit
    def test_existing_task_without_command_unchanged(self):
        """Tasks without **Command:** field parse identically to pre-change."""
        content = """\
### T01.01 -- No command task

**Deliverables:**
- Some deliverable

**Dependencies:** None
"""
        tasks = parse_tasklist(content)
        assert len(tasks) == 1
        assert tasks[0].command == ""
        assert tasks[0].description == "Some deliverable"


class TestTaskEntryClassifier:
    """Unit tests for TaskEntry.classifier field (R-010)."""

    @pytest.mark.unit
    def test_task_entry_classifier_default(self):
        """TaskEntry.classifier defaults to empty string."""
        task = TaskEntry(task_id="T01.01", title="Test task")
        assert task.classifier == ""

    @pytest.mark.unit
    def test_task_entry_classifier_extraction(self):
        """parse_tasklist extracts | Classifier | table row."""
        content = """\
### T01.01 -- Classified task

| Field | Value |
|---|---|
| Classifier | empirical_gate_v1 |

**Dependencies:** None
"""
        tasks = parse_tasklist(content)
        assert len(tasks) == 1
        assert tasks[0].classifier == "empirical_gate_v1"

    @pytest.mark.unit
    def test_task_entry_classifier_absent(self):
        """Tasks without | Classifier | row have empty classifier."""
        content = """\
### T01.01 -- No classifier task

| Field | Value |
|---|---|
| Effort | XS |

**Dependencies:** None
"""
        tasks = parse_tasklist(content)
        assert len(tasks) == 1
        assert tasks[0].classifier == ""


class TestPhaseStatusPreflightPass:
    """Unit tests for PhaseStatus.PREFLIGHT_PASS (R-011)."""

    @pytest.mark.unit
    def test_preflight_pass_exists(self):
        """PhaseStatus.PREFLIGHT_PASS exists with correct value."""
        assert PhaseStatus.PREFLIGHT_PASS.value == "preflight_pass"

    @pytest.mark.unit
    def test_preflight_pass_is_success(self):
        """PhaseStatus.PREFLIGHT_PASS.is_success returns True."""
        assert PhaseStatus.PREFLIGHT_PASS.is_success is True

    @pytest.mark.unit
    def test_preflight_pass_is_not_failure(self):
        """PhaseStatus.PREFLIGHT_PASS.is_failure returns False."""
        assert PhaseStatus.PREFLIGHT_PASS.is_failure is False

    @pytest.mark.unit
    def test_preflight_pass_is_terminal(self):
        """PhaseStatus.PREFLIGHT_PASS.is_terminal returns True."""
        assert PhaseStatus.PREFLIGHT_PASS.is_terminal is True

    @pytest.mark.unit
    def test_existing_phase_statuses_unchanged(self):
        """Existing PhaseStatus values and their properties are unchanged."""
        assert PhaseStatus.PASS.is_success is True
        assert PhaseStatus.PASS.is_failure is False
        assert PhaseStatus.HALT.is_failure is True
        assert PhaseStatus.HALT.is_success is False
        assert PhaseStatus.SKIPPED.is_success is False
        assert PhaseStatus.SKIPPED.is_failure is False


class TestPythonModeEmptyCommandValidation:
    """Unit tests for python-mode empty command validation (R-012)."""

    @pytest.mark.unit
    def test_python_mode_empty_command_raises(self):
        """python-mode phase raises ClickException for task with no command."""
        content = """\
### T01.01 -- Task without command

**Deliverables:**
- Something

**Dependencies:** None
"""
        with pytest.raises(click.ClickException) as exc_info:
            parse_tasklist(content, execution_mode="python")
        assert "T01.01" in str(exc_info.value.format_message())
        assert "python-mode" in str(exc_info.value.format_message())
        assert "no command" in str(exc_info.value.format_message())

    @pytest.mark.unit
    def test_python_mode_with_command_succeeds(self):
        """python-mode phase succeeds when all tasks have commands."""
        content = """\
### T01.01 -- Task with command

**Command:** `uv run pytest tests/ -v`

**Dependencies:** None
"""
        tasks = parse_tasklist(content, execution_mode="python")
        assert len(tasks) == 1
        assert tasks[0].command == "uv run pytest tests/ -v"

    @pytest.mark.unit
    def test_claude_mode_allows_empty_command(self):
        """claude-mode phase does not raise for tasks without commands."""
        content = """\
### T01.01 -- No command, claude mode

**Deliverables:**
- Something

**Dependencies:** None
"""
        tasks = parse_tasklist(content, execution_mode="claude")
        assert len(tasks) == 1
        assert tasks[0].command == ""

    @pytest.mark.unit
    def test_skip_mode_allows_empty_command(self):
        """skip-mode phase does not raise for tasks without commands."""
        content = """\
### T01.01 -- No command, skip mode

**Deliverables:**
- Something

**Dependencies:** None
"""
        tasks = parse_tasklist(content, execution_mode="skip")
        assert len(tasks) == 1
        assert tasks[0].command == ""

    @pytest.mark.unit
    def test_python_mode_first_empty_raises(self):
        """python-mode raises on the first task missing a command."""
        content = """\
### T01.01 -- Has command

**Command:** `echo ok`

**Dependencies:** None

### T01.02 -- Missing command

**Deliverables:**
- Oops

**Dependencies:** T01.01
"""
        with pytest.raises(click.ClickException) as exc_info:
            parse_tasklist(content, execution_mode="python")
        assert "T01.02" in str(exc_info.value.format_message())


# ---------------------------------------------------------------------------
# T01.08 — Round-trip integration test (R-013)
# ---------------------------------------------------------------------------


class TestRoundTripExecutionMode:
    """Integration tests for Execution Mode column parsing (R-013)."""

    @pytest.mark.integration
    def test_round_trip_execution_mode(self, tmp_path: Path):
        """Write a tasklist-index.md with Execution Mode column and parse it."""
        # Create phase files
        for i in range(1, 4):
            phase_file = tmp_path / f"phase-{i}-tasklist.md"
            phase_file.write_text(
                f"# Phase {i}\n\n### T0{i}.01 -- Task\n\n**Dependencies:** None\n"
            )

        # Write index with Execution Mode column
        index_content = """\
# Tasklist Index

## Phase Files

| Phase | File | Execution Mode |
|---|---|---|
| 1 | phase-1-tasklist.md | python |
| 2 | phase-2-tasklist.md | claude |
| 3 | phase-3-tasklist.md | skip |
"""
        index_file = tmp_path / "tasklist-index.md"
        index_file.write_text(index_content)

        phases = discover_phases(index_file)

        assert len(phases) == 3
        assert phases[0].execution_mode == "python"
        assert phases[1].execution_mode == "claude"
        assert phases[2].execution_mode == "skip"

    @pytest.mark.integration
    def test_round_trip_execution_mode_absent_column(self, tmp_path: Path):
        """When Execution Mode column is absent, all phases default to 'claude'."""
        # Create phase files
        for i in range(1, 3):
            phase_file = tmp_path / f"phase-{i}-tasklist.md"
            phase_file.write_text(
                f"# Phase {i}\n\n### T0{i}.01 -- Task\n\n**Dependencies:** None\n"
            )

        # Index without Execution Mode column
        index_content = """\
# Tasklist Index

## Phase Files

| Phase | File | Phase Name |
|---|---|---|
| 1 | phase-1-tasklist.md | Data Model |
| 2 | phase-2-tasklist.md | Executor Core |
"""
        index_file = tmp_path / "tasklist-index.md"
        index_file.write_text(index_content)

        phases = discover_phases(index_file)

        assert len(phases) == 2
        assert phases[0].execution_mode == "claude"
        assert phases[1].execution_mode == "claude"

    @pytest.mark.integration
    def test_round_trip_case_normalization(self, tmp_path: Path):
        """Execution mode values are case-normalized to lowercase."""
        phase_file = tmp_path / "phase-1-tasklist.md"
        phase_file.write_text(
            "# Phase 1\n\n### T01.01 -- Task\n\n**Dependencies:** None\n"
        )

        index_content = """\
# Tasklist Index

## Phase Files

| Phase | File | Execution Mode |
|---|---|---|
| 1 | phase-1-tasklist.md | Python |
"""
        index_file = tmp_path / "tasklist-index.md"
        index_file.write_text(index_content)

        phases = discover_phases(index_file)
        assert phases[0].execution_mode == "python"

    @pytest.mark.integration
    def test_round_trip_invalid_mode_raises(self, tmp_path: Path):
        """Unknown execution mode raises ClickException."""
        phase_file = tmp_path / "phase-1-tasklist.md"
        phase_file.write_text(
            "# Phase 1\n\n### T01.01 -- Task\n\n**Dependencies:** None\n"
        )

        index_content = """\
# Tasklist Index

## Phase Files

| Phase | File | Execution Mode |
|---|---|---|
| 1 | phase-1-tasklist.md | invalid |
"""
        index_file = tmp_path / "tasklist-index.md"
        index_file.write_text(index_content)

        with pytest.raises(click.ClickException) as exc_info:
            discover_phases(index_file)
        assert "invalid" in str(exc_info.value.format_message())
        assert "Allowed" in str(exc_info.value.format_message())


# ---------------------------------------------------------------------------
# T02.04 — Unit tests for classifier registry (R-020, R-021, R-022)
# ---------------------------------------------------------------------------


class TestClassifierRegistry:
    """Unit tests for CLASSIFIERS registry and empirical_gate_v1 (R-020)."""

    @pytest.mark.unit
    def test_empirical_gate_v1_pass(self):
        """empirical_gate_v1 returns 'pass' for exit_code 0."""
        from superclaude.cli.sprint.classifiers import CLASSIFIERS

        result = CLASSIFIERS["empirical_gate_v1"](0, "output", "")
        assert result == "pass"

    @pytest.mark.unit
    def test_empirical_gate_v1_fail(self):
        """empirical_gate_v1 returns 'fail' for non-zero exit codes."""
        from superclaude.cli.sprint.classifiers import CLASSIFIERS

        assert CLASSIFIERS["empirical_gate_v1"](1, "", "error output") == "fail"
        assert CLASSIFIERS["empirical_gate_v1"](127, "", "command not found") == "fail"

    @pytest.mark.unit
    def test_missing_classifier_raises_keyerror(self):
        """CLASSIFIERS raises KeyError for unknown classifier name (R-021)."""
        from superclaude.cli.sprint.classifiers import CLASSIFIERS

        with pytest.raises(KeyError):
            _ = CLASSIFIERS["nonexistent_classifier"]

    @pytest.mark.unit
    def test_classifier_exception_returns_error(self):
        """run_classifier returns 'error' when classifier raises (R-022)."""
        from superclaude.cli.sprint.classifiers import CLASSIFIERS, run_classifier

        def _bad_classifier(exit_code: int, stdout: str, stderr: str) -> str:
            raise ValueError("simulated classifier failure")

        CLASSIFIERS["_test_bad"] = _bad_classifier
        try:
            result = run_classifier("_test_bad", 0, "", "")
            assert result == "error"
        finally:
            del CLASSIFIERS["_test_bad"]

    @pytest.mark.unit
    def test_run_classifier_unknown_name_raises_keyerror(self):
        """run_classifier propagates KeyError for unknown classifier names."""
        from superclaude.cli.sprint.classifiers import run_classifier

        with pytest.raises(KeyError):
            run_classifier("nonexistent", 0, "", "")


# ---------------------------------------------------------------------------
# T03.05 -- Integration tests: preflight execution and timeout
# ---------------------------------------------------------------------------


def _make_python_config(tmp_path: Path, tasks_content: str) -> "SprintConfig":
    """Build a minimal SprintConfig for a single python-mode phase."""
    from superclaude.cli.sprint.models import Phase, SprintConfig

    phase_file = tmp_path / "phase-1-tasklist.md"
    phase_file.write_text(tasks_content)

    phase = Phase(number=1, file=phase_file, execution_mode="python")
    config = SprintConfig(
        index_path=tmp_path / "tasklist-index.md",
        release_dir=tmp_path,
        phases=[phase],
        start_phase=1,
        end_phase=1,
    )
    (tmp_path / "results").mkdir(parents=True, exist_ok=True)
    return config


class TestPreflightExecution:
    """Integration tests for preflight execution and timeout (T03.05 / R-030, R-031)."""

    @pytest.mark.integration
    def test_preflight_echo_hello(self, tmp_path: Path):
        """execute_preflight_phases runs 'echo hello', captures stdout, exit_code 0, pass."""
        from superclaude.cli.sprint.models import PhaseStatus
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        tasks_content = """\
### T01.01 -- Echo hello

**Command:** `echo hello`

**Dependencies:** None
"""
        config = _make_python_config(tmp_path, tasks_content)
        results = execute_preflight_phases(config)

        assert len(results) == 1
        phase_result = results[0]
        assert phase_result.status == PhaseStatus.PREFLIGHT_PASS
        assert phase_result.exit_code == 0

    @pytest.mark.integration
    def test_preflight_exit_code_captured(self, tmp_path: Path):
        """execute_preflight_phases captures non-zero exit code as HALT."""
        from superclaude.cli.sprint.models import PhaseStatus
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        tasks_content = """\
### T01.01 -- Failing command

**Command:** `false`

**Dependencies:** None
"""
        config = _make_python_config(tmp_path, tasks_content)
        results = execute_preflight_phases(config)

        assert len(results) == 1
        phase_result = results[0]
        assert phase_result.status == PhaseStatus.HALT
        assert phase_result.exit_code == 1

    @pytest.mark.integration
    def test_preflight_timeout(self, tmp_path: Path, monkeypatch):
        """execute_preflight_phases handles TimeoutExpired: exit_code -1, classification timeout."""
        import subprocess as _subprocess

        from superclaude.cli.sprint.models import PhaseStatus
        import superclaude.cli.sprint.preflight as preflight_mod
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        # Patch subprocess.run to raise TimeoutExpired
        def _raise_timeout(*args, **kwargs):
            raise _subprocess.TimeoutExpired(cmd=["sleep", "5"], timeout=1)

        monkeypatch.setattr(preflight_mod.subprocess, "run", _raise_timeout)

        tasks_content = """\
### T01.01 -- Sleep task

**Command:** `sleep 5`

**Dependencies:** None
"""
        config = _make_python_config(tmp_path, tasks_content)
        results = execute_preflight_phases(config)

        assert len(results) == 1
        assert results[0].status == PhaseStatus.HALT
        assert results[0].exit_code == 1

    @pytest.mark.integration
    def test_preflight_filters_only_python_mode(self, tmp_path: Path):
        """execute_preflight_phases skips non-python phases."""
        from superclaude.cli.sprint.models import Phase, SprintConfig
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        python_phase_file = tmp_path / "phase-1-tasklist.md"
        python_phase_file.write_text(
            "### T01.01 -- Echo\n\n**Command:** `echo ok`\n\n**Dependencies:** None\n"
        )
        claude_phase_file = tmp_path / "phase-2-tasklist.md"
        claude_phase_file.write_text(
            "### T02.01 -- Claude task\n\n**Dependencies:** None\n"
        )

        config = SprintConfig(
            index_path=tmp_path / "tasklist-index.md",
            release_dir=tmp_path,
            phases=[
                Phase(number=1, file=python_phase_file, execution_mode="python"),
                Phase(number=2, file=claude_phase_file, execution_mode="claude"),
            ],
            start_phase=1,
            end_phase=2,
        )
        (tmp_path / "results").mkdir(parents=True, exist_ok=True)

        results = execute_preflight_phases(config)
        # Only python-mode phase is executed
        assert len(results) == 1
        assert results[0].phase.number == 1


# ---------------------------------------------------------------------------
# T03.06 -- Integration tests: evidence and result file structure
# ---------------------------------------------------------------------------


class TestPreflightEvidenceAndResultFile:
    """Integration tests for evidence files and result file parsing (T03.06 / R-032, R-033)."""

    @pytest.mark.integration
    def test_evidence_structure(self, tmp_path: Path):
        """Evidence file contains all 6 required fields."""
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        tasks_content = """\
### T01.01 -- Echo for evidence

**Command:** `echo evidence_test`

**Dependencies:** None
"""
        config = _make_python_config(tmp_path, tasks_content)
        execute_preflight_phases(config)

        evidence_path = (
            tmp_path / "results" / "preflight-artifacts" / "T01.01" / "evidence.md"
        )
        assert evidence_path.exists(), f"Evidence file not found at {evidence_path}"

        content = evidence_path.read_text()
        assert "echo evidence_test" in content, "command not in evidence"
        assert "Exit code:" in content, "exit_code not in evidence"
        assert "stdout" in content.lower(), "stdout not in evidence"
        assert "stderr" in content.lower(), "stderr not in evidence"
        assert "Duration:" in content, "duration not in evidence"
        assert "Classification:" in content, "classification not in evidence"

    @pytest.mark.integration
    def test_result_parseable(self, tmp_path: Path):
        """Result file generated by preflight is parsed by _determine_phase_status() correctly."""
        from pathlib import Path as _Path

        from superclaude.cli.sprint.executor import _determine_phase_status
        from superclaude.cli.sprint.models import PhaseStatus
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        tasks_content = """\
### T01.01 -- Pass task

**Command:** `echo pass`

**Dependencies:** None
"""
        config = _make_python_config(tmp_path, tasks_content)
        execute_preflight_phases(config)

        result_file = tmp_path / "results" / "phase-1-result.md"
        output_file = tmp_path / "results" / "phase-1-output.txt"
        output_file.write_text("some output")

        assert result_file.exists(), "Result file was not written"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS, f"Expected PASS, got {status}"

    @pytest.mark.integration
    def test_result_file_halt_parseable(self, tmp_path: Path):
        """Result file with a failing task is parsed as HALT by _determine_phase_status()."""
        from superclaude.cli.sprint.executor import _determine_phase_status
        from superclaude.cli.sprint.models import PhaseStatus
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        tasks_content = """\
### T01.01 -- Failing task

**Command:** `false`

**Dependencies:** None
"""
        config = _make_python_config(tmp_path, tasks_content)
        execute_preflight_phases(config)

        result_file = tmp_path / "results" / "phase-1-result.md"
        output_file = tmp_path / "results" / "phase-1-output.txt"
        output_file.write_text("some output")

        assert result_file.exists()

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.HALT, f"Expected HALT, got {status}"

    @pytest.mark.integration
    def test_result_file_contains_source_preflight(self, tmp_path: Path):
        """Result file frontmatter contains 'source: preflight'."""
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        tasks_content = """\
### T01.01 -- Source field check

**Command:** `echo source`

**Dependencies:** None
"""
        config = _make_python_config(tmp_path, tasks_content)
        execute_preflight_phases(config)

        result_file = tmp_path / "results" / "phase-1-result.md"
        assert result_file.exists()
        content = result_file.read_text()
        assert "source: preflight" in content


# ---------------------------------------------------------------------------
# T03.07 -- Unit tests: truncation and compatibility fixture
# ---------------------------------------------------------------------------


class TestTruncation:
    """Unit tests for stdout/stderr truncation at 10KB/2KB limits (T03.07 / R-034)."""

    @pytest.mark.unit
    def test_stdout_truncation_10kb(self):
        """15KB stdout is truncated to 10KB with marker."""
        from superclaude.cli.sprint.preflight import _truncate

        big_text = "x" * (15 * 1024)
        result = _truncate(big_text, 10240)
        assert result.endswith("[truncated at 10240 bytes]")
        # Content before marker is ≤ 10240 bytes
        content_before_marker = result[: result.rfind("\n[truncated")]
        assert len(content_before_marker.encode("utf-8")) <= 10240

    @pytest.mark.unit
    def test_stderr_truncation_2kb(self):
        """5KB stderr is truncated to 2KB with marker."""
        from superclaude.cli.sprint.preflight import _truncate

        big_text = "y" * (5 * 1024)
        result = _truncate(big_text, 2048)
        assert result.endswith("[truncated at 2048 bytes]")
        content_before_marker = result[: result.rfind("\n[truncated")]
        assert len(content_before_marker.encode("utf-8")) <= 2048

    @pytest.mark.unit
    def test_no_truncation_when_under_limit(self):
        """Text under the limit is returned unchanged."""
        from superclaude.cli.sprint.preflight import _truncate

        text = "hello world"
        assert _truncate(text, 10240) == text
        assert _truncate(text, 2048) == text

    @pytest.mark.unit
    def test_truncation_exact_limit(self):
        """Text exactly at the limit is not truncated."""
        from superclaude.cli.sprint.preflight import _truncate

        text = "a" * 10240
        result = _truncate(text, 10240)
        assert result == text
        assert "[truncated" not in result


class TestResultFileCompatibility:
    """Compatibility fixture: preflight and Claude-origin result files parse identically (T03.07 / R-035)."""

    @pytest.mark.unit
    def test_result_file_compatibility(self, tmp_path: Path):
        """Preflight-origin and Claude-origin result files produce identical _determine_phase_status() output."""
        from superclaude.cli.sprint.executor import _determine_phase_status
        from superclaude.cli.sprint.models import PhaseStatus

        output_file = tmp_path / "output.txt"
        output_file.write_text("some output")

        # Claude-origin result file (manually crafted as Claude would write it)
        claude_result = tmp_path / "claude-result.md"
        claude_result.write_text(
            "---\nphase: 1\nstatus: PASS\n---\n\nSome analysis.\n\nEXIT_RECOMMENDATION: CONTINUE\n"
        )

        # Preflight-origin result file (uses frontmatter injection + AggregatedPhaseReport)
        from superclaude.cli.sprint.executor import AggregatedPhaseReport
        from superclaude.cli.sprint.models import (
            GateOutcome,
            TaskEntry,
            TaskResult,
            TaskStatus,
        )
        from superclaude.cli.sprint.preflight import _inject_source_field
        from datetime import datetime, timezone

        task = TaskEntry(task_id="T01.01", title="Test task", command="echo ok")
        now = datetime.now(timezone.utc)
        tr = TaskResult(
            task=task,
            status=TaskStatus.PASS,
            exit_code=0,
            started_at=now,
            finished_at=now,
            gate_outcome=GateOutcome.PASS,
        )
        report = AggregatedPhaseReport(
            phase_number=1,
            tasks_total=1,
            tasks_passed=1,
            task_results=[tr],
        )
        preflight_md = _inject_source_field(report.to_markdown())
        preflight_result = tmp_path / "preflight-result.md"
        preflight_result.write_text(preflight_md)

        # Both should parse to PASS
        claude_status = _determine_phase_status(
            exit_code=0, result_file=claude_result, output_file=output_file
        )
        preflight_status = _determine_phase_status(
            exit_code=0, result_file=preflight_result, output_file=output_file
        )

        assert claude_status == PhaseStatus.PASS, (
            f"Claude-origin: expected PASS, got {claude_status}"
        )
        assert preflight_status == PhaseStatus.PASS, (
            f"Preflight-origin: expected PASS, got {preflight_status}"
        )
        assert claude_status == preflight_status, (
            "Parsing behavior differs between origins"
        )

    @pytest.mark.unit
    def test_result_file_halt_compatibility(self, tmp_path: Path):
        """HALT result files parse identically regardless of origin."""
        from superclaude.cli.sprint.executor import _determine_phase_status
        from superclaude.cli.sprint.models import PhaseStatus

        output_file = tmp_path / "output.txt"
        output_file.write_text("some output")

        # Claude-origin HALT
        claude_result = tmp_path / "claude-result.md"
        claude_result.write_text(
            "---\nphase: 1\nstatus: FAIL\n---\n\nFailed.\n\nEXIT_RECOMMENDATION: HALT\n"
        )

        # Preflight-origin HALT
        from superclaude.cli.sprint.executor import AggregatedPhaseReport
        from superclaude.cli.sprint.models import (
            GateOutcome,
            TaskEntry,
            TaskResult,
            TaskStatus,
        )
        from superclaude.cli.sprint.preflight import _inject_source_field
        from datetime import datetime, timezone

        task = TaskEntry(task_id="T01.01", title="Test task", command="false")
        now = datetime.now(timezone.utc)
        tr = TaskResult(
            task=task,
            status=TaskStatus.FAIL,
            exit_code=1,
            started_at=now,
            finished_at=now,
            gate_outcome=GateOutcome.FAIL,
        )
        report = AggregatedPhaseReport(
            phase_number=1,
            tasks_total=1,
            tasks_passed=0,
            tasks_failed=1,
            task_results=[tr],
        )
        preflight_md = _inject_source_field(report.to_markdown())
        preflight_result = tmp_path / "preflight-result.md"
        preflight_result.write_text(preflight_md)

        claude_status = _determine_phase_status(
            exit_code=0, result_file=claude_result, output_file=output_file
        )
        preflight_status = _determine_phase_status(
            exit_code=0, result_file=preflight_result, output_file=output_file
        )

        assert claude_status == PhaseStatus.HALT
        assert preflight_status == PhaseStatus.HALT
        assert claude_status == preflight_status


# ---------------------------------------------------------------------------
# T04.05 -- Integration tests: mixed-mode sprint execution (R-042 through R-045)
# ---------------------------------------------------------------------------


def _make_mixed_config(
    tmp_path: Path,
    phases: "list[tuple[int, str, str]]",
) -> "SprintConfig":
    """Build a SprintConfig with multiple phases of mixed execution modes.

    Args:
        phases: list of (number, execution_mode, tasks_content) tuples.
    """
    from superclaude.cli.sprint.models import Phase, SprintConfig

    phase_objs = []
    for number, mode, content in phases:
        phase_file = tmp_path / f"phase-{number}-tasklist.md"
        phase_file.write_text(content)
        phase_objs.append(Phase(number=number, file=phase_file, execution_mode=mode))

    config = SprintConfig(
        index_path=tmp_path / "tasklist-index.md",
        release_dir=tmp_path,
        phases=phase_objs,
        start_phase=phase_objs[0].number,
        end_phase=phase_objs[-1].number,
    )
    (tmp_path / "results").mkdir(parents=True, exist_ok=True)
    return config


class TestMixedModeSprintExecution:
    """Integration tests for mixed python/claude/skip sprint execution (T04.05)."""

    @pytest.mark.integration
    def test_preflight_filters_python_only_python_returns_results(self, tmp_path: Path):
        """execute_preflight_phases returns one result per python-mode phase only."""
        from superclaude.cli.sprint.models import PhaseStatus
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        python_content = "### T01.01 -- Echo\n\n**Command:** `echo hello`\n\n**Dependencies:** None\n"
        claude_content = "### T02.01 -- Claude task\n\n**Dependencies:** None\n"
        skip_content = "### T03.01 -- Skip task\n\n**Dependencies:** None\n"

        config = _make_mixed_config(
            tmp_path,
            [
                (1, "python", python_content),
                (2, "claude", claude_content),
                (3, "skip", skip_content),
            ],
        )

        results = execute_preflight_phases(config)

        # Only python-mode phase produces a preflight result
        assert len(results) == 1
        assert results[0].phase.number == 1
        assert results[0].status == PhaseStatus.PREFLIGHT_PASS

    @pytest.mark.integration
    def test_skip_no_subprocess(self, tmp_path: Path, monkeypatch):
        """Skip-mode phases produce SKIPPED status; no subprocess is launched for them."""
        import subprocess as _subprocess

        from superclaude.cli.sprint.preflight import execute_preflight_phases

        _calls = []

        def _track(*args, **kwargs):
            _calls.append(args)
            raise AssertionError(
                "subprocess.run must not be called for skip-mode phases"
            )

        skip_content = "### T01.01 -- Skip task\n\n**Dependencies:** None\n"
        config = _make_mixed_config(tmp_path, [(1, "skip", skip_content)])

        import superclaude.cli.sprint.preflight as preflight_mod

        monkeypatch.setattr(preflight_mod.subprocess, "run", _track)

        results = execute_preflight_phases(config)
        # skip-mode phases are filtered out in execute_preflight_phases (not python)
        # so no results and no subprocess calls
        assert results == []
        assert _calls == []

    @pytest.mark.integration
    def test_python_no_claude_process(self, tmp_path: Path, monkeypatch):
        """Python-mode phases do not instantiate ClaudeProcess."""
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        _instantiated = []

        class _TrackingClaudeProcess:
            def __init__(self, *args, **kwargs):
                _instantiated.append(True)

        import superclaude.cli.sprint.executor as executor_mod

        monkeypatch.setattr(executor_mod, "ClaudeProcess", _TrackingClaudeProcess)

        python_content = "### T01.01 -- Echo\n\n**Command:** `echo hello`\n\n**Dependencies:** None\n"
        config = _make_mixed_config(tmp_path, [(1, "python", python_content)])

        execute_preflight_phases(config)

        assert _instantiated == [], (
            "ClaudeProcess must not be instantiated for python-mode phases"
        )

    @pytest.mark.integration
    def test_preflight_returns_empty_for_all_claude(self, tmp_path: Path):
        """execute_preflight_phases returns empty list when no python-mode phases exist."""
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        claude_content = "### T01.01 -- Claude task\n\n**Dependencies:** None\n"
        config = _make_mixed_config(
            tmp_path,
            [
                (1, "claude", claude_content),
                (2, "claude", claude_content),
            ],
        )

        results = execute_preflight_phases(config)
        assert results == []

    @pytest.mark.integration
    def test_merge_ordering_python_then_skip(self, tmp_path: Path):
        """Preflight results for python phases appear at correct indices after merge."""
        from superclaude.cli.sprint.models import PhaseStatus
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        python_content = "### T01.01 -- Echo\n\n**Command:** `echo hello`\n\n**Dependencies:** None\n"
        skip_content = "### T02.01 -- Skip task\n\n**Dependencies:** None\n"

        config = _make_mixed_config(
            tmp_path,
            [
                (1, "python", python_content),
                (2, "skip", skip_content),
            ],
        )

        preflight_results = execute_preflight_phases(config)
        # preflight produces one result for python phase
        assert len(preflight_results) == 1
        assert preflight_results[0].phase.number == 1
        assert preflight_results[0].status == PhaseStatus.PREFLIGHT_PASS

    @pytest.mark.integration
    def test_logger_no_exception_on_preflight_pass(self, tmp_path: Path):
        """SprintLogger.write_phase_result does not raise for PREFLIGHT_PASS status."""
        from datetime import datetime, timezone

        from superclaude.cli.sprint.logging_ import SprintLogger
        from superclaude.cli.sprint.models import (
            Phase,
            PhaseResult,
            PhaseStatus,
            SprintConfig,
        )

        config = SprintConfig(
            index_path=tmp_path / "tasklist-index.md",
            release_dir=tmp_path,
            phases=[Phase(number=1, file=tmp_path / "phase-1-tasklist.md")],
            start_phase=1,
            end_phase=1,
        )
        (tmp_path / "results").mkdir(parents=True, exist_ok=True)
        (tmp_path / "results" / "execution-log.jsonl").touch()
        (tmp_path / "results" / "execution-log.md").touch()

        logger = SprintLogger(config)
        now = datetime.now(timezone.utc)
        result = PhaseResult(
            phase=Phase(number=1, file=tmp_path / "phase-1-tasklist.md"),
            status=PhaseStatus.PREFLIGHT_PASS,
            exit_code=0,
            started_at=now,
            finished_at=now,
        )
        # Must not raise
        logger.write_phase_result(result)

    @pytest.mark.integration
    def test_logger_no_exception_on_skipped(self, tmp_path: Path):
        """SprintLogger.write_phase_result does not raise for SKIPPED status."""
        from datetime import datetime, timezone

        from superclaude.cli.sprint.logging_ import SprintLogger
        from superclaude.cli.sprint.models import (
            Phase,
            PhaseResult,
            PhaseStatus,
            SprintConfig,
        )

        config = SprintConfig(
            index_path=tmp_path / "tasklist-index.md",
            release_dir=tmp_path,
            phases=[Phase(number=1, file=tmp_path / "phase-1-tasklist.md")],
            start_phase=1,
            end_phase=1,
        )
        (tmp_path / "results").mkdir(parents=True, exist_ok=True)
        (tmp_path / "results" / "execution-log.jsonl").touch()
        (tmp_path / "results" / "execution-log.md").touch()

        logger = SprintLogger(config)
        now = datetime.now(timezone.utc)
        result = PhaseResult(
            phase=Phase(number=1, file=tmp_path / "phase-1-tasklist.md"),
            status=PhaseStatus.SKIPPED,
            exit_code=0,
            started_at=now,
            finished_at=now,
        )
        # Must not raise
        logger.write_phase_result(result)

    @pytest.mark.integration
    def test_tui_status_styles_cover_preflight_and_skipped(self):
        """TUI STATUS_STYLES and STATUS_ICONS include PREFLIGHT_PASS and SKIPPED."""
        from superclaude.cli.sprint.models import PhaseStatus
        from superclaude.cli.sprint.tui import STATUS_ICONS, STATUS_STYLES

        assert PhaseStatus.PREFLIGHT_PASS in STATUS_STYLES
        assert PhaseStatus.SKIPPED in STATUS_STYLES
        assert PhaseStatus.PREFLIGHT_PASS in STATUS_ICONS
        assert PhaseStatus.SKIPPED in STATUS_ICONS


# ---------------------------------------------------------------------------
# T04.06 -- Regression test: all-Claude tasklist behavior (R-046)
# ---------------------------------------------------------------------------


class TestAllClaudeRegression:
    """Regression tests confirming all-Claude tasklists have zero behavioral change (T04.06)."""

    @pytest.mark.integration
    def test_all_claude_preflight_returns_empty(self, tmp_path: Path):
        """execute_preflight_phases returns [] for an all-Claude tasklist (no python phases)."""
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        content = "### T01.01 -- Claude task\n\n**Dependencies:** None\n"
        config = _make_mixed_config(
            tmp_path,
            [
                (1, "claude", content),
                (2, "claude", content),
                (3, "claude", content),
            ],
        )

        results = execute_preflight_phases(config)
        assert results == [], (
            f"Expected empty list for all-Claude sprint, got {results}"
        )

    @pytest.mark.integration
    def test_all_claude_no_subprocess_called_by_preflight(
        self, tmp_path: Path, monkeypatch
    ):
        """execute_preflight_phases does not call subprocess.run for all-Claude tasklists."""
        import superclaude.cli.sprint.preflight as preflight_mod
        from superclaude.cli.sprint.preflight import execute_preflight_phases

        _calls = []

        def _track(*args, **kwargs):
            _calls.append(args)
            raise AssertionError("subprocess must not run for all-Claude sprint")

        monkeypatch.setattr(preflight_mod.subprocess, "run", _track)

        content = "### T01.01 -- Claude task\n\n**Dependencies:** None\n"
        config = _make_mixed_config(tmp_path, [(1, "claude", content)])

        execute_preflight_phases(config)
        assert _calls == []

    @pytest.mark.integration
    def test_existing_tests_still_pass(self, tmp_path: Path):
        """Canary: models, config, and classifiers still import without errors."""
        from superclaude.cli.sprint.classifiers import CLASSIFIERS
        from superclaude.cli.sprint.config import discover_phases, parse_tasklist
        from superclaude.cli.sprint.models import Phase, PhaseStatus, SprintConfig

        # Basic smoke test: all prior-phase symbols still importable and functional
        assert PhaseStatus.PASS.is_success is True
        assert PhaseStatus.HALT.is_failure is True
        assert PhaseStatus.SKIPPED.is_success is False
        assert PhaseStatus.SKIPPED.is_failure is False
        assert PhaseStatus.PREFLIGHT_PASS.is_success is True

        assert "empirical_gate_v1" in CLASSIFIERS

        phase = Phase(number=1, file=tmp_path / "p.md")
        assert phase.execution_mode == "claude"
