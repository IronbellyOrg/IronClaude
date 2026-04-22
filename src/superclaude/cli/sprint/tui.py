"""Sprint TUI — Rich-based terminal dashboard for sprint execution."""

from __future__ import annotations

import logging
import time
from typing import Optional

from rich.console import Console
from rich.console import Group as RichGroup
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import count_tasks_in_file
from .debug_logger import debug_log
from .models import (
    GateDisplayState,
    MonitorState,
    Phase,
    PhaseStatus,
    SprintConfig,
    SprintResult,
)

# TUI v2 Wave 2 (v3.7) constants -----------------------------------------
# Dual progress bar widths (F3). Block characters picked so the bar reads
# at a glance on light and dark terminals.
_BAR_WIDTH = 20
_BAR_FULL = "█"   # █ full block
_BAR_EMPTY = "░"  # ░ light shade
# F5: LLM context lines truncate to this width.
_LLM_LINE_MAX = 60
# F4: error panel render cap (stored cap is ERRORS_MAX=10 in monitor).
_ERROR_PANEL_MAX_DISPLAYED = 5
# F1: seconds of idle before the activity stream shows [thinking...].
_THINKING_IDLE_SECONDS = 2

_dbg = logging.getLogger("superclaude.sprint.debug.tui")

STATUS_STYLES = {
    PhaseStatus.PASS: "bold green",
    PhaseStatus.PASS_NO_SIGNAL: "green",
    PhaseStatus.PASS_NO_REPORT: "green",
    PhaseStatus.PASS_RECOVERED: "green",
    PhaseStatus.PASS_MISSING_CHECKPOINT: "yellow",
    PhaseStatus.PREFLIGHT_PASS: "bold cyan",
    PhaseStatus.INCOMPLETE: "bold red",
    PhaseStatus.HALT: "bold red",
    PhaseStatus.TIMEOUT: "bold red",
    PhaseStatus.ERROR: "bold red",
    PhaseStatus.RUNNING: "bold yellow",
    PhaseStatus.PENDING: "dim",
    PhaseStatus.SKIPPED: "dim strikethrough",
}

STATUS_ICONS = {
    PhaseStatus.PASS: "[green]PASS[/]",
    PhaseStatus.PASS_NO_SIGNAL: "[green]PASS[/]",
    PhaseStatus.PASS_NO_REPORT: "[green]PASS[/]",
    PhaseStatus.PASS_RECOVERED: "[green]PASS✓[/]",
    PhaseStatus.PASS_MISSING_CHECKPOINT: "[yellow]PASS⚠[/]",
    PhaseStatus.PREFLIGHT_PASS: "[cyan]PREFLIGHT✓[/]",
    PhaseStatus.INCOMPLETE: "[red]INCOMPLETE[/]",
    PhaseStatus.HALT: "[red]HALT[/]",
    PhaseStatus.TIMEOUT: "[red]TIMEOUT[/]",
    PhaseStatus.ERROR: "[red]ERROR[/]",
    PhaseStatus.RUNNING: "[yellow]RUNNING[/]",
    PhaseStatus.PENDING: "[dim]pending[/]",
    PhaseStatus.SKIPPED: "[dim]skipped[/]",
}


