# Refactoring Plan: Merge into Base (Variant 1, proposal-A)

## Overview
- Base: Variant 1 (proposal-A)
- Incorporating strengths from: Variant 2 (proposal-B), Variant 3 (proposal-C), and advocates' Round 1 conditions
- Planned changes: 4
- Risk level: Low to Medium (Change 2 adds a condition to the answer)

## Planned Changes

### Change 1: Written brief for the named author (from Variant 2, U-002)
- **Source**: Variant 2, "What happens next" second bullet and "What it unlocks"
- **Target**: Base, "What happens next if the owner picks it" (insert after the first bullet)
- **Rationale**: C-005 unanimous for Variant 2 (90%); Variant 1's advocate conceded "Variant 1 should adopt Variant 2's written brief"
- **Integration point**: "The coordinator gives the named session a short written brief that quotes the 6.3 '#539 author' row, rule 15 (named-path staging), Q28's limits, the A-004 limit (no new key, file or sidecar) and the fork rule (every push and `gh` call to `IronbellyOrg/IronClaude` only). An independent reviewer checks each push against it."
- **Risk**: Low, additive

### Change 2: Condition on role mixing and a fallback (from Variant 2, X-002 debate)
- **Source**: round1-advocate-1.md Concessions; round1-advocate-2.md Position and Concessions
- **Target**: Base, "Answer" (append one sentence) and "What it costs or risks" third bullet (replace)
- **Rationale**: all three advocates flagged evidence that the session dispatching program work runs in this checkout; X-002 60%
- **Integration point**: Answer: "If that session also does program or coordinator work in this checkout, that work moves to the coordinator home (Q26) before the first #539 push; if the owner cannot identify the session, a fresh dedicated top-level session is launched instead (that Orca allows a second launch in this worktree is UNVERIFIED)."
- **Risk**: Medium, adds a condition to the answer

### Change 3: Owner reads each diff before its push grant (middle course, Variant 3)
- **Source**: round1-advocate-1.md Key strengths 5; round1-advocate-3.md Overall
- **Target**: Base, "What happens next" (insert after the push sequence bullet)
- **Rationale**: C-001 unresolved; X-001 Variant 3 minority; two advocates proposed it as the middle course
- **Integration point**: "Before writing each push grant, the owner reads the diff it would publish."
- **Risk**: Low

### Change 4: Record the reading of "tool" (A-001)
- **Source**: diff-analysis A-001; all three advocates
- **Target**: Base, "What stays unresolved" (insert a bullet)
- **Rationale**: A-001 65% for Variant 3's strict-reading concern; all accept the narrow reading with a recorded owner confirmation
- **Integration point**: "The ledger row naming the author records the owner's reading that '6.3: never lets a tool design or push an INV-008 fix' refers to automated tooling such as `/sc:pr-submit`, not the author writing the change the ruling specifies."
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001, X-001 | Variant 3: the owner personally commits and pushes | 2 of 3 advocates and the spec role (6.3: "a top-level session ... because it pushes") favour a session under per-push grants; Change 3 keeps the owner's diff review without the latency |
| X-002 | Variant 2: retire the current session by default | Its own advocate conceded "move its program work", not "retire"; folded into Change 2 as a condition |
| C-002 | Variant 2: always launch fresh | Depends on UNVERIFIED Orca behaviour; kept only as the fallback in Change 2 |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1, 3, 4 | Low | Wording only | Revert to base text |
| 2 | Medium | Adds a precondition to the first push | Remove the appended sentence |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14T01:20:00Z
