"""TUI v2 Wave 1 (v3.7) — signal extraction and pre-scan tests.

Verifies the structured stream-json extraction added in Wave 1:
- F1 activity log (tool_use blocks → ring buffer, tool-name shortening)
- F2 turn counting (each assistant event increments)
- F4 error detection (is_error flag and Bash exit_code parsing)
- F5 last assistant text (tail of last text block)
- F6 token accumulation (input/output tokens summed per turn)
- SprintConfig.total_tasks pre-scan in load_sprint_config
- Monitor.reset(phase_file=...) populates total_tasks_in_phase
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.config import count_tasks_in_file, load_sprint_config
from superclaude.cli.sprint.monitor import (
    ACTIVITY_LOG_MAX,
    ASSISTANT_TEXT_MAX_LEN,
    ERRORS_MAX,
    OutputMonitor,
    _condense_tool_input,
    _flatten_tool_result_content,
    _has_nonzero_exit_code,
    _shorten_tool_name,
)

# ---------------------------------------------------------------------------
# Helpers for building the stream-json events the monitor consumes
# ---------------------------------------------------------------------------


def _assistant_event(
    *,
    text: str | None = None,
    tool_uses: list[dict] | None = None,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> dict:
    content: list[dict] = []
    if text is not None:
        content.append({"type": "text", "text": text})
    for tu in tool_uses or []:
        content.append({"type": "tool_use", **tu})
    return {
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": content,
            "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
        },
    }


def _tool_result_event(content: object, is_error: bool = False) -> dict:
    return {
        "type": "user",
        "message": {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_1",
                    "content": content,
                    "is_error": is_error,
                }
            ],
        },
    }


def _build_monitor(tmp_path: Path) -> OutputMonitor:
    out = tmp_path / "output.txt"
    out.write_text("")
    return OutputMonitor(out, poll_interval=0.1)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


class TestHelperFunctions:
    def test_shorten_known_tool(self):
        assert _shorten_tool_name("TodoWrite") == "Todo"
        assert _shorten_tool_name("MultiEdit") == "Multi"

    def test_shorten_unknown_tool_passthrough(self):
        assert _shorten_tool_name("Read") == "Read"
        assert _shorten_tool_name("CustomTool") == "CustomTool"

    def test_condense_read_uses_file_path(self):
        summary = _condense_tool_input("Read", {"file_path": "/a/b/c.py"})
        assert summary == "/a/b/c.py"

    def test_condense_bash_prefers_description(self):
        summary = _condense_tool_input(
            "Bash",
            {"command": "pytest -x", "description": "Run tests"},
        )
        assert summary == "Run tests"

    def test_condense_truncates_long(self):
        long = "x" * 200
        summary = _condense_tool_input("Read", {"file_path": long})
        assert len(summary) == 60

    def test_condense_no_dict_returns_empty(self):
        assert _condense_tool_input("Read", None) == ""

    def test_flatten_string(self):
        assert _flatten_tool_result_content("hello") == "hello"

    def test_flatten_list_of_text_blocks(self):
        raw = [{"type": "text", "text": "line 1"}, {"type": "text", "text": "line 2"}]
        assert _flatten_tool_result_content(raw) == "line 1 line 2"

    def test_flatten_other_returns_empty(self):
        assert _flatten_tool_result_content(42) == ""

    def test_has_nonzero_exit_code(self):
        assert _has_nonzero_exit_code("exit_code: 1 something") is True
        assert _has_nonzero_exit_code('"exit_code": 127') is True

    def test_zero_exit_code_not_flagged(self):
        assert _has_nonzero_exit_code("exit_code: 0") is False
        assert _has_nonzero_exit_code("no such token here") is False


# ---------------------------------------------------------------------------
# Monitor.reset with phase_file (TUI-Q4)
# ---------------------------------------------------------------------------


class TestMonitorResetWithPhaseFile:
    def test_reset_without_phase_file_is_zero(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        out2 = tmp_path / "other.txt"
        out2.write_text("")
        monitor.reset(out2)
        assert monitor.state.total_tasks_in_phase == 0

    def test_reset_with_phase_file_counts_tasks(self, tmp_path):
        phase_file = tmp_path / "phase-1-tasklist.md"
        phase_file.write_text(
            "# Phase 1\n\n### T01.01 -- First\n\nbody\n\n### T01.02 -- Second\n\n"
            "### T01.03 -- Third\n\n"
        )
        monitor = _build_monitor(tmp_path)
        out2 = tmp_path / "out2.txt"
        out2.write_text("")
        monitor.reset(out2, phase_file=phase_file)
        assert monitor.state.total_tasks_in_phase == 3

    def test_reset_missing_phase_file_falls_back_to_zero(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        out2 = tmp_path / "out2.txt"
        out2.write_text("")
        monitor.reset(out2, phase_file=tmp_path / "missing.md")
        assert monitor.state.total_tasks_in_phase == 0

    def test_reset_clears_wave1_fields(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor.state.turns = 99
        monitor.state.tokens_in = 500
        monitor.state.errors.append(("T01.01", "Bash", "boom"))
        out2 = tmp_path / "out2.txt"
        out2.write_text("")
        monitor.reset(out2)
        assert monitor.state.turns == 0
        assert monitor.state.tokens_in == 0
        assert monitor.state.errors == []


# ---------------------------------------------------------------------------
# F2 turn counting and F6 token accumulation
# ---------------------------------------------------------------------------


class TestTurnAndTokenExtraction:
    def test_single_assistant_event_counts_one_turn(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(_assistant_event(text="hello"))
        assert monitor.state.turns == 1

    def test_multiple_assistant_events_sum(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        for _ in range(5):
            monitor._extract_signals_from_event(_assistant_event(text="t"))
        assert monitor.state.turns == 5

    def test_tokens_accumulate(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(
            _assistant_event(input_tokens=100, output_tokens=50)
        )
        monitor._extract_signals_from_event(
            _assistant_event(input_tokens=200, output_tokens=75)
        )
        assert monitor.state.tokens_in == 300
        assert monitor.state.tokens_out == 125

    def test_missing_usage_does_not_crash(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        bad = {"type": "assistant", "message": {"content": [{"type": "text", "text": "hi"}]}}
        monitor._extract_signals_from_event(bad)
        assert monitor.state.turns == 1
        assert monitor.state.tokens_in == 0

    def test_user_event_does_not_count_as_turn(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(_tool_result_event("ok"))
        assert monitor.state.turns == 0


# ---------------------------------------------------------------------------
# F5 last_assistant_text extraction
# ---------------------------------------------------------------------------


class TestLastAssistantText:
    def test_text_captured(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(_assistant_event(text="Hello world"))
        assert monitor.state.last_assistant_text == "Hello world"

    def test_later_text_overrides_earlier(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(_assistant_event(text="first"))
        monitor._extract_signals_from_event(_assistant_event(text="second"))
        assert monitor.state.last_assistant_text == "second"

    def test_long_text_truncated_to_tail(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        long = "A" * 200 + "END"
        monitor._extract_signals_from_event(_assistant_event(text=long))
        assert len(monitor.state.last_assistant_text) == ASSISTANT_TEXT_MAX_LEN
        assert monitor.state.last_assistant_text.endswith("END")

    def test_whitespace_only_text_ignored(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(_assistant_event(text="real text"))
        monitor._extract_signals_from_event(_assistant_event(text="   \n  "))
        assert monitor.state.last_assistant_text == "real text"


# ---------------------------------------------------------------------------
# F1 activity log (ring buffer + shortening)
# ---------------------------------------------------------------------------


class TestActivityLog:
    def test_tool_use_appended(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(
            _assistant_event(
                tool_uses=[{"name": "Read", "input": {"file_path": "foo.py"}}]
            )
        )
        assert len(monitor.state.activity_log) == 1
        ts, name, desc = monitor.state.activity_log[0]
        assert name == "Read"
        assert desc == "foo.py"
        assert isinstance(ts, float)

    def test_tool_name_shortened(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(
            _assistant_event(tool_uses=[{"name": "TodoWrite", "input": {}}])
        )
        assert monitor.state.activity_log[-1][1] == "Todo"

    def test_ring_buffer_capped(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        for i in range(ACTIVITY_LOG_MAX + 3):
            monitor._extract_signals_from_event(
                _assistant_event(
                    tool_uses=[{"name": "Read", "input": {"file_path": f"f{i}.py"}}]
                )
            )
        assert len(monitor.state.activity_log) == ACTIVITY_LOG_MAX
        # Last entry wins — oldest dropped.
        assert monitor.state.activity_log[-1][2].endswith(
            f"f{ACTIVITY_LOG_MAX + 2}.py"
        )

    def test_last_tool_used_set_from_structured(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(
            _assistant_event(tool_uses=[{"name": "Bash", "input": {"command": "ls"}}])
        )
        assert monitor.state.last_tool_used == "Bash"


# ---------------------------------------------------------------------------
# F4 error extraction
# ---------------------------------------------------------------------------


class TestErrorExtraction:
    def test_is_error_true_recorded(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        # Seed context so attribution is non-empty.
        monitor.state.last_task_id = "T01.02"
        monitor.state.last_tool_used = "Read"
        monitor._extract_signals_from_event(
            _tool_result_event("File not found", is_error=True)
        )
        assert len(monitor.state.errors) == 1
        task, tool, msg = monitor.state.errors[0]
        assert task == "T01.02"
        assert tool == "Read"
        assert "File not found" in msg

    def test_is_error_false_not_recorded(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(_tool_result_event("ok", is_error=False))
        assert monitor.state.errors == []

    def test_bash_exit_code_triggers_error(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(
            _tool_result_event("command failed, exit_code: 127", is_error=False)
        )
        assert len(monitor.state.errors) == 1

    def test_zero_exit_code_not_error(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        monitor._extract_signals_from_event(
            _tool_result_event("done; exit_code: 0", is_error=False)
        )
        assert monitor.state.errors == []

    def test_error_ring_buffer_capped(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        for i in range(ERRORS_MAX + 5):
            monitor._extract_signals_from_event(
                _tool_result_event(f"err {i}", is_error=True)
            )
        assert len(monitor.state.errors) == ERRORS_MAX

    def test_list_content_flattened(self, tmp_path):
        monitor = _build_monitor(tmp_path)
        payload = [
            {"type": "text", "text": "line 1"},
            {"type": "text", "text": "line 2"},
        ]
        monitor._extract_signals_from_event(
            _tool_result_event(payload, is_error=True)
        )
        _, _, msg = monitor.state.errors[0]
        assert "line 1" in msg and "line 2" in msg


# ---------------------------------------------------------------------------
# count_tasks_in_file + load_sprint_config total_tasks
# ---------------------------------------------------------------------------


class TestCountTasksInFile:
    def test_matches_task_headings(self, tmp_path):
        p = tmp_path / "phase-1-tasklist.md"
        p.write_text(
            "# Phase 1\n\n"
            "### T01.01 -- First\n\n"
            "### T01.02 -- Second\n\n"
            "### Not a task\n\n"
            "### T01.10 -- Third\n"
        )
        assert count_tasks_in_file(p) == 3

    def test_missing_file_returns_zero(self, tmp_path):
        assert count_tasks_in_file(tmp_path / "nope.md") == 0

    def test_empty_file_returns_zero(self, tmp_path):
        p = tmp_path / "empty.md"
        p.write_text("")
        assert count_tasks_in_file(p) == 0


class TestLoadSprintConfigTotalTasks:
    def _write_phase(self, tmp_path: Path, num: int, task_count: int) -> Path:
        pf = tmp_path / f"phase-{num}-tasklist.md"
        body = [f"# Phase {num}", ""]
        for t in range(1, task_count + 1):
            body.append(f"### T0{num}.0{t} -- Task {t}\n\nbody\n")
        pf.write_text("\n".join(body))
        return pf

    def test_total_tasks_sums_active_phases(self, tmp_path):
        self._write_phase(tmp_path, 1, task_count=3)
        self._write_phase(tmp_path, 2, task_count=5)
        index = tmp_path / "tasklist-index.md"
        index.write_text(
            "| # | File |\n|---|------|\n"
            "| 1 | phase-1-tasklist.md |\n"
            "| 2 | phase-2-tasklist.md |\n"
        )

        config = load_sprint_config(index)
        assert config.total_tasks == 8

    def test_total_tasks_respects_start_end(self, tmp_path):
        self._write_phase(tmp_path, 1, task_count=3)
        self._write_phase(tmp_path, 2, task_count=5)
        self._write_phase(tmp_path, 3, task_count=7)
        index = tmp_path / "tasklist-index.md"
        index.write_text(
            "| # | File |\n|---|------|\n"
            "| 1 | phase-1-tasklist.md |\n"
            "| 2 | phase-2-tasklist.md |\n"
            "| 3 | phase-3-tasklist.md |\n"
        )

        config = load_sprint_config(index, start_phase=2, end_phase=3)
        # Only phases 2 + 3 are active → 5 + 7 = 12.
        assert config.total_tasks == 12
