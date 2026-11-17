d439ffdf0cf3ceb3bacf1bc5f191ebb59a07f74f
Review one task for spec compliance.

Task brief: ## Task 12: Correct the test-id bookkeeping in acceptance-tests.md (D13)

Edit `.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md`. In the section "Snapshot schema test (CAP-10, recorded owner decision 2)" (about line 64-66) replace "Test ID not yet assigned." with the real test file, `tests/observe/test_snapshot_schema.py`. Mark T7, T17, T45 and T50 as "not built / no automated test" with a reason: T7 and T17 are defined inside the AC-3 and AC-6 mapping rows (about lines 25 and 28), so add the note there (spec test T7 cannot run as written because `_question_refusal` in `src/superclaude/cli/observe/commands.py` refuses `--questions` with `--fixture`; for T17 state that no test cites it); T45 and T50 are table rows (about lines 51 and 56): T45's `read k of N Runs since start` header text is not built, and T50 is a reviewer check on design images, not a test. Re-grep the live file for the exact lines first. Strike nothing; the T45 (OQ-13) and T50 (AC-S input) references stay.

Acceptance criteria:
- The four test ids each carry the words `not built` or `no automated test` with a stated reason, and the snapshot schema section names `tests/observe/test_snapshot_schema.py` instead of "not yet assigned".
- Every test id and table row that existed before the edit is still present (compare `grep -c` of the `| T<n> |` rows and of the ids T1 to T56 before and after), and the OQ-13 and AC-S input references are intact.
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
Start sha: d439ffdf0cf3ceb3bacf1bc5f191ebb59a07f74f
Diff against the start snapshot: diff --git a/.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md b/.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md
index f19ce5d47..7e26a849b 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md
@@ -24,6 +24,6 @@ AC-1..AC-10 are restated from the seed brief. The mapping was re-checked on 2026
 | AC-2 | Deterministic, bounded collection | T4: a fake always returning `hasMore=true` stops at the 5-call cap and renders `PARTIAL: collected 500 of reported T`. T5: a fake sleeping past a configured per-call timeout injected into the fake runner (the real value is measured at the first permitted live read) shows `FAILED (timeout)`; the cycle ends within the 15 s budget. T6: same input renders byte-identical text twice. |
-| AC-3 | Attention items, reasons, scope, changes since last look, evidence | T7: `base` (8 orchestrators, 80 sessions) in fixture mode lists every question oldest first with requester/owner and affected IDs. T8: after `m`, a fixture step changing one `nextAction.kind` stars exactly that row and shows `changed since HH:MM (1)`. T9: live mode with no message source shows `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` (`rendering-rules.md`) and titles the ledger `worker-reported, not questions`. |
+| AC-3 | Attention items, reasons, scope, changes since last look, evidence | T7: `base` (8 orchestrators, 80 sessions) in fixture mode lists every question oldest first with requester/owner and affected IDs (not built / no automated test: spec test T7 cannot run as written, because `_question_refusal` in `src/superclaude/cli/observe/commands.py` refuses `--questions` with `--fixture`). T8: after `m`, a fixture step changing one `nextAction.kind` stars exactly that row and shows `changed since HH:MM (1)`. T9: live mode with no message source shows `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` (`rendering-rules.md`) and titles the ledger `worker-reported, not questions`. |
 | AC-4 | Seen is not resolved | T10: `m` on every item leaves the open count unchanged. T11: `source-loss` keeps the open count and every retained item; nothing becomes resolved or failed. T12: an item missing next cycle stays, marked `no longer in source window`. |
 | AC-5 | Separate lifecycle, outcome, report, acceptance, tests, approval; unknown never 0/false | T13: `missing-fields` renders `unknown` for every absent field; `0`/`false` never stand in (asserted per field). T14: `terminalState=released` with `outcome` absent never renders `done`, `complete` or `settled`. T15: report, acceptance, tests and approval each render `unavailable (no source)` live; no row or inspector ever renders `admitted` from evidence fields (inspectable evidence is not admission). |
