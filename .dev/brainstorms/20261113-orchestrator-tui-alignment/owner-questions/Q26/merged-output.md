<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14T00:30Z -->

# Merged answer for Q26: where the coordinator runs and where its ledger is staged

<!-- Source: Base (original, modified) - person-opened condition added per Change 1 -->
## Answer

The owner creates one dedicated program worktree through Orca from `origin/master` with an agent (`orca worktree create --name <name> --base-branch origin/master --agent claude --prompt "<coordinator brief>"`), and that agent is the coordinator; the ledger package is staged in that worktree, on its own branch. This holds provided the owner states in the ledger that a session they launch this way and attend counts as "person-opened" for the worker contract (`src/superclaude/core/WORKER-CONTRACT.md:69`). If the owner will not make that statement, the Fallback below applies.

<!-- Source: Base (original); step 5 merged per Change 4 -->
## What happens next

1. The owner (a person, not a session) runs the create command; no session creates a worktree for its own use.
2. The owner reads the coordinator's first screen to confirm the brief loaded (a launch receipt is not proof).
3. The coordinator writes the ledger package `.dev/tasks/<program-package>/` there, staged and not committed; the worktree never changes branch, so the staged ledger cannot travel to another branch.
4. XC-10 part (3) (the first-wave intake record) records the path from `orca worktree list` and the branch.
5. If Orca does not answer when the owner gives this answer, the answer is still recorded; the owner keeps the ledger by hand, with every grant row the first-wave items need written out in full, and creates the worktree at the first successful Orca read.

<!-- Source: Variant 2 (proposal-B) and Variant 3 (proposal-C) - merged per Changes 2 and 3 -->
## Fallback: the main checkout on a program branch

Used only if the owner does not accept the person-opened statement. The owner switches `/home/coder/workspaces/IronClaude` from `docs/409-orca-dashboard-designs` to a new branch from `origin/master` and opens the coordinator session there by hand. Preconditions and rules:
- Before the switch, 34 untracked files in the main checkout that are identical to tracked files on origin/master (under `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/`, `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/`, `.dev/issues/431/`, `.dev/issues/450/`) must be moved or removed by the owner; otherwise git aborts the switch (checked 2026-11-14 with git 2.47.3; the abort is safe).
- While the ledger is staged and uncommitted, the main checkout does not change branch and receives no other commit (a plain commit there would take the staged ledger with it).
- The owner's other Claude work moves out of the main checkout for the program's life (one live session per checkout, spec 6.2).

<!-- Source: Base (original, modified) -->
## What it unlocks
XC-09 (standing up the coordinator) and every item it dispatches, with the ledger and grant table on disk in a checkout that holds nothing else.

## What it costs or risks
- Rests on the owner's statement about "person-opened"; without it, the Fallback's three rules apply.
- Needs Orca to create the home; until then the ledger is held by hand.
- One more worktree on a host that already has 19.

## What stays unresolved
- The worktree name and branch name (the owner names them).
