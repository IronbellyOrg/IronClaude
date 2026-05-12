"""PRD pipeline TUI -- Rich-based terminal dashboard for PRD execution.

Displays step progress, gate state machine, and fix cycle counters
using Rich Live display. Gracefully degrades when terminal is not
interactive (CI/CD).

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
"""

from __future__ import annotations

import sys
from typing import Optional

try:
    from rich.console import Console
    from rich.console import Group as RichGroup
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, TextColumn
    from rich.table import Table
    from rich.text import Text

    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from .models import PrdMonitorState, PrdStepStatus


# ---------------------------------------------------------------------------
# Status display mapping
# ---------------------------------------------------------------------------

_STATUS_STYLES: dict[PrdStepStatus, str] = {
    PrdStepStatus.PASS: "bold green",
    PrdStepStatus.PASS_NO_SIGNAL: "green",
    PrdStepStatus.PASS_NO_REPORT: "green",
    PrdStepStatus.HALT: "bold red",
    PrdStepStatus.TIMEOUT: "bold red",
    PrdStepStatus.ERROR: "bold red",
    PrdStepStatus.QA_FAIL: "bold yellow",
    PrdStepStatus.QA_FAIL_EXHAUSTED: "bold red",
    PrdStepStatus.VALIDATION_FAIL: "bold red",
    PrdStepStatus.RUNNING: "bold yellow",
    PrdStepStatus.PENDING: "dim",
    PrdStepStatus.SKIPPED: "dim strikethrough",
    PrdStepStatus.INCOMPLETE: "yellow",
}

_STATUS_ICONS: dict[PrdStepStatus, str] = {
    PrdStepStatus.PASS: "[green]PASS[/]",
    PrdStepStatus.PASS_NO_SIGNAL: "[green]PASS[/]",
    PrdStepStatus.PASS_NO_REPORT: "[green]PASS[/]",
    PrdStepStatus.HALT: "[red]HALT[/]",
    PrdStepStatus.TIMEOUT: "[red]TIMEOUT[/]",
    PrdStepStatus.ERROR: "[red]ERROR[/]",
    PrdStepStatus.QA_FAIL: "[yellow]QA FAIL[/]",
    PrdStepStatus.QA_FAIL_EXHAUSTED: "[red]EXHAUSTED[/]",
    PrdStepStatus.VALIDATION_FAIL: "[red]GATE FAIL[/]",
    PrdStepStatus.RUNNING: "[yellow]RUNNING[/]",
    PrdStepStatus.PENDING: "[dim]pending[/]",
    PrdStepStatus.SKIPPED: "[dim]skipped[/]",
    PrdStepStatus.INCOMPLETE: "[yellow]incomplete[/]",
}

# Gate state machine display
_GATE_ICONS: dict[str, str] = {
    "PENDING": "[dim]--[/]",
    "RUNNING": "[yellow]...[/]",
    "PASS": "[green]OK[/]",
    "FAIL": "[red]FAIL[/]",
}


# ---------------------------------------------------------------------------
# Step display data
# ---------------------------------------------------------------------------


class StepDisplay:
    """Display data for a single pipeline step in the TUI."""

    def __init__(
        self,
        step_id: str,
        step_name: str,
        status: PrdStepStatus = PrdStepStatus.PENDING,
        duration: str = "-",
        agent_count: int = 0,
        qa_verdict: str = "",
        gate_state: str = "PENDING",
        fix_cycle: int = 0,
    ) -> None:
        self.step_id = step_id
        self.step_name = step_name
        self.status = status
        self.duration = duration
        self.agent_count = agent_count
        self.qa_verdict = qa_verdict
        self.gate_state = gate_state
        self.fix_cycle = fix_cycle


# ---------------------------------------------------------------------------
# PrdTUI
# ---------------------------------------------------------------------------


