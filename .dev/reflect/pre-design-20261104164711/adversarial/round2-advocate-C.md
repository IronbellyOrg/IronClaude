# Round 2 — Advocate C (refactorer card, variant-3-original.md)

## Steelman
A's round-2 severity rule is the fairest on the table. It makes CF-03 and CF-04 Medium (false green at the release gate) and CF-18 Low (Task 14 fails loudly). B's Task 8 re-point is the only edge edit that follows the 4a/4b split through to its consumers.

## 1. Responses to criticism of card C
- **F-2 / CF-17 over-reach (A, B).** Already conceded in R1: S:1400 omits `expect_checks_after_push`, so only Task 13 is required. Medium holds.
- **F-1 severity (A: L; B R1: M).** Low drift, as I said in R1. S:1422 puts the resume rows in step 7, so a spec-compliant placement exists.
- **F-5b / CF-04 "9 suffices".** Conceded. Listing Task 6 explicitly costs nothing and survives later edge edits.
- **F-6 / CF-15 Medium.** Conceded in R1: Low, with the reflect test in Task 20 only.
- **F-9 / F-10 "necessary".** Conceded in R1. CF-20 is drift. CF-21 stays necessary, because Task 9's AC collects `test_ci_classify.py` (P:178).
- **CF-07 (my R1: drift).** Conceded as advisory. Tasks 8, 17 and 18 mirror spec steps 7, 11 and 12.
- **CF-14 class.** Conceded as a spec defect. P:53 copies S:731 `:86-99` verbatim (grep confirmed).

## 2. New claims, checked against the plan
- **A: 4b depends on Task 5. Verified hazard, but the edge is not safe as written.** P:93 (Task 4 resume tests) and P:114 (Task 5 triad rows) both append to `test_conflicts_core.py`, so the two tasks must be serialized. Two problems follow from serializing them this way:
  1. Task 5 still reads "Depends on: Task 4" (P:106). If that becomes 4b, the graph has a cycle (4b → 5 → 4b), so the edge also needs Task 5 re-pointed to 4a. Neither A nor B wrote that change.
  2. Task 9 (P:171, depends on 5 and 6) exports `conflict_resume_plan` and `crash_resume_plan` (S:741-744). Under 4a → 5 → 4b, Task 9's closure never reaches 4b. The import fails, and Task 9's AC `pytest tests/pr_submit` breaks. Spec step 8 depends on all of step 3 (S:1423).

  **My fix:** keep the spec order: Task 5 depends on 4b, and 4b depends on 4a and Task 7. This serializes the file with no new edge, needs no change to Task 9, and matches step 4's dependency on all of step 3. If the panel keeps A's ordering instead, it must add both "Task 5 depends on 4a" and "Task 9 depends on 4b".
- **B: Task 8 re-points from Task 4 to 4b. Verified, adopted.** P:155 lists Task 4 and Task 7, and P:166 calls `conflict_resume_plan`, which is in 4b (P:92). Through 4b → 4a, Task 8 still reaches everything in Task 4.

## 3. Final table
| CF | Agreed sev | Agreed class | Agreed fix | Position |
|---|---|---|---|---|
| 01 | M | drift | Chain 11→12→13 on 10 (Task 13 has no Depends-on, P:215) | agree |
| 02 | M | drift | 15 on 4a, 12 | agree |
| 03 | M | drift | 16 on 2, 6, 13 + header grep | agree |
| 04 | M | drift | 20 on 6, 9, 18, 19 | agree |
| 05 | L | drift | 4b on 4a, 5, 7; 8 on 4b | **disagree on the edges:** 5 on 4b, 4b on 4a, 7; 8 on 4b. Otherwise add 5→4a and 9→4b |
| 06 | L | drift | Split 4a/4b | agree |
| 07 | L | advisory | Optional log sections | agree (conceded) |
| 08 | M | drift | Stage paths + `.dev/tasks`; `--cached` AC | agree |
| 09 | M | drift | `test -x` in 10-12 | agree |
| 10 | L | drift | Greps to `./artifacts/` | agree |
| 11 | M | drift | Capability skip in 19 | agree |
| 12 | M | drift | Fixed identity in P:29 | agree |
| 13 | L | drift | Quote the S:728 clause | agree |
| 14 | L | spec defect | Cite `:86-103` | agree (conceded) |
| 15 | L | authorized | Reflect test + "VG-2 not run" in 20 | agree |
| 16 | L | authorized | None | agree |
| 17 | M | drift | 19 on 13; 6, 14 optional | agree |
| 18 | L | drift | `test_static_grep.py` in 11, 12 | agree |
| 19 | L | drift | C1-C4 without `--pr`; stderr names the SHA | agree |
| 20 | L | drift | Anchors + substring AC in 17 | agree |
| 21 | L | necessary | Keep 9→6 | agree |
| 22 | M | drift | 10 on 3, 4a | agree; `merge_parent_ok` and `merge_preflight_ok` are in 4a (P:91) |

## 4. Shared assumptions
- **A-001 ACCEPT.** P:184 lists Task 3 only. The same blind spot recurs in the split: an edge to "Task 4" must now name 4a or 4b, and Task 9 shows the cost of a wrong choice.
- **A-002 ACCEPT.** Compute dependency closures from the plan graph, and expand spec test-case IDs and export lists (S:741-744) into the functions they use.
- **A-006 QUALIFY.** Spec step 10's dependency column is incomplete (S:1070 needs Task 6). The step 13 and step 8 columns are adequate, and they are what refutes the 4a → 5 → 4b ordering.

Verdict: ready-with-fixes. The CF-05 edges are the only open disagreement.