class SprintTUI:
    """Rich-based terminal UI for sprint execution."""

    def __init__(self, config: SprintConfig, console: Console | None = None):
        self.config = config
        self.console = console or Console()
        self.sprint_result: Optional[SprintResult] = None
        self.monitor_state = MonitorState()
        self.current_phase: Optional[Phase] = None
        self._live: Optional[Live] = None
        self._live_failed: bool = False
        # Per-phase gate display state; updated via update() by executor.
        # Only rendered when grace_period > 0 (trailing gates enabled).
        self.gate_states: dict[int, GateDisplayState] = {}
        self._show_gate_column: bool = (
            getattr(config, "grace_period", 0) > 0
        )  # silences future updates after first render error

    def start(self) -> Live:
        """Start the Live display and return it for the executor to use."""
        debug_log(_dbg, "tui_start")
        self._live = Live(
            self._render(),
            console=self.console,
            refresh_per_second=2,
            screen=False,
        )
        self._live.start()
        return self._live

    def stop(self):
        """Stop the Live display."""
        debug_log(_dbg, "tui_stop")
        if self._live:
            self._live.stop()

    def update(
        self,
        sprint_result: SprintResult,
        monitor_state: MonitorState,
        current_phase: Optional[Phase],
    ):
        """Called by the executor to refresh the display.

        Rendering errors (terminal resize race, broken pipe, etc.) are caught
        so a display glitch cannot abort the running sprint.
        """
        self.sprint_result = sprint_result
        self.monitor_state = monitor_state
        self.current_phase = current_phase
        if self._live and not self._live_failed:
            try:
                self._live.update(self._render())
                debug_log(
                    _dbg,
                    "tui_update",
                    events_received=monitor_state.events_received,
                    stall_status=monitor_state.stall_status,
                    last_event_time=round(monitor_state.last_event_time, 1),
                )
            except Exception as exc:
                import sys

                self._live_failed = True
                debug_log(
                    _dbg,
                    "tui_live_failed",
                    error=str(exc),
                    error_type=type(exc).__name__,
                )
                print(
                    f"[TUI] Display error (continuing sprint): {exc}", file=sys.stderr
                )

    def _render(self) -> Panel:
        """Build the complete TUI layout.

        v3.7 Wave 2 layout (top → bottom):
            header  · table  · progress  · [error panel?]  · active
        The error panel (F4) is hidden when no errors are pending.
        """
        header = self._build_header()
        table = self._build_phase_table()
        progress = self._build_progress()
        error_panel = self._build_error_panel()
        detail = self._build_active_panel()

        parts: list = [header, "", table, "", progress, ""]
        if error_panel is not None:
            parts.extend([error_panel, ""])
        parts.append(detail)
        body = RichGroup(*parts)

        # F7 (v3.7): include the release name in the outer panel title
        # so operators running several sprints at once can tell them apart.
        release_name = self._release_name()
        if release_name:
            title = f"[bold]SUPERCLAUDE SPRINT RUNNER[/] [dim]== {release_name}[/]"
        else:
            title = "[bold]SUPERCLAUDE SPRINT RUNNER[/]"
        return Panel(
            body,
            title=title,
            border_style="blue",
            padding=(1, 2),
        )

    def _release_name(self) -> str:
        """Return the release identifier used in the panel title (F7).

        Derived from ``SprintConfig.release_dir`` basename. Falls back to
        the index-file parent when that resolves to ``.`` or empty string.
        """
        try:
            name = self.config.release_dir.name
        except Exception:  # noqa: BLE001 - defensive on Path semantics
            name = ""
        if not name or name in (".", "/"):
            try:
                name = self.config.index_path.parent.name
            except Exception:  # noqa: BLE001
                name = ""
        return name

    def _build_header(self) -> Text:
        elapsed = self.sprint_result.duration_display if self.sprint_result else "0s"
        index_name = self.config.index_path.parent.name
        return Text.from_markup(f"[dim]{index_name}[/]    Elapsed: [bold]{elapsed}[/]")

    def _build_phase_table(self) -> Table:
        """Render the phase table.

        v3.7 Wave 2 (F2): the ``Tasks`` column moves to the active panel
        as part of the progress bar; in its place we expose ``Turns``
        (for turn-budget awareness) and ``Output`` (a rough size signal).
        The ``Gate`` column is preserved and still renders when
        ``grace_period > 0`` (TUI-Q9).
        """
        table = Table(
            show_header=True,
            header_style="bold",
            border_style="dim",
            pad_edge=False,
            box=None,
        )
        table.add_column("#", width=3, justify="right")
        table.add_column("Phase", min_width=30)
        table.add_column("Status", width=12, justify="center")
        if self._show_gate_column:
            table.add_column("Gate", width=6, justify="center")
        table.add_column("Duration", width=10, justify="right")
        table.add_column("Turns", width=6, justify="right")
        table.add_column("Output", width=8, justify="right")

        if not self.sprint_result:
            return table

        for phase in self.config.active_phases:
            result = next(
                (
                    r
                    for r in self.sprint_result.phase_results
                    if r.phase.number == phase.number
                ),
                None,
            )
            status = result.status if result else PhaseStatus.PENDING
            if phase == self.current_phase and not (
                result and result.status.is_terminal
            ):
                status = PhaseStatus.RUNNING

            style = STATUS_STYLES[status]
            duration = (
                result.duration_display
                if result and status.is_terminal
                else (
                    f"{int(self.monitor_state.stall_seconds)}s"
                    if status == PhaseStatus.RUNNING
                    else "-"
                )
            )
            # Turns / Output: completed phases pull from PhaseResult;
            # the running phase pulls live from MonitorState.
            if result and status.is_terminal:
                turns_display = str(result.turns) if result.turns else "-"
                output_display = _format_bytes(result.output_bytes)
            elif status == PhaseStatus.RUNNING:
                turns_display = str(self.monitor_state.turns) if self.monitor_state.turns else "-"
                output_display = self.monitor_state.output_size_display
            else:
                turns_display = "-"
                output_display = "-"

            row: list[str] = [
                str(phase.number),
                phase.display_name,
                STATUS_ICONS.get(status, str(status.value)),
            ]
            if self._show_gate_column:
                gate_state = self.gate_states.get(phase.number, GateDisplayState.NONE)
                row.append(gate_state.icon)
            row.extend([duration, turns_display, output_display])

            table.add_row(
                *row,
                style=style if status == PhaseStatus.PENDING else "",
            )

        return table

    def _build_progress(self) -> Text:
        """Render the dual phase/task progress bar (F3, v3.7 Wave 2).

        Single ``Text`` line with two manual bar renders using block
        characters. Example::

            Phases [████░░░░░░░░░░░░░░░░] 25% 1/4    Tasks [██████████░░░░░░░░░░] 51% 20/39

        The tasks segment shows ``0/0`` when ``SprintConfig.total_tasks``
        is zero (e.g. when the pre-scan found no ``T<PP>.<TT>`` headings
        — common for legacy tasklists). It is still rendered so the
        layout stays stable across sprints.
        """
        phases_total = len(self.config.active_phases)
        phases_done = self._phases_done()
        tasks_total = getattr(self.config, "total_tasks", 0) or 0
        tasks_done = self._tasks_completed_estimate()

        phases_bar = _render_bar(_BAR_WIDTH, phases_done, phases_total)
        tasks_bar = _render_bar(_BAR_WIDTH, tasks_done, tasks_total)
        phases_pct = _render_percent(phases_done, phases_total)
        tasks_pct = _render_percent(tasks_done, tasks_total)

        # Use bright/dim styling so the bars read cleanly on terminals
        # with limited color palettes.
        line = (
            f"[bold]Phases[/] [cyan]{phases_bar}[/] {phases_pct} "
            f"[dim]{phases_done}/{phases_total}[/]    "
            f"[bold]Tasks[/] [green]{tasks_bar}[/] {tasks_pct} "
            f"[dim]{tasks_done}/{tasks_total}[/]"
        )
        return Text.from_markup(line)

    def _phases_done(self) -> int:
        """Count phases with a terminal (success-or-failure) result."""
        if not self.sprint_result:
            return 0
        return sum(1 for r in self.sprint_result.phase_results if r.status.is_terminal)

    def _tasks_completed_estimate(self) -> int:
        """Estimate tasks done: sum of completed phases + live estimate.

        Completed phases contribute their total task heading count (we
        re-scan the phase file; the file is small so this is cheap
        enough at 2 Hz). The currently-running phase contributes
        ``MonitorState.completed_task_estimate`` populated by the
        monitor from ``last_task_id``.
        """
        done = 0
        if self.sprint_result:
            for r in self.sprint_result.phase_results:
                if r.status.is_terminal:
                    done += count_tasks_in_file(r.phase.file)
        if self.current_phase is not None:
            done += max(0, self.monitor_state.completed_task_estimate)
        return done

    def _build_active_panel(self) -> Panel:
        """Detail panel for the currently-running phase.

        v3.7 Wave 2 additions:
        - F5: ``Prompt:`` (static per phase, from ``Phase.prompt_preview``)
          and ``Agent:`` (live, from ``MonitorState.last_assistant_text``).
        - F1: 3-line activity stream of tool calls with a
          ``[thinking... Ns]`` indicator when the subprocess goes idle.
        """
        if not self.current_phase:
            # Terminal state
            if self.sprint_result and self.sprint_result.finished_at:
                return self._build_terminal_panel()
            return Panel("[dim]Waiting...[/]", title="Active Phase")

        ms = self.monitor_state
        stall_display = ms.stall_status
        stall_style = (
            "bold red blink"
            if stall_display == "STALLED"
            else "yellow"
            if stall_display == "thinking..."
            else "green"
        )

        # F5: LLM context lines (truncated so each fits the width).
        prompt_text = _truncate(self.current_phase.prompt_display, _LLM_LINE_MAX)
        agent_text = _truncate(ms.last_assistant_text, _LLM_LINE_MAX)

        lines = [
            f"File:    {self.current_phase.basename}",
            f"Status:  RUNNING -- [{stall_style}]{stall_display}[/]",
            "",
            f"[bold]Prompt:[/]  [dim]{prompt_text}[/]",
            f"[bold]Agent:[/]   {agent_text or '[dim]—[/]'}",
            "",
            f"Last task:     {ms.last_task_id or '-'}",
            f"Last tool:     {ms.last_tool_used or '-'}",
            f"Output size:   {ms.output_size_display}  (+{ms.growth_rate_bps:.1f} B/s)",
            f"Files changed: {ms.files_changed}",
        ]

        # F1: 3-line activity stream (ring buffer). Pad to 3 lines so the
        # panel height stays stable frame-to-frame.
        lines.append("")
        lines.append("[dim]Activity:[/]")
        lines.extend(self._render_activity_stream())

        return Panel(
            "\n".join(lines),
            title=f"[bold yellow]ACTIVE: Phase {self.current_phase.number}[/]",
            border_style="yellow",
        )

    def _render_activity_stream(self) -> list[str]:
        """Build the 3-line activity tail for the active panel (F1).

        When the newest entry is older than ``_THINKING_IDLE_SECONDS``,
        the last line is replaced with a ``[thinking... Ns]`` indicator.
        """
        out: list[str] = []
        log = self.monitor_state.activity_log
        for ts, tool_name, desc in log[-3:]:
            stamp = _format_timestamp(ts)
            truncated = _truncate(desc, 50)
            out.append(f"  [dim]{stamp}[/]  [cyan]{tool_name}[/]  {truncated}")

        # Pad to exactly 3 lines.
        while len(out) < 3:
            out.append("  [dim]—[/]")

        if log:
            last_ts = log[-1][0]
            idle_seconds = max(0.0, time.time() - last_ts)
            if idle_seconds > _THINKING_IDLE_SECONDS:
                out[-1] = f"  [dim italic][thinking... {int(idle_seconds)}s][/]"

        return out

    def _build_error_panel(self) -> Optional[Panel]:
        """Build the conditional error panel (F4, v3.7 Wave 2).

        Returns ``None`` when no errors are pending so the caller can
        omit the section entirely. When errors exist, renders up to
        ``_ERROR_PANEL_MAX_DISPLAYED`` rows with an overflow suffix.
        """
        errors = self.monitor_state.errors
        if not errors:
            return None

        total = len(errors)
        visible = errors[-_ERROR_PANEL_MAX_DISPLAYED:]  # newest wins on tail-end
        overflow = total - len(visible)

        lines: list[str] = []
        for task_id, tool, message in visible:
            label = task_id or "-"
            tool_label = tool or "-"
            # Keep the per-error line tight so the panel doesn't dominate.
            msg = _truncate(message.replace("\n", " "), 80)
            lines.append(f"  [bold]{label:<8}[/]  [cyan]{tool_label:<10}[/]  {msg}")

        if overflow > 0:
            lines.append(f"  [dim](+{overflow} more)[/]")

        return Panel(
            "\n".join(lines),
            title=f"[bold red]ERRORS ({total})[/]",
            border_style="red",
            padding=(0, 1),
        )

    def _build_terminal_panel(self) -> Panel:
        """Build the final state panel (v3.7 Wave 2 F6).

        The success variant surfaces turn / token / file / output
        aggregates from :class:`SprintResult`. The halt variant adds a
        resume command, the last task, and folds in pending errors from
        the monitor so operators can triage without leaving the TUI.
        """
        sr = self.sprint_result
        assert sr is not None  # _build_terminal_panel is only reached with a sprint
        if sr.outcome.value == "success":
            return self._build_success_panel(sr)
        return self._build_halt_panel(sr)

    def _build_success_panel(self, sr: SprintResult) -> Panel:
        phases_done = len(sr.phase_results)
        turns_total = sr.total_turns
        avg_turns = (turns_total / phases_done) if phases_done else 0.0
        lines = [
            "Result:    [bold green]ALL PHASES PASSED[/]",
            f"Duration:  {sr.duration_display}",
            f"Turns:     {turns_total} total  ([dim]avg {avg_turns:.1f}/phase[/])",
            (
                f"Tokens:    in={_format_tokens(sr.total_tokens_in)}  "
                f"out={_format_tokens(sr.total_tokens_out)}"
            ),
            f"Output:    {_format_bytes(sr.total_output_bytes)}",
            f"Files:     {sr.total_files_changed}",
            f"Log:       {self.config.execution_log_md}",
        ]
        return Panel(
            "\n".join(lines),
            title="[bold green]Sprint Complete[/]",
            border_style="green",
        )

    def _build_halt_panel(self, sr: SprintResult) -> Panel:
        phases_done = len(sr.phase_results)
        phases_total = len(self.config.active_phases)
        tasks_done = self._tasks_completed_estimate()
        tasks_total = getattr(self.config, "total_tasks", 0) or 0
        turns_total = sr.total_turns

        lines = [f"Result:    [bold red]{sr.outcome.value.upper()}[/]"]
        if sr.halt_phase is not None:
            lines.append(f"Halted at: Phase {sr.halt_phase}")
        lines.append(f"Completed: {phases_done}/{phases_total} phases  ·  {tasks_done}/{tasks_total} tasks")
        lines.append(f"Duration:  {sr.duration_display}")
        lines.append(f"Turns:     {turns_total} total")
        lines.append(
            f"Tokens:    in={_format_tokens(sr.total_tokens_in)}  "
            f"out={_format_tokens(sr.total_tokens_out)}"
        )

        # Surface the last task id + errors when available.
        if sr.phase_results:
            last_result = sr.phase_results[-1]
            last_task = last_result.last_task_id or "-"
            lines.append(f"Last task: {last_task}  ([dim]{last_result.status.value}[/])")

        errors = self.monitor_state.errors
        if errors:
            lines.append("")
            lines.append(f"[bold]Errors ({len(errors)}):[/]")
            for task_id, tool, message in errors[-_ERROR_PANEL_MAX_DISPLAYED:]:
                label = task_id or "-"
                tool_label = tool or "-"
                msg = _truncate(message.replace("\n", " "), 80)
                lines.append(f"  {label:<8}  [cyan]{tool_label:<10}[/]  {msg}")
            overflow = len(errors) - _ERROR_PANEL_MAX_DISPLAYED
            if overflow > 0:
                lines.append(f"  [dim](+{overflow} more)[/]")

        resume = sr.resume_command()
        if resume:
            lines.append("")
            lines.append(f"Resume:    [bold]{resume}[/]")

        return Panel(
            "\n".join(lines),
            title="[bold red]Sprint Halted[/]",
            border_style="red",
        )


