# QA Report - Research Gate Fix-Cycle Verification (structural), cycle 2

**Topic:** IronClaude issue-to-work pipeline technical reference
**Date:** 2026-11-20
**Phase:** research-gate fix-cycle (structural)
**Fix cycle:** 2
**Fix authorization:** false (report only)
**Status:** In Progress (items verified so far are appended below)

---

Method: the previous BLOCKING list is `qa-research-consolidated-findings-c2.md` (one finding, N-1). The cycle-2 fix is an appended section "Gap-fill c2 N-1" at lines 601-637 of `research/04-claim-flow-and-orca-worktree.md`. The earlier text (lines 1-597) was not altered: the c1 section markers still sit at the line numbers the c1 structural report recorded (B-2 at 498, F-2 at 545, the test_model_alias_policy row at 554). mtimes show files 01, 03, 05 were last written at 05:52-05:55, before the c1 verification reports (06:03, 06:06), so their erratum sections are unchanged since cycle 1; only file 04 changed after (06:08:56). Source was read only from `/home/coder/.cache/ic-snap-20261120/master` (read-only; nothing was written there). Removed code (git show) was not needed.

## Previously BLOCKING items (from qa-research-consolidated-findings-c2.md)

| ID | Research location | FIXED / STILL-OPEN | Evidence |
|---|---|---|---|
| N-1 | research/04-claim-flow-and-orca-worktree.md, row F-2.1 for `skills/test_model_alias_policy.py`, "What it pins" item (5) (line 554), superseded by the erratum at lines 601-637 (N-1.1 at lines 605-612) | FIXED | `grep -n '^def test_'` on the snapshot file `tests/skills/test_model_alias_policy.py` (249 lines) gives 11 functions: 83, 104, 139, 164, 176, 183, 191, 199, 217, 231, 247 (decorator at 246). Items (1) to (4) of the row are :83, :104, :191, :247 (read at lines 83-101, 104-119, 191-196, 246-249), so the others are 11 - 4 = 7, exactly the seven the row lists (:139, :164, :176, :183, :199, :217, :231). The erratum at line 607 states "The other **seven** tests ..." and at lines 609-611 lists all 11 `def` lines and the arithmetic, all of which match the live file. Other numbers in the row re-checked: 249 lines, 11 tests, 13 collected cases (10 + 3 from the one `parametrize` at :246 over `sorted(ISSUE_WORKER_PINS)`, entries :30-32), 0 classes. The word "eight" still occurs at line 554 (not edited in place; the erratum names and supersedes it, same pattern as the five cycle-1 errata and the minor note M-c1-1) |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over / new | previously-rated-PASS |
|---|---|---|---|---|---|
| (none) | - | - | The erratum's new content (lines 601-637) was re-checked claim by claim against the snapshot; see "Checks performed" items 3 to 6 | - | - |

Carried-over BLOCKING findings: 0. New BLOCKING findings: 0. Previously-rated-PASS areas now failing: none.

## Notes (MINOR, not rechecked, do not fail the gate)

- M-c2-1: line 554 of file 04 still says "eight"; the erratum supersedes it. A synthesis agent must be told that the erratum sections at the end of files 01, 03, 04 (two: c1 B-2/F-2 and c2 N-1) and 05 override earlier text (same advice as M-c1-1).
- M-c2-2: erratum line 607 has a garbled sentence ("The live file disagrees with nothing in the instruction, so it needs no correction [CODE-CONTRADICTED: ...]"). The tag belongs to the word "eight" in the row, not to the live file. The numbers in it are right.
- M-c2-3: erratum line 618 says each `parametrize` decorator is "on the line before its `def`". That holds for :336 and :405 only; the decorators at :459 and :514 are multi-line and their `def` lines are :475 and :539. The case counts (2, 5, 2, 2, 6 = 17; 29 - 5 + 17 = 41) are right.
- M-c2-4: line 3 of file 04 ("eight test files") counts the original section 14 table; the F-2 addendum adds two more files. The addendum says so itself, so no wrong behaviour is described.

## Checks performed

