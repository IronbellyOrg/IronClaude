4842ffc8f60ff1f448fd9487c36e08586f404d21
Review one task for spec compliance.

Task brief: ## Task 11: Heading at every width, whole key groups, footer rule, counts never cut

Depends on: Task 10

Spec steps 2.2, 2.3 and 2.4 in `OBS/render.py`. Add `_heading_rows(view, policy)` (2 when `view.visible_rows`, else 0) and use it at the `ledger_fixed` term (line 439) and the heading gate (line 497) in place of the `width_class == "full"` tests, without adding heading rows to `reserved`; add `wrap_groups(text, width, policy)` next to `wrap` and use it in `_help_lines` (line 304) in both branches, removing the `clip(...)` branch for `view.questions is None`; add one `glyph("hrule") * width` row before the footer and count it in `footer_height` (lines 423-431) and the footer branch (lines 514-521); remove the branch of `counts_lines` (lines 127-129) that clips an unprotected token, so a token that does not fit is dropped whole and the line ends with the existing ` >` marker, protected tokens keeping their wrap path.

Acceptance criteria:
- A column heading and rule appear at 116 and 80 whenever rows are visible and are absent when there are none.
- No key line at 80 columns ends in `>`; the pair `n/p question` is never split across lines; no counts line ends inside a token; the footer rule precedes the footer.
- `tests/observe/test_inspector_scroll.py` still passes (the inspector returns earlier).
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
Start sha: 4842ffc8f60ff1f448fd9487c36e08586f404d21
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b (Grep floor, confirmed by Read): wrap_groups and _heading_rows are new; _help_lines is called only inside src/superclaude/cli/observe/render.py (_compose, twice); counts_line_objects and counts_lines keep their signatures (counts_lines has no caller outside render.py). screen_lines callers (tests and the harness) are unedited.
Evidence: uv run pytest tests/observe/ -q printed '4 failed, 862 passed'. The 4 failing tests are exactly the ones the plan assigns to Task 16 (it regenerates both presentation goldens and re-pins the row-count test): tests/observe/test_linkoff_screen_reference.py::test_the_link_off_questions_screen_equals_the_reference[five] and [long_subject] (golden_questions_linkoff.json), tests/observe/test_render.py::test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface (golden_release1_surface.json), and tests/observe/test_render.py::test_decision_2_the_questions_win_on_a_short_terminal_the_ledger_is_squeezed (the questions list has 3 fewer question rows because of the heading and the footer rule). golden_release1_records.json still passes (record, snapshot and headers unchanged). ruff check: All checks passed.
Two safeguards beyond the spec text keep the output within the terminal height: the heading is left out when it would leave no room for one ledger row, and the footer rule is dropped when the output is still too tall (found because test_every_screen_line_fits_at_160_116_and_80_with_the_panel[80-14] overflowed by one row).
Touched: src/superclaude/cli/observe/render.py and tests/observe/test_render.py (both modified).

diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index efd1b4b4c..f5b9eec8c 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -89,6 +89,34 @@ def wrap(text: str, width: int, policy: TerminalPolicy) -> list[str]:
     return lines
 
 
+def wrap_groups(text: str, width: int, policy: TerminalPolicy) -> list[str]:
+    """Wrap a key list on its two-space separators: whole groups are packed greedily into lines
+    joined by two spaces, so no key pair is ever split. Only a single group wider than the width
+    falls back to ``wrap``."""
+    if policy.ascii:
+        text = ascii_safe(text)
+    groups = [g for g in text.split("  ") if g]
+    lines: list[str] = []
+    current = ""
+    for group in groups:
+        candidate = f"{current}  {group}" if current else group
+        if cell_len(candidate) <= width:
+            current = candidate
+            continue
+        if current:
+            lines.append(current)
+            current = ""
+        if cell_len(group) <= width:
+            current = group
+        else:
+            chunks = wrap(group, width, policy)
+            lines.extend(chunks[:-1])
+            current = chunks[-1]
+    if current or not lines:
+        lines.append(current)
+    return lines
+
+
 def _pad(text: str, width: int) -> str:
     return text + " " * max(width - cell_len(text), 0)
 
@@ -198,6 +226,16 @@ def _token_line(text: str, token: CountsToken) -> Line:
     return _absent_tail(text, "identity" if token.protected else "body")
 
 
