# Refactoring Plan: Merge into Base (Variant 1, proposal-A)

## Overview
- Base: Variant 1 (proposal-A, owner-created Orca worktree)
- Incorporating strengths from: Variant 2 (proposal-B), Variant 3 (proposal-C)
- Planned changes: 4
- Risk level: Low (all changes add conditions or a fallback; none changes the base home)

## Planned Changes

### Change 1: Make the person-opened reading an explicit owner condition (from Variant 2)
- **Source**: V2 "What happens next" step 3; scoring X-001 (V2, 95%, V1 conceded)
- **Target**: Base "Answer" (replace)
- **Rationale**: the coordinator must be "an Orca coordinator session the person opened" (`src/superclaude/core/WORKER-CONTRACT.md:69`); no source says an `--agent` session qualifies. The owner, who owns the rule, can state that a session they launch through Orca and attend counts.
- **Integration point**: Answer sentence gains "provided the owner states in the ledger that this session counts as person-opened".
- **Risk**: Low.

### Change 2: Fallback home if the owner does not make that statement (from Variant 2)
- **Source**: V2 whole proposal; V2 advocate concession 1 and 2
- **Target**: Base, new section "Fallback"
- **Rationale**: C-001, X-001, X-002 went to V2.
- **Integration point**: after "What happens next".
- **Risk**: Low.

### Change 3: Preconditions for the fallback switch (from Variant 3 and orchestrator verification)
- **Source**: V3 advocate weakness 5 of V2 (switch edge case), confirmed 2026-11-14; V2 advocate concession 1 (no switch while staged); V3 advocate weakness 1 of V2 (any plain commit takes the staged ledger)
- **Target**: new "Fallback" section (append)
- **Rationale**: A-001 (95%), A-002 (90%), and the reproduced git abort.
- **Integration point**: three bullets under Fallback.
- **Risk**: Low.

### Change 4: What to do if Orca is unreachable when the owner answers (from Variant 3)
- **Source**: V3 "What happens next" step 2 to 4; A-003 responses
- **Target**: Base "What happens next" (append step)
- **Rationale**: V1 cannot create its home without Orca (V1 concession 2); V3's interim (owner holds the ledger, re-ask trigger) covers the gap without abandoning the answer.
- **Integration point**: final step.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-002, A-001 | V2: ledger staged in the main checkout's index | Staged files travel with a branch switch; base keeps them in a checkout that never switches (unanimous) |
| C-004, A-002 | V2: main checkout becomes the coordinator's | The owner's general workspace would host a second session; base avoids it (unanimous) |
| V3 whole | Defer with no home | Unlocks nothing and keeps grants off disk (X-003); kept only as the interim while Orca is down |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Low | Owner declines the statement | Fallback (Change 2) applies |
| 2 | Low | None (conditional) | Remove section |
| 3 | Low | Switch aborts safely | None needed |
| 4 | Low | Ledger held by hand longer | None needed |

## Review Status
- [x] Auto-approved (default)
- Approved by: auto
- Approval timestamp: 2026-11-14T00:30Z
