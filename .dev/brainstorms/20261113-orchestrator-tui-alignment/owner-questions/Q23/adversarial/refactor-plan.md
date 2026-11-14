# Refactoring Plan (Q23)

## Overview
- Base: Variant 3 (proposal-C)
- Incorporated: Variant 2 (2 changes), Variant 1 (2 changes)
- Changes planned: 4; rejected: 2
- Overall risk: Low
- Merged output: `../merged-proposal.md`

## Planned Changes

### Change 1: write the observed facts into the row, as observations
- Source: Variant 2 advocate (fixture evidence), verified by the orchestrator
- Target: base step 1
- Approach: append. The row adds: "In the observer's recorded fixture (`src/superclaude/cli/observe/fixtures/golden-success.json`, one redacted live worker-list read), all 9 reclaimable workers had a finished task (`workerState: succeeded`, `outcome: succeeded`), resources still held (`ownershipState: owned`, `releaseState: not_requested`), next action `release`, and liveness `unverifiable`. This is one sample, not Orca's definition."
- Risk: Low

### Change 2: named reopen step with an owner and wave
- Source: Variant 3 advocate Concession 3; Variant 2 advocate concession
- Target: base step 4
- Approach: replace. The session that runs the shared read-only capture (XC-03, the session Q24 names, wave W1) adds two read-only items: Orca's help text for terminal states and one detail read (`worker-show`) of one reclaimable worker, recording whether its session has exited and whether release is automatic or done by a person.
- Risk: Low

### Change 3: what the reopen decides
- Source: Variant 1 and Variant 2 (conditional outcome)
- Target: base "What it unlocks"
- Approach: append. If the capture shows the session exited and release is automatic, the follow-up is variant 1 (hide with historical, small observer change); if release needs a person, the follow-up is variant 2's wording "not historical: awaiting release", never "live". Either is a separate owner answer.
- Risk: Low

### Change 4: related states and the sweep's different words
- Source: Variant 1 ("What stays unresolved", U-001); Variant 3 advocate Concession 4
- Target: base step 1 and "What stays unresolved"
- Approach: append. The same "own state, Orca's word" rule covers `release_pending` and `release_unknown`; the note states that the sweep's "historical" (6 h window) and "settled" (`outcome`) are different measures from the observer's terminal-state rule.
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002, X-003 | V1: add `reclaimable` to `HISTORICAL_STATES` now | Hides a possibly running worker before Orca's meaning is known (A-001); kept as a conditional follow-up |
| C-001 | V2: record "not historical" as final now | Rests on one fixture; kept as a conditional follow-up wording |

## Out-of-scope observation (not merged)
2 `retained` rows in the same fixture have `workerState: ready`, `dispatchStatus: dispatched`; the observer hides `retained` by default (`view.py:35`). Logged for follow-up in final.md, not part of Q23.

## Review Status
Auto-approved (non-interactive), 2026-11-14.