-| AC-6 | Filtered and global counts with denominators; 100-row cap disclosed | T16: matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders); every count line matches `k of n`, every hidden overflow shows `x/y shown` with y = fixture total. T17: `uneven` per-owner counts sum to the global count. T18: `page.total=287` with 100 rows shows `collected 100 / reported 287`, never `287 workers`; `page.total` absent shows `reported unknown`. T19 (R2, no longer a placeholder; fake-runner test with `--questions` on): the question panel carries the disclosure verbatim, `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost`, under the title `COORDINATOR QUESTIONS` and the line `one Run only: <runId>`; its first state line reads `question read: OK 3s` (or the other state forms), its counts line reads `seen, not resolved: <n> | closed by evidence: unavailable (no source)`, and `no read marker in source: answered questions stay listed` is present. |
+| AC-6 | Filtered and global counts with denominators; 100-row cap disclosed | T16: matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders); every count line matches `k of n`, every hidden overflow shows `x/y shown` with y = fixture total. T17: `uneven` per-owner counts sum to the global count (not built / no automated test: no test cites T17). T18: `page.total=287` with 100 rows shows `collected 100 / reported 287`, never `287 workers`; `page.total` absent shows `reported unknown`. T19 (R2, no longer a placeholder; fake-runner test with `--questions` on): the question panel carries the disclosure verbatim, `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost`, under the title `COORDINATOR QUESTIONS` and the line `one Run only: <runId>`; its first state line reads `question read: OK 3s` (or the other state forms), its counts line reads `seen, not resolved: <n> | closed by evidence: unavailable (no source)`, and `no read marker in source: answered questions stay listed` is present. |
 | AC-7 | No one-to-one session/worktree assumption | T20: `shared-unmapped` shows two sessions sharing one worktree as two rows; opening the inspector on each shows the same `resource.worktreeId`, and the inspector of the session with no worktree shows `unknown (absent in source)` for it; no count divides one by the other, and no `conflict` label appears for the shared worktree. |
@@ -50,3 +50,3 @@ AC-1..AC-10 are restated from the seed brief. The mapping was re-checked on 2026
 | T44 | Worker text containing Rich markup (e.g. `[bold]`) renders literally. | AC-10 |
-| T45 | Default view chosen at start-up, never switches mid-session; header shows `read k of N Runs since start` (which views carry it is an open question, `SPEC.md`). | AC-3 |
+| T45 | Default view chosen at start-up, never switches mid-session; header shows `read k of N Runs since start` (which views carry it is an open question, `SPEC.md`). Not built / no automated test: the `read k of N Runs since start` header text is not built (release 2 reads one Run only). | AC-3 |
 | T46 | For the one named Run, at 1,001 retained questions (distinct Run plus `message.id`), eviction does not lower the seen-not-resolved total; the counts line reads `seen, not resolved: unknown (retention exceeded) (retained 1000)` (and the collapsed one-line summary reads `unknown (retention exceeded)`, never a bare number); oldest first. Test file: `tests/observe/test_questions.py` and `test_view.py`. | AC-4 |
@@ -55,3 +55,3 @@ AC-1..AC-10 are restated from the seed brief. The mapping was re-checked on 2026
 | T49 | When height cannot hold coverage, scope, PARTIAL and the question-source gap notice ahead of optional panels, a too-small diagnostic shows and still carries the gap notice. | AC-9 |
-| T50 | R0 renders of A, B, C at 160/116/80 each carry "synthetic fixture, not live evidence" with a degraded version beside each. | AC-S input |
+| T50 | R0 renders of A, B, C at 160/116/80 each carry "synthetic fixture, not live evidence" with a degraded version beside each. Not built / no automated test: this is a reviewer check on design images, not a test. | AC-S input |
 | T51 | R2, no longer a placeholder (`tests/observe/test_question_quiet_scope.py`): a stateful fake Orca backend over the probe shapes first establishes readable identity (every row has a `msg_` id, a Run id and a created time), then repeated reads on a quiet scope return identical question ids, order and an unchanged fake mailbox state; a consuming fake makes the companion test fail; a pass covers only the visible effects tested, as the Run's owner on a probe Run, and says nothing about a non-owner reader (Q-1) (INV-022). | AC-1 |
@@ -65,3 +65,3 @@ AC-1..AC-10 are restated from the seed brief. The mapping was re-checked on 2026
 
-- Validates every R1 snapshot against `snapshot-export-schema.md`; rejects an unknown `schemaVersion` major; asserts missing values are the string `UNKNOWN`; asserts no message bodies, prompts, file contents or credentials. Test ID not yet assigned.
+- Validates every R1 snapshot against `snapshot-export-schema.md`; rejects an unknown `schemaVersion` major; asserts missing values are the string `UNKNOWN`; asserts no message bodies, prompts, file contents or credentials. Test file: `tests/observe/test_snapshot_schema.py`.
 
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t12-gate.log):
== grep (each pattern expected to match nothing)
== pytest
.                                                                        [100%]

============================= 684 passed in 22.82s =============================
== ruff
All checks passed!
== test ids before and after the edit
before: rows=24 T-ids=56
after:  rows=24 T-ids=56
== the four ids and the schema section
28:T17: `uneven` per-owner counts sum to the global count (not built / no automated test: no test cites T17
66:- Validates every R1 snapshot against `snapshot-export-schema.md`; rejects an
0
== OQ-13 / AC-S references intact
51:| T45 | Default view chosen at start-up, never switches mid-session
56:| T50 | R0 renders of A, B, C at 160/116/80 each carry "synthetic f
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
