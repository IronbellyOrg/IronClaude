# Refactoring Plan (base: V3)

## Overview
- Base: Variant 3 (reviewer 3 card). Incorporated: V1, V2, invariant probe INV-001..INV-010. Output: one merged review whose findings table is the only place severities are stated.
- Normalisation agreed in Round 2: category Drift for static plan gaps (no Regression in this pre-execution audit; one finding is flagged "becomes Regression if executed unchanged"); severities HIGH/MEDIUM/LOW only; the extra sections stay supplements.

## Planned Changes

| # | Change | Source | Target in base | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|
| 1 | Reclassify V3 findings 1 and 2 as one Drift HIGH "shared launch fixture and re-baselined tests"; add INV-004 (full affected-test set, 30 call sites) and INV-002 (environment leakage) | V3, INV-004, INV-002 | findings table row 1 | X-003 and S-001 agreed in Round 2; INV-004 widens the test set | Low |
| 2 | Downgrade V3 finding 3 (owner decision) from HIGH Drift to an advisory note: the refusal is design-mandated (DESIGN:355,514); keep "record the consequence before implementing" | V1, V3 concession | notes | X-001 agreed 3/3 | Low |
| 3 | Add Task 1 gate finding (MEDIUM Drift): the STOP verdict has no consumer, OB-H1 ordering replaced by synthetic fixtures, existing live_probe.py ignored | V1 #1, V2 #1, V3 #11 | new row | C-001 agreed (MEDIUM) | Low |
| 4 | Merge ownership-predicate findings into one MEDIUM Drift with V2's negative cases; escalate through INV-001 (HIGH, UNADDRESSED: no fixture can be built while the install place and marker are open) | V1 #4, V2 #5, V3 #4, INV-001 | new row | C-002; INV-001 blocks convergence | Medium |
| 5 | Merge Task 19/20 status findings into one MEDIUM Drift (status wrong on the owned branch) | V1 #5, V2 #6, V3 #5 | new row | C-003 agreed | Low |
| 6 | Add matcher-ineffective registration cases (MEDIUM) and adapter runtime prerequisites (MEDIUM) | V2 #3, #4 | new rows | C-005 agreed; U-003 | Low |
| 7 | Add INV-005 (check order inside cmd_launch), INV-006 (--pipeline none untestable at script level), INV-009 (circular observation gate), INV-003 (install remedy does not repair a stale script) | probe | new rows | probe findings, MEDIUM | Medium |
| 8 | Add coverage findings: matrix omits three source clauses; T-MSG-4..6 unassigned; F1-F8 unresolvable (file absent) | V2 #2, #8, #9 | new rows | U-002 | Low |
| 9 | Keep V3's remaining rows (enforcement_hook field, Task 3 ids, scope constraint, Task 22 skips) and add LOW items from V1 (Task 12 dependency, IR-3, issue.md, superclaude.* forms, leaks pinned, session-id source) and INV-007, INV-008, INV-010 | V1, V3, probe | rows | agreed, LOW | Low |
| 10 | Keep "checked and correct", advisory A, correctness gaps; add V1's Task 12 "Necessary" note and the IR-7 "Authorized" note | V1, V3 | notes | X-004 | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| C-006 | V2 finding 7: Task 21 drops L2 on a GO verdict without authorization | Withdrawn by V2 in Round 2: unresolved install-place and observation prerequisites justify a follow-up (DESIGN:377). |
| C-001 severity | V2 HIGH Regression for the gate | Lowered to MEDIUM Drift by V2 itself (PLAN:24 and DESIGN:506 scope the gate). |
| X-001 | V3 HIGH Drift "no owner decision" | V3 conceded: the notice ordering is advisory only. |
| S-002 | V1 "LOW-MEDIUM" severity | Rejected by all three: one supported severity per finding. |
| A-002 | V2 REJECT of "static prediction is fine" | Resolved to QUALIFY by 2 of 3: predictions are reported as predicted, not observed. |

## Risk Summary
Overall low risk: a document merge with all findings traceable to a card or a probe id. Rollback: the three original cards remain as variant-N-original.md.

## Review Status
Auto-approved (non-interactive).