class PrdTUI:
    """Rich-based terminal dashboard for PRD pipeline execution.

    Columns: Step ID, Step Name, Status, Duration, Agent Count, QA Verdict.
    Gate state machine: PENDING -> RUNNING -> PASS/FAIL.
    Fix cycle display for QA steps.

    Gracefully degrades when terminal is not interactive or Rich
    is unavailable.
    """

    def __init__(self, *, interactive: Optional[bool] = None) -> None:
        self._interactive = (
            interactive if interactive is not None else _is_interactive()
        )
        self._steps: list[StepDisplay] = []
        self._monitor_state = PrdMonitorState()
        self._live: Optional[Live] = None  # type: ignore[assignment]
        self._live_failed = False
        self._console: Optional[Console] = None  # type: ignore[assignment]

        if _HAS_RICH and self._interactive:
            self._console = Console(stderr=True)

    def register_steps(self, steps: list[tuple[str, str]]) -> None:
        """Register the pipeline steps to display.

        Args:
            steps: List of (step_id, step_name) tuples.
        """
        self._steps = [
            StepDisplay(step_id=sid, step_name=sname)
            for sid, sname in steps
        ]

    def start(self) -> None:
        """Start the Live display."""
        if not self._interactive or not _HAS_RICH or self._console is None:
            return
        self._live = Live(
            self._render(),
            console=self._console,
            refresh_per_second=2,
            screen=False,
        )
        self._live.start()

    def stop(self) -> None:
        """Stop the Live display."""
        if self._live:
            self._live.stop()

    def update_step(
        self,
        step_id: str,
        *,
        status: Optional[PrdStepStatus] = None,
        duration: Optional[str] = None,
        agent_count: Optional[int] = None,
        qa_verdict: Optional[str] = None,
        gate_state: Optional[str] = None,
        fix_cycle: Optional[int] = None,
    ) -> None:
        """Update display data for a specific step."""
        for step in self._steps:
            if step.step_id == step_id:
                if status is not None:
                    step.status = status
                if duration is not None:
                    step.duration = duration
                if agent_count is not None:
                    step.agent_count = agent_count
                if qa_verdict is not None:
                    step.qa_verdict = qa_verdict
                if gate_state is not None:
                    step.gate_state = gate_state
                if fix_cycle is not None:
                    step.fix_cycle = fix_cycle
                break
        self._refresh()

    def update_monitor_state(self, state: PrdMonitorState) -> None:
        """Update the monitor state for display."""
        self._monitor_state = state
        self._refresh()

    # -------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------

    def _refresh(self) -> None:
        """Refresh the live display."""
        if self._live and not self._live_failed:
            try:
                self._live.update(self._render())
            except Exception as exc:
                self._live_failed = True
                print(
                    f"[TUI] Display error (continuing): {exc}",
                    file=sys.stderr,
                )

    def _render(self) -> Panel:
        """Build the complete TUI layout."""
        table = self._build_step_table()
        progress = self._build_progress()
        detail = self._build_detail_panel()

        body = RichGroup(table, "", progress, "", detail)

        return Panel(
            body,
            title="[bold]PRD PIPELINE[/]",
            border_style="blue",
            padding=(1, 2),
        )

    def _build_step_table(self) -> Table:
        """Build the step progress table."""
        table = Table(
            show_header=True,
            header_style="bold",
            border_style="dim",
            pad_edge=False,
            box=None,
        )
        table.add_column("Step", min_width=20)
        table.add_column("Name", min_width=25)
        table.add_column("Status", width=12, justify="center")
        table.add_column("Gate", width=6, justify="center")
        table.add_column("Duration", width=10, justify="right")
        table.add_column("Agents", width=7, justify="center")
        table.add_column("QA", width=10, justify="center")

        for step in self._steps:
            status_icon = _STATUS_ICONS.get(
                step.status, str(step.status.value)
            )
            gate_icon = _GATE_ICONS.get(step.gate_state, "[dim]--[/]")
            qa_display = step.qa_verdict or "-"
            agent_display = str(step.agent_count) if step.agent_count else "-"

            # Fix cycle indicator for QA steps
            if step.fix_cycle > 0:
                qa_display = f"{qa_display} (c{step.fix_cycle})"

            table.add_row(
                step.step_id,
                step.step_name,
                status_icon,
                gate_icon,
                step.duration,
                agent_display,
                qa_display,
            )

        return table

    def _build_progress(self) -> Progress:
        """Build overall pipeline progress bar."""
        progress = Progress(
            TextColumn("[bold]Progress"),
            BarColumn(bar_width=40),
            TextColumn("{task.percentage:>3.0f}%"),
            TextColumn("[dim]{task.completed}/{task.total} steps[/]"),
        )
        total = len(self._steps)
        done = sum(
            1 for s in self._steps if s.status.is_terminal
        )
        progress.add_task("pipeline", total=max(total, 1), completed=done)
        return progress

    def _build_detail_panel(self) -> Panel:
        """Build detail panel showing current monitor state."""
        ms = self._monitor_state
        lines = [
            f"Events:      {ms.events_received}",
            f"Output:      {ms.output_bytes} bytes",
            f"Research:    {ms.research_files_completed} files",
            f"Synthesis:   {ms.synth_files_completed} files",
            f"Fix cycles:  {ms.fix_cycle_count}",
            f"QA verdict:  {ms.qa_verdict or '-'}",
            f"Agent type:  {ms.current_agent_type or '-'}",
        ]
        return Panel(
            "\n".join(lines),
            title="[bold yellow]Monitor[/]",
            border_style="yellow",
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_interactive() -> bool:
    """Check if the terminal is interactive (not CI/CD)."""
    if not _HAS_RICH:
        return False
    return hasattr(sys.stderr, "isatty") and sys.stderr.isatty()
