4f55b0cb08b2fbea0ff8acafeb15196f4eb4f27c
Review one task for spec compliance.

Task brief: ## Task 3: Add the plan-ask hash fixture, pinning tests and height test

Spec steps 0.6 and 0.7. In `tests/observe/test_render.py` (new R3 block after the test ending at line 967) add a `PLAN_ASK` constant (a plan path, two file paths and `"0123456789abcdef" * 4`, under `ASK_CAP = 400` from `OBS/parse.py:475` and under four desk lines at 80 columns) and these tests: the plan-ask wraps cleanly in the desk at every width in `WIDTHS` (every line `cell_len <= width`, the hash whole on one desk line, the ask intact when not cut); a second fixture with the hash after a long path list that fills `DESK_TEXT_LINES = 4` pinning today's `...` cut; a worker with a 120-character `resource.worktreeId` pinning the continuation indent at `OBS/render.py` lines 347-353; and the canary `HASH not in record_text(view)` and `HASH not in snapshot_json(view)`. In `tests/observe/conftest.py` add `strip_sgr(text)` and `sgr_params(text)` with a self-test. Create `tests/observe/test_height_budget.py` with `test_questions_on_screen_fits_the_height(width, height)` for heights 24, 40, 44; if a height fails on today's code, record the failing heights in `.dev/issues/409/visual-parity/scores/baseline.md` and pin only the passing set (a finding for Phase 4, not a fix here).

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green (baseline 766 passed on 2026-11-17, plus the new tests).
- Both hash canaries pass against `OBS/export.py` unchanged.
- `git diff --stat -- src/` is empty.
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
Start sha: 4f55b0cb08b2fbea0ff8acafeb15196f4eb4f27c
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b: Grep floor; the task adds tests and two test helpers (strip_sgr, sgr_params in tests/observe/conftest.py, new names); no existing symbol changed; no dependents outside the diff.
Evidence: uv run pytest tests/observe/ -q printed '794 passed in 20.52s' (baseline 766); git diff --stat -- src/ is empty. All 30 height cases pass on today's code, so no failing height set exists to record. Touched files: tests/observe/test_render.py, tests/observe/conftest.py (modified, tracked) and tests/observe/test_height_budget.py (new).

diff --git a/tests/observe/conftest.py b/tests/observe/conftest.py
index 3dbd9f7b9..f411a67e4 100644
--- a/tests/observe/conftest.py
+++ b/tests/observe/conftest.py
@@ -8,6 +8,7 @@ from __future__ import annotations
 
 import io
 import json
+import re
 import subprocess
 from datetime import datetime, timedelta, timezone
 from importlib import resources
@@ -351,3 +352,18 @@ def routed_runner_responses(worker, message):
         return pick(argv, timeout) if callable(pick) else pick
 
     return respond
+
+
+# -- styled-output helpers (the screen carries SGR from the colour phase on) ------------------------------
+
+_SGR = re.compile(r"\x1b\[([0-9;]*)m")
+
+
+def strip_sgr(text: str) -> str:
+    """``text`` with every SGR (colour and weight) escape sequence removed."""
+    return _SGR.sub("", text)
+
+
+def sgr_params(text: str) -> set[str]:
+    """The parameter strings of every SGR sequence in ``text`` (for example ``"1;38;2;250;178;25"``)."""
+    return set(_SGR.findall(text))
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 679fc1a3e..f27043435 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -1020,3 +1020,104 @@ def test_r3_the_link_on_keys_line_is_shown_only_with_the_link_on(fake_clock):
     )
     assert view.help_line == QUESTIONS_LINK_KEYS_LINE
     assert any("n/p question" in ln for ln in lines)
