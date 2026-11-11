eb6b495c7b138fe38a6700dafc9bfb5ab252e734
Review one task for spec compliance.

Task brief: 
## Task 9: Add session transitions `apply_cycle` and `apply_key`

Depends on: Task 8

Extend `src/superclaude/cli/observe/view.py` and create `tests/observe/test_session.py`, following `ARCHITECTURE-SPINE.md` AD-15 and CD-2, `rendering-rules.md` sections "Keys", "Selection" and "Changes since last look", and tests T3, T8, T25 and T41 in `acceptance-tests.md`. Add `Effect` (`NONE`, `EXPORT`, `QUIT`) and two pure functions that are the only way a `Session` changes: `apply_cycle(session, result, clock) -> Session` (the first successful observation sets the baseline with no change flags; refreshes the selected row's last-known values) and `apply_key(session, key, view, clock) -> (Session, Effect)`. Keys: Up and Down or `j` and `k` move the selection, Enter opens the inspector, Esc returns, `/` enters filter mode (letters are text, Backspace edits, Enter or Esc leaves), `h` toggles historical rows, `m` replaces the baseline with the current rows and sets `mark_wall_time`, `e` returns `EXPORT`, `q` and Ctrl-C return `QUIT`; unknown keys do nothing; there is no `r` key and no key calls the adapter or collector. Selection is the row identity `(namespace, dispatchId)`, never an index; a refresh never changes focus or selection; when the selected row is not in the displayed set it stays selected from its last-known values and the view reads `selected <id> no longer in source window`; a row that dropped out of the source stays listed as `not reobserved`.

Acceptance criteria:
- [T9.AC1] `uv run pytest tests/observe/test_session.py -v` passes.
- [T9.AC2] T3: a test enumerates every key the loop can produce and asserts none reaches the adapter or collector (the functions take no such object and the module imports neither).
- [T9.AC3] T8: after `m`, a fixture step that changes one `nextAction.kind` stars exactly that row and the view shows `changed since HH:MM (1)`; rows added or removed also count.
- [T9.AC4] T41: the first observation is the baseline with no change flags, and a row missing from the next cycle shows `not reobserved`, not "unchanged".
- [T9.AC5] T25: a cycle that reorders rows keeps the cursor on the same identity, and a cycle that drops the selected row leaves the placeholder `selected <id> no longer in source window` until a movement key is pressed, never jumping to another worker.
- [T9.AC6] A test shows `m` never changes the collected, reported or source counts, and that filter mode treats `q` as text, not quit.
- [T9.AC7] A test shows `apply_key` and `apply_cycle` return new `Session` objects and never mutate their input.

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

Start sha: eb6b495c7b138fe38a6700dafc9bfb5ab252e734
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index ef7b5cf35..403b99f12 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -9,7 +9,8 @@ turns the ``UNKNOWN`` sentinel into screen words.
 from __future__ import annotations
 
 from collections.abc import Mapping
-from dataclasses import dataclass
+from dataclasses import dataclass, replace
+from enum import Enum
 from typing import Any
 
 from superclaude import __version__
@@ -589,12 +590,16 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
         (rv for rv in source_order if rv.identity == session.selected), None
     )
     selection_note = None
+    placeholder = False
     if (
         selected_view is None
         and session.selected is not None
         and session.selected_row is not None
     ):
         selected_view = make(session.selected_row, force_not_reobserved=True)
+        placeholder = True
+    if selected_view is not None and (placeholder or not selected_view.raw.reobserved):
+        # Gone from the source window, or read in an earlier cycle only: stays selected.
         selection_note = (
             f"selected {selected_view.dispatch_id} no longer in source window"
         )
@@ -641,3 +646,108 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
         else None,
         help_line=KEYS_LINE,
     )