1. Read task prompt lines 930-955 (the block), the cycle-2 consolidated findings, and the c1 structural report (list of items rated FIXED: B-1, B-2, B-3, F-1, F-2).
2. N-1: `grep -n '^def test_\|^    def test_\|parametrize'` and `wc -l` on `tests/skills/test_model_alias_policy.py`; Read of lines 24-249 (all 11 tests, `ISSUE_WORKER_PINS` :29-33, `TIER_TEXT_ALLOWED` :38-44, `TIER_TEXT_DIRS` :50, `TEXT_SUFFIXES` :51). 11 functions, 4 in items (1)-(4), 7 others. FIXED.
3. New-content check of the erratum counts for `tests/skills/test_clickup_claim.py`: `grep -n -E '^\s*(async )?def test_|^class '` (29 `def test_`, one `class FakeClickUp` at :101, matches the erratum list of 29 line numbers one for one), `grep -c` = 29, `wc -l` = 569, `grep -A2 parametrize` (decorators at :336, :389, :405, :459, :514; lists `[401, 403]`, five values, `[None, "111"]`, two caps, six argument lists), 17 cases, 41 total: correct.
4. New-content check of test line citations: Read of `test_clickup_claim.py` lines 100-189 (fake server :101-157, `AssertionError` :145-146, `clean_env` :160-168, `run()` :179-183), 300-369 (PUT url :316, body :317, auth :318), 370-569 (paging, caps, request error :500, bad args :514-545, token output :548, stdlib :561). N-1.3 claim about :459-482 re-derived against the code: cap 3 gives pages [0,1,2] and `page_cap`; cap 4 reads empty page 3 and assigns. Correct. The statement that no test asserts the token is absent from a GET URL is true (no such assertion in the 569 lines).
5. New-content check of `clickup_claim.py` code citations (Read lines 100-270): Authorization header :109, `network` :125-126, `bad_response` :127-132 and :178-179, `seen` :196-199, page-cap return :203-206, `not_found` :210-211, `ambiguous` :212-220, `already_assigned` :230-231, PUT :232-237, `ClickUpError` catch :239-240, `unexpected` :241-242, `skipped` :166 and :169, argument parsing :245-259, file length 270. All correct.
6. New-content check of N-1.3 wording about `test_model_alias_policy.py`: `.md/.py/.json/.yaml/.yml/.sh/.txt/.toml` set at :51 used at :112; `{"tier1a","tier1b","tier2"} <= set(models["tiers"])` at :243 (no `tier2b`); frontmatter globs at :85-89 non-recursive. Correct. More than 60 new line or count citations were re-read in total (required: 10); 0 wrong paths, constants, counts or fabricated items. The one count error of cycle 1 is the only one and is corrected.
7. Contradiction check: Grep for `eight` in file 04 (hits: line 3 scope, line 554 the superseded word, erratum lines 603, 607, 624, 635 quoting it); Grep for `test_model_alias_policy` over all research files (file 04 and file 05 line 570 only; file 05 makes no count claim about it). No contradiction with another research file.
8. Regression check (areas rated FIXED in cycle 1): B-1, B-2, B-3, F-1 live in files 01, 05, 04 (B-2 section), 03; mtimes of files 01, 03, 05 predate the c1 verification reports, and file 04 lines 1-597 keep the same section line numbers as in the c1 report (498, 545, 554). No regression.
9. Structure: all six research files still carry their completion markers (file 04 ends with "Gap-fill c2 N-1 complete" at line 637); the append-only fix left earlier text unaltered as the erratum states.

Confidence: Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement (approximate): Read: 9 | Grep: 4 | Glob: 1 | Bash: 4. No web research was done. Nothing under the snapshot or the research directory was written.
Unchecked items: none. Unverifiable items: none. Not rechecked (outside the c2 scope): the cycle-1 erratum sections other than the file 04 F-2 rows (rated FIXED in c1 and unchanged since, per mtimes).

## Verdict: PASS

Number of BLOCKING findings: 0. The single previously BLOCKING finding (N-1) is FIXED. No finding is carried over, none is new, and no previously PASS area failed.

Status: Complete