+
+
+# -- Q7: a plan-approval ask with a 64-hex hash and paths in the Decision Desk (pins today's behaviour) ------------------
+
+from superclaude.cli.observe.export import record_text, snapshot_json  # noqa: E402
+from tests.observe.conftest import sgr_params, strip_sgr  # noqa: E402
+
+HASH = "0123456789abcdef" * 4
+# Twin of PLAN_ASK in .dev/issues/409/visual-parity/inputs/tools/render_current.py: keep the two identical.
+PLAN_ASK = (
+    "Approve the plan in .dev/plans/observer-visual-parity/plan.md before the worker edits "
+    "src/superclaude/cli/observe/render.py and src/superclaude/cli/observe/terminal.py "
+    f"(plan hash {HASH})?"
+)
+# A path list that fills the four desk lines at 80 columns, with the hash last (under ASK_CAP = 400).
+PATHS_THEN_HASH = (
+    " ".join(f"src/superclaude/cli/observe/module_{i:02d}.py" for i in range(8))
+    + f" {HASH}"
+)
+
+
+def desk_text_lines(lines):
+    """The question-text lines of the unframed Decision Desk: after ``qid  age`` and up to the first field."""
+    desk = lines[lines.index(DESK_TITLE) :]
+    end = next(i for i, ln in enumerate(desk) if ln.startswith("dispatchId:"))
+    return desk[2:end]
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk(
+    fake_clock, width
+):
+    assert len(PLAN_ASK) < 400
+    rows = r3_rows([("w-001", "first?"), ("w-002", PLAN_ASK)])
+    lines, view = r3_screen(fake_clock, rows, 1, width, height=70)
+    assert all(cell_len(ln) <= width for ln in lines)
+    text = desk_text_lines(lines)
+    assert 1 <= len(text) <= 4 and not text[-1].endswith("...")
+    assert sum(HASH in ln for ln in text) == 1  # the hash stays whole on one desk line
+    assert "".join(text).replace(" ", "") == PLAN_ASK.replace(" ", "")  # nothing lost
+    assert HASH not in record_text(view) and HASH not in snapshot_json(view)  # canary
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_r3_a_hash_after_a_long_path_list_is_cut_with_a_mark_at_80_and_116_columns(
+    fake_clock, width
+):
+    assert len(PATHS_THEN_HASH) <= 400  # the parse cap (ASK_CAP) does not cut it
+    rows = r3_rows([("w-001", PATHS_THEN_HASH)])
+    lines, view = r3_screen(fake_clock, rows, 0, width, height=70)
+    assert all(cell_len(ln) <= width for ln in lines)
+    text = desk_text_lines(lines)
+    if width in (80, 116):  # D-6 exception: four lines cut the ask, so the hash is not shown
+        assert len(text) == 4 and text[-1].endswith("...")
+        assert not any(HASH in ln for ln in lines if not ln.startswith("▸ "))
+    else:  # wide enough for the whole ask inside four lines
+        assert sum(HASH in ln for ln in text) == 1
+        assert "".join(text).replace(" ", "") == PATHS_THEN_HASH.replace(" ", "")
+    assert HASH not in record_text(view) and HASH not in snapshot_json(view)  # canary
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_r3_a_120_character_worktree_id_continues_on_two_cell_indented_lines(
+    fake_clock, width
+):
+    worktree = "wt-" + "0123456789" * 11 + "0123456"
+    assert len(worktree) == 120
+    workers = make_rows(3, 1)
+    for row in workers:
+        row["resource"] = {"worktreeId": worktree}
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
+    assert all(cell_len(ln) <= width for ln in lines)
+    start = next(i for i, ln in enumerate(lines) if ln.startswith("resource.worktreeId:"))
+    if width == 160:  # label, space and value (141 cells) fit one line: no continuation
+        assert lines[start] == f"resource.worktreeId: {worktree}"
+        return
+    tail = []
+    for ln in lines[start + 1 :]:
+        if not ln.startswith("  "):
+            break
+        tail.append(ln)
+    assert len(tail) >= 2 and all(ln.startswith("  ") for ln in tail)
+    assert "".join(ln[2:] for ln in tail) == worktree  # hard-split, nothing lost, no marker
+
+
+def test_strip_sgr_removes_colour_codes_and_sgr_params_lists_them():
+    coloured = "\x1b[1;38;2;250;178;25mage\x1b[0m plain \x1b[31mred\x1b[0m"
+    assert strip_sgr(coloured) == "age plain red"
+    assert sgr_params(coloured) == {"1;38;2;250;178;25", "0", "31"}
+    assert strip_sgr("no escapes") == "no escapes" and sgr_params("no escapes") == set()
diff --git a/tests/observe/test_height_budget.py b/tests/observe/test_height_budget.py
new file mode 100644
index 000000000..444a40047
--- /dev/null
+++ b/tests/observe/test_height_budget.py
@@ -0,0 +1,26 @@
+"""The questions-on screen never has more rows than the terminal (pins today's height budget).
+
+On ``Live(screen=True)`` rows past ``policy.height`` are dropped from the bottom, which are the
+footer keys and the ``shown x/y`` line, with no warning. Every phase that adds rows (frames, a
+count strip, a RETAIN CONTEXT pane) keeps this test green.
+"""
+
+from __future__ import annotations
+
+import pytest
+
+from tests.observe.test_render import WIDTHS, policy_for, r3_rows, r3_screen
+
+HEIGHTS = (24, 40, 44)
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+@pytest.mark.parametrize("height", HEIGHTS)
+@pytest.mark.parametrize("count", (3, 20))
+def test_questions_on_screen_fits_the_height(fake_clock, width, height, count):
+    rows = r3_rows([("w-001", f"question {i}?") for i in range(count)])
+    lines, _ = r3_screen(fake_clock, rows, 0, width, height=height)
+    policy = policy_for(width, height=height)
+    assert len(lines) <= policy.height or policy.too_small, (
+        f"{len(lines)} rows at height {height}, width {width}"
+    )
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
