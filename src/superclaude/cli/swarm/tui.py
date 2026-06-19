"""Swarm TUI -- Rich Live dashboard, flag-gated (T07.01 / COMP-013).

This module owns the optional terminal dashboard the operator sees when
``swarm run --tui`` is passed and stdout is a TTY. The dashboard renders
per-worker status + elapsed against the :class:`SwarmState` snapshot and
the :class:`EventRecord` stream emitted by the dispatch / logging
pipeline (T03.04 / T03.10).

Opt-in gate (INV-012)
=====================

The :func:`should_enable_tui` helper enforces the two-part gate the run
command must consult before instantiating :class:`TUI`:

    1. ``--tui`` was passed.
    2. The target stream (default ``sys.stdout``) is a TTY.

Either side false -> no Rich Live is started, no terminal control
sequences ever reach the caller. The matching grep audit
(``tests/swarm/test_inv012_tui_opt_in.py``) and the unit gate test
(``tests/swarm/test_tui.py::test_should_enable_tui_*``) pin this
contract from both ends.

Per-worker projection
=====================

The :class:`EventRecord` stream describes the lifecycle of each worker
slot via ``worker_start`` / ``worker_progress`` / ``worker_done`` events
keyed by ``worker_index``. :func:`_project_workers` folds the stream
into a per-index :class:`WorkerSnapshot` carrying status, model label,
and elapsed time. ``worker_done.payload["elapsed_ms"]`` (when present,
stamped by ``dispatch._run_worker``) is used verbatim; otherwise
elapsed is computed from the ISO 8601 timestamps stamped by
``logging_.Logger`` on append.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import IO, Iterable, Optional

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from superclaude.cli.swarm.models import EventRecord, SwarmState

__all__ = [
    "TUI",
    "WorkerSnapshot",
    "should_enable_tui",
]


# Status -> Rich style mapping. Keys cover the four DM-013 WorkerStatus
# Literal values plus the synthetic "pending" / "running" states the TUI
# projects from worker_start before worker_done lands.
_WORKER_STATUS_STYLES: dict[str, str] = {
    "pending": "dim",
    "running": "bold yellow",
    "success": "bold green",
    "timeout": "bold red",
    "parse_error": "bold red",
    "proxy_error": "bold red",
    "failed": "bold red",
}


def should_enable_tui(flag: bool, stream: Optional[IO] = None) -> bool:
    """Gate the Rich Live dashboard on ``--tui`` AND a TTY stream (INV-012).

    The run command MUST consult this helper before constructing
    :class:`TUI`. The default ``stream`` is :data:`sys.stdout`; tests
    pass an explicit non-TTY stream to exercise the off path without
    monkey-patching the global.

    A stream that does not expose ``isatty()`` (rare; ``io.StringIO``
    answers ``False``) is treated as non-TTY -- the conservative read
    keeps piped callers safe by default.
    """
    if not flag:
        return False
    target = stream if stream is not None else sys.stdout
    isatty = getattr(target, "isatty", None)
    if not callable(isatty):
        return False
    try:
        return bool(isatty())
    except Exception:
        return False


@dataclass
class WorkerSnapshot:
    """Per-worker view derived from the :class:`EventRecord` stream.

    Populated by :func:`_project_workers`. ``status`` mirrors the
    DM-013 :data:`WorkerStatus` Literal plus the synthetic
    ``"pending"`` / ``"running"`` values used pre-completion.
    """

    index: int
    status: str = "pending"
    model_label: str = ""
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    elapsed_ms: Optional[int] = None

    @property
    def elapsed_seconds(self) -> Optional[float]:
        """Best-available elapsed reading in seconds, or ``None``."""
        if self.elapsed_ms is not None:
            return self.elapsed_ms / 1000.0
        if self.started_at is None:
            return None
        end = self.finished_at if self.finished_at is not None else time.time()
        return max(0.0, end - self.started_at)


def _parse_timestamp(value: object) -> Optional[float]:
    """Convert an ISO 8601 timestamp from an :class:`EventRecord` to epoch s.

    The logging_ module stamps timestamps via
    ``datetime.now(timezone.utc).isoformat()`` which is
    fromisoformat-compatible on all supported Python versions. A
    trailing ``Z`` (used by ``state.py``) is normalized to ``+00:00``
    so both shapes parse uniformly.
    """
    if not isinstance(value, str) or not value:
        return None
    text = value
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text).timestamp()
    except ValueError:
        return None


def _project_workers(
    events: Iterable[EventRecord],
) -> dict[int, WorkerSnapshot]:
    """Fold an :class:`EventRecord` stream into per-worker snapshots.

    Only the three ``worker_*`` event types contribute; ``wave_transition``
    and ``terminal`` events are skipped (they are not per-worker).
    Unknown payload keys are ignored so the projection survives the
    payload-shape evolution downstream tasks may introduce.
    """
    workers: dict[int, WorkerSnapshot] = {}
    for event in events:
        idx = event.worker_index
        if idx is None:
            continue
        if event.event_type not in (
            "worker_start",
            "worker_progress",
            "worker_done",
        ):
            continue

        snap = workers.setdefault(idx, WorkerSnapshot(index=idx))
        ts = _parse_timestamp(event.timestamp)
        payload = event.payload or {}

        model_label = payload.get("model_label") or payload.get("model_id")
        if isinstance(model_label, str) and model_label and not snap.model_label:
            snap.model_label = model_label

        if event.event_type == "worker_start":
            if snap.status == "pending":
                snap.status = "running"
            if ts is not None and snap.started_at is None:
                snap.started_at = ts
        elif event.event_type == "worker_done":
            status = payload.get("status")
            snap.status = status if isinstance(status, str) and status else "success"
            if ts is not None:
                snap.finished_at = ts
            elapsed_ms = payload.get("elapsed_ms")
            if isinstance(elapsed_ms, int) and elapsed_ms >= 0:
                snap.elapsed_ms = elapsed_ms

    return workers


class TUI:
    """Rich Live dashboard for swarm execution.

    Constructed only when :func:`should_enable_tui` returns ``True``.
    The non-TTY / no-``--tui`` path routes around this class entirely
    so callers piping ``swarm run`` to a file or another process never
    see Rich-emitted ANSI bytes (INV-012).
    """

    def __init__(
        self,
        *,
        console: Optional[Console] = None,
        refresh_per_second: int = 2,
    ) -> None:
        self.console = console or Console()
        self._refresh = refresh_per_second
        self._live: Optional[Live] = None
        self._state: Optional[SwarmState] = None
        self._events: list[EventRecord] = []
        self._started_at: float = time.time()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> Live:
        """Start the Live display. Caller owns :meth:`stop`."""
        self._started_at = time.time()
        self._live = Live(
            self.render(self._state, self._events),
            console=self.console,
            refresh_per_second=self._refresh,
            screen=False,
            redirect_stdout=False,
            redirect_stderr=False,
        )
        self._live.start()
        return self._live

    def stop(self) -> None:
        """Stop the Live display. Idempotent."""
        if self._live is not None:
            self._live.stop()
            self._live = None

    def update(
        self,
        state: Optional[SwarmState],
        events: Iterable[EventRecord],
    ) -> None:
        """Refresh the dashboard with a fresh state + event snapshot."""
        self._state = state
        self._events = list(events)
        if self._live is not None:
            self._live.update(self.render(self._state, self._events))

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(
        self,
        state: Optional[SwarmState],
        events: Iterable[EventRecord],
    ) -> Panel:
        """Build the dashboard panel from ``state`` + ``events``.

        Pure -- no Live interaction -- so tests can assert the rendered
        shape without standing up a Console / Live pair.
        """
        workers = _project_workers(events)
        header = self._build_header(state, workers)
        table = self._build_worker_table(workers)
        body = Group(header, "", table)
        return Panel(
            body,
            title="[bold]SUPERCLAUDE SWARM[/]",
            border_style="blue",
            padding=(1, 2),
        )

    def _build_header(
        self,
        state: Optional[SwarmState],
        workers: dict[int, WorkerSnapshot],
    ) -> Text:
        state_value = state.state if state is not None else "-"
        job_id = state.job_id if state is not None else "-"
        elapsed = max(0.0, time.time() - self._started_at)
        return Text.from_markup(
            f"[dim]job:[/] [bold]{job_id or '-'}[/]    "
            f"[dim]state:[/] [bold]{state_value}[/]    "
            f"[dim]workers:[/] [bold]{len(workers)}[/]    "
            f"[dim]elapsed:[/] [bold]{elapsed:.1f}s[/]"
        )

    def _build_worker_table(
        self,
        workers: dict[int, WorkerSnapshot],
    ) -> Table:
        table = Table(
            show_header=True,
            header_style="bold",
            border_style="dim",
            pad_edge=False,
            box=None,
        )
        table.add_column("#", width=3, justify="right")
        table.add_column("Model", min_width=18)
        table.add_column("Status", width=12, justify="center")
        table.add_column("Elapsed", width=10, justify="right")

        for idx in sorted(workers):
            snap = workers[idx]
            style = _WORKER_STATUS_STYLES.get(snap.status, "")
            elapsed = snap.elapsed_seconds
            elapsed_display = f"{elapsed:.1f}s" if elapsed is not None else "-"
            table.add_row(
                str(idx),
                snap.model_label or "-",
                Text(snap.status, style=style),
                elapsed_display,
            )

        return table
