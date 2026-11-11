a47a7bb1e3d1e65ebbaed540aefa159ab0bd7615
Review one task for spec compliance.

Task brief: 
## Task 8: Build the view model in `view.py`

Depends on: Task 7

Extend `src/superclaude/cli/observe/view.py` (it holds only `Key` from Task 1) and create `tests/observe/test_view.py`, following `ARCHITECTURE-SPINE.md` AD-8, AD-10, AD-20, CD-2, CD-10 and CD-16, `rendering-rules.md` (sections "Common to every width", "Worker ledger", "Changes since last look", "Unknown, stale, partial") and tests T9, T11, T13, T14, T15, T18, T20, T21, T31, T33, T34, T38, T42, T43 and T47 (gap-notice half) in `acceptance-tests.md`. Define frozen `Session` (focus mode, selected identity and its last-known values, filter text, show-historical flag, baseline mapping from identity to the four change-flag values or none, `mark_wall_time`) and `View`, and the pure `build_view(result, session, clock) -> View`: no I/O, no global state, time only through the injected clock. `View` carries every typed snapshot field Task 11 exports as full values, not display strings (`cycle`, `generatedAt` from the injected wall clock in UTC ISO 8601, producer name and package version, `source.namespace`, the source status and its short error code, `source.observedAt`, `page.hasMore`, `page.total`, `page.limit`, `scope`, the `counts` map and the `collection.*` values; `ARCHITECTURE-SPINE.md` AD-10), a `FROZEN` marker per row taken from `fixture_frozen`, and display-ready values: header line 1 and 2 strings, the COUNTS strip tokens in priority order, coverage strings, the freshness cell (`OK`, `STALE`, `FAILED (<code>)`, `NOT POLLED`, `NOT AVAILABLE (no Orca CLI validated)` with precedence NOT_AVAILABLE, NOT_POLLED, FAILED, STALE, OK; STALE when 45 s or more have passed on `clock.monotonic()` since `last_success_mono`), poll age and per-row evidence age as separate facts, `all_rows` (every merged row, timestamp order) and `visible_rows` (after the filter and the historical toggle, in source order), per-row cells with absent values as `unknown` and a source value that is itself the text `unknown` shown quoted, the verbatim `nextAction.kind` (blank or absent reads `unknown`), the changed-since-mark flags and `changed since HH:MM (k)`, the historical-hidden count, `x/y shown` and `+N more` (never counting the selected visible row), the footer `shown x/y | collected n / reported T`, the inspector fields (`dispatchId`, `taskId`, `runId`, `resource.worktreeId`, `resource.ownerDispatchId`, `resource.originDispatchId`, `projection.host.id`, `projection.workspace.id`, `projection.stage.*` labelled `worker-reported`, `n unrecognised keys`, absent fields as `unknown (absent in source)`, sanitized warnings and stderr), the gap notice `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`, the ledger title `worker-reported, not questions`, and every literal listed in `ARCHITECTURE-SPINE.md` AD-8 (PARTIAL, mismatch, `PARTIAL (empty page k)`, `reported unknown`, `reported T (page k)`, `reported T1-T2 (changed during read)`, `PARTIAL (cursor missing or not advancing, page k)`, `PARTIAL (cursor rejected, page k)`, `cycle overran (Ns)`, `filter <expr>: k of n collected`, `k historical hidden (h)`, `k duplicate rows ignored`, `one Run only` and `scope unknown`). Historical means `terminalState` exactly `released` or `retained`; any other or absent value is shown with its raw value and is never counted active. Before the first successful poll the header reads `as of never`, the counts read `collected unknown / reported unknown` and the ledger area `no successful worker-list read yet`. Live mode renders report status, acceptance, tests and approval, SETTLED and POLICY FROZEN as `unavailable (no source)` and cost as `cost unavailable`; fixture mode renders a `FROZEN` marker for rows flagged by the fixture. `empty` renders `no observed items in this source window; not proof none exist` and `worker-list returned 0 workers in scope=bound` names the scope. `view.py` re-exports `UNKNOWN` and is the only module that turns it into a screen word.

Acceptance criteria:
- [T8.AC1] `uv run pytest tests/observe/test_view.py -v` passes.
- [T8.AC2] T13: for the `missing-fields` variant every absent field renders `unknown` and the strings `0` and `false` never stand in for one (asserted per field); an aggregate with k unknown members renders `n+? (k unknown)` (T38).
- [T8.AC3] T14 and T15: a row with `terminalState=released` and no `outcome` never renders `done`, `complete` or `settled`; report, acceptance, tests and approval render `unavailable (no source)` live and no row renders `admitted`.
- [T8.AC4] T18: `page.total=287` with 100 rows renders `collected 100 / reported 287` and never `287 workers`; an absent total renders `reported unknown`.
- [T8.AC5] T9 and T47 (gap half): live mode shows the gap notice and the ledger title `worker-reported, not questions`, and no number derives from any message source or `result.count`.
- [T8.AC6] T11: after failing cycles the rows remain, the freshness cell reads `STALE <age>` or `FAILED (<code>) <age>`, values keep their last reading qualified `as of HH:MM:SS`, and no value becomes `failed`.
- [T8.AC7] T42: a successful poll with 20-minute-old worker evidence shows the poll age and the evidence age separately and the source is not STALE.
- [T8.AC8] T20 and CD-16: in `shared-unmapped` the two rows stay two rows, each inspector shows the same `resource.worktreeId`, the row without one shows `unknown (absent in source)`, no count divides one by the other and no `conflict` label appears.
- [T8.AC9] T21: historical rows are hidden by default with `k historical hidden (h)` and listed with their `terminalState` when the toggle is on; the source counts never change with the toggle.
- [T8.AC10] T31: cost reads `cost unavailable`, never `$0`, and elapsed time renders only as a plain age.
- [T8.AC11] T33 and T34: the `empty` text is exact, and `FROZEN` appears in fixture mode while live mode shows `unavailable (no source)` for SETTLED and POLICY FROZEN.
- [T8.AC12] T43: with the selected row visible and others hidden, `+N more` excludes the selected row.
- [T8.AC13] A test shows the same inputs build equal `View` objects twice and that `build_view` makes no call to `time`, `datetime` or the filesystem (module scan plus a clock that raises on unexpected use).
- [T8.AC14] A test builds a `View` from a `CycleResult` and shows every typed snapshot field listed above is present on it as a full value, so `export.py` needs nothing from `parse.py`, and that a row's `FROZEN` marker follows its `fixture_frozen`.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: a47a7bb1e3d1e65ebbaed540aefa159ab0bd7615
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/parse.py b/src/superclaude/cli/observe/parse.py
index d4f29ca38..1947ff42c 100644
--- a/src/superclaude/cli/observe/parse.py
+++ b/src/superclaude/cli/observe/parse.py
@@ -263,6 +263,16 @@ def parse_timestamp(value: Any) -> float | None:
     return None
 
 
+def format_utc_iso(epoch: float) -> str:
+    """Epoch seconds as UTC ISO 8601, whole seconds, e.g. ``2026-11-08T12:00:03Z``."""
+    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
+
+
+def format_local(epoch: float, tz: Any, pattern: str) -> str:
+    """Epoch seconds as local time in ``tz`` (a tzinfo from the injected clock)."""
+    return datetime.fromtimestamp(epoch, tz).strftime(pattern)
+
+
 # -- parsing --------------------------------------------------------------------------
 
 
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index 11b3e4e29..9647c3820 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -1,11 +1,59 @@
-"""View model for the observer. Later tasks add ``Session``, ``View`` and the pure builders."""
+"""The view model: one pure function from a cycle result, a session and a clock to a ``View``.
+
+Every spec status literal is defined here once (AD-8, AD-10); renderers only lay out and
+truncate. This module does no I/O, holds no global state and reads time only through the
+injected clock (``monotonic()``, ``wall()``, ``local_tz()``). It is the only module that
+turns the ``UNKNOWN`` sentinel into screen words.
+"""
 
 from __future__ import annotations
 
+from collections.abc import Mapping
 from dataclasses import dataclass
