# Refactoring Plan: Merge into Base (Variant 3, proposal-C)

## Overview
- Base: Variant 3 (proposal-C)
- Incorporating strengths from: Variant 1 (proposal-A), Variant 2 (proposal-B)
- Planned changes: 3
- Risk level: Low

## Planned Changes

### Change 1: Record that the existing sweep task does not cover SW-02 (from Variant 2)
- **Source**: V2 "Answer" and V2 advocate overall pick
- **Target**: Base "What happens next" step 1 (replace)
- **Rationale**: spec criterion SW-02 (5) "first check whether an adequate existing plan covers SW-02" (`merged-requirements.md:191`); the Done task package does not plan SW-02 (question.md fact 6).
- **Risk**: Low.

### Change 2: Narrow-exception guard (from Variant 1)
- **Source**: V1 "What it unlocks"; V1 advocate overall pick
- **Target**: Base "What it costs or risks" (replace bullet 2 with a rule in "Answer")
- **Rationale**: C-004 went to V1 unanimously; A-004 stays in force for everything else.
- **Risk**: Low.

### Change 3: Files written outside the package and the archive rename (from Variant 3 advocate concessions)
- **Source**: round1-advocate-V3.md Concessions 1 and 2; verified `sc-reflect-protocol/SKILL.md:88`, `:593`
- **Target**: Base "What happens next" step 3 (replace) and "What stays unresolved" (replace)
- **Rationale**: the base said "Nothing material"; two real details remain.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001, C-002, A-002 | V1: plan in the coordinator home | `/sc:implement` refuses a plan from another checkout (`managed-workspace.md:11`) |
| C-003 | V1: wait for Q26 | V3 has no dependency |
| X-003 | V2: task-file phase run by `/task` | level 4 without a stated need (`~/.claude/CLAUDE.md`) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Low | none | remove step |
| 2 | Low | none | remove rule |
| 3 | Low | a reflect file committed by mistake | unstage before commit |

## Review Status
- [x] Auto-approved (default)
- Approved by: auto
- Approval timestamp: 2026-11-14T01:05Z
