# Refactoring Plan (Q25)

## Overview
- Base: Variant 1 (proposal-A)
- Incorporated: Variant 3 (1 change), Variant 2 (1 change), all advocates (1 change), Variant 1 advocate (1 change)
- Changes planned: 4; rejected: 2
- Overall risk: Low (advisory text)
- Merged output: `../merged-proposal.md`

## Planned Changes

### Change 1: named fallback when Orca refuses the second launch, with a stall rule
- Source: Variant 3; Variant 3 advocate Concession 2
- Target: base step 1 and "What stays unresolved"
- Approach: replace "proposal C's route is the natural fallback" with an explicit fallback: if the one-time check shows Orca refuses a second launch in a `worker-start` worktree, PR items switch to one top-level agent per item created with `orca worktree create --base-branch origin/master --agent claude --prompt "<item brief>"` (the spec's own named alternative, line 552), and the coordinator applies a per-item deadline: if no PR exists by then, it makes a read-only check of the worktree and asks the owner (Orca idle notices for such agents are UNVERIFIED).
- Risk: Low

### Change 2: the person's go for the first push in the PR session's conversation
- Source: Variant 2 (C-004 unanimous; A-001)
- Target: base step 2 and step 4
- Approach: insert. Before the first push, the PR session shows the diff and waits for the person's go in its own conversation (which meets `WORKER-CONTRACT.md:240`'s "instruction in its live conversation"); the coordinator's earlier showing (`:244`) stays.
- Risk: Low

### Change 3: name the commit and fix pushes in the grant row; one D3 sentence
- Source: all three advocates (A-001); Variant 1 advocate Concession 3
- Target: base step 2 and "What it costs or risks"
- Approach: insert. `GRANT(<item>,pr-submit)` lists: the commit of the worker's changes (named paths), PR create, the "augment review" re-trigger comment, review-fix commits and pushes made without asking at `--monitor 3`, replies and resolves. The D3 text (or a contract note) states that these are outward actions delegated to the PR session, closing the gap between `WORKER-CONTRACT.md:240,245` and 6.4 rule 14 (merged-requirements.md line 987).
- Risk: Low

### Change 4: reduce the cold-reader cost
- Source: Variant 1 advocate Concession 2 (WC-15 handoff files)
- Target: base step 4 and "What it costs or risks"
- Approach: append. The PR session reads the worker's contract and handoff files before opening the PR.
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, X-003 | V2: owner opens every PR session | Nine owner-attended sessions; owner latency is the program's schedule (line 523); kept as the owner's option, and its authority benefit is partly carried by Change 2 |
| C-002, X-002 | V3 as primary route | Drops brief guard, heartbeats and admitted `worker_done` for the code; kept as the fallback (Change 1) |

## Review Status
Auto-approved (non-interactive), 2026-11-14.
