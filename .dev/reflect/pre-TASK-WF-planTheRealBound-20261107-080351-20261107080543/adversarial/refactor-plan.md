# Refactoring Plan

## Overview
- Base: variant-1 (analyzer card). Incorporated: variant-2 and variant-3 items; invariant-probe items. Output: one merged verdict card (merged-verdict.yaml) that lists every surviving finding once, with the final severity set in the debate and a plan-change recommendation per finding. The reviewed plan file is NOT changed (advisory review).
- Convergence status: BLOCKED_BY_INVARIANTS (INV-001, INV-002, INV-003 are HIGH and UNADDRESSED). At depth standard there is no Round 3, so the debate force-selects by score and records non-convergence.

## Planned Changes
| # | Merge item | Source | Target in verdict | Final severity | Rationale (debate evidence) |
|---|---|---|---|---|---|
| 1 | PASS is predetermined FAIL; fix must pick one: per-case evidence class including an accepted-documented-limit class | R1-04, QA-1, R3-F1, R3-F13, INV-003, INV-004 | M-01 | HIGH | all three advocates concede high; probe shows the per-case fix alone can still return PASS on known escapes (INV-003) |
| 2 | Old governed child must outlive the first process: say how; check survival; exempt it from runner cleanup until resume/fork observed | R1-03, R3-F4, QA-3 (medium, reworded), INV-002 | M-02 | HIGH | helper:16-17, design:555; live_probe cleanup (INV-002) |
| 3 | Throwaway HOME lifetime across the runs that need it | INV-001 | M-03 | HIGH | helper:220-225; live_probe.py:134 |
| 4 | Task 4 foreground-reparent shape: run identify inside the same governed command | R1-01 (scoped), QA-2/R3-F11 label | M-04 | HIGH (that shape only) | helper:16-17 |
| 5 | Task 7: depth data source and dependency on Tasks 2-4 | R1-05, R3-F2 | M-05 | MEDIUM | plan:31, :44, :99, :104 |
| 6 | Task 8 third state "superseded or not applicable (cite)"; F2.3 and F2.6 describe the historical probe; boot compare at helper:234 | R1-06, R1-07, R3-F9, R3-F10, R1-06 | M-06 | LOW to MEDIUM | helper:219-223, :234, :253; plan:118 |
| 7 | Run budget table; count refused runs; skip tasks on refused preflight | R1-08, R3-F12, INV-010, INV-011 | M-07 | MEDIUM | plan:22 |
| 8 | Persist session for resume/fork; name flag set | R1-02 | M-08 | MEDIUM | live_probe.py:235-236, :252 |
| 9 | Tool list for subagent and Monitor runs | R1-09 | M-09 | MEDIUM | live_probe.py:237-240; helper:427-428 |
| 10 | Unavailable branch in Task 2 criterion 1, Task 6, Task 7 | QA-4 (narrowed) | M-10 | MEDIUM | plan:47, :104 |
| 11 | Link each result row to a runner-captured selector-output record by run id | QA-5, A-001, INV-008 | M-11 | MEDIUM | plan:31 |
| 12 | Task 8 case list: launch wrapper, hook/Git process trees, auto mode, decisive row | R3-F3, QA-6 | M-12 | MEDIUM | design:504; plan:114 |
| 13 | Task 6: name the governed pusher, label the shell, cite the existing test or say what it adds, avoid same-ref race | R1-10, R3-F7, R3-F8, INV-007 | M-13 | MEDIUM | tests/hooks/test_launch_job_identity.py:1291-1354; plan:90, :94 |
| 14 | Baseline for "git status unchanged" and staging limited to this package | R1-11, R3-F6 | M-14 | MEDIUM | plan:25, :120 (basis inferred from session snapshot) |
| 15 | Session-id behavior across resume/fork//clear and the reused-process case | INV-005, INV-006 | M-15 | MEDIUM | helper:429-437; design:501, :504 |
| 16 | Orphan and supervisor cleanup | R1-12, INV-009 | M-16 | MEDIUM | live_probe.py:271, :275; helper:292 |
| 17 | Settings checksum per real run | R3-F5 | M-17 | LOW | plan:36, :120 |

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| R3-F13 as standalone | Separate finding | Folded into M-01 (all advocates agreed it is the same mechanism) |
| QA-3 "fabricable-evidence" label | High severity | Overstated: plan:59 already names the overlap; kept at medium with reworded text |
| R1-01 as plan-wide high | Task-wide | Holds for the foreground-reparent shape only |
| R1-06 as medium | medium | Dead branch with harmless wording; low |

## Risk Summary
Low risk: the verdict is advisory and edits nothing. Risk of losing a finding: lowest for items 1-4 (cited in all or most cards). Items 3 and 15 and the probe-sourced items rest on one reviewer or on unobserved harness behavior and are marked inferred where applicable.

## Review Status
Auto-approved (non-interactive).