+from typing import Any
+
+from superclaude import __version__
+from superclaude.cli.observe.parse import (  # noqa: F401  (UNKNOWN is re-exported)
+    UNKNOWN,
+    Coverage,
+    Row,
+    format_local,
+    format_utc_iso,
+    parse_timestamp,
+)
 
 KEY_NAMES = ("up", "down", "enter", "escape", "backspace", "ctrl_c", "text")
 
+PRODUCER_NAME = "superclaude-observe"
+STALE_SECONDS = (
+    45.0  # three intervals without a successful poll, on the monotonic clock
+)
+HISTORICAL_STATES = ("released", "retained")
+CHANGE_KEY_FIELDS = (
+    "stage_worker",
+    "stage_dispatch",
+    "next_action_kind",
+    "liveness_verdict",
+)  # CD-2
+
+# -- literals defined once ---------------------------------------------------------------------
+GAP_NOTICE = (
+    'Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"'
+)
+LEDGER_TITLE = "worker-reported, not questions"
+NO_READ_YET = "no successful worker-list read yet"
+EMPTY_NOTICE = "no observed items in this source window; not proof none exist"
+NOT_AVAILABLE_TEXT = "NOT AVAILABLE (no Orca CLI validated)"
+MESSAGES_CELL = "messages UNVERIFIED (not read)"
+UNAVAILABLE = "unavailable (no source)"
+ABSENT_IN_SOURCE = "unknown (absent in source)"
+PARTIAL_CAP_TEXT = (
+    "newest first; oldest rows not read; long-running active workers may be among them"
+)
+KEYS_LINE = "Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e export  q quit"
+SOURCE_COUNT_KEYS = ("active", "reclaimable", "retained", "released")
+UNAVAILABLE_FACTS = ("report status", "acceptance", "tests", "approval")
+
 
 @dataclass(frozen=True)
 class Key:
@@ -19,3 +67,576 @@ class Key:
             raise ValueError(f"unknown key name: {self.name!r}")
         if (self.name == "text") != bool(self.char):
             raise ValueError("char is required for text keys and forbidden for others")