+def _row_of(pieces: list[Line]) -> Line:
+    """The tokens of one counts line, two spaces apart."""
+    parts: list[Line] = []
+    for index, piece in enumerate(pieces):
+        if index:
+            parts.append(seg("  "))
+        parts.append(piece)
+    return join(*parts)
+
+
 def counts_line_objects(
     tokens: tuple[CountsToken, ...],
     policy: TerminalPolicy,
@@ -209,41 +247,40 @@ def counts_line_objects(
     """
     width = policy.width
     lines: list[Line] = []
-    current = Line("")
+    pieces: list[Line] = []  # the whole tokens of the line being built
     cut = False
     for token in tokens:
         text = ascii_safe(token.text) if policy.ascii else token.text
         if cut and not token.protected:
             continue
         piece = _token_line(text, token)
-        candidate = join(current, seg("  "), piece) if current.plain else piece
-        if cell_len(candidate.plain) <= width:
-            current = candidate
+        if cell_len(_row_of([*pieces, piece]).plain) <= width:
+            pieces.append(piece)
             continue
         if token.protected:
-            if current.plain:
-                lines.append(current)
+            if pieces:
+                lines.append(_row_of(pieces))
             chunks = wrap(text, width, policy)
             lines.extend(seg(chunk, "identity") for chunk in chunks[:-1])
-            current = seg(chunks[-1], "identity")
+            pieces = [seg(chunks[-1], "identity")]
             continue
-        if max_lines is None or len(lines) + 1 < max_lines:
-            if current.plain:
-                lines.append(current)
-            current = _token_line(clip(text, width, policy), token)
+        if cell_len(piece.plain) <= width and (
+            max_lines is None or len(lines) + 1 < max_lines
+        ):
+            if pieces:
+                lines.append(_row_of(pieces))
+            pieces = [piece]
             continue
-        room = width - cell_len(current.plain) - 2
-        if room >= 2:
-            current = join(
-                current, seg("  "), _token_line(clip(text, room, policy), token)
-            )
-        else:
-            current = join(current, seg(" " + glyph("truncate", policy))).clipped(
-                width, policy
-            )
+        # A token that does not fit is dropped whole, never cut inside: the line ends with the
+        # truncation marker after the last whole token (whole tokens are dropped from the end
+        # of the line until the marker fits).
+        marker = glyph("truncate", policy)
+        while pieces and cell_len(_row_of(pieces).plain) + 1 + cell_len(marker) > width:
+            pieces.pop()
+        pieces = [join(_row_of(pieces), seg(" " + marker)) if pieces else seg(marker)]
         cut = True
-    if current.plain:
-        lines.append(current)
+    if pieces:
+        lines.append(_row_of(pieces))
     return lines
 
 
@@ -409,6 +446,12 @@ def _header_lines(columns: list[tuple[str, int]], policy: TerminalPolicy) -> lis
     ]
 
 
+def _heading_rows(view: View, policy: TerminalPolicy) -> int:
+    """The column heading and its rule take 2 rows whenever ledger rows are visible, at every
+    width class (the policy is part of the call shape; the width class no longer matters)."""
+    return 2 if view.visible_rows and not policy.too_narrow else 0
+
+
 # -- screens -------------------------------------------------------------------------------------------------
 
 
@@ -479,10 +522,8 @@ def _notes(view: View) -> list[str]:
 
 
 def _help_lines(view: View, policy: TerminalPolicy) -> list[Line]:
-    """The key list: clipped as in release 1, but wrapped when questions are on (no key is cut)."""
-    if view.questions is None:
-        return [seg(clip(view.help_line, policy.width, policy), "muted")]
-    return _wrapped(view.help_line, policy.width, policy, "muted")
+    """The key list, wrapped by whole key groups: no key is cut and no pair is split."""
+    return _roled(wrap_groups(view.help_line, policy.width, policy), "muted")
 
 
 def _question_line(q: QuestionLine, policy: TerminalPolicy) -> Line:
@@ -641,7 +682,7 @@ def _compose(
     # The footer is one line when it fits, else the key list and the counts on two lines.
     window_probe = view.window(None)
     one_line = view.footer(window_probe)
-    footer_height = (
+    footer_height = 1 + (  # one rule line above the footer
         1
         if cell_len(one_line) <= width
         else len(_help_lines(view, policy))
@@ -654,7 +695,7 @@ def _compose(
     inspecting = view.focus == "inspector" and view.inspector is not None
     if panel is not None and panel.replaces_gap and not inspecting:
         ledger_fixed = len(wrap(view.ledger_title, width, policy)) + (
-            2 if policy.width_class == "full" and view.visible_rows else 0
+            _heading_rows(view, policy)
         )
         base = len(
             _panel_lines(replace(panel, lines=(), empty_text=None), policy, None)
@@ -714,7 +755,13 @@ def _compose(
 
     body = _wrapped(view.ledger_title, width, policy, "secondary")
     columns, getters = _columns(policy)
-    if policy.width_class == "full" and view.visible_rows:
+    heading = _heading_rows(view, policy)
+    # The column heading and its rule at every width, unless that would leave no room for even
+    # one ledger row (then the rows win and the heading is left out).
+    if (
+        heading
+        and policy.height - (len(top) + len(body) + heading + footer_height + 1) >= 1
+    ):
         body += _header_lines(columns, policy)
     reserved = (
         len(top) + len(body) + footer_height + 1
@@ -740,7 +787,8 @@ def _compose(
         footer_lines = _help_lines(view, policy) + _wrapped(
             view.footer_counts(window), width, policy, "muted"
         )
-    return top + body + footer_lines
+    rule = seg(glyph("hrule", policy) * width, "border_secondary")
+    return top + body + [rule] + footer_lines
 
 
 def render(view: View, policy: TerminalPolicy, message: str | None = None) -> Group:
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 403ae639f..fa6b3bd19 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -1286,3 +1286,95 @@ def test_a_frozen_flag_cell_takes_the_frozen_role(fake_clock):
     )
     line = _row_segments(row, columns, getters, policy)
     assert roles_at(line, FROZEN_MARKER) == {"state_frozen"}
+
+
+# -- text defects of the existing layouts: heading, whole key groups, footer rule, counts -----------------------
+
+from superclaude.cli.observe.render import wrap_groups  # noqa: E402
+
+
+def heading_index(lines):
+    return next(
+        (
+            i
+            for i, ln in enumerate(lines)
+            if "dispatchId" in ln and "age" in ln and "w-0" not in ln
+        ),
+        None,
+    )
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_column_heading_and_rule_show_at_every_width_when_rows_are_visible(
+    fake_clock, width
+):
+    lines = screen_lines(fixture_view("base", fake_clock), policy_for(width))
+    i = heading_index(lines)
+    assert i is not None and set(lines[i + 1]) <= {"─", " "} and "─" in lines[i + 1]
+    assert "w-0" in lines[i + 2]  # the first row follows the rule
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_no_heading_when_there_are_no_rows(fake_clock, width):
+    lines = screen_lines(fixture_view("empty", fake_clock), policy_for(width))
+    assert heading_index(lines) is None
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_key_list_is_never_cut_and_no_key_pair_is_split(fake_clock, width):
+    view = fixture_view("base", fake_clock)
+    lines = screen_lines(view, policy_for(width))
+    groups = [g for g in view.help_line.split("  ") if g]
+    assert all(any(g in ln for ln in lines) for g in groups)
+    assert not any(ln.endswith(" >") or ln.endswith("e exp>") for ln in lines[-6:])
+    assert any("q quit" in ln for ln in lines[-3:])
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_a_rule_line_precedes_the_footer_keys(fake_clock, width):
+    view = fixture_view("base", fake_clock)
+    lines = screen_lines(view, policy_for(width))
+    first_key = next(i for i, ln in enumerate(lines) if "Up/Down" in ln)
+    assert (
+        set(lines[first_key - 1]) == {"─"} and cell_len(lines[first_key - 1]) == width
+    )
+
+
+def test_the_link_on_key_pair_n_p_question_stays_on_one_line_at_every_width(fake_clock):
+    rows = r3_rows([("w-001", "q?")])
+    for width in WIDTHS:
+        lines, _ = r3_screen(fake_clock, rows, None, width, height=60)
+        assert any("n/p question" in ln for ln in lines)
+
+
+def test_wrap_groups_packs_whole_groups_and_falls_back_to_wrap_for_a_wide_group():
+    pol = policy_for(80)
+    assert wrap_groups("a b  c d  e f", 20, pol) == ["a b  c d  e f"]
+    assert wrap_groups("a b  c d  e f", 8, pol) == ["a b  c d", "e f"]  # 8 cells fit
+    assert wrap_groups("a b  c d  e f", 7, pol) == ["a b", "c d", "e f"]
+    assert wrap_groups("x" * 15, 10, pol) == ["x" * 10, "x" * 5]  # one wide group
+    assert wrap_groups("", 10, pol) == [""]
+
+
+def test_the_truncation_marker_drops_whole_tokens_until_it_fits_and_never_cuts_one():
+    from superclaude.cli.observe.render import counts_lines
+    from superclaude.cli.observe.view import CountsToken
+
+    pol = dataclasses.replace(policy_for(80), width=20)
+    tokens = (
+        CountsToken("a" * 10, True),
+        CountsToken("b" * 8, False),  # fills the line exactly: no room for " >"
+        CountsToken("cc", False),
+    )
+    assert counts_lines(tokens, pol, max_lines=1) == ["a" * 10 + " >"]
+    # a lone unprotected token wider than the line is dropped whole, never cut inside
+    wide = (CountsToken("x" * 30, False),)
+    assert counts_lines(wide, pol, max_lines=None) == [">"]
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_no_counts_line_ends_inside_a_token(fake_clock, width):
+    lines = screen_lines(fixture_view("base", fake_clock), policy_for(width))
+    for ln in lines[:6]:
+        if ln.endswith(">"):
+            assert ln[-2] == " ", ln  # the marker follows a whole token
Delta diff from the previous reviewed tree (empty on the first review): The previous reviewed tree was not pinned in time, so no mechanical delta diff exists. The changes made after the first review (all in src/superclaude/cli/observe/render.py unless noted):
- counts_line_objects was rewritten around a new helper _row_of: it keeps the whole tokens of the current line in a list; a token that does not fit is dropped whole, and whole tokens are popped from the end of the line until " >" fits; a lone unprotected token wider than the line is dropped whole (no clip of a token remains in that function). (F1.1, F1.2)
- The "give up the footer rule when the screen is still too tall" return statement was removed; the rule is always appended. A sweep of widths 160, 116, 80 and heights 8 to 60 with 0, 1, 5 and 30 questions finds overflow only at heights 8 to 10 (the fixed header rows alone exceed those heights). (F1.3)
- _heading_rows now has the signature _heading_rows(view, policy) and both call sites pass policy. (F1.4)
- tests/observe/test_render.py gained test_the_truncation_marker_drops_whole_tokens_until_it_fits_and_never_cuts_one.
The full diff since the task start is in the Diff slot above.
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T11.AC2 at=src/superclaude/cli/observe/render.py:265-268 anchor="no counts line ends inside a token" chk=y,n,n,n family=counts-marker-overflow fix=when current plus " >" is wider than the width, drop the last whole token(s) from current until the marker fits. covers="a token that does not fit is dropped whole ... the line ends with the existing marker" first=start origin=new: When the last whole token leaves fewer than 2 free cells, join(current, marker) is too wide; .clipped then cuts inside that token and ends the line with ">" attached to it.
F1.2 sev=blocking trigger=B1 ac=T11.AC2 at=src/superclaude/cli/observe/render.py:258-262 anchor="no counts line ends inside a token" chk=y,n,n,n family=counts-token-clip fix=when a lone unprotected token is wider than the whole width, drop it whole with the marker instead of clip(text, width, policy). covers="remove the branch ... that clips an unprotected token" first=start origin=new: The path current = _token_line(clip(text, width, policy), token) still clips an unprotected token wider than one line.
F1.3 sev=blocking trigger=B1 ac=T11.AC2 at=src/superclaude/cli/observe/render.py:778-780 anchor="the footer rule precedes the footer" chk=y,n,n,n family=footer-rule-conditional fix=do not drop the rule after the fact. covers="add one hrule row before the footer ... count it in footer_height" first=start origin=new: footer_height always counts the rule, but the return statement removes it whenever the screen is too tall.
F1.4 sev=blocking trigger=B4 ac=scope at=src/superclaude/cli/observe/render.py:437 anchor="Add `_heading_rows(view, policy)`" chk=n,n,n,y family=signature-drift fix=add the policy parameter, or record the reason for leaving it out. covers="`_heading_rows(view, policy)`" first=start origin=new: The function is defined as _heading_rows(view) and has no policy parameter.
Saved-probe re-check hit locations (may be empty): counts-marker-overflow and counts-token-clip (grep for "clip(text" and ".clipped(width" in render.py): hits at 202, 421, 558, 574; none is inside counts_line_objects any more.
footer-rule-conditional (grep for "rule"): hits at 442, 445, 450, 685, 759, 790, 791; the rule is appended unconditionally at 790-791.
signature-drift (grep for "_heading_rows"): hits at 449 (definition with view and policy), 698 and 758 (call sites).

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
