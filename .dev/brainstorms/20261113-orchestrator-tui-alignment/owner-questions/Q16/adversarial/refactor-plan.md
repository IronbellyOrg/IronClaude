# Refactoring Plan: Merge into Base (Variant 3, proposal-C)

## Overview
- Base: Variant 3 (proposal-C, one vocabulary and one audit record)
- Incorporating strengths from: Variant 1 (proposal-A), Variant 2 (proposal-B), and advocate concessions
- Planned changes: 4
- Risk level: Low (all additive)

## Planned Changes

### Change 1: Re-ask checkpoint at the trust layer (from Variant 1)
- **Source**: Variant 1, "What happens next" bullet 4 and diff point U-001
- **Target**: Base, "What happens next if the owner picks it" (append)
- **Rationale**: U-001 won by Variant 1 in all three advocate verdicts (60 to 70 percent); advocates 1 and 3 said Variant 3 can absorb it.
- **Integration point**: new last bullet: when SW-12's Phase 4 row is opened, the owner re-confirms the narrow promise with the draft vocabulary in view.
- **Risk**: Low, additive.

### Change 2: One owner and no second vocabulary (from Variant 2)
- **Source**: Variant 2, "What it unlocks" bullet 2; diff point U-002 (review 03 Edit 7 idea)
- **Target**: Base, "What happens next" (append)
- **Rationale**: U-002 won by Variant 2 (55 to 70 percent); advocates 2 and 3 recommended Variant 3 borrow it.
- **Integration point**: bullet: the vocabulary and audit format have one owner (the SW-12 Phase 4 row) and no other issue defines a second vocabulary or audit format.
- **Risk**: Low.

### Change 3: Per-program meaning of each term (from advocates 2 and 3)
- **Source**: round1-advocate-2.md "Overall"; round1-advocate-3.md "Concessions"
- **Target**: Base, "What it costs or risks" (append a mitigation to the hidden-differences risk)
- **Rationale**: both advocates named "equal words hide unequal protection" as the main weakness of the base; the fix is a rule for when the vocabulary is defined.
- **Integration point**: after the "shared vocabulary can hide real differences" bullet.
- **Risk**: Low.

### Change 4: Audit records are untrusted input (from advocate 3)
- **Source**: round1-advocate-3.md "Concessions" (shared injection target; TB-UNTRUSTED, merged-requirements line 632)
- **Target**: Base, "What it costs or risks" (append)
- **Rationale**: a security concession not raised by any variant.
- **Integration point**: new bullet at the end of the section.
- **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001, X-003 | Keep "Decide one design, not two." in #409 (V1 by default, V2 by intent) | All three advocates judged the rewrite better (65 to 70 percent); the sentence is out of scope per merged-requirements line 146 |
| X-001 | One mechanism for every consumer (V2) | Different threat models (ADJ lines 295, 809; boundary rows at lines 355, 401, 636) |
| C-004 | Hold V2-03, V2-04, OB-09 and SW-12 Phase 4 until a later re-ask (V1) | The hold is circular (SW-12 is blocked by XC-08, lines 201, 830); Change 1 keeps the re-ask without the hold |
| A-002 | Commit nothing to minimise reversal cost (V1) | Won 2 of 3 at 55 percent only; the narrow promise is reversible by issue history while no code rests on it |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Low | Re-ask forgotten; the narrow promise stands | Remove bullet |
| 2 | Low | None beyond the base | Remove bullet |
| 3 | Low | None beyond the base | Remove bullet |
| 4 | Low | None beyond the base | Remove bullet |

## Review Status
- Approved by: auto (non-interactive)
- Approval timestamp: 2026-11-14
