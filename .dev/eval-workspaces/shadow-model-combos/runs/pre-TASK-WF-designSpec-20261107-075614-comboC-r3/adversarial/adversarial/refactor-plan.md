# Refactoring Plan

## Overview

- Base: Variant 3 (reviewer-3 card)
- Incorporated: Variant 1, Variant 2, invariant probe
- Changes planned: 9; rejected: 4
- Overall risk: Low (additive findings; severity recalibrations follow the debate)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Keep resume row 4 finding as MAJOR; add the vacuous-head-check mechanism and the category `unpassable-check` | V1 F1 + V3 F1 | F1 | modify | C-001 78%: V3 remedy chosen; V1 conceded; S-002 favours the specific category | Low |
| 2 | Add Wave 0 wording ambiguity as its own MINOR finding (spec 241 vs plan 137/140) | V1 F2 | new finding | append | C-002 MERGE 72%: V1 downgraded to MINOR after plan:140 check | Low |
| 3 | Add FR-16 release retry has no bound or test body (MAJOR) | V2 F2 | new finding | append | C-008 85% unanimous | Low |
| 4 | Add cycle-id equality has no test (MINOR, not MAJOR) | V2 F1 | new finding | append | C-007 85%; severity calibrated: plan:124 and plan:33 assign the mint owner | Low |
| 5 | Add crash-boundary coverage narrower than spec section 7 (MINOR) | V2 F3 | new finding | append | not contested | Low |
| 6 | Add guard_status takes no halt reason (MINOR) | V1 F3 | new finding | append | C-006 90% | Low |
| 7 | Widen the whole-line pin finding to every existing Wave bullet | V3 round 2 | F3 | modify | C-009 92%; head-binding bullet is also a classification key | Low |
| 8 | Add exit paths after engage need a held report test (MEDIUM advisory) | probe INV-012/013 | new finding | append | probe: base halts fix_commit_failed, pr_head_mismatch, push_range_mismatch; no task enumerates them; no card raised it | Low |
| 9 | Merge classification-scope findings into one (git write verbs) | V2 F5 + V3 F6 | F6 | merge | C-003 MERGE 82% | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| S-001 | V2 layout ("Not checked" before the block) | unresolved; layouts equivalent |
| C-004 | V2 F4 (Task 1 dependencies as a stand-alone finding) | conceded as padding by V2; fold into V3 F4/F5 as one MINOR |
| A-001/A-002 | keep blocking:false for all findings | QUALIFY/REJECT: the row-4 finding is flagged as a spec-origin defect; severity stays MAJOR non-blocking because a failing test would later reveal it; spec amendment is recommended |
| INV-001, INV-009 | LOW probe items (failed_mutations never decays; next_cycle_number ordering) | recorded in the probe only |

## Risk Summary

All changes are additive or severity recalibrations; rollback is deleting the finding.

## Review Status

Auto-approved (non-interactive).
