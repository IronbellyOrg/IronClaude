# Refactoring Plan (Q21)

## Overview
- Base: Variant 2 (proposal-B)
- Incorporated: Variant 1 (1 change), Variant 3 (3 changes)
- Changes planned: 4; rejected: 3
- Overall risk: Low (additive wording to an advisory proposal)
- Merged output: `../merged-proposal.md`

## Planned Changes

### Change 1: name the watcher store as the fallback signal, not a new input now
- Source: Variant 1, "Answer" and round1-advocate-V1.md Strength 1 and Concession 1
- Target: base "What stays unresolved" and step 3
- Approach: insert. If FU-1 shows Orca's agent rows carry no usable signal, SW-10 records "no reliable signal" and the reopen option is a label from the watcher's versioned store `dispatch.json` (`operation_id`, `launch_cwd`, checked `schema_version`: `record.py:69-95`), which would need its own owner approval of a file read. Not `status --json` (lacks launched sessions' ids: `cycle.py:1308-1323`). No worktree-path fallback.
- Rationale: X-001 won by V1 (68%); V1 and V2 advocates agreed on this synthesis.
- Risk: Low

### Change 2: document the blind spot now
- Source: Variant 3, step 2
- Target: base step 1
- Approach: append. Until SW-10 lands, the sweep design and the contract-note draft say that a Run-less session may have been started by the watcher and the sweep cannot tell (ADJ lines 227, 242).
- Rationale: V3 Strength 6; no advocate opposed.
- Risk: Low

### Change 3: guard against a signal that holds on one row and drifts later
- Source: Variant 3, round1-advocate-V3.md Weaknesses 1 and 2
- Target: base step 3
- Approach: insert. The label may only move a row from "unknown" to "machine-started"; a row whose signal is missing or unrecognised stays "could not determine", never person-started. The fixture test also covers an empty `prompt`.
- Rationale: A-001 and X-001 discussion (one FU-1 row is a sample of one; A-009 build drift).
- Risk: Low

### Change 4: WA-07 dependency note
- Source: Variant 3, round1-advocate-V3.md Concession 1
- Target: base "What it unlocks"
- Approach: append. If SW-10 ends in "no reliable signal", WA-07 item (3) uses its other route ("bound to a Run"); the dependency row is updated then.
- Rationale: C-004 discussion.
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002, X-002 | V1: widen the allow-list or add a file read now | Won by V2 (85%); adds a cross-program input before any evidence |
| C-005 | V1: worktree-path fallback | Unanimous: errs in the unsafe direction (person session labelled machine) |
| C-003 | V3: defer until SW-13 | V2 won unanimously (92%): concrete trigger; SW-13 has no date |

## Risk Summary
All changes are additive wording; rollback = drop the added sentences.

## Review Status
Auto-approved (non-interactive), 2026-11-14.
