# Refactoring Plan: Merge into Base (Variant 1, proposal-A)

## Overview
- Base: Variant 1 (proposal-A)
- Incorporating strengths from: Variant 2 (proposal-B), Variant 3 (proposal-C)
- Planned changes: 5
- Risk level: Low (all add gates or listed writes)

## Planned Changes

### Change 1: Drop the pre-ruling level-1 option (all advocates)
- **Target**: Answer (replace). **Rationale**: X-004 and C-002 (92%, 90%); level 1 sends the INV-008 finding to troubleshoot (`SKILL.md:306`). **Risk**: Low.

### Change 2: Gate on "resolved", not "replied" (all advocates; verified)
- **Target**: Answer and step 3. **Rationale**: A-001; `detection-contract.md:132-136`. **Risk**: Low.

### Change 3: Wait for Codex's review of SW-02's push (from Variant 3)
- **Target**: Answer (insert gate). **Rationale**: A-002 (all REJECT; V3 wins the point); SW-02 changes the git-status code itself. **Risk**: Low; costs time.

### Change 4: Stop rule and PR-open check in the grant row (from Variants 2 and 3, V1 concessions)
- **Target**: step 2. **Rationale**: X-001, A-003; `SKILL.md:309` versus `refs/merge-guard.md:94-97`; owner memory. **Risk**: Low.

### Change 5: List the decline-fallback comment (from Variant 2)
- **Target**: step 2. **Rationale**: `refs/auggie-fallback.md:35`. **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001 | V2: level 2 permanently | Hand pushes lose the tool's head and parent checks (A-003, V1 85%); the extra gate of Change 3 covers the riskiest window |
| C-001 | V3: never | Loses verification and push checks for the whole life of a 1003-file PR; V3 itself asked for a revisit clause |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1-5 | Low | a gate not observed by the session | the grant row is the owner's wording; the session halts on any unlisted write |

## Review Status
- [x] Auto-approved (default). Approved by: auto. Timestamp: 2026-11-14T01:45Z
