# Merge Log

- Plan: refactor-plan.md (auto-approved, 2026-10-31)
- Base: variant-3-original.md (reviewer-3, opus:refactorer)
- Sources: variant-1-original.md (sonnet:analyzer), variant-2-original.md (haiku:qa), invariant-probe.md, debate-transcript.md (the scoring matrix sets the final classes and severities)
- Output: merged-verdict.yaml (28 findings: 2 high, 13 medium, 13 low)
- Convergence: 0.94, status BLOCKED_BY_INVARIANTS (INV-001 and INV-002 are open HIGH items, carried as M-01 and M-02)
- Executed: 2026-10-31

## Merge rules used

- Every base finding (R3-F1 to R3-F11) carries over unless the plan changes it.
- `sources` lists the original finding ids plus the debate diff-point ids (C-xxx, X-xxx) from the scoring matrix, so each finding traces back to the variant claim and to the debate ruling.
- Citations are copied word-for-word from the source files. A citation written as `a; b` in a variant is split into its two parts, each kept verbatim. Short forms from the probe and debate (`design:226`, `plan:102`, `SKILL.md:196`) are kept as written, not expanded.
- The plan gives no class for the invariant items. Each UNADDRESSED probe item is classed `gap`: the task plan does not cover that requirement. Severity is the probe's severity.
- Task numbers refer to TASK-WF-implementTheDesi-20261031-182028.md. That file was read to map findings to tasks and was not edited.

## Applied changes

### Change 1: Reclassifications per the debate. Status: APPLIED

| Item | Before (base) | After | Merged id |
|---|---|---|---|
| R3-F2 (X-002, C-001) | drift / medium | gap / medium; dependency list taken from V1's R1-1 (1, 4, 6, 7, 8), per the C-001 ruling | M-04 |
| R3-F7 | refinement / low, standalone | withdrawn as a standalone finding; merged into the R1-6 equality test, refinement / low (R2-12 is the same claim and is attributed too) | M-19 |
| X-001 (R3-F3) | drift / medium | stays drift / medium; INV-009 key-presence rule added to the remedy (an explicit "" disables Codex; a missing key falls back to the shipped value) | M-05 |
| C-006 (R3-F9, R2-05) | gap / low, one finding | split in two: `rereview_requested{reviewer}` gap / medium, because pending_retriggers treats a missing reviewer as augment (debate citation `plan:112`); the other events gap / low | M-07, M-16 |

### Change 2: Invariant probe items added. Status: APPLIED

| Probe id | Severity | Merged id |
|---|---|---|
| INV-001 | high | M-01 (refers to M-03 for the completed_at parameter) |
| INV-002 | high | M-02 |
| INV-003 | medium | M-08 |
| INV-004 | medium | M-09 |
| INV-005 | medium | M-10 |
| INV-006 | medium | M-11 |
| INV-007 | low | M-23 |
| INV-008 | low | M-24 |
| INV-011 | low | M-25 |

INV-009 is folded into M-05 (Change 1), as the plan says. INV-010 and INV-012 are ADDRESSED in the probe and the plan does not list them, so they are not carried over.

### Change 3: V2 obligations added. Status: APPLIED

| Sources | Class / severity | Merged id |
|---|---|---|
| R2-01 + R2-03 + R2-04 + R2-09 (C-008) | gap / medium. R2-01's high and R2-09's low are both set to the C-008 ruling of medium | M-12 |
| R2-02 + R2-07 (C-009) | gap / medium | M-13 |
| R2-06 | gap / medium | M-14 |
| R2-08 | gap / low | M-27 |
| R2-13 | refinement / low | M-28 |

### Change 4: V1 items added. Status: APPLIED

| Sources | Class / severity | Merged id |
|---|---|---|
| R1-2 | gap / medium; remedy: Tasks 7-9 state that the Task 10 tests prove them, and the Task 7 dry check becomes best-effort with a recorded-payload fallback | M-15 |
| R1-9 | gap / low | M-26 |
| R1-5 merged into C-005 (R3-F5, R2-10) with `models.py:211-212` | refinement / low (base class kept) | M-17 |
| R1-8 + R3-F8 (C-004) | gap / low | M-20 |

