081cf949ba9dd6b478f54815fe09167cc50cf6fa
Review one task for spec compliance.

Task brief: ## Task 6: Remove the two aggregate unrecognised-key counters from parse.py (R3)

Depends on: Task 3

Edit `src/superclaude/cli/observe/parse.py`: delete `ParsedPage.unrecognised_keys` (:177) and its sum in `parse_page`'s return (:409), and `Coverage.unrecognised_keys` (:195) and its sum (:647). Keep `_FIELDS`, `_KNOWN`, `_count_unexpected`, `_BLOCK_FIELDS` (:91-93, the sanitizer block mode), the per-row field and its count (:155, :356), and the inspector line in `PKG/view.py:407`. Adjust only test assertions that read an aggregate counter (a `page.unrecognised_keys` or `coverage.unrecognised_keys` access); the per-row reads in `tests/observe/test_parse.py:188`, `:198`, `tests/observe/test_fixtures.py:145`, `:166` and `tests/observe/test_view.py:722` stay.

Acceptance criteria:
- Grep for `unrecognised_keys` matches only the per-row field, the `_count_unexpected` call in the row builder, `PKG/view.py:407` and the per-row test reads; no page-level or coverage-level counter remains, and `PKG/export.py` and `PKG/view.py` do not read one.
- The row-level tests listed above pass unchanged.
- The gate passes and the passed count equals the count before the task, unless an aggregate-only assertion was removed from an otherwise kept test.
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
Start sha: 081cf949ba9dd6b478f54815fe09167cc50cf6fa
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/parse.py b/src/superclaude/cli/observe/parse.py
index 8b8bd80da..4f5d17ca8 100644
--- a/src/superclaude/cli/observe/parse.py
+++ b/src/superclaude/cli/observe/parse.py
@@ -176,3 +176,2 @@ class ParsedPage:
     malformed_rows: int = 0
-    unrecognised_keys: int = 0
 
@@ -194,3 +193,2 @@ class Coverage:
     malformed_rows: int = 0
-    unrecognised_keys: int = 0
 
@@ -408,3 +406,2 @@ def parse_page(
         malformed_rows=malformed,
-        unrecognised_keys=sum(row.unrecognised_keys for row in rows),
     )
@@ -646,3 +643,2 @@ def merge(
         malformed_rows=sum(page.malformed_rows for page in pages),
-        unrecognised_keys=sum(page.unrecognised_keys for page in pages),
     )
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t6-gate.log):
== grep (each pattern expected to match nothing)
none: page\.unrecognised_keys
none: coverage\.unrecognised_keys
none: sum\(.*unrecognised_keys
== pytest
.                                                                        [100%]

============================= 685 passed in 22.65s =============================
== ruff
All checks passed!
== remaining unrecognised_keys uses (per-row field, call, inspector line, per-row test reads)
src/superclaude/cli/observe/parse.py:155:    unrecognised_keys: int = 0
src/superclaude/cli/observe/parse.py:354:        unrecognised_keys=_count_unexpected(raw, _KNOWN),
src/superclaude/cli/observe/view.py:407:        ("unrecognised keys", f"{row.unrecognised_keys} unrecognised keys"),
tests/observe/test_parse.py:188:    assert row.unrecognised_keys == 5
tests/observe/test_parse.py:198:    assert page([worker()]).rows[0].unrecognised_keys == 0
tests/observe/test_fixtures.py:153:    assert page.rows[2].unrecognised_keys == 0
tests/observe/test_fixtures.py:174:        page.rows[2].unrecognised_keys == 1
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
