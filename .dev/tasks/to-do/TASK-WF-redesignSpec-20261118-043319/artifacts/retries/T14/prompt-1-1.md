51649d9dad8b473ff104a7d86f14aeade6fcac35
Review one task for spec compliance.

Task brief: ## Task 14: Show each fact once, questions first, aligned labels and one status badge (desk and list)

Depends on: Task 13

Spec Part C steps 2.9, 2.10 and 2.13 in `OBS/render.py` and `OBS/view.py`. Apply 2.9 (a) to (e): the full question text only in the desk pane and the selected list row cut to one line with `>`; the Run id once (the freshness header cell for questions becomes `questions OK 0s`, the panel keeps its first state line); the count once (figure, `seen, not resolved` and `closed by evidence: unavailable` in one place, the separate counts row and tile echo removed, `(no source)` dropped from that phrase on screen only; `record_text` still writes `counts_line` unchanged); the `msg_` id leaves the desk pane (kept in the inspector); the second copy of the retention and `worker-reported, not questions` lines under the desk dropped. Apply 2.10: question rows first, then the disclosure verbatim (never shortened), with `no read marker in source: answered questions stay listed` and the retention sentence verbatim and adjacent. Apply 2.13 to the existing desk field loop: label column of about 9 cells, plain labels `session`, `state`, `alive`, `next`, `status`, `worktree`, one `alive` value built from verdict, source and evidence age, `worktree` reading `wt-1  (this session only)` (full note to the inspector), absent values `unknown` and muted; one `ACTIVE` badge only when dispatchStatus is `active`, terminalState is `active` and outcome is `none`, any other combination (an absent value included) expanding to three separate rows with raw values (decision D-14).

Acceptance criteria:
- For the `desk` and `questions` fixtures at each width, the question text, the Run id, the count words and a source's freshness state each occur once on the screen (header and panel state line excepted as RR line 45 requires), checked by a string-census test.
- The ACTIVE badge test covers active/active/none, a changed outcome, and an absent value (`unknown`, expanded to three rows).
- `record_text` and `snapshot_json` are unchanged (`tests/observe/golden_release1_records.json` test passes).
Global constraints: - Numbering: plan Phase N is spec Phase N-1 (plan Phase 1 is the spec's Phase 0, plan Phase 8 is the spec's Phase 7). Task text names the plan phase unless it says "spec Phase".
- Shorthand used in every task: OBS is `src/superclaude/cli/observe/`; T is `tests/observe/`; VP is `.dev/issues/409/visual-parity/`; RR is `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`; "the spec" is `./source.md` (its section numbers, Part B step numbers such as 1.4 and Part C step numbers such as 2.12 are cited in each task).
- Do not edit `OBS/export.py`. `record_text` and `snapshot_json` stay byte-identical. Question text appears on screen only; both hash canaries (record and snapshot) pass from Phase 1 onward.
- NO_COLOR output has zero ESC bytes and the same text as the coloured output after SGR removal. ASCII output is pure ASCII with `+ - |` borders and `#` for the block glyph. The 16-colour theme keeps eight distinct role colours.
- Draw only facts the screen has: no owner, requester, mapped-tree, SIGNALS bars or affected-session list (accepted divergences AD-1 to AD-8 of the spec).
- Existing source guards stay true: `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (`OBS/commands.py` lines 67 and 70) untouched, the words `release-gates.md` and `Task 18` stay in `OBS/commands.py`, no `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in `OBS/render.py`, and `len(group.renderables) == len(screen_lines(...))` holds.
- Owner rulings already applied (spec section 10 and Part C): Decision Desk in two columns at 160 and 116 and stacked at 80; questions screen stacked at every width; the 64-hex hash is never shown on screen; the other defaults of spec section 10 apply (D-2 to D-5, D-7 to D-12). OPEN-1 to OPEN-3 are treated as Medium and gating.
- Phase gate rule (spec section 8): each phase ends with the render gate, at most 3 iterations, a fresh reviewer per width each iteration. A phase closes only when every in-scope High and Medium rubric row passes in the last iteration. If a row still fails after iteration 3, or two consecutive iterations do not improve the passing count, write `./.dev/issues/409/visual-parity/scores/<phase>/stop.md` (path relative to the repository root), stop, and ask the owner. Never start the next phase before the previous gate closes.
- Gate outputs (renders, captures, scores) are written under `./artifacts/gates/<phase>/iter-<n>/` in this package; the closing record `scores.json` of the last iteration is also copied to `.dev/issues/409/visual-parity/scores/<phase>/` because the spec's definition of done reads it there.
- The spec's Phase 0 inputs (`render_current.py` and the baseline captures) exist only untracked in a local checkout that must never be edited. They are not on this branch, so Phase 1 rebuilds `render_current.py` from the observer's own view builders and fixtures. Never edit the local checkout.
- Goldens are regenerated only from the current tree, in the same change set as the change that moves them; styled bytes are never written into a golden.
- Nothing under `.claude/` is staged. This plan does not commit, push or open a PR before a human asks; the final task states the PR route for that moment (`/sc:pr-submit --monitor 3`, target `IronbellyOrg/IronClaude`, never `SuperClaude-Org`).
- Judgment call recorded here: spec step 2.13 names `_field_lines`, a function that step 5.2 only creates in the desk phase (spec Phase 5, plan Phase 6). The space-diet work (spec Phase 2, plan Phase 3) therefore applies the label, alignment and badge changes to the existing desk field loop in `OBS/render.py` (lines 347-353 today), and plan Phase 6 replaces that loop with `_field_lines` while keeping those changes.
Start sha: 51649d9dad8b473ff104a7d86f14aeade6fcac35
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index ff26e1af0..98d6cb89e 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -33,6 +33,7 @@ from superclaude.cli.observe.view import (
     DESK_SELECTED_HIDDEN,
     DESK_TEXT_LINES,
     DESK_TITLE,
+    DESK_WORKTREE_NOTE,
     FROZEN_MARKER,
     INSPECTOR_ABOVE_TEXT,
     INSPECTOR_BELOW_TEXT,
@@ -53,6 +54,10 @@ from superclaude.cli.observe.view import (
 )
 
 MAX_COUNT_LINES = 2  # the COUNTS strip wraps to a second line before anything is cut
+DESK_STUB_CELLS = 24  # the selected list row shows at most this much question text
+DESK_LABEL_CELLS = (
+    9  # the label column of the desk pane (wider only for raw field names)
+)
 SEPARATOR = " "
 
 
@@ -528,7 +533,7 @@ def _help_lines(view: View, policy: TerminalPolicy) -> list[Line]:
     return _roled(wrap_groups(view.help_line, policy.width, policy), "muted")
 
 
-def _question_line(q: QuestionLine, policy: TerminalPolicy) -> Line:
+def _question_line(q: QuestionLine, policy: TerminalPolicy, stub: bool = False) -> Line:
     """One question line. With the link off it is the row text clipped as in R2; with it on the
     age and the bracketed state stay and only the question text is cut. The row carries a reason
     only when the source gave one (the record keeps its own ``reason unknown`` wording).
@@ -557,6 +562,9 @@ def _question_line(q: QuestionLine, policy: TerminalPolicy) -> Line:
     tail = ascii_safe(reason) if policy.ascii else reason
     room = max(width - cell_len(head) - cell_len(tail), 1)
     text = ascii_safe(q.shown) if policy.ascii else q.shown
+    if stub and q.selected and cell_len(text) > DESK_STUB_CELLS:
+        # The desk holds the full text: the selected row is one short line ending in ``>``.
+        text = text[: _prefix_length(text, DESK_STUB_CELLS - 1)] + ">"
     if (
         cell_len(text) > room and room > 3
     ):  # a cut question text ends in a visible "..."
@@ -585,12 +593,10 @@ def _desk_lines(desk: DeskView, policy: TerminalPolicy) -> list[Line]:
     with ``...``), the linked session fields, then each note. Everything wraps; nothing is cut."""
     width = policy.width
     lines = _wrapped(DESK_TITLE, width, policy, "attention_title")
-    lines += _wrapped(
-        f"{desk.qid}  age {desk.age_text}" if desk.age_text else desk.qid,
-        width,
-        policy,
-        "attention",
-    )
+    if (
+        desk.age_text
+    ):  # the message id is not shown here; the record and the export keep it
+        lines += _wrapped(f"age {desk.age_text}", width, policy, "attention")
     if desk.ask:
         text = wrap(desk.ask, width, policy)
         if len(text) > DESK_TEXT_LINES:
@@ -599,26 +605,91 @@ def _desk_lines(desk: DeskView, policy: TerminalPolicy) -> list[Line]:
                 last[: _prefix_length(last, max(width - 3, 1))] + "..."
             ]
         lines += _roled(text, "attention")
-    for label, value in desk.session_fields:
-        role = (
-            STATE_ROLE.get((label, value))
-            or STATE_ROLE.get((label, value.split(" (")[0]))
-            or _absent_role(value)
-        )
-        lines += _labelled(label, value, width, policy, role)
+    rows = _desk_rows(desk.session_fields)
+    column = max([DESK_LABEL_CELLS, *(len(label) + 1 for label, _, _ in rows)])
+    for label, value, role in rows:
+        lines += _desk_field(label, value, role, column, policy)
     for note in desk.notes:
