"""T07.01 -- ``cli/swarm/tui.py`` on/off paths.

Covers the acceptance criteria from
``.dev/releases/Current/MultiModelSwarm/tasklist/phase-7-tasklist.md``::

    - TUI renders only when ``--tui`` passed.
    - No terminal control sequences emitted on non-TTY stdout.
    - Dashboard shows per-worker status + elapsed.
    - ``tests/swarm/test_tui.py`` covers TUI on/off paths.

The INV-012 end-to-end subprocess audit lives in T07.03
(``test_inv012_tui_opt_in.py``); this file pins the per-helper unit
contract so a regression surfaces before the integration test runs.
"""

from __future__ import annotations

import io
import re

import pytest
from rich.console import Console

from superclaude.cli.swarm.models import EventRecord, SwarmState
from superclaude.cli.swarm.tui import (
    TUI,
    WorkerSnapshot,
    _project_workers,
    should_enable_tui,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


class _FakeTTY(io.StringIO):
    """In-memory stream that claims to be a TTY (for the on-path test)."""

    def isatty(self) -> bool:  # type: ignore[override]
        return True


def _render_to_string(tui: TUI, *, force_terminal: bool) -> str:
    """Render the panel through a captured Console at the given color setting."""
    buf = io.StringIO()
    console = Console(
        file=buf,
        force_terminal=force_terminal,
        color_system="truecolor" if force_terminal else None,
        width=120,
    )
    state = SwarmState(state="dispatching", job_id="job-tui-test")
    events = [
        EventRecord(
            event_type="worker_start",
            timestamp="2026-06-01T15:00:00+00:00",
            worker_index=0,
            payload={"model_label": "alpha-7b", "timeout_sec": 180},
        ),
        EventRecord(
            event_type="worker_done",
            timestamp="2026-06-01T15:00:03+00:00",
            worker_index=0,
            payload={"status": "success", "elapsed_ms": 3210},
        ),
        EventRecord(
            event_type="worker_start",
            timestamp="2026-06-01T15:00:01+00:00",
            worker_index=1,
            payload={"model_label": "beta-13b"},
        ),
    ]
    console.print(tui.render(state, events))
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Gate (--tui + TTY)
# ---------------------------------------------------------------------------


def test_should_enable_tui_flag_off_returns_false() -> None:
    """``--tui`` absent -> gate stays closed regardless of stream type."""
    assert should_enable_tui(False, _FakeTTY()) is False


def test_should_enable_tui_flag_on_non_tty_returns_false() -> None:
    """Non-TTY stream blocks the dashboard even when ``--tui`` is set."""
    plain = io.StringIO()  # StringIO.isatty() -> False
    assert should_enable_tui(True, plain) is False


def test_should_enable_tui_flag_on_tty_returns_true() -> None:
    """``--tui`` + TTY -> dashboard is allowed."""
    assert should_enable_tui(True, _FakeTTY()) is True


def test_should_enable_tui_handles_stream_without_isatty() -> None:
    """Conservative read: a stream missing ``isatty`` is treated as non-TTY."""

    class _NoIsAtty:
        pass

    assert should_enable_tui(True, _NoIsAtty()) is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Per-worker projection
# ---------------------------------------------------------------------------


def test_project_workers_status_and_elapsed_from_done_payload() -> None:
    """``worker_done.payload['elapsed_ms']`` takes precedence over timestamps."""
    events = [
        EventRecord(
            event_type="worker_start",
            timestamp="2026-06-01T15:00:00+00:00",
            worker_index=2,
            payload={"model_label": "gamma-mini"},
        ),
        EventRecord(
            event_type="worker_done",
            timestamp="2026-06-01T15:00:05+00:00",
            worker_index=2,
            payload={"status": "success", "elapsed_ms": 4200},
        ),
    ]
    projected = _project_workers(events)
    assert set(projected) == {2}
    snap = projected[2]
    assert isinstance(snap, WorkerSnapshot)
    assert snap.status == "success"
    assert snap.model_label == "gamma-mini"
    assert snap.elapsed_seconds == pytest.approx(4.2)


def test_project_workers_running_state_before_done() -> None:
    """A lone ``worker_start`` projects to ``running`` with elapsed from ts."""
    events = [
        EventRecord(
            event_type="worker_start",
            timestamp="2026-06-01T15:00:00+00:00",
            worker_index=0,
            payload={"model_id": "delta-v"},
        )
    ]
    snap = _project_workers(events)[0]
    assert snap.status == "running"
    assert snap.model_label == "delta-v"
    # Elapsed without finished_at falls back to wall-clock; must be non-None.
    assert snap.elapsed_seconds is not None and snap.elapsed_seconds >= 0.0


def test_project_workers_skips_non_per_worker_events() -> None:
    """``wave_transition`` / ``terminal`` events are not per-worker."""
    events = [
        EventRecord(
            event_type="wave_transition",
            timestamp="2026-06-01T15:00:00+00:00",
            worker_index=None,
            payload={"from": "preflight_ok", "to": "dispatching"},
        ),
        EventRecord(
            event_type="terminal",
            timestamp="2026-06-01T15:00:10+00:00",
            worker_index=None,
            payload={"status": "success"},
        ),
    ]
    assert _project_workers(events) == {}


def test_project_workers_done_without_status_defaults_to_success() -> None:
    """Missing/blank ``payload['status']`` falls back to ``success``."""
    events = [
        EventRecord(
            event_type="worker_start",
            timestamp="2026-06-01T15:00:00+00:00",
            worker_index=4,
            payload={},
        ),
        EventRecord(
            event_type="worker_done",
            timestamp="2026-06-01T15:00:01+00:00",
            worker_index=4,
            payload={"elapsed_ms": 800},
        ),
    ]
    snap = _project_workers(events)[4]
    assert snap.status == "success"
    assert snap.elapsed_seconds == pytest.approx(0.8)


# ---------------------------------------------------------------------------
# Render contract
# ---------------------------------------------------------------------------


def test_render_emits_no_ansi_on_non_terminal_console() -> None:
    """Rendering through a non-terminal Console produces zero ANSI bytes.

    Mirrors the INV-012 contract for piped callers: when the run command
    routes around :class:`TUI` (or renders to a plain console), the
    output must be free of terminal control sequences.
    """
    tui = TUI()
    rendered = _render_to_string(tui, force_terminal=False)
    assert _ANSI_RE.search(rendered) is None
    # Per-worker content must still be present so the test pins the
    # "TUI renders per-worker status + elapsed" acceptance.
    assert "alpha-7b" in rendered
    assert "beta-13b" in rendered
    assert "success" in rendered
    assert "running" in rendered
    # elapsed_ms=3210 renders as 3.2s
    assert "3.2s" in rendered


def test_render_emits_ansi_on_terminal_console() -> None:
    """When the gate is open (TTY console), Rich emits styled ANSI bytes."""
    tui = TUI()
    rendered = _render_to_string(tui, force_terminal=True)
    assert _ANSI_RE.search(rendered) is not None
    # Worker rows + state still surface in the styled output.
    assert "alpha-7b" in rendered
    assert "dispatching" in rendered


def test_render_handles_empty_event_stream() -> None:
    """An empty event stream still produces a panel (header + empty table)."""
    tui = TUI()
    buf = io.StringIO()
    console = Console(file=buf, force_terminal=False, width=120)
    console.print(tui.render(SwarmState(state="preflight_ok", job_id="job-empty"), []))
    out = buf.getvalue()
    assert "job-empty" in out
    assert "preflight_ok" in out
    # Header field labels remain stable across renders.
    assert "workers:" in out


def test_render_handles_missing_state() -> None:
    """``state=None`` is tolerated -- header shows ``-`` placeholders."""
    tui = TUI()
    buf = io.StringIO()
    console = Console(file=buf, force_terminal=False, width=120)
    console.print(tui.render(None, []))
    out = buf.getvalue()
    assert "job:" in out
    assert "state:" in out
