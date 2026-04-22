"""TUI v2 Wave 2 (v3.7) — rendering tests.

Covers the visual refactor:
- F1: 3-line activity stream + thinking indicator
- F2: enhanced phase table (Turns, Output columns; no Tasks)
- F3: dual block-char progress bar (phases + tasks)
- F4: conditional error panel (hidden when empty; overflow marker)
- F5: Prompt / Agent LLM context lines
- F6: enhanced terminal panels (success + halt) + _format_tokens
- F7: sprint name in the outer panel title
- Cross-domain: PASS_MISSING_CHECKPOINT renders without crashing.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from io import StringIO
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from superclaude.cli.sprint.models import (
    MonitorState,
    Phase,
    PhaseResult,
    PhaseStatus,
    SprintConfig,
    SprintOutcome,
    SprintResult,
)
from superclaude.cli.sprint.tui import (
    SprintTUI,
    _format_bytes,
    _format_timestamp,
    _format_tokens,
    _render_bar,
    _render_percent,
    _truncate,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_config(
    *,
    release_dir: Path = Path("/tmp/release"),
    total_tasks: int = 0,
    grace_period: int = 0,
    phases: list[Phase] | None = None,
) -> SprintConfig:
    if phases is None:
        phases = [
            Phase(
                number=1,
                file=Path("/tmp/p1.md"),
                name="Foundation",
                prompt_preview="Lay the foundation for the data model",
            ),
            Phase(
                number=2,
                file=Path("/tmp/p2.md"),
                name="Backend",
                prompt_preview="Wire up backend endpoints",
            ),
        ]
    return SprintConfig(
        index_path=Path("/tmp/tasklist-index.md"),
        release_dir=release_dir,
        phases=phases,
        grace_period=grace_period,
        total_tasks=total_tasks,
    )


def _render_to_string(tui: SprintTUI) -> str:
    output = StringIO()
    # Generous width prevents Rich's soft-wrap from splitting our marker strings.
    console = Console(file=output, width=160, force_terminal=True)
    console.print(tui._render())
    return output.getvalue()


def _make_phase_result(**kwargs) -> PhaseResult:
    now = datetime.now(timezone.utc)
    defaults = dict(
        phase=Phase(number=1, file=Path("/tmp/p1.md")),
        status=PhaseStatus.PASS,
        started_at=now - timedelta(seconds=30),
        finished_at=now,
    )
    defaults.update(kwargs)
    return PhaseResult(**defaults)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


class TestFormatHelpers:
    def test_format_tokens_small(self):
        assert _format_tokens(0) == "0"
        assert _format_tokens(999) == "999"

    def test_format_tokens_k(self):
        assert _format_tokens(1_500) == "1.5K"
        assert _format_tokens(999_999).endswith("K")

    def test_format_tokens_m(self):
        assert _format_tokens(2_500_000) == "2.5M"

    def test_format_tokens_negative_clamps(self):
        assert _format_tokens(-5) == "0"

    def test_format_bytes_b_kb_mb(self):
        assert _format_bytes(512) == "512 B"
        assert _format_bytes(2048) == "2.0 KB"
        assert _format_bytes(2 * 1024 * 1024) == "2.0 MB"

    def test_render_bar_empty_on_zero_total(self):
        bar = _render_bar(10, 0, 0)
        assert bar == "░" * 10

    def test_render_bar_half_filled(self):
        bar = _render_bar(10, 5, 10)
        assert bar.count("█") == 5
        assert bar.count("░") == 5

    def test_render_bar_full(self):
        assert _render_bar(10, 10, 10) == "█" * 10

    def test_render_bar_over_cap(self):
        # done > total clamps to full
        assert _render_bar(10, 99, 10) == "█" * 10

    def test_render_percent(self):
        assert _render_percent(0, 0) == "  0%"
        assert _render_percent(1, 4).strip() == "25%"
        assert _render_percent(10, 10).strip() == "100%"

    def test_truncate(self):
        assert _truncate("hello", 10) == "hello"
        assert _truncate("hello world", 8) == "hello..."
        assert _truncate("", 8) == ""

    def test_format_timestamp_shape(self):
        stamp = _format_timestamp(time.time())
        assert len(stamp) == 8 and stamp.count(":") == 2


# ---------------------------------------------------------------------------
# F7 sprint name in title
# ---------------------------------------------------------------------------


class TestOuterPanelTitle:
    def test_title_includes_release_name(self):
        config = _make_config(release_dir=Path("/tmp/v3.7-task-unified-v2"))
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), None)
        output = _render_to_string(tui)
        assert "SUPERCLAUDE SPRINT RUNNER" in output
        assert "v3.7-task-unified-v2" in output

    def test_title_falls_back_to_index_parent(self):
        # release_dir is "." → should fall back to index_path.parent name
        config = _make_config(release_dir=Path("."))
        config.index_path = Path("/tmp/foo-release/tasklist-index.md")
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), None)
        output = _render_to_string(tui)
        assert "foo-release" in output


# ---------------------------------------------------------------------------
# F2 phase table columns
# ---------------------------------------------------------------------------


class TestPhaseTableColumns:
    def test_default_columns(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), None)
        table = tui._build_phase_table()
        headers = [c.header for c in table.columns]
        assert "Tasks" not in headers
        assert "Turns" in headers
        assert "Output" in headers

    def test_running_phase_shows_monitor_turns_and_output(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        sr = SprintResult(config=config)
        ms = MonitorState(turns=7, output_bytes=4096)
        tui.update(sr, ms, config.phases[0])
        output = _render_to_string(tui)
        assert "7" in output
        assert "4.0 KB" in output

    def test_completed_phase_shows_phase_result_turns(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        sr = SprintResult(
            config=config,
            phase_results=[
                _make_phase_result(
                    phase=config.phases[0],
                    status=PhaseStatus.PASS,
                    turns=12,
                    output_bytes=2048,
                ),
            ],
        )
        tui.update(sr, MonitorState(), None)
        output = _render_to_string(tui)
        assert "12" in output
        assert "2.0 KB" in output


# ---------------------------------------------------------------------------
# F3 dual progress bar
# ---------------------------------------------------------------------------


class TestDualProgressBar:
    def test_returns_text(self):
        config = _make_config(total_tasks=10)
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), None)
        bar = tui._build_progress()
        assert isinstance(bar, Text)

    def test_phases_and_tasks_labels(self):
        config = _make_config(total_tasks=10)
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), None)
        output = _render_to_string(tui)
        assert "Phases" in output
        assert "Tasks" in output

    def test_percentage_present(self):
        config = _make_config(total_tasks=4)
        phase_result = _make_phase_result(
            phase=config.phases[0], status=PhaseStatus.PASS
        )
        sr = SprintResult(config=config, phase_results=[phase_result])
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(sr, MonitorState(), None)
        bar_text = tui._build_progress().plain
        # 1 of 2 phases done → 50%
        assert "50%" in bar_text

    def test_zero_total_tasks_renders_empty_bar(self):
        config = _make_config(total_tasks=0)
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), None)
        bar_text = tui._build_progress().plain
        # Tasks section should show 0/0 and not crash
        assert "0/0" in bar_text


# ---------------------------------------------------------------------------
# F5 Prompt + Agent lines, F1 activity stream
# ---------------------------------------------------------------------------


class TestActivePanelContextAndActivity:
    def test_prompt_preview_rendered(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), config.phases[0])
        output = _render_to_string(tui)
        assert "Prompt:" in output
        assert "Lay the foundation" in output

    def test_agent_line_shows_last_assistant_text(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        ms = MonitorState(last_assistant_text="Implementing checkpoint gate")
        tui.update(SprintResult(config=config), ms, config.phases[0])
        output = _render_to_string(tui)
        assert "Agent:" in output
        assert "Implementing checkpoint gate" in output

    def test_activity_stream_renders_entries(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        ms = MonitorState()
        now = time.time()
        ms.activity_log.extend(
            [
                (now - 3, "Read", "models.py"),
                (now - 2, "Edit", "tui.py"),
                (now - 1, "Bash", "pytest"),
            ]
        )
        tui.update(SprintResult(config=config), ms, config.phases[0])
        output = _render_to_string(tui)
        assert "Activity" in output
        assert "models.py" in output
        assert "tui.py" in output

    def test_activity_stream_pads_to_three_lines(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), config.phases[0])
        lines = tui._render_activity_stream()
        assert len(lines) == 3
        # With no entries every line should be the em-dash placeholder.
        assert all("—" in line for line in lines)

    def test_thinking_indicator_when_idle(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        ms = MonitorState()
        # Last entry 10s ago → well beyond the 2s threshold.
        ms.activity_log.append((time.time() - 10, "Read", "foo.py"))
        tui.update(SprintResult(config=config), ms, config.phases[0])
        lines = tui._render_activity_stream()
        joined = "\n".join(lines)
        assert "thinking" in joined


# ---------------------------------------------------------------------------
# F4 conditional error panel
# ---------------------------------------------------------------------------


class TestErrorPanel:
    def test_hidden_when_no_errors(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.update(SprintResult(config=config), MonitorState(), config.phases[0])
        assert tui._build_error_panel() is None
        output = _render_to_string(tui)
        assert "ERRORS (" not in output

    def test_rendered_when_errors_present(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        ms = MonitorState()
        ms.errors.append(("T01.02", "Read", "File not found"))
        tui.update(SprintResult(config=config), ms, config.phases[0])
        panel = tui._build_error_panel()
        assert isinstance(panel, Panel)
        output = _render_to_string(tui)
        assert "ERRORS (1)" in output
        assert "File not found" in output

    def test_overflow_marker_when_more_than_five(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        ms = MonitorState()
        for i in range(8):
            ms.errors.append((f"T01.{i:02d}", "Bash", f"err {i}"))
        tui.update(SprintResult(config=config), ms, config.phases[0])
        output = _render_to_string(tui)
        assert "ERRORS (8)" in output
        # 8 - 5 displayed = 3 overflow
        assert "+3 more" in output


# ---------------------------------------------------------------------------
# F6 terminal panels (success + halt)
# ---------------------------------------------------------------------------


class TestSuccessTerminalPanel:
    def test_renders_aggregates(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        sr = SprintResult(
            config=config,
            outcome=SprintOutcome.SUCCESS,
            phase_results=[
                _make_phase_result(turns=5, tokens_in=500, tokens_out=200, output_bytes=1024, files_changed=2),
                _make_phase_result(turns=3, tokens_in=300, tokens_out=100, output_bytes=2048, files_changed=3),
            ],
        )
        sr.finished_at = datetime.now(timezone.utc)
        tui.update(sr, MonitorState(), None)
        output = _render_to_string(tui)
        assert "ALL PHASES PASSED" in output
        assert "Turns:" in output and "8" in output  # 5+3
        assert "800" in output  # 500+300 input tokens
        assert "3.0 KB" in output  # 1024+2048 output
        assert "5" in output  # 2+3 files changed


class TestHaltTerminalPanel:
    def test_renders_halt_with_resume_and_errors(self):
        config = _make_config(total_tasks=6)
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        phase_result = _make_phase_result(
            phase=config.phases[0],
            status=PhaseStatus.HALT,
            last_task_id="T01.02",
        )
        sr = SprintResult(
            config=config,
            outcome=SprintOutcome.HALTED,
            phase_results=[phase_result],
            halt_phase=1,
        )
        sr.finished_at = datetime.now(timezone.utc)
        ms = MonitorState()
        ms.errors.append(("T01.02", "Bash", "exit_code: 2"))
        tui.update(sr, ms, None)
        output = _render_to_string(tui)
        assert "HALTED" in output
        assert "Halted at: Phase 1" in output
        assert "Resume:" in output
        assert "Errors (1)" in output
        assert "exit_code: 2" in output
        assert "Last task: T01.02" in output


# ---------------------------------------------------------------------------
# Cross-domain: PASS_MISSING_CHECKPOINT must render without crashing.
# ---------------------------------------------------------------------------


class TestPassMissingCheckpointRender:
    def test_phase_with_missing_checkpoint_status_renders(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        sr = SprintResult(
            config=config,
            phase_results=[
                _make_phase_result(
                    phase=config.phases[0],
                    status=PhaseStatus.PASS_MISSING_CHECKPOINT,
                )
            ],
        )
        tui.update(sr, MonitorState(), None)
        output = _render_to_string(tui)
        assert "PASS" in output


# ---------------------------------------------------------------------------
# TUI v2 Wave 4 (v3.7, F9): --no-tmux summary notification
# ---------------------------------------------------------------------------


class TestLatestSummaryNotification:
    def test_default_is_none_and_no_line_rendered(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        assert tui.latest_summary_notification is None
        tui.update(SprintResult(config=config), MonitorState(), None)
        output = _render_to_string(tui)
        assert "Summary:" not in output

    def test_notification_line_rendered_when_set(self):
        config = _make_config()
        tui = SprintTUI(config, console=Console(file=StringIO(), width=160))
        tui.latest_summary_notification = (
            "Phase 2 summary ready: results/phase-2-summary.md"
        )
        tui.update(SprintResult(config=config), MonitorState(), None)
        output = _render_to_string(tui)
        assert "Summary:" in output
        assert "phase-2-summary.md" in output
