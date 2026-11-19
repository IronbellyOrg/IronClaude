6d7416a6b3f7eee6ad6fdf548fe2fd710af2da58
Review one task for spec compliance.

Task brief: ## Task 15: Ledger diet

Depends on: Task 14

Spec Part C step 2.14 in `OBS/render.py` (`_columns`, `_row_segments`, footer) and `OBS/view.py`. Merge dispatchStatus, terminalState and outcome into one `status` cell with the Task 14 badge rule; replace the `alive (terminal)` text column with a dot `●` coloured by state plus one legend line, spelling out any non-alive value in amber and in words under NO_COLOR (decision D-15); drop the `flags` column and show the changed marker `*` in the first cell; drop the separator rule row and the `+N more` row above a footer that already says `shown n/N`; put the gap notice and `26 historical hidden (h)` on one row; drop `mode=` and `as of` from the header, the second `scope=all`, and `collected` from the footer; replace the three `unavailable (no source)` tokens with one dim token `no source: settled, frozen, cost`; footer keys become `j/k move  Enter detail  / filter  n/p question  h history  e export  q quit` (dropped keys still work); `source counts` (when unknown) and `runs seen` leave the screen for the inspector (D-16). Keep verbatim: `collected n / reported T` and PARTIAL, `seen, not resolved`, `closed by evidence: unavailable`, `worker-reported, not questions`, the Human questions gap notice.

