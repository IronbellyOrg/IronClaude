# Round 1 — Advocate C (refactorer card)

## Steelman
- **A** covers the most acceptance criteria. Only A found that the Task 10 mode check cannot be observed (P:191) and that the staging step is missing (S:1429).
- **B** is the only card to tie the dropped author/committer and the missing capability skip to real breakage of F9, F10, X1 and X3 (S:1316).
- A and B both caught CF-13 and CF-14; C missed them.

## Defence
- **F-2.** Spec step 13 depends on all of step 9 (S:1428). Task 19's dependency closure (5, 4, 3, 2, 8, 7, 11, 10, 12) has no Task 13.
- **F-4.** Tasks 11 and 12 are siblings, and Task 13 has no "Depends on" line (P:207, P:215). Chaining them is the only fix for both the missing-file risk and the parallel-append risk.
- **F-3.** ci-poll.md also names `ci.expect_checks_after_push` (S:1070), which Task 6 creates.
- **F-8.** Confirmed: `poll-ci-checks.sh:30` exits 2 when `--pr` is missing.

## Concessions
- **F-2 overreaches.** X1's command list (S:1400) omits `expect_checks_after_push` and `--evidence-sha`. Only the Task 13 edge is spec-required; the Task 6 and Task 14 edges are optional. U-001 is Medium, not High.
- **F-1 severity drops to Low.** Task 8 (P:166) and Task 19 (P:294) exercise `conflict_resume_plan` and `rebuild_state` on real logs, so a mismatch would still surface later. The class stays drift: P:19 says the source wins, and stating a deviation does not authorize it.
- **F-6.** `tests/pr_submit` already imports the package `__init__`, so adding the test to Task 9 is redundant. Task 20 alone is enough.
- **F-9.** The spec itself splits E5 and E12 (S:1416, S:1426), so "necessary" was the wrong label. The real defect is the missing placement anchor: Low drift.
- **F-10 / X-004.** Spec step 3 covers Tasks 3 and 4, so the Task 5 and Task 8 edges to Task 4 are spec-required. Only the Task 9 to Task 6 edge is stricter than the spec.
- **CF-22.** C also missed it.

## Shared assumptions
| A-NNN | Verdict | Reason |
|---|---|---|
| A-001 | ACCEPT | Task 10 depends on Task 3 only (P:184), but spec step 9 depends on all of step 3. Adding "Depends on: Task 4" (4a if split) to Task 10 closes CF-22 and CF-02. |
| A-002 | ACCEPT | C matched edges by function name and missed tasks that cite only test IDs. |
| A-003 | ACCEPT | Stated in F-4. |
| A-004 | ACCEPT | Stated at P:28. |
| A-005 | QUALIFY | B's 21 unresolved rows remain open. |
| A-006 | QUALIFY | The column is incomplete for step 10 (S:1070) and complete for step 13 (S:1400). |

## Points
| Point | Preferred card | Reason |
|---|---|---|
| S-002 | C | One severity scale for every broken edge |
| C-001 | C | The chain also orders the shared-file appends |
| C-002 | C, plus B's grep | Task 6 and Task 13 edges, both from the content |
| C-004 | A severity, C fix | Low; 4a/4b split |
| C-005 | C | Split along the dependency on Task 7 |
| C-006 | A | Exact paths plus a `--cached` check |
| C-007 | B | Names the concrete breakage |
| C-009 | B fix, A severity | Task 20 only; rate Low |
| X-001 | A = C | Drift, Low |
| X-002 | A | Imports are already covered; only the CLI behaviour is not |
| X-003 | Diff | The split is not a deviation; the missing anchor is Low drift |
| X-004 | Diff | Conceded |
| X-005 | C | Consistent scale |
| U-001 | C | Medium |
| U-002 | A | The check cannot be observed |
| U-003 | C | Step 9's done-when (S:1424) |
| U-004 | C | Anchor needed; label corrected |
| U-005 | C | Confirmed at `:30` |
| A-001 | Diff | Accepted |

## Canonical findings
| CF | Severity | Class | Fix |
|---|---|---|---|
| 01 | M | drift | Task 12 depends on Task 11; Task 13 depends on Task 12 |
| 02 | M | drift | A-001, plus an explicit Task 4 edge on Task 15 |
| 03 | M | drift | Task 16 depends on Tasks 2, 6, 13 |
| 04 | M | drift | Task 20 depends on Tasks 9, 18, 19 |
| 05 | L | drift | Task 4b depends on Task 4a and Task 7; state comes from `rebuild_state()` |
| 06 | L | drift | Split into 4a and 4b |
| 07 | L | drift | One log section per test family |
| 08 | M | drift | Task 20 stages exact paths and `.dev/tasks` |
| 09 | M | drift | Use `test -x`, or stage the file in Task 10 |
| 10 | L | drift | grep checks |
| 11 | M | drift | Capability skip in Task 19 |
| 12 | M | drift | Fixed identity at P:29 |
| 13 | L | drift | Quote the clause |
| 14 | L | drift | Cite `:86-103` |
| 15 | L | authorized | Reflect test in Task 20; log that `make test` was not run |
| 16 | L | authorized | None |
| 17 | M | drift | Task 19 depends on Task 13 |
| 18 | L | drift | Add `test_static_grep.py` to Tasks 11 and 12 |
| 19 | L | drift | C1 to C4 run without `--pr` |
| 20 | L | drift | Name the anchors in Task 17 |
| 21 | L | necessary | Only the Task 9 to Task 6 edge; it may stay |
| 22 | M | drift | Task 10 depends on Task 4 |
