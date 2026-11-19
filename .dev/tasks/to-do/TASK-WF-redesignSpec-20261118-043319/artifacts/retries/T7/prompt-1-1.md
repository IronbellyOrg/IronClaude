76d17eb2aa1ba423dce667538b302ca392975ff2
Review one task for spec compliance.

Task brief: ## Task 7: Assign roles at the builders

Depends on: Task 6

Spec step 1.4 (no text edits). In `OBS/render.py` give roles at `counts_lines`, `_row_line` (rebuilt as `_row_segments`), `_header_lines`, `_inspector_lines`, `_question_line`, `_desk_lines`, `_panel_lines` and the footer exactly as step 1.4 lists: title, muted header2 and footer, protected counts tokens `identity` and `UNAVAILABLE` suffix muted, question line segments (age `attention` bold, subject `body_bold`, reason tail muted, selected marker and line `selected`), desk title and qid and question text `attention` bold, field labels muted. A cell whose stripped text is the bare `unknown` is muted; `workerState`, `dispatchStatus` (full layout) and the liveness verdict take `STATE_ROLE` by exact `(field, raw value)` equality (the verdict is `row.raw.liveness_verdict`, and in the `full` layout the cell text is `<verdict> (<source>)`); a flags cell containing `FROZEN_MARKER` is `state_frozen`; `nextAction.kind` and `terminalState` stay `body`. Re-read `RowView` construction (`OBS/view.py` lines 481-518) and the `OBS/parse.py` value sets before coding. No regex runs over worker-controlled text.