+
+
+@dataclass(frozen=True)
+class Session:
+    """What the user has done so far. Changed only by ``apply_cycle`` and ``apply_key``."""
+
+    focus: str = "list"  # "list" | "inspector" | "filter"
+    selected: tuple | None = None  # row identity, never an index
+    selected_row: Any = None  # last-known ``Row`` of the selected identity
+    filter_text: str = ""
+    show_historical: bool = False
+    baseline: Mapping | None = (
+        None  # identity -> the four change-flag values; None before the first look
+    )
+    mark_wall_time: float | None = None
+    marked: bool = False  # True once the user pressed ``m``
+
+
+@dataclass(frozen=True)
+class CountsToken:
+    text: str
+    protected: bool  # protected tokens are never truncated
+
+
+@dataclass(frozen=True)
+class RowView:
+    """One ledger row, display-ready, with the typed ``Row`` kept for the exports."""
+
+    identity: tuple
+    dispatch_id: str
+    run: str
+    worker_state: str
+    dispatch_status: str
+    terminal_state: str
+    outcome: str
+    next_action: str  # verbatim; blank or absent reads "unknown"
+    liveness: str  # "verdict (source)"
+    evidence_age: str
+    flags: tuple[
+        str, ...
+    ]  # identity unknown, order unknown, conflict (time went back), not reobserved
+    changed: bool  # the "*" marker
+    frozen: bool  # fixture mode only
+    historical: bool
+    selected: bool
+    inspector: tuple[tuple[str, str], ...]
+    raw: Row
+
+
+@dataclass(frozen=True)
+class SnapshotMeta:
+    """Typed (not display) values the JSON snapshot needs (AD-10, AD-12)."""
+
+    cycle: int
+    generated_at: str  # UTC ISO 8601
+    producer_name: str
+    producer_version: str
+    namespace: str
+    source_status: str  # "OK" | "STALE" | "ERROR" | "UNKNOWN"
+    source_observed_at: Any  # UTC ISO 8601 or UNKNOWN
+    source_error: str | None  # short code, only when source_status is "ERROR"
+    has_more: Any
+    total: Any
+    limit: Any
+    scope: Any
+    counts: Any
+    collection_state: str | None
+    collection_collected: int | None
+    collection_changed_during_read: bool | None
+    collection_duplicates_ignored: int | None
+
+
+@dataclass(frozen=True)
+class Window:
+    rows: tuple[RowView, ...]
+    shown: int
+    total: int
+    more: int  # rows not shown, never counting the selected row
+    text: str  # "x/y shown"
+    more_text: str  # "+N more" or ""
+
+
+@dataclass(frozen=True)
+class View:
+    mode: str
+    variant: str | None
+    meta: SnapshotMeta
+    source_state: str  # NOT_AVAILABLE > NOT_POLLED > FAILED > STALE > OK
+    as_of: str  # "HH:MM:SS" of the last good poll, or "never"
+    scope_text: str
+    synthetic_banner: str | None
+    header1: str
+    header2: str
+    freshness_cells: tuple[str, ...]
+    poll_age: str | None
+    counts_tokens: tuple[CountsToken, ...]
+    collected_text: str
+    gap_notice: str
+    ledger_title: str
+    ledger_empty: tuple[str, ...]
+    changes_line: str | None
+    filter_line: str | None
+    historical_note: str | None
+    duplicates_note: str | None
+    selection_note: str | None
+    all_rows: tuple[RowView, ...]  # every merged row, newest first (AD-12 order)
+    visible_rows: tuple[
+        RowView, ...
+    ]  # after filter and historical toggle, in source order
+    selected: RowView | None
+    focus: str
+    filter_text: str
+    show_historical: bool
+    inspector: tuple[tuple[str, str], ...] | None
+    help_line: str
+
+    def window(self, capacity: int | None) -> Window:
+        """The rows that fit ``capacity`` lines, always including the selected visible row."""
+        rows = self.visible_rows
+        total = len(rows)
+        if capacity is None or capacity >= total:
+            shown = rows
+        else:
+            capacity = max(capacity, 1)
+            index = next((i for i, r in enumerate(rows) if r.selected), None)
+            start = 0 if index is None or index < capacity else index - capacity + 1
+            shown = rows[start : start + capacity]
+        shown_ids = {r.identity for r in shown}
+        selected_id = self.selected.identity if self.selected is not None else None
+        more = sum(
+            1 for r in rows if r.identity not in shown_ids and r.identity != selected_id
+        )
+        return Window(
+            rows=shown,
+            shown=len(shown),
+            total=total,
+            more=more,
+            text=f"{len(shown)}/{total} shown",
+            more_text=f"+{more} more" if more else "",
+        )
+
+    def footer(self, window: Window) -> str:
+        return f"{self.help_line}  {window.text} | {self.collected_text}"
+
+
+# -- small helpers -------------------------------------------------------------------------------
+
+
+def text_of(value: Any) -> str:
+    """A source value as screen text: UNKNOWN reads ``unknown``; the text "unknown" is quoted."""
+    if value is UNKNOWN:
+        return "unknown"
+    if isinstance(value, bool):
+        return "true" if value else "false"
+    if isinstance(value, str):
+        return f'"{value}"' if value.strip().lower() == "unknown" else value
+    return str(value)
+
+
+def aggregate(count: int, unknown: int) -> str:
+    """An aggregate with unknown members is never a clean number: ``n+? (k unknown)``."""
+    return str(count) if unknown == 0 else f"{count}+? ({unknown} unknown)"
+
+
+def format_age(seconds: float) -> str:
+    whole = max(0, int(seconds))
+    if whole < 60:
+        return f"{whole}s"
+    if whole < 3600:
+        return f"{whole // 60}m"
+    return f"{whole // 3600}h"
+
+
+def code_label(code: str | None) -> str:
+    """``exit:2`` -> ``exit 2``, ``spawn-error`` -> ``spawn error``."""
+    return (code or "error").replace(":", " ").replace("-", " ")
+
+
+def source_state(result: Any, clock: Any) -> str:
+    state = result.state
+    if state in ("NOT_AVAILABLE", "NOT_POLLED", "FAILED"):
+        return state
+    last = result.last_success_mono
+    if last is None or clock.monotonic() - last >= STALE_SECONDS:
+        return "STALE"
+    return "OK"
+
+
+def is_historical(row: Row) -> bool:
+    return (
+        isinstance(row.terminal_state, str) and row.terminal_state in HISTORICAL_STATES
+    )
+
+
+def change_key(row: Row) -> tuple:
+    return tuple(getattr(row, name) for name in CHANGE_KEY_FIELDS)
+
+
+def _sort_key(row: Row) -> tuple:
+    stamp = parse_timestamp(row.liveness_observed_at)
+    if stamp is None:
+        stamp = parse_timestamp(row.evidence_last_observed_at)
+    dispatch = row.dispatch_id if isinstance(row.dispatch_id, str) else ""
+    return (0 if stamp is not None else 1, -(stamp or 0.0), dispatch, row.namespace)
+
+
+def _field(row: Row, attr: str) -> str:
+    value = getattr(row, attr)
+    if value is UNKNOWN or attr in row.absent_fields:
+        return ABSENT_IN_SOURCE
+    return text_of(value)
+
+
+def _inspector(row: Row, result: Any, snapshot: Any) -> tuple[tuple[str, str], ...]:
+    lines: list[tuple[str, str]] = [
+        ("dispatchId", _field(row, "dispatch_id")),
+        ("taskId", _field(row, "task_id")),
+        ("runId", _field(row, "run_id")),
+        ("workerState", _field(row, "worker_state")),
+        ("dispatchStatus", _field(row, "dispatch_status")),
+        ("terminalState", _field(row, "terminal_state")),
+        ("projection.outcome", _field(row, "outcome")),
+        ("projection.nextAction.kind", _field(row, "next_action_kind")),
+        ("resource.worktreeId", _field(row, "worktree_id")),
+        ("resource.ownerDispatchId", _field(row, "owner_dispatch_id")),
+        ("resource.originDispatchId", _field(row, "origin_dispatch_id")),
+        ("projection.host.id", _field(row, "host_id")),
+        ("projection.workspace.id", _field(row, "workspace_id")),
+        ("projection.stage.worker (worker-reported)", _field(row, "stage_worker")),
+        ("projection.stage.dispatch (worker-reported)", _field(row, "stage_dispatch")),
+        ("projection.stage.activity (worker-reported)", _field(row, "stage_activity")),
+        ("projection.stage.detail (worker-reported)", _field(row, "stage_detail")),
+        ("unrecognised keys", f"{row.unrecognised_keys} unrecognised keys"),
+    ]
+    flags = row.flags + (() if row.reobserved else ("not reobserved",))
+    if flags:
+        lines.append(("flags", ", ".join(flags)))
+    lines.extend((fact, UNAVAILABLE) for fact in UNAVAILABLE_FACTS)
+    if snapshot is not None:
+        lines.extend(("source warning", warning) for warning in snapshot.warnings)
+    if result.diagnostic:
+        lines.append(("last poll error (sanitized)", result.diagnostic))
+    return tuple(lines)
+
+
+def _next_action_text(row: Row) -> str:
+    value = row.next_action_kind
+    if value is UNKNOWN or not str(value).strip():
+        return "unknown"  # absent or blank
+    return text_of(value)
+
+
+def _row_view(
+    row: Row,
+    *,
+    result: Any,
+    snapshot: Any,
+    clock: Any,
+    selected: bool,
+    changed: bool,
+    mode: str,
+    force_not_reobserved: bool = False,
+) -> RowView:
+    stamp = parse_timestamp(row.evidence_last_observed_at)
+    age = "unknown" if stamp is None else format_age(clock.wall() - stamp)
+    flags = row.flags + (
+        () if row.reobserved and not force_not_reobserved else ("not reobserved",)
+    )
+    return RowView(
+        identity=row.identity,
+        dispatch_id=text_of(row.dispatch_id),
+        run=text_of(row.run_id),
+        worker_state=text_of(row.worker_state),
+        dispatch_status=text_of(row.dispatch_status),
+        terminal_state=text_of(row.terminal_state),
+        outcome=text_of(row.outcome),
+        next_action=_next_action_text(row),
+        liveness=f"{text_of(row.liveness_verdict)} ({text_of(row.liveness_source)})",
+        evidence_age=age,
+        flags=flags,
+        changed=changed,
+        frozen=bool(row.fixture_frozen) and mode == "fixture",
+        historical=is_historical(row),
+        selected=selected,
+        inspector=_inspector(row, result, snapshot),
+        raw=row,
+    )
+
+
+def _matches(view: RowView, text: str) -> bool:
+    if not text:
+        return True
+    cells = (
+        view.dispatch_id,
+        view.run,
+        view.worker_state,
+        view.dispatch_status,
+        view.terminal_state,
+        view.outcome,
+        view.next_action,
+        view.liveness,
+    )
+    return text.lower() in " ".join(cells).lower()
+
+
+def _scope_text(snapshot: Any) -> tuple[str, bool]:
+    scope = snapshot.scope if snapshot is not None else UNKNOWN
+    source = scope.get("source") if isinstance(scope, dict) else None
+    if not isinstance(source, str) or not source:
+        return "scope unknown", False
+    return f"scope={source}", source == "bound"
+
+
+def _partial_text(coverage: Coverage) -> str | None:
+    if not coverage.partial:
+        return None
+    total = coverage.reported_total
+    reported = f"reported {total}" if isinstance(total, int) else "reported unknown"
+    error = coverage.stopped_by_error
+    if coverage.empty_page is not None:
+        return f"PARTIAL (empty page {coverage.empty_page})"
+    if error == "cursor-stalled":
+        return f"PARTIAL (cursor missing or not advancing, page {coverage.pages_read})"
+    if error == "cursor-rejected":
+        return f"PARTIAL (cursor rejected, page {coverage.pages_read})"
+    if error is not None:
+        return f"PARTIAL ({code_label(error)}, page {coverage.pages_read})"
+    return f"PARTIAL: collected {coverage.collected} of {reported} ({PARTIAL_CAP_TEXT})"
+
+
+def _collected_text(coverage: Coverage | None) -> str:
+    """The ``collected n / reported T`` text."""
+    if coverage is None:
+        return "collected unknown / reported unknown"
+    known = [t for t in coverage.page_totals if isinstance(t, int)]
+    if coverage.total_changed:
+        reported = f"reported {known[0]}-{known[-1]} (changed during read)"
+    elif isinstance(coverage.reported_total, int):
+        reported = f"reported {coverage.reported_total}"
+        if coverage.pages_read > 1:
+            reported += f" (page {coverage.pages_read})"
+    else:
+        reported = "reported unknown"
+    text = f"collected {coverage.collected} / {reported}"
+    if coverage.mismatch and not coverage.total_changed:
+        text += " (mismatch)"
+    return text
+
+
+def _freshness(result: Any, clock: Any, state: str) -> tuple[str, str | None]:
+    age = (
+        None
+        if result.last_success_mono is None
+        else format_age(clock.monotonic() - result.last_success_mono)
+    )
+    if state == "NOT_AVAILABLE":
+        return f"worker-list {NOT_AVAILABLE_TEXT}", None
+    if state == "NOT_POLLED":
+        return "worker-list NOT POLLED", None
+    if state == "FAILED":
+        cell = f"worker-list FAILED ({code_label(result.code)})"
+    else:
+        cell = f"worker-list {state}"
+    return (f"{cell} {age}" if age else cell), age
+
+
+def _meta(
+    result: Any, snapshot: Any, coverage: Coverage | None, state: str, clock: Any
+) -> SnapshotMeta:
+    status = {"OK": "OK", "STALE": "STALE", "FAILED": "ERROR"}.get(state, "UNKNOWN")
+    observed = (
+        UNKNOWN
+        if result.last_success_wall is None
+        else format_utc_iso(result.last_success_wall)
+    )
+    return SnapshotMeta(
+        cycle=result.cycle,
+        generated_at=format_utc_iso(clock.wall()),
+        producer_name=PRODUCER_NAME,
+        producer_version=__version__,
+        namespace=result.namespace,
+        source_status=status,
+        source_observed_at=observed,
+        source_error=result.code if status == "ERROR" else None,
+        has_more=snapshot.has_more if snapshot is not None else UNKNOWN,
+        total=snapshot.total if snapshot is not None else UNKNOWN,
+        limit=snapshot.limit if snapshot is not None else UNKNOWN,
+        scope=snapshot.scope if snapshot is not None else UNKNOWN,
+        counts=snapshot.counts if snapshot is not None else UNKNOWN,
+        collection_state=coverage.state if coverage is not None else None,
+        collection_collected=coverage.collected if coverage is not None else None,
+        collection_changed_during_read=coverage.total_changed
+        if coverage is not None
+        else None,
+        collection_duplicates_ignored=coverage.duplicates
+        if coverage is not None
+        else None,
+    )
+
+
+def _source_counts_text(snapshot: Any) -> str:
+    counts = snapshot.counts if snapshot is not None else UNKNOWN
+    if not isinstance(counts, dict):
+        return "source counts: unknown"
+    parts = [
+        f"{key} {text_of(counts[key]) if key in counts else 'unknown'}"
+        for key in SOURCE_COUNT_KEYS
+    ]
+    return "source counts: " + " / ".join(parts)
+
+
+def _changes(rows: tuple[Row, ...], session: Session) -> tuple[frozenset, int]:
+    """(identities of rows to star, k for ``changed since``): added, removed or changed rows."""
+    baseline = session.baseline
+    if baseline is None:
+        return frozenset(), 0
+    current = {
+        r.identity: r for r in rows if not r.identity_unknown
+    }  # no identity, no tracking
+    flagged = {
+        i
+        for i, r in current.items()
+        if i not in baseline or baseline[i] != change_key(r)
+    }
+    removed = sum(1 for i in baseline if i not in current)
+    return frozenset(flagged), len(flagged) + removed
+
+
+def build_view(result: Any, session: Session, clock: Any) -> View:
+    """Pure: the same inputs always give an equal ``View``. ``result`` is a ``CycleResult``."""
+    snapshot = result.snapshot
+    coverage = result.coverage
+    state = source_state(result, clock)
+    rows: tuple[Row, ...] = snapshot.rows if snapshot is not None else ()
+    tz = clock.local_tz()
+    mode = result.mode
+
+    scope_text, bound = _scope_text(snapshot)
+    as_of = (
+        "never"
+        if result.last_success_wall is None
+        else format_local(result.last_success_wall, tz, "%H:%M:%S")
+    )
+    banner = (
+        f"SYNTHETIC FIXTURE {result.fixture_variant}, not Orca data"
+        if mode == "fixture"
+        else None
+    )
+    header_parts = ["ORCA OBSERVER", f"mode={mode}"]
+    if banner:
+        header_parts.append(banner)
+    header_parts.append(scope_text)
+    if bound:
+        header_parts.append("one Run only")
+    header_parts.append(f"as of {as_of}")
+    header1 = "  ".join(header_parts)
+
+    fresh_cell, age = _freshness(result, clock, state)
+    cells = [fresh_cell, MESSAGES_CELL]
+    if snapshot is not None and snapshot.warnings:
+        cells.append(f"source warnings: {len(snapshot.warnings)} (inspector)")
+    if result.code == "overrun":
+        cells.append(f"cycle overran ({int(result.duration)}s)")
+    header2 = "  ".join(cells)
+
+    collected_text = _collected_text(coverage)
+    tokens = [CountsToken(collected_text, True)]
+    partial = _partial_text(coverage) if coverage is not None else None
+    if partial:
+        tokens.append(CountsToken(partial, True))
+    tokens.append(CountsToken(scope_text, True))
+    tokens.append(CountsToken(_source_counts_text(snapshot), False))
+    if snapshot is not None:
+        runs = {r.run_id for r in rows if r.run_id is not UNKNOWN}
+        unknown_runs = sum(1 for r in rows if r.run_id is UNKNOWN)
+        tokens.append(
+            CountsToken(f"runs seen: {aggregate(len(runs), unknown_runs)}", False)
+        )
+    tokens.append(CountsToken(f"SETTLED {UNAVAILABLE}", False))
+    tokens.append(CountsToken(f"POLICY FROZEN {UNAVAILABLE}", False))
+    tokens.append(CountsToken("cost unavailable", False))
+
+    flagged, changed_k = _changes(rows, session)
+    changes_line = None
+    if session.baseline is not None and session.mark_wall_time is not None:
+        hhmm = format_local(session.mark_wall_time, tz, "%H:%M")
+        changes_line = f"changed since {hhmm} ({changed_k})"
+        if not session.marked:
+            changes_line = f"new baseline at {hhmm} (observer started) | {changes_line}"
+
+    def make(row: Row, **extra: Any) -> RowView:
+        return _row_view(
+            row,
+            result=result,
+            snapshot=snapshot,
+            clock=clock,
+            selected=row.identity == session.selected,
+            changed=row.identity in flagged,
+            mode=mode,
+            **extra,
+        )
+
+    source_order = tuple(make(r) for r in rows)
+    all_rows = tuple(sorted(source_order, key=lambda rv: _sort_key(rv.raw)))
+    matching = tuple(rv for rv in source_order if _matches(rv, session.filter_text))
+    hidden_historical = (
+        0 if session.show_historical else sum(1 for rv in matching if rv.historical)
+    )
+    visible = tuple(
+        rv for rv in matching if session.show_historical or not rv.historical
+    )
+
+    filter_line = None
+    if session.filter_text:
+        filter_line = f"filter {session.filter_text}: {len(matching)} of {len(source_order)} collected"
+    duplicates = coverage.duplicates if coverage is not None else 0
+
+    selected_view = next(
+        (rv for rv in source_order if rv.identity == session.selected), None
+    )
+    selection_note = None
+    if (
+        selected_view is None
+        and session.selected is not None
+        and session.selected_row is not None
+    ):
+        selected_view = make(session.selected_row, force_not_reobserved=True)
+        selection_note = (
+            f"selected {selected_view.dispatch_id} no longer in source window"
+        )
+
+    if rows:
+        ledger_empty: tuple[str, ...] = ()
+    elif result.last_success_mono is None:
+        ledger_empty = (NO_READ_YET,)
+    else:
+        ledger_empty = (EMPTY_NOTICE, f"worker-list returned 0 workers in {scope_text}")
+
+    return View(
+        mode=mode,
+        variant=result.fixture_variant,
+        meta=_meta(result, snapshot, coverage, state, clock),
+        source_state=state,
+        as_of=as_of,
+        scope_text=scope_text,
+        synthetic_banner=banner,
+        header1=header1,
+        header2=header2,
+        freshness_cells=tuple(cells),
+        poll_age=age,
+        counts_tokens=tuple(tokens),
+        collected_text=collected_text,
+        gap_notice=GAP_NOTICE,
+        ledger_title=LEDGER_TITLE,
+        ledger_empty=ledger_empty,
+        changes_line=changes_line,
+        filter_line=filter_line,
+        historical_note=f"{hidden_historical} historical hidden (h)"
+        if hidden_historical
+        else None,
+        duplicates_note=f"{duplicates} duplicate rows ignored" if duplicates else None,
+        selection_note=selection_note,
+        all_rows=all_rows,
+        visible_rows=visible,
+        selected=selected_view,
+        focus=session.focus,
+        filter_text=session.filter_text,
+        show_historical=session.show_historical,
+        inspector=selected_view.inspector
+        if session.focus == "inspector" and selected_view is not None
+        else None,
+        help_line=KEYS_LINE,
+    )
diff --git a/tests/observe/test_view.py b/tests/observe/test_view.py
new file mode 100644
index 000000000..477f20b1b
--- /dev/null
+++ b/tests/observe/test_view.py
@@ -0,0 +1,867 @@
+"""View model tests (AD-8, AD-10; T9, T11, T13, T14, T15, T18, T20, T21, T31, T33, T34, T38, T42, T43, T47)."""
+
+from __future__ import annotations
+
+import json
+import re
+from datetime import timedelta
+from pathlib import Path
+
+import superclaude
+import superclaude.cli.observe.view as view_module
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.parse import UNKNOWN
+from superclaude.cli.observe.view import (
+    ABSENT_IN_SOURCE,
+    EMPTY_NOTICE,
+    GAP_NOTICE,
+    LEDGER_TITLE,
+    NO_READ_YET,
+    UNAVAILABLE,
+    Session,
+    aggregate,
+    build_view,
+    change_key,
+    format_age,
+    text_of,
+)
+from tests.observe.conftest import (
+    BASE_TIME,
+    FakeClock,
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_rows,
+)
+
+
+def fixture_result(variant, clock, cycles=1):
+    collector = Collector(FixtureSource(variant), clock)
+    result = None
+    for _ in range(cycles):
+        result = collector.run_once()
+    return result
+
+
+def live_collector(responses, clock, argv_log, path="/opt/fake/orca"):
+    runner = FakeRunner(argv_log, responses)
+    return Collector(LiveSource(runner, FakeDiscover(argv_log, path)), clock)
+
+
+def rows_reply(rows, total=None, has_more=False, cursor=None, **result_extra):
+    envelope = make_envelope(rows, total=total, has_more=has_more)
+    if cursor is not None:
+        envelope["result"]["page"]["nextCursor"] = cursor
+    envelope["result"].update(result_extra)
+    return 0, json.dumps(envelope)
+
+
+def texts(view, with_gap=True):
+    """Every string a screen or export could show for this view."""
+    parts = [
+        view.header1,
+        view.header2,
+        view.collected_text,
+        view.ledger_title,
+        *view.ledger_empty,
+    ]
+    parts += [t.text for t in view.counts_tokens]
+    for note in (
+        view.changes_line,
+        view.filter_line,
+        view.historical_note,
+        view.duplicates_note,
+        view.selection_note,
+    ):
+        if note:
+            parts.append(note)
+    for rv in view.all_rows:
+        parts += [
+            rv.dispatch_id,
+            rv.run,
+            rv.worker_state,
+            rv.dispatch_status,
+            rv.terminal_state,
+            rv.outcome,
+        ]
+        parts += [rv.next_action, rv.liveness, rv.evidence_age, *rv.flags]
+        parts += [f"{label}: {value}" for label, value in rv.inspector]
+    if with_gap:
+        parts.append(view.gap_notice)
+    return parts
+
+
+def build(result, clock, session=None):
+    return build_view(result, session or Session(), clock)
+
+
+# -- T13 and T38: unknown is never zero ----------------------------------------------------------------
+
+ABSENT_LABELS = {
+    "task_id": "taskId",
+    "run_id": "runId",
+    "worktree_id": "resource.worktreeId",
+    "owner_dispatch_id": "resource.ownerDispatchId",
+    "origin_dispatch_id": "resource.originDispatchId",
+    "host_id": "projection.host.id",
+    "workspace_id": "projection.workspace.id",
+    "stage_worker": "projection.stage.worker (worker-reported)",
+    "stage_dispatch": "projection.stage.dispatch (worker-reported)",
+    "next_action_kind": "projection.nextAction.kind",
+    "outcome": "projection.outcome",
+}
+
+
+def test_every_absent_field_renders_unknown_and_never_zero_or_false(fake_clock):
+    view = build(fixture_result("missing-fields", fake_clock), fake_clock)
+    checked = 0
+    for rv in view.all_rows:
+        inspector = dict(rv.inspector)
+        for attr in rv.raw.absent_fields:
+            label = ABSENT_LABELS.get(attr)
+            if label is None:
+                continue
+            assert inspector[label] == ABSENT_IN_SOURCE, (rv.dispatch_id, attr)
+            assert inspector[label] not in ("0", "false", "-", "")
+            checked += 1
+    assert checked >= 5
+    by_dispatch = {rv.dispatch_id: rv for rv in view.all_rows}
+    first = by_dispatch["w-001"]  # no liveness and no nextAction
+    assert first.next_action == "unknown" and first.liveness == "unknown (unknown)"
+    anonymous = next(rv for rv in view.all_rows if "identity unknown" in rv.flags)
+    assert (
+        anonymous.dispatch_id == "unknown"
+        and dict(anonymous.inspector)["dispatchId"] == ABSENT_IN_SOURCE
+    )
+    assert (
+        next(rv for rv in view.all_rows if rv.dispatch_id == "w-003").run == "unknown"
+    )  # a JSON null
+    assert (
+        next(rv for rv in view.all_rows if rv.dispatch_id == "w-004").evidence_age
+        == "unknown"
+    )
+
+
+def test_aggregates_with_unknown_members_render_n_plus_question_mark(fake_clock):
+    assert aggregate(3, 0) == "3"
+    assert aggregate(3, 2) == "3+? (2 unknown)" and aggregate(0, 4) == "0+? (4 unknown)"
+    view = build(fixture_result("missing-fields", fake_clock), fake_clock)
+    assert "runs seen: 1+? (1 unknown)" in [t.text for t in view.counts_tokens]
+    clean = build(fixture_result("base", fake_clock), fake_clock)
+    assert "runs seen: 8" in [t.text for t in clean.counts_tokens]
+
+
+def test_a_source_value_that_is_the_text_unknown_is_quoted():
+    assert text_of(UNKNOWN) == "unknown"
+    assert text_of("unknown") == '"unknown"' and text_of("UNKNOWN") == '"UNKNOWN"'
+    assert (
+        text_of("running") == "running"
+        and text_of(0) == "0"
+        and text_of(False) == "false"
+    )
+
+
+def test_missing_fields_header_says_scope_unknown_and_total_unknown(fake_clock):
+    view = build(fixture_result("missing-fields", fake_clock), fake_clock)
+    assert "scope unknown" in view.header1 and view.scope_text == "scope unknown"
+    assert "reported unknown" in view.collected_text
+
+
+# -- T14 and T15: separate facts, nothing inferred ---------------------------------------------------------
+
+
+def test_a_released_row_without_an_outcome_never_reads_done_complete_or_settled(
+    fake_clock, argv_log
+):
+    rows = make_rows(2, 1)
+    for row in rows:
+        row["terminalState"] = "released"
+        row["workerState"] = "exited"
+        row["dispatchStatus"] = "exited"
+        del row["projection"]["outcome"]
+    collector = live_collector([rows_reply(rows, total=2)], fake_clock, argv_log)
+    view = build(collector.run_once(), fake_clock, Session(show_historical=True))
+    assert len(view.visible_rows) == 2
+    for rv in view.visible_rows:
+        assert rv.terminal_state == "released" and rv.outcome == "unknown"
+    row_texts = " ".join(
+        t
+        for rv in view.all_rows
+        for t in (
+            rv.worker_state,
+            rv.dispatch_status,
+            rv.terminal_state,
+            rv.outcome,
+            rv.liveness,
+            *rv.flags,
+        )
+    ).lower()
+    for word in ("done", "complete", "settled"):
+        assert word not in row_texts
+
+
+def test_report_acceptance_tests_and_approval_are_unavailable_and_nothing_is_admitted(
+    fake_clock,
+):
+    view = build(
+        fixture_result("base", fake_clock), fake_clock, Session(focus="inspector")
+    )
+    for rv in view.all_rows:
+        inspector = dict(rv.inspector)
+        for fact in ("report status", "acceptance", "tests", "approval"):
+            assert inspector[fact] == UNAVAILABLE
+    assert not any("admitted" in t.lower() for t in texts(view))
+    assert "admitted" not in repr(view).lower()
+
+
+# -- T18: collected / reported ----------------------------------------------------------------------------------
+
+
+def test_total_287_with_100_rows_reads_collected_100_of_reported_287_never_287_workers(
+    fake_clock, argv_log
+):
+    collector = live_collector(
+        [rows_reply(make_rows(100, 4), total=287)], fake_clock, argv_log
+    )
+    view = build(collector.run_once(), fake_clock)
+    assert view.collected_text.startswith("collected 100 / reported 287")
+    assert not any("287 workers" in t for t in texts(view))
+
+
+def test_absent_total_reads_reported_unknown(fake_clock, argv_log):
+    collector = live_collector([rows_reply(make_rows(3, 1))], fake_clock, argv_log)
+    view = build(collector.run_once(), fake_clock)
+    assert view.collected_text == "collected 3 / reported unknown"
+
+
+def test_coverage_literals(fake_clock, argv_log):
+    counter = {"n": 0}
+
+    def more(argv, timeout):
+        counter["n"] += 1
+        rows = make_rows(100, 1)
+        for row in rows:
+            row["dispatchId"] += f"-{counter['n']}"
+        return rows_reply(rows, total=9999, has_more=True, cursor=f"c{counter['n']}")
+
+    view = build(live_collector([more], fake_clock, argv_log).run_once(), fake_clock)
+    partial = [t.text for t in view.counts_tokens if t.text.startswith("PARTIAL")]
+    assert partial == [
+        "PARTIAL: collected 500 of reported 9999 (newest first; oldest rows not read; long-running active workers may be among them)"
+    ]
+    assert view.collected_text == "collected 500 / reported 9999 (page 5)"
+
+    stalled = build(
+        live_collector(
+            [rows_reply(make_rows(2, 1), total=9, has_more=True)], fake_clock, argv_log
+        ).run_once(),
+        fake_clock,
+    )
+    assert "PARTIAL (cursor missing or not advancing, page 1)" in [
+        t.text for t in stalled.counts_tokens
+    ]
+    rejected = build(
+        live_collector(
+            [rows_reply(make_rows(2, 1), total=9, has_more=True, cursor="-bad")],
+            fake_clock,
+            argv_log,
+        ).run_once(),
+        fake_clock,
+    )
+    assert "PARTIAL (cursor rejected, page 1)" in [
+        t.text for t in rejected.counts_tokens
+    ]
+
+    empty = rows_reply([], total=5, has_more=True, cursor="c2")
+    paged = build(
+        live_collector(
+            [rows_reply(make_rows(2, 1), total=5, has_more=True, cursor="c1"), empty],
+            fake_clock,
+            argv_log,
+        ).run_once(),
+        fake_clock,
+    )
+    assert "PARTIAL (empty page 2)" in [t.text for t in paged.counts_tokens]
+
+    def renamed(n):
+        return [dict(r, dispatchId=r["dispatchId"] + "x") for r in make_rows(n, 1)]
+
+    first_page = rows_reply(make_rows(2, 1), total=250, has_more=True, cursor="c1")
+    changed = build(
+        live_collector(
+            [first_page, rows_reply(renamed(2), total=251)], fake_clock, argv_log
+        ).run_once(),
+        fake_clock,
+    )
+    assert (
+        changed.collected_text == "collected 4 / reported 250-251 (changed during read)"
+    )
+
+    first_page = rows_reply(make_rows(2, 1), total=4, has_more=True, cursor="c1")
+    two_pages = build(
+        live_collector(
+            [first_page, rows_reply(renamed(2), total=4)], fake_clock, argv_log
+        ).run_once(),
+        fake_clock,
+    )
+    assert two_pages.collected_text == "collected 4 / reported 4 (page 2)"
+
+
+def test_cycle_overran_warnings_and_duplicates_have_their_literals(
+    fake_clock, argv_log
+):
+    def first(argv, timeout):
+        fake_clock.advance(12)
+        return rows_reply(
+            make_rows(2, 1),
+            total=9,
+            has_more=True,
+            cursor="c1",
+            warnings=["careful", "again"],
+        )
+
+    def second(argv, timeout):
+        fake_clock.advance(timeout)
+        raise TimeoutError
+
+    view = build(
+        live_collector([first, second], fake_clock, argv_log).run_once(), fake_clock
+    )
+    assert "cycle overran (15s)" in view.freshness_cells
+    assert "source warnings: 2 (inspector)" in view.freshness_cells
+    dup = build(fixture_result("duplicate-out-of-order", fake_clock), fake_clock)
+    assert dup.duplicates_note == "1 duplicate rows ignored"
+
+
+# -- T9 and T47: the question-source gap ------------------------------------------------------------------------------
+
+
+def test_live_mode_shows_the_gap_notice_and_the_ledger_title_and_derives_nothing_from_count(
+    fake_clock, argv_log
+):
+    collector = live_collector(
+        [rows_reply(make_rows(3, 1), total=3, count=999)], fake_clock, argv_log
+    )
+    view = build(collector.run_once(), fake_clock)
+    assert (
+        view.gap_notice
+        == GAP_NOTICE
+        == 'Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"'
+    )
+    assert view.ledger_title == LEDGER_TITLE == "worker-reported, not questions"
+    assert not any("999" in t for t in texts(view))
+    assert not any("no questions" in t for t in texts(view, with_gap=False))
+
+
+# -- T11 and T42: freshness ------------------------------------------------------------------------------------------
+
+
+def test_freshness_cell_ok_stale_and_failed_with_ages_and_values_keep_their_last_reading(
+    fake_clock,
+):
+    collector = Collector(FixtureSource("source-loss"), fake_clock)
+    good = collector.run_once()
+    collector.run_once()
+    fake_clock.advance(4)
+    assert build(good, fake_clock).freshness_cells[0] == "worker-list OK 4s"
+    fake_clock.advance(48)
+    stale = build(good, fake_clock)
+    assert (
+        stale.freshness_cells[0] == "worker-list STALE 52s"
+        and stale.source_state == "STALE"
+    )
+    fake_clock.advance(8)  # the same result at 60 s: a minute
+    assert build(good, fake_clock).freshness_cells[0] == "worker-list STALE 1m"
+    failed = collector.run_once()  # third cycle of the fixture: {"fail": "timeout"}
+    view = build(failed, fake_clock)
+    assert (
+        view.freshness_cells[0] == "worker-list FAILED (timeout) 1m"
+        and view.source_state == "FAILED"
+    )
+    assert (
+        len(view.all_rows) == 5
+        and view.as_of != "never"
+        and f"as of {view.as_of}" in view.header1
+    )
+
+    def cells(v):
+        return [
+            (rv.worker_state, rv.outcome, rv.liveness, rv.terminal_state)
+            for rv in v.all_rows
+        ]
+
+    assert cells(view) == cells(build(good, fake_clock))  # no value turns into "failed"
+    exit_failed = Collector(FixtureSource("source-loss"), fake_clock)
+    for _ in range(5):
+        last = exit_failed.run_once()
+    assert (
+        build(last, fake_clock)
+        .freshness_cells[0]
+        .startswith("worker-list FAILED (exit 2)")
+    )
+
+
+def test_stale_is_exactly_forty_five_seconds_on_the_monotonic_clock(fake_clock):
+    result = fixture_result("base", fake_clock)
+    fake_clock.advance(44)
+    assert build(result, fake_clock).source_state == "OK"
+    fake_clock.advance(1)
+    assert build(result, fake_clock).source_state == "STALE"
+    fake_clock.jump_wall(-7200)  # a wall-clock jump changes nothing about staleness
+    assert build(result, fake_clock).source_state == "STALE"
+
+
+def test_before_the_first_poll_and_when_no_orca_is_available(fake_clock, argv_log):
+    collector = live_collector([rows_reply([])], fake_clock, argv_log)
+    view = build(collector.latest(), fake_clock)
+    assert (
+        view.source_state == "NOT_POLLED"
+        and view.freshness_cells[0] == "worker-list NOT POLLED"
+    )
+    assert "as of never" in view.header1
+    assert view.collected_text == "collected unknown / reported unknown"
+    assert (
+        view.ledger_empty == (NO_READ_YET,) == ("no successful worker-list read yet",)
+    )
+    unavailable = build(
+        live_collector([rows_reply([])], fake_clock, argv_log, path=None).run_once(),
+        fake_clock,
+    )
+    assert unavailable.source_state == "NOT_AVAILABLE"
+    assert (
+        unavailable.freshness_cells[0]
+        == "worker-list NOT AVAILABLE (no Orca CLI validated)"
+    )
+    assert unavailable.ledger_empty == (NO_READ_YET,)
+
+
+def test_poll_age_and_evidence_age_are_separate_facts(fake_clock, argv_log):
+    rows = make_rows(2, 1)
+    old = (BASE_TIME - timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
+    for row in rows:
+        row["projection"]["evidence"]["lastObservedAt"] = old
+        row["projection"]["liveness"]["observedAt"] = old
+    result = live_collector(
+        [rows_reply(rows, total=2)], fake_clock, argv_log
+    ).run_once()
+    fake_clock.advance(4)
+    view = build(result, fake_clock)
+    assert view.poll_age == "4s" and view.source_state == "OK"
+    assert view.freshness_cells[0] == "worker-list OK 4s"
+    assert {rv.evidence_age for rv in view.all_rows} == {"20m"}
+
+
+def test_format_age():
+    assert [format_age(s) for s in (-5, 0, 4, 59, 60, 119, 3599, 3600, 7300)] == [
+        "0s",
+        "0s",
+        "4s",
+        "59s",
+        "1m",
+        "1m",
+        "59m",
+        "1h",
+        "2h",
+    ]
+
+
+# -- T20, CD-16: shared worktrees --------------------------------------------------------------------------------------
+
+
+def test_sessions_sharing_a_worktree_stay_two_rows_with_the_same_worktree_in_each_inspector(
+    fake_clock,
+):
+    view = build(fixture_result("shared-unmapped", fake_clock), fake_clock)
+    assert len(view.all_rows) == 3
+    by_dispatch = {rv.dispatch_id: dict(rv.inspector) for rv in view.all_rows}
+    assert (
+        by_dispatch["w-001"]["resource.worktreeId"]
+        == "wt-shared"
+        == by_dispatch["w-002"]["resource.worktreeId"]
+    )
+    assert by_dispatch["w-003"]["resource.worktreeId"] == ABSENT_IN_SOURCE
+    assert not any("conflict" in t.lower() for t in texts(view))
+
+
+# -- T21: historical rows ----------------------------------------------------------------------------------------------------
+
+
+def test_historical_rows_are_hidden_by_default_and_listed_with_their_state_on_toggle(
+    fake_clock,
+):
+    result = fixture_result("historical", fake_clock)
+    hidden = build(result, fake_clock)
+    assert hidden.historical_note == "5 historical hidden (h)"
+    assert len(hidden.visible_rows) == 4 and len(hidden.all_rows) == 9
+    states = {rv.dispatch_id: rv.terminal_state for rv in hidden.visible_rows}
+    assert states == {
+        "w-001": "active",
+        "w-007": "unknown",
+        "w-008": "orphaned",
+        "w-009": "active",
+    }
+    shown = build(result, fake_clock, Session(show_historical=True))
+    assert shown.historical_note is None and len(shown.visible_rows) == 9
+    assert {rv.terminal_state for rv in shown.visible_rows} >= {
+        "released",
+        "retained",
+        "orphaned",
+        "unknown",
+    }
+
+    def counts(v):
+        return [
+            t.text
+            for t in v.counts_tokens
+            if t.text.startswith(("collected", "source counts"))
+        ]
+
+    assert counts(hidden) == counts(shown)  # the toggle never changes source counts
+
+
+# -- T31, T33, T34 -------------------------------------------------------------------------------------------------------------
+
+
+def test_cost_is_unavailable_never_a_dollar_amount_and_elapsed_time_is_only_an_age(
+    fake_clock,
+):
+    view = build(fixture_result("base", fake_clock), fake_clock)
+    assert "cost unavailable" in [t.text for t in view.counts_tokens]
+    assert not any("$" in t or "%" in t for t in texts(view))
+    assert all(
+        re.fullmatch(r"\d+[smh]|unknown", rv.evidence_age) for rv in view.all_rows
+    )
+
+
+def test_empty_fixture_reads_exactly_the_not_proof_text_and_names_the_scope(fake_clock):
+    view = build(fixture_result("empty", fake_clock), fake_clock)
+    assert view.ledger_empty == (
+        EMPTY_NOTICE,
+        "worker-list returned 0 workers in scope=bound",
+    )
+    assert (
+        EMPTY_NOTICE == "no observed items in this source window; not proof none exist"
+    )
+    assert "one Run only" in view.header1 and "scope=bound" in view.header1
+    assert not any("no questions" in t for t in texts(view, with_gap=False))
+
+
+def test_fixture_mode_marks_frozen_rows_and_live_mode_reads_unavailable(
+    fake_clock, argv_log
+):
+    fixture = build(fixture_result("base", fake_clock), fake_clock)
+    assert [rv.dispatch_id for rv in fixture.all_rows if rv.frozen] == ["w-003"]
+    assert (
+        fixture.synthetic_banner == "SYNTHETIC FIXTURE base, not Orca data"
+        and fixture.synthetic_banner in fixture.header1
+    )
+    live = build(
+        live_collector(
+            [rows_reply(make_rows(3, 1), total=3)], fake_clock, argv_log
+        ).run_once(),
+        fake_clock,
+    )
+    tokens = [t.text for t in live.counts_tokens]
+    assert (
+        "SETTLED unavailable (no source)" in tokens
+        and "POLICY FROZEN unavailable (no source)" in tokens
+    )
+    assert not any(rv.frozen for rv in live.all_rows) and live.synthetic_banner is None
+    assert "mode=live" in live.header1
+
+
+# -- T43: overflow ------------------------------------------------------------------------------------------------------------------
+
+
+def test_plus_n_more_never_counts_the_selected_row(fake_clock):
+    result = fixture_result("base", fake_clock)
+    plain = build(result, fake_clock, Session(show_historical=True))
+    target = plain.visible_rows[50].identity
+    view = build(result, fake_clock, Session(selected=target, show_historical=True))
+    window = view.window(10)
+    assert window.shown == 10 and window.total == 80 and window.text == "10/80 shown"
+    assert any(rv.selected for rv in window.rows)  # the selected row is kept in view
+    assert window.more == 70 and window.more_text == "+70 more"
+    assert view.footer(window).endswith("10/80 shown | collected 80 / reported 80")
+    # selected row not in the visible set (filtered out): it is not counted in "+N more" either
+    row_view = view.selected
+    narrowed = build(
+        result,
+        fake_clock,
+        Session(
+            selected=target,
+            selected_row=row_view.raw,
+            filter_text="run-a",
+            show_historical=True,
+        ),
+    )
+    assert target not in {rv.identity for rv in narrowed.visible_rows}
+    nw = narrowed.window(4)
+    assert nw.total == 10 and nw.more == 6
+    everything = view.window(None)
+    assert (everything.shown, everything.more, everything.more_text) == (80, 0, "")
+    assert view.window(500).text == "80/80 shown"
+
+
+def test_window_without_a_selection_starts_at_the_top(fake_clock):
+    view = build(
+        fixture_result("base", fake_clock), fake_clock, Session(show_historical=True)
+    )
+    window = view.window(5)
+    assert [rv.dispatch_id for rv in window.rows] == [
+        rv.dispatch_id for rv in view.visible_rows[:5]
+    ]
+    assert window.more == 75
+
+
+# -- header, filter, changes, selection --------------------------------------------------------------------------------------------
+
+
+def test_filter_line_names_the_expression_and_counts(fake_clock):
+    view = build(
+        fixture_result("base", fake_clock), fake_clock, Session(filter_text="run-a")
+    )
+    assert view.filter_line == "filter run-a: 10 of 80 collected"
+    assert (
+        len(view.visible_rows) == 7
+    )  # 3 of the 10 are historical and hidden by default
+    assert view.historical_note == "3 historical hidden (h)"
+    assert "collected 80 / reported 80" in view.collected_text
+    assert build(fixture_result("base", fake_clock), fake_clock).filter_line is None
+
+
+def test_next_action_is_verbatim_and_blank_reads_unknown(fake_clock, argv_log):
+    rows = make_rows(3, 1)
+    rows[0]["projection"]["nextAction"]["kind"] = "Review-Needed "
+    rows[1]["projection"]["nextAction"]["kind"] = "   "
+    del rows[2]["projection"]["nextAction"]
+    view = build(
+        live_collector([rows_reply(rows, total=3)], fake_clock, argv_log).run_once(),
+        fake_clock,
+    )
+    by_dispatch = {rv.dispatch_id: rv.next_action for rv in view.all_rows}
+    assert by_dispatch == {
+        "w-001": "Review-Needed ",
+        "w-002": "unknown",
+        "w-003": "unknown",
+    }
+
+
+def test_changed_rows_are_starred_and_counted_since_the_baseline(fake_clock):
+    first = fixture_result("base", fake_clock)
+    second = fixture_result("base", fake_clock, cycles=2)
+    baseline = {r.identity: change_key(r) for r in first.snapshot.rows}
+    marked = Session(
+        baseline=baseline, mark_wall_time=BASE_TIME.timestamp(), marked=True
+    )
+    view = build(second, fake_clock, marked)
+    assert [rv.dispatch_id for rv in view.all_rows if rv.changed] == ["w-005"]
+    assert view.changes_line == "changed since 12:00 (1)"
+    restart = build(
+        second,
+        fake_clock,
+        Session(baseline=baseline, mark_wall_time=BASE_TIME.timestamp(), marked=False),
+    )
+    assert (
+        restart.changes_line
+        == "new baseline at 12:00 (observer started) | changed since 12:00 (1)"
+    )
+    # added and removed rows count too
+    smaller = dict(baseline)
+    gone = next(iter(smaller))
+    del smaller[gone]
+    smaller[("fixture:base", "w-gone")] = ()
+    counted = build(
+        second,
+        fake_clock,
+        Session(baseline=smaller, mark_wall_time=BASE_TIME.timestamp(), marked=True),
+    )
+    assert (
+        counted.changes_line == "changed since 12:00 (3)"
+    )  # w-005 changed, one added, one removed
+    assert build(second, fake_clock, Session()).changes_line is None  # no baseline yet
+
+
+def test_a_selected_row_that_left_the_source_stays_selected_with_a_placeholder(
+    fake_clock, argv_log
+):
+    collector = live_collector(
+        [
+            rows_reply(make_rows(3, 1), total=3),
+            rows_reply(make_rows(3, 1)[:2], total=2),
+        ],
+        fake_clock,
+        argv_log,
+    )
+    first = collector.run_once()
+    gone = next(r for r in first.snapshot.rows if r.dispatch_id == "w-003")
+    only_two = Collector(FixtureSource("empty"), fake_clock).run_once()
+    view = build(
+        only_two, fake_clock, Session(selected=gone.identity, selected_row=gone)
+    )
+    assert view.selection_note == "selected w-003 no longer in source window"
+    assert view.selected is not None and "not reobserved" in view.selected.flags
+    present = build(
+        first, fake_clock, Session(selected=gone.identity, selected_row=gone)
+    )
+    assert present.selection_note is None and present.selected.selected
+
+
+def test_inspector_is_built_only_in_inspector_focus_with_full_ids_and_worker_reported_labels(
+    fake_clock,
+):
+    result = fixture_result("long-identifiers", fake_clock)
+    ident = build(result, fake_clock).visible_rows[1].identity
+    view = build(result, fake_clock, Session(focus="inspector", selected=ident))
+    labels = [label for label, _ in view.inspector]
+    assert (
+        "projection.stage.detail (worker-reported)" in labels
+        and "unrecognised keys" in labels
+    )
+    assert dict(view.inspector)["dispatchId"] == view.selected.raw.dispatch_id
+    assert build(result, fake_clock, Session(selected=ident)).inspector is None
+
+
+def test_source_warnings_and_poll_errors_are_listed_in_the_inspector(
+    fake_clock, argv_log
+):
+    rows = make_rows(1, 1)
+    collector = live_collector(
+        [rows_reply(rows, total=1, warnings=["w one"]), (2, "", "\x1b[31mboom")],
+        fake_clock,
+        argv_log,
+    )
+    collector.run_once()
+    failed = collector.run_once()
+    view = build(
+        failed,
+        fake_clock,
+        Session(focus="inspector", selected=failed.snapshot.rows[0].identity),
+    )
+    inspector = dict(view.inspector)
+    assert (
+        inspector["source warning"] == "w one"
+        and inspector["last poll error (sanitized)"] == "boom"
+    )
+
+
+# -- typed snapshot fields on the View (AD-10) ------------------------------------------------------------------------------------------
+
+
+def test_the_view_carries_every_typed_snapshot_field_as_a_full_value(fake_clock):
+    view = build(fixture_result("base", fake_clock), fake_clock)
+    meta = view.meta
+    assert (meta.cycle, meta.namespace, meta.source_status, meta.source_error) == (
+        1,
+        "fixture:base",
+        "OK",
+        None,
+    )
+    assert (
+        meta.generated_at == "2026-11-08T12:00:00Z"
+        and meta.source_observed_at == "2026-11-08T12:00:00Z"
+    )
+    assert (meta.producer_name, meta.producer_version) == (
+        "superclaude-observe",
+        superclaude.__version__,
+    )
+    assert (meta.has_more, meta.total, meta.limit) == (False, 80, 100)
+    assert meta.scope == {"source": "all"} and set(meta.counts) == {
+        "active",
+        "reclaimable",
+        "retained",
+        "released",
+    }
+    assert (
+        meta.collection_state,
+        meta.collection_collected,
+        meta.collection_changed_during_read,
+        meta.collection_duplicates_ignored,
+    ) == ("COMPLETE", 80, False, 0)
+    assert all(rv.raw.dispatch_id == rv.dispatch_id for rv in view.all_rows)
+    not_polled = build(
+        Collector(FixtureSource("base"), fake_clock).latest(), fake_clock
+    ).meta
+    assert (
+        not_polled.source_status == "UNKNOWN"
+        and not_polled.source_observed_at is UNKNOWN
+    )
+    assert (
+        not_polled.scope is UNKNOWN
+        and not_polled.collection_state is None
+        and not_polled.total is UNKNOWN
+    )
+    collector = Collector(FixtureSource("source-loss"), fake_clock)
+    for _ in range(3):
+        failed = collector.run_once()
+    assert (
+        build(failed, fake_clock).meta.source_status,
+        build(failed, fake_clock).meta.source_error,
+    ) == ("ERROR", "timeout")
+    fake_clock.advance(60)
+    assert build(failed, fake_clock).meta.source_status == "ERROR"
+    stale_cycle = fixture_result("base", fake_clock)
+    fake_clock.advance(50)
+    assert build(stale_cycle, fake_clock).meta.source_status == "STALE"
+
+
+def test_all_rows_are_in_timestamp_order_newest_first_with_untimed_rows_last(
+    fake_clock,
+):
+    view = build(fixture_result("duplicate-out-of-order", fake_clock), fake_clock)
+    assert [rv.dispatch_id for rv in view.all_rows] == ["w-001", "w-002", "w-003"]
+    assert [rv.dispatch_id for rv in view.visible_rows] == [
+        "w-001",
+        "w-002",
+    ]  # w-003 is released
+    base = build(fixture_result("base", fake_clock), fake_clock)
+    assert [rv.dispatch_id for rv in base.all_rows[:3]] == ["w-001", "w-002", "w-003"]
+
+
+# -- purity --------------------------------------------------------------------------------------------------------------------------------
+
+
+class StrictClock:
+    """Only the three clock methods exist; anything else raises."""
+
+    def __init__(self, clock: FakeClock):
+        self._clock = clock
+
+    def monotonic(self):
+        return self._clock.monotonic()
+
+    def wall(self):
+        return self._clock.wall()
+
+    def local_tz(self):
+        return self._clock.local_tz()
+
+
+def test_same_inputs_build_equal_views_and_build_view_does_no_io(fake_clock):
+    result = fixture_result("injection", fake_clock)
+    session = Session(filter_text="w-inj", show_historical=True)
+    strict = StrictClock(fake_clock)
+    assert build_view(result, session, strict) == build_view(result, session, strict)
+    assert build_view(result, Session(), strict) == build_view(
+        result, Session(), strict
+    )
+    text = Path(view_module.__file__).read_text(encoding="utf-8")
+    assert not re.search(
+        r"^\s*(import time|from time|import datetime|from datetime|import os|import pathlib|from pathlib)",
+        text,
+        re.M,
+    )
+    assert not re.search(r"\b(time|datetime)\.\w+\(|\bopen\(", text)
+    assert not re.search(r"observe\.(adapter|collector|render|export)\b", text)
+    assert session == Session(
+        filter_text="w-inj", show_historical=True
+    )  # inputs untouched
+
+
+def test_view_reexports_unknown_and_is_the_only_place_that_names_it_as_a_screen_word():
+    assert view_module.UNKNOWN is UNKNOWN
+    for name in ("export.py", "render.py"):
+        path = Path(view_module.__file__).with_name(name)
+        if path.exists():
+            assert "observe.parse" not in path.read_text(encoding="utf-8")

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
