7980f38fe2c522e8932969aab8b44e68fe32d8ad
Review one task for spec compliance.

Task brief: ## Task 2: Remove the unused CODES set from adapter.py (R1 part)

Edit `src/superclaude/cli/observe/adapter.py`: delete the `CODES` frozenset (:65-82) and reword the comment at :340 (`# a code from CODES, or "exit:<n>"`) so it no longer names `CODES`. Edit `tests/observe/test_adapter.py`: delete only the assertion `assert expected in adapter.CODES` (:719); keep the exact-code assertion at :718 and the rest of `test_error_envelopes_map_to_source_codes_whatever_the_exit_status`.

Acceptance criteria:
- Grep for `\bCODES\b` over `src/superclaude/cli/observe` and `tests/observe` finds nothing.
- `tests/observe/test_adapter.py:718` still asserts the exact source code (`consumer-fenced` and `no-active-terminal`) and the test passes.
- No test function is deleted: the passed count is unchanged and the gate passes. `PKG/adapter.py`'s argv allow-list, forbidden prefixes and error mapping are otherwise unchanged (`git diff` of the file shows only the deleted set and the reworded comment).
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
Start sha: 7980f38fe2c522e8932969aab8b44e68fe32d8ad
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/adapter.py b/src/superclaude/cli/observe/adapter.py
index 3d4c95074..b63b46869 100644
--- a/src/superclaude/cli/observe/adapter.py
+++ b/src/superclaude/cli/observe/adapter.py
@@ -64,20 +64,2 @@ KILL_GRACE_SECONDS = 2.0
 
-# Closed set of source codes besides ``exit:<n>``.
-CODES = frozenset(
-    {
-        "timeout",
-        "spawn-error",
-        "output-cap",
-        "json",
-        "shape",
-        "not-found",
-        "overrun",
-        "cursor-rejected",
-        "cursor-stalled",
-        "empty-page",
-        "consumer-fenced",
-        "no-active-terminal",
-        "no-question-fixture",
-    }
-)
 # Error codes of an ``{"ok": false, "error": {"code": ...}}`` envelope -> source codes.
@@ -339,3 +321,3 @@ class SourceResult:
     pages: tuple = ()  # decoded JSON of each page read, in order
-    code: str | None = None  # a code from CODES, or "exit:<n>"
+    code: str | None = None  # a source code such as "timeout" or "json", or "exit:<n>"
     diagnostic: str = ""  # sanitized stderr, at most 2 KiB
diff --git a/tests/observe/test_adapter.py b/tests/observe/test_adapter.py
index 2071c9ad6..ee6adf88e 100644
--- a/tests/observe/test_adapter.py
+++ b/tests/observe/test_adapter.py
@@ -718,3 +718,2 @@ def test_error_envelopes_map_to_source_codes_whatever_the_exit_status(
     assert (result.state, result.code, result.pages) == ("FAILED", expected, ())
-    assert expected in adapter.CODES
     assert sum(1 for a in argv_log if a[1:3] == ["orchestration", "check"]) == 1
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t2-gate.log):
== grep (each pattern expected to match nothing)
none: \bCODES\b
== pytest
.                                                                        [100%]

============================= 685 passed in 21.87s =============================
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
