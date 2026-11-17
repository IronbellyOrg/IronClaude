736b212197b8efab08d1fff3876cb6759f53d3f8
Review one task for spec compliance.

Task brief: ## Task 5: Remove the synthetic question replay from FixtureSource (R1 part)

Edit `src/superclaude/cli/observe/collector.py`: in `FixtureSource` remove the `question_fixture` constructor argument (:97), `self._question_fixture` (:103), `self._question_index` and the replay loop in `read_questions` (:128-142); keep `read_questions` as a two-line method that returns `SourceResult("FAILED", code="no-question-fixture")` (the `CycleSource` protocol needs it). Edit `tests/observe/test_collector.py`: in `test_a_fixture_source_has_no_question_fixture_unless_one_is_supplied` keep the assertions up to the `no-question-fixture` check (:662-666), delete the synthetic-replay part (:667-678), and rename the test to `test_a_fixture_source_has_no_question_fixture` so the name is true. `--questions` with `--fixture` stays refused by `_question_refusal` in `PKG/commands.py`. Remove the comment `# SYNTHETIC question cycles: ...` (about :102) together with the attributes it describes.

Acceptance criteria:
- Grep for `question_fixture=`, `_question_fixture`, `question_fixture:` and `_question_index` in `src/superclaude/cli/observe` and `tests/observe` finds nothing; the string code `no-question-fixture` and the renamed test name `test_a_fixture_source_has_no_question_fixture` stay, and the synthetic-cycles comment is gone.
- The refusal test for `--questions` with `--fixture` in `tests/observe/test_commands.py` and the collector tests that use `FixtureSource` pass; `FixtureSource` still satisfies the `CycleSource` protocol (the collector tests that build one with `questions=True` pass).
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
Start sha: 736b212197b8efab08d1fff3876cb6759f53d3f8
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/collector.py b/src/superclaude/cli/observe/collector.py
index abf93b5e9..82ff7882c 100644
--- a/src/superclaude/cli/observe/collector.py
+++ b/src/superclaude/cli/observe/collector.py
@@ -96,3 +96,3 @@ class FixtureSource:
 
-    def __init__(self, variant: str, question_fixture: list | None = None) -> None:
+    def __init__(self, variant: str) -> None:
         self.variant = variant
@@ -101,5 +101,2 @@ class FixtureSource:
         self.frozen_positions: frozenset = frozenset()  # of the cycle read last
-        # SYNTHETIC question cycles: each an envelope dict or ``{"fail": <code>}``.
-        self._question_fixture = question_fixture
-        self._question_index = 0
 
@@ -130,12 +127,4 @@ class FixtureSource:
     ) -> SourceResult:
-        """Replay the supplied synthetic question cycles, else fail with a plain code."""
-        if not self._question_fixture:
-            return SourceResult("FAILED", code="no-question-fixture")
-        entry = self._question_fixture[
-            min(self._question_index, len(self._question_fixture) - 1)
-        ]
-        self._question_index += 1
-        if isinstance(entry, dict) and "fail" in entry and "result" not in entry:
-            return SourceResult("FAILED", code=str(entry["fail"]))
-        return SourceResult("OK", pages=(entry,), calls=1)
+        """A fixture source has no question fixture: fail with a plain code."""
+        return SourceResult("FAILED", code="no-question-fixture")
 
diff --git a/tests/observe/test_collector.py b/tests/observe/test_collector.py
index b6dc28a0f..e08745396 100644
--- a/tests/observe/test_collector.py
+++ b/tests/observe/test_collector.py
@@ -661,3 +661,3 @@ def test_exactly_100_rows_sets_window_full_in_the_retained_state(fake_clock, arg
 
-def test_a_fixture_source_has_no_question_fixture_unless_one_is_supplied(fake_clock):
+def test_a_fixture_source_has_no_question_fixture(fake_clock):
     plain = Collector(FixtureSource("base"), fake_clock, run_id=QRUN, questions=True)
@@ -666,13 +666 @@ def test_a_fixture_source_has_no_question_fixture_unless_one_is_supplied(fake_cl
     assert result.question_code == "no-question-fixture"
-    synthetic = [json.loads(question_reply((1, 2))[1]), {"fail": "timeout"}]
-    supplied = Collector(
-        FixtureSource("base", question_fixture=synthetic),
-        fake_clock,
-        run_id=QRUN,
-        questions=True,
-    )
-    first = supplied.run_once()
-    assert first.question_state == "OK" and first.questions.retained == 2
-    second = supplied.run_once()
-    assert (second.question_state, second.question_code) == ("FAILED", "timeout")
-    assert second.questions is first.questions
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t5-gate.log):
== grep (each pattern expected to match nothing)
none: question_fixture=
HITS for _question_fixture:
tests/observe/test_collector.py:662:def test_a_fixture_source_has_no_question_fixture(fake_clock):
none: question_fixture:
none: _question_index
none: SYNTHETIC question cycles
== pytest
.                                                                        [100%]

============================= 685 passed in 22.52s =============================
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
