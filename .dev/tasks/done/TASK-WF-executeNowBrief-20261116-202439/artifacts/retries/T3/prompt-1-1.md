9865e9e9d8118b38b379c1ff6e51dae26c9b52ca
Review one task for spec compliance.

Task brief: ## Task 3: Remove Fixture.parse from parse.py and route its test callers through parse_page and apply_frozen (R1 part)

Edit `src/superclaude/cli/observe/parse.py`: delete the `Fixture.parse` method (:723-733). Keep `Fixture.cycle` and `apply_frozen` (:736; also used by `PKG/collector.py:297`). Edit `tests/observe/test_fixtures.py`: the three callers (`fixture.parse(...)` at :44, :141 and :149) must call `parse_page(cycle.envelope, namespace, cycle_number, source_rank_base)` followed by `apply_frozen(parsed, cycle.frozen, source_rank_base)` through one small local helper in the test file, with the same arguments the removed method used. Add `apply_frozen` to the existing `from superclaude.cli.observe.parse import (...)` block at `tests/observe/test_fixtures.py:14-19` (`parse_page` is already imported there). The frozen-marker test (`test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true`, spec test T34) and `test_every_variant_loads_and_every_cycle_parses` keep their names and assertions.

Acceptance criteria:
- Grep for `fixture.parse(` and `def parse(` inside the `Fixture` class finds nothing; `apply_frozen` and `parse_page` are still used by `PKG/collector.py`.
- Both tests named above pass with their original assertions, including that only `w-003` is frozen and that the source-rank offsets are honoured.
- No test function is deleted: the passed count is unchanged and the gate passes.
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
Start sha: 9865e9e9d8118b38b379c1ff6e51dae26c9b52ca
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/parse.py b/src/superclaude/cli/observe/parse.py
index 9eb842e7a..8b8bd80da 100644
--- a/src/superclaude/cli/observe/parse.py
+++ b/src/superclaude/cli/observe/parse.py
@@ -722,14 +722,2 @@ class Fixture:
 
-    def parse(
-        self, index: int, namespace: str, cycle: int, source_rank_base: int = 0
-    ) -> ParsedPage:
-        """Parse a non-failing cycle with ``parse_page``, then mark frozen rows."""
-        entry = self.cycle(index)
-        if entry.envelope is None:
-            raise ValueError(
-                f"fixture cycle {index} is a failure ({entry.fail}), it has no page"
-            )
-        parsed = parse_page(entry.envelope, namespace, cycle, source_rank_base)
-        return apply_frozen(parsed, entry.frozen, source_rank_base)
-
 
diff --git a/tests/observe/test_fixtures.py b/tests/observe/test_fixtures.py
index d9ed6803c..be0c9e000 100644
--- a/tests/observe/test_fixtures.py
+++ b/tests/observe/test_fixtures.py
@@ -16,2 +16,3 @@ from superclaude.cli.observe.parse import (
     VARIANTS,
+    apply_frozen,
     load_fixture,
@@ -24,2 +25,9 @@ ROOT = Path(__file__).resolve().parents[2]
 
+def parse_cycle(fixture, index, namespace, cycle, source_rank_base=0):
+    """Parse a non-failing fixture cycle with ``parse_page``, then mark its frozen rows."""
+    entry = fixture.cycle(index)
+    parsed = parse_page(entry.envelope, namespace, cycle, source_rank_base)
+    return apply_frozen(parsed, entry.frozen, source_rank_base)
+
+
 def fixture_files():
@@ -43,3 +51,3 @@ def test_every_variant_loads_and_every_cycle_parses(variant):
             continue
-        page = fixture.parse(index, f"fixture:{variant}", index + 1)
+        page = parse_cycle(fixture, index, f"fixture:{variant}", index + 1)
         assert page.raw_count == len(cycle.envelope["result"]["workers"])
@@ -140,3 +148,3 @@ def test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true()
     fixture = load_fixture("base")
-    page = fixture.parse(0, "fixture:base", 1)
+    page = parse_cycle(fixture, 0, "fixture:base", 1)
     frozen = [r.dispatch_id for r in page.rows if r.fixture_frozen]
@@ -148,3 +156,3 @@ def test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true()
         r.dispatch_id
-        for r in fixture.parse(0, "fixture:base", 1, 100).rows
+        for r in parse_cycle(fixture, 0, "fixture:base", 1, 100).rows
         if r.fixture_frozen
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t3-gate.log):
== grep (each pattern expected to match nothing)
none: fixture\.parse\(
none: ^    def parse\(
== pytest
.                                                                        [100%]

============================= 685 passed in 23.47s =============================
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
