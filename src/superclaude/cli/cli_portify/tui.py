"""Basic Rich TUI live dashboard for CLI Portify.

Implements PortifyTUI start/stop lifecycle (T03.12 / NFR-008).
Degrades gracefully in non-terminal environments (CI, tests).
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from typing import Optional

try:
    from rich.table import Table
    from rich.live import Live
    from rich.console import Console

    _RICH_AVAILABLE = True
except ImportError:
    _RICH_AVAILABLE = False

# ---------------------------------------------------------------------------
# Pipeline step definitions
# ---------------------------------------------------------------------------

PIPELINE_STEPS: tuple[str, ...] = (
    "validate-config",
    "discover-components",
    "analyze-workflow",
    "brainstorm-gaps",
    "synthesize-spec",
    "design-pipeline",
    "panel-review",
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class StepDisplayState:
    """Display state for a single pipeline step."""

    name: str
    status: str = "pending"
    duration_seconds: float = 0.0
    gate_result: str = ""
    iteration: int = 0
    warning: str = ""


@dataclass
class DashboardState:
    """Mutable dashboard state updated during pipeline execution."""

    steps: list[StepDisplayState] = field(default_factory=list)
    current_step: str = ""
    review_paused: bool = False
    review_prompt: str = ""
    warnings: list[str] = field(default_factory=list)
    pipeline_start: float = field(default_factory=time.time)
    total_elapsed: float = 0.0

    def __post_init__(self) -> None:
        if not self.steps:
            self.steps = [StepDisplayState(name=s) for s in PIPELINE_STEPS]

    def _find_step(self, name: str) -> Optional[StepDisplayState]:
        for step in self.steps:
            if step.name == name:
                return step
        return None

    def update_step(
        self,
        name: str,
        *,
        status: str = "",
        duration: float = 0.0,
        gate_result: str = "",
        iteration: int = 0,
        warning: str = "",
    ) -> None:
        step = self._find_step(name)
        if step is None:
            return
        if status:
            step.status = status
        if duration:
            step.duration_seconds = duration
        if gate_result:
            step.gate_result = gate_result
        if iteration:
            step.iteration = iteration
        if warning:
            step.warning = warning

    def mark_running(self, name: str) -> None:
        step = self._find_step(name)
        if step:
            step.status = "running"
            self.current_step = name

    def mark_complete(
        self, name: str, status: str, duration: float, gate_result: str = ""
    ) -> None:
        step = self._find_step(name)
        if step:
            step.status = status
            step.duration_seconds = duration
            step.gate_result = gate_result
        self.current_step = ""

    def set_review_pause(self, prompt: str) -> None:
        self.review_paused = True
        self.review_prompt = prompt

    def clear_review_pause(self) -> None:
        self.review_paused = False
        self.review_prompt = ""

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def compute_elapsed(self) -> None:
        self.total_elapsed = time.time() - self.pipeline_start


# ---------------------------------------------------------------------------
# Table rendering
# ---------------------------------------------------------------------------


def _build_dashboard_table(state: DashboardState) -> "Table":
    """Build a Rich Table from DashboardState."""
    if not _RICH_AVAILABLE:
        # Return a stub table for non-Rich environments
        class _StubTable:
            columns: list = []
            row_count: int = len(state.steps) + 1

            class _Col:
                def __init__(self, header: str):
                    self.header = header

            def add_column(self, header: str, **kw):
                self.columns.append(self._Col(header))

            def add_row(self, *cells, **kw):
                pass

        t = _StubTable()
        for col in ("#", "Step", "Status", "Gate", "Time", "Info"):
            t.add_column(col)
        for step in state.steps:
            t.add_row(
                str(state.steps.index(step) + 1),
                step.name,
                step.status,
                step.gate_result or "-",
                f"{step.duration_seconds:.1f}s",
                step.warning or "",
            )
        # Footer row
        t.add_row("", "Pipeline", f"elapsed {state.total_elapsed:.1f}s", "", "", "")
        return t

    table = Table(title="CLI Portify Pipeline")
    table.add_column("#", style="dim")
    table.add_column("Step")
    table.add_column("Status")
    table.add_column("Gate")
    table.add_column("Time")
    table.add_column("Info")

    for i, step in enumerate(state.steps, start=1):
        table.add_row(
            str(i),
            step.name,
            step.status,
            step.gate_result or "-",
            f"{step.duration_seconds:.1f}s",
            step.warning or "",
        )

    # Footer row
    table.add_row(
        "",
        "Pipeline",
        f"elapsed {state.total_elapsed:.1f}s",
        "",
        "",
        "",
    )

    return table


# ---------------------------------------------------------------------------
# TuiDashboard
# ---------------------------------------------------------------------------


class TuiDashboard:
    """Controller for the Rich live dashboard.

    Degrades gracefully in non-terminal environments (CI, tests):
    - start() / stop() are no-ops when not in a real terminal
    - All state mutations still occur (enabling test assertions)
    """

    def __init__(self) -> None:
        self.state = DashboardState()
        self._live: Optional["Live"] = None
        self._is_terminal: bool = (
            sys.stdout.isatty() if hasattr(sys.stdout, "isatty") else False
        )

    @property
    def is_live(self) -> bool:
        return self._live is not None

    def start(self) -> None:
        """Start the live dashboard (no-op in non-terminal environments)."""
        if not _RICH_AVAILABLE or not self._is_terminal:
            return
        console = Console()
        self._live = Live(
            _build_dashboard_table(self.state),
            console=console,
            refresh_per_second=4,
        )
        self._live.start()

    def stop(self) -> None:
        """Stop the live dashboard."""
        if self._live is not None:
            self._live.stop()
            self._live = None

    def _refresh(self) -> None:
        if self._live is not None:
            self.state.compute_elapsed()
            self._live.update(_build_dashboard_table(self.state))

    def step_start(self, step_name: str) -> None:
        self.state.mark_running(step_name)
        self._refresh()

    def step_complete(
        self, step_name: str, status: str, duration: float, gate_result: str = ""
    ) -> None:
        self.state.mark_complete(step_name, status, duration, gate_result)
        self._refresh()

    def set_iteration(self, step_name: str, iteration: int) -> None:
        self.state.update_step(step_name, iteration=iteration)
        self._refresh()

    def add_warning(self, message: str) -> None:
        self.state.add_warning(message)
        self._refresh()

    def pause_for_review(self, prompt: str) -> None:
        self.state.set_review_pause(prompt)
        self._refresh()

    def resume_after_review(self) -> None:
        self.state.clear_review_pause()
        self._refresh()


# ---------------------------------------------------------------------------
# PortifyTUI — NFR-008 compliant TUI with update_step / update_convergence
# ---------------------------------------------------------------------------


class PortifyTUI:
    """NFR-008 compliant TUI providing real-time step and convergence updates.

    Wraps TuiDashboard and adds:
    - update_step(step_id, status, bytes_written, elapsed_s) — real-time per-step update
    - update_convergence(iteration, findings_count, placeholder_count) — Phase 8 loop display
    - start() / stop() lifecycle (delegates to TuiDashboard)

    Degrades gracefully in non-terminal (CI, test) environments.
    """

    def __init__(self) -> None:
        self._dashboard = TuiDashboard()
        # Convergence tracking state
        self._convergence_iteration: int = 0
        self._findings_count: int = 0
        self._placeholder_count: int = 0

    def start(self) -> None:
        """Start the live TUI dashboard."""
        self._dashboard.start()

    def stop(self) -> None:
        """Stop the live TUI dashboard."""
        self._dashboard.stop()

    @property
    def is_live(self) -> bool:
        return self._dashboard.is_live

    def update_step(
        self,
        step_id: str,
        status: str,
        bytes_written: int = 0,
        elapsed_s: float = 0.0,
    ) -> None:
        """Update a pipeline step with real-time status, byte count, and elapsed time.

        Args:
            step_id: Step identifier matching a PIPELINE_STEPS name.
            status: One of 'running', 'pass', 'fail', 'timeout', 'error', 'pending'.
            bytes_written: Bytes written to the step's output so far.
            elapsed_s: Elapsed time in seconds for this step.
        """
        self._dashboard.state.update_step(
            step_id,
            status=status,
            duration=elapsed_s,
        )
        self._dashboard._refresh()

    def update_convergence(
        self,
        iteration: int,
        findings_count: int,
        placeholder_count: int,
    ) -> None:
        """Update convergence loop display state for Phase 8 panel-review.

        Args:
            iteration: Current iteration number (1-3).
            findings_count: Number of findings from the current iteration.
            placeholder_count: Number of unresolved placeholder sentinels.
        """
        self._convergence_iteration = iteration
        self._findings_count = findings_count
        self._placeholder_count = placeholder_count
        self._dashboard.set_iteration("panel-review", iteration)

    def step_start(self, step_name: str) -> None:
        """Mark a step as running."""
        self._dashboard.step_start(step_name)

    def step_complete(
        self, step_name: str, status: str, duration: float, gate_result: str = ""
    ) -> None:
        """Mark a step as complete."""
        self._dashboard.step_complete(step_name, status, duration, gate_result)
