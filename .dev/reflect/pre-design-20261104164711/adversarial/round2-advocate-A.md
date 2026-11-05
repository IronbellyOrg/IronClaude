# Round 2 advocate: Variant A (analyzer card)

## Steelman
B's Q-5 frames CF-11/12 best: S:1316 requires a fixed author/committer and a per-module capability skip; P:29 drops the first and P:291 says X1 skips "only when uv is absent", so F9, F10, X1, X3 commit with no identity under `GIT_CONFIG_GLOBAL=/dev/null`. C's 4a/4b split beats my "move the tests", which leaves untested resume code in Task 4.

## 1. Responses to B and C
1. **Scale (X-005).** Conceded. Rule: Medium when an AC or test, run as written, fails, passes falsely or cannot be observed; Low when only prose or order is affected and a later gate fails loudly.
2. **CF-03 (B, C: M).** Conceded. R1 adopted B's header-match grep, which makes Task 16's AC read Task 13's script; "Low" and the grep contradicted each other.
3. **CF-04 (B, C: M).** Conceded. Task 20 is the release gate; without Tasks 6 and 9 in its closure, `pytest tests/pr_submit` can go green before their tests exist (false green).
4. **CF-11/12 (B, C: M).** Conceded, per the steelman.
5. **CF-05/06 (B: necessary, M).** Rejected. Resume tests belong to step 7 (S:1422), so a spec-compliant path exists; no AC is wrong. Low drift. I adopt C's split, plus one new edge: resume tests and Task 5's triad rows both append to `test_conflicts_core.py`, so 4b depends on Task 5 (the CF-01 hazard).
6. **CF-07 (B, C: drift).** Maintained. Tasks 8, 17, 18 mirror spec steps 7, 11, 12; size is not deviation. Per-family log sections are optional.
7. **CF-10 (B, C: drift).** Class conceded; Low, since Tasks 14-16 run `test_static_grep.py`.
8. **CF-14 (drift).** Maintained as spec defect: P:53 copies S:731 verbatim; the list ends at `:103`. Same fix.
9. **CF-15 (B: M).** Rejected. An `__init__` import failure breaks every `tests/pr_submit` test; only the CLI path is unexercised, and one path in Task 20 covers it.
10. **CF-18 (B: M).** Rejected. Tasks 10 and 13 run the force-push scan over the scripts and Task 14 over all files, so it fails loudly. Add the file to Tasks 11 and 12 anyway.
11. **CF-17.** My R1 over-asked. S:1400 omits `expect_checks_after_push` and `--evidence-sha`; only Task 13 is required (C's concession accepted).
12. **CF-21 ("no finding").** Revised: Task 9 on Task 6 is AC-driven (`pytest tests/pr_submit` collects `test_ci_classify.py`), so necessary.

## 2. Final table
| CF | Sev | Class | Fix | R1 majority |
|---|---|---|---|---|
| 01 | M | drift | Chain 11, 12, 13 rooted on Task 10 | agree |
| 02 | M | drift | Task 15 on Task 4a, 12 | agree |
| 03 | M | drift | Task 16 on 2, 6, 13; header-match grep | agree (conceded) |
| 04 | M | drift | Task 20 on 6, 9, 18, 19 | agree (conceded) |
| 05 | L | drift | 4b (resume code and tests) on 4a, 5, 7 | agree |
| 06 | L | drift | Split 4a/4b | agree |
| 07 | L | drift, advisory | Optional per-family log sections | disagree (no deviation) |
| 08 | M | drift | Task 20 stages exact paths and `.dev/tasks`; AC `git diff --cached --name-only` | agree |
| 09 | M | drift | `test -x` in Tasks 10-12; `ls-files -s` after staging | agree |
| 10 | L | drift | Literal greps saved to `./artifacts/` | agree (conceded) |
| 11 | M | drift | Capability skip in Task 19 | agree (conceded) |
| 12 | M | drift | Fixed author/committer in P:29 | agree (conceded) |
| 13 | L | drift | Quote the S:728 clause in Task 2 | agree |
| 14 | L | spec defect | Cite `:86-103` | disagree (class) |
| 15 | L | authorized | Reflect test and "VG-2 not run" in Task 20 | agree |
| 16 | L | authorized | None | agree |
| 17 | M | drift | Task 19 on Task 13; 6, 14 optional | agree |
| 18 | L | drift | `test_static_grep.py` in Tasks 11, 12 | agree |
| 19 | L | drift | C1-C4 without `--pr`; stderr names the SHA | agree |
| 20 | L | drift | Anchors and final-substring AC in Task 17 | agree |
| 21 | L | necessary | Keep the edge | no majority; with C |
| 22 | M | drift | Task 10 on Task 3, 4a | agree |

## 3. Shared assumptions
- **A-001 ACCEPT.** P:184 gives Task 10 only Task 3; one edge to Task 4a closes CF-22 and CF-02.
- **A-002 ACCEPT.** Fix the method: expand spec test-case IDs to the functions they assert, and compute closures from the plan graph, not by name matching.
- **A-006 QUALIFY.** Spec step 10 omits Task 6 (S:1070 documents `expect_checks_after_push`); the step 13 column is adequate.