+
+
+# -- session transitions: the only two ways a Session changes (AD-15) -----------------------
+
+
+class Effect(Enum):
+    """What the loop must do after a key; no effect ever reaches Orca."""
+
+    NONE = "none"
+    EXPORT = "export"
+    QUIT = "quit"
+
+
+def _baseline_of(rows: Any) -> dict:
+    return {r.identity: change_key(r) for r in rows if not r.identity_unknown}
+
+
+def apply_cycle(session: Session, result: Any, clock: Any) -> Session:
+    """A new cycle arrived: take the baseline on the first successful look, refresh the selection."""
+    snapshot = result.snapshot
+    changes: dict[str, Any] = {}
+    if (
+        session.baseline is None
+        and snapshot is not None
+        and result.last_success_mono is not None
+    ):
+        changes.update(
+            baseline=_baseline_of(snapshot.rows),
+            mark_wall_time=clock.wall(),
+            marked=False,
+        )
+    if snapshot is not None and session.selected is not None:
+        fresh = next((r for r in snapshot.rows if r.identity == session.selected), None)
+        if fresh is not None:
+            changes["selected_row"] = fresh  # last-known values follow the source
+    return replace(session, **changes)
+
+
+def _move(session: Session, view: View, step: int) -> Session:
+    rows = view.visible_rows
+    if not rows:
+        return replace(session)
+    index = next(
+        (i for i, r in enumerate(rows) if r.identity == session.selected), None
+    )
+    if index is None:  # nothing selected, or the selection is not in the list
+        target = 0 if step > 0 else len(rows) - 1
+    else:
+        target = min(max(index + step, 0), len(rows) - 1)
+    row = rows[target]
+    return replace(session, selected=row.identity, selected_row=row.raw)
+
+
+def _filter_key(session: Session, key: Key) -> Session:
+    if key.name == "text":
+        return replace(session, filter_text=session.filter_text + key.char)
+    if key.name == "backspace":
+        return replace(session, filter_text=session.filter_text[:-1])
+    if key.name in ("enter", "escape"):
+        return replace(session, focus="list")
+    return replace(session)  # arrows and the rest do nothing while typing
+
+
+def apply_key(
+    session: Session, key: Key, view: View, clock: Any
+) -> tuple[Session, Effect]:
+    """One key press. Keys change the session only; there is no refresh key and none reaches Orca."""
+    if key.name == "ctrl_c":
+        return replace(session), Effect.QUIT
+    if session.focus == "filter":
+        return _filter_key(session, key), Effect.NONE
+    name = key.name
+    char = key.char if name == "text" else ""
+    inspecting = session.focus == "inspector"
+    if name == "up" or char == "k":
+        return _move(session, view, -1), Effect.NONE
+    if name == "down" or char == "j":
+        return _move(session, view, 1), Effect.NONE
+    if char == "q":
+        return replace(session), Effect.QUIT
+    if char == "e":
+        return replace(session), Effect.EXPORT
+    if char == "m":
+        rows = tuple(rv.raw for rv in view.all_rows)
+        return (
+            replace(
+                session,
+                baseline=_baseline_of(rows),
+                mark_wall_time=clock.wall(),
+                marked=True,
+            ),
+            Effect.NONE,
+        )
+    if name == "escape" and inspecting:
+        return replace(session, focus="list"), Effect.NONE
+    if not inspecting:
+        if name == "enter" and view.selected is not None:
+            return replace(session, focus="inspector"), Effect.NONE
+        if char == "/":
+            return replace(session, focus="filter"), Effect.NONE
+        if char == "h":
+            return replace(
+                session, show_historical=not session.show_historical
+            ), Effect.NONE
+    return replace(session), Effect.NONE
diff --git a/tests/observe/test_session.py b/tests/observe/test_session.py
new file mode 100644
index 000000000..66c197623
--- /dev/null
+++ b/tests/observe/test_session.py
@@ -0,0 +1,433 @@
+"""Session transition tests (AD-15, CD-2; T3, T8, T25, T41 in acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import copy
+import inspect
+import json
+import re
+import string
+from pathlib import Path
+
+import pytest
+
+import superclaude.cli.observe.view as view_module
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.view import (
+    Effect,
+    Key,
+    Session,
+    apply_cycle,
+    apply_key,
+    build_view,
+)
+from tests.observe.conftest import (
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_rows,
+)
+
+
+def text(char):
+    return Key("text", char)
+
+
+def view_of(result, session, clock):
+    return build_view(result, session, clock)
+
+
+def press(session, key, result, clock):
+    """Build the view for this session, apply one key, return (session, effect)."""
+    return apply_key(session, key, build_view(result, session, clock), clock)
+
+
+def live_collector(responses, clock, argv_log):
+    runner = FakeRunner(argv_log, responses)
+    return Collector(LiveSource(runner, FakeDiscover(argv_log)), clock)
+
+
+def reply(rows):
+    return 0, json.dumps(make_envelope(rows, total=len(rows)))
+
+
+def three_active_rows(clock):
+    """One cycle with three active rows w-001..w-003, none historical."""
+    return live_collector([reply(make_rows(3, 1))], clock, []).run_once()
+
+
+def fixture_cycles(variant, clock, count):
+    collector = Collector(FixtureSource(variant), clock)
+    return [collector.run_once() for _ in range(count)]
+
+
+# -- apply_cycle ---------------------------------------------------------------------------------
+
+
+def test_the_first_successful_observation_is_the_baseline_with_no_change_flags(
+    fake_clock,
+):
+    (first,) = fixture_cycles("base", fake_clock, 1)
+    session = apply_cycle(Session(), first, fake_clock)
+    assert session.baseline is not None and len(session.baseline) == 80
+    assert session.mark_wall_time == fake_clock.wall() and session.marked is False
+    view = view_of(first, session, fake_clock)
+    assert not any(rv.changed for rv in view.all_rows)
+    assert (
+        view.changes_line
+        == "new baseline at 12:00 (observer started) | changed since 12:00 (0)"
+    )
+
+
+def test_no_baseline_is_taken_before_a_successful_read(fake_clock, argv_log):
+    collector = live_collector([(2, "")], fake_clock, argv_log)
+    assert apply_cycle(Session(), collector.latest(), fake_clock).baseline is None
+    failed = collector.run_once()
+    assert failed.state == "FAILED"
+    assert apply_cycle(Session(), failed, fake_clock).baseline is None
+    unavailable = live_collector([reply([])], fake_clock, []).latest()
+    assert apply_cycle(Session(), unavailable, fake_clock).baseline is None
+
+
+def test_a_later_cycle_never_replaces_the_baseline(fake_clock):
+    first, second = fixture_cycles("base", fake_clock, 2)
+    session = apply_cycle(Session(), first, fake_clock)
+    fake_clock.advance(30)
+    later = apply_cycle(session, second, fake_clock)
+    assert (
+        later.baseline == session.baseline
+        and later.mark_wall_time == session.mark_wall_time
+    )
+
+
+def test_an_empty_first_observation_still_sets_the_baseline(fake_clock):
+    (empty,) = fixture_cycles("empty", fake_clock, 1)
+    assert apply_cycle(Session(), empty, fake_clock).baseline == {}
+
+
+def test_apply_cycle_refreshes_the_selected_rows_last_known_values(fake_clock):
+    first, second = fixture_cycles("base", fake_clock, 2)
+    session = apply_cycle(Session(), first, fake_clock)
+    row = next(r for r in first.snapshot.rows if r.dispatch_id == "w-005")
+    ident = row.identity
+    session = Session(selected=ident, selected_row=row, baseline=session.baseline)
+    assert session.selected_row.next_action_kind == "none"
+    session = apply_cycle(session, second, fake_clock)
+    assert (
+        session.selected_row.next_action_kind == "approve" and session.selected == ident
+    )
+
+
+# -- T8: m marks, a changed row is starred ------------------------------------------------------------
+
+
+def test_after_m_a_changed_next_action_stars_exactly_that_row(fake_clock):
+    first, second = fixture_cycles("base", fake_clock, 2)
+    session = apply_cycle(Session(), first, fake_clock)
+    session, effect = press(session, text("m"), first, fake_clock)
+    assert effect is Effect.NONE and session.marked is True
+    session = apply_cycle(session, second, fake_clock)
+    view = view_of(second, session, fake_clock)
+    assert [rv.dispatch_id for rv in view.all_rows if rv.changed] == ["w-005"]
+    assert view.changes_line == "changed since 12:00 (1)"
+
+
+def test_added_and_removed_rows_count_in_changed_since(fake_clock, argv_log):
+    rows = make_rows(4, 1)
+    collector = live_collector(
+        [reply(rows[:3]), reply([rows[0], rows[1], rows[3]])], fake_clock, argv_log
+    )
+    first = collector.run_once()
+    session, _ = press(
+        apply_cycle(Session(), first, fake_clock), text("m"), first, fake_clock
+    )
+    second = collector.run_once()  # w-004 added; w-003 not returned
+    view = view_of(second, apply_cycle(session, second, fake_clock), fake_clock)
+    assert [rv.dispatch_id for rv in view.all_rows if rv.changed] == ["w-004"]
+    assert (
+        view.changes_line == "changed since 12:00 (1)"
+    )  # w-003 is kept, flagged not reobserved
+    assert (
+        "not reobserved"
+        in next(rv for rv in view.all_rows if rv.dispatch_id == "w-003").flags
+    )
+
+
+def test_m_replaces_the_baseline_and_never_changes_any_count(fake_clock):
+    first, second = fixture_cycles("base", fake_clock, 2)
+    session = apply_cycle(Session(), first, fake_clock)
+    before = view_of(second, session, fake_clock)
+    fake_clock.advance(90)
+    marked, _ = press(session, text("m"), second, fake_clock)
+    after = view_of(second, marked, fake_clock)
+    assert marked.mark_wall_time == fake_clock.wall() != session.mark_wall_time
+    assert after.counts_tokens == before.counts_tokens
+    assert (
+        after.collected_text == before.collected_text
+        and after.meta.counts == before.meta.counts
+    )
+    assert after.changes_line.endswith("(0)") and not any(
+        rv.changed for rv in after.all_rows
+    )
+
+
+# -- T41: first look and dropped rows ------------------------------------------------------------------------
+
+
+def test_a_row_missing_from_the_next_cycle_shows_not_reobserved_not_unchanged(
+    fake_clock, argv_log
+):
+    rows = make_rows(3, 1)
+    collector = live_collector([reply(rows), reply(rows[:2])], fake_clock, argv_log)
+    first = collector.run_once()
+    session = apply_cycle(Session(), first, fake_clock)
+    second = collector.run_once()
+    view = view_of(second, apply_cycle(session, second, fake_clock), fake_clock)
+    dropped = next(rv for rv in view.all_rows if rv.dispatch_id == "w-003")
+    assert "not reobserved" in dropped.flags and dropped.changed is False
+    assert view.changes_line.endswith("(0)")
+
+
+# -- T25: selection is anchored to identity ----------------------------------------------------------------------
+
+
+def test_a_reordering_cycle_keeps_the_cursor_on_the_same_identity(fake_clock, argv_log):
+    rows = make_rows(3, 1)
+    collector = live_collector(
+        [reply(rows), reply(list(reversed(rows)))], fake_clock, argv_log
+    )
+    first = collector.run_once()
+    session = apply_cycle(Session(), first, fake_clock)
+    session, _ = press(session, Key("down"), first, fake_clock)
+    session, _ = press(session, Key("down"), first, fake_clock)
+    assert view_of(first, session, fake_clock).selected.dispatch_id == "w-002"
+    second = collector.run_once()
+    session = apply_cycle(session, second, fake_clock)
+    view = view_of(second, session, fake_clock)
+    assert view.selected.dispatch_id == "w-002" and view.selected.selected
+    assert [rv.dispatch_id for rv in view.visible_rows] == ["w-003", "w-002", "w-001"]
+    assert view.selection_note is None
+
+
+def test_a_dropped_selected_row_stays_selected_until_a_movement_key(
+    fake_clock, argv_log
+):
+    rows = make_rows(3, 1)
+    collector = live_collector(
+        [reply(rows), reply([rows[0], rows[2]])], fake_clock, argv_log
+    )
+    first = collector.run_once()
+    session = apply_cycle(Session(), first, fake_clock)
+    session, _ = press(session, Key("down"), first, fake_clock)
+    session, _ = press(session, Key("down"), first, fake_clock)
+    assert session.selected_row.dispatch_id == "w-002"
+    second = collector.run_once()
+    session = apply_cycle(session, second, fake_clock)
+    view = view_of(second, session, fake_clock)
+    assert view.selection_note == "selected w-002 no longer in source window"
+    assert (
+        view.selected.dispatch_id == "w-002" and "not reobserved" in view.selected.flags
+    )
+    # a cycle that drops the row altogether leaves the placeholder from its last-known values
+    gone = Collector(FixtureSource("empty"), fake_clock).run_once()
+    placeholder = view_of(gone, apply_cycle(session, gone, fake_clock), fake_clock)
+    assert placeholder.selection_note == "selected w-002 no longer in source window"
+    assert placeholder.selected.dispatch_id == "w-002"
+    # until a movement key is pressed: then the selection goes to a real row
+    moved, _ = press(
+        session, Key("up"), second, fake_clock
+    )  # w-002 is last in source order
+    assert moved.selected != session.selected
+    assert view_of(second, moved, fake_clock).selection_note is None
+
+
+# -- keys ------------------------------------------------------------------------------------------------------------
+
+
+def test_movement_keys_select_by_identity_and_clamp_at_the_ends(fake_clock):
+    result = three_active_rows(fake_clock)
+    session = Session()
+    ids = []
+    for key in (
+        Key("down"),
+        text("j"),
+        Key("down"),
+        Key("down"),
+    ):  # the last one clamps
+        session, effect = press(session, key, result, fake_clock)
+        assert effect is Effect.NONE
+        ids.append(view_of(result, session, fake_clock).selected.dispatch_id)
+    assert ids == ["w-001", "w-002", "w-003", "w-003"]
+    top = session
+    for key in (Key("up"), text("k"), Key("up")):
+        top, _ = press(top, key, result, fake_clock)
+    assert view_of(result, top, fake_clock).selected.dispatch_id == "w-001"
+    from_nothing, _ = press(Session(), Key("up"), result, fake_clock)
+    assert view_of(result, from_nothing, fake_clock).selected.dispatch_id == "w-003"
+    empty = Collector(FixtureSource("empty"), fake_clock).run_once()
+    none_selected, _ = press(Session(), Key("down"), empty, fake_clock)
+    assert none_selected.selected is None
+
+
+def test_enter_opens_the_inspector_and_escape_returns(fake_clock):
+    result = three_active_rows(fake_clock)
+    nothing, _ = press(Session(), Key("enter"), result, fake_clock)
+    assert nothing.focus == "list"  # nothing selected: nothing to inspect
+    selected, _ = press(Session(), Key("down"), result, fake_clock)
+    opened, effect = press(selected, Key("enter"), result, fake_clock)
+    assert (opened.focus, effect) == ("inspector", Effect.NONE)
+    assert view_of(result, opened, fake_clock).inspector is not None
+    still, _ = press(opened, Key("enter"), result, fake_clock)
+    assert still.focus == "inspector"
+    moved, _ = press(opened, Key("down"), result, fake_clock)
+    assert moved.focus == "inspector" and moved.selected != opened.selected
+    back, effect = press(opened, Key("escape"), result, fake_clock)
+    assert (back.focus, effect) == ("list", Effect.NONE)
+    same, effect = press(selected, Key("escape"), result, fake_clock)
+    assert (same.focus, effect) == ("list", Effect.NONE)  # Esc in the list does nothing
+
+
+def test_filter_mode_takes_letters_as_text_including_q_and_edits_with_backspace(
+    fake_clock,
+):
+    (result,) = fixture_cycles("base", fake_clock, 1)
+    session, effect = press(Session(), text("/"), result, fake_clock)
+    assert (session.focus, effect) == ("filter", Effect.NONE)
+    for char in "qjhme/r":
+        session, effect = press(session, text(char), result, fake_clock)
+        assert effect is Effect.NONE and session.focus == "filter"
+    assert session.filter_text == "qjhme/r"
+    session, _ = press(session, Key("backspace"), result, fake_clock)
+    session, _ = press(session, Key("backspace"), result, fake_clock)
+    assert session.filter_text == "qjhme"
+    ignored, effect = press(session, Key("down"), result, fake_clock)
+    assert (
+        ignored.filter_text == "qjhme"
+        and ignored.selected is None
+        and effect is Effect.NONE
+    )
+    left, _ = press(session, Key("enter"), result, fake_clock)
+    assert (left.focus, left.filter_text) == ("list", "qjhme")
+    escaped, _ = press(session, Key("escape"), result, fake_clock)
+    assert (escaped.focus, escaped.filter_text) == ("list", "qjhme")
+    quit_session, effect = press(session, Key("ctrl_c"), result, fake_clock)
+    assert effect is Effect.QUIT and quit_session.focus == "filter"
+    empty_backspace, _ = press(
+        Session(focus="filter"), Key("backspace"), result, fake_clock
+    )
+    assert empty_backspace.filter_text == ""
+    assert view_of(
+        result, Session(filter_text="run-b"), fake_clock
+    ).filter_line.startswith("filter run-b")
+
+
+def test_h_toggles_historical_rows_and_e_exports_and_q_quits(fake_clock):
+    (result,) = fixture_cycles("historical", fake_clock, 1)
+    session, effect = press(Session(), text("h"), result, fake_clock)
+    assert session.show_historical is True and effect is Effect.NONE
+    assert len(view_of(result, session, fake_clock).visible_rows) == 9
+    session, _ = press(session, text("h"), result, fake_clock)
+    assert session.show_historical is False
+    exported, effect = press(session, text("e"), result, fake_clock)
+    assert effect is Effect.EXPORT and exported == session
+    for key in (text("q"), Key("ctrl_c")):
+        quit_session, effect = press(session, key, result, fake_clock)
+        assert effect is Effect.QUIT and quit_session == session
+
+
+def test_unknown_keys_do_nothing_and_there_is_no_refresh_key(fake_clock):
+    (result,) = fixture_cycles("base", fake_clock, 1)
+    session = Session(
+        selected=result.snapshot.rows[0].identity, selected_row=result.snapshot.rows[0]
+    )
+    for key in (
+        text("r"),
+        text("x"),
+        text("Z"),
+        text("1"),
+        text(" "),
+        Key("backspace"),
+    ):
+        after, effect = press(session, key, result, fake_clock)
+        assert (after, effect) == (session, Effect.NONE), key
+
+
+# -- T3: no key reaches Orca; nothing mutates ------------------------------------------------------------------------------
+
+
+def test_no_key_can_reach_the_adapter_or_collector(fake_clock):
+    (result,) = fixture_cycles("shared-unmapped", fake_clock, 1)
+    assert list(inspect.signature(apply_key).parameters) == [
+        "session",
+        "key",
+        "view",
+        "clock",
+    ]
+    assert list(inspect.signature(apply_cycle).parameters) == [
+        "session",
+        "result",
+        "clock",
+    ]
+    source = Path(view_module.__file__).read_text(encoding="utf-8")
+    assert not re.search(r"observe\.(adapter|collector)\b|import subprocess", source)
+    keys = [
+        Key(name) for name in ("up", "down", "enter", "escape", "backspace", "ctrl_c")
+    ]
+    keys += [text(c) for c in string.printable.strip() + " " + "é日"]
+    effects = {}
+    for focus in ("list", "inspector", "filter"):
+        for key in keys:
+            session, effect = apply_key(
+                Session(focus=focus, selected=result.snapshot.rows[0].identity),
+                key,
+                view_of(result, Session(focus=focus), fake_clock),
+                fake_clock,
+            )
+            assert isinstance(session, Session) and isinstance(effect, Effect)
+            effects.setdefault(effect, set()).add((focus, key.name, key.char))
+    assert {f[2] or f[1] for f in effects[Effect.EXPORT]} == {"e"}
+    assert {f[2] or f[1] for f in effects[Effect.QUIT]} == {"q", "ctrl_c"}
+    # in filter mode only Ctrl-C quits; "q" and "e" are text there
+    assert {f[1:] for f in effects[Effect.QUIT] if f[0] == "filter"} == {("ctrl_c", "")}
+    assert not any(f[0] == "filter" for f in effects[Effect.EXPORT])
+
+
+def test_transitions_return_new_sessions_and_never_mutate_their_input(fake_clock):
+    first, second = fixture_cycles("base", fake_clock, 2)
+    session = apply_cycle(Session(), first, fake_clock)
+    snapshot = copy.deepcopy(session)
+    view = view_of(first, session, fake_clock)
+    keys = [
+        Key("down"),
+        Key("enter"),
+        text("m"),
+        text("h"),
+        text("/"),
+        text("q"),
+        text("e"),
+        Key("escape"),
+    ]
+    for key in keys:
+        new, _ = apply_key(session, key, view, fake_clock)
+        assert new is not session and session == snapshot
+    assert (
+        apply_cycle(session, second, fake_clock) is not session and session == snapshot
+    )
+    marked, _ = apply_key(session, text("m"), view, fake_clock)
+    assert (
+        marked.baseline is not session.baseline
+        and session.baseline == snapshot.baseline
+    )
+
+
+def test_session_defaults_are_the_start_up_state():
+    session = Session()
+    assert (session.focus, session.selected, session.filter_text) == ("list", None, "")
+    assert (session.show_historical, session.baseline, session.mark_wall_time) == (
+        False,
+        None,
+        None,
+    )
+    with pytest.raises(Exception):
+        session.focus = "filter"  # frozen

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
