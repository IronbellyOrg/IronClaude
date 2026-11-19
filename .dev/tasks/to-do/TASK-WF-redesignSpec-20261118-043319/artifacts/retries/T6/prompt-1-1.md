db7ddea677fc59686c2b449349eb68a279040226
Review one task for spec compliance.

Task brief: ## Task 6: Add the Line layer to render.py

Depends on: Task 5

Spec step 1.3. In `OBS/render.py` add frozen `Span(start, end, role)` and `Line(plain, spans)` with `seg`, `join`, `Line.clipped`, an `ascii_safe` path that keeps offsets valid, and `_roled(strings, role)`. Rename the body of `screen_lines` (line 390) to `_compose(view, policy, message=None) -> list[Line]` and define `screen_lines(...) = [l.plain for l in _compose(...)]` with the public signature unchanged. `render` (line 524) builds `Text(l.plain, no_wrap=True, overflow="crop")` per line and stylizes spans through `theme.style_for` only when `policy.color_system` is not None. Wrap every existing builder output as one `body` line so behaviour is unchanged.

Acceptance criteria:
- Every `screen_lines` string result is unchanged: `tests/observe/test_render.py`, `test_linkoff_screen_reference.py`, `test_golden_contract.py`, `test_inspector_scroll.py`, `test_question_cap.py` and `test_export.py` pass with no edit to a golden.
- `len(group.renderables) == len(screen_lines(...))` still holds (`tests/observe/test_render.py:399`) and the source guards at lines 400-404 pass.
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
Start sha: db7ddea677fc59686c2b449349eb68a279040226
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b (Grep floor, confirmed by Read): screen_lines keeps its signature and string results; callers (tests test_question_cap.py, test_render.py, release1_surface.py, test_inspector_scroll.py, test_export.py, test_linkoff_screen_reference.py, test_golden_contract.py, and the harness) are unedited and pass. render() keeps its signature; it is called by src/superclaude/cli/observe/commands.py (run_once, LiveScreen.draw) and tests. This task adds no role to any builder (that is the next task), so every Line has no spans and the output bytes are unchanged.
Evidence: uv run pytest tests/observe/ -q printed '824 passed in 19.78s' (819 before this task); ruff check: All checks passed; git diff --stat -- tests/observe/*.json is empty (no golden changed). Touched: src/superclaude/cli/observe/render.py, tests/observe/test_render.py (both modified).

diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 33b3dcdf5..7de34c6c4 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -7,7 +7,7 @@ from data (never markup strings). It never imports the adapter or the collector.
 
 from __future__ import annotations
 
-from dataclasses import replace
+from dataclasses import dataclass, replace
 
 from rich.cells import cell_len
 from rich.console import Group
@@ -21,6 +21,7 @@ from superclaude.cli.observe.terminal import (
     clip,
     glyph,
 )
+from superclaude.cli.observe.theme import style_for
 from superclaude.cli.observe.view import (
     DESK_HIDDEN,
     DESK_SELECTED_HIDDEN,
@@ -88,6 +89,68 @@ def _cell(text: str, width: int, policy: TerminalPolicy) -> str:
     return _pad(clip(text, width, policy), width)
 
 
+# -- lines with colour roles ---------------------------------------------------------------------
+
+
+@dataclass(frozen=True)
+class Span:
+    """A role over ``plain[start:end]``. Offsets count characters, never cells (a wide character
+    is two cells but one character), so they stay valid whatever the terminal width."""
+
+    start: int
+    end: int
+    role: str
+
+
+@dataclass(frozen=True)
+class Line:
+    """One screen line: its plain text (the source of truth for every test, golden and export)
+    plus the role spans that colour it."""
+
+    plain: str
+    spans: tuple[Span, ...] = ()
+
+    def clipped(self, width: int, policy: TerminalPolicy) -> Line:
+        """The line cut to ``width`` cells by ``clip``; spans are trimmed to the kept text."""
+        text = clip(self.plain, width, policy)
+        source = ascii_safe(self.plain) if policy.ascii else self.plain
+        kept = 0
+        while kept < min(len(text), len(source)) and text[kept] == source[kept]:
+            kept += 1
+        spans = tuple(
+            Span(s.start, min(s.end, kept), s.role)
+            for s in self.spans
+            if s.start < kept
+        )
+        return Line(text, spans)
+
+    def to_ascii(self) -> Line:
+        """Every non-ASCII character becomes one ``?``, so the span offsets stay valid."""
+        return Line(ascii_safe(self.plain), self.spans)
+
+
+def seg(text: str, role: str | None = None) -> Line:
+    """A piece of text, with one role over all of it when ``role`` is given."""
+    return Line(text, (Span(0, len(text), role),) if role and text else ())
+
+
+def join(*parts: Line) -> Line:
+    """The parts end to end; each span moves by the character length of what precedes it."""
+    plain = ""
+    spans: list[Span] = []
+    for part in parts:
+        spans += [
+            Span(s.start + len(plain), s.end + len(plain), s.role) for s in part.spans
+        ]
+        plain += part.plain
+    return Line(plain, tuple(spans))
+
+
+def _roled(strings: list[str], role: str) -> list[Line]:
+    """Existing plain lines (from ``wrap`` and friends), each carrying one whole-line role."""
+    return [seg(text, role) for text in strings]
+
+
 # -- the COUNTS strip ------------------------------------------------------------------------------
 
 
@@ -394,6 +457,19 @@ def screen_lines(
 
     ``message`` is a one-off notice from the command loop (an export result); it sits above the footer.
     """
+    return [line.plain for line in _compose(view, policy, message)]
+
+
+def _compose(
+    view: View, policy: TerminalPolicy, message: str | None = None
+) -> list[Line]:
+    """The screen as ``Line`` objects: the plain text of ``screen_lines`` plus colour roles."""
+    return [Line(text) for text in _screen_strings(view, policy, message)]
+
+
+def _screen_strings(
+    view: View, policy: TerminalPolicy, message: str | None = None
+) -> list[str]:
     width = policy.width
     if (
         policy.too_narrow
@@ -522,10 +598,15 @@ def screen_lines(
 
 
 def render(view: View, policy: TerminalPolicy, message: str | None = None) -> Group:
-    """The screen as Rich renderables: one plain ``Text`` per line, never reflowed."""
-    return Group(
-        *(
-            Text(line, no_wrap=True, overflow="crop")
-            for line in screen_lines(view, policy, message)
-        )
-    )
+    """The screen as Rich renderables: one ``Text`` per line, never reflowed, coloured by role
+    only when the policy has a colour depth."""
+    texts = []
+    for line in _compose(view, policy, message):
+        text = Text(line.plain, no_wrap=True, overflow="crop")
+        if policy.color_system is not None:
+            for span in line.spans:
+                style = style_for(span.role, policy.color_system)
+                if style is not None and span.end > span.start:
+                    text.stylize(style, span.start, span.end)
+        texts.append(text)
+    return Group(*texts)
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index f27043435..6b213407e 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -1072,7 +1072,10 @@ def test_r3_a_hash_after_a_long_path_list_is_cut_with_a_mark_at_80_and_116_colum
     lines, view = r3_screen(fake_clock, rows, 0, width, height=70)
     assert all(cell_len(ln) <= width for ln in lines)
     text = desk_text_lines(lines)
-    if width in (80, 116):  # D-6 exception: four lines cut the ask, so the hash is not shown
+    if width in (
+        80,
+        116,
+    ):  # D-6 exception: four lines cut the ask, so the hash is not shown
         assert len(text) == 4 and text[-1].endswith("...")
         assert not any(HASH in ln for ln in lines if not ln.startswith("▸ "))
     else:  # wide enough for the whole ask inside four lines
@@ -1103,7 +1106,9 @@ def test_r3_a_120_character_worktree_id_continues_on_two_cell_indented_lines(
     session = Session(selected_question=(QRUN, f"msg_{1:012x}"))
     lines = screen_lines(build_view(result, session, fake_clock), policy_for(width, 70))
     assert all(cell_len(ln) <= width for ln in lines)
-    start = next(i for i, ln in enumerate(lines) if ln.startswith("resource.worktreeId:"))
+    start = next(
+        i for i, ln in enumerate(lines) if ln.startswith("resource.worktreeId:")
+    )
     if width == 160:  # label, space and value (141 cells) fit one line: no continuation
         assert lines[start] == f"resource.worktreeId: {worktree}"
         return
@@ -1113,7 +1118,9 @@ def test_r3_a_120_character_worktree_id_continues_on_two_cell_indented_lines(
             break
         tail.append(ln)
     assert len(tail) >= 2 and all(ln.startswith("  ") for ln in tail)
-    assert "".join(ln[2:] for ln in tail) == worktree  # hard-split, nothing lost, no marker
+    assert (
+        "".join(ln[2:] for ln in tail) == worktree
+    )  # hard-split, nothing lost, no marker
 
 
 def test_strip_sgr_removes_colour_codes_and_sgr_params_lists_them():
@@ -1121,3 +1128,54 @@ def test_strip_sgr_removes_colour_codes_and_sgr_params_lists_them():
     assert strip_sgr(coloured) == "age plain red"
     assert sgr_params(coloured) == {"1;38;2;250;178;25", "0", "31"}
     assert strip_sgr("no escapes") == "no escapes" and sgr_params("no escapes") == set()
+
+
+# -- the Line layer: role spans over plain text ----------------------------------------------------------
+
+from superclaude.cli.observe.render import Line, Span, _roled, join, seg  # noqa: E402
+from superclaude.cli.observe.terminal import clip  # noqa: E402
+
+
+def test_join_shifts_span_offsets_by_characters_not_cells():
+    wide = seg("中中", "attention")  # two characters, four cells
+    line = join(wide, seg(" "), seg("ab", "muted"))
+    assert line.plain == "中中 ab"
+    assert line.spans == (Span(0, 2, "attention"), Span(3, 5, "muted"))
+    assert cell_len(line.plain) == 7  # the spans are not in cells
+
+
+def test_a_clipped_line_keeps_its_plain_text_and_trims_its_spans():
+    pol = policy_for(80)
+    line = seg("x" * 30, "body")
+    cut = line.clipped(10, pol)
+    assert cut.plain == "x" * 9 + ">" and cut.plain == clip(line.plain, 10, pol)
+    assert cut.spans == (Span(0, 9, "body"),)
+    assert line.clipped(40, pol) == line  # nothing to cut: unchanged
+
+
+def test_ascii_mode_replaces_each_character_with_one_question_mark():
+    line = join(seg("▸ ", "selected"), seg("中", "body")).to_ascii()
+    assert line.plain == "? ?" and line.spans == (
+        Span(0, 2, "selected"),
+        Span(2, 3, "body"),
+    )
+
+
+def test_roled_wraps_existing_plain_lines_with_one_whole_line_role():
+    lines = _roled(["ab", ""], "muted")
+    assert lines == [Line("ab", (Span(0, 2, "muted"),)), Line("", ())]
+
+
+def test_render_colours_a_span_only_when_the_policy_has_a_colour_depth(
+    monkeypatch, fake_clock
+):
+    view = fixture_view("base", fake_clock)
+    monkeypatch.setattr(
+        render_module,
+        "_compose",
+        lambda v, p, m=None: [Line("hello world", (Span(0, 5, "attention"),))],
+    )
+    coloured = printed(view, policy_for(80))
+    plain = printed(view, policy_for(80, no_color=True))
+    assert "\x1b[" in coloured and strip_sgr(coloured) == plain == "hello world\n"
+    assert "\x1b" not in plain
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
