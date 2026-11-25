# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (keep Task sub-agents), file `variant-1-original.md`
- Incorporating strengths from: Variant B, plus debate findings A-001 to A-004
- Planned changes: 5
- Risk level: Low (all changes are text edits to a recommendation document; nothing in the repo is changed)

## Planned Changes

### Change 1: Replace the "keep Task" rationale with the layering rule (from debate A-004, C-003)
- **Source**: Debate A-004; `~/.claude/WORKER-CONTRACT.md` WC-7, WC-8, WC-13
- **Target**: Base "Claim" and "Case" point 3 (replace)
- **Rationale**: Both advocates REJECT A-004 at 90%. "Two dispatch paths forever" is void because the skill would hold no Orca code. The real reason not to refactor is that WC-8 forbids it.
- **Integration point**: Open the document with the layering rule: Task fan-out stays in the command, Orca fan-out belongs to the coordinator.
- **Risk**: Low, wording only

### Change 2: Add the coordinator-level path for B's goals (from B, C-006/C-007/C-008, A-001)
- **Source**: Variant B points 2, 3, 4; debate A-001 (agreed 80%)
- **Target**: Base, new section "Where B's benefits are available without refactoring" (append)
- **Rationale**: Observability, isolation and resume arrive when a coordinator runs one `/sc:brainstorm --unattended` worker per Task. Retries are new Tasks per WC-6, not `--retry-of`.
- **Integration point**: New section after the Case list
- **Risk**: Medium, depends on the `--unattended` section being present in the source `brainstorm.md`, which this branch lacks (UNVERIFIED on master)

### Change 3: Replace the cross-family diversity item with the two real routes (C-004, unresolved)
- **Source**: Variant A point 6; Variant B point 1; debate C-004
- **Target**: Base point 6 (replace)
- **Rationale**: C-004 stayed open (lean A). Route 1: `sc-bare-review` (no Orca; proposal generation UNVERIFIED, it is described as reviews). Route 2: a coordinator runs one worker per model family and then `/sc:adversarial --compare`; whether a non-Claude worker can run `/sc:` commands is UNVERIFIED.
- **Integration point**: Same position as base point 6
- **Risk**: Medium, two unverified premises are labelled as such

### Change 4: Add a cost-measurement gate (from debate A-003)
- **Source**: Debate A-003 (agreed 80%)
- **Target**: Base "What to do instead" (append)
- **Rationale**: Neither variant has latency or cost numbers; measure worker cold-start before any decision to use workers for brainstorm.
- **Integration point**: Last bullet
- **Risk**: Low

### Change 5: Record rejected claims from B and the verified spec defects (X-001, X-002, U-001)
- **Source**: Debate X-001, X-002; Variant A U-001
- **Target**: Base, new table "Claims rejected"
- **Rationale**: Keep a record of why B's points fail: X-001 (single-advocate retry exists), X-002 (the skill runs in-session), `--retry-of` (WC-6).
- **Integration point**: End of document
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|----------------------------|
| B point 6 | `--runtime orca` flag on S2 | Violates WC-8 and WC-13 (A-004, 90%) |
| B point 5 / U-006 | Merge enrichment into the proposer | Low value; touches the same forbidden mechanism |
| B point 4 | `--resume-from` reattaches to proposals | `--resume-from` resumes only the seed brief today; WC-6 handles retries as new Tasks |
| B mitigation | Token accounting by transcript size | Does not satisfy the 1.25x kill rule (C-005, 78%) |
| C-002, C-008, C-009 | Open points | Not decisive; recorded as unresolved |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Wrong reason given | Revert to base point 3 |
| 2 | Medium | Recommends a route not yet in source | Remove section; the installed copy still has the section |
| 3 | Medium | Unverified premises mislead | Keep labels; remove route |
| 4 | Low | None | Remove bullet |
| 5 | Low | None | Remove table |

## Review Status
- [x] Auto-approved (default)
- Approved by: auto
- Approval timestamp: 2026-11-11T21:20:00Z
