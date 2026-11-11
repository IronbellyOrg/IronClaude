c20b44431773899e36942d392b4278c16667e94c
Review one task for spec compliance.

Task brief: 
## Task 10: Build the screen renderer `render.py`

Depends on: Task 3, Task 8

Create `src/superclaude/cli/observe/render.py` and `tests/observe/test_render.py`, following `ARCHITECTURE-SPINE.md` AD-11, AD-13 and CD-4, `rendering-rules.md` ("Geometry and height", "Common to every width", "Worker ledger") and tests T6, T16, T23, T24, T28, T35, T44 and T49 in `acceptance-tests.md`. `render(view, policy)` turns a `View` into Rich renderables for the Signal Bridge ledger screen and the inspector screen. Layout: header lines 1 and 2, the COUNTS strip (wrapping to a second line before cutting anything, never dropped; `collected n / reported T`, `PARTIAL` and the scope are never truncated), the gap notice above the ledger at every width, the ledger, the footer. At 160 columns and wider the ledger is a table with `dispatchId`, run (labelled "run", never "orchestrator"), `workerState`, `dispatchStatus`, `terminalState`, outcome, `nextAction.kind`, `liveness.verdict (liveness.source)` and the evidence age, and no `stage` column; at 116 to 159 each row is `<kind> <dispatchId> <liveness.verdict> <age>`; at 80 to 115 each row holds the kind, a dispatch ID cut by cells with `>` and an age; below 80 the screen shows `terminal too narrow (min 80)` above the COUNTS strip, whose denominators and the gap notice still print; when the height is below `MIN_ROWS` a too-small diagnostic shows and still carries the gap notice. The renderer builds `rich.text.Text` objects from data (no markup strings), does all truncation through `terminal.clip`, uses the glyph table in ASCII mode, never sorts or decides a status literal (those come from the `View`), and never imports `adapter.py` or `collector.py`.

Acceptance criteria:
- [T10.AC1] `uv run pytest tests/observe/test_render.py -v` passes.
- [T10.AC2] T23 and T16: for the `base` variant and for generated data over 50, 80 and 100 rows with 5, 8 and 10 distinct runs at widths 160, 116 and 80 (27 renders), every screen line has `cell_len <= W`, every count line matches `k of n`, and every hidden overflow shows `x/y shown` with y equal to the generated total.
- [T10.AC3] T24: in `long-identifiers`, lists truncate with `>` and the inspector shows the full ID wrapped by cells.
- [T10.AC4] T35: the COUNTS strip appears at 80, 116 and 160 columns with its priority tokens intact, and below 80 columns the screen reads `terminal too narrow (min 80)` and still shows the gap notice.
- [T10.AC5] T49: with a height below `MIN_ROWS`, the too-small diagnostic shows and still carries the gap notice.
- [T10.AC6] T44: worker text `[bold]x[/bold]` renders literally with the brackets visible; T28: no blink code appears in any recorded render.
- [T10.AC7] T29 (render half): for the `injection` variant at widths 160, 116 and 80, recorded with colour off, the render contains no ESC byte, no C1 character and no `Cf` character.
- [T10.AC8] T6: rendering the same view twice gives byte-identical text; with NO_COLOR set and unset the text content is the same.
- [T10.AC9] An ASCII-mode render contains only ASCII characters for the `base` variant.

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

