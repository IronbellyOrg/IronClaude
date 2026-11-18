555688d0d4fcc758d3cb236581f152029bf5675b
Review one task for spec compliance.

Task brief: ## Task 11: Mark owner decisions 6 and 8 as decided where they are still listed as open (D1)

Depends on: Task 10

In place only, mark open owner decision 6 (permission to read the question scope) and open owner decision 8 (what identifies a human question) as decided by `.dev/issues/409/owner-decisions-20261111.md` (decision 6: "Permission granted, proceed", one named Run, `--types question`, never run-use; decision 8: "coordinator questions only") in `.dev/issues/409/bmad/spec-orca-observer/SPEC.md` lines 104 and 106 and `.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md` lines 22 and 24; check `.dev/issues/409/bmad/prd-orca-observer/prd.md` lines 423 (OQ-5) and 469 (12.3 item 6) and fix the same rows if they still read as open. Do not collapse the lists, do not replace prd.md section 12.1 with a pointer (the OQ-n labels exist only there), and leave decision 5 (fallback date) open.

Acceptance criteria:
- Each of the rows named above says decided and cites `owner-decisions-20261111.md` by path; the decision numbering and the OQ-n labels still resolve (Grep for `OQ-5` and `open owner decision 6` finds the same labels as before).
- Decision 5 (fallback date) and every other open row are unchanged (`git diff` touches only the rows named).
- The gate passes with the passed count unchanged (document-only task).
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
Start sha: 555688d0d4fcc758d3cb236581f152029bf5675b
Diff against the start snapshot: diff --git a/.dev/issues/409/bmad/prd-orca-observer/prd.md b/.dev/issues/409/bmad/prd-orca-observer/prd.md
index c7889fef3..f68048cd7 100644
--- a/.dev/issues/409/bmad/prd-orca-observer/prd.md
+++ b/.dev/issues/409/bmad/prd-orca-observer/prd.md
@@ -422,3 +422,3 @@ Recorded dissents (owner-decisions-and-risks.md): `page.total` required (V1) ver
 - **OQ-4.** Fallback date for QUESTION-OBSERVATION?
-- **OQ-5.** Sample capture and acquisition permission for live reads (open owner decision 6)?
+- **OQ-5.** Decided 2026-11-11 (`.dev/issues/409/owner-decisions-20261111.md`): sample capture and acquisition permission for live reads (open owner decision 6); granted for one named Run, `--types question`, never `run-use`.
 - **OQ-6.** Message-content exposure (open owner decision 7)?
@@ -468,3 +468,3 @@ The recommendations are the spec's, recorded for the owner. None is a decision.
 5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option. (OQ-4)
-6. **Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, with the owner setting redaction rules. Unblocks B's headline panel. (OQ-5)
+6. **Sample capture and acquisition permission. Decided 2026-11-11 in `.dev/issues/409/owner-decisions-20261111.md`: granted for one named Run, `--types question`, never `run-use`.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, with the owner setting redaction rules. Unblocks B's headline panel. (OQ-5)
 7. **Message-content exposure.** What may be displayed and what exported, kept as separate permissions; no recommendation beyond that. (OQ-6)
diff --git a/.dev/issues/409/bmad/spec-orca-observer/SPEC.md b/.dev/issues/409/bmad/spec-orca-observer/SPEC.md
index ee1eacb74..c799c76fd 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/SPEC.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/SPEC.md
@@ -103,5 +103,5 @@ Pain to solve. One human supervising 5-10 Orca orchestrators and 50-100 sessions
 - Fallback date for QUESTION-OBSERVATION?
-- Sample capture and acquisition permission for live reads (open owner decision 6)?
+- Decided 2026-11-11 (`.dev/issues/409/owner-decisions-20261111.md`): sample capture and acquisition permission for live reads (open owner decision 6); granted for one named Run, `--types question`, never `run-use`.
 - Message-content exposure (open owner decision 7)?
-- What identifies a human question (open owner decision 8)?
+- Decided 2026-11-11 (`.dev/issues/409/owner-decisions-20261111.md`): what identifies a human question (open owner decision 8); coordinator questions only, messages of type `question`.
 - Multi-observer restriction (open owner decision 9)?
diff --git a/.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md b/.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md
index 36a7a68ba..13ec42508 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md
@@ -21,5 +21,5 @@
 5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option.
-6. **Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, owner sets redaction rules. Unblocks B's headline panel.
+6. **Sample capture and acquisition permission. Decided 2026-11-11 in `.dev/issues/409/owner-decisions-20261111.md`: "Permission granted, proceed" for one named Run, `--types question`, never `run-use`.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, owner sets redaction rules. Unblocks B's headline panel.
 7. **Message-content exposure.** What may be displayed and what exported; kept as separate permissions; no recommendation beyond that.
-8. **Question-type choices.** What makes a message a "human question", which `type` values count, which handle or Run carries it. Needs the owner or Orca. Recommend an explicit message type, never text inference.
+8. **Question-type choices. Decided 2026-11-11 in `.dev/issues/409/owner-decisions-20261111.md`: "coordinator questions only", messages of type `question`.** What makes a message a "human question", which `type` values count, which handle or Run carries it. Needs the owner or Orca. Recommend an explicit message type, never text inference.
 9. **Multi-observer restriction.** Caps are per process, no singleton. Recommend disclosure only.
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t11-gate.log):
== grep (each pattern expected to match nothing)
== pytest
.                                                                        [100%]

============================= 684 passed in 23.68s =============================
== ruff
All checks passed!
== labels still resolve (open owner decision 6 / 8, OQ-5)
.dev/issues/409/bmad/spec-orca-observer/SPEC.md:104:- Decided 2026-11-11 (`.dev/issues/409/owner-decisions-20261111.md`): sample c
.dev/issues/409/bmad/spec-orca-observer/SPEC.md:106:- Decided 2026-11-11 (`.dev/issues/409/owner-decisions-20261111.md`): what ide
.dev/issues/409/bmad/prd-orca-observer/prd.md:423:- **OQ-5.** Decided 2026-11-11 (`.dev/issues/409/owner-decisions-20261111.md`): 
.dev/issues/409/bmad/prd-orca-observer/prd.md:469:6. **Sample capture and acquisition permission. Decided 2026-11-11 in `.dev/issu
== rows changed (git diff vs task start, line counts)
 .dev/issues/409/bmad/prd-orca-observer/prd.md                        | 4 ++--
 .dev/issues/409/bmad/spec-orca-observer/SPEC.md                      | 4 ++--
 .dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md | 4 ++--
 3 files changed, 6 insertions(+), 6 deletions(-)
== decision 5 (fallback date) rows unchanged
.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md:21:5. **Fallback deadline.** Date by which QUESTION
.dev/issues/409/bmad/spec-orca-observer/SPEC.md:103:- Fallback date for QUESTION-OBSERVATION?
.dev/issues/409/bmad/prd-orca-observer/prd.md:422:- **OQ-4.** Fallback date for QUESTION-OBSERVATION?
.dev/issues/409/bmad/prd-orca-observer/prd.md:468:5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass
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
