# Refactoring Plan: Merge into Base (Variant 1, proposal-A)

## Overview
- Base: Variant 1 (proposal-A, not yet)
- Incorporating strengths from: Variant 2 (proposal-B), Variant 3 (proposal-C), advocate concessions
- Planned changes: 5
- Risk level: Low (four additive, one small wording replacement)

## Planned Changes

### Change 1: Data exposure as a fifth CO-04 design concern (from Variant 2)
- **Source**: Variant 2 "What it costs or risks" bullet 1; diff points C-005, U-002; round1-advocate-3.md "Shared assumptions" A-001 (whole snapshot or reduced part)
- **Target**: Base, "What happens next", the CO-04 bullet (extend)
- **Rationale**: C-005 won by Variant 2 unanimously (60 to 85 percent).
- **Integration point**: after "a transport, an identity envelope, an age rule (Q22) and a re-sanitising step (ADJ line 306)", add: "and who may read a copy, because the snapshot is written with mode 0600 on purpose (ADJ line 244), including whether the whole snapshot or only part of it leaves the host."
- **Risk**: Low.

### Change 2: Accurate Coder#477 wording (from advocates 1 and 3)
- **Source**: round1-advocate-1.md "Concessions" 4; round1-advocate-3.md C-002 verdict
- **Target**: Base, "What happens next", the CO-01 bullet (replace wording)
- **Rationale**: "no channel exists or is planned yet" reads as a "no", stronger than the owner's "may become".
- **Integration point**: replace with: the Coder#477 reply (CO-01) states that no channel exists and one is deferred until observer release 4 or an owner decision on a TUIBBS screen.
- **Risk**: Low.

### Change 3: Remove an overclaim (from advocate 1)
- **Source**: round1-advocate-1.md "Concessions" 3
- **Target**: Base, "What it unlocks", third bullet (replace)
- **Rationale**: ADJ line 306 lists an identity envelope and an age rule as missing; whether they need new snapshot fields is undecided.
- **Integration point**: replace "so a later channel needs no change to the observer's file" with "so a later channel starts from the existing file; whether the identity and age pieces need new fields in it is not yet decided".
- **Risk**: Low.

### Change 4: Conditional contract-note sentence (resolves split point C-004)
- **Source**: Variant 2 "What happens next" bullet 5; round1-advocate-3.md "Concessions" (fix: keep the preconditions as a standing rule)
- **Target**: Base, "What happens next", the contract-note bullet (extend)
- **Rationale**: C-004 split three ways; the orchestrator takes the version that keeps the single-host line unchanged and adds only a guard.
- **Integration point**: add: "and adds one guard sentence: any future copy off this host is read-only and may start only after CO-04's design names all its pieces."
- **Risk**: Low.

### Change 5: The ledger is the authoritative record (from advocate 2)
- **Source**: round1-advocate-2.md "Shared assumptions" A-002
- **Target**: Base, "What happens next", first bullet (extend)
- **Rationale**: Q3 may close Coder#477; the answer must not depend on it.
- **Integration point**: append: "The ledger is the authoritative record; the Coder#477 sentence below only repeats it."
- **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001, X-001 | Open CO-04 now (V2) or close it (V3) | All three advocates judged deferral best; the record says "Background, not deciding" (ADJ line 306) |
| C-003 | Pull Q22 and an authentication design forward (V2) | MR line 375: no transport until Q4, Q18 and authentication are settled |
| U-003 | Use Q18 as the basis to close Coder#477 (V3) | Q3 can still choose its close text under the base, since "TUIBBS is not near" holds while deferred (advocate 1) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 to 5 | Low | None beyond the base | Restore base text |

## Review Status
- Approved by: auto (non-interactive)
- Approval timestamp: 2026-11-14