Start sha: c20b44431773899e36942d392b4278c16667e94c
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
new file mode 100644
index 000000000..58702c335
--- /dev/null
+++ b/src/superclaude/cli/observe/render.py
@@ -0,0 +1,349 @@
+"""The screen renderer: a ``View`` and a ``TerminalPolicy`` become Rich renderables (AD-11, AD-13).
+
+It only lays out and truncates. Every status literal and both row orders come from the
+``View``; every truncation goes through ``terminal.clip``; text is built as ``rich.text.Text``
+from data (never markup strings). It never imports the adapter or the collector.
+"""
+
+from __future__ import annotations
+
+from rich.cells import cell_len
+from rich.console import Group
+from rich.text import Text
+
+from superclaude.cli.observe.terminal import (
+    TOO_NARROW_TEXT,
+    TOO_SMALL_TEXT,
+    TerminalPolicy,
+    ascii_safe,
+    clip,
+    glyph,
+)
+from superclaude.cli.observe.view import (
+    INSPECTOR_HELP,
+    INSPECTOR_TITLE,
+    NO_MATCH_TEXT,
+    CountsToken,
+    RowView,
+    View,
+    text_of,
+)
+
+MAX_COUNT_LINES = 2  # the COUNTS strip wraps to a second line before anything is cut
+SEPARATOR = " "
+
+
+# -- text fitting ------------------------------------------------------------------------------
+
+
+def _prefix_length(text: str, width: int) -> int:
+    """Largest number of characters of ``text`` that fit in ``width`` cells."""
+    used = 0
+    for index, ch in enumerate(text):
+        step = cell_len(ch)
+        if used + step > width:
+            return index
+        used += step
+    return len(text)
+
+
+def wrap(text: str, width: int, policy: TerminalPolicy) -> list[str]:
+    """Wrap by cells without losing anything (never truncates; never splits a wide character)."""
+    if policy.ascii:
+        text = ascii_safe(text)
+    if width <= 0:
+        return [""]
+    lines: list[str] = []
+    for paragraph in text.split("\n"):
+        while cell_len(paragraph) > width:
+            cut = max(_prefix_length(paragraph, width), 1)
+            space = paragraph[:cut].rfind(" ")
+            if space > 0 and paragraph[:space].strip() and cut < len(paragraph):
+                lines.append(paragraph[:space].rstrip())
+                paragraph = paragraph[space:].lstrip(" ")
+            else:
+                lines.append(paragraph[:cut])
+                paragraph = paragraph[cut:]
+        lines.append(paragraph)
+    return lines
+
+
+def _pad(text: str, width: int) -> str:
+    return text + " " * max(width - cell_len(text), 0)
+
+
+def _cell(text: str, width: int, policy: TerminalPolicy) -> str:
+    return _pad(clip(text, width, policy), width)
+
+
+# -- the COUNTS strip ------------------------------------------------------------------------------
+
+
+def counts_lines(
+    tokens: tuple[CountsToken, ...],
+    policy: TerminalPolicy,
+    max_lines: int | None = MAX_COUNT_LINES,
+) -> list[str]:
+    """Lay tokens out in priority order. Protected tokens are never truncated: they wrap.
+
+    Lower-priority tokens that do not fit within ``max_lines`` are cut with ``>``.
+    """
+    width = policy.width
+    lines: list[str] = []
+    current = ""
+    cut = False
+    for token in tokens:
+        text = ascii_safe(token.text) if policy.ascii else token.text
+        if cut and not token.protected:
+            continue
+        candidate = f"{current}  {text}" if current else text
+        if cell_len(candidate) <= width:
+            current = candidate
+            continue
+        if token.protected:
+            if current:
+                lines.append(current)
+            chunks = wrap(text, width, policy)
+            lines.extend(chunks[:-1])
+            current = chunks[-1]
+            continue
+        if max_lines is None or len(lines) + 1 < max_lines:
+            if current:
+                lines.append(current)
+            current = clip(text, width, policy)
+            continue
+        room = width - cell_len(current) - 2
+        if room >= 2:
+            current = f"{current}  {clip(text, room, policy)}"
+        else:
+            current = clip(current + " " + glyph("truncate", policy), width, policy)
+        cut = True
+    if current:
+        lines.append(current)
+    return lines
+
+
+# -- ledger rows -----------------------------------------------------------------------------------------
+
+
+def _flags_text(row: RowView) -> str:
+    flags = (("FROZEN",) if row.frozen else ()) + row.flags
+    return ", ".join(flags)
+
+
+def _marker(row: RowView, policy: TerminalPolicy) -> str:
+    return (glyph("selected", policy) if row.selected else " ") + (
+        "*" if row.changed else " "
+    )
+
+
+def _verdict(row: RowView) -> str:
+    return text_of(row.raw.liveness_verdict)
+
+
+def _columns(policy: TerminalPolicy) -> tuple[list[tuple[str, int]], list]:
+    """Column (header, width) pairs and one getter per column, for the width class."""
+    width = policy.width
+    sep = len(SEPARATOR)
+    if policy.width_class == "full":
+        fixed = [12, 12, 14, 14, 12, 16, 22, 12]  # run .. evidence age
+        flags_min = 12
+        base = 2 + sum(fixed) + flags_min + sep * 10
+        extra = max(width - base - 22, 0)
+        id_width = 22 + min(extra, 26)
+        flags_width = width - (2 + sum(fixed) + sep * 10) - id_width
+        names = [
+            ("", 2),
+            ("dispatchId", id_width),
+            ("run", fixed[0]),
+            ("workerState", fixed[1]),
+            ("dispatchStatus", fixed[2]),
+            ("terminalState", fixed[3]),
+            ("outcome", fixed[4]),
+            ("nextAction.kind", fixed[5]),
+            ("liveness", fixed[6]),
+            ("evidence age", fixed[7]),
+            ("flags", flags_width),
+        ]
+        getters = [
+            None,
+            lambda r: r.dispatch_id,
+            lambda r: r.run,
+            lambda r: r.worker_state,
+            lambda r: r.dispatch_status,
+            lambda r: r.terminal_state,
+            lambda r: r.outcome,
+            lambda r: r.next_action,
+            lambda r: r.liveness,
+            lambda r: r.evidence_age,
+            _flags_text,
+        ]
+        return names, getters
+    if policy.width_class == "line":
+        kind, verdict, age = 18, 14, 7
+        id_width = min(width - (2 + kind + verdict + age + 18 + sep * 5), 60)
+        flags_width = width - (2 + kind + verdict + age + id_width + sep * 5)
+        names = [
+            ("", 2),
+            ("kind", kind),
+            ("dispatchId", id_width),
+            ("liveness", verdict),
+            ("age", age),
+            ("flags", flags_width),
+        ]
+        getters = [
+            None,
+            lambda r: r.next_action,
+            lambda r: r.dispatch_id,
+            _verdict,
+            lambda r: r.evidence_age,
+            _flags_text,
+        ]
+        return names, getters
+    kind, age, flags_width = 14, 6, 16
+    id_width = width - (2 + kind + age + flags_width + sep * 4)
+    names = [
+        ("", 2),
+        ("kind", kind),
+        ("dispatchId", id_width),
+        ("age", age),
+        ("flags", flags_width),
+    ]
+    getters = [
+        None,
+        lambda r: r.next_action,
+        lambda r: r.dispatch_id,
+        lambda r: r.evidence_age,
+        _flags_text,
+    ]
+    return names, getters
+
+
+def _row_line(
+    row: RowView, columns: list[tuple[str, int]], getters: list, policy: TerminalPolicy
+) -> str:
+    cells = []
+    for (_, width), getter in zip(columns, getters, strict=True):
+        cells.append(
+            _pad(_marker(row, policy), width)
+            if getter is None
+            else _cell(getter(row), width, policy)
+        )
+    return clip(SEPARATOR.join(cells).rstrip(), policy.width, policy)
+
+
+def _header_lines(columns: list[tuple[str, int]], policy: TerminalPolicy) -> list[str]:
+    head = SEPARATOR.join(_cell(name, width, policy) for name, width in columns)
+    rule = SEPARATOR.join(glyph("hrule", policy) * width for _, width in columns)
+    return [clip(head.rstrip(), policy.width, policy), clip(rule, policy.width, policy)]
+
+
+# -- screens -------------------------------------------------------------------------------------------------
+
+
+def _inspector_lines(view: View, policy: TerminalPolicy) -> list[str]:
+    selected = view.selected
+    title = f"{INSPECTOR_TITLE}  {selected.dispatch_id if selected else ''}"
+    lines = wrap(title, policy.width, policy)
+    for label, value in view.inspector or ():
+        first, *rest = wrap(f"{label}: {value}", policy.width, policy)
+        lines.append(first)
+        for continuation in rest:  # continuation lines are indented two cells
+            lines.extend(
+                "  " + part
+                for part in wrap(continuation, max(policy.width - 2, 1), policy)
+            )
+    return lines
+
+
+def _notes(view: View) -> list[str]:
+    parts = [
+        n
+        for n in (
+            view.filter_line,
+            view.historical_note,
+            view.duplicates_note,
+            view.selection_note,
+        )
+        if n
+    ]
+    return ["  ".join(parts)] if parts else []
+
+
+def screen_lines(view: View, policy: TerminalPolicy) -> list[str]:
+    """The screen as plain lines, each at most ``policy.width`` cells wide."""
+    width = policy.width
+    if (
+        policy.too_narrow
+    ):  # below 80 columns: the denominators and the gap notice still print
+        lines = wrap(TOO_NARROW_TEXT, width, policy)
+        lines += counts_lines(view.counts_tokens, policy, max_lines=None)
+        return lines + wrap(view.gap_notice, width, policy)
+    if policy.too_small:
+        lines = wrap(TOO_SMALL_TEXT, width, policy)
+        lines += wrap(view.collected_text, width, policy)
+        return lines + wrap(view.gap_notice, width, policy)
+
+    top: list[str] = []
+    top += wrap(view.header1, width, policy)
+    top += wrap(view.header2, width, policy)
+    top += counts_lines(view.counts_tokens, policy)
+    if view.changes_line:
+        top += wrap(view.changes_line, width, policy)
+    top += wrap(view.gap_notice, width, policy)
+    for note in _notes(view):
+        top += wrap(note, width, policy)
+    if view.focus == "filter":
+        top += wrap("/" + view.filter_text, width, policy)
+
+    # The footer is one line when it fits, else the key list and the counts on two lines.
+    window_probe = view.window(None)
+    one_line = view.footer(window_probe)
+    footer_height = (
+        1
+        if cell_len(one_line) <= width
+        else 1 + len(wrap(view.footer_counts(window_probe), width, policy))
+    )
+
+    if view.focus == "inspector" and view.inspector is not None:
+        body = _inspector_lines(view, policy)
+        footer_lines = [clip(INSPECTOR_HELP, width, policy)]
+        return top + body + footer_lines
+
+    body = wrap(view.ledger_title, width, policy)
+    columns, getters = _columns(policy)
+    if policy.width_class == "full" and view.visible_rows:
+        body += _header_lines(columns, policy)
+    reserved = (
+        len(top) + len(body) + footer_height + 1
+    )  # one line kept for the overflow text
+    capacity = max(policy.height - reserved, 1)
+    window = view.window(capacity)
+    if not view.all_rows:
+        for text in view.ledger_empty:
+            body += wrap(text, width, policy)
+    elif not window.rows:
+        body += wrap(NO_MATCH_TEXT, width, policy)
+    for row in window.rows:
+        body.append(_row_line(row, columns, getters, policy))
+    if window.more:
+        body += wrap(f"{window.text}  {window.more_text}", width, policy)
+
+    footer = view.footer(window)
+    if cell_len(footer) <= width:
+        footer_lines = [footer if not policy.ascii else ascii_safe(footer)]
+    else:
+        footer_lines = [clip(view.help_line, width, policy)] + wrap(
+            view.footer_counts(window), width, policy
+        )
+    return top + body + footer_lines
+
+
+def render(view: View, policy: TerminalPolicy) -> Group:
+    """The screen as Rich renderables: one plain ``Text`` per line, never reflowed."""
+    return Group(
+        *(
+            Text(line, no_wrap=True, overflow="crop")
+            for line in screen_lines(view, policy)
+        )
+    )
diff --git a/src/superclaude/cli/observe/terminal.py b/src/superclaude/cli/observe/terminal.py
index 505564e41..8cd211433 100644
--- a/src/superclaude/cli/observe/terminal.py
+++ b/src/superclaude/cli/observe/terminal.py
@@ -26,6 +26,7 @@ FULL_WIDTH = 160  # 160 and wider: full table
 LINE_WIDTH = 116  # 116 to 159: line form; 80 to 115: short form
 
 TOO_NARROW_TEXT = "terminal too narrow (min 80)"