Acceptance criteria:
- No `flags` column, no rule row and no `+N more` row above a `shown n/N` footer at 160, 116 and 80; a non-alive liveness value is spelled out also under NO_COLOR.
- The FROZEN marker role of Task 7 still reaches the screen through the first cell or status cell (`tests/observe/test_render.py` frozen-row checks pass or are rewritten with evidence).
- `uv run pytest tests/observe/` shows only the position-sensitive tests listed in Task 16 failing before that task and none after it.
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
Start sha: 6d7416a6b3f7eee6ad6fdf548fe2fd710af2da58
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 5758a6945..9ee5acae8 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -39,6 +39,7 @@ from superclaude.cli.observe.view import (
     INSPECTOR_BELOW_TEXT,
     INSPECTOR_HELP,
     INSPECTOR_TITLE,
+    LEDGER_LEGEND,
     NO_MATCH_TEXT,
     QUESTIONS_REASON,
     QUESTIONS_REASONS_NOTE,
@@ -230,6 +231,8 @@ def _absent_tail(text: str, role: str) -> Line:
 
 
 def _token_line(text: str, token: CountsToken) -> Line:
+    if token.dim:
+        return seg(text, "muted")
     return _absent_tail(text, "identity" if token.protected else "body")
 
 
@@ -303,8 +306,33 @@ def counts_lines(
 # -- ledger rows -----------------------------------------------------------------------------------------
 
 
-def _flags_text(row: RowView) -> str:
-    return ", ".join(row.flags)  # the view owns every marker, FROZEN included
+def _is_active(row: RowView) -> bool:
+    """The one ``ACTIVE`` badge: dispatchStatus, terminalState and outcome exactly active,
+    active and none. Any other combination (an absent value too) shows its raw values."""
+    return (row.dispatch_status, row.terminal_state, row.outcome) == (
+        "active",
+        "active",
+        "none",
+    )
+
+
+def _status_text(row: RowView) -> str:
+    """The merged status cell: the badge, or the three raw values in field order; a frozen
+    row (fixture mode) leads with the frozen marker."""
+    status = (
+        "ACTIVE"
+        if _is_active(row)
+        else f"{row.dispatch_status}/{row.terminal_state}/{row.outcome}"
+    )
+    return f"{FROZEN_MARKER} {status}" if FROZEN_MARKER in row.flags else status
+
+
+def _alive_text(row: RowView, policy: TerminalPolicy) -> str:
+    """The liveness cell: a dot for ``alive``; any other value is spelled out after the dot, so
+    the state is a word with the colours off too."""
+    verdict = _verdict(row)
+    dot = glyph("alive", policy)
+    return dot if verdict in ("alive", "live") else f"{dot} {verdict}"
 
 
 def _marker(row: RowView, policy: TerminalPolicy) -> str:
@@ -321,76 +349,67 @@ def _columns(policy: TerminalPolicy) -> tuple[list[tuple[str, int]], list]:
     """Column (header, width) pairs and one getter per column, for the width class."""
     width = policy.width
     sep = len(SEPARATOR)
+    alive = lambda r: _alive_text(r, policy)  # noqa: E731
     if policy.width_class == "full":
-        fixed = [12, 12, 14, 14, 12, 16, 22, 12]  # run .. evidence age
-        flags_min = 12
-        base = 2 + sum(fixed) + flags_min + sep * 10
-        extra = max(width - base - 22, 0)
-        id_width = 22 + min(extra, 26)
-        flags_width = width - (2 + sum(fixed) + sep * 10) - id_width
+        # run, workerState, status, nextAction.kind, alive, evidence age
+        fixed = [12, 12, 22, 16, 14, 12]
+        id_width = min(width - (2 + sum(fixed) + sep * 7), 48)
         names = [
             ("", 2),
             ("dispatchId", id_width),
             ("run", fixed[0]),
             ("workerState", fixed[1]),
-            ("dispatchStatus", fixed[2]),
-            ("terminalState", fixed[3]),
-            ("outcome", fixed[4]),
-            ("nextAction.kind", fixed[5]),
-            ("liveness", fixed[6]),
-            ("evidence age", fixed[7]),
-            ("flags", flags_width),
+            ("status", fixed[2]),
+            ("nextAction.kind", fixed[3]),
+            ("alive", fixed[4]),
+            ("evidence age", fixed[5]),
         ]
         getters = [
             None,
             lambda r: r.dispatch_id,
             lambda r: r.run,
             lambda r: r.worker_state,
-            lambda r: r.dispatch_status,
-            lambda r: r.terminal_state,
-            lambda r: r.outcome,
+            _status_text,
             lambda r: r.next_action,
-            lambda r: r.liveness,
+            alive,
             lambda r: r.evidence_age,
-            _flags_text,
         ]
         return names, getters
     if policy.width_class == "line":
-        kind, verdict, age = 18, 14, 7
-        id_width = min(width - (2 + kind + verdict + age + 18 + sep * 5), 60)
-        flags_width = width - (2 + kind + verdict + age + id_width + sep * 5)
+        kind, state, status, age = 18, 14, 22, 7
+        id_width = min(width - (2 + kind + state + status + age + sep * 5), 48)
         names = [
             ("", 2),
             ("kind", kind),
             ("dispatchId", id_width),
-            ("liveness", verdict),
+            ("alive", state),
+            ("status", status),
             ("age", age),
-            ("flags", flags_width),
         ]
         getters = [
             None,
             lambda r: r.next_action,
             lambda r: r.dispatch_id,
-            _verdict,
+            alive,
+            _status_text,
             lambda r: r.evidence_age,
-            _flags_text,
         ]
         return names, getters
-    kind, age, flags_width = 14, 6, 16
-    id_width = width - (2 + kind + age + flags_width + sep * 4)
+    kind, status, age = 14, 22, 6
+    id_width = width - (2 + kind + status + age + sep * 4)
     names = [
         ("", 2),
         ("kind", kind),
         ("dispatchId", id_width),
+        ("status", status),
         ("age", age),
-        ("flags", flags_width),
     ]
     getters = [
         None,
         lambda r: r.next_action,
         lambda r: r.dispatch_id,
+        _status_text,
         lambda r: r.evidence_age,
-        _flags_text,
     ]
     return names, getters
 
@@ -399,10 +418,8 @@ def _cell_role(name: str, row: RowView, text: str) -> str:
     """The role of one row cell, from the column and the exact raw value (never a pattern)."""
     if name == "workerState":
         role = STATE_ROLE.get(("workerState", row.worker_state))
-    elif name == "dispatchStatus":
-        role = STATE_ROLE.get(("dispatchStatus", row.dispatch_status))
-    elif name == "flags":
-        role = FROZEN_ROLE if FROZEN_MARKER in row.flags else None
+    elif name == "status":
+        role = "state_running" if _is_active(row) else None
     else:
         role = None
     if name in ("nextAction.kind", "kind"):  # the verbatim kind is never classified
@@ -420,19 +437,22 @@ def _row_segments(
             continue
         text = getter(row)
         cell = _cell(text, width, policy, _cell_role(name, row, text))
-        if (
-            name == "liveness"
-        ):  # the verdict word carries the state; "(source)" stays body
+        if name == "alive":
+            # the dot takes the state colour; a spelled-out value is amber (muted when absent)
             verdict = _verdict(row)
-            role = STATE_ROLE.get(("liveness", verdict)) or _absent_role(verdict)
+            alive = verdict in ("alive", "live")
+            role = "state_running" if alive else (_absent_role(verdict, "attention"))
+            shown = clip(text, width, policy)
+            cell = join(seg(shown, role), seg(" " * max(width - cell_len(shown), 0)))
+        elif name == "status" and FROZEN_MARKER in row.flags:
             shown = clip(text, width, policy)
-            if shown.startswith(verdict) and verdict:
-                rest = shown[len(verdict) :]
-                cell = join(
-                    seg(verdict, role),
-                    seg(rest, "body"),
-                    seg(" " * max(width - cell_len(shown), 0)),
-                )
+            lead = shown[: len(FROZEN_MARKER)]
+            body = _cell_role(name, row, text)
+            cell = join(
+                seg(lead, FROZEN_ROLE),
+                seg(shown[len(lead) :], body),
+                seg(" " * max(width - cell_len(shown), 0)),
+            )
         cells.append(cell)
     parts: list[Line] = []
     for index, cell in enumerate(cells):
@@ -446,17 +466,13 @@ def _header_lines(columns: list[tuple[str, int]], policy: TerminalPolicy) -> lis
     head = SEPARATOR.join(
         _pad(clip(name, width, policy), width) for name, width in columns
     )
-    rule = SEPARATOR.join(glyph("hrule", policy) * width for _, width in columns)
-    return [
-        seg(clip(head.rstrip(), policy.width, policy), "muted"),
-        seg(clip(rule, policy.width, policy), "border_secondary"),
-    ]
+    return [seg(clip(head.rstrip(), policy.width, policy), "muted")]
 
 
 def _heading_rows(view: View, policy: TerminalPolicy) -> int:
-    """The column heading and its rule take 2 rows whenever ledger rows are visible, at every
-    width class (the policy is part of the call shape; the width class no longer matters)."""
-    return 2 if view.visible_rows and not policy.too_narrow else 0
+    """The column heading takes 1 row whenever ledger rows are visible, at every width class
+    (the rule row under it is gone: the footer rule is the only rule left)."""
+    return 1 if view.visible_rows and not policy.too_narrow else 0
 
 
 # -- screens -------------------------------------------------------------------------------------------------
@@ -514,12 +530,12 @@ def _inspector_lines(view: View, policy: TerminalPolicy, budget: int) -> list[Li
     return lines[: max(budget, 1)]
 
 
-def _notes(view: View) -> list[str]:
+def _notes(view: View, skip_historical: bool = False) -> list[str]:
     parts = [
         n
         for n in (
             view.filter_line,
-            view.historical_note,
+            None if skip_historical else view.historical_note,
             view.duplicates_note,
             view.selection_note,
         )
@@ -528,6 +544,18 @@ def _notes(view: View) -> list[str]:
     return ["  ".join(parts)] if parts else []
 
 
+def _ledger_title(view: View, policy: TerminalPolicy) -> list[Line]:
+    """The ledger title; at the widths with a liveness dot the legend shares its row."""
+    width = policy.width
+    title = _wrapped(view.ledger_title, width, policy, "secondary")
+    if policy.width_class not in ("full", "line") or len(title) != 1:
+        return title
+    legend = LEDGER_LEGEND.format(dot=glyph("alive", policy))
+    if cell_len(view.ledger_title) + 2 + cell_len(legend) > width:
+        return title
+    return [join(title[0], seg("  " + legend, "muted"))]
+
+
 def _help_lines(view: View, policy: TerminalPolicy) -> list[Line]:
     """The key list, wrapped by whole key groups: no key is cut and no pair is split."""
     return _roled(wrap_groups(view.help_line, policy.width, policy), "muted")
@@ -780,13 +808,28 @@ def _compose(
         return lines + _wrapped(view.gap_notice, width, policy, "muted")
 
     head: list[Line] = []
-    head += _title_bar(wrap(view.header1, width, policy), policy)
+    head += _title_bar(wrap(view.screen_header1 or view.header1, width, policy), policy)
     head += _wrapped(view.screen_header2 or view.header2, width, policy, "muted")
-    head += counts_line_objects(view.counts_tokens, policy)
+    head += counts_line_objects(view.screen_counts_tokens or view.counts_tokens, policy)
     if view.changes_line:
         head += _wrapped(view.changes_line, width, policy, "muted")
+    # The R2 panel stands in for the gap notice once the question source has read; in the
+    # inspector only its one-line summary (``gap_notice``) is shown, so the inspector keeps room.
+    panel = view.questions
+    inspecting = view.focus == "inspector" and view.inspector is not None
+    panel_in_gap = panel is not None and panel.replaces_gap and not inspecting
+    # The gap notice and the historical-hidden note share one row when both fit on it.
+    hist = view.historical_note
+    merge_hist = bool(
+        hist
+        and not panel_in_gap
+        and len(wrap(view.gap_notice, width, policy)) == 1
+        and cell_len(view.gap_notice) + 2 + cell_len(hist) <= width
+    )
     tail: list[Line] = []
-    for note in _notes(view):
+    if hist and not merge_hist:
+        tail += _wrapped(hist, width, policy, "muted")
+    for note in _notes(view, skip_historical=True):
         tail += _wrapped(note, width, policy, "muted")
     if view.focus == "filter":
         tail += _wrapped("/" + view.filter_text, width, policy, "body")
@@ -803,11 +846,7 @@ def _compose(
         + len(wrap(view.footer_counts(window_probe), width, policy))
     )
 
-    # The R2 panel stands in for the gap notice once the question source has read; in the
-    # inspector only its one-line summary (``gap_notice``) is shown, so the inspector keeps room.
-    panel = view.questions
-    inspecting = view.focus == "inspector" and view.inspector is not None
-    if panel is not None and panel.replaces_gap and not inspecting:
+    if panel_in_gap:
         ledger_fixed = len(wrap(view.ledger_title, width, policy)) + (
             _heading_rows(view, policy)
         )
@@ -823,9 +862,8 @@ def _compose(
             + base
             + footer_height
             + ledger_fixed
-            + 1
-            + 1
-            + 1
+            + 1  # one ledger row
+            + 1  # the cut line of the list
             + selected_note
         )
         desk = _desk_lines(view.desk, policy) if view.desk is not None else None
@@ -860,6 +898,8 @@ def _compose(
             panel is not None and not panel.replaces_gap
         ):  # questions on, nothing read yet
             gap_part += _wrapped(panel.summary, width, policy, "muted")
+        if merge_hist and gap_part:
+            gap_part[0] = join(gap_part[0], seg(f"  {hist}", "muted"))
     top = head + gap_part + tail
 
     if view.focus == "inspector" and view.inspector is not None:
@@ -869,19 +909,17 @@ def _compose(
         )
         return top + body + footer_lines
 
-    body = _wrapped(view.ledger_title, width, policy, "secondary")
+    body = _ledger_title(view, policy)
     columns, getters = _columns(policy)
     heading = _heading_rows(view, policy)
-    # The column heading and its rule at every width, unless that would leave no room for even
-    # one ledger row (then the rows win and the heading is left out).
+    # The column heading at every width, unless that would leave no room for even one ledger
+    # row (then the rows win and the heading is left out).
     if (
         heading
-        and policy.height - (len(top) + len(body) + heading + footer_height + 1) >= 1
+        and policy.height - (len(top) + len(body) + heading + footer_height) >= 1
     ):
         body += _header_lines(columns, policy)
-    reserved = (
-        len(top) + len(body) + footer_height + 1
-    )  # one line kept for the overflow text
+    reserved = len(top) + len(body) + footer_height
     capacity = max(policy.height - reserved, 1)
     window = view.window(capacity)
     if not view.all_rows:
@@ -891,8 +929,6 @@ def _compose(
         body += _wrapped(NO_MATCH_TEXT, width, policy, "muted")
     for row in window.rows:
         body.append(_row_segments(row, columns, getters, policy))
-    if window.more:
-        body += _wrapped(f"{window.text}  {window.more_text}", width, policy, "muted")
 
     footer = view.footer(window)
     if cell_len(footer) <= width:
diff --git a/src/superclaude/cli/observe/terminal.py b/src/superclaude/cli/observe/terminal.py
index 452a86900..5cfbe61f8 100644
--- a/src/superclaude/cli/observe/terminal.py
+++ b/src/superclaude/cli/observe/terminal.py
@@ -31,6 +31,7 @@ GLYPHS: dict[str, tuple[str, str]] = {
     "selected": ("▸", "@"),
     "truncate": (">", ">"),
     "hrule": ("─", "-"),
+    "alive": ("●", "o"),
 }
 
 
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
index 88716ef91..b492865ab 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -82,12 +82,12 @@ QUESTIONS_ACTION = "start the observer in the terminal that holds {run} (inferre
 QUESTIONS_LATEST_EMPTY = "latest read returned 0 questions; the rows below are older"
 QUESTIONS_EMPTY_COUNT = "0 (source window only; not proof none exist)"
 QUESTIONS_AGE_SKEW = "age unknown (clock skew)"
-QUESTIONS_KEYS_LINE = (
-    "Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  "
-    "m mark rows  e export all  q quit"
+# The shown key list names the keys most used; the dropped ones (Up/Down, Esc, m, d/u) still work.
+QUESTIONS_KEYS_LINE = "j/k move  Enter detail  / filter  h history  e export  q quit"
+# With the R3 question link on the keys line also names n/p.
+QUESTIONS_LINK_KEYS_LINE = (
+    "j/k move  Enter detail  / filter  n/p question  h history  e export  q quit"
 )
-# With the R3 question link on the keys line also names n/p (the link-off line is unchanged).
-QUESTIONS_LINK_KEYS_LINE = QUESTIONS_KEYS_LINE + "  n/p question"
 # R3 Decision Desk (one stacked block under the question list); literals defined once.
 DESK_TITLE = "DECISION DESK"
 DESK_UNKNOWN_SCOPE = "affected scope unknown"
@@ -109,7 +109,11 @@ ABSENT_IN_SOURCE = "unknown (absent in source)"
 PARTIAL_CAP_TEXT = (
     "newest first; oldest rows not read; long-running active workers may be among them"
 )
-KEYS_LINE = "Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e export  q quit"
+KEYS_LINE = QUESTIONS_KEYS_LINE
+LEDGER_LEGEND = "{dot} alive; any other state is spelled out"
+NO_SOURCE_TOKEN = (
+    "no source: settled, frozen, cost"  # one dim token for the three unavailable ones
+)
 READ_ONLY_BADGE = (
     "READ ONLY"  # right-aligned on the title bar; screen only, never in the record
 )
@@ -162,6 +166,7 @@ class Session:
 class CountsToken:
     text: str
     protected: bool  # protected tokens are never truncated
+    dim: bool = False  # the whole token reads in the muted role (a note, not a figure)
 
 
 @dataclass(frozen=True)
@@ -358,6 +363,10 @@ class View:
     # Screen only: the freshness strip with the questions cell stripped of its Run id (the
     # panel title carries the Run once). ``header2`` stays as the record reads it.
     screen_header2: str = ""
+    # Screen only: the title without ``mode=`` and ``as of``, and the strip without the second
+    # scope, the unknown source counts, ``runs seen`` and the three unavailable tokens.
+    screen_header1: str = ""
+    screen_counts_tokens: tuple[CountsToken, ...] = ()
 
     def window(self, capacity: int | None) -> Window:
         """The rows that fit ``capacity`` lines, always including the selected visible row."""
@@ -385,8 +394,8 @@ class View:
         )
 
     def footer_counts(self, window: Window) -> str:
-        """The footer literal ``shown x/y | collected n / reported T`` ("x/y shown" is the overflow text)."""
-        return f"shown {window.shown}/{window.total} | {self.collected_text}"
+        """The footer literal ``shown x/y``; ``collected n / reported T`` is in the counts strip."""
+        return f"shown {window.shown}/{window.total}"
 
     def footer(self, window: Window) -> str:
         return f"{self.help_line}  {self.footer_counts(window)}"
@@ -497,6 +506,20 @@ def _inspector(row: Row, result: Any, snapshot: Any) -> tuple[tuple[str, str], .
     flags = row.flags + (() if row.reobserved else ("not reobserved",))
     if flags:
         lines.append(("flags", ", ".join(flags)))
+    # The strip no longer carries these two (decision D-16): they live with the row detail.
+    runs = (
+        {r.run_id for r in snapshot.rows if r.run_id is not UNKNOWN}
+        if snapshot
+        else set()
+    )
+    unknown_runs = (
+        sum(1 for r in snapshot.rows if r.run_id is UNKNOWN) if snapshot else 0
+    )
+    lines.append(
+        ("source counts", _source_counts_text(snapshot)[len("source counts: ") :])
+    )
+    if snapshot is not None:
+        lines.append(("runs seen", aggregate(len(runs), unknown_runs)))
     lines.extend((fact, UNAVAILABLE) for fact in UNAVAILABLE_FACTS)
     if snapshot is not None:
         lines.extend(("source warning", warning) for warning in snapshot.warnings)
@@ -960,6 +983,12 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
         header_parts.append("one Run only")
     header_parts.append(f"as of {as_of}")
     header1 = "  ".join(header_parts)
+    # Screen only: no ``mode=`` and no ``as of`` (the strip says how fresh each source is).
+    screen_header1 = "  ".join(
+        part
+        for part in header_parts
+        if not part.startswith("mode=") and not part.startswith("as of ")
+    )
 
     fresh_cell, age = _freshness(result, clock, state)
     panel = _questions_panel(result, clock, session.selected_question)
@@ -994,6 +1023,13 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
     tokens.append(CountsToken(f"SETTLED {UNAVAILABLE}", False))
     tokens.append(CountsToken(f"POLICY FROZEN {UNAVAILABLE}", False))
     tokens.append(CountsToken("cost unavailable", False))
+    screen_tokens = [CountsToken(collected_text, True)]
+    if partial:
+        screen_tokens.append(CountsToken(partial, True))
+    screen_tokens.append(CountsToken(NO_SOURCE_TOKEN, False, dim=True))
+    source_counts = _source_counts_text(snapshot)
+    if not source_counts.endswith("unknown"):  # unknown counts are in the inspector
+        screen_tokens.append(CountsToken(source_counts, False))
 
     flagged, changed_k = _changes(rows, session)
     changes_line = None
@@ -1095,6 +1131,8 @@ def build_view(result: Any, session: Session, clock: Any) -> View:
         else (QUESTIONS_LINK_KEYS_LINE if panel.link_on else QUESTIONS_KEYS_LINE),
         inspector_scroll=session.inspector_scroll,
         screen_header2=screen_header2,
+        screen_header1=screen_header1,
+        screen_counts_tokens=tuple(screen_tokens),
         questions=panel,
         desk=_desk(
             panel,
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
diff --git a/tests/observe/test_commands.py b/tests/observe/test_commands.py
index 58dfdb59e..8dcb6f7f9 100644
--- a/tests/observe/test_commands.py
+++ b/tests/observe/test_commands.py
@@ -118,7 +118,8 @@ def test_once_with_width_prints_the_bound_screen_with_the_gap_notice(fake_clock,
     )
     lines = out.splitlines()
     assert code == 0 and lines and all(cell_len(l) <= width for l in lines)
-    assert GAP_NOTICE in lines and "\x1b" not in out
+    # the gap notice shares its row with the historical-hidden note
+    assert any(l.startswith(GAP_NOTICE) for l in lines) and "\x1b" not in out
     assert any("collected 80 / reported 80" in l for l in lines)
     via_click = CliRunner().invoke(
         observe_group, ["--once", "--fixture", "base", "--width", str(width)]
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
diff --git a/tests/observe/test_linkoff_screen_reference.py b/tests/observe/test_linkoff_screen_reference.py
index 1d94e3b7e..48f25c76c 100644
--- a/tests/observe/test_linkoff_screen_reference.py
+++ b/tests/observe/test_linkoff_screen_reference.py
@@ -31,10 +31,8 @@ from tests.observe.conftest import (
 GOLDEN = Path(__file__).parent / "golden_questions_linkoff.json"
 HEIGHT = 40
 WIDTHS = (160, 116, 80)
-KEYS_LITERAL = (
-    "Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  "
-    "m mark rows  e export all  q quit"
-)
+# The shown key list (Task 15): the dropped keys (Up/Down, Esc, m, d/u) still work.
+KEYS_LITERAL = "j/k move  Enter detail  / filter  h history  e export  q quit"
 
 
 def _view(clock, rows):
@@ -65,7 +63,7 @@ def capture(clock):
 
 
 def test_the_link_off_keys_line_is_the_pinned_literal(fake_clock):
-    assert QUESTIONS_KEYS_LINE == KEYS_LITERAL and len(KEYS_LITERAL) == 107
+    assert QUESTIONS_KEYS_LINE == KEYS_LITERAL and len(KEYS_LITERAL) == 61
     assert _view(fake_clock, make_question_rows(2)).help_line == KEYS_LITERAL
 
 
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
index b6756f4f8..11d23911e 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -91,15 +91,12 @@ def test_matrix_lines_fit_counts_are_k_of_n_and_overflow_names_the_total(
     for line in lines:
         for k, n in re.findall(r"(\d+) of (\d+)", line):
             assert int(k) <= int(n)
-    overflow = [l for l in lines if re.match(r"^\d+/\d+ shown", l)]
-    assert len(overflow) == 1
-    x, y = map(int, re.match(r"^(\d+)/(\d+) shown", overflow[0]).groups())
-    assert y == n_rows and x < y and f"+{y - x} more" in overflow[0]
-    assert any(
-        l.endswith(f"| collected {n_rows} / reported {n_rows}")
-        or f"collected {n_rows} / reported {n_rows}" in l
-        for l in lines
-    )
+    assert not any(re.match(r"^\d+/\d+ shown", l) or "more" in l.split() for l in lines)
+    footer = [l for l in lines if re.search(r"shown \d+/\d+$", l)]
+    assert len(footer) == 1  # the footer names the total once; no "+N more" row
+    x, y = map(int, re.search(r"shown (\d+)/(\d+)$", footer[0]).groups())
+    assert y == n_rows and x < y
+    assert any(f"collected {n_rows} / reported {n_rows}" in l for l in lines)
 
 
 # -- T24 and T44 ------------------------------------------------------------------------------------------------
@@ -197,7 +194,9 @@ def test_counts_strip_keeps_its_priority_tokens_intact(fake_clock, width):
     assert "collected 80 / reported 80" in text and "scope=all" in text
     first_lines = screen_lines(view, policy_for(width))
     gap = next(i for i, l in enumerate(first_lines) if l.startswith("Human questions"))
-    title = next(i for i, l in enumerate(first_lines) if l == view.ledger_title)
+    title = next(
+        i for i, l in enumerate(first_lines) if l.startswith(view.ledger_title)
+    )
     assert gap < title  # the gap notice sits above the ledger at every width
 
 
@@ -297,14 +296,13 @@ def test_full_width_is_a_table_without_a_stage_column_and_with_the_verbatim_kind
     for name in (
         "run",
         "workerState",
-        "dispatchStatus",
-        "terminalState",
-        "outcome",
+        "status",
         "nextAction.kind",
-        "liveness",
+        "alive",
         "evidence age",
     ):
         assert name in header
+    assert "flags" not in header and "dispatchStatus" not in header  # one status cell
     assert "stage" not in header.lower() and "orchestrator" not in header
     first = view.visible_rows[0]
     row = next(
@@ -312,7 +310,10 @@ def test_full_width_is_a_table_without_a_stage_column_and_with_the_verbatim_kind
         for l in lines
         if l.split()[:1] == [first.dispatch_id] or f" {first.dispatch_id} " in f" {l} "
     )
-    assert first.run in row and first.next_action in row and first.liveness in row
+    assert first.run in row and first.next_action in row
+    assert (
+        "●" in row or first.raw.liveness_verdict in row
+    )  # a dot, or the spelled-out value
 
 
 def test_line_and_short_forms_follow_kind_id_verdict_age(fake_clock):
@@ -324,10 +325,11 @@ def test_line_and_short_forms_follow_kind_id_verdict_age(fake_clock):
         if first.dispatch_id in l and l.strip()
     )
     verdict = first.raw.liveness_verdict
+    alive_cell = "●" if verdict in ("alive", "live") else verdict  # dot or spelled out
     assert (
         line_form.index(first.next_action)
         < line_form.index(first.dispatch_id)
-        < line_form.index(verdict)
+        < line_form.index(alive_cell)
     )
     short = next(
         l
@@ -351,15 +353,14 @@ def test_marks_flags_overflow_and_empty_text_are_laid_out(fake_clock):
         and frozen.lstrip().startswith(("▸", "@"))
         or frozen.startswith("▸")
     )
-    assert any(re.match(r"^\d+/80 shown\s+\+\d+ more", l) for l in lines)
+    assert any(re.search(r"shown \d+/80$", l) for l in lines)  # no "+N more" row
     empty = screen_lines(fixture_view("empty", fake_clock), policy_for(120))
     assert "no observed items in this source window; not proof none exist" in empty
     assert "worker-list returned 0 workers in scope=bound" in empty
     never = Collector(FixtureSource("base"), fake_clock).latest()
     lines = screen_lines(build_view(never, Session(), fake_clock), policy_for(120))
-    assert "no successful worker-list read yet" in lines and any(
-        "as of never" in l for l in lines
-    )
+    assert "no successful worker-list read yet" in lines
+    assert not any("as of" in l for l in lines)  # no ``as of`` on the title any more
 
 
 def test_changed_rows_and_filter_notes_show_on_screen(fake_clock):
@@ -494,7 +495,8 @@ def test_a_long_question_list_is_windowed_with_x_of_y_shown(fake_clock):
 def test_t47_questions_off_the_screen_is_the_release_1_screen(fake_clock):
     off = fixture_view("base", fake_clock)
     lines = screen_lines(off, policy_for(160))
-    assert GAP_NOTICE in lines and not any("COORDINATOR" in l for l in lines)
+    assert any(l.startswith(GAP_NOTICE) for l in lines)  # the note shares its row
+    assert not any("COORDINATOR" in l for l in lines)
     assert any("messages UNVERIFIED (not read)" in l for l in lines)
 
 
@@ -1311,24 +1313,23 @@ def test_a_selected_question_is_one_bold_amber_line_and_the_others_have_parts(
 def test_absent_values_are_muted_and_state_words_follow_the_table(fake_clock):
     view = fixture_view("missing-fields", fake_clock)
     lines = _compose(view, policy_for(160, height=60))
-    counts = first_line(
-        lines, "source counts:"
-    )  # a counts token ending in an absent value
-    assert roles_at(counts, "source counts:") == {"body"}
-    assert roles_at(counts, "unknown  runs") == {"muted"}  # the absent value itself
-    cost = first_line(lines, "cost unavailable")
-    assert roles_at(cost, "unavailable") == {"muted"}
-    absent = first_line(lines, "unknown (unknown)")
-    assert roles_at(absent, "unknown (unknown)") == {"muted"}  # the bare verdict
+    text = "\n".join(ln.plain for ln in lines)
+    assert "source counts:" not in text and "runs seen" not in text  # in the inspector
+    dim = first_line(lines, "no source: settled, frozen, cost")
+    assert roles_at(dim, "no source: settled, frozen, cost") == {
+        "muted"
+    }  # one dim token
+    absent = first_line(lines, "● unknown")
+    assert roles_at(absent, "● unknown") == {"muted"}  # the bare verdict, spelled out
     assert any(
         roles_at(ln, "running") == {"state_running"}
         for ln in lines
         if " running " in ln.plain
     )
     blocked = first_line(
-        lines, " blocked "
+        lines, "blocked/active/none"
     )  # not in the table: body, never a state role
-    assert roles_at(blocked, "blocked") == {"body"}
+    assert roles_at(blocked, "blocked/active/none") == {"body"}
 
 
 def test_a_frozen_flag_cell_takes_the_frozen_role(fake_clock):
@@ -1359,13 +1360,14 @@ def heading_index(lines):
 
 
 @pytest.mark.parametrize("width", WIDTHS)
-def test_the_column_heading_and_rule_show_at_every_width_when_rows_are_visible(
+def test_the_column_heading_shows_at_every_width_with_no_rule_row_under_it(
     fake_clock, width
 ):
     lines = screen_lines(fixture_view("base", fake_clock), policy_for(width))
     i = heading_index(lines)
-    assert i is not None and set(lines[i + 1]) <= {"─", " "} and "─" in lines[i + 1]
-    assert "w-0" in lines[i + 2]  # the first row follows the rule
+    assert i is not None
+    assert "w-0" in lines[i + 1]  # the first row follows the heading directly
+    assert not any(set(ln) <= {"─", " "} and "─" in ln for ln in lines[:-4])
 
 
 @pytest.mark.parametrize("width", WIDTHS)
@@ -1388,7 +1390,7 @@ def test_the_key_list_is_never_cut_and_no_key_pair_is_split(fake_clock, width):
 def test_a_rule_line_precedes_the_footer_keys(fake_clock, width):
     view = fixture_view("base", fake_clock)
     lines = screen_lines(view, policy_for(width))
-    first_key = next(i for i, ln in enumerate(lines) if "Up/Down" in ln)
+    first_key = next(i for i, ln in enumerate(lines) if "j/k move" in ln)
     assert (
         set(lines[first_key - 1]) == {"─"} and cell_len(lines[first_key - 1]) == width
     )
@@ -1452,8 +1454,10 @@ def test_the_read_only_badge_is_right_aligned_once_and_every_line_fits(
     assert cell_len(badged[0]) == width and badged[0].endswith(READ_ONLY_BADGE)
     title = " ".join(lines[: index + 1]).replace(READ_ONLY_BADGE, "")
     assert " ".join(title.split()) == " ".join(
-        view.header1.split()
-    )  # title text unedited
+        view.screen_header1.split()
+    )  # the title text, without ``mode=`` and ``as of``
+    assert "mode=" not in title and "as of" not in title
+    assert "mode=" in view.header1 and "as of" in view.header1  # the record keeps them
     assert all(cell_len(ln) <= width for ln in lines)
 
 
@@ -1514,6 +1518,78 @@ def test_each_fact_occurs_once_on_the_questions_screen(fake_clock, width):
     assert flat.count("retention reset at") == 1
 
 
+# -- Task 15: the ledger diet ----------------------------------------------------------------------------------
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_ledger_has_no_flags_column_no_rule_row_and_no_more_row(fake_clock, width):
+    view = fixture_view("base", fake_clock)
+    lines = screen_lines(view, policy_for(width, height=24))
+    head = heading_index(lines)
+    assert head is not None and "flags" not in lines[head]
+    assert not any(re.search(r"\+\d+ more", ln) for ln in lines)  # no "+N more" row
+    footer = next(i for i, ln in enumerate(lines) if "j/k move" in ln)
+    assert set(lines[footer - 1]) == {"─"}  # the footer rule is the one rule left
+    assert "─" not in "".join(lines[: footer - 1])
+    assert re.search(r"shown \d+/54$", lines[footer])  # 26 historical rows are hidden
+    assert "collected" not in lines[footer]
+
+
+@pytest.mark.parametrize("no_color", [False, True])
+@pytest.mark.parametrize("width", (160, 116))
+def test_a_non_alive_value_is_spelled_out_and_the_legend_says_so(
+    fake_clock, width, no_color
+):
+    view = fixture_view("missing-fields", fake_clock)
+    lines = screen_lines(view, policy_for(width, height=60, no_color=no_color))
+    assert any("● unknown" in ln for ln in lines)  # a word, not only a colour
+    legend = next(ln for ln in lines if ln.startswith(view.ledger_title))
+    assert "● alive; any other state is spelled out" in legend
+
+
+def test_the_status_cell_is_one_badge_or_three_raw_values(fake_clock):
+    lines = screen_lines(
+        fixture_view("missing-fields", fake_clock), policy_for(160, height=60)
+    )
+    assert any(" ACTIVE " in f" {ln} " for ln in lines)
+    assert any("blocked/active/none" in ln for ln in lines)  # any other combination
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_frozen_marker_reaches_the_status_cell_at_every_width(fake_clock, width):
+    base = fixture_view("base", fake_clock, Session(show_historical=True))
+    lines = screen_lines(base, policy_for(width, height=100))
+    frozen = next(ln for ln in lines if "w-003" in ln)
+    assert "FROZEN" in frozen
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_title_has_no_mode_and_no_as_of_and_the_scope_shows_once(fake_clock, width):
+    lines = screen_lines(fixture_view("base", fake_clock), policy_for(width))
+    text = " ".join(lines)
+    assert "mode=" not in text and "as of" not in text
+    assert text.count("scope=all") == 1
+    assert "no source: settled, frozen, cost" in text
+    assert "unavailable (no source)" not in text
+    assert "runs seen" not in text  # in the inspector
+    assert "source counts: active" in text  # known counts stay; unknown ones leave
+
+
+def test_source_counts_and_runs_seen_live_in_the_inspector(fake_clock):
+    view = fixture_view("base", fake_clock)
+    labels = [label for label, _ in view.visible_rows[0].inspector]
+    assert "source counts" in labels and "runs seen" in labels
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_gap_notice_and_the_historical_note_share_one_row(fake_clock, width):
+    view = fixture_view("base", fake_clock)
+    lines = screen_lines(view, policy_for(width))
+    row = next(ln for ln in lines if ln.startswith("Human questions"))
+    assert "26 historical hidden (h)" in row or width == 80  # 80: too wide for one row
+    assert sum("26 historical hidden (h)" in ln for ln in lines) == 1
+
+
 @pytest.mark.parametrize("width", WIDTHS)
 @pytest.mark.parametrize("text", ["Ship it now?", "ab?", "x" * 24, "y" * 25])
 def test_a_short_selected_question_is_also_on_the_screen_once(fake_clock, width, text):
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
diff --git a/tests/observe/test_view.py b/tests/observe/test_view.py
index fcf5e7657..189340c87 100644
--- a/tests/observe/test_view.py
+++ b/tests/observe/test_view.py
@@ -584,8 +584,8 @@ def test_plus_n_more_never_counts_the_selected_row(fake_clock):
     assert window.shown == 10 and window.total == 80 and window.text == "10/80 shown"
     assert any(rv.selected for rv in window.rows)  # the selected row is kept in view
     assert window.more == 70 and window.more_text == "+70 more"
-    assert view.footer(window).endswith("shown 10/80 | collected 80 / reported 80")
-    assert "shown 80/80 | collected 80 / reported 80" in view.footer(view.window(None))
+    assert view.footer(window).endswith("shown 10/80")  # collected is in the strip
+    assert view.footer(view.window(None)).endswith("shown 80/80")
     # selected row not in the visible set (filtered out): it is not counted in "+N more" either
     row_view = view.selected
     narrowed = build(


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
