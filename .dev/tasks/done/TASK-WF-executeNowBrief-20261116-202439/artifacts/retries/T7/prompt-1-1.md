36388c552504064bbc9ae8e4d38a3117fefe3ef4
Review one task for spec compliance.

Task brief: ## Task 7: Remove QuestionsPanel.count_text (R2)

Edit `src/superclaude/cli/observe/view.py`: delete the `count_text` field of `QuestionsPanel` (:209) and its assignment `count_text=open_text` (:732). Keep `open_text` (it is also used at :693 and :718) and the other 21 fields; make no comment edits. Do not edit any golden file.

Acceptance criteria:
- Grep for `count_text` over `src/superclaude/cli/observe` and `tests/observe` finds nothing; `open_text` is still used by the counts line and the header cell.
- The panel tests (`tests/observe/test_question_cap.py:71-134`, `tests/observe/test_view.py`, `tests/observe/test_render.py`) and the questions-off golden test (`tests/observe/test_render.py:616-629`) pass with `tests/observe/golden_release1_surface.json` unchanged (`git diff` shows no change to it). The export fields `open_total`, `window_full`, `retained`, `evicted` read at `PKG/export.py:165-168` still work.
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
Start sha: 36388c552504064bbc9ae8e4d38a3117fefe3ef4
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index 1c3a59bac..eaf16dcf3 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -208,3 +208,2 @@ class QuestionsPanel:
     header_cell: str  # the freshness-strip cell, with the same state words
-    count_text: str  # the count as a phrase, never a bare number when it may be partial
     lines: tuple[QuestionLine, ...]  # oldest created first
@@ -731,3 +730,2 @@ def _questions_panel(result: Any, clock: Any) -> QuestionsPanel | None:
         header_cell=header_cell,
-        count_text=open_text,
         lines=lines,
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t7-gate.log):
== grep (each pattern expected to match nothing)
none: count_text
== pytest
.                                                                        [100%]

============================= 685 passed in 22.50s =============================
== ruff
All checks passed!
== open_text still used (counts line and header cell)
649:        open_text = "unknown (no question read yet)"
655:        open_text = retained.open_total_text
657:            open_text += f" (retained {retained.retained})"
660:            open_text = f"{retained.open_total}+ (window full)"
662:            open_text = QUESTIONS_EMPTY_COUNT
692:    counts_line = f"{QUESTIONS_COUNT_LABEL}: {open_text} | {QUESTIONS_CLOSED}"
717:        f"coordinator questions: {QUESTIONS_COUNT_LABEL} {open_text}; {status}; "
== golden file diff (expect empty)
(end)
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
