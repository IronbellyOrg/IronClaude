5660b16cdd9e54e06b65f186020f0844ce495e19
Review one task for spec compliance.

Task brief: ## Task 1: Remove the unused palette, glyphs and box style from terminal.py and their tests (R1 part, T9)

Before any edit in this plan, save the output of `git status --short` to `./artifacts/baseline-status.txt` in this package (it lists the untracked paths that exist today) so the whole-package check at the end has a baseline.

Edit `src/superclaude/cli/observe/terminal.py`: delete `PALETTE` with the comment above it (:41-42), `_FORBIDDEN_ATTRS` with its comment (:44-53), `palette_style` (:161-172), the glyph entries `sep`, `vrule` and `cross` in the glyph table (:33, :37, :38), the `TerminalPolicy.box_style` property (:72-74), and the imports `from rich import box` (:18) and `from rich.style import Style` (:21) once Grep shows no remaining use in the file. Keep `safe_box=policy.ascii` in `make_console`.

Edit `tests/observe/test_terminal.py`: delete `test_colour_only_where_the_palette_sets_it` (:56-59), `test_palette_refuses_forbidden_styles` and `test_palette_accepts_plain_colour_and_bold` (:73-82), the T28 header comment (:62) and `test_no_blink_code_in_any_console_output` with its parametrize decorator (:65-70); drop the `box_style` assertion at :126; change the two `sep` assertions in `test_glyph_table_maps_to_ascii` (:132-133) to assert the `selected` glyph under the UTF and the ASCII policy instead; remove the `box` and `palette_style` imports if they become unused. The no-blink guard that survives is `tests/observe/test_render.py:182-190` (real screen, every width, both colour modes); do not edit that file in this task.