# ---------------------------------------------------------------------------
# Module-level render helpers (v3.7 Wave 2)
# ---------------------------------------------------------------------------


def _format_tokens(n: int) -> str:
    """Human-readable token count (F6 helper, Section 6.5).

    Under 1_000 → bare integer. Below one million → ``<N.M>K``. Beyond
    that → ``<N.M>M``. Negative numbers clamp to ``0``.
    """
    if n <= 0:
        return "0"
    if n < 1_000:
        return str(n)
    if n < 1_000_000:
        return f"{n / 1_000:.1f}K"
    return f"{n / 1_000_000:.1f}M"


def _format_bytes(n: int) -> str:
    """Render a byte count using the same grammar as MonitorState."""
    if n <= 0:
        return "0 B"
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.1f} MB"


def _render_bar(width: int, done: int, total: int) -> str:
    """Render a ``█``/``░`` progress bar of fixed ``width`` characters."""
    width = max(0, width)
    if total <= 0 or done <= 0:
        return _BAR_EMPTY * width
    ratio = min(1.0, done / total)
    filled = int(round(width * ratio))
    return _BAR_FULL * filled + _BAR_EMPTY * (width - filled)


def _render_percent(done: int, total: int) -> str:
    """Render a right-aligned percentage string like ``"25%"``."""
    if total <= 0:
        return "  0%"
    pct = max(0, min(100, int(round(100 * done / total))))
    return f"{pct:>3d}%"


def _format_timestamp(ts: float) -> str:
    """Render a wall-clock timestamp as ``HH:MM:SS``."""
    try:
        return time.strftime("%H:%M:%S", time.localtime(ts))
    except (ValueError, OSError):
        return "--:--:--"


def _truncate(text: str, limit: int) -> str:
    """Truncate ``text`` to ``limit`` chars, suffixing ``"..."`` when cut."""
    if not text:
        return ""
    if len(text) <= limit:
        return text
    # Leave three chars for the ellipsis.
    if limit <= 3:
        return text[:limit]
    return text[: limit - 3] + "..."
