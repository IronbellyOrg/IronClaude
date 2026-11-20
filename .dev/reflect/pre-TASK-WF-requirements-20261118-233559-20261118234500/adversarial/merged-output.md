<!-- Source: Variant 3 (base, structure and card layout); register content per refactor-plan.md; corrected after the evidence-validator gate (see "Corrections after the gate") -->
# Merged reflection verdict: TASK-WF-requirements-20261118-233559 (pre-execution)

## Verdict

FAIL: 4 blocking (M-1, M-2, M-3, M-5), 8 medium (M-4, M-6 to M-12), 1 note group (M-13).

Plan file: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/TASK-WF-requirements-20261118-233559.md. `plan:N` below means line N of that file; `source.md:N` means line N of source.md next to it. Code paths are relative to src/superclaude/.

## Findings (final register)

Severity follows one rule: what changes if the text is corrected. The plan states a requirement row only where it names one; other entries say "not named in the plan".

### M-1 BLOCKING (Decision)
<!-- Source: Variant 2 (QA-3) -->
- Task: Tasks 14 and 15 (plan:173-189).
- Requirement row: R5 (one launch per sweep, source.md:31).
- Evidence: cli/issue_watch/cycle.py:1099-1109. An unknown launch outcome returns `launch_unknown` and never sets `launched_issue` (set only at 1104). Task 14 prints a `launched:` line only from that field and Task 15 stops after a `launched:` line (plan:183), so a second repo can launch after an uncertain one.
- Fix: `once` also prints a line for an unknown outcome and the dispatcher stops on it; add a test.

### M-2 BLOCKING (Decision)
<!-- Source: Variant 2 (QA-4) -->
- Task: Task 5 (plan:70-80).
- Requirement row: R23 (source.md:47).
- Evidence: cli/issue_watch/cycle.py:1054 builds the prompt, then `_revalidate` is called at 1058. `_revalidate` rereads the project items (1012-1016) but feeds only `project_check` and the approval recheck; nothing compares the reread Status or Pipeline with the ones the prompt uses.
- Fix: build the prompt from the revalidated item, or refuse when Status or Pipeline differ from the examined values; add tests, including a Pipeline lowered between examine and launch.

### M-3 BLOCKING (Missing)
<!-- Source: Variant 3 (F3) and Variant 2 (QA-1) -->
- Task: Task 13 (plan:161-169) and Task 20.
- Requirement row: R18 (source.md:44).
- Evidence: R18 names the shadow run, lock test and restart test as one automatic first-run check. Task 13 runs only config validation, init-state and a dry run. source.md:62 allows leaving some as an owner check, but the plan says neither.
- Fix: add the lock test and restart test to Task 13, or state in Task 13 and Task 20 that they stay an owner check.

### M-4 MEDIUM
<!-- Source: Variant 1 (F1), Variant 3 (F4), Variant 2 (QA-6) -->
- Task: Task 13, Task 20 and the Constraints (plan:25).
- Requirement row: R18.
- Evidence: source.md:60 says switching the watcher on is the owner's decision; R18 (source.md:44) and Task 13 enable it automatically. Precedence is not stated in any file. The owner's chat answers of 2026-11-18 (conversation record, not a file) said every manual step becomes automatic except the approval label and the issue state.
- Fix: Task 20 rewrites source line 60; the Constraints name R18 as superseding it.

### M-5 BLOCKING (Safety, upgraded after the gate)
<!-- Source: Variant 3 (F1), evidence corrected by the evidence-validator -->
- Task: Tasks 4 and 6 (plan:63, plan:84, plan:91).
- Requirement row: R19 (source.md:45).
- Evidence: approval_record.py has two row kinds. The adoption row holds no approver or event id (137-139). Approver and event ids fit only an approval row's `evidence` (140-153), and that row is keyed by plan hash (132-133). WORKER-CONTRACT.md:298 says to create it only when the worker's `ask` carries the plan hash. Task 6 says to create "the approval record" from stored approver and event ids and tests it with just those two ids (plan:84, 91). As worded it fits neither row without inventing a hash, so an implementer could release a worker past its plan boundary on a claim-time label (WORKER-CONTRACT.md:300).
- Fix: Task 4 names which record R19 means; Task 6 acceptance adds that no plan-hash row is created from claim-time fields, and the test must refuse a claim-time event.

### M-6 MEDIUM
<!-- Source: Variant 3 (F2, narrowed) and Variant 2 (QA-2) -->
- Task: Task 4 and Task 20.
- Requirement row: R23 rows (a) to (d) (source.md:47).
- Evidence: the board has four Pipeline values; `/sc:issue` accepts three plus `--submit` (commands/issue.md:43-44, 56). Coordinator duties cover only `--pipeline none` claims (core/WORKER-CONTRACT.md:293), and a push needs the person's go (WORKER-CONTRACT.md:245). source.md:47 still lists (a) to (d) as open; the owner replied "Recommendations approved, proceed" in chat on 2026-11-18 (conversation record, not a file). Task 4 (plan:63) already states (a) and (b).
- Fix: Task 4 states the mapping of the four board values and how `worktree` and `full` launches fit the coordinator duties; Task 20 records the chat approval. Owner to confirm that cron may launch `full` or `full --submit` (push and PR).