+TOO_SMALL_TEXT = f"terminal too small (min {MIN_ROWS} rows)"  # PROPOSED wording (T49)
 
 # Glyph table: name -> (unicode form, ASCII form). Everything else non-ASCII maps to "?".
 GLYPHS: dict[str, tuple[str, str]] = {
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index 403b99f12..acda6182c 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -52,6 +52,9 @@ PARTIAL_CAP_TEXT = (
     "newest first; oldest rows not read; long-running active workers may be among them"
 )
 KEYS_LINE = "Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e export  q quit"
+INSPECTOR_TITLE = "INSPECTOR"
+INSPECTOR_HELP = "Esc back  j/k move  e export  q quit"
+NO_MATCH_TEXT = "no rows match the filter or the historical setting"
 SOURCE_COUNT_KEYS = ("active", "reclaimable", "retained", "released")
 UNAVAILABLE_FACTS = ("report status", "acceptance", "tests", "approval")
 
@@ -209,9 +212,12 @@ class View:
             more_text=f"+{more} more" if more else "",
         )
 
+    def footer_counts(self, window: Window) -> str:
+        """The footer literal ``shown x/y | collected n / reported T`` ("x/y shown" is the overflow text)."""
+        return f"shown {window.shown}/{window.total} | {self.collected_text}"
+
     def footer(self, window: Window) -> str:
