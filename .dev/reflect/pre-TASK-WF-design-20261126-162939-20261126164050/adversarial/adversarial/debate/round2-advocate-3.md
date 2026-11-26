# Round 2 rebuttal: advocate 3 (Variant 3, reviewer-3, refactorer)

PLAN, DESIGN and REQ mean what they mean in diff-analysis.md. Evidence comes from reading source only. Nothing was run, so every "fails" comes from reading test code.

## Responses to criticisms

- **C-008 / X-006, "nothing forbids an early copy" (V1, V2): partly conceded.** `qa.md:52` does count "editing text the plan reserves for another task" as a breach. But the reviewer sees only "Ti text + AC ids + global constraints" (`qa.md:9`), so Constraint 24 covers an early copy. I withdraw "either way breaches". The finding stands: Task 26 names two `src` files, yet its acceptance runs `test_workflow_command.py`, which compares both trees byte for byte (`:218-220`). PLAN:429 says that test passes because of Task 38's copy.
- **C-016 is a Note (V1): rejected.** Task 34 lists files, not "primitives", and Task 37 adds the string to the docs. Read literally, the check breaks the Task 38 gate. It stays Medium.
- **C-017: kept.** `--stat` counts insertions plus deletions, but NFR-012 (REQ:733) limits net growth.
- C-011, NFR-014, the row 9 label and C-015 as Medium stay conceded.

## Updated view of the other variants

- **V1:** its Round 2 grades are right, and I adopt its X-006 fix. "Feasibility doubtful" is unproven: `SKILL.md` has 215 lines, and most Task 26 additions are one line each.
- **V2:** its T-21/T-04 point changed my C-012 vote, and its T-16 evidence (REQ:679) shapes the C-009 fix. Its Blocking grades for C-013, C-017 and C-020 rest on nothing named. Its C-008 Note ignores PLAN:429.

## New evidence

1. PLAN:429 makes `test_workflow_command.py` passing depend on Task 38's copy, yet PLAN:307 runs it in Task 26.
2. DESIGN:411 named `test_implement_saved_prompt_rule.py` as a pin to read. Lines 91-93 of that test require byte-identical plugin copies of `qa.md`, `ledger.md` and `managed-workspace.md`. Task 31's `-k "implement ..."` selects it by name (not run).
3. C-012: Task 38 check 3 (PLAN:431) needs AC-07 and AC-18, which pass only by T-04 and T-21 (REQ:803, 814). T-21 is "The FR-126 cases" (REQ:684), which include a crash after the resolution append, two resumes and surviving pins (REQ:610). Task 18 omits all three.
4. C-009 needs no test edit. Lifecycle `:686-688` scans only `retry.md`, `ledger.md` and `SKILL.md`, and FR-116 (REQ:592) does not say where the reasons are listed.
5. X-005: FR-064 (REQ:501) and DESIGN:431 carry the 40-line cap, and Task 29 cites FR-054 to FR-067.

## Revised per-point table

| point | vote | right grade or resolution | reason |
|---|---|---|---|
| S-001 | V2 | Note | coverage tables; form only |
| S-002 | V3 | Note | Authorized expansion used as defined |
| C-002 | V3 | Blocking | REQ:475 exclusion missing; safety boundary |
| C-003 | V3 | Blocking | acceptance 2 cannot pass; scope it per REQ:631 |
| C-008 | V3 | Blocking | Task 26 fails its own check; PLAN:429 relies on Task 38 |
| C-012 | V2 (was TIE) | Blocking | Task 38 check 3 needs the cases that Tasks 15 and 18 omit |
| C-013 | V1 | Medium | the stop-on-prompt half is missing; the 600000 ms timeout limits the wait |
| C-017 | V3 (was TIE) | Medium; anchor Note | Task 30 never re-checks the budget; wrong measure |
| C-023 | V2 | Note | FR-064 carries the instruction; only the assertion is missing |
| X-002 | V1 | Medium | the prompt clause is not covered |
| X-003 | V3 | Blocking for both | required exclusion; a check that cannot pass |
| X-005 | NONE | Note: Task 29 names "first 40 lines"; Task 34 asserts it | V2's "no instruction" claim is wrong |
| X-006 | NONE | Blocking: each task copies its own files; Task 38 only verifies | V3 overstated B4; V1/V2 understated B1 |

## Final shared-assumption responses

- **A-001 QUALIFY:** the executor halts only on B1 to B4, judged per task (`qa.md:9`, `:41-52`). Review Blocking also covers defects that pass every check (C-002, C-010, C-011, C-014).
- **A-002 ACCEPT:** the plan runs these suites itself (PLAN:307, 358, 388, 429).
- **A-003 REJECT:** DD-8 and T-16's "unchanged" conflict with needed fixes, so record the overrides in the plan or amend `source.md`.
- **A-004 QUALIFY:** `origin/integration` moves. Record the merge-base SHA in Task 1.

## Necessary plan fixes

Halts:
1. PLAN:29: forbid running or recommending the tokens; allow deny-lists, refusal text and tests (C-001).
2. Task 3: allow `add -A` only with a private index, and test it (C-015).
3. Task 19: move the S23 edit and the routing test to Task 20 (C-004).
4. Task 24 acceptance 2: scan only new files (C-003).
5. Task 25: check `test ! -e`, or use `git rm` (C-005).
6. Tasks 26, 27, 30, 31, 32: copy each changed file to the plugin and `cmp` it; Task 38 only verifies (C-008).
7. Task 31: list both reasons in `refs/commit-step.md` only, or update `_TRANSIENT` and record a T-16 override (C-009).
8. Tasks 15, 18: add the T-04 and T-21 cases (C-012).
9. Task 34: limit the `--commit-tasks` scan to primitive folders (C-016).

Pass every check but ship wrong:
10. Task 13: add the `.dev/implement/` exclusion and a test (C-002).
11. Task 9: add `_HEADER` and `_ARCH` and record the DD-8 override (C-010).
12. Task 12: add a `record-skipped` action (C-011).
13. Task 32: run reconcile only when `commits.md` exists (C-014).