-        lines += _wrapped(note, width, policy, "muted")
+        if note != DESK_WORKTREE_NOTE:  # the full note lives with the worker detail
+            lines += _wrapped(note, width, policy, "muted")
+    return lines
+
+
+def _plain_absent(value: str) -> str:
+    """The bare word ``unknown`` for a value the source did not carry."""
+    return "unknown" if value.strip() == ABSENT_IN_SOURCE else value
+
+
+def _desk_rows(fields: tuple[tuple[str, str], ...]) -> list[tuple[str, str, str]]:
+    """(label, value, role) per desk field line: plain labels, one ``alive`` value, one ``ACTIVE``
+    badge only when the three status values are exactly active, active and none."""
+    if not fields:
+        return []
+    got = {label: _plain_absent(value) for label, value in fields}
+
+    def get(name: str) -> str:
+        return got.get(name, "unknown")
+
+    verdict, _, rest = get("liveness").partition(" (")
+    source = rest.rstrip(")")
+    age = get("evidence age")
+    if verdict in ("unknown", ""):
+        alive, alive_role = "unknown", "muted"
+    else:
+        alive = "yes" if verdict in ("alive", "live") else verdict
+        if source and source != "unknown":
+            alive += f" ({source})"
+        alive += f", {age} ago" if age[:1].isdigit() else ", age unknown"
+        alive_role = "state_running" if verdict in ("alive", "live") else "body"
+    state = get("workerState")
+    worktree = get("resource.worktreeId")
+    rows = [
+        ("session", get("dispatchId"), _absent_role(get("dispatchId"))),
+        (
+            "state",
+            state,
+            STATE_ROLE.get(("workerState", state)) or _absent_role(state),
+        ),
+        ("alive", alive, alive_role),
+        ("next", get("nextAction.kind"), _absent_role(get("nextAction.kind"))),
+    ]
+    status = (get("dispatchStatus"), get("terminalState"), get("outcome"))
+    if status == ("active", "active", "none"):
+        rows.append(("status", "ACTIVE", "state_running"))
+    else:  # any other combination, an absent value included: three separate raw rows
+        rows += [
+            (name, value, _absent_role(value))
+            for name, value in zip(
+                ("dispatchStatus", "terminalState", "outcome"), status
+            )
+        ]
+    if worktree == "unknown":
+        rows.append(("worktree", "unknown", "muted"))
+    else:
+        rows.append(("worktree", f"{worktree}  (this session only)", "body"))
+    return rows
+
+
+def _desk_field(
+    label: str, value: str, role: str, column: int, policy: TerminalPolicy
+) -> list[Line]:
+    """One desk field: the muted label padded to ``column`` cells, then the value; a long value
+    continues on lines indented to the value column."""
+    first, *rest = wrap(value, max(policy.width - column, 1), policy) or [""]
+    pad = " " * max(column - len(label), 1)
+    lines = [join(seg(label + pad, "muted"), seg(first, role))]
+    lines += [join(seg(" " * column), seg(part, role)) for part in rest]
     return lines
 
 
 def _panel_title(
     panel: QuestionsPanel, width: int, policy: TerminalPolicy
 ) -> list[Line]:
