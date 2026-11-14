# Refactoring Plan: Q5

## Overview
- Base variant: Variant 2 (proposal-B)
- Incorporated from: Variant 3 (re-ask trigger), Variant 1 (caller-side capture as the later path), advocates' additions
- Planned changes: 5
- Overall risk: Low (additive; the answer is unchanged)
- Rule carried: do not claim an orchestrator that manages work, a watcher handoff, the v2 knowledge layer or a TUI decision loop exists.

## Planned Changes

### Change 1: re-ask Q17 once the real-id comparison is recorded
- Source: Variant 3 (U-003); Variant 2 and 3 advocates
- Target: base "What happens next", new step after step 3
- Approach: insert
- Rationale: makes the one open fact (whether the observer's dispatch ids match the sweep's row ids) inform the panel question, without holding the note.
- Risk: Low

### Change 2: name the later path if Q17 becomes "yes"
- Source: Variant 1 (U-001)
- Target: base "What stays unresolved"
- Approach: append
- Rationale: a panel would read a copy captured from the coordinator's at-most-every-5-minutes pass (Q9 caller-side capture), never run the sweep itself (running it writes a report and runs `git status` in every worktree, ADJ Part 8 line 808).
- Risk: Low

### Change 3: the #409 correction pass records the choice
- Source: Variant 1 advocate
- Target: base "What happens next", step 4
- Approach: append
- Rationale: the live #409 body still proposes "one shared set of facts" (body line 55, read 2026-11-14); left alone it contradicts the owner's answer.
- Risk: Low

### Change 4: the mapping table states each program's stale threshold
- Source: Variants 1 and 2 advocates; `merged-requirements.md:1160`
- Target: base "What happens next", step 1 (note content)
- Approach: append clause
- Risk: Low

### Change 5: the draft may need revising before it lands
- Source: Variant 2 advocate concession 3; Variant 3 advocate concession 2
- Target: base "What it costs or risks"
- Approach: append bullet
- Rationale: the comparison test reads constants that exist only on #539's head; the Q1 ruling is expected to change the git allow-list, not the note's contents (keys, shared words, Orca verbs, join basis), which "Add no JSON keys and no files inside #539" (ADJ line 210) keeps stable.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, X-001 | Variant 1: an observer panel on the sweep JSON in version 1 | 3 of 3: reverses three debate verdicts; mixes 5-minute data with 15-second rows; unverified join; no on-screen disagreement exists yet in version 1. Kept as the named later path (Change 2). |
| C-002, X-002 | Variant 3: write nothing yet | 3 of 3: the draft is cheap now and the note is needed under every surviving option; kept only its re-ask trigger (Change 1). |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 to 5 | Low | added steps and notes | revert to `variant-2-original.md` |

## Review Status
- Approval: auto-approved (non-interactive), 2026-11-14