### M-7 MEDIUM
<!-- Source: Variant 1 (F4) and Variant 3 (F6) -->
- Task: Tasks 18 and 20.
- Requirement row: not named in the plan.
- Evidence: Task 18 depends only on Task 17 (plan:218); Task 20 depends only on Task 19 (plan:239). Tasks 2, 4 and 6 are in neither chain.
- Fix: Task 18 adds Depends on Tasks 2, 4 and 6; Task 20 depends on all earlier tasks.

### M-8 MEDIUM
<!-- Source: Variant 3 (F7) -->
- Task: Task 16 (plan:193).
- Requirement rows: R14 (source.md:34), R11 (source.md:42).
- Evidence: Task 16 creates labels through `repo_init.py` from the loop; R14 says the loop reports a missing label and R11 says the per-project init creates them.
- Fix: the loop reports, first_run creates.

### M-9 MEDIUM
<!-- Source: Variant 1 (F7) -->
- Task: Task 7 (plan:98).
- Requirement row: R13 (source.md:33).
- Evidence: Task 7 omits `argv_events` (cli/issue_watch/github.py:218) and `argv_comments` (github.py:223); both call `_argv_rest_page`.
- Fix: add both to Task 7.

### M-10 MEDIUM
<!-- Source: Variant 1 (F2) -->
- Task: Task 19 (plan:231).
- Requirement row: R20 (source.md:48).
- Evidence: Task 19 acceptance asks for "the exact value or text the template must use" for R20, which is "open (to verify)".
- Fix: reword to "recorded as open with the reproduction step". R20 is a Coder row, so it is not a plan gap.

### M-11 MEDIUM (partly INFERRED)
<!-- Source: Variant 3 (F8) -->
- Task: Tasks 9 to 13 and 15.
- Requirement row: not named in the plan.
- Evidence: the tasks name real home paths (`~/.config/superclaude/...`, `~/.local/state/...`). The only isolation seen is the `tmp_state` fixture setting HOME and XDG_STATE_HOME (tests/issue_watch/conftest.py:244-248); the rest of conftest.py was not read.
- Fix: require an injectable base directory and a test that nothing is written under the real home.

### M-12 MEDIUM (added after the gate)
<!-- Source: Variant 1 (F5), promoted by the evidence-validator -->
- Task: Task 2 (plan:41).
- Requirement row: R22.
- Evidence: docs/designs/issue-watcher.md:15 says the cycle finds issues "in the Project's Backlog column". Task 2 lists lines 21, 692 and 884 only, so its own acceptance (no line says Backlog allows action) would fail.
- Fix: add line 15 to Task 2.

### M-13 NOTE (unverified items)
<!-- Source: Variant 1, Variant 3 -->
- Task 6: the file list and pytest scope omit tests/commands and some docs (card V1 F6, not checked by the gate).
- Task 11: new REST reads should pass `--method GET` (card V3 F9, not checked).
- cli.py: the group decorator is at line 94 and `def` at 95 (cli/issue_watch/cli.py:94-95), so "line 94" in Task 17 is the decorator line.

## Refuted or not adopted

<!-- Source: refactor-plan.md "Changes not made"; debate-transcript.md -->
- R20 as a plan gap: refuted. R20 is a Coder row (source.md:48); only the M-10 wording fix stands.
- Variant 2's blanket "Blocking" labels: not adopted.

## No-finding list

<!-- Source: Variant 3 -->
- github.py stays read-only in every task that touches it.
- Task 1's allow-list matches R22.
- The 255 s child kill matches R5.
- Task 19's `gh auth status` check is read-only.
- Every line number and symbol the plan cites that the reviewers read matched (about 40 checks).

## Corrections after the gate

The evidence-validator found: M-7 wrongly said Task 18 has no Depends line (fixed to "depends only on Task 17"); M-5 had a wrong sub-claim about the adoption row (corrected from approval_record.py:137-153, and the finding was raised to blocking because that evidence shows the claim-time ids fit only a plan-hash row); M-12 (line 15) was a real gap, not a note (promoted); "R18 is the later owner decision" and "R23 rows are stale" had no file support (reworded as chat records); `record.py:112-113` was dropped from the header since no finding rests on it.

## Not checked

- cli/issue_watch/record.py:381 and the lock behaviour.
- tests/issue_watch/conftest.py beyond lines 244-248; tests/hooks and tests/skills.
- The launch-level hook source and tests/commands.
