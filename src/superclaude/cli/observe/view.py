"""The view model: one pure function from a cycle result, a session and a clock to a ``View``.

Every spec status literal is defined here once (AD-8, AD-10); renderers only lay out and
truncate. This module does no I/O, holds no global state and reads time only through the
injected clock (``monotonic()``, ``wall()``, ``local_tz()``). It is the only module that
turns the ``UNKNOWN`` sentinel into screen words.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from enum import Enum
from typing import Any

from superclaude import __version__
from superclaude.cli.observe.parse import (  # noqa: F401  (UNKNOWN is re-exported)
    ORDER_UNKNOWN as ORDER_UNKNOWN_FLAG,
)
from superclaude.cli.observe.parse import (
    UNKNOWN,
    Coverage,
    Row,
    format_local,
    format_utc_iso,
    parse_timestamp,
)

KEY_NAMES = ("up", "down", "enter", "escape", "backspace", "ctrl_c", "text")

PRODUCER_NAME = "superclaude-observe"
STALE_SECONDS = (
    45.0  # three intervals without a successful poll, on the monotonic clock
)
HISTORICAL_STATES = ("released", "retained")
CHANGE_KEY_FIELDS = (
    "stage_worker",
    "stage_dispatch",
    "next_action_kind",
    "liveness_verdict",
)  # CD-2

# -- literals defined once ---------------------------------------------------------------------
GAP_NOTICE = (
    'Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"'
)
LEDGER_TITLE = "worker-reported, not questions"
NO_READ_YET = "no successful worker-list read yet"
EMPTY_NOTICE = "no observed items in this source window; not proof none exist"
NOT_AVAILABLE_TEXT = "NOT AVAILABLE (no Orca CLI validated)"
MESSAGES_CELL = "messages UNVERIFIED (not read)"
UNAVAILABLE = "unavailable (no source)"
ABSENT_IN_SOURCE = "unknown (absent in source)"
PARTIAL_CAP_TEXT = (
    "newest first; oldest rows not read; long-running active workers may be among them"
)
KEYS_LINE = "Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e export  q quit"
FROZEN_MARKER = "FROZEN"  # fixture mode only; no other state overrides it (T34)
INSPECTOR_TITLE = "INSPECTOR"
INSPECTOR_HELP = "Esc back  j/k move  d/u scroll  e export  q quit"
INSPECTOR_ABOVE_TEXT = "{n} lines above (u)"
INSPECTOR_BELOW_TEXT = "{n} more lines below (d)"
INSPECTOR_SCROLL_STEP = 3  # lines per d/u press
NO_MATCH_TEXT = "no rows match the filter or the historical setting"
SOURCE_COUNT_KEYS = ("active", "reclaimable", "retained", "released")
UNAVAILABLE_FACTS = ("report status", "acceptance", "tests", "approval")


@dataclass(frozen=True)
class Key:
    """One decoded key press. ``char`` is set only for ``text``."""

    name: str
    char: str = ""

    def __post_init__(self) -> None:
        if self.name not in KEY_NAMES:
            raise ValueError(f"unknown key name: {self.name!r}")
        if (self.name == "text") != bool(self.char):
            raise ValueError("char is required for text keys and forbidden for others")


@dataclass(frozen=True)
class Session:
    """What the user has done so far. Changed only by ``apply_cycle`` and ``apply_key``."""

    focus: str = "list"  # "list" | "inspector" | "filter"
    selected: tuple | None = None  # row identity, never an index
    selected_row: Any = None  # last-known ``Row`` of the selected identity
    filter_text: str = ""
    show_historical: bool = False
    baseline: Mapping | None = (
        None  # identity -> the four change-flag values; None before the first look
    )
    mark_wall_time: float | None = None
    marked: bool = False  # True once the user pressed ``m``
    inspector_scroll: int = 0  # inspector fields scrolled off the top (d/u keys)


@dataclass(frozen=True)
class CountsToken:
    text: str
    protected: bool  # protected tokens are never truncated


@dataclass(frozen=True)
class RowView:
    """One ledger row, display-ready, with the typed ``Row`` kept for the exports."""

    identity: tuple
    dispatch_id: str
    run: str
    worker_state: str
    dispatch_status: str
    terminal_state: str
    outcome: str
    next_action: str  # verbatim; blank or absent reads "unknown"
    liveness: str  # "verdict (source)"
    evidence_age: str
    flags: tuple[
        str, ...
    ]  # identity unknown, order unknown, conflict (time went back), not reobserved
    changed: bool  # the "*" marker
    frozen: bool  # fixture mode only
    historical: bool
    selected: bool
    inspector: tuple[tuple[str, str], ...]
    raw: Row


@dataclass(frozen=True)
class SnapshotMeta:
    """Typed (not display) values the JSON snapshot needs (AD-10, AD-12)."""

    cycle: int
    generated_at: str  # UTC ISO 8601
    producer_name: str
    producer_version: str
    namespace: str
    source_status: str  # "OK" | "STALE" | "ERROR" | "UNKNOWN"
    source_observed_at: Any  # UTC ISO 8601 or UNKNOWN
    source_error: str | None  # short code, only when source_status is "ERROR"
    has_more: Any
    total: Any
    limit: Any
    scope: Any
    counts: Any
    collection_state: str | None
    collection_collected: int | None
    collection_changed_during_read: bool | None
    collection_duplicates_ignored: int | None


@dataclass(frozen=True)
class Window:
    rows: tuple[RowView, ...]
    shown: int
    total: int
    more: int  # rows not shown, never counting the selected row
    text: str  # "x/y shown"
    more_text: str  # "+N more" or ""


@dataclass(frozen=True)
class View:
    mode: str
    variant: str | None
    meta: SnapshotMeta
    source_state: str  # NOT_AVAILABLE > NOT_POLLED > FAILED > STALE > OK
    as_of: str  # "HH:MM:SS" of the last good poll, or "never"
    scope_text: str
    synthetic_banner: str | None
    header1: str
    header2: str
    freshness_cells: tuple[str, ...]
    poll_age: str | None
    counts_tokens: tuple[CountsToken, ...]
    collected_text: str
    gap_notice: str
    ledger_title: str
    ledger_empty: tuple[str, ...]
    changes_line: str | None
    filter_line: str | None
    historical_note: str | None
    duplicates_note: str | None
    selection_note: str | None
    all_rows: tuple[RowView, ...]  # every merged row, newest first (AD-12 order)
    visible_rows: tuple[
        RowView, ...
    ]  # after filter and historical toggle, in source order
    selected: RowView | None
    focus: str
    filter_text: str
    show_historical: bool
    inspector: tuple[tuple[str, str], ...] | None
    help_line: str
    inspector_scroll: int = 0

    def window(self, capacity: int | None) -> Window:
        """The rows that fit ``capacity`` lines, always including the selected visible row."""
        rows = self.visible_rows
        total = len(rows)
        if capacity is None or capacity >= total:
            shown = rows
        else:
            capacity = max(capacity, 1)
            index = next((i for i, r in enumerate(rows) if r.selected), None)
            start = 0 if index is None or index < capacity else index - capacity + 1
            shown = rows[start : start + capacity]
        shown_ids = {r.identity for r in shown}
        selected_id = self.selected.identity if self.selected is not None else None
        more = sum(
            1 for r in rows if r.identity not in shown_ids and r.identity != selected_id
        )
        return Window(
            rows=shown,
            shown=len(shown),
            total=total,
            more=more,
            text=f"{len(shown)}/{total} shown",
            more_text=f"+{more} more" if more else "",
        )

    def footer_counts(self, window: Window) -> str:
        """The footer literal ``shown x/y | collected n / reported T`` ("x/y shown" is the overflow text)."""
        return f"shown {window.shown}/{window.total} | {self.collected_text}"

    def footer(self, window: Window) -> str:
        return f"{self.help_line}  {self.footer_counts(window)}"


# -- small helpers -------------------------------------------------------------------------------


def text_of(value: Any) -> str:
    """A source value as screen text: UNKNOWN reads ``unknown``; the text "unknown" is quoted."""
    if value is UNKNOWN:
        return "unknown"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return f'"{value}"' if value.strip().lower() == "unknown" else value
    return str(value)


def aggregate(count: int, unknown: int) -> str:
    """An aggregate with unknown members is never a clean number: ``n+? (k unknown)``."""
    return str(count) if unknown == 0 else f"{count}+? ({unknown} unknown)"


def format_age(seconds: float) -> str:
    whole = max(0, int(seconds))
    if whole < 60:
        return f"{whole}s"
    if whole < 3600:
        return f"{whole // 60}m"
    return f"{whole // 3600}h"


def code_label(code: str | None) -> str:
    """``exit:2`` -> ``exit 2``, ``spawn-error`` -> ``spawn error``."""
    return (code or "error").replace(":", " ").replace("-", " ")


def source_state(result: Any, clock: Any) -> str:
    state = result.state
    if state in ("NOT_AVAILABLE", "NOT_POLLED", "FAILED"):
        return state
    last = result.last_success_mono
    if last is None or clock.monotonic() - last >= STALE_SECONDS:
        return "STALE"
    return "OK"


def is_historical(row: Row) -> bool:
    return (
        isinstance(row.terminal_state, str) and row.terminal_state in HISTORICAL_STATES
    )


def change_key(row: Row) -> tuple:
    return tuple(getattr(row, name) for name in CHANGE_KEY_FIELDS)


def _sort_key(row: Row) -> tuple:
    stamp = parse_timestamp(row.liveness_observed_at)
    if stamp is None:
        stamp = parse_timestamp(row.evidence_last_observed_at)
    dispatch = row.dispatch_id if isinstance(row.dispatch_id, str) else ""
    return (0 if stamp is not None else 1, -(stamp or 0.0), dispatch, row.namespace)


def _field(row: Row, attr: str) -> str:
    value = getattr(row, attr)
    if value is UNKNOWN or attr in row.absent_fields:
        return ABSENT_IN_SOURCE
    return text_of(value)


def _inspector(row: Row, result: Any, snapshot: Any) -> tuple[tuple[str, str], ...]:
    lines: list[tuple[str, str]] = [
        ("dispatchId", _field(row, "dispatch_id")),
        ("taskId", _field(row, "task_id")),
        ("runId", _field(row, "run_id")),
        ("workerState", _field(row, "worker_state")),
        ("dispatchStatus", _field(row, "dispatch_status")),
        ("terminalState", _field(row, "terminal_state")),
        ("projection.outcome", _field(row, "outcome")),
        ("projection.nextAction.kind", _field(row, "next_action_kind")),
        ("resource.worktreeId", _field(row, "worktree_id")),
        ("resource.ownerDispatchId", _field(row, "owner_dispatch_id")),
        ("resource.originDispatchId", _field(row, "origin_dispatch_id")),
        ("projection.host.id", _field(row, "host_id")),
        ("projection.workspace.id", _field(row, "workspace_id")),
        ("projection.stage.worker (worker-reported)", _field(row, "stage_worker")),
        ("projection.stage.dispatch (worker-reported)", _field(row, "stage_dispatch")),
        ("projection.stage.activity (worker-reported)", _field(row, "stage_activity")),
        ("projection.stage.detail (worker-reported)", _field(row, "stage_detail")),
        ("unrecognised keys", f"{row.unrecognised_keys} unrecognised keys"),
    ]
    flags = row.flags + (() if row.reobserved else ("not reobserved",))
    if flags:
        lines.append(("flags", ", ".join(flags)))
    lines.extend((fact, UNAVAILABLE) for fact in UNAVAILABLE_FACTS)
    if snapshot is not None:
        lines.extend(("source warning", warning) for warning in snapshot.warnings)
    if result.diagnostic:
        lines.append(("last poll error (sanitized)", result.diagnostic))
    return tuple(lines)


def _next_action_text(row: Row) -> str:
    value = row.next_action_kind
    if value is UNKNOWN or not str(value).strip():
        return "unknown"  # absent or blank
    return text_of(value)


def _row_view(
    row: Row,
    *,
    result: Any,
    snapshot: Any,
    clock: Any,
    selected: bool,
    changed: bool,
    mode: str,
    force_not_reobserved: bool = False,
) -> RowView:
    stamp = parse_timestamp(row.evidence_last_observed_at)
    age = "unknown" if stamp is None else format_age(clock.wall() - stamp)
    frozen = bool(row.fixture_frozen) and mode == "fixture"
    flags = (
        ((FROZEN_MARKER,) if frozen else ())
        + row.flags
        + (() if row.reobserved and not force_not_reobserved else ("not reobserved",))
    )
    return RowView(
        identity=row.identity,
        dispatch_id=text_of(row.dispatch_id),
        run=text_of(row.run_id),
        worker_state=text_of(row.worker_state),
        dispatch_status=text_of(row.dispatch_status),
        terminal_state=text_of(row.terminal_state),
        outcome=text_of(row.outcome),
        next_action=_next_action_text(row),
        liveness=f"{text_of(row.liveness_verdict)} ({text_of(row.liveness_source)})",
        evidence_age=age,
        flags=flags,
        changed=changed,
        frozen=frozen,
        historical=is_historical(row),
        selected=selected,
        inspector=_inspector(row, result, snapshot),
        raw=row,
    )


def _matches(view: RowView, text: str) -> bool:
    if not text:
        return True
    cells = (
        view.dispatch_id,
        view.run,
        view.worker_state,
        view.dispatch_status,
        view.terminal_state,
        view.outcome,
        view.next_action,
        view.liveness,
    )
    return text.lower() in " ".join(cells).lower()


def _scope_text(snapshot: Any) -> tuple[str, bool]:
    scope = snapshot.scope if snapshot is not None else UNKNOWN
    source = scope.get("source") if isinstance(scope, dict) else None
    if not isinstance(source, str) or not source:
        return "scope unknown", False
    return f"scope={source}", source == "bound"


def _partial_text(coverage: Coverage) -> str | None:
    if not coverage.partial:
        return None
    total = coverage.reported_total
    reported = f"reported {total}" if isinstance(total, int) else "reported unknown"
    error = coverage.stopped_by_error
    if coverage.empty_page is not None:
        return f"PARTIAL (empty page {coverage.empty_page})"
    if error == "cursor-stalled":
        return f"PARTIAL (cursor missing or not advancing, page {coverage.pages_read})"
    if error == "cursor-rejected":
        return f"PARTIAL (cursor rejected, page {coverage.pages_read})"
    if error is not None:
        return f"PARTIAL ({code_label(error)}, page {coverage.pages_read})"
    return f"PARTIAL: collected {coverage.collected} of {reported} ({PARTIAL_CAP_TEXT})"


def _collected_text(coverage: Coverage | None) -> str:
    """The ``collected n / reported T`` text."""
    if coverage is None:
        return "collected unknown / reported unknown"
    known = [t for t in coverage.page_totals if isinstance(t, int)]
    if coverage.total_changed:
        reported = f"reported {known[0]}-{known[-1]} (changed during read)"
    elif isinstance(coverage.reported_total, int):
        reported = f"reported {coverage.reported_total}"
        if coverage.pages_read > 1:
            reported += f" (page {coverage.pages_read})"
    else:
        reported = "reported unknown"
    text = f"collected {coverage.collected} / {reported}"
    if coverage.mismatch and not coverage.total_changed:
        text += " (mismatch)"
    return text


def _freshness(result: Any, clock: Any, state: str) -> tuple[str, str | None]:
    age = (
        None
        if result.last_success_mono is None
        else format_age(clock.monotonic() - result.last_success_mono)
    )
    if state == "NOT_AVAILABLE":
        return f"worker-list {NOT_AVAILABLE_TEXT}", None
    if state == "NOT_POLLED":
        return "worker-list NOT POLLED", None
    if state == "FAILED":
        cell = f"worker-list FAILED ({code_label(result.code)})"
    else:
        cell = f"worker-list {state}"
    return (f"{cell} {age}" if age else cell), age


def _meta(
    result: Any, snapshot: Any, coverage: Coverage | None, state: str, clock: Any
) -> SnapshotMeta:
    status = {"OK": "OK", "STALE": "STALE", "FAILED": "ERROR"}.get(state, "UNKNOWN")
    observed = (
        UNKNOWN
        if result.last_success_wall is None
        else format_utc_iso(result.last_success_wall)
    )
    return SnapshotMeta(
        cycle=result.cycle,
        generated_at=format_utc_iso(clock.wall()),
        producer_name=PRODUCER_NAME,
        producer_version=__version__,
        namespace=result.namespace,
        source_status=status,
        source_observed_at=observed,
        source_error=result.code if status == "ERROR" else None,
        has_more=snapshot.has_more if snapshot is not None else UNKNOWN,
        total=snapshot.total if snapshot is not None else UNKNOWN,
        limit=snapshot.limit if snapshot is not None else UNKNOWN,
        scope=snapshot.scope if snapshot is not None else UNKNOWN,
        counts=snapshot.counts if snapshot is not None else UNKNOWN,
        collection_state=coverage.state if coverage is not None else None,
        collection_collected=coverage.collected if coverage is not None else None,
        collection_changed_during_read=coverage.total_changed
        if coverage is not None
        else None,
        collection_duplicates_ignored=coverage.duplicates
        if coverage is not None
        else None,
    )


def _source_counts_text(snapshot: Any) -> str:
    counts = snapshot.counts if snapshot is not None else UNKNOWN
    if not isinstance(counts, dict):
        return "source counts: unknown"
    parts = [
        f"{key} {text_of(counts[key]) if key in counts else 'unknown'}"
        for key in SOURCE_COUNT_KEYS
    ]
    return "source counts: " + " / ".join(parts)


def _changes(rows: tuple[Row, ...], session: Session) -> tuple[frozenset, int]:
    """(identities of rows to star, k for ``changed since``): added, removed or changed rows."""
    baseline = session.baseline
    if baseline is None:
        return frozenset(), 0
    current = {
        r.identity: r for r in rows if not r.identity_unknown
    }  # no identity, no tracking
    flagged = {
        i
        for i, r in current.items()
        if i not in baseline or baseline[i] != change_key(r)
    }
    removed = sum(1 for i in baseline if i not in current)
    return frozenset(flagged), len(flagged) + removed


def build_view(result: Any, session: Session, clock: Any) -> View:
    """Pure: the same inputs always give an equal ``View``. ``result`` is a ``CycleResult``."""
    snapshot = result.snapshot
    coverage = result.coverage
    state = source_state(result, clock)
    rows: tuple[Row, ...] = snapshot.rows if snapshot is not None else ()
    tz = clock.local_tz()
    mode = result.mode

    scope_text, bound = _scope_text(snapshot)
    as_of = (
        "never"
        if result.last_success_wall is None
        else format_local(result.last_success_wall, tz, "%H:%M:%S")
    )
    banner = (
        f"SYNTHETIC FIXTURE {result.fixture_variant}, not Orca data"
        if mode == "fixture"
        else None
    )
    header_parts = ["ORCA OBSERVER", f"mode={mode}"]
    if banner:
        header_parts.append(banner)
    header_parts.append(scope_text)
    if bound:
        header_parts.append("one Run only")
    header_parts.append(f"as of {as_of}")
    header1 = "  ".join(header_parts)

    fresh_cell, age = _freshness(result, clock, state)
    cells = [fresh_cell, MESSAGES_CELL]
    if snapshot is not None and snapshot.warnings:
        cells.append(f"source warnings: {len(snapshot.warnings)} (inspector)")
    if result.code == "overrun":
        cells.append(f"cycle overran ({int(result.duration)}s)")
    header2 = "  ".join(cells)

    collected_text = _collected_text(coverage)
    tokens = [CountsToken(collected_text, True)]
    partial = _partial_text(coverage) if coverage is not None else None
    if partial:
        tokens.append(CountsToken(partial, True))
    tokens.append(CountsToken(scope_text, True))
    tokens.append(CountsToken(_source_counts_text(snapshot), False))
    if snapshot is not None:
        runs = {r.run_id for r in rows if r.run_id is not UNKNOWN}
        unknown_runs = sum(1 for r in rows if r.run_id is UNKNOWN)
        tokens.append(
            CountsToken(f"runs seen: {aggregate(len(runs), unknown_runs)}", False)
        )
    tokens.append(CountsToken(f"SETTLED {UNAVAILABLE}", False))
    tokens.append(CountsToken(f"POLICY FROZEN {UNAVAILABLE}", False))
    tokens.append(CountsToken("cost unavailable", False))

    flagged, changed_k = _changes(rows, session)
    changes_line = None
    if session.baseline is not None and session.mark_wall_time is not None:
        hhmm = format_local(session.mark_wall_time, tz, "%H:%M")
        changes_line = f"changed since {hhmm} ({changed_k})"
        if not session.marked:
            changes_line = f"new baseline at {hhmm} (observer started) | {changes_line}"

    def make(row: Row, **extra: Any) -> RowView:
        return _row_view(
            row,
            result=result,
            snapshot=snapshot,
            clock=clock,
            selected=row.identity == session.selected,
            changed=row.identity in flagged,
            mode=mode,
            **extra,
        )

    source_order = tuple(make(r) for r in rows)
    all_rows = tuple(sorted(source_order, key=lambda rv: _sort_key(rv.raw)))
    matching = tuple(rv for rv in source_order if _matches(rv, session.filter_text))
    hidden_historical = (
        0 if session.show_historical else sum(1 for rv in matching if rv.historical)
    )
    visible = tuple(
        rv for rv in matching if session.show_historical or not rv.historical
    )

    filter_line = None
    if session.filter_text:
        filter_line = f"filter {session.filter_text}: {len(matching)} of {len(source_order)} collected"
    duplicates = coverage.duplicates if coverage is not None else 0

    selected_view = next(
        (rv for rv in source_order if rv.identity == session.selected), None
    )
    selection_note = None
    placeholder = False
    if (
        selected_view is None
        and session.selected is not None
        and session.selected_row is not None
    ):
        selected_view = make(session.selected_row, force_not_reobserved=True)
        placeholder = True
    if selected_view is not None and (placeholder or not selected_view.raw.reobserved):
        # Gone from the source window, or read in an earlier cycle only: stays selected.
        selection_note = (
            f"selected {selected_view.dispatch_id} no longer in source window"
        )

    if rows:
        ledger_empty: tuple[str, ...] = ()
    elif result.last_success_mono is None:
        ledger_empty = (NO_READ_YET,)
    else:
        ledger_empty = (EMPTY_NOTICE, f"worker-list returned 0 workers in {scope_text}")

    return View(
        mode=mode,
        variant=result.fixture_variant,
        meta=_meta(result, snapshot, coverage, state, clock),
        source_state=state,
        as_of=as_of,
        scope_text=scope_text,
        synthetic_banner=banner,
        header1=header1,
        header2=header2,
        freshness_cells=tuple(cells),
        poll_age=age,
        counts_tokens=tuple(tokens),
        collected_text=collected_text,
        gap_notice=GAP_NOTICE,
        ledger_title=LEDGER_TITLE,
        ledger_empty=ledger_empty,
        changes_line=changes_line,
        filter_line=filter_line,
        historical_note=f"{hidden_historical} historical hidden (h)"
        if hidden_historical
        else None,
        duplicates_note=f"{duplicates} duplicate rows ignored" if duplicates else None,
        selection_note=selection_note,
        all_rows=all_rows,
        visible_rows=visible,
        selected=selected_view,
        focus=session.focus,
        filter_text=session.filter_text,
        show_historical=session.show_historical,
        inspector=selected_view.inspector
        if session.focus == "inspector" and selected_view is not None
        else None,
        help_line=KEYS_LINE,
        inspector_scroll=session.inspector_scroll,
    )


# -- session transitions: the only two ways a Session changes (AD-15) -----------------------


class Effect(Enum):
    """What the loop must do after a key; no effect ever reaches Orca."""

    NONE = "none"
    EXPORT = "export"
    QUIT = "quit"


def _baseline_of(rows: Any) -> dict:
    return {r.identity: change_key(r) for r in rows if not r.identity_unknown}


def apply_cycle(session: Session, result: Any, clock: Any) -> Session:
    """A new cycle arrived: take the baseline on the first successful look, refresh the selection."""
    snapshot = result.snapshot
    changes: dict[str, Any] = {}
    if (
        session.baseline is None
        and snapshot is not None
        and result.last_success_mono is not None
    ):
        changes.update(
            baseline=_baseline_of(snapshot.rows),
            mark_wall_time=clock.wall(),
            marked=False,
        )
    if snapshot is not None and session.selected is not None:
        fresh = next((r for r in snapshot.rows if r.identity == session.selected), None)
        if fresh is not None:
            changes["selected_row"] = fresh  # last-known values follow the source
    return replace(session, **changes)


def _move(session: Session, view: View, step: int) -> Session:
    rows = view.visible_rows
    if not rows:
        return replace(session)
    index = next(
        (i for i, r in enumerate(rows) if r.identity == session.selected), None
    )
    if index is None:  # nothing selected, or the selection is not in the list
        target = 0 if step > 0 else len(rows) - 1
    else:
        target = min(max(index + step, 0), len(rows) - 1)
    row = rows[target]
    return replace(
        session, selected=row.identity, selected_row=row.raw, inspector_scroll=0
    )


def inspector_line_bound(fields: tuple[tuple[str, str], ...]) -> int:
    """An upper bound on the wrapped inspector lines at the narrowest width (80 columns).

    The view knows no width, so the scroll limit uses this; the renderer clamps to the real
    count, so an overshoot only costs a press or two of ``u`` at the end.
    """
    return sum(-(-(len(label) + 2 + len(value)) // 60) or 1 for label, value in fields)


def _filter_key(session: Session, key: Key) -> Session:
    if key.name == "text":
        return replace(session, filter_text=session.filter_text + key.char)
    if key.name == "backspace":
        return replace(session, filter_text=session.filter_text[:-1])
    if key.name in ("enter", "escape"):
        return replace(session, focus="list")
    return replace(session)  # arrows and the rest do nothing while typing


def apply_key(
    session: Session, key: Key, view: View, clock: Any
) -> tuple[Session, Effect]:
    """One key press. Keys change the session only; there is no refresh key and none reaches Orca."""
    if key.name == "ctrl_c":
        return replace(session), Effect.QUIT
    if session.focus == "filter":
        return _filter_key(session, key), Effect.NONE
    name = key.name
    char = key.char if name == "text" else ""
    inspecting = session.focus == "inspector"
    if name == "up" or char == "k":
        return _move(session, view, -1), Effect.NONE
    if name == "down" or char == "j":
        return _move(session, view, 1), Effect.NONE
    if inspecting and char in ("d", "u") and view.inspector:
        step = INSPECTOR_SCROLL_STEP if char == "d" else -INSPECTOR_SCROLL_STEP
        top = session.inspector_scroll + step
        top = min(max(top, 0), max(inspector_line_bound(view.inspector) - 1, 0))
        return replace(session, inspector_scroll=top), Effect.NONE
    if char == "q":
        return replace(session), Effect.QUIT
    if char == "e":
        return replace(session), Effect.EXPORT
    if char == "m":
        rows = tuple(rv.raw for rv in view.all_rows)
        return (
            replace(
                session,
                baseline=_baseline_of(rows),
                mark_wall_time=clock.wall(),
                marked=True,
            ),
            Effect.NONE,
        )
    if name == "escape" and inspecting:
        return replace(session, focus="list", inspector_scroll=0), Effect.NONE
    if not inspecting:
        if name == "enter" and view.selected is not None:
            return replace(session, focus="inspector", inspector_scroll=0), Effect.NONE
        if char == "/":
            return replace(session, focus="filter"), Effect.NONE
        if char == "h":
            return replace(
                session, show_historical=not session.show_historical
            ), Effect.NONE
    return replace(session), Effect.NONE
