# Refactoring Plan: Merge into Base (Variant 2, proposal-B)

## Overview
- Base: Variant 2 (proposal-B)
- Incorporating strengths from: Variant 1 (proposal-A), Variant 3 (proposal-C), and the advocates' concessions
- Planned changes: 4
- Risk level: Low (the answer "no" does not change)

## Planned Changes

### Change 1: Guard the uncommitted gap (from Variant 2 advocate concession, A-002)
- **Source**: round1-advocate-2.md, Shared assumption responses, A-002
- **Target**: Base, "What happens next if the owner picks it" (append a bullet) and "What it costs or risks" first bullet (append one sentence)
- **Rationale**: X-002 (60%) and A-002 (90%): the gap is the main weakness of "no"; the orchestrator found no general spec rule preventing cleanup of a worker's worktree before its PR session commits (only line 898 for `issue-409-mvp`, line 1074 on resume)
- **Integration point**: "The coordinator does not remove, clean or reuse a worker's worktree until its PR session has committed the change; this guard is not yet written in the spec as a general rule, so it is recorded in the ledger with Q32's answer."
- **Risk**: Low, additive

### Change 2: Door stays open per Task (from Variant 1, C-003)
- **Source**: Variant 1, "Answer" and "What it unlocks"
- **Target**: Base, "What stays unresolved" (insert a bullet)
- **Rationale**: C-003 unanimous for Variant 1: per-Task owner words are the strict WC-9 fit; the spec's decision-lifetime rule (section 3) lets a changed answer apply later
- **Integration point**: "If the owner later wants a checkpoint commit for one specific Task, that Task can get its own owner sentence and grant, which meets WC-9 strictly."
- **Risk**: Low

### Change 3: Stronger "yes" sentence for reference (from Variant 3, S-002)
- **Source**: round1-advocate-3.md, Concessions (item-list sentence)
- **Target**: Base, "What stays unresolved" (insert a bullet)
- **Rationale**: S-002 unanimous for Variant 3: the question asks for a sentence on a yes
- **Integration point**: "If the owner prefers yes after all, a sentence naming all nine work items (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07) lets each brief quote it unchanged; whether that meets WC-9's 'for that Task' is UNVERIFIED."
- **Risk**: Low

### Change 4: Citation fix (from Variant 1 advocate)
- **Source**: round1-advocate-1.md, Weaknesses identified in Variant 2
- **Target**: Base, "What happens next", second bullet (replace `:42` with `:44`)
- **Rationale**: the quoted sentence is at `WORKER-CONTRACT.md:44`
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001, C-002 | Variant 3: every Task commits under one standing sentence | Unanimous for Variant 2 (90%, 95%): rests on two UNVERIFIED contract readings and adds a review step |
| C-002, X-001 | Variant 1: ask per Task at each dispatch | Up to nine more owner questions under "Owner latency is the real schedule" (95%) |
| C-004 | Variant 3: commit checkpoint for every Task | Addressed instead by Change 1's guard |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 to 4 | Low | Wording only | Revert to base text |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14T00:45:00Z