Acceptance criteria:
- With colour on, the plain text is unchanged: `strip_sgr(coloured print) == NO_COLOR print` at 160, 116 and 80 for the base fixture.
- A selected question has a bold amber role in addition to its glyph; absent values are muted; state words are always printed.
- `uv run pytest tests/observe/ -v` is green with both goldens untouched.
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
Start sha: 76d17eb2aa1ba423dce667538b302ca392975ff2
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b (Grep floor, confirmed by Read): the private builders changed from strings to Line objects (_row_line renamed _row_segments, _header_lines, _help_lines, _question_line, _desk_lines, _panel_lines, _inspector_lines; counts_lines keeps its string return and now wraps counts_line_objects); grep over src/ and tests/ finds no other caller of any of them (only src/superclaude/cli/observe/render.py itself), screen_lines and render keep their signatures. Also changed because colour now reaches printed output: tests/observe/release1_surface.py (_printed strips SGR) and two tests in tests/observe/test_render.py.
Evidence: uv run pytest tests/observe/ -q printed '830 passed in 19.76s' (824 before this task); ruff check: All checks passed; git diff --stat -- tests/observe/*.json is empty (no golden changed). The state-word table values are in src/superclaude/cli/observe/theme.py (STATE_ROLE). Touched: src/superclaude/cli/observe/render.py, tests/observe/test_render.py, tests/observe/release1_surface.py.

diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 7de34c6c4..8c67ec947 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -3,6 +3,11 @@
 It only lays out and truncates. Every status literal and both row orders come from the
 ``View``; every truncation goes through ``terminal.clip``; text is built as ``rich.text.Text``
 from data (never markup strings). It never imports the adapter or the collector.
+
+Each screen line is a ``Line``: its plain text (the source of truth for the record, the goldens
+and every test) plus colour roles that ``render`` turns into styles for the terminal's colour
+depth. Roles are attached where a builder already knows what a piece of text is; no pattern is
+matched over worker-controlled text.
 """
 
 from __future__ import annotations
@@ -21,18 +26,21 @@ from superclaude.cli.observe.terminal import (
     clip,
     glyph,
 )
-from superclaude.cli.observe.theme import style_for
+from superclaude.cli.observe.theme import FROZEN_ROLE, STATE_ROLE, style_for
 from superclaude.cli.observe.view import (
+    ABSENT_IN_SOURCE,
     DESK_HIDDEN,
     DESK_SELECTED_HIDDEN,
     DESK_TEXT_LINES,
     DESK_TITLE,
+    FROZEN_MARKER,
     INSPECTOR_ABOVE_TEXT,
     INSPECTOR_BELOW_TEXT,
     INSPECTOR_HELP,
     INSPECTOR_TITLE,
     NO_MATCH_TEXT,
     QUESTIONS_REASON,
+    UNAVAILABLE,
     CountsToken,
     DeskView,
     QuestionLine,
@@ -85,10 +93,6 @@ def _pad(text: str, width: int) -> str:
     return text + " " * max(width - cell_len(text), 0)
 
 
-def _cell(text: str, width: int, policy: TerminalPolicy) -> str:
-    return _pad(clip(text, width, policy), width)
-
-
 # -- lines with colour roles ---------------------------------------------------------------------
 
 
@@ -124,6 +128,16 @@ class Line:
         )
         return Line(text, spans)
 
+    def rstripped(self) -> Line:
+        """The line without trailing spaces; spans are trimmed to the kept text."""
+        text = self.plain.rstrip()
+        spans = tuple(
+            Span(s.start, min(s.end, len(text)), s.role)
+            for s in self.spans
+            if s.start < len(text)
+        )
+        return Line(text, spans)
+
     def to_ascii(self) -> Line:
         """Every non-ASCII character becomes one ``?``, so the span offsets stay valid."""
         return Line(ascii_safe(self.plain), self.spans)
@@ -151,53 +165,92 @@ def _roled(strings: list[str], role: str) -> list[Line]:
     return [seg(text, role) for text in strings]
 
 
+def _wrapped(text: str, width: int, policy: TerminalPolicy, role: str) -> list[Line]:
+    return _roled(wrap(text, width, policy), role)
+
+
+def _cell(text: str, width: int, policy: TerminalPolicy, role: str = "body") -> Line:
+    """One padded column cell; the role covers the text, never the padding."""
+    shown = clip(text, width, policy)
+    return join(seg(shown, role), seg(" " * max(width - cell_len(shown), 0)))
+
+
+def _absent_role(text: str, role: str = "body") -> str:
+    """``muted`` for a bare absent value (``text_of`` quotes a real value "unknown", so the bare
+    word means the source had none); otherwise ``role``."""
+    return "muted" if text.strip() in ("unknown", ABSENT_IN_SOURCE) else role
+
+
 # -- the COUNTS strip ------------------------------------------------------------------------------
 
 
-def counts_lines(
+def _token_line(text: str, token: CountsToken) -> Line:
+    if token.protected:
+        return seg(text, "identity")
+    if text.endswith(UNAVAILABLE):  # the suffix is the absent part: muted
+        cut = len(text) - len(UNAVAILABLE)
+        return join(seg(text[:cut], "body"), seg(text[cut:], "muted"))
+    return seg(text, "body")
+
+
+def counts_line_objects(
     tokens: tuple[CountsToken, ...],
     policy: TerminalPolicy,
     max_lines: int | None = MAX_COUNT_LINES,
-) -> list[str]:
+) -> list[Line]:
     """Lay tokens out in priority order. Protected tokens are never truncated: they wrap.
 
     Lower-priority tokens that do not fit within ``max_lines`` are cut with ``>``.
     """
     width = policy.width
-    lines: list[str] = []
-    current = ""
+    lines: list[Line] = []
+    current = Line("")
     cut = False
     for token in tokens:
         text = ascii_safe(token.text) if policy.ascii else token.text
         if cut and not token.protected:
             continue
-        candidate = f"{current}  {text}" if current else text
-        if cell_len(candidate) <= width:
+        piece = _token_line(text, token)
+        candidate = join(current, seg("  "), piece) if current.plain else piece
+        if cell_len(candidate.plain) <= width:
             current = candidate
             continue
         if token.protected:
-            if current:
+            if current.plain:
                 lines.append(current)
             chunks = wrap(text, width, policy)
-            lines.extend(chunks[:-1])
-            current = chunks[-1]
+            lines.extend(seg(chunk, "identity") for chunk in chunks[:-1])
+            current = seg(chunks[-1], "identity")
             continue
         if max_lines is None or len(lines) + 1 < max_lines:
-            if current:
+            if current.plain:
                 lines.append(current)
-            current = clip(text, width, policy)
+            current = _token_line(clip(text, width, policy), token)
             continue
-        room = width - cell_len(current) - 2
+        room = width - cell_len(current.plain) - 2
         if room >= 2:
-            current = f"{current}  {clip(text, room, policy)}"
+            current = join(
+                current, seg("  "), _token_line(clip(text, room, policy), token)
+            )
         else:
-            current = clip(current + " " + glyph("truncate", policy), width, policy)
+            current = join(current, seg(" " + glyph("truncate", policy))).clipped(
+                width, policy
+            )
         cut = True
-    if current:
+    if current.plain:
         lines.append(current)
     return lines
 
 
+def counts_lines(
+    tokens: tuple[CountsToken, ...],
+    policy: TerminalPolicy,
+    max_lines: int | None = MAX_COUNT_LINES,
+) -> list[str]:
+    """The plain text of ``counts_line_objects``."""
+    return [line.plain for line in counts_line_objects(tokens, policy, max_lines)]
+
+
 # -- ledger rows -----------------------------------------------------------------------------------------
 
 
@@ -293,29 +346,87 @@ def _columns(policy: TerminalPolicy) -> tuple[list[tuple[str, int]], list]:
     return names, getters
 
 
-def _row_line(
-    row: RowView, columns: list[tuple[str, int]], getters: list, policy: TerminalPolicy
-) -> str:
-    cells = []
-    for (_, width), getter in zip(columns, getters, strict=True):
-        cells.append(
-            _pad(_marker(row, policy), width)
-            if getter is None
-            else _cell(getter(row), width, policy)
-        )
-    return clip(SEPARATOR.join(cells).rstrip(), policy.width, policy)
+def _cell_role(name: str, row: RowView, text: str) -> str:
+    """The role of one row cell, from the column and the exact raw value (never a pattern)."""
+    if name == "workerState":
+        role = STATE_ROLE.get(("workerState", row.worker_state))
+    elif name == "dispatchStatus":
+        role = STATE_ROLE.get(("dispatchStatus", row.dispatch_status))
+    elif name == "flags":
+        role = FROZEN_ROLE if FROZEN_MARKER in row.flags else None
+    else:
+        role = None
+    if name in ("nextAction.kind", "kind"):  # the verbatim kind is never classified
+        return _absent_role(text)
+    return role or _absent_role(text)
 
 
-def _header_lines(columns: list[tuple[str, int]], policy: TerminalPolicy) -> list[str]:
-    head = SEPARATOR.join(_cell(name, width, policy) for name, width in columns)
+def _row_segments(
+    row: RowView, columns: list[tuple[str, int]], getters: list, policy: TerminalPolicy
+) -> Line:
+    cells: list[Line] = []
+    for (name, width), getter in zip(columns, getters, strict=True):
+        if getter is None:
+            cells.append(_cell(_marker(row, policy), width, policy, "body"))
+            continue
+        text = getter(row)
+        cell = _cell(text, width, policy, _cell_role(name, row, text))
+        if (
+            name == "liveness"
+        ):  # the verdict word carries the state; "(source)" stays body
+            verdict = _verdict(row)
+            role = STATE_ROLE.get(("liveness", verdict)) or _absent_role(verdict)
+            shown = clip(text, width, policy)
+            if shown.startswith(verdict) and verdict:
+                rest = shown[len(verdict) :]
+                cell = join(
+                    seg(verdict, role),
+                    seg(rest, "body"),
+                    seg(" " * max(width - cell_len(shown), 0)),
+                )
+        cells.append(cell)
+    parts: list[Line] = []
+    for index, cell in enumerate(cells):
+        if index:
+            parts.append(seg(SEPARATOR))
+        parts.append(cell)
+    return join(*parts).rstripped().clipped(policy.width, policy)
+
+
+def _header_lines(columns: list[tuple[str, int]], policy: TerminalPolicy) -> list[Line]:
+    head = SEPARATOR.join(
+        _pad(clip(name, width, policy), width) for name, width in columns
+    )
     rule = SEPARATOR.join(glyph("hrule", policy) * width for _, width in columns)
-    return [clip(head.rstrip(), policy.width, policy), clip(rule, policy.width, policy)]
+    return [
+        seg(clip(head.rstrip(), policy.width, policy), "muted"),
+        seg(clip(rule, policy.width, policy), "border_secondary"),
+    ]
 
 
 # -- screens -------------------------------------------------------------------------------------------------
 
 
-def _inspector_lines(view: View, policy: TerminalPolicy, budget: int) -> list[str]:
+def _labelled(
+    label: str, value: str, width: int, policy: TerminalPolicy, role: str
+) -> list[Line]:
+    """``label: value`` wrapped to ``width``; continuation lines are indented two cells.
+    The label is muted; ``role`` covers the value."""
+    first, *rest = wrap(f"{label}: {value}", width, policy)
+    prefix = f"{label}:"
+    if first.startswith(prefix):
+        lines = [join(seg(prefix, "muted"), seg(first[len(prefix) :], role))]
+    else:
+        lines = [seg(first, role)]
+    for continuation in rest:
+        lines += [
+            seg("  " + part, role)
+            for part in wrap(continuation, max(width - 2, 1), policy)
+        ]
+    return lines
+
+
+def _inspector_lines(view: View, policy: TerminalPolicy, budget: int) -> list[Line]:
     """The title, then the field lines from ``view.inspector_scroll`` on, never more than ``budget`` lines.
 
     The scroll is in wrapped lines, so a field taller than the screen is still readable (d/u);
@@ -323,16 +434,10 @@ def _inspector_lines(view: View, policy: TerminalPolicy, budget: int) -> list[st
     """
     selected = view.selected
     title = f"{INSPECTOR_TITLE}  {selected.dispatch_id if selected else ''}"
-    lines = wrap(title, policy.width, policy)
-    body: list[str] = []
+    lines = _wrapped(title, policy.width, policy, "attention_title")
+    body: list[Line] = []
     for label, value in view.inspector or ():
-        first, *rest = wrap(f"{label}: {value}", policy.width, policy)
-        body.append(first)
-        for continuation in rest:  # continuation lines are indented two cells
-            body.extend(
-                "  " + part
-                for part in wrap(continuation, max(policy.width - 2, 1), policy)
-            )
+        body += _labelled(label, value, policy.width, policy, _absent_role(value))
     room = max(budget - len(lines), 1)
     # never scroll past the point where the last line is on screen under an "above" line
     start = min(max(view.inspector_scroll, 0), max(len(body) - max(room - 1, 1), 0))
@@ -343,10 +448,14 @@ def _inspector_lines(view: View, policy: TerminalPolicy, budget: int) -> list[st
         take = max(space - 1, 1)  # one line kept for the "below" text
         shown, below = body[start : start + take], len(body) - start - take
     if start:
-        lines += wrap(INSPECTOR_ABOVE_TEXT.format(n=start), policy.width, policy)
+        lines += _wrapped(
+            INSPECTOR_ABOVE_TEXT.format(n=start), policy.width, policy, "muted"
+        )
     lines += shown
     if below:
-        lines += wrap(INSPECTOR_BELOW_TEXT.format(n=below), policy.width, policy)
+        lines += _wrapped(
+            INSPECTOR_BELOW_TEXT.format(n=below), policy.width, policy, "muted"
+        )
     return lines[: max(budget, 1)]
 
 
@@ -364,19 +473,33 @@ def _notes(view: View) -> list[str]:
     return ["  ".join(parts)] if parts else []
 
 
-def _help_lines(view: View, policy: TerminalPolicy) -> list[str]:
+def _help_lines(view: View, policy: TerminalPolicy) -> list[Line]:
     """The key list: clipped as in release 1, but wrapped when questions are on (no key is cut)."""
     if view.questions is None:
-        return [clip(view.help_line, policy.width, policy)]
-    return wrap(view.help_line, policy.width, policy)
+        return [seg(clip(view.help_line, policy.width, policy), "muted")]
+    return _wrapped(view.help_line, policy.width, policy, "muted")
 
 
-def _question_line(q: QuestionLine, policy: TerminalPolicy) -> str:
+def _question_line(q: QuestionLine, policy: TerminalPolicy) -> Line:
     """One question line. With the link off it is ``text`` clipped as in R2; with it on the
-    age, the bracketed state and ``reason unknown`` stay and only the question text is cut."""
+    age, the bracketed state and ``reason unknown`` stay and only the question text is cut.
+
+    The age is ``attention``, the subject ``body_bold`` and the reason tail ``muted``; the
+    selected question is one ``selected`` line."""
     width = policy.width
     if not q.link:
-        return clip(q.text, width, policy)
+        text = clip(q.text, width, policy)
+        split = text.find("  ")
+        tail = text.rfind("  " + QUESTIONS_REASON)
+        if split <= 0:
+            return seg(text, "body_bold")
+        if tail > split:
+            return join(
+                seg(text[:split], "attention"),
+                seg(text[split:tail], "body_bold"),
+                seg(text[tail:], "muted"),
+            )
+        return join(seg(text[:split], "attention"), seg(text[split:], "body_bold"))
     mark = glyph("selected", policy) + " " if q.selected else "  "
     head = ascii_safe(mark + q.lead + "  ") if policy.ascii else mark + q.lead + "  "
     tail = "  " + QUESTIONS_REASON
@@ -386,18 +509,31 @@ def _question_line(q: QuestionLine, policy: TerminalPolicy) -> str:
         cell_len(text) > room and room > 3
     ):  # a cut question text ends in a visible "..."
         text = text[: _prefix_length(text, room - 3)] + "..."
-    return clip(head + clip(text, room, policy) + tail, width, policy)
+    shown = clip(text, room, policy)
+    if q.selected:
+        return seg(clip(head + shown + tail, width, policy), "selected")
+    lead = ascii_safe(q.lead) if policy.ascii else q.lead
+    marker = head[: len(head) - len(lead) - 2]
+    line = join(
+        seg(marker),
+        seg(lead, "attention"),
+        seg("  "),
+        seg(shown, "body_bold"),
+        seg(tail, "muted"),
+    )
+    return line.clipped(width, policy)
 
 
-def _desk_lines(desk: DeskView, policy: TerminalPolicy) -> list[str]:
+def _desk_lines(desk: DeskView, policy: TerminalPolicy) -> list[Line]:
     """The Decision Desk block: title, id and age, the question text (at most 4 lines, cut
     with ``...``), the linked session fields, then each note. Everything wraps; nothing is cut."""
     width = policy.width
-    lines = wrap(DESK_TITLE, width, policy)
-    lines += wrap(
+    lines = _wrapped(DESK_TITLE, width, policy, "attention_title")
+    lines += _wrapped(
         f"{desk.qid}  age {desk.age_text}" if desk.age_text else desk.qid,
         width,
         policy,
+        "attention",
     )
     if desk.ask:
         text = wrap(desk.ask, width, policy)
@@ -406,16 +542,16 @@ def _desk_lines(desk: DeskView, policy: TerminalPolicy) -> list[str]:
             text = text[: DESK_TEXT_LINES - 1] + [
                 last[: _prefix_length(last, max(width - 3, 1))] + "..."
             ]
-        lines += text
+        lines += _roled(text, "attention")
     for label, value in desk.session_fields:
-        first, *rest = wrap(f"{label}: {value}", width, policy)
-        lines.append(first)
-        for continuation in rest:  # continuation lines are indented two cells
-            lines += [
-                "  " + part for part in wrap(continuation, max(width - 2, 1), policy)
-            ]
+        role = (
+            STATE_ROLE.get((label, value))
+            or STATE_ROLE.get((label, value.split(" (")[0]))
+            or _absent_role(value)
+        )
+        lines += _labelled(label, value, width, policy, role)
     for note in desk.notes:
-        lines += wrap(note, width, policy)
+        lines += _wrapped(note, width, policy, "muted")
     return lines
 
 
@@ -423,31 +559,31 @@ def _panel_lines(
     panel: QuestionsPanel,
     policy: TerminalPolicy,
     capacity: int | None,
-    desk: list[str] | None = None,
-) -> list[str]:
+    desk: list[Line] | None = None,
+) -> list[Line]:
     """The coordinator-questions block: header lines, up to ``capacity`` questions, then the
     desk block (when given), notes."""
     width = policy.width
-    lines = wrap(panel.title, width, policy)
-    lines += wrap(panel.run_line, width, policy)
+    lines = _wrapped(panel.title, width, policy, "attention_title")
+    lines += _wrapped(panel.run_line, width, policy, "muted")
     for state_line in panel.state_lines:  # the state of the read comes first
-        lines += wrap(state_line, width, policy)
-    lines += wrap(panel.disclosure, width, policy)
-    lines += wrap(panel.counts_line, width, policy)
-    lines += wrap(panel.caveat_line, width, policy)
+        lines += _wrapped(state_line, width, policy, "muted")
+    lines += _wrapped(panel.disclosure, width, policy, "muted")
+    lines += _wrapped(panel.counts_line, width, policy, "identity")
+    lines += _wrapped(panel.caveat_line, width, policy, "muted")
     shown, cut = panel.window(capacity)
     lines += [_question_line(q, policy) for q in shown]
     if cut:
-        lines += wrap(cut, width, policy)
+        lines += _wrapped(cut, width, policy, "muted")
     if any(q.selected for q in panel.lines) and not any(q.selected for q in shown):
-        lines += wrap(
-            DESK_SELECTED_HIDDEN, width, policy
+        lines += _wrapped(
+            DESK_SELECTED_HIDDEN, width, policy, "muted"
         )  # the owner's oldest-first window
     lines += desk or []
     for text in (panel.empty_text, panel.window_full_text, *panel.notes):
         if text:
-            lines += wrap(text, width, policy)
-    return lines + wrap(panel.retention_line, width, policy)
+            lines += _wrapped(text, width, policy, "muted")
+    return lines + _wrapped(panel.retention_line, width, policy, "muted")
 
 
 def screen_lines(
@@ -464,37 +600,31 @@ def _compose(
     view: View, policy: TerminalPolicy, message: str | None = None
 ) -> list[Line]:
     """The screen as ``Line`` objects: the plain text of ``screen_lines`` plus colour roles."""
-    return [Line(text) for text in _screen_strings(view, policy, message)]
-
-
-def _screen_strings(
-    view: View, policy: TerminalPolicy, message: str | None = None
-) -> list[str]:
     width = policy.width
     if (
         policy.too_narrow
     ):  # below 80 columns: the denominators and the gap notice still print
-        lines = wrap(TOO_NARROW_TEXT, width, policy)
-        lines += counts_lines(view.counts_tokens, policy, max_lines=None)
-        return lines + wrap(view.gap_notice, width, policy)
+        lines = _wrapped(TOO_NARROW_TEXT, width, policy, "attention")
+        lines += counts_line_objects(view.counts_tokens, policy, max_lines=None)
+        return lines + _wrapped(view.gap_notice, width, policy, "muted")
     if policy.too_small:
-        lines = wrap(TOO_SMALL_TEXT, width, policy)
-        lines += wrap(view.collected_text, width, policy)
-        return lines + wrap(view.gap_notice, width, policy)
-
-    head: list[str] = []
-    head += wrap(view.header1, width, policy)
-    head += wrap(view.header2, width, policy)
-    head += counts_lines(view.counts_tokens, policy)
+        lines = _wrapped(TOO_SMALL_TEXT, width, policy, "attention")
+        lines += _wrapped(view.collected_text, width, policy, "muted")
+        return lines + _wrapped(view.gap_notice, width, policy, "muted")
+
+    head: list[Line] = []
+    head += _wrapped(view.header1, width, policy, "title")
+    head += _wrapped(view.header2, width, policy, "muted")
+    head += counts_line_objects(view.counts_tokens, policy)
     if view.changes_line:
-        head += wrap(view.changes_line, width, policy)
-    tail: list[str] = []
+        head += _wrapped(view.changes_line, width, policy, "muted")
+    tail: list[Line] = []
     for note in _notes(view):
-        tail += wrap(note, width, policy)
+        tail += _wrapped(note, width, policy, "muted")
     if view.focus == "filter":
-        tail += wrap("/" + view.filter_text, width, policy)
+        tail += _wrapped("/" + view.filter_text, width, policy, "body")
     if message:
-        tail += wrap(message, width, policy)
+        tail += _wrapped(message, width, policy, "muted")
 
     # The footer is one line when it fits, else the key list and the counts on two lines.
     window_probe = view.window(None)
@@ -532,9 +662,9 @@ def _screen_strings(
             + selected_note
         )
         desk = _desk_lines(view.desk, policy) if view.desk is not None else None
-        notice = wrap(DESK_HIDDEN, width, policy)
+        notice = _wrapped(DESK_HIDDEN, width, policy, "muted")
         if desk is None:
-            panel_part: list[str] | None = (
+            panel_part: list[Line] | None = (
                 _panel_lines(panel, policy, spare) if spare >= 1 else None
             )
         elif spare - len(desk) >= 1:  # the desk is sized first; the list keeps a line
@@ -550,25 +680,27 @@ def _screen_strings(
         elif (
             desk is not None
         ):  # no room for the panel: the summary names the hidden desk
-            gap_part = wrap(f"{view.gap_notice}; {DESK_HIDDEN}", width, policy)
+            gap_part = _wrapped(
+                f"{view.gap_notice}; {DESK_HIDDEN}", width, policy, "muted"
+            )
         else:  # no room for the panel: its one-line summary stands in for it
-            gap_part = wrap(view.gap_notice, width, policy)
+            gap_part = _wrapped(view.gap_notice, width, policy, "muted")
     else:
-        gap_part = wrap(view.gap_notice, width, policy)
+        gap_part = _wrapped(view.gap_notice, width, policy, "muted")
         if (
             panel is not None and not panel.replaces_gap
         ):  # questions on, nothing read yet
-            gap_part += wrap(panel.summary, width, policy)
+            gap_part += _wrapped(panel.summary, width, policy, "muted")
     top = head + gap_part + tail
 
     if view.focus == "inspector" and view.inspector is not None:
-        footer_lines = [clip(INSPECTOR_HELP, width, policy)]
+        footer_lines = [seg(clip(INSPECTOR_HELP, width, policy), "muted")]
         body = _inspector_lines(
             view, policy, max(policy.height - len(top) - len(footer_lines), 1)
         )
         return top + body + footer_lines
 
-    body = wrap(view.ledger_title, width, policy)
+    body = _wrapped(view.ledger_title, width, policy, "secondary")
     columns, getters = _columns(policy)
     if policy.width_class == "full" and view.visible_rows:
         body += _header_lines(columns, policy)
@@ -579,20 +711,22 @@ def _screen_strings(
     window = view.window(capacity)
     if not view.all_rows:
         for text in view.ledger_empty:
-            body += wrap(text, width, policy)
+            body += _wrapped(text, width, policy, "muted")
     elif not window.rows:
-        body += wrap(NO_MATCH_TEXT, width, policy)
+        body += _wrapped(NO_MATCH_TEXT, width, policy, "muted")
     for row in window.rows:
-        body.append(_row_line(row, columns, getters, policy))
+        body.append(_row_segments(row, columns, getters, policy))
     if window.more:
-        body += wrap(f"{window.text}  {window.more_text}", width, policy)
+        body += _wrapped(f"{window.text}  {window.more_text}", width, policy, "muted")
 
     footer = view.footer(window)
     if cell_len(footer) <= width:
-        footer_lines = [footer if not policy.ascii else ascii_safe(footer)]
+        footer_lines = [
+            seg(footer if not policy.ascii else ascii_safe(footer), "muted")
+        ]
     else:
-        footer_lines = _help_lines(view, policy) + wrap(
-            view.footer_counts(window), width, policy
+        footer_lines = _help_lines(view, policy) + _wrapped(
+            view.footer_counts(window), width, policy, "muted"
         )
     return top + body + footer_lines
 
diff --git a/tests/observe/release1_surface.py b/tests/observe/release1_surface.py
index d2d089355..cfbda46c8 100644
--- a/tests/observe/release1_surface.py
+++ b/tests/observe/release1_surface.py
@@ -20,7 +20,7 @@ from superclaude.cli.observe.export import record_text, snapshot_json
 from superclaude.cli.observe.render import render, screen_lines
 from superclaude.cli.observe.terminal import make_console, resolve_policy
 from superclaude.cli.observe.view import Session, build_view
-from tests.observe.conftest import FakeClock
+from tests.observe.conftest import FakeClock, strip_sgr
 
 VARIANTS = ("base", "empty", "source-loss", "injection", "missing-fields")
 WIDTHS = (160, 116, 80)
@@ -32,10 +32,12 @@ def _policy(width: int, height: int):
 
 
 def _printed(view, policy) -> str:
+    """The printed text with SGR removed: release 1 wrote none, so the strip changes nothing
+    there, and a golden never holds styled bytes."""
     buffer = io.StringIO()
     console: Console = make_console(policy, file=buffer, record=True)
     console.print(render(view, policy))
-    return buffer.getvalue()
+    return strip_sgr(buffer.getvalue())
 
 
 def surface() -> dict:
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 6b213407e..443021841 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -73,7 +73,7 @@ def test_every_line_fits_the_width_for_the_base_variant(fake_clock, width):
         assert all(cell_len(line) <= width for line in lines), [
             l for l in lines if cell_len(l) > width
         ]
-        out = printed(view, policy)
+        out = strip_sgr(printed(view, policy))
         assert all(cell_len(line) <= width for line in out.splitlines())
 
 
@@ -252,8 +252,10 @@ def test_rendering_twice_is_byte_identical_and_no_color_changes_no_text(
 ):
     view = fixture_view("base", fake_clock, Session(show_historical=True))
     colour = policy_for(width)
+    nocolor = printed(view, policy_for(width, no_color=True))
     assert printed(view, colour) == printed(view, colour)
-    assert printed(view, colour) == printed(view, policy_for(width, no_color=True))
+    assert strip_sgr(printed(view, colour)) == nocolor  # colour adds no text
+    assert "\x1b" in printed(view, colour) and "\x1b" not in nocolor
     assert screen_lines(view, colour) == screen_lines(
         view, policy_for(width, no_color=True)
     )
@@ -1179,3 +1181,73 @@ def test_render_colours_a_span_only_when_the_policy_has_a_colour_depth(
     plain = printed(view, policy_for(80, no_color=True))
     assert "\x1b[" in coloured and strip_sgr(coloured) == plain == "hello world\n"
     assert "\x1b" not in plain
+
+
+# -- roles assigned at the builders (no text change) ------------------------------------------------------
+
+from superclaude.cli.observe.render import (  # noqa: E402
+    _columns,
+    _compose,
+    _row_segments,
+)
+from superclaude.cli.observe.view import FROZEN_MARKER  # noqa: E402
+
+
+def roles_at(line, needle):
+    """The roles covering the first character of ``needle`` in ``line.plain``."""
+    index = line.plain.index(needle)
+    return {s.role for s in line.spans if s.start <= index < s.end}
+
+
+def first_line(lines, needle):
+    return next(ln for ln in lines if needle in ln.plain)
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_colour_never_changes_the_text_of_a_questions_screen(fake_clock, width):
+    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
+    _, view = r3_screen(fake_clock, rows, 1, width, height=60)
+    coloured = printed(view, policy_for(width, height=60))
+    plain = printed(view, policy_for(width, height=60, no_color=True))
+    assert "\x1b" in coloured and strip_sgr(coloured) == plain
+
+
+def test_a_selected_question_is_one_bold_amber_line_and_the_others_have_parts(
+    fake_clock,
+):
+    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
+    _, view = r3_screen(fake_clock, rows, 1, 160, height=60)
+    lines = _compose(view, policy_for(160, height=60))
+    selected = next(ln for ln in lines if ln.plain.startswith("▸ "))
+    assert {s.role for s in selected.spans} == {"selected"}
+    other = first_line(lines, "first?")
+    assert roles_at(other, "first?") == {"body_bold"}
+    assert roles_at(other, "reason unknown") == {"muted"}
+    assert roles_at(other, other.plain.strip().split()[0]) == {"attention"}  # the age
+
+
+def test_absent_values_are_muted_and_state_words_follow_the_table(fake_clock):
+    view = fixture_view("missing-fields", fake_clock)
+    lines = _compose(view, policy_for(160, height=60))
+    absent = first_line(lines, "unknown (unknown)")
+    assert roles_at(absent, "unknown (unknown)") == {"muted"}  # the bare verdict
+    assert any(
+        roles_at(ln, "running") == {"state_running"}
+        for ln in lines
+        if " running " in ln.plain
+    )
+    blocked = first_line(
+        lines, " blocked "
+    )  # not in the table: body, never a state role
+    assert roles_at(blocked, "blocked") == {"body"}
+
+
+def test_a_frozen_flag_cell_takes_the_frozen_role(fake_clock):
+    view = fixture_view("base", fake_clock)
+    policy = policy_for(160)
+    columns, getters = _columns(policy)
+    row = dataclasses.replace(
+        view.window(1).rows[0], flags=(FROZEN_MARKER,), frozen=True
+    )
+    line = _row_segments(row, columns, getters, policy)
+    assert roles_at(line, FROZEN_MARKER) == {"state_frozen"}
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
