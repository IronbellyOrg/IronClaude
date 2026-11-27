# Qualitative scoring, pass 2 (evaluated in order V3, V2, V1)

Evaluator: independent pass 2. Binary criteria, evidence required. Column order is V1, V2, V3. Evidence from the debate files (round 1 and round 2) was used to rule out claims shown false: V1 "DESIGN:192 lacks hooks_path"; V2 "FR-109, NFR-014, T-14/AC-13 covered" and "no instruction for the 40-line cap"; V3 "NFR-014 covered by Tasks 4 and 29" and the "early copy is a breach" reasoning (withdrawn in round 2).

| id | V1 | V2 | V3 |
|---|---|---|---|
| C1 | 1 - "Spec units audited: 38 plan tasks, DD-1 to DD-11, invariants I1 to I9, and the 29 ids" | 1 - "Read all 38 task bodies and acceptance blocks and the complete design"; "Design sections 3 to 8 and 10" table | 0 - "Not verified: ... the full text of Tasks 13-18 against every FR they cite"; "Not checked: FR-024 to FR-029, FR-037, ... NFR-015, NFR-016" |
| C2 | 1 - row 11: "`git gc --prune=now` between crash and resume", "a mixed batch", stale installed copy | 1 - row 3: "crashing after the resolution append, resuming twice, ... outside-change pins" | 1 - row 6: header-only legacy ledger and trailing `ARCHIVE: failed` give false `LedgerCorrupt` |
| C3 | 1 - row 1: Task 19 runs a test needing the skill file "Task 20 creates"; row 16 incomplete `Depends on:` lines | 0 - only dependency content is the note "F2 confirmed, not a blocker for this executor (source order)"; it missed the Task 19 / Task 20 ordering defect (C-004) | 1 - row 2: "`sc-git-protocol/SKILL.md` is created only in Task 20"; row 15 incomplete `Depends on:` lines |
| C4 | 0 - no verdict; adherence summary only ("Blocking: 4 (rows 1-4)"), no pass/fail or gate condition | 1 - "Reviewer verdict: FAIL (contradictory checks and acceptance gaps)" | 1 - "fix rows 1-9 before `/sc:implement`" with a named fix per row |
| C5 | 1 - "UNVERIFIED: every file in `commands/` is tracked ... `origin/integration` resolves"; "Unread: `refs/ledger.md` lines 127 and 139" | 1 - "No tests or commands were run. Real hook-framework behavior, the git version floor and CI submodule behavior remain UNVERIFIED" | 1 - "Not verified: `WORKER-CONTRACT.md:247` ..."; "Evidence limits: ... No tests were run" |
| K1 | 0 - states DESIGN:192 "lacks `snapshot_lossless` and `hooks_path`" (R1 adv3: line lists `hooks_path`); "Fully adherent: 23 tasks" overclaimed (Task 9 wrong, conceded) | 0 - lists FR-109, NFR-014 and T-14/AC-13 as covered (shown false, X-001/X-002/C-004); "no implementation instruction" for the 40-line cap withdrawn | 0 - notes "NFR-014 by Tasks 4, 29" (shown false, conceded); row 1 "treats ... as a breach" withdrawn in round 2 |
| K2 | 1 - row 3 fix "`test -e` check and the work-tree count"; row 1 "move the fixture edit ... or create a stub skill" | 1 - row 1 "Limit the prohibition to executing or recommending bypasses"; row 5 "Keep the check scoped to new production code" | 1 - recommended action: per-task plugin copy, move S23 change to Task 20, add `_TRANSIENT` update to Task 31 (adopted by advocates 1 and 3 in round 2) |
| K3 | 0 - "Regression" on planned omissions and "Regression (internal conflict)" (conceded "label stretch"); "Drift (missing task)" off-taxonomy | 0 - all ten rows start "Blocking" but labels mix HIGH/MEDIUM (rows 5-10); "Regression" for planned omissions (withdrawn) | 1 - uses "Authorized expansion" as defined (row 13); grade and label agree except row 9 (S-002 and S-003 debate result: V3 best taxonomy) |
| K4 | 0 - summary "Drift 14, Regression 2" vs table: rows 1, 3, 5 are Regression (13 Drift); "Fully adherent: 23" vs 17 tasks listed with findings | 0 - "Total deviations: 10" vs summary "Drift 18 \| Regression 3"; FR-109 "covered" while rows 3, 6, 7 report FR-109/T-21/T-04 gaps | 0 - row 1 says early plugin copy "treats as a breach" while the recommended action says "copy each implement-side file into the plugin in the same task"; Tasks 17 and 27 listed adherent while rows 11 and 1 cite them |
| K5 | 1 - every row has a file:line cell, e.g. row 4 "DESIGN:290-291; REQ:551, 576, 580" | 1 - every row cites PLAN/DESIGN lines; row 5 cites `tests/worktree_cleanup/test_git_facts.py:217` | 1 - rows cite tests, e.g. row 3 `test_task_workspace_lifecycle.py:611, 682-688` |
| S1 | 1 - Deviations, Adherence summary, 29 ids, Notes | 1 - Deviations, unmapped IDs, design sections, adherence, notes | 1 - Deviations, Correctness gaps, Adherence, Notes |
| S2 | 1 - H2 sections with one H3 "The 29 ids" under the summary | 1 - five H2 sections, flat | 1 - four H2 sections, flat |
| S3 | 1 - findings table apart from adherence summary and notes | 1 - separate tables for unmapped IDs and design sections | 1 - advisory "Correctness gaps" table apart from deviations |
| S4 | 1 - numbered rows; row cross-references ("rows 1 and 3", "row 5") | 1 - numbered rows; summary refers to "row 9", "rows 4, 8" | 1 - numbered rows; "fix rows 1-9"; "T1 lead F1" cross-refs |
| S5 | 1 - header, Deviations table with the six agent columns, adherence summary, notes (no Timestamp line) | 1 - same columns; adds verdict line and extra tables (no Timestamp line) | 1 - same columns plus correctness-gap table in the agent's format (no Timestamp line) |
| L1 | 1 - grades and labels agree on all 16 rows (R1 adv1: "Blocking=HIGH, Medium=MEDIUM, Note=LOW") | 0 - six rows read "Blocking (Missing)" but are labelled MEDIUM (rows 5-10) | 1 - only row 9 mismatches ("Blocking (Decision)" / MEDIUM); every other row is unambiguous |
| L2 | 1 - cites exact tokens and lines, e.g. row 7 lists the seven refusal tokens | 1 - names concrete fields (`header_len`, `rule`, `runs`, `segments`) | 1 - names five hit files for the Task 24 scan |
| L3 | 1 - each section has one purpose (findings, counts, 29 ids, notes) | 1 - each table has a stated purpose | 1 - each section has one purpose |
| L4 | 0 - defines only PLAN/DESIGN/REQ; FR, NFR, DD-8, T-nn, Q0, "T1 F1" undefined | 0 - defines only PLAN/DESIGN/REQ; "T-21", "FR-109", "I4" undefined | 0 - defines only PLAN/DESIGN/REQ; "Q0 method", "DD-8", "T1 lead F1" undefined |
| L5 | 0 - "Fix:" only on rows 1-3; rows 4-16 and the card have no next-step list | 0 - fix text only on rows 1 and 5; no consolidated next steps | 1 - "Reviewer's recommended action: fix rows 1-9 before `/sc:implement`: copy each implement-side file ..." |
| R1 | 1 - rows 1-4 Blocking, 5-13 Medium (grade as impact), each naming the affected action | 1 - rows 1-10 graded Blocking with named affected checks (e.g. row 1 Tasks 3 and 29) | 1 - rows 1-9 Blocking with "Affected action: QA verdicts of Tasks 26, 27, 30, 31, 34" |
| R2 | 0 - fixes given for rows 1-3 only; rows 4-16 have none | 0 - fixes given for rows 1 and 5 only | 1 - recommended action gives a fix for each Blocking row 1-9 |
| R3 | 1 - row 2 "every QA review of Tasks 3, 13, 15, 21, 29, 34" gets a blocking `quoted-constraint-breach` | 1 - row 5 "Task 24's check cannot pass literally"; row 3 crash and resume proof missing | 1 - row 6 "False failures: a fresh legacy ledger ... at Wave 0 step 6b `reconcile`" |
| R4 | 1 - row 1 `test_routing_refresh.py:101-107`; row 12 `origin/integration` may move | 1 - row 5 existing cleanup tests `test_git_facts.py:217` | 1 - row 1 byte-parity tests `test_workflow_command.py:204-220`; row 3 `_TRANSIENT` pin |
| R5 | 1 - row 3 fix "`test -e` check and the work-tree count"; row 12 compare to merge-base | 1 - rows 2-3, 6-9 name the missing assertion that would prove the behaviour | 1 - fix names "filesystem checks in Task 25", "narrow Task 24 AC2" |
| E1 | 1 - row 4 `reason=empty` skip with no producing step | 1 - row 7 "when no sidecar exists ... appends exactly one `off` record when one exists" | 1 - row 6 header-only ledger; row 9 no `commits.md` |
| E2 | 1 - row 9 the 15-line budget shared by Tasks 26 and 30 | 1 - row 3 outside-change pins must survive crash, resume and both answers | 1 - row 12 line 129 shifts after Task 26 inserts steps 5b and 6b |
| E3 | 1 - row 8 missing `.dev/implement/` exclusion; row 13 no prompt-stop rule | 1 - row 4 missing exclusion; row 2 no assertion rejecting agent or plan-origin writes | 1 - row 9 no `commits.md` guard before `reconcile`; row 8 exclusion missing |
| E4 | 1 - row 7 "acceptance says 'each of the five refusal tokens'" vs seven listed | 1 - notes "199-id denominator ... includes 18 unused or deleted ids; not 199 active requirements" | 1 - row 5 count 21 vs 20; row 14 README says four, should name five |
| E5 | 1 - row 5 `FORBIDDEN_FLAGS` `-A` (Task 3) vs `add -A` in Task 15 | 1 - row 5 Task 24 check collides with existing tests that Task 1 reserves unchanged | 1 - row 10 Task 37 docs plus `make sync-dev` break the Task 34 "appears only in" check |

## Subtotals (out of 5 per dimension unless noted)

| dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness (C1-C5) | 4 | 4 | 4 |
| Correctness (K1-K5) | 2 | 2 | 3 |
| Structure (S1-S5) | 5 | 5 | 5 |
| Clarity (L1-L5) | 3 | 2 | 4 |
| Risk Coverage (R1-R5) | 4 | 4 | 5 |
| Invariant and Edge Case (E1-E5) | 5 | 5 | 5 |

## Totals (out of 30)

- V1: 23
- V2: 22
- V3: 26