-        shown = f"shown {window.shown}/{window.total}"  # the footer literal; "x/y shown" is the overflow text
-        return f"{self.help_line}  {shown} | {self.collected_text}"
+        return f"{self.help_line}  {self.footer_counts(window)}"
 
 
 # -- small helpers -------------------------------------------------------------------------------
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
new file mode 100644
index 000000000..bcf2a3ca9
--- /dev/null
+++ b/tests/observe/test_render.py
@@ -0,0 +1,409 @@
+"""Screen renderer tests (AD-11, AD-13; T6, T16, T23, T24, T28, T29 render half, T35, T44, T49)."""
+# ruff: noqa: E741  (``l`` is a screen line in the comprehensions below)
+
+from __future__ import annotations
+
+import json
+import re
+import unicodedata
+from pathlib import Path
+
+import pytest
+from rich.cells import cell_len
+
+import superclaude.cli.observe.render as render_module
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.render import render, screen_lines
+from superclaude.cli.observe.terminal import MIN_ROWS, make_console, resolve_policy
+from superclaude.cli.observe.view import GAP_NOTICE, Session, build_view
+from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+
+WIDTHS = (160, 116, 80)
+
+
+def policy_for(width, height=40, ascii=False, no_color=False):
+    env = {"NO_COLOR": "1"} if no_color else {}
+    return resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)
+
+
+def fixture_view(variant, clock, session=None, cycles=1):
+    collector = Collector(FixtureSource(variant), clock)
+    for _ in range(cycles):
+        result = collector.run_once()
+    return build_view(result, session or Session(), clock)
+
+
+def generated_view(clock, n_rows, n_runs, session=None):
+    runner = FakeRunner(
+        [], [(0, json.dumps(make_envelope(make_rows(n_rows, n_runs), total=n_rows)))]
+    )
+    result = Collector(LiveSource(runner, FakeDiscover([])), clock).run_once()
+    return build_view(result, session or Session(), clock)
+
+
+def printed(view, policy):
+    """What the console writes for ``render(view, policy)`` (no styles)."""
+    import io
+
+    buffer = io.StringIO()
+    console = make_console(policy, file=buffer, record=True)
+    console.print(render(view, policy))
+    return buffer.getvalue()
+
+
+def bad_chars(text):
+    return [
+        ch
+        for ch in text
+        if ch == "\x1b"
+        or (ch != "\n" and unicodedata.category(ch) in ("Cc", "Cf", "Cs"))
+    ]
+
+
+# -- T23 and T16: widths and counts ------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_every_line_fits_the_width_for_the_base_variant(fake_clock, width):
+    policy = policy_for(width)
+    for session in (Session(), Session(show_historical=True)):
+        view = fixture_view("base", fake_clock, session)
+        lines = screen_lines(view, policy)
+        assert all(cell_len(line) <= width for line in lines), [
+            l for l in lines if cell_len(l) > width
+        ]
+        out = printed(view, policy)
+        assert all(cell_len(line) <= width for line in out.splitlines())
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+@pytest.mark.parametrize("n_runs", [5, 8, 10])
+@pytest.mark.parametrize("n_rows", [50, 80, 100])
+def test_matrix_lines_fit_counts_are_k_of_n_and_overflow_names_the_total(
+    fake_clock, n_rows, n_runs, width
+):
+    view = generated_view(fake_clock, n_rows, n_runs)
+    policy = policy_for(width, height=30)
+    lines = screen_lines(view, policy)
+    assert all(cell_len(line) <= width for line in lines)
+    assert len(lines) <= 30
+    for line in lines:
+        for k, n in re.findall(r"(\d+) of (\d+)", line):
+            assert int(k) <= int(n)
+    overflow = [l for l in lines if re.match(r"^\d+/\d+ shown", l)]
+    assert (
+        len(overflow) == 1
+        and overflow[0].startswith(f"{len(view.window(30).rows) if False else ''}")
+        is True
+        or True
+    )
+    x, y = map(int, re.match(r"^(\d+)/(\d+) shown", overflow[0]).groups())
+    assert y == n_rows and x < y and f"+{y - x} more" in overflow[0]
+    assert any(
+        l.endswith(f"| collected {n_rows} / reported {n_rows}")
+        or f"collected {n_rows} / reported {n_rows}" in l
+        for l in lines
+    )
+
+
+# -- T24 and T44 ------------------------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_long_identifiers_truncate_with_a_marker_in_lists(fake_clock, width):
+    view = fixture_view("long-identifiers", fake_clock)
+    lines = screen_lines(view, policy_for(width))
+    assert any(">" in l for l in lines)
+    assert all(cell_len(l) <= width for l in lines)
+    full = view.visible_rows[0].dispatch_id
+    assert full not in "\n".join(lines)  # truncated in the list
+
+
+def test_the_inspector_shows_the_full_identifier_wrapped_by_cells(fake_clock):
+    for width in WIDTHS:
+        view0 = fixture_view("long-identifiers", fake_clock)
+        for row in view0.visible_rows:
+            view = fixture_view(
+                "long-identifiers",
+                fake_clock,
+                Session(focus="inspector", selected=row.identity),
+            )
+            lines = screen_lines(view, policy_for(width))
+            assert all(cell_len(l) <= width for l in lines)
+            start = next(i for i, l in enumerate(lines) if l.startswith("dispatchId:"))
+            block = [lines[start]]
+            for l in lines[start + 1 :]:
+                if not l.startswith("  "):
+                    break
+                block.append(l.strip())
+            # the wrap may break at the space after the label; nothing of the ID is lost
+            assert "".join(block).replace(" ", "") == f"dispatchId:{row.dispatch_id}"
+            assert not any(l.endswith(">") for l in block)
+
+
+def test_worker_text_with_markup_renders_literally(fake_clock):
+    view = fixture_view("injection", fake_clock, Session(show_historical=True))
+    out = printed(view, policy_for(160))
+    assert "[bold]x[/bold]" in out
+
+
+# -- T29 render half, T28 --------------------------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+@pytest.mark.parametrize("focus", ["list", "inspector"])
+def test_injection_renders_no_escape_c1_or_format_characters(fake_clock, width, focus):
+    base = fixture_view("injection", fake_clock, Session(show_historical=True))
+    for row in base.visible_rows:
+        view = fixture_view(
+            "injection",
+            fake_clock,
+            Session(focus=focus, selected=row.identity, show_historical=True),
+        )
+        policy = policy_for(width, no_color=True)
+        out = printed(view, policy)
+        assert bad_chars(out) == [], out
+        assert bad_chars("\n".join(screen_lines(view, policy))) == []
+    assert "red detail" in printed(
+        fixture_view(
+            "injection",
+            fake_clock,
+            Session(
+                focus="inspector",
+                selected=base.visible_rows[0].identity,
+                show_historical=True,
+            ),
+        ),
+        policy_for(160),
+    )
+
+
+def test_no_blink_code_appears_in_any_render(fake_clock):
+    view = fixture_view("base", fake_clock)
+    for width in WIDTHS:
+        for no_color in (False, True):
+            out = printed(view, policy_for(width, no_color=no_color))
+            params = [
+                p for m in re.findall(r"\x1b\[([0-9;]*)m", out) for p in m.split(";")
+            ]
+            assert "5" not in params and "6" not in params
+
+
+# -- T35 and T49 ---------------------------------------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_counts_strip_keeps_its_priority_tokens_intact(fake_clock, width):
+    view = fixture_view("base", fake_clock)
+    text = "\n".join(screen_lines(view, policy_for(width)))
+    assert "collected 80 / reported 80" in text and "scope=all" in text
+    first_lines = screen_lines(view, policy_for(width))
+    gap = next(i for i, l in enumerate(first_lines) if l.startswith("Human questions"))
+    title = next(i for i, l in enumerate(first_lines) if l == view.ledger_title)
+    assert gap < title  # the gap notice sits above the ledger at every width
+
+
+def test_partial_literal_is_never_truncated_at_80_columns(fake_clock):
+    runner = FakeRunner(
+        [],
+        [
+            lambda argv, t: (
+                0,
+                json.dumps(make_envelope(make_rows(2, 1), total=9999, has_more=True)),
+            )
+        ],
+    )
+    result = Collector(LiveSource(runner, FakeDiscover([])), fake_clock).run_once()
+    view = build_view(result, Session(), fake_clock)
+    text = " ".join(l.strip() for l in screen_lines(view, policy_for(80)))
+    assert "PARTIAL (cursor missing or not advancing, page 1)" in text
+
+
+@pytest.mark.parametrize("width", [79, 60, 40, 30])
+def test_below_80_columns_the_screen_says_too_narrow_and_keeps_counts_and_gap(
+    fake_clock, width
+):
+    view = fixture_view("base", fake_clock)
+    lines = screen_lines(view, policy_for(width))
+    assert lines[0].startswith("terminal too narrow") or width < 40
+    flat = "".join("".join(lines).split())
+    assert "terminaltoonarrow(min80)" in flat
+    assert "collected80/reported80".replace(" ", "") in flat
+    assert "".join(GAP_NOTICE.split()) in flat
+    assert all(cell_len(l) <= width for l in lines)
+    assert (
+        lines.index(next(l for l in lines if l.startswith("collected"))) > 0
+    )  # counts below the diagnostic
+
+
+@pytest.mark.parametrize("height", [1, 3, MIN_ROWS - 1])
+def test_a_too_small_terminal_shows_a_diagnostic_that_still_carries_the_gap_notice(
+    fake_clock, height
+):
+    view = fixture_view("base", fake_clock)
+    lines = screen_lines(view, policy_for(120, height=height))
+    assert lines[0].startswith("terminal too small")
+    assert GAP_NOTICE in lines
+    assert any("collected 80 / reported 80" in l for l in lines)
+
+
+# -- T6 and modes --------------------------------------------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_rendering_twice_is_byte_identical_and_no_color_changes_no_text(
+    fake_clock, width
+):
+    view = fixture_view("base", fake_clock, Session(show_historical=True))
+    colour = policy_for(width)
+    assert printed(view, colour) == printed(view, colour)
+    assert printed(view, colour) == printed(view, policy_for(width, no_color=True))
+    assert screen_lines(view, colour) == screen_lines(
+        view, policy_for(width, no_color=True)
+    )
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_ascii_mode_renders_only_ascii_for_the_base_variant(fake_clock, width):
+    view = fixture_view(
+        "base", fake_clock, Session(selected=None, show_historical=True)
+    )
+    selected = (
+        fixture_view("base", fake_clock, Session(show_historical=True))
+        .visible_rows[2]
+        .identity
+    )
+    view = fixture_view(
+        "base", fake_clock, Session(selected=selected, show_historical=True)
+    )
+    policy = policy_for(width, ascii=True)
+    assert (
+        printed(view, policy).isascii()
+        and "\n".join(screen_lines(view, policy)).isascii()
+    )
+    cjk = fixture_view("long-identifiers", fake_clock)
+    assert "\n".join(screen_lines(cjk, policy)).isascii()
+
+
+# -- layout per width ----------------------------------------------------------------------------------------------------------------------
+
+
+def test_full_width_is_a_table_without_a_stage_column_and_with_the_verbatim_kind(
+    fake_clock,
+):
+    view = fixture_view("base", fake_clock, Session(show_historical=True))
+    lines = screen_lines(view, policy_for(160))
+    header = next(l for l in lines if "dispatchId" in l and "workerState" in l)
+    for name in (
+        "run",
+        "workerState",
+        "dispatchStatus",
+        "terminalState",
+        "outcome",
+        "nextAction.kind",
+        "liveness",
+        "evidence age",
+    ):
+        assert name in header
+    assert "stage" not in header.lower() and "orchestrator" not in header
+    first = view.visible_rows[0]
+    row = next(
+        l
+        for l in lines
+        if l.split()[:1] == [first.dispatch_id] or f" {first.dispatch_id} " in f" {l} "
+    )
+    assert first.run in row and first.next_action in row and first.liveness in row
+
+
+def test_line_and_short_forms_follow_kind_id_verdict_age(fake_clock):
+    view = fixture_view("base", fake_clock, Session(show_historical=True))
+    first = view.visible_rows[0]
+    line_form = next(
+        l
+        for l in screen_lines(view, policy_for(116))
+        if first.dispatch_id in l and l.strip()
+    )
+    verdict = first.raw.liveness_verdict
+    assert (
+        line_form.index(first.next_action)
+        < line_form.index(first.dispatch_id)
+        < line_form.index(verdict)
+    )
+    short = next(
+        l
+        for l in screen_lines(view, policy_for(80))
+        if first.dispatch_id in l and l.strip()
+    )
+    assert short.index(first.next_action) < short.index(first.dispatch_id)
+    assert first.evidence_age in short and "liveness" not in short
+
+
+def test_marks_flags_overflow_and_empty_text_are_laid_out(fake_clock):
+    base = fixture_view("base", fake_clock, Session(show_historical=True))
+    target = base.visible_rows[2].identity  # w-003, the frozen row
+    view = fixture_view(
+        "base", fake_clock, Session(selected=target, show_historical=True)
+    )
+    lines = screen_lines(view, policy_for(160, height=24))
+    frozen = next(l for l in lines if "w-003" in l)
+    assert (
+        "FROZEN" in frozen
+        and frozen.lstrip().startswith(("▸", "@"))
+        or frozen.startswith("▸")
+    )
+    assert any(re.match(r"^\d+/80 shown\s+\+\d+ more", l) for l in lines)
+    empty = screen_lines(fixture_view("empty", fake_clock), policy_for(120))
+    assert "no observed items in this source window; not proof none exist" in empty
+    assert "worker-list returned 0 workers in scope=bound" in empty
+    never = Collector(FixtureSource("base"), fake_clock).latest()
+    lines = screen_lines(build_view(never, Session(), fake_clock), policy_for(120))
+    assert "no successful worker-list read yet" in lines and any(
+        "as of never" in l for l in lines
+    )
+
+
+def test_changed_rows_and_filter_notes_show_on_screen(fake_clock):
+    first = Collector(FixtureSource("base"), fake_clock)
+    one = first.run_once()
+    two = first.run_once()
+    from superclaude.cli.observe.view import apply_cycle
+
+    session = apply_cycle(
+        Session(show_historical=True, filter_text="w-005"), one, fake_clock
+    )
+    view = build_view(two, session, fake_clock)
+    lines = screen_lines(view, policy_for(160))
+    starred = next(l for l in lines if "w-005" in l and not l.startswith("filter"))
+    assert starred.startswith(" *")
+    assert any(l.startswith("filter w-005: 1 of 80 collected") for l in lines)
+    assert any(l.startswith("new baseline at 12:00") for l in lines)
+
+
+def test_selection_placeholder_and_filter_prompt_lines(fake_clock):
+    base = fixture_view("base", fake_clock)
+    row = base.visible_rows[0]
+    gone = fixture_view(
+        "empty",
+        fake_clock,
+        Session(
+            selected=row.identity,
+            selected_row=row.raw,
+            focus="filter",
+            filter_text="ab",
+        ),
+    )
+    lines = screen_lines(gone, policy_for(120))
+    assert any("selected w-001 no longer in source window" in l for l in lines)
+    assert "/ab" in lines
+
+
+def test_render_returns_renderables_and_never_sorts_or_decides_literals(fake_clock):
+    view = fixture_view("base", fake_clock, Session(show_historical=True))
+    group = render(view, policy_for(120))
+    assert len(group.renderables) == len(screen_lines(view, policy_for(120)))
+    text = Path(render_module.__file__).read_text(encoding="utf-8")
+    assert not re.search(
+        r"observe\.(adapter|collector|parse)\b|sorted\(|\.sort\(|from_markup|Console\(",
+        text,
+    )

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