### Change 5: X-004 test design. Status: APPLIED

R3-F4 keeps V3's location: the SKILL and refs resume text in Tasks 12 and 14, with no change to recovery.py. The remedy adds V3's Round-2 test design: a Task 10 log fixture with only an augment `rereview_requested`, asserting `resolve_crash_window` returns S5 and `pending_retriggers` returns `["codex"]`, plus a Task 12 acceptance grep that the SKILL resume section calls `pending_retriggers` before the S5 poll. R1-3 is listed as a source because the test came from it; its recovery.py change is not adopted (see below). Merged id: M-06.

## Base findings carried over without change

| Base id | Merged id |
|---|---|
| R3-F1 (C-002; remedy uses the explicit completed_at parameter the matrix chose; R1-4 attributed) | M-03 |
| R3-F6 | M-18 |
| R3-F10 | M-21 |
| R3-F11 (aligned; its absent_reviewers seeding advice is now M-25, so its remedy points there instead of repeating it) | M-22 |

## Changes not made (per the plan)

- R1-3's recovery.py change: rejected. M-06 says there is no recovery.py change.
- R2-01 at high severity: rejected; it is medium inside M-12.
- R2-11 ("record toward empty"): rejected in favour of the X-001 fallback; it is not a source of any finding.

## Variant and probe ids not in the verdict

| Id | Reason |
|---|---|
| R1-7 | Same issue as X-001. V1 conceded X-001 to V3, and R1-7's remedy (overrides must repeat the Codex fields) conflicts with M-05. |
| R2-11 | Rejected by the plan (see above). |
| R1-10, R2-14 | Aligned findings from non-base variants; the plan does not carry them. |
| INV-010, INV-012 | ADDRESSED in the probe; the plan does not list them. |

## Post-merge checks

A script parsed merged-verdict.yaml and compared it with the plan and the six source files.

| Check | Result |
|---|---|
| merged-verdict.yaml parses as YAML and the top-level keys match the requested values | PASS |
| Every source id in the plan's Planned Changes (34 ids: C-005, C-006, C-008, C-009, INV-001 to INV-009, INV-011, R1-2, R1-5, R1-6, R1-8, R1-9, R2-01 to R2-04, R2-06 to R2-09, R2-13, R3-F2, R3-F7, R3-F8, X-001, X-002, X-004) appears in some finding's `sources` | PASS (0 missing) |
| Ids under "Changes NOT Being Made": R1-3, R2-01 and X-001 are present in the form the plan describes; R2-11 is absent on purpose | PASS |
| No finding without citations | PASS (0 findings with an empty list) |
| Every citation appears word-for-word in a source file | PASS (0 not found) |
| Findings sorted high, then medium, then low; ids M-01 to M-28 in order; class and severity values valid | PASS |
| No new contradictions | PASS (manual review, below) |

Contradiction review:

- M-01 and M-03 agree: M-03 adds the completed_at parameter and M-01 sets the value passed through it.
- M-05 replaces Task 2's line-44 acceptance. No other finding keeps the "override disables Codex" behaviour, and R1-7 is left out for that reason.
- M-06 and the plan's rejection of R1-3 agree: no recovery.py change. M-06's fixture expectation (`["codex"]`) matches Task 9's existing pending_retriggers acceptance.
- M-07 and M-08 both put fields on `rereview_requested` (reviewer; cycle_id, reviewer, watermark) and do not conflict.
- M-10 overrides Task 7's "two summary comments -> polling" acceptance. No other finding keeps that row.
- M-22 (aligned) and M-25 (gap) cover different things: the count rule matches the existing test, while the absent_reviewers seed is missing. M-22's remedy points to M-25, so the two do not give different answers about the seed.
- M-12 sets one severity for the whole group (medium), which replaces both R2-01's high and R2-09's low. No finding still states either of those severities.

## Escalations

None. All five planned changes applied as written.
