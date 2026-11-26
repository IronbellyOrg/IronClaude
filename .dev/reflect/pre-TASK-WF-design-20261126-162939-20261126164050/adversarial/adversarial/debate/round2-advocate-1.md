# Round 2 rebuttal: advocate 1 (Variant 1, reviewer-1, analyzer)

PLAN = TASK-WF-design-20261126-162939.md, DESIGN = source.md, REQ = merged-requirements.md. Read-only; no command run. "Verified" means read in source.

## Responses to criticisms

- **C-002 and C-003 under-graded (V2, V3): conceded.** Both are Blocking. C-002: REQ:475 requires the `.dev/implement/` exclusion and Task 13 omits it, so following the plan can stage legacy-run files (data and safety boundary). C-003: Task 24 acceptance 2 cannot pass as written (`worktree_cleanup.py:2642` is list-form argv, so a text scan never matches it). That is `refs/qa.md:49` (B1, unmet acceptance check), and the fix is to scope the check to files this work adds (REQ:631, T-17).
- **C-008/C-009/C-010 missed: stands as conceded in Round 1.** Verified again: `test_workflow_command.py:207-220` compares plugin and source bytes; `test_task_workspace_lifecycle.py:611, 682-688` pin four transient reasons.
- **C-013 "overstated" (V2, V3, and my own Round 1): partly withdrawn.** NFR-014 (REQ:735) has two halves. The plan realises only the timeout half. A grep of the plan for "prompt" finds no hit, so "stop rather than wait on a credential prompt" appears nowhere. Both "covered" claims are false. It is Medium, not Blocking: the 600000 ms timeout plus the `commit-interrupted` stop bounds the wait, and no named decision changes.
- **C-018 should be Blocking (V2's rule reading): rejected.** Nothing the plan rests on depends on "five"; the executor tests all seven tokens. Medium.
- **"Regression" label stretch:** conceded in Round 1.

## Updated view of the other variants

- **V2:** its T-21 point is real. FR-126 (REQ:610) requires crash after the resolution append, two resumes and surviving pins, and Task 18's acceptance omits them. Its Blocking grades are too high, and it withdrew the "no instruction" claim for the 40-line cap. Its C-008 "NONE" is half right (PLAN:24 means no unavoidable halt) but does not remove the defect.
- **V3:** it conceded C-011 and NFR-014, so its card is now the strongest on blocking defects. Its X-006 reasoning was wrong, the finding right. Its DD-8 argument moved me on A-003.

## New evidence

1. `refs/qa.md:41, 49, 52`: blocking is mechanical (B1 unmet acceptance, B4 quotable constraint). So C-003, C-004, C-005, C-008 and C-009 halt the executor, while C-002, C-010, C-011 and C-014 ship with passing checks.
2. Task 25 copies git files into the plugin inside the same task. Tasks 26 to 32 never do, so the omission for implement files is real and not the plan's convention.
3. REQ:716 (NFR-007) caps refusal logs at 40 lines. FR-064, cited in Task 29, carries it, and Task 18's size checks test only 64 KiB and 200 entries.
4. Task 30 spends the same 15-line budget as Task 26, and no later check re-measures it. `--stat` also reports insertions plus deletions, not net growth.

## Revised per-point table

| point | V1/V2/V3/TIE/NONE | right grade or resolution | reason |
|---|---|---|---|
| S-001 | V2 | Note | explicit tables show coverage scope; my 29-id section answers the brief but is not a layout win |
| S-002 | V3 | Note | uses Authorized expansion as defined (`snapshot_lossless` is a FR-112 expansion) |
| C-002 | V3 | Blocking | REQ:475 rule absent from Task 13; V1 under-graded |
| C-003 | V3 | Blocking | acceptance 2 unsatisfiable; narrow the scan to new code (REQ:631) |
| C-008 | V3 | Blocking | Task 26's own acceptance runs the byte-parity test before any plugin copy exists; Constraint 24 and Task 38 contradict each other |
| C-012 | V2 | Medium | T-21 crash-after-append, two resumes and T-04 refused line are missing sub-cases; Task 38 AC-20 does not replace them |
| C-013 | V1 | Medium | NFR-014 stop-on-prompt half absent; DESIGN:431 narrowed it silently |
| C-017 | V3 | Medium | 15-line budget shared with Task 30 and never re-checked; `--stat` is the wrong measure; line-129 anchor shifts (Note) |
| C-023 | V2 | Note | cap carried by FR-064 citation and PLAN:19; only the assertion is missing |
| X-002 | V1 | Medium | "covered" is false for the prompt clause; "not covered at all" is overstated |
| X-003 | V3 | Blocking for both | acceptance check and required behaviour change |
| X-005 | NONE | Note | V2's "no instruction" is wrong (PLAN:334 plus PLAN:19 carry FR-064); add one sentence and one assertion to Task 29 |
| X-006 | NONE | Blocking (same as C-008) | see fix below |

**X-006 fix.** Constraint 24 (PLAN:24) is right and Task 38 is wrong in kind. Each of Tasks 26 to 32 should end with the plugin copy of the files it changed, as Task 25 does. Task 26's acceptance gains `cmp` for `implement.md` and `SKILL.md`. Task 27 copies `commit-step.md` so the file-set test holds. Task 38 becomes verification and sync only: `cmp`, `diff -r`, `make sync-dev`, `make verify-sync` and the final gate.

## Final shared-assumption responses

- **A-001: QUALIFY.** Review severity is wider than implement's halt model (`qa.md:41-52`): it also covers defects that pass every acceptance check (C-002, C-010, C-011, C-014).
- **A-002: ACCEPT.** The plan names these tests itself (Tasks 26, 30, 31, 34 and 38), and C-008 and C-009 are in checks the plan runs. V2's narrower reading still ends at the Task 38 gate.
- **A-003: REJECT** (changed from QUALIFY). DD-8 and the NFR-014 narrowing start in the design, and PLAN:19 says "the design wins". A plan-only fix needs an explicit override sentence, or `source.md` must change.
- **A-004: QUALIFY.** The baseline log in Task 1 helps. But `origin/integration` is a moving ref outside HEAD's ancestry, and cited line numbers drift. Record the merge-base SHA in Task 1 and compare to it.
