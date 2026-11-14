# Refactoring Plan: Merge into Base (Variant 1, proposal-A)

## Overview
- Base: Variant 1 (proposal-A), selected by input order after two tied tiebreaker levels
- Incorporating strengths from: Variant 2 (proposal-B), Variant 3 (proposal-C)
- Planned changes: 4
- Risk level: Medium (Change 1 restructures the base's route)

## Planned Changes

### Change 1: Replace the route with the Coder template (from Variant 2)
- **Source**: V2 Answer and steps 1-2. **Target**: Base Answer and steps (restructure). **Rationale**: C-001 (72%), X-001 (95%), X-003 (92%), C-003 (95%); 2 of 3 overall picks. **Risk**: Medium.

### Change 2: One owner-approved removal of the shadowing install, after the update (from Variant 2 advocate; all advocates agree removal is needed)
- **Target**: new step. **Rationale**: X-002, A-002; `main.tf:594-597` (home persists). **Risk**: Low; ordering avoids a fall-back to the older image revision.

### Change 3: Gate check in the coordinator's own environment (from Variant 2 advocate)
- **Target**: final step. **Rationale**: A-001 unresolved; worktree `.venv/bin/superclaude` exists. **Risk**: Low.

### Change 4: Interim record (from Variant 3)
- **Target**: first step. **Rationale**: V3 advocate pick. **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale |
|---|---|---|
| C-002, C-004 | Keep V1's in-place reinstall for speed and no restart | Requires an exception to the owner's stated rule (X-001, 95%) and turns a stray install into a sanctioned one; speed matters little because XC-04 also waits on Orca being reachable and on Q24 |
| V3 whole | Wait for the template to deliver on its own | Cannot pass on this host while the shadow persists |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | gate waits on the Coder PR and update | none needed |
| 2 | Low | `ic` or a script relied on the user-level install | reinstall from the receipt |
| 3, 4 | Low | none | none |

## Review Status
- [x] Auto-approved (default). Approved by: auto. Timestamp: 2026-11-14T02:30Z