Acceptance criteria:
- Grep over `src/superclaude/cli/observe` and `tests/observe` finds no `PALETTE`, `_FORBIDDEN_ATTRS`, `palette_style`, `box_style`, or glyph names `"sep"`, `"vrule"`, `"cross"`.
- `tests/observe/test_render.py:182-190` (no blink) still exists and passes; the `safe_box` test around `tests/observe/test_terminal.py:142-149` and the ASCII-mode test pass.
- The task states the number of test functions it deleted (expected 4: the palette-colour test, the forbidden-styles test, the plain-colour test and the no-blink test) and the number of collected cases that disappear (expected 9: the forbidden-styles test runs 5 cases and the no-blink test 2), and the gate passes with the passed count lower by exactly that number.
- `./artifacts/baseline-status.txt` exists and holds the `git status --short` output taken before the first edit.
Global constraints: 
- Shorthand. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. The debate's final list and its row text are copied into `./source.md`; each task below restates what it needs.
- Scope is these eleven rows only. No commit, no push, no pull request. Every other row of the debate (KEEP, owner decisions, low confidence) is out of scope.
- Never touch: the sanitizer (`PKG/sanitize.py` and its use), the argv allow-list and forbidden verbs in `PKG/adapter.py`, process-group kill and output caps, terminal restore on exit and signals, the rule that message bodies, payload and `to_handle` are never kept, snapshot redaction, the disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, `QUESTION_GATE_TEXT` in `PKG/commands.py` (pinned by `TESTS/test_commands.py`), any DIRECTION-SELECTED line, and any file git does not track (for example `.dev/issues/409/handoff-mvp-brainstorm.md`).
- Line numbers in the tasks were read live on 2026-11-16 at HEAD f104ca51a and are leads only: re-grep every target right before editing, because other sessions share the worktree.
- Gate for every task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` passes and `uv run ruff check src/superclaude/cli/observe tests/observe` is clean. The baseline is 694 passed; the passed count falls only by the test functions a task deliberately deletes, and the task states the number it expects and the number it got. UV only; never bare python or pip. A failing gate is reported as a finding and never loosened to pass.
- Edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Whole-package checks, applied by the final review and not tasks of their own: Task 1 first saves `git status --short` to `./artifacts/baseline-status.txt`; at the end `git status --short` differs from that baseline only by the files these tasks name, `.dev/issues/409/` and this package; the full gate passes with the passed count equal to 694 minus the test cases the tasks removed (9 in Task 1 and 1 in Task 9, so 684, unless Task 6 had to remove an aggregate-only test); and `grep -rn "run-use" src/superclaude/cli/observe/` shows `run-use` only in the forbidden set in `PKG/adapter.py` and in the help text that says the observer never runs it.
- Names, not line numbers, wherever a check or a document points at code, because earlier tasks shift line numbers (for example `_question_refusal` in `PKG/commands.py`). A Grep check below means uses of the named symbol, not test function names that merely contain the word (`tests/observe/test_questions.py:50` and `tests/observe/test_view.py:174` keep such names).
- Labels. T5, T7, T8 and T9 in task titles are the debate's row names; the spec test ids in Task 12 are written "spec test T7", "T17", "T45" and "T50".
- Facts the debate found false in the earlier proposal, not to be repeated: the R1 test ranges were too wide, R3 must not drop the five parsed row fields, T9 keeps the `test_render.py` copy and deletes the `test_terminal.py` copy, T7 keeps the 32-character rule and the id rule, T8 keeps all 27 cases, D1 touches owner decisions 6 and 8 only.
Start sha: 5660b16cdd9e54e06b65f186020f0844ce495e19
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/terminal.py b/src/superclaude/cli/observe/terminal.py
index 8cd211433..5c1b36819 100644
--- a/src/superclaude/cli/observe/terminal.py
+++ b/src/superclaude/cli/observe/terminal.py
@@ -17,6 +17,4 @@ from typing import IO
 
-from rich import box
 from rich.cells import cell_len
 from rich.console import Console
-from rich.style import Style
 
@@ -32,3 +30,2 @@ TOO_SMALL_TEXT = f"terminal too small (min {MIN_ROWS} rows)"  # PROPOSED wording
 GLYPHS: dict[str, tuple[str, str]] = {
-    "sep": ("·", "."),
     "selected": ("▸", "@"),
@@ -36,20 +33,4 @@ GLYPHS: dict[str, tuple[str, str]] = {
     "hrule": ("─", "-"),
-    "vrule": ("│", "|"),
-    "cross": ("┼", "+"),
 }
 
-# Palette table (CD-8): empty, so every style is plain text and meaning lives in words.
-PALETTE: dict[str, str] = {}
-
-# Style attributes the observer never uses; the background is never painted either.
-_FORBIDDEN_ATTRS = (
-    "blink",
-    "blink2",
-    "dim",
-    "italic",
-    "underline",
-    "underline2",
-    "conceal",
-)
-
 
@@ -71,6 +52,2 @@ class TerminalPolicy:
 
-    @property
-    def box_style(self) -> box.Box:
-        return box.ASCII if self.ascii else box.SQUARE
-
 
@@ -160,16 +137,2 @@ def ascii_safe(text: str) -> str:
 
-def palette_style(name: str) -> Style:
-    """A palette entry as a ``Style``; refuses blink, faint, italic, underline and backgrounds."""
-    spec = PALETTE.get(name, "")
-    style = Style.parse(spec) if spec else Style.null()
-    for attr in _FORBIDDEN_ATTRS:
-        if getattr(style, attr):
-            raise ValueError(
-                f"palette style {name!r} uses forbidden attribute {attr!r}"
-            )
-    if style.bgcolor is not None:
-        raise ValueError(f"palette style {name!r} paints a background")
-    return style
-
-
 def clip(text: str, width: int, policy: TerminalPolicy) -> str:
diff --git a/tests/observe/test_terminal.py b/tests/observe/test_terminal.py
index dcfd56f08..3f63a2841 100644
--- a/tests/observe/test_terminal.py
+++ b/tests/observe/test_terminal.py
@@ -9,3 +9,2 @@ from pathlib import Path
 import pytest
-from rich import box
 from rich.cells import cell_len
@@ -19,3 +18,2 @@ from superclaude.cli.observe.terminal import (
     make_console,
-    palette_style,
     resolve_policy,
@@ -55,31 +53,2 @@ def test_no_color_unset_or_empty_keeps_colour_available(env):
 
-def test_colour_only_where_the_palette_sets_it():
-    assert terminal.PALETTE == {}  # CD-8: empty palette, plain text
-    assert not palette_style("anything")  # a null style
-    assert "\x1b" not in render(policy(), palette_style("anything"))
-
-
-# -- T28: no blink, faint, italic, underline ------------------------------------
-
-
-@pytest.mark.parametrize("env", [{}, {"NO_COLOR": "1"}])
-def test_no_blink_code_in_any_console_output(env):
-    for style in ("bold", "red", "green on black", "reverse"):
-        out = render(policy(env), style)
-        params = [p for m in SGR.findall(out) for p in m.split(";")]
-        assert "5" not in params and "6" not in params
-
-
-@pytest.mark.parametrize("spec", ["blink", "dim", "italic", "underline", "on red"])
-def test_palette_refuses_forbidden_styles(monkeypatch, spec):
-    monkeypatch.setitem(terminal.PALETTE, "bad", spec)
-    with pytest.raises(ValueError):
-        palette_style("bad")
-
-
-def test_palette_accepts_plain_colour_and_bold(monkeypatch):
-    monkeypatch.setitem(terminal.PALETTE, "ok", "bold red")
-    assert palette_style("ok").bold
-
-
 # -- width classes, height, ASCII -----------------------------------------------
@@ -125,3 +94,2 @@ def test_ascii_mode_from_flag_or_non_utf8_encoding(encoding, flags, expected):
     assert pol.ascii is expected
-    assert pol.box_style is (box.ASCII if expected else box.SQUARE)
 
@@ -131,4 +99,3 @@ def test_glyph_table_maps_to_ascii():
     utf_pol = policy()
-    assert terminal.glyph("sep", utf_pol) == "·"
-    assert terminal.glyph("sep", ascii_pol) == "."
+    assert terminal.glyph("selected", utf_pol) == "▸"
     assert terminal.glyph("selected", ascii_pol) == "@"
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t1-gate.log):
== grep (expect none)
grep-rc=1
== no-blink guard still present
182:def test_no_blink_code_appears_in_any_render(fake_clock):
190:            assert "5" not in params and "6" not in params
== pytest
.                                                                        [100%]

============================= 685 passed in 22.15s =============================
== ruff
All checks passed!
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
