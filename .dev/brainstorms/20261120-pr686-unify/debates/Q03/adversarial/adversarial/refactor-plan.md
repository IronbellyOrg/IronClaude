# Refactoring Plan: Merge into Base (Variant 1, OURS) (Q03)

## Overview
- Base: Variant 1 (OURS, read-only variant now), `variant-1-original.md`
- Incorporating strengths from: Variant 2 (CLAY, keep dormant), `variant-2-original.md`
- Planned changes: 6 (5 incorporations, 1 base correction set)
- Risk level: Low (additive text and corrections; no change to the base recommendation)
- Debate status: NOT_CONVERGED at 71.4% (depth quick), moderator resolution used for the six open points

## Planned Changes

### Change 1: Add the moderator-verified facts M1 and M2 to the base (from the diff analysis, confirmed by both advocates)
- **Source**: `diff-analysis.md` M1 and M2; Variant 2 concessions
- **Target**: Base, Cited facts (new facts 10 and 11) and Mechanism
- **Rationale**: C-001, C-003, C-006, X-001, X-002 (OURS wins 67 to 78%); both advocates accepted M1 and M2
- **Integration point**: insert after fact 5 of the base
- **Risk**: Low, additive

### Change 2: Write down the deferred label-write form (from Variant 2, U-005)
- **Source**: Variant 2, fact 2 (`github.py:983-992`) and Mechanism
- **Target**: Base, new section "The deferred label-write form" (replaces the base's one-line fact 8)
- **Rationale**: U-005 Medium; C-009 CLAY 65%; Variant 1's own fact 8 points to the form without describing it
- **Integration point**: after Costs
- **Risk**: Low

### Change 3: Keep a `would_hold` dry-run listing and make the dry-run shadow run plus a cron label-write test the switch-on gate (from Variant 2, U-006, C-007)
- **Source**: Variant 2, fact 3; moderator note on X-003
- **Target**: Base, fact 7 of "What it gets right" and the Risks section
- **Rationale**: C-007 unresolved 50%; moderator: `would_hold` survives, `would_release` does not; D09 makes the shadow run the gate
- **Integration point**: replace the base's dry-run sentence
- **Risk**: Low

### Change 4: State the costs Variant 2 priced (from Variant 2, C-005, C-009, C-011, U-008)
- **Source**: Variant 2 Costs and fact 6; Variant 1 advocate concessions
- **Target**: Base, Costs
- **Rationale**: both advocates agreed rework size is unmeasured (C-005 unresolved); C-009 and C-011 went to CLAY at 65%
- **Integration point**: extend Costs with: restoring the code is a second PR; `test_hold.py` is 1,073 lines and 58 tests; a hand-placed `hold:plan` stops being a stop signal; and the fallback if rework is judged too large (delete only the write calls, keep the table and entry creation, drop `issue.hold` from the reference config)
- **Risk**: Low

### Change 5: Add a sizing step before the rework is asked of Clay (from Variant 2, A-002)
- **Source**: Variant 2 concession; Variant 1 advocate concession on A-002
- **Target**: Base, new section "Conditions and open points"
- **Rationale**: A-002 QUALIFY in both statements
- **Integration point**: after Risks
- **Risk**: Low

### Change 6: Correct the base's defects
- **Source**: Step 3 evaluators; X-003
- **Target**: Base, Mechanism, Cited facts 2, 7 and 9, Costs
- **Fixes**: say `HOLD_LABEL` is defined in `predicates.py:30` and the text `hold:plan` appears in the `record.py` docstring; replace "No label read" with "no `hold:plan` label read"; use "rows 3 to 5" consistently or define the rows once; remove "dry-run shows holds before any write" and say `would_hold` is kept and `would_release` goes; add a "Success tests" list (zero-write test with the grant absent; a leftover label does not block a passing issue; entry created with no write; the grant not listed in the reference config)
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001 | Ship the label code dormant behind the grant | OURS 74%: dormant is not the default (M1) and the dormant form has no entry for poll-found issues (M2); both advocates agreed |
| C-002 | Grant plus NG-2 test is a sufficient switch | Unresolved 55%; the standing grant list is the element the owner's per-issue grant row rejects; the advocate's own hybrid drops the grant from the reference config |
| C-004 | Keep the three-call NG-2 test | OURS 67%: the test describes a capability master does not have |
| C-005 | Rework is too large to ask of Clay | Unresolved; both sizes unmeasured; handled by Change 5 and the fallback in Change 4 |
| C-011 | Keep the hand-placed `hold:plan` stop | CLAY 65% but minor; `hold:backlog` remains; recorded as a cost (Change 4) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | A fact wrongly stated | Remove the two facts |
| 2 | Low | Deferred form mis-described | Revert to the one-line fact 8 |
| 3 | Low | Gate wording too strong | Keep the shadow run only |
| 4 | Low | Cost figures wrong | Mark them rough |
| 5 | Low | Extra step slows the decision | Drop the section |
| 6 | Low | A correction introduces an error | Revert to base text |

## Review Status
- [x] Auto-approved (default; non-interactive, --unattended)
- Approved by: auto
- Approval timestamp: 2026-11-20T08:20:00Z
