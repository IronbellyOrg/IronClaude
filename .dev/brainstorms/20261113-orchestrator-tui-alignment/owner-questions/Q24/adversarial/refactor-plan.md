# Refactoring Plan (Q24)

## Overview
- Base: Variant 1 (proposal-A)
- Incorporated: Variant 1 advocate (2 changes), all advocates (1 change), Variant 2 (1 change), Variant 3 (1 change)
- Changes planned: 5; rejected: 2
- Overall risk: Low
- Merged output: `../merged-proposal.md`

## Planned Changes

### Change 1: keep the sweep report before removing the worktree
- Source: Variant 1 advocate Concession 4
- Target: base step 5
- Approach: replace. Before the worktree is removed, the sweep report written under `<root>/.dev/sweeps/` (`sweep/commands.py:235-241`) is copied into the ledger package and the copy path recorded in the XC-04 record.
- Risk: Low

### Change 2: first recorded read settles the shared assumption
- Source: all three advocates (A-001)
- Target: base step 3
- Approach: insert. XC-03's first recorded step is one `orca orchestration worker-list --run <id> --json` read, from the terminal that holds no Run, of a non-empty Run held by another terminal, with `page.total` recorded next to the unscoped count. Reason: Q-1 fenced only the mailbox read `check --all` (`q1-result.md`), not `worker-list`; whether a Run-less terminal can list another terminal's non-empty Run is UNVERIFIED.
- Risk: Low

### Change 3: OB-03 stays with the owner by default
- Source: Variant 2 (C-002; INV-014 authorship)
- Target: base "Answer" and step list
- Approach: replace the vague "owner or a session the owner names" with: the owner runs OB-03 and authors its record, unless the owner names another runner in writing under `GRANT(OB-03,seeded-write)`; the capture session never holds that row.
- Rationale: C-002 unresolved; the only write among the three items and its authored record fit the owner; no advocate argued the capture session should hold it.
- Risk: Low

### Change 4: the 409 session advises, it does not run
- Source: Variant 3 (X-002, familiarity) and Variant 1 advocate Concession 2
- Target: base "What it costs or risks" (cold start) and step 3
- Approach: append. The capture session is handed the observer's verified field list (`src/superclaude/cli/observe/parse.py`) and, if the 409 session is alive, may ask it read-only questions about observer fields; the 409 session runs no live Orca command for these items.
- Risk: Low

### Change 5: note that XC-03 alone needs no worktree
- Source: Variant 1 advocate Concession 5 (merged-requirements.md line 451: "CAP runs no git and no sweep")
- Target: base "What it costs or risks"
- Approach: append. The worktree's cost is earned at XC-04; creating it for XC-03 too keeps one runner and one record.
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001 | V3: the 409 session runs XC-03, OB-03, XC-04 | V1 won 70%; 409 session's survival UNVERIFIED; its worktree is on an unmerged branch and holds evidence that must survive until OB-01 |
| X-001 | V2: no agent holds a live-read row | Unresolved; owner time is the program's bottleneck (merged-requirements.md line 523), and per-item grant rows already narrow agent authority; V2's own advocate chose V1 overall |

## Review Status
Auto-approved (non-interactive), 2026-11-14.