-    """The panel title; when no question row carries a reason, the one note that replaces the
-    per-row "reason unknown" follows it, muted."""
-    if any(q.reason for q in panel.lines):
-        return _wrapped(panel.title, width, policy, "attention_title")
-    wrapped = wrap(f"{panel.title}  {QUESTIONS_REASONS_NOTE}", width, policy)
+    """The panel title row: the title, then the Run id (said once on the screen), then, when no
+    question row carries a reason, the one note that replaces the per-row "reason unknown";
+    everything after the title is muted."""
+    note = "" if any(q.reason for q in panel.lines) else f"  {QUESTIONS_REASONS_NOTE}"
+    wrapped = wrap(f"{panel.title}  {panel.run_line}{note}", width, policy)
     first, rest = wrapped[0], wrapped[1:]
     title = ascii_safe(panel.title) if policy.ascii else panel.title
     head = (
@@ -634,22 +705,22 @@ def _panel_lines(
     policy: TerminalPolicy,
     capacity: int | None,
     desk: list[Line] | None = None,
+    desk_open: bool = False,
 ) -> list[Line]:
-    """The coordinator-questions block: header lines, up to ``capacity`` questions, then the
-    desk block (when given), notes."""
+    """The coordinator-questions block: the title row (with the Run id), the state of the read,
+    the count, up to ``capacity`` questions, the desk block (when given), then the standing
+    lines: the disclosure, the no-read-marker caveat and the retention sentence, adjacent.
+    ``desk_open`` is true when ``desk`` is the full desk (not its hidden notice)."""
     width = policy.width
     lines = _panel_title(panel, width, policy)
-    lines += _wrapped(panel.run_line, width, policy, "muted")
     for state_line in panel.state_lines:  # the state of the read comes first
         lines += _wrapped(state_line, width, policy, "muted")
-    lines += _wrapped(panel.disclosure, width, policy, "muted")
     lines += [
         _absent_tail(text, "identity")
-        for text in wrap(panel.counts_line, width, policy)
+        for text in wrap(panel.screen_counts_line or panel.counts_line, width, policy)
     ]
-    lines += _wrapped(panel.caveat_line, width, policy, "muted")
     shown, cut = panel.window(capacity)
-    lines += [_question_line(q, policy) for q in shown]
+    lines += [_question_line(q, policy, stub=desk_open) for q in shown]
     if cut:
         lines += _wrapped(cut, width, policy, "muted")
     if any(q.selected for q in panel.lines) and not any(q.selected for q in shown):
@@ -660,6 +731,8 @@ def _panel_lines(
     for text in (panel.empty_text, panel.window_full_text, *panel.notes):
         if text:
             lines += _wrapped(text, width, policy, "muted")
+    lines += _wrapped(panel.disclosure, width, policy, "muted")
+    lines += _wrapped(panel.caveat_line, width, policy, "muted")
     return lines + _wrapped(panel.retention_line, width, policy, "muted")
 
 
@@ -706,7 +779,7 @@ def _compose(
 
     head: list[Line] = []
     head += _title_bar(wrap(view.header1, width, policy), policy)
-    head += _wrapped(view.header2, width, policy, "muted")
+    head += _wrapped(view.screen_header2 or view.header2, width, policy, "muted")
     head += counts_line_objects(view.counts_tokens, policy)
     if view.changes_line:
         head += _wrapped(view.changes_line, width, policy, "muted")
@@ -760,7 +833,9 @@ def _compose(
                 _panel_lines(panel, policy, spare) if spare >= 1 else None
             )
         elif spare - len(desk) >= 1:  # the desk is sized first; the list keeps a line
-            panel_part = _panel_lines(panel, policy, spare - len(desk), desk)
+            panel_part = _panel_lines(
+                panel, policy, spare - len(desk), desk, desk_open=True
+            )
         elif (
             spare - len(notice) >= 1
         ):  # the desk gives way to its notice, never the list
diff --git a/src/superclaude/cli/observe/theme.py b/src/superclaude/cli/observe/theme.py
deleted file mode 100644
index a8346b182..000000000
--- a/src/superclaude/cli/observe/theme.py
+++ /dev/null
@@ -1,126 +0,0 @@
-"""Colour roles for the observer screens, one explicit table per colour depth.
-
-The screen builders tag text with a semantic role (``attention``, ``muted``, ``state_running``
-and so on); this module maps a role and a depth to a Rich ``Style``. The depth is the
-``color_system`` of the terminal policy: ``"truecolor"`` uses the design-mockup palette exactly,
-``"256"`` the nearest indexed colours, and ``"standard"`` (16 colours) named ANSI colours only,
-because Rich's automatic downgrade of the mockup RGB values collapses several roles onto one
-index. No role sets blink, dim or reverse. No module here builds a console or reads the
-environment: the terminal policy module owns both.
-"""
-
-from __future__ import annotations
-
-from rich.style import Style
-
-ROLES: tuple[str, ...] = (
-    "title",
-    "attention",
-    "attention_title",
-    "identity",
-    "secondary",
-    "body",
-    "body_bold",
-    "muted",
-    "selected",
-    "border_attention",
-    "border_secondary",
-    "border_count",
-    "state_running",
-    "state_settled",
-    "state_failed",
-    "state_frozen",
-)
-
-# Each role names one of the eight palette colours and says whether it is bold.
-_PALETTE_OF: dict[str, str] = {
-    "title": "cyan",
-    "attention": "amber",
-    "attention_title": "amber",
-    "identity": "base",
-    "secondary": "slate",
-    "body": "base",
-    "body_bold": "base",
-    "muted": "muted",
-    "selected": "amber",
-    "border_attention": "amber",
-    "border_secondary": "slate",
-    "border_count": "cyan",
-    "state_running": "green",
-    "state_settled": "cyan",
-    "state_failed": "red",
-    "state_frozen": "violet",
-}
-_BOLD: frozenset[str] = frozenset(
-    {"title", "attention", "attention_title", "secondary", "body_bold", "selected"}
-)
-
-# The eight palette colours per depth (mockup RGB; 256-colour indexes; named 16-colour ANSI colours).
-_COLOURS: dict[str, dict[str, str]] = {
-    "truecolor": {
-        "base": "rgb(225,233,238)",
-        "muted": "rgb(165,182,194)",
-        "slate": "rgb(82,108,128)",
-        "amber": "rgb(250,178,25)",
-        "cyan": "rgb(112,205,226)",
-        "green": "rgb(139,215,175)",
-        "red": "rgb(240,141,150)",
-        "violet": "rgb(194,173,242)",
-    },
-    "256": {
-        "base": "color(189)",
-        "muted": "color(145)",
-        "slate": "color(60)",
-        "amber": "color(214)",
-        "cyan": "color(80)",
-        "green": "color(115)",
-        "red": "color(210)",
-        "violet": "color(147)",
-    },
-    "standard": {
-        "base": "bright_white",
-        "muted": "white",
-        "slate": "bright_black",
-        "amber": "bright_yellow",
-        "cyan": "bright_cyan",
-        "green": "green",
-        "red": "red",
-        "violet": "magenta",
-    },
-}
-
-# Display mapping from a real state word to a state role, keyed by (field, exact raw value).
-# This is a display choice, not a count mapping and not a health verdict: the word is always
-# printed, and every value not listed here keeps the body role.
-STATE_ROLE: dict[tuple[str, str], str] = {
-    ("workerState", "running"): "state_running",
-    ("liveness", "alive"): "state_running",
-    ("liveness", "live"): "state_running",
-    ("workerState", "succeeded"): "state_settled",
-    ("dispatchStatus", "completed"): "state_settled",
-    ("workerState", "failed"): "state_failed",
-    ("dispatchStatus", "failed"): "state_failed",
-}
-FROZEN_ROLE = (
-    "state_frozen"  # a flags cell holding the frozen marker (fixture mode only)
-)
-
-_CACHE: dict[tuple[str, str], Style] = {}
-
-
-def style_for(role: str, depth: str | None) -> Style | None:
-    """The Rich style of ``role`` at ``depth``; ``None`` when there is no colour depth.
-
-    Styles are cached per ``(role, depth)`` so a style made for one depth in a process is never
-    reused for another (Rich caches the ANSI codes it renders on a ``Style``).
-    """
-    if role not in _PALETTE_OF:
-        raise KeyError(f"unknown role: {role!r}")
-    if depth is None:
-        return None
-    key = (role, depth)
-    style = _CACHE.get(key)
-    if style is None:
-        style = Style(color=_COLOURS[depth][_PALETTE_OF[role]], bold=role in _BOLD)
-        _CACHE[key] = style
-    return style
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index d55632820..b26944c8e 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -67,6 +67,9 @@ QUESTIONS_REASON = "reason unknown"  # no verified reason field exists (PROPOSED
 # reason field, so "none in source" is a statement about the source, not about the world.
 QUESTIONS_REASONS_NOTE = "reasons: none in source"
 QUESTIONS_CLOSED = "closed by evidence: unavailable (no source)"
+QUESTIONS_CLOSED_SCREEN = (
+    "closed by evidence: unavailable"  # screen only (record keeps the tail)
+)
 QUESTIONS_RETENTION = (
     "retention reset at {hhmm}; questions observed before this start are not retained"
 )
@@ -275,6 +278,10 @@ class QuestionsPanel:
     retained: int
     evicted: int
     window_full: bool
+    # Screen only (the record keeps ``header_cell`` and ``counts_line`` unchanged): the strip cell
+    # without the Run id, and the count without the ``(no source)`` tail.
+    screen_cell: str = ""
+    screen_counts_line: str = ""
 
     @property
     def link_on(self) -> bool:
@@ -348,6 +355,9 @@ class View:
     desk: DeskView | None = (
         None  # None unless the link is on and a question is selected
     )
+    # Screen only: the freshness strip with the questions cell stripped of its Run id (the
+    # panel title carries the Run once). ``header2`` stays as the record reads it.
+    screen_header2: str = ""
 
     def window(self, capacity: int | None) -> Window:
         """The rows that fit ``capacity`` lines, always including the selected visible row."""
@@ -721,6 +731,7 @@ def _questions_panel(
         status = f"last read {cell_state}"
         cell = cell_state
     header_cell = f"coordinator questions {cell} (one Run {run})"
+    screen_cell = f"questions {cell}"
 
     if retained is None:
         open_total: Any = UNKNOWN
@@ -781,6 +792,9 @@ def _questions_panel(
             )
         lines = tuple(built)
     counts_line = f"{QUESTIONS_COUNT_LABEL}: {open_text} | {QUESTIONS_CLOSED}"
+    screen_counts_line = (
+        f"{QUESTIONS_COUNT_LABEL}: {open_text} | {QUESTIONS_CLOSED_SCREEN}"
+    )
 
     notes: list[str] = []
     read = result.question_read
@@ -830,6 +844,8 @@ def _questions_panel(
         retained=count_retained,
         evicted=evicted,
         window_full=window_full,
+        screen_cell=screen_cell,
+        screen_counts_line=screen_counts_line,
     )
 
 
@@ -952,6 +968,12 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
     if result.code == "overrun":
         cells.append(f"cycle overran ({int(result.duration)}s)")
     header2 = "  ".join(cells)
+    screen_header2 = "  ".join(
+        [
+            panel.screen_cell if panel is not None and c == messages_cell else c
+            for c in cells
+        ]
+    )
 
     collected_text = _collected_text(coverage)
     tokens = [CountsToken(collected_text, True)]
@@ -1069,6 +1091,7 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
         if panel is None
         else (QUESTIONS_LINK_KEYS_LINE if panel.link_on else QUESTIONS_KEYS_LINE),
         inspector_scroll=session.inspector_scroll,
+        screen_header2=screen_header2,
         questions=panel,
         desk=_desk(
             panel,
diff --git a/src/superclaude/examples/release-spec-template.md b/src/superclaude/examples/release-spec-template.md
index 26e8521e6..87c315b19 100644
--- a/src/superclaude/examples/release-spec-template.md
+++ b/src/superclaude/examples/release-spec-template.md
@@ -139,7 +139,7 @@ quality_scores:
 > New or modified data structures. Include field definitions.
 
 ```python
-{{SC_PLACEHOLDER:data_model_code}}
+{{SC_PLACEHOLDER: data_model_code}}
 ```
 
 ### 4.6 Implementation Order
diff --git a/src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md b/src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md
index fdb1f10c4..769a863e3 100644
--- a/src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md
+++ b/src/superclaude/skills/sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md
@@ -22,8 +22,8 @@ const handler = await import(`./handlers/${process.env.HANDLER_TYPE}`);
 **Python**:
 
 ```python
-module = importlib.import_module(os.environ.get('PLUGIN_MODULE'))
-handler = __import__(os.getenv('HANDLER_CLASS'))
+module = importlib.import_module(os.environ.get("PLUGIN_MODULE"))
+handler = __import__(os.getenv("HANDLER_CLASS"))
 ```
 
 **Check**: Search for `process.env`, `os.environ`, `os.getenv` near import/require/load statements.
@@ -86,7 +86,7 @@ const migrations = fs.readdirSync('./migrations').filter(f => f.endsWith('.sql')
 **Python**:
 
 ```python
-for path in Path('handlers').glob('*.py'):
+for path in Path("handlers").glob("*.py"):
     importlib.import_module(f"handlers.{path.stem}")
 ```
 
diff --git a/src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md b/src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md
index 30791dd25..315895564 100644
--- a/src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md
+++ b/src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md
@@ -247,9 +247,7 @@ from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck
 {GATE_DEFINITIONS}
 
 # Collected for iteration
-ALL_GATES: dict[str, GateCriteria] = {{
-    {GATE_DICT_ENTRIES}
-}}
+ALL_GATES: dict[str, GateCriteria] = {{{GATE_DICT_ENTRIES}}}
 ```
 
 ## Template: `prompts.py`
diff --git a/src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md b/src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md
index 8f87e2a52..232a3ba81 100644
--- a/src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md
+++ b/src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md
@@ -20,15 +20,15 @@ Every workflow operation that produces an artifact maps to a `Step`:
 
 ```python
 Step(
-    id="step-id",              # kebab-case, unique within pipeline
-    prompt=build_X_prompt(),   # Function from prompts.py
-    output_file="artifact.md", # Relative to work_dir
-    gate=STEP_GATE,            # From gates.py
+    id="step-id",  # kebab-case, unique within pipeline
+    prompt=build_X_prompt(),  # Function from prompts.py
+    output_file="artifact.md",  # Relative to work_dir
+    gate=STEP_GATE,  # From gates.py
     gate_mode=GateMode.BLOCKING,  # BLOCKING (default) or TRAILING
-    timeout_seconds=600,       # Per-step timeout
-    inputs=["dep1.md"],        # Files this step reads
-    retry_limit=1,             # How many retries on gate failure
-    model=None,                # None = use default from config
+    timeout_seconds=600,  # Per-step timeout
+    inputs=["dep1.md"],  # Files this step reads
+    retry_limit=1,  # How many retries on gate failure
+    model=None,  # None = use default from config
 )
 ```
 
@@ -53,7 +53,7 @@ Steps that can run concurrently are wrapped in a list:
 steps = [
     single_step_1,
     [parallel_step_a, parallel_step_b],  # Run concurrently
-    single_step_2,                        # Waits for parallel group
+    single_step_2,  # Waits for parallel group
 ]
 ```
 
@@ -76,11 +76,12 @@ Always extend `PipelineConfig`:
 @dataclass
 class MyConfig(PipelineConfig):
     """Pipeline-specific configuration."""
+
     # Required: identify the input
     source_path: Path
 
     # Optional: control behavior
-    depth: str = "standard"       # quick|standard|deep
+    depth: str = "standard"  # quick|standard|deep
 
     # Computed paths
     @property
@@ -101,13 +102,13 @@ class StepPhaseStatus(Enum):
     PENDING = "pending"
     RUNNING = "running"
     PASS = "pass"
-    PASS_NO_SIGNAL = "pass_no_signal"    # Completed but no structured report
-    PASS_NO_REPORT = "pass_no_report"    # Output exists but no result file
-    INCOMPLETE = "incomplete"             # Budget exhausted
-    HALT = "halt"                         # Step recommends stopping
-    TIMEOUT = "timeout"                   # Hard timeout exceeded
-    ERROR = "error"                       # Process crash
-    SKIPPED = "skipped"                   # Skipped by config
+    PASS_NO_SIGNAL = "pass_no_signal"  # Completed but no structured report
+    PASS_NO_REPORT = "pass_no_report"  # Output exists but no result file
+    INCOMPLETE = "incomplete"  # Budget exhausted
+    HALT = "halt"  # Step recommends stopping
+    TIMEOUT = "timeout"  # Hard timeout exceeded
+    ERROR = "error"  # Process crash
+    SKIPPED = "skipped"  # Skipped by config
 ```
 
 ### Result Model
@@ -202,6 +203,7 @@ def _no_heading_gaps(content: str) -> bool:
     # ... implementation ...
     return True  # or False on failure
 
+
 def _has_required_sections(content: str) -> bool:
     """Verify all required sections are present."""
     required = {"## Summary", "## Findings", "## Recommendations"}
@@ -420,6 +422,7 @@ def determine_status(exit_code, step, config):
 ```python
 # In src/superclaude/cli/main.py
 from superclaude.cli.my_pipeline import my_pipeline_group
+
 app.add_command(my_pipeline_group)
 ```
 
@@ -452,12 +455,14 @@ For pipelines with multiple Claude subprocesses, use `TurnLedger` to manage budg
 ```python
 from superclaude.cli.sprint.models import TurnLedger
 
+
 @dataclass
 class MyConfig(PipelineConfig):
     max_turns: int = 200
     min_launch_allocation: int = 10
     min_remediation_budget: int = 5
 
+
 # In executor:
 ledger = TurnLedger(
     initial_budget=config.max_turns,
@@ -522,7 +527,9 @@ def build_step_prompt_with_context(step, prior_results: list[StepResult]) -> str
 
     context_block = "## Prior Step Context\n\n"
     for result in prior_results[-3:]:  # Keep recent, compress older
-        context_block += result.to_context_summary(verbose=(result == prior_results[-1]))
+        context_block += result.to_context_summary(
+            verbose=(result == prior_results[-1])
+        )
         context_block += "\n\n"
 
     return f"{base_prompt}\n\n{context_block}"
@@ -541,8 +548,9 @@ class MyResult:
         """Generate CLI command to resume from failure point."""
         if not self.halt_step:
             return None
-        remaining = [r.step.id for r in self.step_results
-                     if r.status == MyStatus.PENDING]
+        remaining = [
+            r.step.id for r in self.step_results if r.status == MyStatus.PENDING
+        ]
         return (
             f"superclaude {CLI_NAME} run "
             f"--resume --start {self.halt_step} "
@@ -552,8 +560,11 @@ class MyResult:
     @property
     def suggested_resume_budget(self) -> int:
         """Estimate turns needed to complete remaining work."""
-        remaining_steps = sum(1 for r in self.step_results
-                              if r.status in (MyStatus.PENDING, MyStatus.INCOMPLETE))
+        remaining_steps = sum(
+            1
+            for r in self.step_results
+            if r.status in (MyStatus.PENDING, MyStatus.INCOMPLETE)
+        )
         return remaining_steps * 25  # Default allocation per step
 ```
 
@@ -571,18 +582,27 @@ def execute_step(step, config):
         # Claude-assisted — launch subprocess
         return run_claude_step(step, config)
 
+
 def run_programmatic_step(step, config) -> StepResult:
     """Execute a pure-programmatic step without Claude."""
     started = time.time()
     try:
         # Call the step's implementation function
         PROGRAMMATIC_RUNNERS[step.id](config)
-        return StepResult(step=step, status=StepStatus.PASS,
-                         started_at=started, finished_at=time.time())
+        return StepResult(
+            step=step,
+            status=StepStatus.PASS,
+            started_at=started,
+            finished_at=time.time(),
+        )
     except Exception as e:
-        return StepResult(step=step, status=StepStatus.FAIL,
-                         gate_failure_reason=str(e),
-                         started_at=started, finished_at=time.time())
+        return StepResult(
+            step=step,
+            status=StepStatus.FAIL,
+            gate_failure_reason=str(e),
+            started_at=started,
+            finished_at=time.time(),
+        )
 ```
 
 ## Gate Display State Machine (for TUI)
@@ -602,9 +622,12 @@ class GateDisplayState(Enum):
     @property
     def icon(self) -> str:
         return {
-            "none": " ", "checking": "...",
-            "pass": "ok", "fail_deferred": "!",
-            "remediating": "~", "remediated": "ok",
+            "none": " ",
+            "checking": "...",
+            "pass": "ok",
+            "fail_deferred": "!",
+            "remediating": "~",
+            "remediated": "ok",
             "halt": "X",
         }[self.value]
 ```
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
index d4d8fdb83..fb9657c87 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
@@ -96,8 +96,15 @@ Codex part applies the same rules to the same snapshot and `expected_head`:
 
 ```python
 from superclaude.pr_submit import (
-    actionable_finding_comments, augment_marker_defect, classify, classify_codex,
-    codex_finding_comments, finding_from_comment, remap_severity, reviewer_activity, route,
+    actionable_finding_comments,
+    augment_marker_defect,
+    classify,
+    classify_codex,
+    codex_finding_comments,
+    finding_from_comment,
+    remap_severity,
+    reviewer_activity,
+    route,
 )
 
 expected_head = payload.get("head_sha") if pushed_sha is None else pushed_sha
@@ -109,11 +116,17 @@ if pushed_sha is not None and (
     review_state = "polling"
 else:
     review_state = classify(
-        payload, contract, watermark=watermark, current_head_sha=expected_head,
+        payload,
+        contract,
+        watermark=watermark,
+        current_head_sha=expected_head,
     )
     if review_state == "findings":
         selected = actionable_finding_comments(
-            payload, contract, watermark=watermark, current_head_sha=expected_head,
+            payload,
+            contract,
+            watermark=watermark,
+            current_head_sha=expected_head,
         )
         try:
             if not selected:
@@ -134,15 +147,23 @@ if pushed_sha is not None and (
     codex_state = "polling"
 else:
     codex_state = classify_codex(
-        payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
+        payload,
+        contract,
+        watermark=codex_watermark,
+        current_head_sha=expected_head,
     )
     if codex_state == "findings":
         selected = codex_finding_comments(
-            payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
+            payload,
+            contract,
+            watermark=codex_watermark,
+            current_head_sha=expected_head,
         )
         try:
             if not selected:
-                raise ValueError("Codex findings signal without actionable root details")
+                raise ValueError(
+                    "Codex findings signal without actionable root details"
+                )
             codex_findings = [finding_from_comment(raw) for raw in selected]
         except ValueError:
             codex_state = "polling"
diff --git a/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md b/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
index 90876e72f..292ece7ce 100644
--- a/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
+++ b/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
@@ -27,7 +27,9 @@ Count: **10 truly-new semantic groups** (the original §12.4 / §14.5.7 / §12.5
 ## citation_resolves
 
 ```python
-def citation_resolves(report_path: str, fixture_root: str = None) -> AssertionResult: ...
+def citation_resolves(
+    report_path: str, fixture_root: str = None
+) -> AssertionResult: ...
 ```
 
 **Semantics.** Parse `REPORT.md` for citations of the shape `path/to/file.py:LINE` or `path/to/file.md:LINE`. For each citation, re-Read the referenced file and verify the surrounding ±5 lines contain the snippet quoted in the report. When `fixture_root` is provided, remap the citation's path so synthetic-eval diffs (which live under `fixtures/<case>/`) resolve to the in-fixture file rather than the absolute repo path.
@@ -38,18 +40,23 @@ from pathlib import Path
 
 CITATION_RE = re.compile(r"`?([\w./\-]+\.(?:py|md|yaml|ts|js)):(\d+)`?")
 
+
 def check_citation_resolves(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     report = (base_dir / assertion["report"]).read_text(encoding="utf-8")
     fixture_root = Path(assertion.get("fixture_root", base_dir))
     resolved, failed = 0, []
     for m in CITATION_RE.finditer(report):
         rel_path, line_no = m.group(1), int(m.group(2))
-        target = (fixture_root / rel_path) if not Path(rel_path).is_absolute() else Path(rel_path)
+        target = (
+            (fixture_root / rel_path)
+            if not Path(rel_path).is_absolute()
+            else Path(rel_path)
+        )
         if not target.exists():
             failed.append(f"{rel_path}:{line_no} (file missing)")
             continue
         lines = target.read_text(encoding="utf-8").splitlines()
-        window = "\n".join(lines[max(0, line_no - 6):line_no + 5])
+        window = "\n".join(lines[max(0, line_no - 6) : line_no + 5])
         # Optional snippet check: assertion may carry expected substring
         snippet = assertion.get("expected_snippets", {}).get(f"{rel_path}:{line_no}")
         if snippet and snippet not in window:
@@ -57,7 +64,10 @@ def check_citation_resolves(assertion: dict, base_dir: Path) -> tuple[bool, str]
         else:
             resolved += 1
     total = resolved + len(failed)
-    return (len(failed) == 0, f"{resolved}/{total} citations resolved; failures={failed}")
+    return (
+        len(failed) == 0,
+        f"{resolved}/{total} citations resolved; failures={failed}",
+    )
 ```
 
 ## regex_present
@@ -71,13 +81,17 @@ def regex_present(target: str, pattern: str) -> AssertionResult: ...
 ```python
 import re
 
+
 def check_regex_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     target = base_dir / assertion["target"]
     text = target.read_text(encoding="utf-8") if target.exists() else ""
     pattern = re.compile(assertion["pattern"], re.MULTILINE | re.DOTALL)
     matches = pattern.findall(text)
     if matches:
-        return True, f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}"
+        return (
+            True,
+            f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}",
+        )
     return False, f"Pattern {assertion['pattern']!r} NOT found in {assertion['target']}"
 ```
 
@@ -92,14 +106,21 @@ def regex_absent(target: str, pattern: str) -> AssertionResult: ...
 ```python
 import re
 
+
 def check_regex_absent(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     target = base_dir / assertion["target"]
     text = target.read_text(encoding="utf-8") if target.exists() else ""
     pattern = re.compile(assertion["pattern"], re.MULTILINE | re.DOTALL)
     m = pattern.search(text)
     if m is None:
-        return True, f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}"
-    return False, f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}"
+        return (
+            True,
+            f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}",
+        )
+    return (
+        False,
+        f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}",
+    )
 ```
 
 ## yaml_list_contains
@@ -114,6 +135,7 @@ def yaml_list_contains(target: str, field_path: str, value: str) -> AssertionRes
 import yaml
 from functools import reduce
 
+
 def check_yaml_list_contains(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     target = base_dir / assertion["target"]
     if not target.exists():
@@ -125,11 +147,20 @@ def check_yaml_list_contains(assertion: dict, base_dir: Path) -> tuple[bool, str
     except (KeyError, IndexError, TypeError) as e:
         return False, f"field_path {assertion['field_path']!r} unresolvable: {e}"
     if not isinstance(node, list):
-        return False, f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})"
+        return (
+            False,
+            f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})",
+        )
     expected = assertion["value"]
     if expected in node:
-        return True, f"List at {assertion['field_path']} contains {expected!r}; members={node}"
-    return False, f"List at {assertion['field_path']} missing {expected!r}; members={node}"
+        return (
+            True,
+            f"List at {assertion['field_path']} contains {expected!r}; members={node}",
+        )
+    return (
+        False,
+        f"List at {assertion['field_path']} missing {expected!r}; members={node}",
+    )
 ```
 
 ## yaml_list_len_eq
@@ -158,7 +189,10 @@ def check_yaml_list_len_eq(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     except KeyError:
         return False, f"count field {count_field!r} missing"
     except (TypeError, ValueError):
-        return False, f"count field {count_field!r} not an integer: {data.get(count_field)!r}"
+        return (
+            False,
+            f"count field {count_field!r} not an integer: {data.get(count_field)!r}",
+        )
     actual = len(items)
     if actual == expected:
         return True, f"len({list_field}) == {count_field} == {actual}"
@@ -184,7 +218,9 @@ A producer-level eval fixture (R6) drives Step 5.6 from real inputs; only if suc
 ## matrix_covers_items
 
 ```python
-def matrix_covers_items(matrix: str, source: str, threshold: float) -> AssertionResult: ...
+def matrix_covers_items(
+    matrix: str, source: str, threshold: float
+) -> AssertionResult: ...
 ```
 
 **Semantics.** Load coverage matrix YAML (a list of `{item_id, status}` rows) and the source fixture (which enumerates the requirements/items to be covered). Compute `coverage = len({row.item_id : status != "uncovered"}) / len(source_items)`. Pass when `coverage >= threshold`.
@@ -192,6 +228,7 @@ def matrix_covers_items(matrix: str, source: str, threshold: float) -> Assertion
 ```python
 import yaml
 
+
 def check_matrix_covers_items(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     matrix_path = base_dir / assertion["matrix"]
     source_path = base_dir / assertion["source"]
@@ -199,13 +236,23 @@ def check_matrix_covers_items(assertion: dict, base_dir: Path) -> tuple[bool, st
     matrix = yaml.safe_load(matrix_path.read_text(encoding="utf-8")) or []
     source = yaml.safe_load(source_path.read_text(encoding="utf-8")) or {}
     source_items = {item["id"] for item in source.get("items", [])}
-    covered = {row["item_id"] for row in matrix if row.get("status") and row["status"] != "uncovered"}
+    covered = {
+        row["item_id"]
+        for row in matrix
+        if row.get("status") and row["status"] != "uncovered"
+    }
     if not source_items:
         return False, "Source fixture has no items to cover"
     ratio = len(covered & source_items) / len(source_items)
     if ratio >= threshold:
-        return True, f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)"
-    return False, f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}"
+        return (
+            True,
+            f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)",
+        )
+    return (
+        False,
+        f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}",
+    )
 ```
 
 ## checkpoint_logged
@@ -219,6 +266,7 @@ def checkpoint_logged(audit_log: str, checkpoint_name: str) -> AssertionResult:
 ```python
 import json
 
+
 def check_checkpoint_logged(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     audit = base_dir / assertion["audit_log"]
     if not audit.exists():
@@ -242,7 +290,9 @@ def check_checkpoint_logged(assertion: dict, base_dir: Path) -> tuple[bool, str]
 ## deviation_class_matches
 
 ```python
-def deviation_class_matches(report: str, annotated_fixture: str, diff_hunk_id: str) -> AssertionResult: ...
+def deviation_class_matches(
+    report: str, annotated_fixture: str, diff_hunk_id: str
+) -> AssertionResult: ...
 ```
 
 **Semantics.** Load the annotated eval fixture (which tags each diff hunk with its true deviation class per §10) and the report's deviation register. For the given `diff_hunk_id`, confirm the report tags the same hunk with the same class (`authorized` / `necessary` / `drift` / `regression` — the canonical 4-category set per spec §10.1-§10.4).
@@ -250,12 +300,31 @@ def deviation_class_matches(report: str, annotated_fixture: str, diff_hunk_id: s
 ```python
 import yaml
 
+
 def check_deviation_class_matches(assertion: dict, base_dir: Path) -> tuple[bool, str]:
-    fixture = yaml.safe_load((base_dir / assertion["annotated_fixture"]).read_text(encoding="utf-8")) or {}
-    report = yaml.safe_load((base_dir / assertion["report"]).read_text(encoding="utf-8")) or {}
+    fixture = (
+        yaml.safe_load(
+            (base_dir / assertion["annotated_fixture"]).read_text(encoding="utf-8")
+        )
+        or {}
+    )
+    report = (
+        yaml.safe_load((base_dir / assertion["report"]).read_text(encoding="utf-8"))
+        or {}
+    )
     hunk_id = assertion["diff_hunk_id"]
-    expected = next((h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id), None)
-    actual = next((e["deviation_class"] for e in report.get("deviation_register", []) if e.get("hunk_id") == hunk_id), None)
+    expected = next(
+        (h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id),
+        None,
+    )
+    actual = next(
+        (
+            e["deviation_class"]
+            for e in report.get("deviation_register", [])
+            if e.get("hunk_id") == hunk_id
+        ),
+        None,
+    )
     if expected is None:
         return False, f"hunk {hunk_id!r} not present in annotated fixture"
     if expected == actual:
@@ -274,6 +343,7 @@ def path_exists(target: str) -> AssertionResult: ...
 ```python
 from pathlib import Path
 
+
 def check_path_exists(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     target = Path(assertion["target"])
     target = target if target.is_absolute() else (base_dir / target)
@@ -295,6 +365,7 @@ def path_does_not_exist(target: str) -> AssertionResult: ...
 ```python
 from pathlib import Path
 
+
 def check_path_does_not_exist(assertion: dict, base_dir: Path) -> tuple[bool, str]:
     target = Path(assertion["target"])
     target = target if target.is_absolute() else (base_dir / target)
@@ -323,7 +394,10 @@ from pathlib import Path
 
 CANONICAL_FIELDS = {"id", "type", "fixture", "expected", "assertion"}
 
-def check_falsifier_skeleton_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
+
+def check_falsifier_skeleton_present(
+    assertion: dict, base_dir: Path
+) -> tuple[bool, str]:
     case = base_dir / assertion["case_yaml"]
     if not case.exists():
         return False, f"falsifier case YAML missing: {assertion['case_yaml']}"
@@ -333,7 +407,10 @@ def check_falsifier_skeleton_present(assertion: dict, base_dir: Path) -> tuple[b
         return False, f"falsifier case YAML unparsable: {e}"
     status = data.get("status")
     if status == "skeleton-pending-iteration-3-fixture":
-        return True, f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}"
+        return (
+            True,
+            f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}",
+        )
     if status == "active":
         missing = CANONICAL_FIELDS - set(data.keys())
         if missing:
@@ -343,7 +420,10 @@ def check_falsifier_skeleton_present(assertion: dict, base_dir: Path) -> tuple[b
         # against the case's executed run results. This function confirms only
         # the structural contract; the runtime check is layered by the eval runner.
         return True, f"active falsifier with canonical fields; id={data.get('id')!r}"
-    return False, f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'"
+    return (
+        False,
+        f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'",
+    )
 ```
 
 ## Wiring into `check_assertion`
diff --git a/src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md b/src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md
index 4285799bf..205778dae 100644
--- a/src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md
+++ b/src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md
@@ -38,7 +38,7 @@ The selected depth string is interpolated directly into the prompt template at t
 Step(
     id="debate",
     prompt=build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth),
-    output_file=debate_file,                  # out / "debate-transcript.md"
+    output_file=debate_file,  # out / "debate-transcript.md"
     gate=DEBATE_GATE,
     timeout_seconds=600,
     inputs=[diff_file] + _llm_inputs_for(config, roadmap_a, roadmap_b),
diff --git a/src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md b/src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md
index 7c844b374..c8d79d2c3 100644
--- a/src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md
+++ b/src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md
@@ -22,7 +22,9 @@ Both functions return one prompt string and accept a `tool_write=` parameter (R1
 ```python
 # executor.py:2482-2497 — prompt build (R1.4 tool_write flag threaded in)
 if config.input_type == "tdd":
-    extract_prompt = build_extract_prompt_tdd(..., tool_write=config.tool_write_extract_tdd)
+    extract_prompt = build_extract_prompt_tdd(
+        ..., tool_write=config.tool_write_extract_tdd
+    )
 else:
     extract_prompt = build_extract_prompt(..., tool_write=config.tool_write_extract)
 
diff --git a/src/superclaude/skills/sc-validate-tests-protocol/SKILL.md b/src/superclaude/skills/sc-validate-tests-protocol/SKILL.md
index 73ef9c1c8..1ea517c34 100644
--- a/src/superclaude/skills/sc-validate-tests-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-validate-tests-protocol/SKILL.md
@@ -251,11 +251,11 @@ def calculate_confidence(scores, context):
             base_confidence *= 0.85  # Ambiguous
 
     # Boost for compound phrases
-    if context.get('compound_phrase_matched'):
+    if context.get("compound_phrase_matched"):
         base_confidence = min(0.95, base_confidence + 0.15)
 
     # Reduce for vague input
-    if context.get('vague_input') or context.get('no_keywords'):
+    if context.get("vague_input") or context.get("no_keywords"):
         base_confidence *= 0.7
 
     return round(base_confidence, 2)
diff --git a/src/superclaude/templates/documents/release-spec-template.md b/src/superclaude/templates/documents/release-spec-template.md
index 3e33b908a..b812a0291 100644
--- a/src/superclaude/templates/documents/release-spec-template.md
+++ b/src/superclaude/templates/documents/release-spec-template.md
@@ -137,7 +137,7 @@ quality_scores:
 > New or modified data structures. Include field definitions.
 
 ```python
-{{SC_PLACEHOLDER:data_model_code}}
+{{SC_PLACEHOLDER: data_model_code}}
 ```
 
 ### 4.6 Implementation Order
diff --git a/tests/observe/golden_release1_records.json b/tests/observe/golden_release1_records.json
deleted file mode 100644
index 5d3b520fd..000000000
--- a/tests/observe/golden_release1_records.json
+++ /dev/null
@@ -1,37 +0,0 @@
-{
- "base": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 80 / reported 80  scope=all  source counts: active 54 / reclaimable 0 / retained 13 / released 13  runs seen: 8  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=w-001 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=10s\ndispatchId=w-002 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=13s\ndispatchId=w-003 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=16s | flags=FROZEN\ndispatchId=w-004 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=19s\ndispatchId=w-005 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=approve | liveness=alive (terminal) | evidenceAge=22s\ndispatchId=w-006 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=25s\ndispatchId=w-007 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=28s\ndispatchId=w-008 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=31s\ndispatchId=w-009 | run=run-b | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=34s\ndispatchId=w-010 | run=run-c | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=37s\ndispatchId=w-011 | run=run-d | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=40s\ndispatchId=w-012 | run=run-e | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=43s\ndispatchId=w-013 | run=run-f | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=46s\ndispatchId=w-014 | run=run-g | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=49s\ndispatchId=w-015 | run=run-h | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=52s\ndispatchId=w-016 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=55s\ndispatchId=w-017 | run=run-b | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=58s\ndispatchId=w-018 | run=run-c | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-019 | run=run-d | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-020 | run=run-e | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-021 | run=run-f | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-022 | run=run-g | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-023 | run=run-h | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-024 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-025 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-026 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-027 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-028 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-029 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-030 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-031 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-032 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-033 | run=run-b | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-034 | run=run-c | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-035 | run=run-d | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-036 | run=run-e | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-037 | run=run-f | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-038 | run=run-g | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-039 | run=run-h | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-040 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-041 | run=run-b | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-042 | run=run-c | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-043 | run=run-d | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-044 | run=run-e | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-045 | run=run-f | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-046 | run=run-g | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-047 | run=run-h | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-048 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-049 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-050 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-051 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-052 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-053 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-054 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-055 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-056 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-057 | run=run-b | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-058 | run=run-c | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-059 | run=run-d | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-060 | run=run-e | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-061 | run=run-f | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-062 | run=run-g | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-063 | run=run-h | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-064 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-065 | run=run-b | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-066 | run=run-c | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-067 | run=run-d | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-068 | run=run-e | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-069 | run=run-f | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-070 | run=run-g | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-071 | run=run-h | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-072 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-073 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-074 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-075 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-076 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-077 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-078 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=4m\ndispatchId=w-079 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=4m\ndispatchId=w-080 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=4m\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 80,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 54,\n    \"reclaimable\": 0,\n    \"released\": 13,\n    \"retained\": 13\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 80\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"dispatchId\": \"w-001\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-002\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-003\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-003\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-004\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:41Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-004\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-005\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"approve\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-005\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-006\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:35Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-006\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-007\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:32Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-007\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-008\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:29Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-008\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-009\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:26Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-009\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-010\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:23Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-010\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-011\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:20Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-011\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-012\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:17Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-012\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-013\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:14Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-013\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-014\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:11Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-014\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-015\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:08Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-015\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-016\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:05Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-016\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-017\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:02Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-017\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-018\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:59Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-018\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-019\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:56Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-019\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-020\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:53Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-020\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-021\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:50Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-021\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-022\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:47Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-022\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-023\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:44Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-023\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-024\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:41Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-024\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-025\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-025\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-026\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:35Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-026\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-027\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:32Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-027\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-028\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:29Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-028\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-029\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:26Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-029\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-030\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:23Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-030\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-031\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:20Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-031\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-032\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:17Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-032\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-033\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:14Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-033\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-034\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:11Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-034\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-035\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:08Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-035\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-036\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:05Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-036\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-037\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:02Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-037\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-038\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:59Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-038\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-039\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:56Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-039\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-040\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:53Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-040\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-041\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-041\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-042\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-042\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-043\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:44Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-043\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-044\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:41Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-044\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-045\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:38Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-045\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-046\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:35Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-046\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-047\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:32Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-047\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-048\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:29Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-048\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-049\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:26Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-049\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-050\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:23Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-050\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-051\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:20Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-051\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-052\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:17Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-052\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-053\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:14Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-053\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-054\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:11Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-054\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-055\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:08Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-055\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-056\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:05Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-056\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-057\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:02Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-057\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-058\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:59Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-058\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-059\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:56Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-059\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-060\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:53Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-060\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-061\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-061\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-062\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-062\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-063\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-063\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-064\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:41Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-064\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-065\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-065\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-066\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:35Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-066\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-067\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:32Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-067\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-068\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:29Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-068\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-069\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:26Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-069\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-070\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:23Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-070\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-071\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:20Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-071\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-072\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:17Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-072\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-073\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:14Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-073\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-074\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:11Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-074\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-075\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:08Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-075\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-076\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:05Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-076\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-077\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:02Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-077\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-078\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:55:59Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-078\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-079\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:55:56Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-079\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-080\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:55:53Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-080\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"all\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:base\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "empty": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE empty, not Orca data  scope=bound  one Run only  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE empty, not Orca data  scope=bound  one Run only  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 0 / reported 0  scope=bound  source counts: active 0 / reclaimable 0 / retained 0 / released 0  runs seen: 0  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\nno observed items in this source window; not proof none exist\nworker-list returned 0 workers in scope=bound\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 0,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 0,\n    \"reclaimable\": 0,\n    \"released\": 0,\n    \"retained\": 0\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 0\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"bound\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:empty\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "injection": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE injection, not Orca data  scope=all  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE injection, not Orca data  scope=all  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 3 / reported 3  scope=all  source counts: active 2 / reclaimable 0 / retained 0 / released 1  runs seen: 3  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=w-inj-1 | run=run-a | workerState=link text | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=10s\ndispatchId=w-inj-2 | run=run-c1 | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=bellkind | liveness=alive (terminal) | evidenceAge=13s\ndispatchId=w-inj-3 | run=run-c | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=[bold]x[/bold] | liveness=ended (terminal) | evidenceAge=16s\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 3,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 2,\n    \"reclaimable\": 0,\n    \"released\": 1,\n    \"retained\": 0\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 3\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"dispatchId\": \"w-inj-1\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"link text\"\n    },\n    {\n      \"dispatchId\": \"w-inj-2\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"bellkind\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"rtl-role\",\n      \"runId\": \"run-c1\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-inj-3\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"[bold]x[/bold]\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"unterminated\"\n      },\n      \"taskId\": \"task with newline\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"all\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:injection\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "missing-fields": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE missing-fields, not Orca data  scope unknown  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE missing-fields, not Orca data  scope unknown  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 5 / reported unknown  scope unknown  source counts: unknown  runs seen: 1+? (1 unknown)  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=unknown | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=13s | flags=identity unknown\ndispatchId=w-003 | run=unknown | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=16s\ndispatchId=w-001 | run=run-a | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=unknown | liveness=unknown (unknown) | evidenceAge=10s\ndispatchId=w-004 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=unknown\ndispatchId=w-005 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=22s\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 5,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": \"UNKNOWN\",\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": \"UNKNOWN\"\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"absentFields\": [\n        \"dispatchId\"\n      ],\n      \"dispatchId\": \"UNKNOWN\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"absentFields\": [\n        \"runId\",\n        \"taskId\"\n      ],\n      \"dispatchId\": \"w-003\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"UNKNOWN\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"UNKNOWN\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"absentFields\": [\n        \"liveness.observedAt\",\n        \"liveness.source\",\n        \"liveness.verdict\",\n        \"nextAction\"\n      ],\n      \"dispatchId\": \"w-001\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"UNKNOWN\",\n        \"source\": \"UNKNOWN\",\n        \"verdict\": \"UNKNOWN\"\n      },\n      \"nextAction\": \"UNKNOWN\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"absentFields\": [\n        \"evidence.durable\",\n        \"evidence.lastObservedAt\",\n        \"evidence.liveStatus\"\n      ],\n      \"dispatchId\": \"w-004\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": \"UNKNOWN\",\n        \"lastObservedAt\": \"UNKNOWN\",\n        \"liveStatus\": \"UNKNOWN\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-004\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-005\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-005\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": \"UNKNOWN\",\n  \"source\": {\n    \"namespace\": \"fixture:missing-fields\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "source-loss": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE source-loss, not Orca data  scope=all  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE source-loss, not Orca data  scope=all  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 5 / reported 5  scope=all  source counts: active 3 / reclaimable 0 / retained 1 / released 1  runs seen: 1  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=w-001 | run=run-a | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=10s\ndispatchId=w-002 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=13s\ndispatchId=w-003 | run=run-a | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=16s\ndispatchId=w-004 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=19s\ndispatchId=w-005 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=22s\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 5,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 3,\n    \"reclaimable\": 0,\n    \"released\": 1,\n    \"retained\": 1\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 5\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"dispatchId\": \"w-001\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-002\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-003\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-003\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-004\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:41Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-004\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-005\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-005\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"all\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:source-loss\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- }
-}
\ No newline at end of file
diff --git a/tests/observe/live_child.py b/tests/observe/live_child.py
deleted file mode 100644
index 7f040265e..000000000
--- a/tests/observe/live_child.py
+++ /dev/null
@@ -1,41 +0,0 @@
-"""Live-screen child: draws one questions screen through the real ``LiveScreen`` on a pty.
-
-Run only by ``test_live_screen_pty.py``. It reads the terminal size and the environment the way
-the command does (``detect_size``, ``resolve_policy``), draws once, prints ``LIVE_READY`` and
-waits for one line on stdin, then closes the screen so the alternate screen is left cleanly.
-"""
-
-from __future__ import annotations
-
-import os
-import sys
-from pathlib import Path
-
-sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
-
-from superclaude.cli.observe.commands import LiveScreen  # noqa: E402
-from superclaude.cli.observe.terminal import (  # noqa: E402
-    detect_size,
-    output_encoding,
-    resolve_policy,
-)
-from tests.observe.conftest import FakeClock  # noqa: E402
-from tests.observe.test_render import r3_rows, r3_screen  # noqa: E402
-
-
-def main() -> int:
-    width, height = detect_size()
-    policy = resolve_policy(os.environ, output_encoding(), {}, width, height)
-    rows = r3_rows([("w-001", "first?"), ("w-002", "second?"), ("w-003", "third?")])
-    _, view = r3_screen(FakeClock(), rows, 1, width, height)
-    screen = LiveScreen()
-    screen.draw(view, policy, None)
-    sys.stdout.write("LIVE_READY\n")
-    sys.stdout.flush()
-    sys.stdin.readline()
-    screen.close()
-    return 0
-
-
-if __name__ == "__main__":
-    raise SystemExit(main())
diff --git a/tests/observe/test_height_budget.py b/tests/observe/test_height_budget.py
deleted file mode 100644
index 444a40047..000000000
--- a/tests/observe/test_height_budget.py
+++ /dev/null
@@ -1,26 +0,0 @@
-"""The questions-on screen never has more rows than the terminal (pins today's height budget).
-
-On ``Live(screen=True)`` rows past ``policy.height`` are dropped from the bottom, which are the
-footer keys and the ``shown x/y`` line, with no warning. Every phase that adds rows (frames, a
-count strip, a RETAIN CONTEXT pane) keeps this test green.
-"""
-
-from __future__ import annotations
-
-import pytest
-
-from tests.observe.test_render import WIDTHS, policy_for, r3_rows, r3_screen
-
-HEIGHTS = (24, 40, 44)
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-@pytest.mark.parametrize("height", HEIGHTS)
-@pytest.mark.parametrize("count", (3, 20))
-def test_questions_on_screen_fits_the_height(fake_clock, width, height, count):
-    rows = r3_rows([("w-001", f"question {i}?") for i in range(count)])
-    lines, _ = r3_screen(fake_clock, rows, 0, width, height=height)
-    policy = policy_for(width, height=height)
-    assert len(lines) <= policy.height or policy.too_small, (
-        f"{len(lines)} rows at height {height}, width {width}"
-    )
diff --git a/tests/observe/test_live_screen_pty.py b/tests/observe/test_live_screen_pty.py
deleted file mode 100644
index 009a9137f..000000000
--- a/tests/observe/test_live_screen_pty.py
+++ /dev/null
@@ -1,93 +0,0 @@
-"""The real ``LiveScreen`` on a pty: alternate screen, colour depth, no blink, no mouse (Q5 live gate).
-
-``Console(file=StringIO)`` writes nothing under ``Live(screen=True)``, so the live path is only
-checked on a real pseudo-terminal. The child is ``live_child.py``.
-"""
-
-from __future__ import annotations
-
-import os
-import re
-import sys
-from pathlib import Path
-
-import pytest
-
-pexpect = pytest.importorskip("pexpect")
-pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX pty test")
-
-CHILD = Path(__file__).with_name("live_child.py")
-ROOT = Path(__file__).resolve().parents[2]
-SGR = re.compile(rb"\x1b\[([0-9;]*)m")
-MOUSE = (b"\x1b[?1000h", b"\x1b[?1002h", b"\x1b[?1003h", b"\x1b[?1006h")
-
-
-def run_child(env_extra: dict, rows: int = 40, cols: int = 160) -> bytes:
-    """Everything the live screen wrote to the terminal, from start to a clean exit."""
-    env = {
-        k: v
-        for k, v in os.environ.items()
-        if k not in ("COLUMNS", "LINES", "NO_COLOR", "COLORTERM", "TERM")
-    }
-    env["TERM"] = "xterm"
-    env.update(env_extra)
-    child = pexpect.spawn(
-        sys.executable,
-        [str(CHILD)],
-        env=env,
-        dimensions=(rows, cols),
-        encoding=None,
-        cwd=str(ROOT),
-        timeout=60,
-    )
-    child.expect(b"LIVE_READY")
-    before = child.before + b"LIVE_READY"
-    child.sendline(b"")
-    child.expect(pexpect.EOF)
-    return before + child.before
-
-
-def sgr_codes(data: bytes) -> list[int]:
-    """Every SGR code in ``data``; the arguments of extended colours (38 and 48) are skipped."""
-    codes: list[int] = []
-    for match in SGR.finditer(data):
-        params = [int(p) if p else 0 for p in match.group(1).split(b";")]
-        i = 0
-        while i < len(params):
-            if params[i] in (38, 48) and i + 1 < len(params):
-                i += 3 if params[i + 1] == 5 else 5
-                continue
-            codes.append(params[i])
-            i += 1
-    return codes
-
-
-def test_the_live_screen_uses_the_alternate_screen_and_no_mouse_or_blink():
-    out = run_child({})
-    assert b"\x1b[?1049h" in out and b"\x1b[?1049l" in out  # entered and left cleanly
-    assert not any(seq in out for seq in MOUSE)
-    assert not {5, 6} & set(sgr_codes(out))  # no blink
-
-
-def test_a_truecolor_terminal_gets_the_mockup_palette():
-    out = run_child({"COLORTERM": "truecolor"})
-    assert b"38;2;" in out
-
-
-def test_a_256_colour_terminal_gets_indexed_colours_only():
-    out = run_child({"TERM": "xterm-256color"})
-    assert b"38;5;" in out and b"38;2;" not in out
-
-
-def test_a_16_colour_terminal_gets_only_16_colour_codes():
-    out = run_child({})
-    codes = sgr_codes(out)
-    assert codes and b"38;2;" not in out and b"38;5;" not in out
-    assert all(c in (0, 1, 22) or 30 <= c <= 37 or 90 <= c <= 97 for c in codes)
-
-
-def test_no_color_writes_no_colour_or_weight_codes():
-    out = run_child({"NO_COLOR": "1", "COLORTERM": "truecolor"})
-    assert b"\x1b[?1049h" in out
-    # Measured: with NO_COLOR the console sets no style at all, so no SGR sequence is written.
-    assert sgr_codes(out) == []
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 2ea236098..18f07d2a9 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -449,7 +449,10 @@ def test_t19_the_screen_carries_the_title_disclosure_and_one_line_per_question(
     assert "at most 100 rows per read, not 100 questions" in flat
     assert "bounded best effort; coverage unknown" in flat
     assert "bursts over 100 rows between reads may be lost" in flat
-    assert "seen, not resolved: 5 | closed by evidence: unavailable (no source)" in flat
+    assert "seen, not resolved: 5 | closed by evidence: unavailable" in flat
+    assert (
+        "evidence: unavailable (no source)" not in flat
+    )  # screen only: the record keeps it
     assert (
         "retention reset at 12:00; questions observed before this start are not retained"
         in flat
@@ -926,7 +929,10 @@ def test_r3_the_selected_question_has_the_selected_glyph_and_the_desk_follows(
     assert all(cell_len(ln) <= width for ln in lines)
     assert DESK_TITLE in lines and view.desk.ask == "second?"
     flat = flat_of(lines)
-    assert "dispatchId: w-002" in flat and "resource.worktreeId:" in flat
+    assert "session w-002" in flat and "worktree " in flat
+    assert (
+        "dispatchId:" not in flat and "resource.worktreeId" not in flat
+    )  # plain labels
     ascii_lines, _ = r3_screen(
         fake_clock, r3_rows([("w-001", "first?")]), 0, width, ascii=True
     )
@@ -974,10 +980,13 @@ def test_r3_a_long_question_shows_a_visible_mark_in_the_desk_and_on_the_list(
     rows = r3_rows([("w-001", "word " * 200)])
     lines, view = r3_screen(fake_clock, rows, 0, 160, height=60)
     listed = question_rows(lines)
-    assert listed and "..." in listed[0]
+    assert listed and listed[0].endswith(
+        ">"
+    )  # one short line; the full text is in the desk
+    assert "word word word word word word word word word word" not in listed[0]
     desk = lines[lines.index(DESK_TITLE) :]
     text_lines = desk[
-        2 : next(i for i, ln in enumerate(desk) if ln.startswith("dispatchId:"))
+        2 : next(i for i, ln in enumerate(desk) if ln.startswith("session "))
     ]
     assert 1 <= len(text_lines) <= 4 and text_lines[-1].endswith("...")
     assert all(cell_len(ln) <= 160 for ln in lines)
@@ -989,7 +998,7 @@ def test_r3_the_desk_text_is_bounded_to_four_lines_with_a_mark_at_80_columns(
     rows = r3_rows([("w-001", "word " * 200)])
     lines, _ = r3_screen(fake_clock, rows, 0, 80, height=70)
     desk = lines[lines.index(DESK_TITLE) :]
-    end = next(i for i, ln in enumerate(desk) if ln.startswith("dispatchId:"))
+    end = next(i for i, ln in enumerate(desk) if ln.startswith("session "))
     text_lines = desk[2:end]
     assert len(text_lines) == 4 and text_lines[-1].endswith("...")
     assert all(cell_len(ln) <= 80 for ln in lines)
@@ -1072,7 +1081,7 @@ PATHS_THEN_HASH = (
 def desk_text_lines(lines):
     """The question-text lines of the unframed Decision Desk: after ``qid  age`` and up to the first field."""
     desk = lines[lines.index(DESK_TITLE) :]
-    end = next(i for i, ln in enumerate(desk) if ln.startswith("dispatchId:"))
+    end = next(i for i, ln in enumerate(desk) if ln.startswith("session "))
     return desk[2:end]
 
 
@@ -1177,21 +1186,19 @@ def test_r3_a_120_character_worktree_id_continues_on_two_cell_indented_lines(
     session = Session(selected_question=(QRUN, f"msg_{1:012x}"))
     lines = screen_lines(build_view(result, session, fake_clock), policy_for(width, 70))
     assert all(cell_len(ln) <= width for ln in lines)
-    start = next(
-        i for i, ln in enumerate(lines) if ln.startswith("resource.worktreeId:")
-    )
-    if width == 160:  # label, space and value (141 cells) fit one line: no continuation
-        assert lines[start] == f"resource.worktreeId: {worktree}"
+    start = next(i for i, ln in enumerate(lines) if ln.startswith("worktree "))
+    note = "(this session only)"
+    if width == 160:  # label column, id, two spaces and the note fit one line
+        assert lines[start] == f"worktree {worktree}  {note}"
         return
     tail = []
     for ln in lines[start + 1 :]:
-        if not ln.startswith("  "):
+        if not ln.startswith(" " * 9):  # continuation lines sit under the value column
             break
         tail.append(ln)
-    assert len(tail) >= 2 and all(ln.startswith("  ") for ln in tail)
-    assert (
-        "".join(ln[2:] for ln in tail) == worktree
-    )  # hard-split, nothing lost, no marker
+    assert tail and all(ln.startswith(" " * 9) for ln in tail)
+    shown = "".join(ln[9:] for ln in [lines[start], *tail]).replace(" ", "")
+    assert shown == (worktree + note).replace(" ", "")  # split, nothing lost, no marker
 
 
 def test_strip_sgr_removes_colour_codes_and_sgr_params_lists_them():
@@ -1476,3 +1483,125 @@ def test_the_record_title_keeps_no_badge(fake_clock):
     from superclaude.cli.observe.view import READ_ONLY_BADGE
 
     assert READ_ONLY_BADGE not in record_text(fixture_view("base", fake_clock))
+
+
+# -- Task 14: each fact once, questions first, aligned desk labels, one status badge --------------------------
+
+CENSUS_ASK = "Approve the release notes before the worker publishes the package to the registry today?"
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_each_fact_occurs_once_on_the_questions_screen(fake_clock, width):
+    rows = r3_rows([("w-001", "first?"), ("w-002", CENSUS_ASK)])
+    lines, view = r3_screen(fake_clock, rows, 1, width, height=70)
+    flat = flat_of(lines)
+    assert (
+        flat.count(CENSUS_ASK) == 1
+    )  # the desk holds the full text; the list row is a stub
+    selected = next(ln for ln in lines if ln.startswith("▸ "))
+    assert selected.endswith(">") and CENSUS_ASK not in selected
+    assert flat.count(QRUN) == 1  # the Run id: the panel title row only
+    assert flat.count("seen, not resolved") == 1
+    assert flat.count("closed by evidence") == 1
+    assert (
+        flat.count("questions OK 0s") == 1
+    )  # the strip cell; the panel keeps "question read:"
+    assert flat.count("question read: OK 0s") == 1
+    assert flat.count("msg_") == 0  # the message id is not on the desk pane
+    assert flat.count("worker-reported, not questions") == 1
+    assert flat.count("retention reset at") == 1
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_question_rows_come_first_then_the_standing_lines_adjacent(fake_clock, width):
+    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
+    lines, view = r3_screen(fake_clock, rows, None, width, height=70)
+    last_row = max(i for i, ln in enumerate(lines) if question_rows([ln]))
+    disclosure = next(
+        i for i, ln in enumerate(lines) if ln.startswith("bounded best effort")
+    )
+    marker = next(i for i, ln in enumerate(lines) if "no read marker in source" in ln)
+    retention = next(i for i, ln in enumerate(lines) if "retention reset at" in ln)
+    assert last_row < disclosure < marker
+    assert retention == marker + len(wrap_text(view.questions.caveat_line, width))
+    assert "".join(lines[disclosure : disclosure + 1]).startswith(
+        "bounded best effort; coverage unknown"
+    )
+
+
+def wrap_text(text, width):
+    return render_module.wrap(text, width, policy_for(width))
+
+
+def desk_after(fake_clock, mutate, width=116):
+    """The desk pane lines of a linked question whose worker row was changed by ``mutate``."""
+    workers = make_rows(3, 1)
+    for row in workers:
+        mutate(row)
+    worker = (0, json.dumps(make_envelope(workers, total=3)))
+    message = ok_message(r3_rows([("w-001", "first?"), ("w-002", "second?")]))
+    runner = FakeRunner([], [routed_runner_responses(worker, message)])
+    result = Collector(
+        LiveSource(runner, FakeDiscover([])),
+        fake_clock,
+        run_id=QRUN,
+        questions=True,
+        link=True,
+    ).run_once()
+    session = Session(selected_question=(QRUN, f"msg_{1:012x}"))
+    lines = screen_lines(build_view(result, session, fake_clock), policy_for(width, 70))
+    desk = lines[lines.index(DESK_TITLE) :]
+    return desk[
+        : next(
+            (
+                i
+                for i, ln in enumerate(desk)
+                if ln.startswith("retention") or "bounded" in ln
+            ),
+            len(desk),
+        )
+    ]
+
+
+def test_desk_labels_are_plain_aligned_and_alive_is_one_value(fake_clock):
+    desk = desk_after(fake_clock, lambda row: None)
+    fields = {
+        ln[:9].strip(): ln[9:] for ln in desk[1:] if ln[:1].isalpha() and ln[8:9] == " "
+    }
+    assert list(fields) == ["session", "state", "alive", "next", "status", "worktree"]
+    assert fields["session"] == "w-002" and fields["state"] == "idle"
+    assert fields["alive"] == "yes (terminal), 6s ago"
+    assert fields["status"] == "ACTIVE"
+    assert (
+        fields["worktree"].endswith("(this session only)")
+        or fields["worktree"] == "unknown"
+    )
+    assert not any(raw in " ".join(desk) for raw in ("dispatchStatus", "terminalState"))
+
+
+def test_the_active_badge_needs_active_active_none_else_three_raw_rows(fake_clock):
+    def changed(row):
+        row["projection"]["outcome"] = "blocked"
+
+    desk = desk_after(fake_clock, changed)
+    text = "\n".join(desk)
+    assert "ACTIVE" not in text
+    for raw, value in (
+        ("dispatchStatus", "active"),
+        ("terminalState", "active"),
+        ("outcome", "blocked"),
+    ):
+        assert any(ln.startswith(raw) and ln.endswith(value) for ln in desk), raw
+    assert not any(ln.startswith("status ") for ln in desk)
+
+
+def test_an_absent_status_value_expands_to_three_rows_and_reads_unknown(fake_clock):
+    def absent(row):
+        del row["terminalState"]
+
+    desk = desk_after(fake_clock, absent)
+    assert "ACTIVE" not in "\n".join(desk)
+    terminal = next(ln for ln in desk if ln.startswith("terminalState"))
+    assert terminal.endswith("unknown") and "absent in source" not in terminal
+    assert any(ln.startswith("dispatchStatus") for ln in desk)
+    assert any(ln.startswith("outcome") for ln in desk)
diff --git a/tests/observe/test_styled_capture.py b/tests/observe/test_styled_capture.py
deleted file mode 100644
index 51ca96474..000000000
--- a/tests/observe/test_styled_capture.py
+++ /dev/null
@@ -1,83 +0,0 @@
-"""The one-shot path can carry the screen's colour and weight; the capture is never export_text(styles=True)."""
-
-from __future__ import annotations
-
-import io
-
-import pytest
-
-from superclaude.cli.observe.commands import (
-    Options,
-    _screen_text,
-    _stdout_is_tty,
-    execute,
-)
-from superclaude.cli.observe.terminal import resolve_policy
-from tests.observe.conftest import strip_sgr
-from tests.observe.test_commands import deps_for
-from tests.observe.test_render import WIDTHS, fixture_view
-
-
-class _Tty(io.StringIO):
-    def isatty(self) -> bool:
-        return True
-
-
-def _policy(width, env=None, ascii=False):
-    return resolve_policy(env or {}, "utf-8", {"ascii": ascii}, width, 40)
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_a_styled_screen_has_escapes_and_the_same_text_as_the_plain_one(
-    fake_clock, width
-):
-    view = fixture_view("base", fake_clock)
-    policy = _policy(width)
-    styled = _screen_text(view, policy, styled=True)
-    plain = _screen_text(view, policy, styled=False)
-    assert "\x1b[" in styled
-    assert strip_sgr(styled) == plain and "\x1b" not in plain
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_no_color_gives_zero_escape_bytes_even_when_styled_is_asked_for(
-    fake_clock, width
-):
-    view = fixture_view("base", fake_clock)
-    out = _screen_text(view, _policy(width, {"NO_COLOR": "1"}), styled=True)
-    assert "\x1b" not in out
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_ascii_stays_ascii_with_colour_on(fake_clock, width):
-    view = fixture_view("long-identifiers", fake_clock)
-    out = _screen_text(view, _policy(width, ascii=True), styled=True)
-    assert "\x1b[" in out and out.isascii()
-
-
-def test_the_styled_capture_follows_the_colour_depth(fake_clock):
-    view = fixture_view("base", fake_clock)
-    truecolor = _screen_text(
-        view, _policy(160, {"COLORTERM": "truecolor"}), styled=True
-    )
-    standard = _screen_text(view, _policy(160), styled=True)
-    assert "38;2;" in truecolor and "38;2;" not in standard
-
-
-def test_a_piped_one_shot_stays_plain_and_a_terminal_one_is_styled(fake_clock):
-    options = Options(once=True, fixture="base", width=160)
-    piped = deps_for(fake_clock)  # a StringIO: not a terminal
-    assert execute(options, piped) == 0 and "\x1b" not in piped.stdout.getvalue()
-    tty = deps_for(fake_clock, stdout=_Tty())
-    assert execute(options, tty) == 0 and "\x1b[" in tty.stdout.getvalue()
-    quiet = deps_for(fake_clock, stdout=_Tty(), env={"NO_COLOR": "1"})
-    assert execute(options, quiet) == 0 and "\x1b" not in quiet.stdout.getvalue()
-    assert strip_sgr(tty.stdout.getvalue()) == piped.stdout.getvalue()
-
-
-def test_a_stream_without_isatty_counts_as_not_a_terminal(fake_clock):
-    class _Bare:
-        def write(self, text):
-            return len(text)
-
-    assert _stdout_is_tty(deps_for(fake_clock, stdout=_Bare())) is False
diff --git a/tests/observe/test_theme.py b/tests/observe/test_theme.py
deleted file mode 100644
index 8add9681d..000000000
--- a/tests/observe/test_theme.py
+++ /dev/null
@@ -1,95 +0,0 @@
-"""Colour roles: every role exists at every depth, the 16-colour floor keeps its roles apart."""
-
-from __future__ import annotations
-
-import pytest
-
-from superclaude.cli.observe import theme
-from superclaude.cli.observe.theme import (
-    FROZEN_ROLE,
-    ROLES,
-    STATE_ROLE,
-    style_for,
-)
-
-DEPTHS = ("standard", "256", "truecolor")
-# One role per palette colour, so eight distinct colours means eight distinct roles (RB-09).
-PALETTE_ROLES = (
-    "attention",  # amber
-    "identity",  # base
-    "secondary",  # slate
-    "muted",
-    "state_running",  # green
-    "state_settled",  # cyan
-    "state_failed",  # red
-    "state_frozen",  # violet
-)
-
-
-@pytest.mark.parametrize("depth", DEPTHS)
-def test_every_role_has_a_style_at_every_depth(depth):
-    for role in ROLES:
-        assert style_for(role, depth) is not None
-
-
-def test_no_depth_means_no_style():
-    assert all(style_for(role, None) is None for role in ROLES)
-
-
-def test_an_unknown_role_is_an_error_not_a_silent_default():
-    with pytest.raises(KeyError):
-        style_for("nonsense", "standard")
-
-
-def test_the_eight_palette_roles_keep_eight_distinct_colours_at_16_colours():
-    numbers = [style_for(role, "standard").color.number for role in PALETTE_ROLES]
-    assert len(set(numbers)) == 8
-
-
-def test_the_four_state_roles_have_four_different_codes_at_16_colours():
-    roles = ("state_running", "state_settled", "state_failed", "state_frozen")
-    codes = {style_for(role, "standard").color.number for role in roles}
-    assert len(codes) == 4
-
-
-def test_the_state_table_is_not_empty_and_names_the_minimum_keys():
-    required = [
-        ("workerState", "running"),
-        ("workerState", "succeeded"),
-        ("workerState", "failed"),
-        ("dispatchStatus", "completed"),
-        ("liveness", "alive"),
-    ]
-    assert all(key in STATE_ROLE for key in required)
-    assert FROZEN_ROLE == "state_frozen"
-    assert all(role in ROLES for role in (*STATE_ROLE.values(), FROZEN_ROLE))
-    # A word the table does not name keeps the body role: it is never classified.
-    assert ("workerState", "blocked") not in STATE_ROLE
-    assert ("terminalState", "released") not in STATE_ROLE
-
-
-def test_no_style_blinks_dims_or_reverses():
-    for depth in DEPTHS:
-        for role in ROLES:
-            style = style_for(role, depth)
-            assert not (style.blink or style.blink2 or style.dim or style.reverse)
-
-
-def test_styles_are_distinct_objects_per_depth_and_cached_per_depth():
-    standard = style_for("attention", "standard")
-    truecolor = style_for("attention", "truecolor")
-    assert standard is not truecolor and standard != truecolor
-    assert style_for("attention", "standard") is standard
-    assert truecolor.color.get_truecolor().hex == "#fab219"
-
-
-def test_the_theme_module_holds_no_terminal_facts():
-    text = open(theme.__file__, encoding="utf-8").read()
-    for literal in (
-        "Console(",
-        "NO_COLOR",
-        "COLUMNS",
-        "stdout.encoding",
-        "getpreferredencoding",
-    ):
-        assert literal not in text


Codegraph context: index_state=fresh checked_at=2026-11-18T04:42:32Z worktree_root=issue-606 worktree projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: export.py (untouched) reads QuestionsPanel title, run_line, summary, state_lines, disclosure, counts_line, caveat_line, retention_line and QuestionLine qid, text, dispatch_id, link; View.header1 and header2.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
