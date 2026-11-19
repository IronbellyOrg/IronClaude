a3481eb75e656a641605efd19eb1ac20444482e9
Review one task for spec compliance.

Task brief: ## Task 12: Title bar badge and the optional blank-band fix

Depends on: Task 11

Spec steps 2.5 and 2.6. Add `READ_ONLY_BADGE = "READ ONLY"` to `OBS/view.py` and `_title_bar(lines, policy)` to `OBS/render.py`, placing the badge right-aligned on the first wrapped header line if it fits, else the last, else on its own line, in the `attention` role; `view.header1` is not edited. Apply step 2.6 (the `line` and `short` id rule of `_columns`, lines 195-196 and 215) only if RB-22 against the baseline number N fails; otherwise log the skip in the Task 16 commit notes.

Acceptance criteria:
- `READ ONLY` appears exactly once on the screen and every line fits the width at 160, 116 and 80; `header1` in `tests/observe/golden_release1_records.json` is unchanged.
- The RB-22 outcome (fixed or skipped with its measured numbers) is written into `.dev/issues/409/visual-parity/scores/p2/notes.md`.
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
Start sha: a3481eb75e656a641605efd19eb1ac20444482e9
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b (Grep floor, confirmed by Read): READ_ONLY_BADGE is a new constant in src/superclaude/cli/observe/view.py used only by src/superclaude/cli/observe/render.py (_title_bar) and the new tests; view.header1 is not edited and src/superclaude/cli/observe/export.py does not mention the badge (record_text writes header1 as before; golden_release1_records.json still passes).
Evidence: uv run pytest tests/observe/ -q printed '4 failed, 868 passed'. The 4 failing tests are the ones assigned to Task 16 in the plan (both presentation goldens and the row-count test); they fail now because every screen has the badge in its first title line, in addition to the heading and footer rule of Task 11. ruff check: All checks passed.
Optional step 2.6 (the blank-band fix) was not applied; the measured numbers and the reason are in .dev/issues/409/visual-parity/scores/p2/notes.md (new file, untracked): the spec's rule would shrink the id column at 116 from 52 to 48 and widen it at 80 from 38 to 42, and cannot reach the threshold N=18.
Touched: src/superclaude/cli/observe/view.py, src/superclaude/cli/observe/render.py, tests/observe/test_render.py (modified); .dev/issues/409/visual-parity/scores/p2/notes.md (new).

diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index f5b9eec8c..3d7dae082 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -40,6 +40,7 @@ from superclaude.cli.observe.view import (
     INSPECTOR_TITLE,
     NO_MATCH_TEXT,
     QUESTIONS_REASON,
+    READ_ONLY_BADGE,
     UNAVAILABLE,
     CountsToken,
     DeskView,
@@ -639,6 +640,21 @@ def _panel_lines(
     return lines + _wrapped(panel.retention_line, width, policy, "muted")
 
 
+def _title_bar(lines: list[str], policy: TerminalPolicy) -> list[Line]:
+    """The title lines with the ``READ ONLY`` badge right-aligned: on the first line when it
+    fits there, else on the last, else on a line of its own. ``view.header1`` is not edited, so
+    the record keeps its title text."""
+    width = policy.width
+    badge = ascii_safe(READ_ONLY_BADGE) if policy.ascii else READ_ONLY_BADGE
+    out = [seg(text, "title") for text in lines]
+    for index in (0, len(lines) - 1):
+        if cell_len(lines[index]) + 2 + cell_len(badge) <= width:
+            pad = width - cell_len(lines[index]) - cell_len(badge)
+            out[index] = join(out[index], seg(" " * pad), seg(badge, "attention"))
+            return out
+    return out + [join(seg(" " * (width - cell_len(badge))), seg(badge, "attention"))]
+
+
 def screen_lines(
     view: View, policy: TerminalPolicy, message: str | None = None
 ) -> list[str]:
@@ -666,7 +682,7 @@ def _compose(
         return lines + _wrapped(view.gap_notice, width, policy, "muted")
 
     head: list[Line] = []
-    head += _wrapped(view.header1, width, policy, "title")
+    head += _title_bar(wrap(view.header1, width, policy), policy)
     head += _wrapped(view.header2, width, policy, "muted")
     head += counts_line_objects(view.counts_tokens, policy)
     if view.changes_line:
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index 7a9900b30..46bc82151 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -103,6 +103,9 @@ PARTIAL_CAP_TEXT = (
     "newest first; oldest rows not read; long-running active workers may be among them"
 )
 KEYS_LINE = "Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e export  q quit"
+READ_ONLY_BADGE = (
+    "READ ONLY"  # right-aligned on the title bar; screen only, never in the record
+)
 FROZEN_MARKER = "FROZEN"  # fixture mode only; no other state overrides it (T34)
 INSPECTOR_TITLE = "INSPECTOR"
 INSPECTOR_HELP = "Esc back  j/k move  d/u scroll  e export  q quit"
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index fa6b3bd19..6fa4992d8 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -1378,3 +1378,54 @@ def test_no_counts_line_ends_inside_a_token(fake_clock, width):
     for ln in lines[:6]:
         if ln.endswith(">"):
             assert ln[-2] == " ", ln  # the marker follows a whole token
+
+
+# -- the title bar and its READ ONLY badge -----------------------------------------------------------------
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_the_read_only_badge_is_right_aligned_once_and_every_line_fits(
+    fake_clock, width
+):
+    from superclaude.cli.observe.view import READ_ONLY_BADGE
+
+    view = fixture_view("base", fake_clock)
+    lines = screen_lines(view, policy_for(width))
+    badged = [ln for ln in lines if READ_ONLY_BADGE in ln]
+    assert len(badged) == 1
+    index = lines.index(badged[0])
+    assert index <= 1  # the title wraps to at most two lines
+    assert cell_len(badged[0]) == width and badged[0].endswith(READ_ONLY_BADGE)
+    title = " ".join(lines[: index + 1]).replace(READ_ONLY_BADGE, "")
+    assert " ".join(title.split()) == " ".join(view.header1.split())  # title text unedited
+    assert all(cell_len(ln) <= width for ln in lines)
+
+
+def test_the_badge_role_is_attention_and_the_title_keeps_its_role(fake_clock):
+    from superclaude.cli.observe.view import READ_ONLY_BADGE
+
+    view = fixture_view("base", fake_clock)
+    first = _compose(view, policy_for(160))[0]
+    assert roles_at(first, READ_ONLY_BADGE) == {"attention"}
+    assert roles_at(first, "ORCA OBSERVER") == {"title"}
+
+
+def test_the_badge_moves_to_the_last_title_line_or_its_own_line_when_it_does_not_fit():
+    from superclaude.cli.observe.render import _title_bar
+    from superclaude.cli.observe.view import READ_ONLY_BADGE
+
+    pol = dataclasses.replace(policy_for(80), width=30)
+    fits_last = _title_bar(["x" * 30, "short"], pol)
+    assert fits_last[0].plain == "x" * 30 and fits_last[1].plain.endswith(
+        READ_ONLY_BADGE
+    )
+    own_line = _title_bar(["x" * 30, "y" * 30], pol)
+    assert len(own_line) == 3 and own_line[2].plain == READ_ONLY_BADGE.rjust(30)
+    ascii_pol = dataclasses.replace(pol, ascii=True)
+    assert _title_bar(["ab"], ascii_pol)[0].plain.isascii()
+
+
+def test_the_record_title_keeps_no_badge(fake_clock):
+    from superclaude.cli.observe.view import READ_ONLY_BADGE
+
+    assert READ_ONLY_BADGE not in record_text(fixture_view("base", fake_clock))
diff --git a/.dev/issues/409/visual-parity/scores/p2/notes.md b/.dev/issues/409/visual-parity/scores/p2/notes.md
new file mode 100644
index 000000000..1bab261ca
--- /dev/null
+++ b/.dev/issues/409/visual-parity/scores/p2/notes.md
@@ -0,0 +1,12 @@
+# Text-defects phase notes (plan Phase 3)
+
+## RB-22 (wide blank band after the id column), spec step 2.6: not applied, deferred (Low row)
+
+Measured at the start of the phase on the `ledger` screen, `base` fixture (`scores/baseline.md`): the longest blank run inside a row is 18 cells at 160 columns (threshold N), 48 at 116 and 34 at 80, so RB-22 fails at 116 and 80.
+
+Why step 2.6 was not applied: the step gives `line` and `short` the full-width id rule (`22 + min(extra, 26)`, rest to the flags column). Worked from the formulas in `_columns`:
+
+- at 116 columns the id column would go from 52 to 48 cells (blank run about 43, still above 18);
+- at 80 columns it would go from 38 to 42 cells (a wider band, not a narrower one).
+
+Reaching N = 18 needs an id column of about 22 cells, which would cut the long identifiers of the `long-identifiers` fixture with `>` in the list. The spec marks the step optional and the row Low, and a Low row may be logged as deferred. RB-22 is deferred with this reason; the rule that column widths stay static between refreshes (finding M-17) is untouched.
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
