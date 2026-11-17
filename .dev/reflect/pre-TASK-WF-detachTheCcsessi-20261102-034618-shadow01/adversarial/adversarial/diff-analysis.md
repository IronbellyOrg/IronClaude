# Diff Analysis: reviewer-card comparison (UC-1 pre audit of TASK-WF-detachTheCcsessi-20261102-034618)

## Metadata

- Variants compared: 3 (V1 = analyzer/sonnet, V2 = qa/haiku, V3 = refactorer/opus), files `variant-N-original.md`
- Subject: findings against the plan `.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md` (cited below as "plan:<line>")
- Categories: structural (2), content (9), contradictions (3), unique (6), shared assumptions (3)
- Orchestrator checks run while building this file (facts, not opinions): `_real_launch` sets `HOME` (test_ccsession_tiers.py, 15th line of the function at 1757); `remediation-source.md` HC5 reads "off-path review required (PR reviewers and /sc:reflect --mode post)" under "Pipeline Hardening", closure verdict advisory; `remediation-source.md` item 3a says the reply "ends with `message_stop`"; plan:32 says "contains `b"message_stop"`"; the `isatty` guard entered HEAD in commit 77d83d785, the same commit as the fix; the word "before" appears in plan lines 33, 43, 52 and 70.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card shape | Requested shape (Findings, Disputed or confirmed, Verdict) | Table of "deviations" using UC-2 class "Drift", plus its own sections | Requested shape | Low |
| S-002 | Severity vocabulary | blocking/medium/minor, one label per finding | Same words, but F2 has two labels (text "Blocking", table MEDIUM) | One label per finding | Medium |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | verify-sync needs `make sync-dev`, not in plan (plan:19, 82; Makefile:171-178) | medium, "not blocking" | medium, says "cannot be met" is too absolute | medium, notes it is needed with or without the missing `.claude/` copies | Low (agree) |
| C-002 | No task records the "before" pids for plan:70 | medium | minor (requirement exists; only the timing is missing) | medium | Medium |
| C-003 | Stale line anchors (plan:21, 29, 52, 64 vs HEAD) | minor, confirm | reject as a plan defect (source doc used the same anchors) | reject as a plan defect (anchors were accurate when the plan ran) | Medium |
| C-004 | T1.AC3 "no shim or sleep process" but `pgrep -f <copy path>` cannot match `sleep` (plan:29, 34) | minor | minor | minor | Low (agree) |
| C-005 | Scope sentence "exactly the four files" (plan:19) vs evidence outputs (plan:69, ./artifacts) | minor | not raised | not raised | Low |
| C-006 | Off-path review (HC5) has no plan task | not raised | "Blocking" in text, MEDIUM in table | not raised (its coverage check stops at remediation-source.md:26) | High |
| C-007 | Task 1 asserts `contains message_stop` where source says `ends with` | not raised | medium | not raised | Medium |
| C-008 | Task 3 `os.setsid()` reasoning covers only the group-leader case | not raised | not raised | medium, INFERRED (wrapper such as `uv run`) | Medium |
| C-009 | T2.AC2 post-teardown assertion cannot be written in the test; `pgrep -f` pattern not unique | not raised | not raised | minor (its test-file citation was wrong; fixture is at test_ccsession_tiers.py:855, 863) | Low |

## Contradictions

| # | Point of conflict | Positions | Impact |
|---|---|---|---|
| X-001 | Plan verdict | V1 PASS, V3 PASS, V2 FAIL | High |
| X-002 | V2 internal: F2 is "Blocking" in text and MEDIUM in table; its FAIL rests on F2 | V2 text vs V2 table | High |
| X-003 | Anchor staleness: defect (V1) versus not a defect (V2, V3) | see C-003 | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V2 | C-006 off-path review missing from plan | Medium |
| U-002 | V2 | C-007 `contains` weakens `ends with` | Medium |
| U-003 | V3 | C-008 setsid reasoning gap | Medium |
| U-004 | V3 | Task dependency chain does not match real dependencies (plan:38, 50, 56) | Low |
| U-005 | V3 | Task 1 cleanup says `pkill -f` while Constraints say exact pid (plan:23, 29) | Low |
| U-006 | V3 | Task 1 does not mention a temp `HOME` (orchestrator check: `_real_launch` sets `HOME`, so "Mirror `_real_launch`" covers it) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | `remediation-source.md` is part of the spec for coverage purposes, although `--spec` is the one-line `source.md` that points to it | all three map plan items to remediation-source.md | STATED (T1 card) | No |
| A-002 | The plan is judged as the historical plan, not against HEAD code | all three | STATED (reviewer prompt) | No |
| A-003 | The brief's quoted hunks (Makefile:166-181, t5-checks.log:23-38) are accurate; V1 says it did not Read them | V1, V3 lean on them | UNSTATED | Yes, as A-003 (L3: guard / boundary of evidence) |

## Summary

- Structural 2, content 9, contradictions 3, unique 6, shared assumptions 3 (UNSTATED 1)
- Highest-severity items: C-006, X-001, X-002
